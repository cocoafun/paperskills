---
name: research-design
description: Use when the user wants to transform literature gaps or a problem statement into research questions, hypotheses, methods, variables, data plans, or an empirical or theoretical study design.
---

# Research Design

Convert a scoped topic and literature evidence into a defendable study design.

Read [references/brief-schema.md](references/brief-schema.md) for the normalized design brief shape.
Read [references/design-playbook.md](references/design-playbook.md) for question, method, and evidence matching rules.
Use [assets/design_template.md](assets/design_template.md) when you want a manual design scaffold.
Use [examples/proposal-brief.json](examples/proposal-brief.json) as a starter example.

## Brief-first execution

When local files are useful, prefer this pipeline:

1. Build a JSON brief following [references/brief-schema.md](references/brief-schema.md).
2. Render a starter markdown file:

```bash
python3 skills/research-design/scripts/render_design.py \
  --brief skills/research-design/examples/proposal-brief.json \
  --output research_design.md
```

3. Replace the starter content with project-specific questions, methods, and risks.

## Use this skill when

- The user asks how to study a problem after reviewing the literature.
- The user wants hypotheses, propositions, variables, methods, or identification logic.
- The user is preparing a proposal, thesis plan, or methods section.

## Required inputs

Prefer a `design-brief` built from:

- scoped topic
- manuscript type
- literature gaps
- theoretical lens
- target contribution
- feasible data or experiment context

## Core workflow

1. Identify the target contribution.
2. Confirm whether the target manuscript is conceptual, review-led, proposal-style, or empirical.
3. Translate gaps into research questions or propositions.
4. Match each question to a method family.
5. Specify variables, constructs, data, or evaluation criteria.
6. Surface assumptions, feasibility risks, and identification limits.

## Required outputs

- research questions or hypotheses
- manuscript-type statement and study-completion status
- candidate method path
- data or evidence requirements
- contribution statement
- major risks and open dependencies

## Guardrails

- Do not claim causal strength without a plausible design.
- Do not propose measurements that cannot realistically be obtained.
- Distinguish theory-building, empirical testing, systems evaluation, and review-style contributions.
- If no completed data or results exist, output a defendable design or proposal path instead of implying that the study has already been executed.
