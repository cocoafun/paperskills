---
name: research-scoping
description: Use when a research request is broad, fuzzy, or under-scoped and needs to be turned into a concrete question set, boundary, keyword plan, and downstream research brief.
---

# Research Scoping

Turn an early-stage research idea into a scoped brief that downstream skills can execute.

Read [references/brief-schema.md](references/brief-schema.md) for the normalized JSON shape.
Read [references/scoping-playbook.md](references/scoping-playbook.md) for narrowing and boundary-setting rules.
Use [assets/scoping_template.md](assets/scoping_template.md) when you want a manual markdown scaffold.
Use [examples/topic-brief.json](examples/topic-brief.json) as a starter example.

## Brief-first execution

When local files are useful, prefer this pipeline:

1. Build a JSON brief following [references/brief-schema.md](references/brief-schema.md).
2. Render a starter markdown file:

```bash
python3 skills/research-scoping/scripts/render_scope.py \
  --brief skills/research-scoping/examples/topic-brief.json \
  --output scoped_topic.md
```

3. Replace generic placeholders with the current user's scoped topic.

## Use this skill when

- The user has a topic but not a precise question.
- The request is too broad for search or writing to be reliable.
- The user needs keywords, scope boundaries, or a research framing before literature work starts.

## Required outputs

Produce a `scoping-brief` with:

- topic
- objective
- target artifact
- language
- domain
- time window
- core questions
- keyword clusters
- inclusion boundaries
- exclusion boundaries
- recommended next skill

## Core workflow

1. Restate the topic in plain language.
2. Narrow it to 2-4 concrete research questions.
3. Define boundary conditions: domain, population, method, period, or artifact.
4. Build keyword clusters for later retrieval.
5. Identify the most appropriate downstream skill.

## Guardrails

- Do not pretend the scoping step is complete if the topic is still vague.
- Do not skip boundary-setting for convenience.
- When the user wants a draft immediately, still produce a compact scoping summary first if the request is under-specified.
- State what was inferred versus what the user explicitly gave.
