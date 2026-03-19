# Workflow Example: Review To Revision

This example shows the critique-and-revision branch of PaperSkills.

## User request

`这是我的论文摘要、方法和审稿意见，帮我判断问题并生成修改计划。请用英文输出。`

## Stage 1: `using-paperskills`

- Detect that the request spans critique and revision.
- Start with `peer-review` if the paper still needs diagnosis.
- Start with `revision-planning` if the review comments are already the main artifact.
- Normalize `language: en` for the critique and revision outputs.

## Stage 2: `peer-review`

- Assess novelty, soundness, empirical quality, clarity, and significance.
- Produce reviewer-style strengths and weaknesses.
- Keep the review report in English.

## Stage 3: `revision-planning`

- Normalize comments into issue units.
- Produce a prioritized revision table.
- Separate paper changes from response-letter strategy.
- Keep `language: en` in the revision brief and rendered plan.

Suggested artifact:

- `skills/revision-planning/examples/reviewer-comments-brief.json`

## Expected workflow property

`revision-planning` should not promise fixes that require unavailable experiments or missing paper sections.
