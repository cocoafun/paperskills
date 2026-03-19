# Skill Authoring Checklist

Use this checklist when adding or revising a PaperSkills skill.

## Required files

- `SKILL.md`
- at least one `references/` file when the workflow is nontrivial
- at least one `examples/` file showing a realistic brief or request
- an `assets/` template when the output has a stable structure

## Required content in `SKILL.md`

- trigger description in frontmatter
- when to use
- when not to use
- required inputs
- core workflow
- required outputs
- guardrails

## Repository fit checks

- Does the skill belong to the entry, orchestration, or execution layer?
- Does it define a structured handoff?
- Does it preserve evidence boundaries?
- Does it remain portable across agent environments?
