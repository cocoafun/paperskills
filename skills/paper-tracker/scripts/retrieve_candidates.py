#!/usr/bin/env python3
"""Retrieve candidate papers from a unified search brief."""

from __future__ import annotations

import argparse
import re
from typing import Any

from paper_tracker_lib import (
    authors_from_crossref,
    best_publication_date,
    dump_json,
    http_get_json,
    load_json,
    normalize_window,
    read_registry,
    within_window,
)


def brief_topics(brief: dict[str, Any]) -> list[str]:
    filters = brief.get("filters", {})
    topics = filters.get("topics", [])
    domain = filters.get("domain")
    if domain and not topics:
        topics = [domain, *topics]
    return [topic for topic in topics if topic]


def author_name_matches(author_query: str, candidate_names: list[str]) -> bool:
    cleaned = [token for token in re.findall(r"[a-z0-9]+", author_query.lower()) if len(token) > 1]
    if not cleaned:
        return False
    family = cleaned[-1]
    givens = cleaned[:-1]
    for candidate in candidate_names:
        candidate_tokens = re.findall(r"[a-z0-9]+", candidate.lower())
        if family not in candidate_tokens:
            continue
        if not givens:
            return True
        if any(any(token.startswith(given) or given.startswith(token) for token in candidate_tokens) for given in givens):
            return True
    return False


def resolve_journals(brief: dict[str, Any]) -> list[dict[str, Any]]:
    filters = brief.get("filters", {})
    registry_rows = read_registry(brief.get("registry_path"))
    registry_map = {row["journal"].lower(): row for row in registry_rows}
    resolved = []
    for journal in filters.get("journals", []):
        row = registry_map.get(journal.lower())
        if row:
            resolved.append(row)
    return resolved


def crossref_record(item: dict[str, Any], strategy: str, matched_on: str) -> dict[str, Any]:
    published_at, date_source = best_publication_date(item)
    doi = item.get("DOI")
    link = f"https://doi.org/{doi}" if doi else ""
    return {
        "title": ((item.get("title") or [""])[0]).strip(),
        "authors": authors_from_crossref(item),
        "journal": ((item.get("container-title") or [""])[0]).strip(),
        "published_at": published_at,
        "date_source": date_source,
        "doi": doi,
        "url": link,
        "abstract": item.get("abstract"),
        "crossref_type": item.get("type"),
        "source": "crossref",
        "retrieval_strategy": strategy,
        "matched_on": matched_on,
    }


def openalex_record(item: dict[str, Any], strategy: str, matched_on: str) -> dict[str, Any]:
    doi = item.get("doi") or ""
    if doi.startswith("https://doi.org/"):
        doi = doi.replace("https://doi.org/", "", 1)
    return {
        "title": item.get("title", "").strip(),
        "authors": [authorship["author"]["display_name"] for authorship in item.get("authorships", [])],
        "journal": ((item.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
        "published_at": item.get("publication_date"),
        "date_source": "publication_date" if item.get("publication_date") else None,
        "doi": doi or None,
        "url": item.get("primary_location", {}).get("landing_page_url") or item.get("id"),
        "abstract": None,
        "crossref_type": "journal-article" if item.get("type") == "article" else item.get("type"),
        "source": "openalex",
        "retrieval_strategy": strategy,
        "matched_on": matched_on,
    }


def crossref_window_filter(window: dict[str, str]) -> str:
    return ",".join(
        [
            f"from-pub-date:{window['from']}",
            f"until-pub-date:{window['to']}",
        ]
    )


def fetch_by_journal(journal: dict[str, Any], window: dict[str, str], rows: int) -> list[dict[str, Any]]:
    records = []
    for issn in journal.get("issns", []):
        payload = http_get_json(
            f"https://api.crossref.org/journals/{issn}/works",
            {
                "rows": rows,
                "filter": crossref_window_filter(window),
                "sort": "published",
                "order": "desc",
            },
        )
        items = payload.get("message", {}).get("items", [])
        for item in items:
            records.append(crossref_record(item, "journal", journal["journal"]))
    return records


def fetch_by_author(author: str, window: dict[str, str], rows: int) -> list[dict[str, Any]]:
    try:
        payload = http_get_json(
            "https://api.crossref.org/works",
            {
                "query.author": author,
                "rows": rows,
                "sort": "published",
                "order": "desc",
                "filter": crossref_window_filter(window),
            },
        )
        items = payload.get("message", {}).get("items", [])
        records = [crossref_record(item, "author", author) for item in items]
        strong_matches = [
            record for record in records if author_name_matches(author, record.get("authors", []))
        ]
        if strong_matches:
            return strong_matches
    except RuntimeError:
        pass
    author_search = http_get_json(
        "https://api.openalex.org/authors",
        {
            "search": author,
            "per-page": 5,
        },
    )
    author_results = author_search.get("results", [])
    if not author_results:
        return []
    selected = None
    for candidate in author_results:
        if candidate.get("display_name", "").lower() == author.lower():
            selected = candidate
            break
    selected = selected or author_results[0]
    works = http_get_json(
        "https://api.openalex.org/works",
        {
            "filter": ",".join(
                [
                    f"author.id:{selected['id']}",
                    f"from_publication_date:{window['from']}",
                    f"to_publication_date:{window['to']}",
                ]
            ),
            "sort": "publication_date:desc",
            "per-page": rows,
        },
    )
    return [openalex_record(item, "author", author) for item in works.get("results", [])]


def fetch_by_topic(topic: str, window: dict[str, str], rows: int) -> list[dict[str, Any]]:
    payload = http_get_json(
        "https://api.crossref.org/works",
        {
            "query.bibliographic": topic,
            "rows": rows,
            "sort": "published",
            "order": "desc",
            "filter": crossref_window_filter(window),
        },
    )
    items = payload.get("message", {}).get("items", [])
    return [crossref_record(item, "topic", topic) for item in items]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", required=True, help="Path to search brief JSON")
    parser.add_argument("--rows-per-source", type=int, default=25)
    args = parser.parse_args()

    brief = load_json(args.brief)
    window = normalize_window(brief["window"])
    filters = brief.get("filters", {})

    candidates: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []

    for journal in resolve_journals(brief):
        records = fetch_by_journal(journal, window, args.rows_per_source)
        candidates.extend(records)
        coverage.append(
            {
                "type": "journal",
                "value": journal["journal"],
                "source": "crossref-journal-endpoint",
                "count": len(records),
            }
        )

    for author in filters.get("authors", []):
        records = fetch_by_author(author, window, args.rows_per_source)
        candidates.extend(records)
        source_name = "crossref-query.author"
        if records and records[0].get("source") == "openalex":
            source_name = "openalex-author-fallback"
        coverage.append(
            {
                "type": "author",
                "value": author,
                "source": source_name,
                "count": len(records),
            }
        )

    for topic in brief_topics(brief):
        records = fetch_by_topic(topic, window, args.rows_per_source)
        candidates.extend(records)
        coverage.append(
            {
                "type": "topic",
                "value": topic,
                "source": "crossref-query.bibliographic",
                "count": len(records),
            }
        )

    filtered = [
        record for record in candidates if within_window(record.get("published_at"), window)
    ]

    dump_json(
        {
            "brief": brief,
            "normalized_window": window,
            "candidate_count": len(filtered),
            "coverage": coverage,
            "candidates": filtered,
        }
    )


if __name__ == "__main__":
    main()
