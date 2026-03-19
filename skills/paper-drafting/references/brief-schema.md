# Draft Brief Schema

Use this schema when generating an outline or draft from structured research inputs.

## Minimal shape

```json
{
  "paper_goal": "Conference paper draft on retrieval-grounded literature review agents",
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
- `audience`: intended readers.
- `venue_target`: optional but useful for tone and structure.
- `sections`: required list of sections to draft or plan.
- `claims`: statements that the section must support.
- `evidence`: the source groups, papers, or notes that support the section.
