# Review Brief Schema

Use this schema when the skill wants a structured handoff from a user's topic description to a review draft.

## Minimal shape

```json
{
  "topic": "Large-language-model systems for automated literature review generation",
  "objective": "Summarize methods, evaluation patterns, and open reliability issues.",
  "review_type": "narrative",
  "language": "zh-CN",
  "citation_style": "APA",
  "depth": "standard",
  "window": {
    "from_year": 2020,
    "to_year": 2026
  },
  "questions": [
    "How do current systems perform retrieval, screening, synthesis, and writing?",
    "How is review quality and citation faithfulness evaluated?",
    "What gaps remain in grounding, coverage, and workflow integration?"
  ],
  "keywords": [
    "large language model",
    "literature review",
    "scientific writing",
    "evidence synthesis"
  ],
  "concept_groups": [
    {
      "name": "model",
      "terms": ["large language model", "LLM", "foundation model"]
    },
    {
      "name": "task",
      "terms": ["literature review", "related work generation", "scientific writing"]
    }
  ],
  "source_preferences": [
    "Semantic Scholar",
    "OpenAlex",
    "arXiv"
  ],
  "inclusion_criteria": [
    "Peer-reviewed papers or clearly labeled preprints",
    "Methods or studies directly addressing the topic",
    "English or Chinese full text or abstract"
  ],
  "exclusion_criteria": [
    "Pure marketing pages or product announcements",
    "Duplicate versions without better metadata",
    "Papers only weakly related to the target problem"
  ],
  "target_length": "2500-4000 words"
}
```

## Field rules

- `topic`: Short natural-language statement of the review target.
- `objective`: What the review should help the user do.
- `review_type`: Usually `narrative`, `scoping`, `systematic`, or `related-work`.
- `language`: Follow the user's language when possible.
- `citation_style`: Only the final formatting choice. It does not change retrieval.
- `depth`: `quick`, `standard`, or `deep`.
- `window`: Use `from_year` and `to_year` unless the user gives exact dates.
- `questions`: 2-4 review questions are enough. If absent, infer them from the topic.
- `keywords`: Plain retrieval phrases.
- `concept_groups`: Optional but preferred for generating boolean queries.
- `source_preferences`: Ordered list of preferred databases or discovery layers.
- `inclusion_criteria` and `exclusion_criteria`: Keep these practical, not ceremonial.
- `target_length`: Word range or a short output label such as `section`, `full review`, or `thesis chapter`.

## Retrieval semantics

- If `concept_groups` is present, use it to build boolean search strings.
- If `source_preferences` is empty, choose sources from the domain in the topic.
- If `window` is missing, default to the last 5 years plus older seminal work when needed.
- If the user names seed papers, add a `seed_papers` array and use citation chaining.

## Writing semantics

- The brief controls scope, not truth. All facts still require sources.
- If the corpus is small or weak, produce an exploratory draft and say so.
- If only metadata is available, stop short of strong comparative claims.
