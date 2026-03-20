---
name: manuscript-finalization
description: Use when a PaperSkills workflow already has a structured draft package and needs to produce a submission-ready manuscript or thesis-ready full text instead of stopping at a working draft.
---

# Manuscript Finalization

Turn a working draft into a submission-ready manuscript package.

Read [references/brief-schema.md](references/brief-schema.md) for the normalized finalization brief shape.
Read [references/finalization-playbook.md](references/finalization-playbook.md) for completion, structure, and evidence-boundary checks.
Use [assets/finalization_template.md](assets/finalization_template.md) when you want a manual finalization scaffold.
Use [examples/finalization-brief.json](examples/finalization-brief.json) as a starter example.

## Brief-first execution

When local files are useful, prefer this pipeline:

1. Build a JSON brief following [references/brief-schema.md](references/brief-schema.md).
2. Render a starter checklist file:

```bash
python3 skills/manuscript-finalization/scripts/render_finalization.py \
  --brief skills/manuscript-finalization/examples/finalization-brief.json \
  --output finalization_checklist.md
```

3. Replace placeholders with manuscript-specific fixes, front matter, references, and readiness notes.
4. Produce the final manuscript artifact only after the readiness checks pass.

## Use this skill when

- The user asks for a complete paper, complete thesis, final manuscript, 定稿, 完整终稿, or a submission-ready output.
- `paper-drafting` has produced a working draft, but the workflow must continue to a final deliverable.
- The workflow needs front matter, chapter completeness, reference normalization, and final limitation language.
- The artifact is an undergraduate thesis, course paper, dissertation-style manuscript, or paper intended to read as a finished scholarly document rather than a scaffold.

## Do not use this skill for

- Early outlines or section stubs with no section-level draft content.
- Pure reviewer critique. Use `peer-review` for that.
- Revision planning from external comments only. Use `revision-planning` for that.

## Required inputs

Prefer a `finalization-brief` containing:

- paper title or working title
- target artifact
- manuscript type
- study completion status
- language and citation style
- chapter or section checklist
- draft package path or draft summary
- evidence status
- unresolved gaps
- required completion standard such as `submission-ready`, `thesis-ready`, or `defense-ready`

## Core workflow

1. Confirm the target completion standard.
2. Check whether the draft is a working draft, revised draft, or nearly final manuscript.
3. Validate manuscript structure against manuscript type and target artifact.
4. Fill missing scholarly components such as abstract, keywords, references, limitations, appendices, and acknowledgements when appropriate.
5. Normalize chapter flow, section naming, and citation style.
6. Remove placeholder language, duplicated claims, and draft-only notes.
7. Preserve explicit evidence limitations instead of polishing them away.
8. Produce a final manuscript package plus a readiness memo.

## Required outputs

- final manuscript or thesis-ready text
- completion checklist
- remaining risk list
- explicit evidence-boundary statement
- final handoff status such as `submission-ready`, `thesis-ready`, or `not yet final`

## Guardrails

- Do not convert a weak draft into a fake finished empirical paper.
- Do not invent data, results, or citations just to make the manuscript look complete.
- If the manuscript type is non-empirical, keep method and findings language aligned with that type.
- If target artifact is `undergraduate thesis`, ensure chapter completeness and academic-paper tone without drifting into consultancy recommendations.
- Do not say the manuscript is final if placeholder sections, unsupported claims, or unresolved references remain.

## Before claiming completion

- Check that the `finalization-brief` includes manuscript type, target artifact, completion standard, and evidence status.
- Check that every major section exists and is aligned with the manuscript type.
- Distinguish what was directly supported by evidence from what remains interpretive or provisional.
- Use `paperskills:brief-compliance-review` and `paperskills:evidence-before-completion` discipline before saying the manuscript is final.
- If the draft still lacks core sections or supported references, mark the output as `not yet final` or `partial finalization`.

## Downstream handoff

- Recommended next skills: `peer-review` for simulated critique or `revision-planning` when actual feedback exists
- Pass forward the final manuscript package plus the finalization checklist
- Preserve `language`, `manuscript_type`, `target_artifact`, `evidence_status`, and `completion_standard`
- If finalization is partial, say exactly what still blocks a true final manuscript

## Local artifact persistence

When persisting local work, keep the final manuscript, readiness memo, and remaining-risk list distinct from the incoming draft package.

Before writing stage content, ensure the stage package exists:

```bash
python3 skills/using-paperskills/scripts/paperskills_artifacts.py ensure-stage \
  --run-dir artifacts/paperskills/<run-id> \
  --stage manuscript-finalization \
  --index 7 \
  --status in_progress
```

- Write `brief.json` for the normalized `finalization-brief`.
- Save chapter-completeness checks, citation cleanup notes, and unresolved risks in `notes.md`.
- Save the finalized manuscript in `output.md` or a manuscript file.
- Preserve completion status and evidence-boundary markers in `status.json`.
- Write `handoff.json` only when sending the finalized manuscript into review or revision work.
