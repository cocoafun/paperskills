---
name: paperskills
description: Academic paper and literature workflow. Use when the user needs help with topic framing, research question sharpening, paper title convergence, paper writing, literature search, research gaps, citation checking, peer review, journal matching, paper tracking, abstracts, or academic report generation. Triggers: paper, manuscript, topic framing, research question, paper title, literature review, abstract, peer review, citation, journal, research gap, paper tracker, paper tracking.
---

# PaperSkills

Use this skill as the entry point for academic research and paper-writing tasks.

## When To Use

Use PaperSkills when the user asks to:

- Frame a research topic or converge on a paper title
- Search or map literature
- Identify research gaps
- Verify citations or supporting evidence
- Draft or revise abstracts
- Perform peer review
- Match a manuscript to journals
- Track newly published papers for specific journals, authors, venues, institutions, or keywords
- Generate academic-style reports

## Workflow

1. Identify the user's immediate task.
2. Invoke the relevant sub-skill below.
3. Follow that skill's procedure closely.
4. If the task spans multiple stages, complete the current stage first and then propose the next one.

## Reference Routing

- For topic framing, research question sharpening, or title convergence: use `/topic-framing` skill
- For abstract writing: use `/abstract` skill
- For literature search: use `/lit-search` skill
- For citation verification: use `/cite-verify` skill
- For citation network analysis: use `/citation-network` skill
- For journal matching: use `/journal-match` skill
- For paper tracking and periodic paper watchlists: use `/paper-tracker` skill
- For research gap analysis: use `/research-gap` skill
- For peer review: use `/peer-review` skill
- For report design or HTML report generation: read `shared/report-template.md` (in the paperskills root directory)

## Notes

- Keep the entry skill concise; do not load all sub-skills unless needed.
- Prefer direct execution for simple drafting tasks.
- Use public web sources only when the selected skill explicitly requires current literature or citation checks.
