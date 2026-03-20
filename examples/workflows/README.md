# Workflow Examples

These examples show how PaperSkills should chain stages together.

- `idea-to-draft.md`: early-stage research idea to scoped draft workflow
- `full-paper-from-topic.md`: topic-only request to final manuscript workflow
- `review-to-revision.md`: critique and revision workflow

Each workflow may carry a shared `language` field across stages, such as `zh-CN` or `en`.

Each workflow run should also persist its intermediate artifacts under a task-local run directory such as:

```text
artifacts/paperskills/<run-id>/stages/
```

If a user runs only one stage from these examples, that stage should still produce a self-contained stored brief and output package.
