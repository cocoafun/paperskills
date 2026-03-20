---
name: paper-drafting
description: Use when the user wants to turn a structured research brief, literature synthesis, or study design into an outline, section plan, or evidence-backed paper draft.
---

# Paper Drafting

Generate manuscript structure and working-draft text from explicit evidence and research design inputs.

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
4. If the requested deliverable is a finished manuscript rather than a working draft, hand off to `manuscript-finalization` instead of stopping here.

## Use this skill when

- The user wants an outline or section draft.
- The user wants to turn a literature review and design brief into a paper structure.
- The user wants evidence-backed writing instead of free-form generation.
- The user needs a working draft as the input to a later finalization stage.

## Required inputs

Prefer a `draft-brief` containing:

- paper goal
- manuscript type
- study completion status
- target venue or audience
- section list
- evidence ledger or source list
- claims that each section must support
- language and citation style

## Core workflow

1. Confirm the target artifact: outline, section draft, full draft, or proposal-style manuscript.
2. Confirm manuscript type before choosing section structure.
3. Map claims to sections and evidence.
4. Draft section-by-section, keeping evidence traceable and genre-consistent.
5. Persist substantive draft text for every promised major section; do not replace the draft artifact with a one-line handoff note.
6. Mark unsupported assertions as placeholders or evidence gaps.
7. Close with unresolved writing dependencies.
8. If the user asked for a complete manuscript, emit an explicit handoff to `manuscript-finalization`.

`paper-drafting` must produce a real working manuscript package. At minimum, `output.md` should contain:

- a chapter or section outline
- substantive prose for each promised major section
- visible citation anchors or source bindings for nontrivial claims
- a short unresolved-gaps block at the end

## Guardrails

- Do not write polished prose that exceeds the evidence base.
- Do not merge literature summary, design claims, and future work into one undifferentiated narrative.
- If the evidence ledger is weak, produce a scaffolded draft with explicit gaps rather than fake certainty.
- Do not let management, strategy, or policy recommendations replace the core scholarly sections of the manuscript.
- If the manuscript type is not `empirical-paper`, do not imply completed data collection, statistical findings, or validated results.
- Do not describe the output as final, thesis-ready, or submission-ready. That is `manuscript-finalization` work.
- Do not make `output.md` a pointer such as “see next stage”. The drafting stage is for inspectable draft content, not only workflow narration.
- If `target_artifact` is `undergraduate thesis`, prefer chapter-complete drafting over a compressed article skeleton.

## Before claiming completion

- Check that the `draft-brief` contains the required section plan, manuscript type, evidence ledger, and claim mapping.
- Separate paper text, cited evidence, and agent-authored inference.
- If parts of the draft rely only on partial sources or upstream placeholders, mark them explicitly.
- Check that every section promised in the brief has at least scaffold-plus-prose coverage in the saved draft artifact.
- Do not say the manuscript is ready if key sections still exceed the evidence base.
- If the user asked for a finished paper, mark this stage as a working draft and route to `manuscript-finalization`.
- Use `paperskills:evidence-before-completion` before claiming the draft is evidence-backed or downstream-ready.

## Downstream handoff

- Recommended next skills: `manuscript-finalization`, `peer-review`, or `revision-planning` after review feedback exists
- Pass forward a `draft-brief` or draft package with section claims and evidence ledger
- Preserve `language`, `manuscript_type`, `evidence_status`, `target_artifact`, citation style, and unresolved writing dependencies
- Include the draft artifact path or an embedded section-completion summary so finalization does not need to guess what text actually exists
- If the current draft is proposal-style or evidence-limited, state that downstream finalization or review should evaluate it under those limits

## Local artifact persistence

When persisting local work, keep the draft package traceable to its supporting brief and evidence state.

Before writing stage content, ensure the stage package exists:

```bash
python3 skills/using-paperskills/scripts/paperskills_artifacts.py ensure-stage \
  --run-dir artifacts/paperskills/<run-id> \
  --stage paper-drafting \
  --index <stage-index> \
  --status in_progress
```

- Write `brief.json` for the normalized `draft-brief` as soon as the section plan is stable.
- Save claim-to-evidence mapping notes or unresolved section dependencies in `notes.md`.
- Save the drafted manuscript artifact in `output.md` or a manuscript file.
- Preserve evidence limitations and manuscript type in `status.json`.
- Before handing off to `manuscript-finalization` or review, call `update-stage` so the actual draft artifact is committed before downstream work begins.
- If drafting is run on its own, the stage must still create a self-contained stored brief before writing prose.
