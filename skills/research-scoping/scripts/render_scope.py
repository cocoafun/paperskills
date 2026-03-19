#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def bullet_lines(items):
    return "\n".join(f"- {item}" for item in items) if items else "- None"


def numbered_lines(items):
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, start=1)) if items else "1. TBD"


def main():
    parser = argparse.ArgumentParser(description="Render a scoping brief into markdown.")
    parser.add_argument("--brief", required=True, help="Path to scoping brief JSON")
    parser.add_argument("--output", required=True, help="Output markdown path")
    args = parser.parse_args()

    brief = json.loads(Path(args.brief).read_text())
    time_window = brief.get("time_window", {})
    if time_window:
        time_label = f"{time_window.get('from_year', '?')}-{time_window.get('to_year', '?')}"
    else:
        time_label = "Not specified"

    markdown = f"""# {brief.get("topic", "Scoping Brief")}

**Topic**: {brief.get("topic", "TBD")}  
**Objective**: {brief.get("objective", "TBD")}  
**Target Artifact**: {brief.get("target_artifact", "research brief")}  
**Language**: {brief.get("language", "en")}  
**Domain**: {brief.get("domain", "unspecified")}  
**Time Window**: {time_label}  
**Recommended Next Skill**: {brief.get("next_skill", "TBD")}

## 1. Core Research Questions

{numbered_lines(brief.get("questions", []))}

## 2. Keyword Clusters

{bullet_lines(brief.get("keywords", []))}

## 3. In Scope

{bullet_lines(brief.get("in_scope", []))}

## 4. Out of Scope

{bullet_lines(brief.get("out_of_scope", []))}
"""

    Path(args.output).write_text(markdown)


if __name__ == "__main__":
    main()
