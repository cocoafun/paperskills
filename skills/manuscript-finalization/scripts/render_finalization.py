#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def render(brief: dict) -> str:
    required_sections = "\n".join(
        f"- {section}: [present / missing]"
        for section in brief.get("required_sections", [])
    ) or "- [Add required sections]"

    unresolved = "\n".join(
        f"- {item}" for item in brief.get("unresolved_gaps", [])
    ) or "- None listed"

    return f"""# {brief.get("paper_title", "[Final Manuscript Title]")}

**Target Artifact**: {brief.get("target_artifact", "submission-ready manuscript")}  
**Completion Standard**: {brief.get("completion_standard", "submission-ready")}  
**Manuscript Type**: {brief.get("manuscript_type", "conceptual-paper")}  
**Draft Status**: {brief.get("draft_status", "working-draft")}  
**Language**: {brief.get("language", "zh-CN")}  
**Citation Style**: {brief.get("citation_style", "GB/T 7714")}  
**Evidence Status**: {brief.get("evidence_status", "unknown")}

## Required Sections

{required_sections}

## Unresolved Gaps

{unresolved}

## Finalization Notes

- Replace checklist markers with manuscript-specific completion notes.
- Do not mark the manuscript as final until placeholders and unsupported claims are removed.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a PaperSkills manuscript finalization scaffold.")
    parser.add_argument("--brief", required=True, help="Path to a finalization brief JSON file.")
    parser.add_argument("--output", required=True, help="Path to the markdown output file.")
    args = parser.parse_args()

    brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))
    Path(args.output).write_text(render(brief), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
