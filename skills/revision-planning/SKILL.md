---
name: revision-planning
description: Use when the user has review comments, internal critique, or rebuttal feedback and needs a structured revision plan, response strategy, and prioritized task list.
---

# Revision Planning

Turn review feedback into an actionable revision roadmap.

Read [references/brief-schema.md](references/brief-schema.md) for the normalized revision brief shape.
Read [references/revision-playbook.md](references/revision-playbook.md) for issue breakdown and prioritization rules.
Use [assets/revision_template.md](assets/revision_template.md) when you want a manual revision plan scaffold.
Use [examples/reviewer-comments-brief.json](examples/reviewer-comments-brief.json) as a starter example.

## Brief-first execution

When local files are useful, prefer this pipeline:

1. Build a JSON brief following [references/brief-schema.md](references/brief-schema.md).
2. Render a starter markdown file:

```bash
python3 skills/revision-planning/scripts/render_revision.py \
  --brief skills/revision-planning/examples/reviewer-comments-brief.json \
  --output revision_plan.md
```

3. Replace the starter content with paper-specific actions and response strategy.

## Use this skill when

- The user has reviewer comments and needs a response plan.
- The user wants to prioritize revisions before resubmission.
- The user wants a rebuttal-oriented change list tied to specific paper sections.

## Required inputs

Prefer a `revision-brief` containing:

- review comments
- manuscript status
- target deadline
- target venue or decision stage
- output language
- known author constraints

## Core workflow

1. Normalize comments into issue units.
2. Separate major concerns from minor edits.
3. Map each issue to affected sections, evidence needs, and owner actions.
4. Draft a revision order based on risk and dependency.
5. Produce a response-ready plan with unresolved questions.

## Required outputs

- prioritized revision table
- per-comment action
- evidence or experiment requirements
- rebuttal notes where relevant
- remaining risks before resubmission
- response language consistent with the brief

## Guardrails

- Do not collapse all comments into generic prose.
- Do not promise fixes without identifying the required evidence or edits.
- Preserve the distinction between paper changes and response-letter changes.
