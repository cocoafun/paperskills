#!/usr/bin/env python3
"""Dedupe and rank retrieved candidate papers."""

from __future__ import annotations

import argparse
from typing import Any

from paper_tracker_lib import dump_json, load_json, title_key


NONRESEARCH_TERMS = [
    "call for papers",
    "editorial",
    "foreword",
    "corrigendum",
    "erratum",
    "book review",
    "introduction",
]


def is_nonresearch(paper: dict[str, Any]) -> bool:
    title = (paper.get("title") or "").lower()
    if any(term in title for term in NONRESEARCH_TERMS):
        return True
    return paper.get("crossref_type") != "journal-article"


def is_preprint(paper: dict[str, Any]) -> bool:
    journal = (paper.get("journal") or "").lower()
    url = (paper.get("url") or "").lower()
    paper_type = (paper.get("crossref_type") or "").lower()
    return "arxiv" in journal or "arxiv.org" in url or paper_type == "posted-content"


def score_paper(paper: dict[str, Any], brief: dict[str, Any]) -> int:
    score = 0
    if paper.get("abstract"):
        score += 2
    if paper.get("date_source") in {"published-online", "published-print", "issued"}:
        score += 2
    filters = brief.get("filters", {})
    journal_names = {name.lower() for name in filters.get("journals", [])}
    if paper.get("journal", "").lower() in journal_names:
        score += 3
    matched_on = (paper.get("matched_on") or "").lower()
    for author in filters.get("authors", []):
        if author.lower() in matched_on:
            score += 2
    for topic in filters.get("topics", []):
        if topic.lower() in matched_on:
            score += 2
    if paper.get("published_at"):
        score += 1
    return score


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to raw candidate JSON")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    payload = load_json(args.input)
    brief = payload.get("brief", {})
    limit = args.limit or int(brief.get("limit", 10))

    deduped: dict[str, dict[str, Any]] = {}
    excluded = []
    include_preprints = bool(brief.get("include_preprints", False))
    for paper in payload.get("candidates", []):
        if not include_preprints and is_preprint(paper):
            excluded.append(
                {
                    "title": paper.get("title"),
                    "reason": "preprint",
                    "matched_on": paper.get("matched_on"),
                }
            )
            continue
        if is_nonresearch(paper):
            excluded.append(
                {
                    "title": paper.get("title"),
                    "reason": "nonresearch",
                    "matched_on": paper.get("matched_on"),
                }
            )
            continue
        key = paper.get("doi") or title_key(paper.get("title", ""))
        existing = deduped.get(key)
        if not existing or score_paper(paper, brief) > score_paper(existing, brief):
            deduped[key] = paper

    ranked = sorted(
        deduped.values(),
        key=lambda paper: (
            score_paper(paper, brief),
            paper.get("published_at") or "",
        ),
        reverse=True,
    )

    dump_json(
        {
            "brief": brief,
            "normalized_window": payload.get("normalized_window"),
            "coverage": payload.get("coverage", []),
            "shortlist": ranked[:limit],
            "full_list": ranked,
            "excluded": excluded,
        }
    )


if __name__ == "__main__":
    main()
