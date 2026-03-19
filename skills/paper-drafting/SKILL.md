---
name: paper-drafting
description: Use when the user wants to turn a structured research brief, literature synthesis, or study design into an outline, section plan, or evidence-backed paper draft.
---

# Paper Drafting

Generate manuscript structure and draft text from explicit evidence and research design inputs.

Read [references/brief-schema.md](references/brief-schema.md) for the normalized draft brief shape.
Read [references/drafting-playbook.md](references/drafting-playbook.md) for section planning and evidence-binding rules.
Use [assets/draft_template.md](assets/draft_template.md) when you want a manual outline scaffold.
Use [examples/section-brief.json](examples/section-brief.json) as a starter example.

## Brief-first execution

When local files are useful, prefer this pipeline:

1. Build a JSON brief following [references/brief-schema.md](references/brief-schema.md).
2. Render a starter markdown file:

```bash
python3 skills/paper-drafting/scripts/render_draft.py \
  --brief skills/paper-drafting/examples/section-brief.json \
  --output paper_outline.md
```

3. Expand the generated scaffold with evidence-backed prose.

## Use this skill when

- The user wants an outline or section draft.
- The user wants to turn a literature review and design brief into a paper structure.
- The user wants evidence-backed writing instead of free-form generation.

## Required inputs

Prefer a `draft-brief` containing:

- paper goal
- target venue or audience
- section list
- evidence ledger or source list
- claims that each section must support
- language and citation style

## Core workflow

1. Confirm the target artifact: outline, section draft, full draft, or proposal.
2. Map claims to sections and evidence.
3. Draft section-by-section, keeping evidence traceable.
4. Mark unsupported assertions as placeholders or evidence gaps.
5. Close with unresolved writing dependencies.

## Guardrails

- Do not write polished prose that exceeds the evidence base.
- Do not merge literature summary, design claims, and future work into one undifferentiated narrative.
- If the evidence ledger is weak, produce a scaffolded draft with explicit gaps rather than fake certainty.
