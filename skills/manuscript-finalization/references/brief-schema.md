# Finalization Brief Schema

Use this schema when converting a working draft into a final manuscript or thesis-ready output.

## Minimal shape

```json
{
  "paper_title": "人工智能搜索引擎广告模式策略研究",
  "target_artifact": "undergraduate thesis",
  "completion_standard": "thesis-ready",
  "manuscript_type": "conceptual-paper",
  "study_completion_status": "literature-grounded",
  "language": "zh-CN",
  "citation_style": "GB/T 7714",
  "evidence_status": "full-text-reviewed",
  "draft_status": "working-draft",
  "required_sections": [
    "中文摘要",
    "关键词",
    "引言",
    "文献综述",
    "分析框架",
    "策略分析",
    "结论与不足",
    "参考文献"
  ],
  "unresolved_gaps": [
    "参考文献格式尚未统一",
    "摘要尚未压缩到正式篇幅"
  ]
}
```

## Field rules

- `paper_title`: current title or working title.
- `target_artifact`: for example `submission-ready manuscript`, `undergraduate thesis`, or `journal article`.
- `completion_standard`: one of `submission-ready`, `thesis-ready`, `defense-ready`, or `partial-finalization`.
- `manuscript_type`: one of `literature-review-paper`, `conceptual-paper`, `proposal-style-manuscript`, or `empirical-paper`.
- `study_completion_status`: describe what is actually complete, such as `design-only`, `literature-grounded`, `partial-results`, or `completed-study`.
- `evidence_status`: describe how strong the supporting evidence is.
- `draft_status`: for example `outline`, `working-draft`, `revised-draft`, or `near-final`.
- `required_sections`: the sections or chapters that must be present before finalization can pass.
- `unresolved_gaps`: explicit blockers or risks that still remain.

## Target-artifact discipline

- `undergraduate thesis` should usually include front matter, body chapters, conclusion, and references.
- `submission-ready manuscript` should usually include title, abstract, keywords, core body sections, references, and any required appendices.
- If the manuscript type is non-empirical, the final structure must not imply finished experiments or fabricated results.
