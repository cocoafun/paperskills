#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def bullet_lines(items):
    return "\n".join(f"- {item}" for item in items) if items else "- None"


def render_section(section):
    return f"""## {section.get("name", "Section")}

**Goal**: {section.get("goal", "TBD")}

### Claims

{bullet_lines(section.get("claims", []))}

### Evidence

{bullet_lines(section.get("evidence", []))}
"""


def main():
    parser = argparse.ArgumentParser(description="Render a draft brief into markdown.")
    parser.add_argument("--brief", required=True, help="Path to draft brief JSON")
    parser.add_argument("--output", required=True, help="Output markdown path")
    args = parser.parse_args()

    brief = json.loads(Path(args.brief).read_text())
    sections = "\n\n".join(render_section(section) for section in brief.get("sections", []))

    markdown = f"""# {brief.get("paper_goal", "Paper Draft")}

**Audience**: {brief.get("audience", "unspecified")}  
**Venue Target**: {brief.get("venue_target", "unspecified")}  
**Language**: {brief.get("language", "en")}  
**Citation Style**: {brief.get("citation_style", "APA")}

{sections}
"""

    Path(args.output).write_text(markdown)


if __name__ == "__main__":
    main()
