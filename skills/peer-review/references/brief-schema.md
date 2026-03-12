# Peer Review Brief Schema

Use this schema when the skill wants a structured handoff from a user-provided paper draft to a review report.

## Minimal shape

```json
{
  "title": "Retrieval-Grounded Agent Systems for Automated Related-Work Drafting",
  "domain": "computer science",
  "venue_target": "conference",
  "paper_type": "empirical",
  "language": "zh-CN",
  "review_style": "balanced",
  "review_depth": "standard",
  "input_completeness": "full-paper",
  "focus_areas": [
    "novelty",
    "technical soundness",
    "empirical quality",
    "clarity",
    "significance"
  ],
  "content": {
    "abstract": "This paper proposes ...",
    "introduction": "We study ...",
    "method": "Our method consists of ...",
    "experiments": "We evaluate on ...",
    "conclusion": "Results show ..."
  },
  "claims": [
    "The paper proposes a retrieval-grounded agent pipeline for related-work drafting.",
    "The method improves citation faithfulness compared with baseline LLM generation."
  ],
  "known_constraints": [
    "Related work section not provided",
    "Appendix and implementation details unavailable"
  ],
  "target_output": "full reviewer report with simulated recommendation"
}
```

## Field rules

- `title`: Use the paper title if available. If missing, create a short working label.
- `domain`: Broad field label such as `computer science`, `management`, or `biomedicine`.
- `venue_target`: Optional. Use the user's target venue if provided; otherwise use `unknown`.
- `paper_type`: Choose the closest type from the visible content.
- `language`: Follow the user's language when possible.
- `review_style`: Usually `balanced`, `strict`, or `supportive`.
- `review_depth`: `quick`, `standard`, or `deep`.
- `input_completeness`: `full-paper`, `partial-paper`, or `abstract-only`.
- `focus_areas`: Optional priority dimensions the user cares about.
- `content`: Include only what the user actually provided.
- `claims`: Short list of the paper's own stated or strongly implied contributions.
- `known_constraints`: Missing sections, unreadable figures, missing appendix, or absent baselines.
- `target_output`: Short description such as `review memo`, `rebuttal prep`, or `full reviewer report`.

## Interpretation rules

- If only `abstract` is present, set `input_completeness` to `abstract-only`.
- If method and experiments are both missing, avoid strong soundness claims.
- If the user names a venue but gives no reviewing rubric, use general standards and mention that the review is not venue-calibrated.
- If the user explicitly asks for a recommendation label, always provide one and pair it with a confidence note.

## Writing semantics

- The brief controls review scope, not factual certainty.
- Every major criticism should point to visible evidence or a clearly stated missing verification point.
- If the paper content is partial, convert hard claims into risks, open questions, or conditional concerns.
