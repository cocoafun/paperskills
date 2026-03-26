# Installing PaperSkills for Cursor

Guide for using PaperSkills with Cursor through project rules.

## Quick Install

Tell Cursor:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.cursor/INSTALL.md
```

## Manual Installation

Cursor does not currently load `SKILL.md` repositories as native skills. The practical setup is:

1. Put the PaperSkills repo inside your project so Cursor can read it.
2. Add a Cursor Rule that tells the agent when to consult `paperskills/SKILL.md`.

### Steps

Clone the repo into your project-local `.cursor` directory:

```bash
git clone https://github.com/cocoafun/paperskills.git .cursor/paperskills
```

Create the rules directory:

```bash
mkdir -p .cursor/rules
```

Then create `.cursor/rules/paperskills.mdc` with the following content:

```md
---
description: Use PaperSkills for academic research, literature search, research gaps, citation verification, peer review, journal matching, paper tracking, and abstract writing.
globs:
alwaysApply: false
---

When the user asks for an academic paper or literature workflow task, first read `.cursor/paperskills/SKILL.md`.

Use `.cursor/paperskills/SKILL.md` as the router:
- topic framing -> `.cursor/paperskills/skills/topic-framing/SKILL.md`
- abstract writing -> `.cursor/paperskills/skills/abstract/SKILL.md`
- literature search -> `.cursor/paperskills/skills/lit-search/SKILL.md`
- citation verification -> `.cursor/paperskills/skills/cite-verify/SKILL.md`
- citation network -> `.cursor/paperskills/skills/citation-network/SKILL.md`
- research gap analysis -> `.cursor/paperskills/skills/research-gap/SKILL.md`
- peer review -> `.cursor/paperskills/skills/peer-review/SKILL.md`
- journal matching -> `.cursor/paperskills/skills/journal-match/SKILL.md`
- paper tracking -> `.cursor/paperskills/skills/paper-tracker/SKILL.md`

Do not load every sub-skill up front. Read only the skill needed for the current task.
```

Open a new Cursor Agent chat after creating the rule.

## Updating

```bash
cd .cursor/paperskills && git pull
```

Update the rule only if you want to change routing behavior.

## Troubleshooting

### Cursor is not using PaperSkills

1. Check the repo exists at `.cursor/paperskills`
2. Check the rule exists at `.cursor/rules/paperskills.mdc`
3. Start a fresh Agent chat so the new rule is loaded

### Cursor reads too many skill files

Keep the rule scoped to the router and tell Cursor to load only the sub-skill needed for the current task.
