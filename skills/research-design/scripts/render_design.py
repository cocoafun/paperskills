#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def bullet_lines(items):
    return "\n".join(f"- {item}" for item in items) if items else "- None"


def numbered_lines(items):
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, start=1)) if items else "1. TBD"


def main():
    parser = argparse.ArgumentParser(description="Render a design brief into markdown.")
    parser.add_argument("--brief", required=True, help="Path to design brief JSON")
    parser.add_argument("--output", required=True, help="Output markdown path")
    args = parser.parse_args()

    brief = json.loads(Path(args.brief).read_text())

    markdown = f"""# {brief.get("topic", "Research Design")}

**Topic**: {brief.get("topic", "TBD")}  
**Target Contribution**: {brief.get("target_contribution", "TBD")}  
**Theory Lens**: {brief.get("theoretical_lens", "Not specified")}

## 1. Research Questions

{numbered_lines(brief.get("research_questions", []))}

## 2. Hypotheses or Propositions

{bullet_lines(brief.get("hypotheses", []))}

## 3. Candidate Methods

{bullet_lines(brief.get("method_candidates", []))}

## 4. Data Sources

{bullet_lines(brief.get("data_sources", []))}

## 5. Constraints

{bullet_lines(brief.get("constraints", []))}
"""

    Path(args.output).write_text(markdown)


if __name__ == "__main__":
    main()
