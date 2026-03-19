---
name: writing-paperskills
description: Use when creating new PaperSkills skills, editing existing ones, or aligning skill design with the repository's workflow, schema, and evidence-discipline conventions.
---

# Writing PaperSkills

Use this skill when extending the PaperSkills library.

Read [references/skill-authoring-checklist.md](references/skill-authoring-checklist.md) for repository-specific authoring rules.

## Design rules

- Write descriptions as trigger conditions, not workflow summaries.
- Every skill should state when to use it and when not to use it.
- Prefer structured brief contracts over loose narrative inputs.
- Make evidence boundaries explicit.
- Keep skills portable across agent environments.

## Minimum structure

Each skill should define:

- triggering conditions
- exclusions
- required inputs
- core workflow
- required outputs
- guardrails

## Repository fit

New skills should fit one of three layers:

1. entry layer
2. orchestration layer
3. execution layer

If the skill does not fit one of these layers, reconsider whether it belongs in PaperSkills.
