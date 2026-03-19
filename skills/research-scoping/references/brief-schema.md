# Scoping Brief Schema

Use this schema when the skill needs a structured handoff from a vague research request to an executable brief.

## Minimal shape

```json
{
  "topic": "Agentic systems for academic literature synthesis",
  "objective": "Narrow the topic into a thesis-ready question set and retrieval plan.",
  "target_artifact": "research brief",
  "language": "zh-CN",
  "domain": "information systems",
  "time_window": {
    "from_year": 2021,
    "to_year": 2026
  },
  "questions": [
    "Which parts of the literature review workflow are already supported by agentic systems?",
    "How do these systems evaluate citation faithfulness and evidence grounding?",
    "What practical gaps remain for thesis or paper writing support?"
  ],
  "keywords": [
    "agentic system",
    "literature synthesis",
    "scientific writing",
    "citation faithfulness"
  ],
  "in_scope": [
    "systems for literature discovery, screening, synthesis, or related-work drafting",
    "papers in English and Chinese"
  ],
  "out_of_scope": [
    "general-purpose chatbots with no research workflow component",
    "non-academic content generation tools"
  ],
  "next_skill": "literature-review"
}
```

## Field rules

- `topic`: one-sentence normalized topic.
- `objective`: what the user is trying to achieve with the scoped topic.
- `target_artifact`: the next artifact to create, such as `research brief`, `proposal`, or `retrieval plan`.
- `language`: follow the user's language.
- `domain`: broad field label.
- `time_window`: optional, but recommended when the topic is fast-moving.
- `questions`: 2-4 concrete questions are enough.
- `keywords`: plain-language search terms for later retrieval.
- `in_scope` and `out_of_scope`: practical boundaries, not ceremonial statements.
- `next_skill`: usually `paper-tracker`, `literature-review`, or `research-design`.
