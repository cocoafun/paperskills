---
name: brief-compliance-review
description: Use when checking whether a PaperSkills output actually satisfies the current normalized brief, preserves required fields, states evidence limits, and is safe to hand off downstream.
---

# Brief Compliance Review

Review whether a stage output satisfies the current brief before optimizing style or polish.

## Use this skill when

- A stage output is about to be finalized.
- You need to check that a generated artifact matches the normalized brief or schema.
- You need to confirm that downstream handoff fields were preserved.

## Core checks

- Does the output satisfy the corresponding schema or normalized brief?
- Are user goals and required fields preserved?
- Are `language`, `manuscript_type`, and `target_artifact` still explicit?
- Is `evidence_status` or an equivalent evidence-completeness marker preserved?
- Are limitations and missing evidence stated clearly?
- Did the output add strong conclusions that the brief did not justify?

## Output contract

Report:

- compliant items
- missing or drifted fields
- evidence-boundary failures
- downstream handoff risks
- whether the stage is actually ready to finalize
