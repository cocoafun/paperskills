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

## Failure-first authoring

Before writing a new skill, first draft 2-3 prompts that expose the failure you are trying to prevent.

Check how the agent fails without the skill:

- wrong stage routing
- unsupported inference
- overconfident completion claims
- missing downstream handoff fields

Design the skill around preventing those failures, not around writing a generic process description.

## Skill test cases

Every new skill should be testable against at least these cases:

- trigger test
- wrong-skill avoidance test
- workflow handoff test
- evidence-boundary test

If the skill changes workflow discipline, include at least one case where the correct behavior is to stop, de-scope, or route upstream.

## Description anti-patterns

- Do not write the description as a summary of what the skill will do.
- Do not hide triggering conditions inside vague phrases like "helps with" or "supports".
- Do not assume downstream behavior will be obvious if the trigger text is weak.

Descriptions should primarily answer: when must this skill be used?

## Guardrail design

Every new skill must state:

- evidence boundary
- allowed inference
- forbidden claims
- downstream handoff contract

If the skill can end with a completion claim, it should explicitly reference `evidence-before-completion` or define an equivalent stage-completion gate.

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

Cross-cutting skills are allowed when they enforce workflow discipline across multiple stages. They should still define explicit trigger conditions and handoff expectations.
