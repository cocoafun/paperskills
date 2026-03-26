---
name: paper-tracker
description: Track newly published papers from specified journals, venues, keywords, authors, institutions, or domains within a time window. Produces a one-shot summary report in Markdown or HTML.
---

Track newly published papers for "$ARGUMENTS".

Input may specify:
- **Time window**: `1 day`, `1 week`, `1 month`, `last 90 days`, or explicit dates such as `2026-01-01 to 2026-03-01`
- **Scope**: one or more of domain, keywords, journals, venues, authors, institutions
- **Output**: quick list, HTML report, or markdown report

Examples:
- `track papers from Nature and Science in the last month`
- `追踪 Geoffrey Hinton 和 Yann LeCun 过去 30 天的新论文`
- `track new LLM safety papers from CMU and Stanford between 2026-01-01 and 2026-03-15`

## MAIN FLOW

```
Main Session — coordination
  │
  ├── STEP 1: Normalize tracking request (self)
  ├── STEP 2: Query primary source by scope (self)
  ├── STEP 3: Merge, deduplicate, and filter to time window (self)
  ├── STEP 4: Enrich every matched paper with abstracts / links (self)
  └── STEP 5: Produce one-shot summary report
```

Do NOT use subagents unless the user explicitly asks for broader comparative analysis.

## STEP 1: Normalize Tracking Request

Extract:
- **Window type**: relative (`1 week`) or explicit dates
- **Date field**: prefer online publication / publication date; if unavailable, use indexed date and state that fallback
- **Track entities**:
  - authors
  - institutions
  - journals / venues
  - keywords
  - domain or discipline
- **Language**: follow explicit user request; otherwise infer from the prompt
- **Output format**:
  - short answer in chat
  - HTML report
  - markdown report

If the user gives no date window, default to the last 30 days and state that assumption.

## STEP 2: Query Sources

Use **OpenAlex as the primary source** because it supports filters for authors, institutions, sources, concepts, and date ranges.

### OpenAlex — works search

Use the smallest number of focused calls that match the scope. Prefer filters over broad text search.

Examples:

**Author**
```text
https://api.openalex.org/authors?search={author_name}&per_page=5&mailto=paperskills@example.com
https://api.openalex.org/works?filter=author.id:{author_id},from_publication_date:{start},to_publication_date:{end}&sort=publication_date:desc&per_page=50&mailto=paperskills@example.com
```

**Institution**
```text
https://api.openalex.org/institutions?search={institution_name}&per_page=5&mailto=paperskills@example.com
https://api.openalex.org/works?filter=institutions.id:{institution_id},from_publication_date:{start},to_publication_date:{end}&sort=publication_date:desc&per_page=50&mailto=paperskills@example.com
```

**Journal / Venue**
```text
https://api.openalex.org/sources?search={journal_name}&per_page=5&mailto=paperskills@example.com
https://api.openalex.org/works?filter=primary_location.source.id:{source_id},from_publication_date:{start},to_publication_date:{end}&sort=publication_date:desc&per_page=50&mailto=paperskills@example.com
```

**Keyword / Domain**
```text
https://api.openalex.org/works?search={query}&filter=from_publication_date:{start},to_publication_date:{end}&sort=publication_date:desc&per_page=50&mailto=paperskills@example.com
```

When the user gives multiple scopes, run multiple focused queries and merge them.

### Abstract and metadata enrichment

For every matched paper, make a best effort to fetch an abstract.

Priority:
1. Use OpenAlex abstract data if available
2. If OpenAlex lacks a usable abstract, query Semantic Scholar by DOI or title
3. If still missing, keep the paper and mark abstract as unavailable

Use Semantic Scholar as the primary fallback:

```text
https://api.semanticscholar.org/graph/v1/paper/search?query={title_or_doi}&limit=1&fields=title,abstract,authors,year,venue,externalIds,openAccessPdf
```

Use Crossref only when the item is missing publication date or DOI metadata:

```text
https://api.crossref.org/works?query.title={title}&rows=3
```

## STEP 3: Merge and Filter

1. Normalize DOI
2. Deduplicate by DOI; if DOI missing, fuzzy-match titles
3. Keep only items inside the requested window
4. Record **why each paper matched**:
   - matched author
   - matched journal
   - matched institution
   - matched keyword
5. If a paper matches multiple scopes, keep all reasons

Sort primarily by publication date descending.
Use citation count only as a secondary tie-breaker.

## STEP 4: Build Tracking Summary

For each paper keep:
- title
- authors
- publication date
- journal / venue
- matched reason
- DOI
- abstract
- 2-4 sentence abstract snippet for summary blocks
- open access / PDF link if available

Also compute:
- total papers found
- papers by day or week in the window
- top journals / venues in the matched set
- most frequent authors in the matched set
- keyword themes inferred from titles / abstracts

## STEP 5: Output Report

Default output is a single-file HTML report. Read `shared/report-template.md` first and follow that design system exactly.

For HTML reports include:
- header with scope and date range
- executive summary
- stats bar
- paper list or paper cards
- for each paper: metadata row plus abstract block
- short thematic observations
- methodology / coverage note

Suggested filename:
`reports/{date}-paper-tracker-{slug}.html`

If the user explicitly asks for Markdown, use this structure:

```markdown
# Paper Tracking Report

## Tracking Scope
- Window: 2026-02-01 to 2026-02-29
- Journals: Nature, Science
- Keywords: large language model safety

## Executive Summary
- 14 papers matched
- Most active venue: Nature Machine Intelligence
- Main themes: evaluation, alignment, red teaming

## New Papers
### 1. Paper Title
- Date: 2026-02-03
- Authors: A, B, C
- Venue: Nature
- Match Reason: journal + keyword
- DOI: 10.xxxx/xxxx
- Abstract: ...

## Observations
- Short trend summary
- Notable new authors / labs
- Gaps or caveats in coverage
```

## LANGUAGE

Determine report language:
- If the user explicitly requests a language (for example `in Chinese`, `用中文`): use that language
- Otherwise infer from the prompt
- Default to English if mixed or unclear

When generating in Chinese:
- Set `<html lang="zh">`
- Use Chinese headings and labels
- Keep journal names, DOI, and API names in original form
- Use Chinese punctuation

## COVERAGE RULES

- Treat this as a **freshness-first** task: prioritize newest papers over highly cited historical papers
- Prefer publication date over citation count
- State clearly when a result is an early-access / online-first publication
- If the exact journal / author resolution is ambiguous, show the top candidate and mention the ambiguity
- If the requested scope resolves to zero results, broaden carefully and explain what changed

## ERROR HANDLING

- OpenAlex search ambiguity: show the resolved entity before listing papers
- Missing abstracts: continue, do not block the report; show `Abstract unavailable`
- Missing DOI: keep the paper with source URL
- Rate limiting: reduce page size and retry once
- Sparse metadata across APIs: keep the report factual and note incomplete fields

## TOKEN BUDGET

- Normal run: ~20-35K
- Multi-scope tracking with HTML report: ~30-45K
