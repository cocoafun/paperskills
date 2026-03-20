---
name: using-paperskills
description: Use when starting any research-oriented conversation to diagnose the current PaperSkills stage, decide whether the task needs a multi-stage workflow, and route the agent before answering directly.
---

# Using PaperSkills

Use this skill at the start of any research task. Its job is to decide which stage or workflow chain of the PaperSkills system applies before the agent begins drafting content.

Read [references/stage-router.md](references/stage-router.md) for routing rules and edge cases.
Read [examples/common-entry-cases.md](examples/common-entry-cases.md) for representative user requests.

## Use this skill when

- The user is starting a research or paper-writing task from scratch.
- The user names `using-paperskills` or asks to "use paperskills" without naming the exact downstream skill.
- The request may span more than one research stage, such as "完整写一篇论文", "from topic to proposal", or "find papers and identify gaps".

## Do not use this skill for

- Single-stage requests that already clearly belong to one downstream skill and do not need entry-stage diagnosis.
- Nonresearch writing tasks that are outside the PaperSkills workflow.

## Core rule

Do not jump directly into writing, reviewing, or paper search if a more specific PaperSkills skill should be activated first.

If the request may span multiple research stages, you must do stage diagnosis first. Do not draft content first and route later.

## Workflow routing

First determine the immediate next stage. Then decide whether the user also needs a downstream workflow chain in the same turn.

Immediate stage options:

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
6. `manuscript-finalization`
   Use when the user already has a working draft and wants a thesis-ready or submission-ready manuscript.
7. `peer-review`
   Use when the user wants reviewer-style critique on one paper.
8. `revision-planning`
   Use when the user wants to turn comments or review feedback into revision tasks.

Common multi-stage chains:

- `research-scoping -> literature-review`
  Use when the topic is broad and the user needs evidence-backed synthesis next.
- `research-scoping -> paper-tracker -> literature-review`
  Use when the topic is broad and the field is time-sensitive, or the user has no corpus and needs a recent retrieval pass before synthesis.
- `literature-review -> research-design`
  Use when the user wants gaps translated into research questions, hypotheses, or methods.
- `research-scoping -> literature-review -> research-design -> paper-drafting`
  Use when the user wants a proposal or defendable study plan from a rough topic.
- `research-scoping -> literature-review -> paper-drafting -> manuscript-finalization`
  Use when the user wants a non-empirical full paper or undergraduate thesis from a rough topic and the defensible artifact is conceptual or review-led.
- `research-scoping -> paper-tracker -> literature-review -> research-design -> paper-drafting -> manuscript-finalization`
  Default full-paper workflow when the user asks for a complete paper from only a topic title or theme and no evidence ledger is provided.
- `research-scoping -> paper-tracker -> literature-review -> paper-drafting -> manuscript-finalization`
  Prefer this chain when the user wants a non-empirical undergraduate thesis from only a title and the topic depends on live platform behavior, product features, policy pages, or recent field movement.

## Routing discipline

- If the request is ambiguous, first produce a concise stage diagnosis.
- If the request spans multiple stages, identify the earliest missing stage and also name the planned downstream chain.
- If the user asks for content that requires evidence not yet collected, route upstream instead of fabricating downstream certainty.
- If the user asks for a full paper, draft, proposal, or review from thin evidence, diagnose evidence status before selecting a later-stage skill.
- If the user asks for a full paper, proposal, thesis chapter, or "完整撰写" from only a topic, do not stop at scoping. Produce a compact scoping brief, then continue through the missing evidence and design stages as needed.
- If the user asks for a full paper or thesis from only a title and no source list or evidence ledger is provided, treat retrieval as still missing. Do not route directly from scoping into synthesis unless the retrieval plan and evidence status are both explicit.
- If the user asks for a complete paper or thesis, do not stop the workflow at `paper-drafting`. Add `manuscript-finalization` when the requested deliverable is meant to read as a finished manuscript rather than a working draft.
- Treat `paper-tracker` as a retrieval accelerator, not a mandatory stage. Use it when recency matters, when the user explicitly wants recent papers or a reading shortlist, or when a live field needs a fast candidate pool before `literature-review`.
- If evidence coverage is partial, require an explicit confidence or limitation note in the final output.
- Do not mark `evidence_status` as `mixed-full-text-and-abstract`, `full-text`, or similar before retrieval has actually happened in the current run. Use `no-corpus-yet`, `needs-retrieval`, or `planned-retrieval` until sources are collected.
- If you continue through multiple PaperSkills stages in the same turn, persist each completed stage before creating the next one. Do not precreate the full chain and backfill artifacts at the end.

Short routing defaults:

- broad or fuzzy topic -> `research-scoping`
- recent papers, trends, or shortlist -> `paper-tracker`
- synthesis, gaps, or related work -> `literature-review`
- questions, hypotheses, methods, or study plan -> `research-design`
- manuscript drafting -> first verify manuscript type and evidence status; if they are insufficient, route upstream
- final manuscript or thesis-ready delivery -> `manuscript-finalization`

## Red flags

Stop and re-route if you are about to do any of these:

- "先写一版再说"
- "先搜几篇再判断阶段"
- "用户要完整论文，所以直接进入 drafting"
- "证据不够也先按完成态写"
- writing an empirical-paper style result section without completed study evidence

## Certainty discipline

- Do not skip straight to downstream drafting when upstream evidence gathering is still missing.
- Do not present incomplete evidence gathering as if the workflow already supports a finished empirical manuscript.
- If the user has not provided data, completed results, or a verified corpus, do not let later stages speak in a completed-study voice.
- When later-stage work is requested on partial evidence, require explicit limits such as `partial`, `provisional`, or `low confidence`.
- When the user asks for a finished manuscript, remember that `paper-drafting` still produces a draft package. Use `manuscript-finalization` before claiming the workflow has produced a thesis-ready or submission-ready artifact.

## Expected handoff

Before handing off to a downstream skill, normalize:

- user goal
- output language
- target artifact
- manuscript type
- thesis mode or article mode when the artifact is academic
- evidence availability
- study completion status
- time sensitivity
- downstream brief type
- evidence status
- evidence limitations
- whether a verified corpus already exists in the run
- whether live retrieval is still required before synthesis

## Local artifact persistence

When the task produces reusable stage state, create or reuse a task-local run directory such as:

```text
artifacts/paperskills/<run-id>/
```

Before producing any stage diagnosis or downstream handoff, initialize local storage with:

```bash
python3 skills/using-paperskills/scripts/paperskills_artifacts.py init \
  --task "<task-title>" \
  --user-query "<original-user-request>" \
  --entry-stage using-paperskills \
  --planned-chain research-scoping,paper-tracker,literature-review,paper-drafting,manuscript-finalization
```

Storage rules:

- `using-paperskills` should initialize the run when it is the entry stage.
- Do not treat local persistence as optional when the task is producing reusable workflow state.
- Archive the user's original request at run level. Preserve it in machine-readable form in `manifest.json` and in a human-readable file such as `user-query.md`.
- Write a machine-readable stage brief before routing downstream.
- Record the diagnosed immediate stage and planned chain in a run-level manifest or stage status file.
- If the user is doing only one stage later, that downstream stage must still be able to create its own standalone run.
- Do not assume every task will continue through the full workflow.
- Reuse a user-specified run path when the user explicitly asks to continue a prior task.

Stage progression rules:

- Only create the current stage package. Do not call `ensure-stage` for later stages until you are actually starting them.
- Use the real stage position in the active chain for `--index`. Example indices in downstream skills are illustrative, not universal.
- As soon as a stage brief is stable, write `brief.json` instead of waiting until the end of the run.
- Before routing to the next stage, persist `notes.md`, `output.md`, `status.json`, and `handoff.json` as needed, then call `update-stage` so the timestamps reflect real stage boundaries.
- Do not backfill multiple completed stages in one batch after the full workflow is already done.

Completion example:

```bash
python3 skills/using-paperskills/scripts/paperskills_artifacts.py update-stage \
  --run-dir artifacts/paperskills/<run-id> \
  --stage <stage-name> \
  --index <stage-index> \
  --status completed \
  --evidence-status <evidence-status> \
  --next-skill <next-skill> \
  --handoff-ready true
```

Prefer a structured brief over free-form context whenever possible.

## Required outputs

At minimum, emit:

- a concise stage diagnosis
- the immediate next skill
- the planned workflow chain when more than one stage is required
- a normalized handoff brief containing the core fields above
- an explicit manuscript-type label such as `literature-review-paper`, `conceptual-paper`, `proposal-style-manuscript`, or `empirical-paper`
- explicit evidence limitations when later-stage writing is requested before evidence is ready
- an explicit downstream brief or a statement that handoff is not yet ready
- if the requested deliverable is a complete thesis, an explicit note that downstream stages must preserve `target_artifact=undergraduate thesis` instead of silently downgrading to a generic paper brief
- if no verified corpus exists yet, an explicit `retrieval_required` marker and a non-final evidence status
- if the workflow continues in the same turn, a persisted stage package for the completed stage before the next stage begins

## Manuscript-type discipline

- If the user asks for a "论文" but does not provide data, completed experiments, or finished results, do not silently default to a finished empirical article.
- First infer the most defensible manuscript type:
  - `literature-review-paper` for synthesis-led requests
  - `conceptual-paper` for framework, proposition, or theory-building requests
  - `proposal-style-manuscript` for topic-to-study-plan requests with no completed study
  - `empirical-paper` only when the user provides completed study evidence, results, or reproducible findings
- Pass the inferred manuscript type downstream so later skills do not drift into report-style writing or fake completed results.
- If the user explicitly asks for `中文本科毕业论文`, preserve both the manuscript type and the thesis artifact through every downstream brief. Do not let a later stage rewrite the artifact as only `research brief`, `review note`, or `draft` without also carrying forward the final thesis target.
- If the user explicitly excludes `完成态实证论文`, write that exclusion into the normalized brief and require downstream stages to avoid empirical sections such as sample description, model estimation, or validated findings.

## Language handling

- If the user specifies a language such as `用中文`, `英文`, `zh-CN`, or `in English`, preserve it as the normalized `language` field.
- Pass the same `language` field to downstream PaperSkills stages unless the user explicitly changes it mid-workflow.
- If the user does not specify a language, follow the language of the current conversation.
