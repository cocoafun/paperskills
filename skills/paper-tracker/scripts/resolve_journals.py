#!/usr/bin/env python3
"""Resolve journal names to stable identifiers."""

from __future__ import annotations

import argparse
from typing import Any

from paper_tracker_lib import dump_json, http_get_json, read_registry


def resolve_from_crossref(journal_name: str) -> dict[str, Any]:
    payload = http_get_json(
        "https://api.crossref.org/journals",
        {"query": journal_name, "rows": 5},
    )
    items = payload.get("message", {}).get("items", [])
    for item in items:
        title = (item.get("title") or "").strip()
        if title.lower() == journal_name.lower():
            return {
                "journal": journal_name,
                "issns": item.get("ISSN", []),
                "publisher_hint": item.get("publisher", ""),
                "source": "crossref",
                "confidence": "high",
            }
    if items:
        item = items[0]
        return {
            "journal": journal_name,
            "issns": item.get("ISSN", []),
            "publisher_hint": item.get("publisher", ""),
            "source": "crossref",
            "confidence": "medium",
            "matched_title": item.get("title", ""),
        }
    return {
        "journal": journal_name,
        "issns": [],
        "publisher_hint": "",
        "source": "crossref",
        "confidence": "none",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", help="Markdown registry file", default=None)
    parser.add_argument("journals", nargs="+")
    args = parser.parse_args()

    registry_rows = read_registry(args.registry)
    registry_map = {row["journal"].lower(): row for row in registry_rows}

    resolved = []
    for journal in args.journals:
        row = registry_map.get(journal.lower())
        if row:
            resolved.append(
                {
                    **row,
                    "source": "registry",
                    "confidence": "high",
                }
            )
            continue
        resolved.append(resolve_from_crossref(journal))

    dump_json({"journals": resolved})


if __name__ == "__main__":
    main()
