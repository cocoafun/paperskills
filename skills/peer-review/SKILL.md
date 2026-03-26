---
name: peer-review
description: Perform academic peer review with 8-criteria scoring (originality, argument, literature, discussion, consistency, methodology, presentation, evidence). Generates HTML report with radar chart.
---

Perform an academic peer review of "$ARGUMENTS".

Resolve file path:
- Filename only: look in current working directory
- Full path: use as-is
- .docx: extract text with `pandoc -t plain "$ARGUMENTS"` first

## MAIN FLOW

```
Main Session — coordination only, does NOT read the manuscript
  │
  ├── 1a. Subagent → read manuscript + evaluate 8 criteria (parallel)
  ├── 1b. Subagent → search for missing references via public APIs (parallel)
  │
  └── 2. Report subagent → combine 1a + 1b → HTML report + open
```

1a and 1b run IN PARALLEL. Main session stays clean.

## STEP 1a: Manuscript Evaluation (subagent)

Launch subagent. Prompt:

```
TASK: Evaluate this manuscript to peer-review standards.
FILE: {file_path}

Read with Read tool. Analyze:

### STRUCTURAL ANALYSIS
- Title, author(s), section count, estimated word count
- Reference/footnote count and distribution across sections
- Clear thesis statement in introduction?
- Conclusion aligns with introductory promises?
- Abstract present and accurate?

### 8 CRITERIA (each: 1-5 score + justification + specific suggestion)

K1 ORIGINALITY: What does this contribute? Novel argument, new data, synthesis?
K2 ARGUMENT STRUCTURE: Thesis clear? Logical chain coherent? Repetition?
K3 LITERATURE COVERAGE: Source base adequate? Primary/secondary balance? Currency?
    Are key works in the field missing? Check by searching Semantic Scholar for the topic.
K4 DEPTH OF DISCUSSION: Counterarguments fairly represented? Author takes position?
    Is there genuine engagement with opposing views, or just listing them?
    Does the author clearly distinguish their own position from others'?
K5 CONCEPTUAL CONSISTENCY: Terminology consistent? Translations correct?
    If multilingual: are foreign-language terms used consistently with standard equivalents?
K6 METHODOLOGY: Method stated? Source/data selection justified?
K7 PRESENTATION: Academic language, paragraph lengths, footnote/text balance?
K8 EVIDENCE: Claims supported? Unsupported assertions?

### STRENGTHS (5-6 items, specific)
### AREAS FOR IMPROVEMENT (5-6 items, each with concrete suggestion)
### SECTION-BY-SECTION NOTES (1-2 sentences per section)

### CITATION SPOT-CHECK (pick 5 key claims)
For 5 central claims that rely heavily on a citation:
- Does the cited source actually support what the manuscript says?
- Is the author citing someone's own view, or their report of another's view?
- Any signs of overstatement, misattribution, or approval/critique confusion?
(This is a quick sample — full verification via /cite-verify)

### RECOMMENDATION: Accept / Minor revisions / Major revisions / Reject

OUTPUT: Plain text with tables. Also list all cited authors/works.
```

## STEP 1b: Missing Reference Detection (subagent, parallel)

Launch subagent. Prompt:

```
TASK: Find potentially missing references for a manuscript about "{topic}".

EXISTING AUTHORS: {list from 1a or grep from main session}

Search these PUBLIC APIs using WebFetch:

### Semantic Scholar (no auth needed)
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=20&fields=title,authors,year,venue,citationCount,abstract,externalIds

Run 3-5 query variants (different angles on the topic).

### OpenAlex (no auth, add mailto=)
WebFetch: https://api.openalex.org/works?search={query}&per_page=20&sort=cited_by_count:desc&mailto=paperskills@example.com

### CrossRef (no auth)
WebFetch: https://api.crossref.org/works?query={query}&rows=10&sort=relevance

PROCESS:
1. Generate 3-5 search queries from topic (core, broader, methodological, recent)
2. Search all three APIs per query
3. Deduplicate by DOI or title similarity
4. Filter out works already cited in manuscript
5. Rank by citation count × relevance
6. Return top 15 missing references

OUTPUT:
| # | Author(s) | Title | Venue/Year | Citations | Why Relevant |
```

## STEP 2: HTML Report (subagent)

Combine 1a + 1b results. Write HTML report:

```
File: reports/{date}-peer-review-{manuscript-name}.html

DESIGN:
- Radar chart for 8 criteria scores (Chart.js)
- Color-coded scores: green (4-5), yellow (3), red (1-2)
- Collapsible sections (details/summary)
- Missing references table
- Print-friendly

Open with: open {file_path}
```

## STEP 3: Next Actions

Ask user:
- "Verify citations? (/cite-verify {file})"
- "Search literature on specific gaps? (/lit-search {topic})"
- "Generate abstract? (/abstract {file})"

## ERROR HANDLING
- 429 rate limit: wait 60s, retry once
- 0 API results: broaden query terms
- API down: skip, note in report
- .docx without pandoc: tell user to install or convert to .md

## TOKEN BUDGET
- Main: ~2K (coordination)
- 1a subagent: ~15-30K (manuscript + evaluation)
- 1b subagent: ~10-20K (API calls + dedup)
- Report subagent: ~5-10K
- Total: ~35-60K

## LANGUAGE

Determine report language:
- If the user explicitly requests a language (e.g., "in Chinese", "用中文"): use that language
- If the manuscript/input is primarily in Chinese: default to Chinese
- Otherwise: default to English

When generating in Chinese:
- Set `<html lang="zh">` on the HTML document
- Write all headings, labels, descriptions, and analysis text in Chinese
- Keep technical terms in original form (DOI, journal names, API names)
- Use Chinese punctuation (，。、；：)
- stat-label text in the stats bar should be Chinese (e.g., "综合评分" not "Overall Score")
- Badge text should be Chinese (e.g., "小修通过" not "MINOR REVISIONS", "接受" not "ACCEPT")
- Criteria names in Chinese (e.g., "K1 原创性", "K2 论证结构", "K3 文献覆盖", "K4 讨论深度", "K5 概念一致性", "K6 方法论", "K7 表达规范", "K8 论据支撑")

## REPORT DESIGN
When writing the HTML report, read and follow the design system in `assets/report-template.md` (in the paperskills root directory) EXACTLY.
Do NOT use Tailwind CDN. Use the custom CSS variables, Crimson Pro font, and academic book aesthetic defined there.
