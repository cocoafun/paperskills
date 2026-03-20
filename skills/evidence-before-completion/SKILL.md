---
name: evidence-before-completion
description: Use when about to claim that a research stage is complete, evidence is sufficient, a draft is supportable, or a workflow can move downstream; verify evidence status, brief completeness, and uncertainty markings before making completion claims.
---

# Evidence Before Completion

## Overview

In research workflows, unsupported certainty is not efficiency. It is a failure to preserve evidence boundaries.

**Core principle:** verify the evidence state before making any completion, sufficiency, or downstream-readiness claim.

If you have not checked the current source base, brief completeness, and handoff fields in this turn, do not present the stage as complete.

## The Iron Law

```text
NO STAGE-COMPLETION CLAIMS WITHOUT FRESH EVIDENCE AND BRIEF VERIFICATION
```

If you cannot show what sources were checked, what remains missing, and why the current brief is sufficient, you cannot truthfully say:

- "the literature shows"
- "research consistently finds"
- "this stage is complete"
- "this can go directly to the next stage"

## When To Use

Apply this skill before:

- closing `paper-tracker`, `literature-review`, `research-design`, `paper-drafting`, `peer-review`, or `revision-planning`
- claiming the evidence base is adequate
- asserting that a synthesis, design, or draft is evidence-backed
- telling the user the workflow can proceed directly downstream
- converting partial material into high-confidence judgments

## Verification Gate

Before making any completion claim:

1. Identify what evidence the current stage actually used.
2. Check whether the sources were directly inspected, partially inspected, or only inferred from metadata or abstracts.
3. Check whether the current brief contains all required fields for this stage.
4. Separate explicit evidence from agent inference.
5. Check whether downstream handoff fields are explicit enough for the next skill.
6. Only then state either:
   - the stage is complete, with evidence boundaries, or
   - the stage is partial, blocked, or low confidence, with the missing items named

Skip any step and the completion claim is not reliable.

## Required Checks

### Source verification

- Do not say "文献表明", "the literature shows", or "studies agree" unless the cited source set actually supports that scope of claim.
- If the claim comes from one or two papers, say that directly.
- If only abstracts, snippets, or metadata were reviewed, mark the output as `partial`, `abstract-based`, `metadata-based`, `low confidence`, or equivalent.
- If important sources were not checked in full text, do not imply strong consensus.

### Evidence versus inference

- Label source-grounded findings separately from your synthesis or inference.
- Do not convert a plausible interpretation into a high-confidence conclusion without explicit support.
- If a recommendation depends on unverified assumptions, state those assumptions.

### Brief completeness

- If required brief fields are missing, do not say the stage is complete.
- If the brief omits manuscript type, language, target artifact, evidence status, or other stage-critical fields, surface the gap.
- If you inferred missing fields, state that they were inferred rather than provided.

### Downstream handoff

- Do not say "ready for the next stage" unless the downstream handoff is explicit.
- Name the next skill and the brief type to pass forward.
- Preserve required fields such as `language`, `manuscript_type`, `evidence_status`, `time_window`, and `target_artifact` when relevant.
- If downstream execution depends on missing evidence or unresolved choices, say the workflow is not yet ready to advance.

## Common False Claims

| False claim | What is actually missing |
|---|---|
| "The literature clearly shows X" | Source set too small, too partial, or not directly checked |
| "The review is complete" | Required brief fields or evidence gaps remain |
| "This design is well supported" | Gaps were inferred, not grounded in reviewed sources |
| "The draft is ready" | Claims exceed the evidence ledger or manuscript type |
| "This can directly move to the next stage" | Handoff brief and persistent fields are not explicit |
| "The review recommends accept/reject" | Only abstract or partial paper evidence was available |

## Output Language For Uncertainty

Use explicit limitation language when the evidence is incomplete:

- `partial`
- `low confidence`
- `abstract-based synthesis`
- `metadata-based screening`
- `provisional`
- `requires full-text verification`
- `handoff not ready`
- `brief incomplete`

Preferred patterns:

- "Based on the reviewed abstracts, the evidence tentatively suggests ..."
- "This is a partial review because full-text verification was not completed."
- "The current design is provisional and depends on the following unverified assumptions ..."
- "The stage is not complete because the brief still lacks ..."

## Common Mistakes

- Writing polished certainty over thin evidence
- Treating retrieval as synthesis
- Treating synthesis as proof of consensus
- Forgetting to mark abstract-only or partial-paper judgments as low confidence
- Saying a stage is complete when the brief is still missing required fields
- Saying downstream work can begin without an explicit handoff contract

## Bottom Line

Evidence boundaries are part of the deliverable.

If the evidence is partial, say it is partial. If the brief is incomplete, say it is incomplete. If the handoff is not explicit, do not claim readiness.
