#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Render a revision brief into markdown.")
    parser.add_argument("--brief", required=True, help="Path to revision brief JSON")
    parser.add_argument("--output", required=True, help="Output markdown path")
    args = parser.parse_args()

    brief = json.loads(Path(args.brief).read_text())
    rows = []
    for comment in brief.get("comments", []):
        text = comment.get("text", "").replace("|", "/")
        rows.append(
            f"| {comment.get('id', 'TBD')} | {comment.get('severity', 'unknown')} | "
            f"{comment.get('source', 'unknown')} | {text} |"
        )
    table = "\n".join(rows) if rows else "| TBD | TBD | TBD | TBD |"
    constraints = "\n".join(f"- {item}" for item in brief.get("constraints", [])) or "- None"

    markdown = f"""# Revision Plan

**Manuscript Status**: {brief.get("manuscript_status", "unknown")}  
**Target Venue**: {brief.get("target_venue", "unspecified")}  
**Deadline**: {brief.get("deadline", "unspecified")}

## Comments

| ID | Severity | Source | Comment |
| --- | --- | --- | --- |
{table}

## Constraints

{constraints}
"""

    Path(args.output).write_text(markdown)


if __name__ == "__main__":
    main()
