# Workflow Example: Idea To Draft

This example shows how PaperSkills should hand work across multiple stages.

## User request

`我想研究大模型如何支持文献综述写作，最终想写一篇 proposal。过程中请用中文。`

## Stage 1: `using-paperskills`

- Diagnose the request as an early-stage research workflow.
- Route first to `research-scoping`.
- Normalize `language: zh-CN` and pass it downstream.

## Stage 2: `research-scoping`

- Normalize the topic.
- Produce a `scoping-brief`.
- Recommend `literature-review` as the next step.
- Keep `language: zh-CN` in the brief.

Suggested artifact:

- `skills/research-scoping/examples/topic-brief.json`

## Stage 3: `literature-review`

- Build a source plan and evidence ledger.
- Produce themes and research gaps.
- Hand off gaps to `research-design`.
- Write the review scaffold in Chinese while preserving source metadata fidelity.

## Stage 4: `research-design`

- Convert the strongest gap into research questions and a method path.
- Produce a `design-brief`.
- Preserve `language: zh-CN` for the proposal-facing output.

Suggested artifact:

- `skills/research-design/examples/proposal-brief.json`

## Stage 5: `paper-drafting`

- Turn the design into an outline or proposal draft.
- Keep claims tied to evidence.
- Draft the proposal in Chinese unless the user switches language.

Suggested artifact:

- `skills/paper-drafting/examples/section-brief.json`

## Expected workflow property

No stage should skip evidence boundaries. If the literature evidence is weak, `paper-drafting` should emit a scaffolded draft rather than polished certainty.
