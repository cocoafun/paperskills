# Search Brief Schema

Use this schema when the skill wants a structured retrieval plan that can be passed to local scripts.

## Minimal shape

```json
{
  "window": {
    "from": "2026-03-05",
    "to": "2026-03-12"
  },
  "filters": {
    "journals": [],
    "authors": [],
    "topics": [],
    "domain": ""
  },
  "limit": 10,
  "include_preprints": false,
  "registry_path": "skills/paper-tracker/examples/om-or-journal-registry.md"
}
```

## Field rules

- `window`: either explicit `from` and `to`, or `days`.
- `filters.journals`: journal titles exactly as named by the user.
- `filters.authors`: author names as strings. Do not assume a stable author ID exists.
- `filters.topics`: keyword phrases.
- `filters.domain`: a higher-level field label. It is used as a retrieval query only when `topics` is empty; otherwise it stays as ranking context, not a taxonomy ID.
- `limit`: final shortlist size.
- `include_preprints`: if `false`, local postprocessing excludes obvious preprint sources such as arXiv.
- `registry_path`: optional markdown registry with journal to ISSN mapping.

## Retrieval semantics

- If `journals` is present, prefer journal-bounded retrieval by ISSN.
- If `authors` is present, use author-name query retrieval.
- If `topics` or `domain` is present, use keyword retrieval.
- Multiple filters are additive. The pipeline retrieves from each route, then dedupes.
