---
name: using-paperskills
description: Use when starting any research-oriented conversation to identify the current research stage and route the agent to the correct PaperSkills workflow before answering directly.
---

# Using PaperSkills

Use this skill at the start of any research task. Its job is to decide which stage of the PaperSkills workflow applies before the agent begins drafting content.

Read [references/stage-router.md](references/stage-router.md) for routing rules and edge cases.
Read [examples/common-entry-cases.md](examples/common-entry-cases.md) for representative user requests.

## Core rule

Do not jump directly into writing, reviewing, or paper search if a more specific PaperSkills skill should be activated first.

## Workflow routing

Map the user's request to one primary stage:

1. `research-scoping`
   Use when the topic is still broad, fuzzy, or under-specified.
2. `paper-tracker`
   Use when the user wants recent papers, trend scanning, or a reading shortlist.
3. `literature-review`
   Use when the user wants related work, thematic synthesis, or gap analysis.
4. `research-design`
   Use when the user wants to turn literature gaps into questions, hypotheses, methods, or identification logic.
5. `paper-drafting`
   Use when the user wants outlines, section drafts, or evidence-backed manuscript writing.
6. `peer-review`
   Use when the user wants reviewer-style critique on one paper.
7. `revision-planning`
   Use when the user wants to turn comments or review feedback into revision tasks.

## Routing discipline

- If the request is ambiguous, first produce a concise stage diagnosis.
- If the request spans multiple stages, start with the earliest missing stage and say so.
- If the user asks for content that requires evidence not yet collected, route upstream instead of fabricating downstream certainty.
- If evidence coverage is partial, require an explicit confidence or limitation note in the final output.

## Expected handoff

Before handing off to a downstream skill, normalize:

- user goal
- output language
- target artifact
- evidence availability
- time sensitivity

Prefer a structured brief over free-form context whenever possible.
