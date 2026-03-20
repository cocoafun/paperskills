# PaperSkills

PaperSkills is a workflow system for AI-native research. It helps agents turn vague research intent into scoped questions, recent-paper tracking, structured synthesis, study design, paper drafting, reviewer-style critique, and revision planning.

It is not just a folder of academic prompts. The goal is to provide a reusable research workflow with explicit skill routing, structured briefs, evidence boundaries, and portable documentation that works across agent environments.

## How It Works

PaperSkills is organized as a staged workflow:

1. `using-paperskills` identifies the current research stage and, when needed, the downstream workflow chain.
2. `research-scoping` narrows broad ideas into executable research briefs.
3. `paper-tracker` gathers recent papers and builds a candidate pool.
4. `literature-review` synthesizes the evidence into themes and gaps.
5. `research-design` converts gaps into questions, methods, and data plans.
6. `paper-drafting` turns evidence and design into outlines and draft text.
7. `peer-review` critiques a paper draft as a reviewer would.
8. `revision-planning` converts feedback into an actionable revision roadmap.

The intended flow is:

`idea -> scope -> track -> synthesize -> design -> draft -> review -> revise`

## Language Control

PaperSkills supports explicit output language control across the workflow.

- Set `language` in the structured brief when a stage uses JSON input.
- Common values are `zh-CN`, `en`, and `en-US`.
- If the user says "用中文", "in English", or similar, the active stage should normalize that into the brief and pass it downstream.
- If no language is specified, skills should follow the user's current language by default.

Recommended pattern:

```json
{
  "language": "zh-CN"
}
```

This field is intended to persist across stage handoffs, for example:

`using-paperskills -> research-scoping -> literature-review -> research-design -> paper-drafting`

## Current Skills

### Entry Layer

- `skills/using-paperskills`

### Orchestration Layer

- `skills/research-scoping`
- `skills/research-design`
- `skills/paper-drafting`
- `skills/revision-planning`
- `skills/writing-paperskills`
- `skills/brief-compliance-review`

### Execution Layer

- `skills/paper-tracker`
- `skills/literature-review`
- `skills/peer-review`

### Cross-Cutting Layer

- `skills/evidence-before-completion`

## Shared Brief Schemas

PaperSkills now defines shared schema contracts in `schemas/`:

- `scoping-brief.schema.json`
- `tracking-brief.schema.json`
- `review-brief.schema.json`
- `design-brief.schema.json`
- `draft-brief.schema.json`
- `reviewer-brief.schema.json`
- `revision-brief.schema.json`

These schemas are intended to make upstream skill outputs reusable by downstream skills and scripts.

## Repository Structure

```text
paperskills/
  docs/
  schemas/
  skills/
  related/
```

`skills/` contains the skill library.

`schemas/` contains shared machine-readable brief contracts.

`docs/` contains product and contributor documentation in Chinese and English.

`related/` contains upstream references, experiments, and adjacent tools that are not part of the core PaperSkills runtime surface.

## Getting Started

Start with the docs:

- Chinese: `docs/zh/`
- English: `docs/en/`

## Installation

PaperSkills is currently used with Codex through native skill discovery.

### Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.codex/INSTALL.md
```

Manual installation is also available in `.codex/INSTALL.md`.

If you are extending the skill system, read:

- `docs/zh/architecture-v2.mdx`
- `skills/writing-paperskills/SKILL.md`

## Design Principles

- Stage-first, not tool-first
- Evidence-backed outputs
- Evidence before completion claims
- Structured briefs over loose context
- Portable across agent environments
- Explicit limits when evidence is incomplete

## Roadmap

### Phase 1

- Product-facing workflow docs
- Entry and orchestration skill scaffolding
- Shared schemas

### Phase 2

- More references, examples, and templates for new workflow skills
- Cross-skill examples and sample end-to-end briefs
- Better installation and platform-specific setup docs

### Phase 3

- Triggering and workflow smoke tests
- Release notes and versioned changelog
- More domain-specific extensions

## Contributing

Contributions should extend the workflow cleanly rather than add isolated prompts. New skills should define:

- when the skill triggers
- what structured input it expects
- what output contract it guarantees
- what evidence limits it must preserve

Use `skills/writing-paperskills/SKILL.md` as the internal authoring guide.
