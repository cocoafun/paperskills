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

## Stage 5: `research-design`

- Convert the literature gaps into research questions, hypotheses, and a feasible method path.
- Produce a `design-brief` that distinguishes supported claims from open assumptions.
- If no study has been completed, label the manuscript as `conceptual-paper` or `proposal-style-manuscript` rather than a finished empirical article.

## Stage 6: `paper-drafting`

- Draft the manuscript in Chinese from the scoped topic, evidence ledger, and design brief.
- Keep claims tied to collected evidence.
- Preserve the inferred manuscript type so the output stays in academic-paper form instead of drifting into a consultancy report.
- Mark unsupported sections as limitations or placeholders instead of presenting fabricated certainty.

## Expected workflow property

The workflow must not stop after stage diagnosis or a scoping note. A complete-paper request from only a topic should continue through evidence collection, synthesis, design, and drafting.
