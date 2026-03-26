---
name: abstract
description: Generate abstracts in multiple formats (IMRaD, thematic, extended, short) for academic manuscripts. Supports bilingual output for non-English papers.
---

Generate an abstract for "$ARGUMENTS".

Resolve file path:
- Filename only: look in current working directory
- Full path: use as-is

Do NOT use subagents — this is a pure LLM task, do it yourself.

## STEP 1: Read Manuscript

Read file with Read tool. Identify:
- Title
- Research question / thesis statement
- Methodology (if applicable)
- Key arguments / findings
- Conclusion

## STEP 2: Detect Discipline & Choose Format

- **STEM / empirical**: Use IMRaD format (Background, Objective, Methods, Results, Conclusion)
- **Humanities / law / theoretical**: Use thematic format (Context, Thesis, Approach, Argument, Contribution)
- If unclear: generate BOTH formats

## STEP 3: Generate All Variants

### A. Structured Abstract (IMRaD — for empirical/science papers)
```
Background: [1-2 sentences]
Objective: [1 sentence]
Methods: [1-2 sentences]
Results: [2-3 sentences]
Conclusion: [1-2 sentences]
Keywords: [5-7 terms]
```
~250 words

### B. Structured Abstract (for humanities/theoretical papers)
```
Context: [1-2 sentences — why this topic matters]
Thesis: [1 sentence — central argument]
Approach: [1-2 sentences — methodology, scope, sources]
Argument: [2-3 sentences — key steps]
Contribution: [1-2 sentences — what this adds to the field]
Keywords: [5-7 terms]
```
~250 words

### C. Unstructured Abstract (single paragraph)
~150 words — concise narrative

### D. Extended Abstract
~500 words — conference submission style

### E. Short Abstract
~50-75 words — for indexing/cataloging

## STEP 4: Bilingual (if applicable)

If manuscript is NOT in English:
- Generate all variants in original language AND English
- Label: "Abstract (Original)" / "Abstract (English)"

## STEP 5: Quality Checks

For each abstract verify:
- [ ] Contains main research question
- [ ] States methodology or approach
- [ ] Mentions key findings/arguments
- [ ] Does NOT include info not in manuscript
- [ ] No first person (unless discipline norm)
- [ ] No citations in abstract
- [ ] Stands alone — understandable without reading paper
- [ ] Keywords specific enough for discoverability

## STEP 6: Present

Show all variants with word counts. Ask:
- "Which format fits your target journal/conference?"
- "Adjust word count for a specific limit?"
- "Search keyword usage in literature? (/lit-search {keywords})"

## NOTES
- No API calls needed
- If manuscript has existing abstract: show COMPARISON of what's different
- Total tokens: ~10-20K depending on manuscript length
