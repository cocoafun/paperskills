# Design Brief Schema

Use this schema when converting a scoped problem and literature gaps into a study design.

## Minimal shape

```json
{
  "topic": "Retrieval-grounded agent support for literature review writing",
  "manuscript_type": "proposal-style-manuscript",
  "study_completion_status": "design-only",
  "target_contribution": "Explain how grounding mechanisms affect review quality and citation reliability.",
  "theoretical_lens": "sociotechnical systems",
  "research_questions": [
    "How do grounding mechanisms change citation faithfulness in review drafting systems?",
    "What tradeoff exists between coverage and controllability?"
  ],
  "hypotheses": [
    "Systems with explicit evidence retrieval produce fewer unsupported claims.",
    "Stronger grounding reduces writing fluency less than users expect when workflow design is good."
  ],
  "method_candidates": [
    "comparative experiment",
    "artifact evaluation",
    "mixed-method user study"
  ],
  "data_sources": [
    "benchmark review-writing tasks",
    "human evaluation rubrics",
    "retrieval logs"
  ],
  "constraints": [
    "limited access to domain experts",
    "no proprietary dataset"
  ]
}
```

## Field rules

- `topic`: scoped study topic.
- `manuscript_type`: one of `conceptual-paper`, `literature-review-paper`, `proposal-style-manuscript`, or `empirical-paper`.
- `study_completion_status`: one of `design-only`, `partial-results`, or `completed-study`.
- `target_contribution`: what the study should add beyond existing literature.
- `theoretical_lens`: optional, but useful in social science or management contexts.
- `research_questions`: the central questions the study must answer.
- `hypotheses`: include only when hypothesis testing is appropriate.
- `method_candidates`: shortlist of plausible methods, not a wish list.
- `data_sources`: real candidate data or evidence sources.
- `constraints`: practical limits that affect feasibility.

## Design semantics

- If `manuscript_type` is `proposal-style-manuscript`, the output should emphasize study plan, feasibility, and open dependencies rather than finished findings.
- If `manuscript_type` is `conceptual-paper`, propositions may be appropriate, but they should still map to a defendable mechanism and literature gap.
- Use `empirical-paper` only when `study_completion_status` is `completed-study` or the user provides finished results.
