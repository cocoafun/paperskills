#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


FRONTMATTER_PATTERN = re.compile(r"---\n(.*?)\n---\n", re.S)


def parse_frontmatter(text):
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise ValueError("SKILL.md missing valid frontmatter")

    frontmatter = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter


def build_agents_md(skills_root: Path):
    skill_entries = []
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        frontmatter = parse_frontmatter(skill_md.read_text())
        name = frontmatter.get("name", skill_md.parent.name)
        description = frontmatter.get("description", "Use when relevant.")
        skill_entries.append(f"- {name}: {description} (file: {skill_md})")

    skills_block = "\n".join(skill_entries)
    return f"""## Skills
A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. Below is the list of skills that can be used. Each entry includes a name, description, and file path so you can open the source for full instructions when using a specific skill.
### Available skills
{skills_block}
### How to use skills
- Discovery: The list above is the skills available in this session (name + description + file path). Skill bodies live on disk at the listed paths.
- Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown above, you must use that skill for that turn. Multiple mentions mean use them all. Do not carry skills across turns unless re-mentioned.
- Missing/blocked: If a named skill isn't in the list or the path can't be read, say so briefly and continue with the best fallback.
- How to use a skill (progressive disclosure):
  1) After deciding to use a skill, open its `SKILL.md`. Read only enough to follow the workflow.
  2) When `SKILL.md` references relative paths (e.g., `scripts/foo.py`), resolve them relative to the skill directory listed above first, and only consider other paths if needed.
  3) If `SKILL.md` points to extra folders such as `references/`, load only the specific files needed for the request; don't bulk-load everything.
  4) If `scripts/` exist, prefer running or patching them instead of retyping large code blocks.
  5) If `assets/` or templates exist, reuse them instead of recreating from scratch.
- Coordination and sequencing:
  - If multiple skills apply, choose the minimal set that covers the request and state the order you'll use them.
  - Announce which skill(s) you're using and why (one short line). If you skip an obvious skill, say why.
- Context hygiene:
  - Keep context small: summarize long sections instead of pasting them; only load extra files when needed.
  - Avoid deep reference-chasing: prefer opening only files directly linked from `SKILL.md` unless you're blocked.
  - When variants exist (frameworks, providers, domains), pick only the relevant reference file(s) and note that choice.
- Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best approach, and continue.
"""


def main():
    parser = argparse.ArgumentParser(description="Render AGENTS.md from a skills directory.")
    parser.add_argument("--skills-root", required=True, help="Path to the skills root")
    parser.add_argument("--output", required=True, help="Output AGENTS.md path")
    args = parser.parse_args()

    skills_root = Path(args.skills_root).resolve()
    output = Path(args.output).resolve()
    output.write_text(build_agents_md(skills_root))


if __name__ == "__main__":
    main()
