# PaperSkills

PaperSkills is a workflow system for AI-native research. It helps agents turn vague research intent into scoped questions, recent-paper tracking, structured synthesis, study design, paper drafting, manuscript finalization, reviewer-style critique, and revision planning.

It is not just a folder of academic prompts. The goal is to provide a reusable research workflow with explicit skill routing, structured briefs, evidence boundaries, and portable documentation that works across agent environments.

## How It Works

PaperSkills is organized as a staged workflow:

1. `using-paperskills` identifies the current research stage and, when needed, the downstream workflow chain.
2. `research-scoping` narrows broad ideas into executable research briefs.
3. `paper-tracker` gathers recent papers and builds a candidate pool.
4. `literature-review` synthesizes the evidence into themes and gaps.
5. `research-design` converts gaps into questions, methods, and data plans.
6. `paper-drafting` turns evidence and design into outlines and working-draft text.
7. `manuscript-finalization` turns a working draft into a submission-ready manuscript or thesis-ready full text.
8. `peer-review` critiques a paper draft as a reviewer would.
9. `revision-planning` converts feedback into an actionable revision roadmap.

The intended flow is:

`idea -> scope -> track -> synthesize -> design -> draft -> finalize`

Optional external-critique loop:

`draft -> review -> revise -> finalize`

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

`using-paperskills -> research-scoping -> literature-review -> research-design -> paper-drafting -> manuscript-finalization`

## Current Skills

### Entry Layer

- `skills/using-paperskills`

### Orchestration Layer

- `skills/research-scoping`
- `skills/research-design`
- `skills/paper-drafting`
- `skills/manuscript-finalization`
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
- `finalization-brief.schema.json`
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

## Local Artifact Storage

PaperSkills should persist intermediate execution content locally whenever a stage produces a reusable brief, evidence ledger, review memo, or handoff package.

This storage model must work for both:

- full workflows such as `using-paperskills -> research-scoping -> literature-review -> research-design -> paper-drafting -> manuscript-finalization`
- single-stage runs such as a one-off `peer-review` or `revision-planning` request

Recommended storage root:

```text
artifacts/paperskills/<run-id>/
```

Recommended `run-id` shape:

```text
YYYYMMDD-HHMMSS-<task-slug>
```

Recommended layout:

```text
artifacts/paperskills/<run-id>/
  manifest.json
  stages/
    01-using-paperskills/
      brief.json
      notes.md
      handoff.json
      status.json
    02-research-scoping/
      brief.json
      output.md
      handoff.json
      status.json
```

Bootstrap commands:

```bash
python3 skills/using-paperskills/scripts/paperskills_artifacts.py init \
  --task "人工智能搜索引擎广告模式策略研究" \
  --entry-stage using-paperskills \
  --planned-chain research-scoping,paper-tracker,literature-review,paper-drafting,manuscript-finalization \
  --language zh-CN \
  --manuscript-type conceptual-paper \
  --target-artifact "undergraduate thesis"
```

```bash
python3 skills/using-paperskills/scripts/paperskills_artifacts.py ensure-stage \
  --run-dir artifacts/paperskills/<run-id> \
  --stage research-scoping \
  --index 2 \
  --status in_progress \
  --next-skill paper-tracker
```

Storage rules:

- Each invocation creates or joins one `run-id`. Do not assume the task is a full workflow.
- If the user is only doing one stage, still create a run and persist that stage as a self-contained unit.
- Each stage should write its own normalized `brief.json` even when there is no upstream stage.
- Use `handoff.json` only when there is an actual downstream next step.
- Preserve machine-readable state and human-readable output separately.
- Never silently overwrite an earlier stage result. Create a new run or a new stage attempt instead.
- If the user explicitly provides a run directory or asks to continue a previous run, reuse that path and append the new stage artifacts there.
- Use `skills/using-paperskills/scripts/paperskills_artifacts.py` to initialize the run and stage folders before writing content.

Intent:

- make downstream reference and audit easier
- allow partial workflows to resume cleanly
- keep evidence boundaries visible at each stage
- avoid losing intermediate reasoning products that later drafting, finalization, review, or revision work depends on

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
