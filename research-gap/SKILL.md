---
name: research-gap
description: Analyze and identify research gaps in a field using Semantic Scholar and OpenAlex trend data. Covers temporal, methodological, thematic, application, and population gaps. Generates HTML report with Chart.js visualizations.
---

Analyze research gaps for "$ARGUMENTS".

## MAIN FLOW

```
Main Session — coordination
  │
  ├── STEP 1: Subagent → comprehensive literature search + trend data
  ├── STEP 2: Subagent → identify gaps from landscape data
  └── STEP 3: Report subagent → HTML gap analysis report
```

## STEP 1: Literature Landscape (subagent)

Launch subagent:

```
TASK: Map the research landscape for "{topic}".

Generate 5 search queries:
1. Core topic (exact)
2. Broader field
3. Methodology-focused
4. Application-focused
5. "{topic} challenges OR future OR limitations"

### Semantic Scholar — recent + highly cited
For each query:
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=40&fields=title,authors,year,venue,citationCount,abstract,fieldsOfStudy&year=2019-2026

### OpenAlex — publication trends over time
WebFetch: https://api.openalex.org/works?search={core_query}&group_by=publication_year&mailto=paperskills@example.com

### OpenAlex — concept trends
WebFetch: https://api.openalex.org/concepts?search={topic}&mailto=paperskills@example.com

### OpenAlex — recent vs old comparison
Recent: https://api.openalex.org/works?search={topic}&filter=publication_year:2023-2026&per_page=20&sort=cited_by_count:desc&mailto=paperskills@example.com
Old: https://api.openalex.org/works?search={topic}&filter=publication_year:2010-2015&per_page=20&sort=cited_by_count:desc&mailto=paperskills@example.com

COLLECT:
- Paper count per year (2010-2026)
- Top 30 papers by citations (all time)
- Top 20 papers from last 2 years
- Top venues
- Key authors (most papers + most cited)
- Related concepts/subfields
- Abstracts of top 30 papers (for theme extraction)
```

## STEP 2: Gap Identification (subagent)

Launch subagent with landscape data:

```
TASK: Identify research gaps.

LANDSCAPE DATA:
{output from step 1}

ANALYZE:

### A. Temporal Gaps
- Topics studied 5+ years ago but NOT recently revisited
- Declining publication count despite unresolved questions
- Emerging topics with <5 papers

### B. Methodological Gaps
- Mostly theoretical → empirical gap
- Mostly quantitative → qualitative gap
- Mostly single-country → comparative gap
- No meta-analyses/reviews → synthesis gap

### C. Thematic Gaps
- Extract themes from top paper abstracts
- Find theme COMBINATIONS that don't appear
  (e.g., "fairness + NLP" has 200 papers, "fairness + speech" has 3)
- Disconnected clusters that should connect

### D. Application Gaps
- Theory exists but no applied/practical studies
- Applied in one domain but not another

### E. Population/Context Gaps
- Geographic: studied in US/EU but not elsewhere?
- Demographic: adults but not children?
- Domain: medicine but not law?

### F. Contradictions
- Opposing findings on same question
- Unresolved theoretical debates

OUTPUT per gap:
- Gap description (1-2 sentences)
- Evidence: what exists vs. what's missing (with paper counts)
- Suggested research question
- Feasibility: data availability, method needed
- Impact: high/medium/low
- Priority: 1 (most promising) to 3 (niche)
```

## STEP 3: HTML Report (report subagent)

```
File: reports/{date}-research-gap-{topic}.html

SECTIONS:
1. Executive Summary — top 5 gaps, prioritized
2. Literature Landscape
   - Chart.js line chart: papers per year
   - Top venues table
   - Key authors table
   - Related concepts as tag cloud
3. Gap Analysis
   - Each gap as a card with evidence, questions, priority badge
   - Color: red=high priority, yellow=medium, blue=niche
4. Suggested Research Questions (numbered)
5. Methodology Notes & Limitations

Open with: open {file_path}
```

## STEP 4: Next Actions

- "Deep-dive a specific gap? (/lit-search {gap topic})"
- "Check if a gap was recently addressed?"
- "Draft a research proposal outline for one of these gaps?"

## API REFERENCE

### OpenAlex Group-By (trends)
```
Papers per year: /works?search={topic}&group_by=publication_year
By OA status: /works?search={topic}&group_by=open_access.is_oa
By type: /works?search={topic}&group_by=type
```

### OpenAlex Concepts
```
/concepts?search={topic} → related concepts, works_count, description
```

### Semantic Scholar Recommendations
```
/recommendations/v1/papers/forpaper/{paperId}?limit=20&fields=title,authors,year,citationCount,abstract
```

## ERROR HANDLING
- Topic too broad (>100K papers): ask user to narrow
- Topic too narrow (0-5 papers): broaden, check spelling
- Trend data gaps: note which years incomplete
- Abstract coverage: not all papers have abstracts in API

## TOKEN BUDGET
- Main: ~3K (coordination)
- Landscape subagent: ~25-40K
- Gap analysis subagent: ~15-25K
- Report subagent: ~10-15K
- Total: ~55-85K (most intensive skill)
- If landscape output too large: summarize before passing to gap analysis

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
- stat-label text in the stats bar should be Chinese (e.g., "论文总数" not "Total Papers")
- Badge text should be Chinese (e.g., "高优先级" not "HIGH PRIORITY", "方法缺口" not "METHODOLOGICAL GAP")

## REPORT DESIGN
When writing the HTML report, read and follow the design system in `shared/report-template.md` (in the paperskills root directory) EXACTLY.
Do NOT use Tailwind CDN. Use the custom CSS variables, Crimson Pro font, and academic book aesthetic defined there.
