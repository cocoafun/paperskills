# Draft Brief Schema

Use this schema when generating an outline or draft from structured research inputs.

## Minimal shape

```json
{
  "paper_goal": "Conference paper draft on retrieval-grounded literature review agents",
  "manuscript_type": "proposal-style-manuscript",
  "study_completion_status": "design-only",
  "audience": "researchers in information systems and AI",
  "venue_target": "conference",
  "language": "en",
  "citation_style": "APA",
  "sections": [
    {
      "name": "Introduction",
      "goal": "Frame the problem and motivate the contribution.",
      "claims": [
        "Current LLM writing systems often lack citation grounding.",
        "Academic review writing requires evidence traceability."
      ],
      "evidence": [
        "Recent papers on grounded scientific writing",
        "Evidence from literature review workflow studies"
      ]
    }
  ]
}
```

## Field rules

- `paper_goal`: what artifact is being drafted.
- `manuscript_type`: one of `literature-review-paper`, `conceptual-paper`, `proposal-style-manuscript`, or `empirical-paper`.
- `study_completion_status`: one of `design-only`, `partial-results`, or `completed-study`.
- `audience`: intended readers.
- `venue_target`: optional but useful for tone and structure.
- `sections`: required list of sections to draft or plan.
- `claims`: statements that the section must support.
- `evidence`: the source groups, papers, or notes that support the section.

## Section semantics

- `literature-review-paper` should usually include `Introduction`, `Review Scope or Search Strategy`, `Thematic Synthesis`, `Research Gaps`, and `Conclusion`.
- `conceptual-paper` should usually include `Introduction`, `Theoretical Background`, `Framework or Mechanism`, `Propositions or Arguments`, `Discussion`, and `Conclusion`.
- `proposal-style-manuscript` should usually include `Introduction`, `Literature Review`, `Research Questions or Hypotheses`, `Method or Research Design`, `Expected Contributions`, `Limitations`, and `Conclusion`.
- `empirical-paper` should usually include `Introduction`, `Literature Review`, `Method`, `Results`, `Discussion`, and `Conclusion`.

Do not replace these core scholarly sections with report-style sections such as `策略设计`, `对策建议`, or `管理启示` unless they are explicitly framed as a subordinate discussion subsection.
