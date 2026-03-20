# Workflow Example: Full Paper From Topic

This example shows how PaperSkills should handle a "write the whole paper" request when the user only provides a topic.

## User request

`请使用 using-paperskills。题目为“人工智能搜索引擎广告模式策略研究”，用中文。完整写一篇论文。`

## Stage 1: `using-paperskills`

- Diagnose this as a multi-stage paper-writing workflow rather than a single drafting task.
- Normalize `language: zh-CN`, target artifact `full paper`, manuscript type, and `evidence_availability: none provided`.
- Route first to `research-scoping` and declare the planned downstream chain.

## Stage 2: `research-scoping`

- Narrow the topic into concrete research questions, scope boundaries, and keyword clusters.
- Produce a `scoping-brief`.
- Recommend `paper-tracker` or `literature-review` based on evidence availability and time sensitivity.

## Stage 3: `paper-tracker`

- Build a recent-paper candidate pool because the user did not provide a source list.
- Record search scope, cutoff date, and shortlist rationale.
- Hand off the candidate pool to `literature-review`.

## Stage 4: `literature-review`

- Screen the candidate pool and synthesize themes, debates, and gaps.
- Produce an evidence ledger and a related-work synthesis in Chinese.
- Hand the strongest gaps and supported claims to `research-design`.

## Stage 5a: `research-design` when needed

- Use this stage only if the intended manuscript genuinely needs research questions, hypotheses, or a future-tense study plan.
- If no study has been completed and the target is a non-empirical undergraduate thesis, the workflow may skip this stage and keep the manuscript type as `conceptual-paper` or `literature-review-paper`.

## Stage 6: `paper-drafting`

- Draft the manuscript in Chinese from the scoped topic, evidence ledger, and optional design brief.
- Keep claims tied to collected evidence.
- Preserve the inferred manuscript type so the output stays in academic-paper form instead of drifting into a consultancy report.
- Mark unsupported sections as limitations or placeholders instead of presenting fabricated certainty.

## Stage 7: `manuscript-finalization`

- Convert the working draft into a thesis-ready full manuscript rather than stopping at a draft.
- Ensure abstract, keywords, chapter completeness, references, and conclusion are all present and mutually consistent.
- Preserve explicit evidence limits instead of polishing them away.

## Expected workflow property

The workflow must not stop after stage diagnosis, scoping, or working-draft output. A complete-paper request from only a topic should continue through evidence collection, synthesis, drafting, and finalization, using `research-design` only when the manuscript type actually requires it.
