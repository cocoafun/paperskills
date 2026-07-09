---
name: citation-network
description: Build and visualize citation networks from seed papers using Semantic Scholar and OpenCitations. Generates interactive HTML report with vis.js network graph.
---

Build a citation network from "$ARGUMENTS".

Input can be:
- One or more DOIs: "10.1038/s41586-023-06221-2"
- Paper titles: "Attention is All You Need"
- Mix: "10.1038/... + transformer architecture survey"

## MAIN FLOW

```
Main Session — coordination
  │
  ├── STEP 1: Resolve seed papers (self)
  ├── STEP 2: Subagent → fetch references + citations, build network
  ├── STEP 3: Subagent → identify key nodes + clusters
  └── STEP 4: Report subagent → HTML visualization with vis.js
```

## STEP 1: Resolve Seed Papers (self)

For each input:

**If DOI:**
```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=paperId,title,authors,year,venue,citationCount,references.paperId,references.title,references.authors,references.year,references.citationCount,references.externalIds,citations.paperId,citations.title,citations.authors,citations.year,citations.citationCount,citations.externalIds
```

**If title:**
```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={title}&limit=1&fields=paperId,title,authors,year
```
Then use paperId for full fetch above.

## STEP 2: Build Network (subagent)

Launch subagent:

```
TASK: Build a citation network from seed papers.

SEED PAPERS (with references and citations):
{data from step 1}

PROCESS:
1. List each seed's references (backward) and citations (forward)

2. Find OVERLAP: papers appearing in multiple seeds' lists
   These are KEY PAPERS in the field.

3. For top 10 most-connected papers, fetch their refs too (1 level deeper):
   WebFetch: https://api.semanticscholar.org/graph/v1/paper/{paperId}?fields=title,authors,year,citationCount,references.title,references.citationCount

4. Also check OpenCitations for additional links:
   WebFetch: https://opencitations.net/index/api/v2/citations/{doi}
   WebFetch: https://opencitations.net/index/api/v2/references/{doi}

5. Identify clusters:
   - Methodological (shared methods)
   - Temporal (foundational vs. recent)
   - Thematic (shared topic keywords)

OUTPUT:
- Node list: [{id, title, authors, year, citations, role: seed|key|bridge|peripheral}]
- Edge list: [{source, target, type: cites}]
- Clusters: [{name, papers, description}]
- Key papers: top 10 by connectivity
- Foundational works: highly cited, >10 years old
- Recent frontier: last 2 years, growing citations
```

## STEP 3: Insights (self or subagent)

From network data identify:
- **Seminal papers**: highest citations, referenced by most seeds
- **Bridge papers**: connect different clusters
- **Rising stars**: low total but high recent citations
- **Research front**: newest papers citing seeds

## STEP 4: HTML Visualization (report subagent)

```
File: reports/{date}-citation-network-{topic}.html

INCLUDES:
1. Network graph — vis.js (CDN: https://unpkg.com/vis-network/standalone/umd/vis-network.min.js)
   - Nodes sized by citation count
   - Colored by cluster
   - Seed papers highlighted (star shape)
   - Click node → details panel

2. Timeline view — horizontal, papers as dots on year axis
   - Connected by citation arrows
   - Colored by cluster

3. Key Papers table:
   | # | Title | Authors | Year | Cites | Role | Cluster |

4. Cluster summary cards

5. Statistics:
   - Total papers in network
   - Date range
   - Most prolific authors
   - Most common venues

After writing the file:
- Return the exact absolute file path to the user
- Ask whether they want it opened
- Only run `open {file_path}` after the user explicitly confirms
```

## API REFERENCE

### Semantic Scholar — Paper + Refs + Citations
```
GET /graph/v1/paper/{paperId}?fields=title,authors,year,venue,citationCount,references.title,references.authors,references.year,references.citationCount,references.externalIds,citations.title,citations.authors,citations.year,citations.citationCount,citations.externalIds

paperId formats: DOI:{doi}, PMID:{pmid}, CorpusId:{id}, or S2 paper ID
```

### Semantic Scholar Batch (efficient)
```
POST /graph/v1/paper/batch
Body: {"ids": ["DOI:10.1...", "DOI:10.2..."]}
?fields=title,authors,year,citationCount
Max 500 IDs per request.
```

### OpenCitations COCI
```
GET /index/api/v2/citations/{doi}
GET /index/api/v2/references/{doi}
Returns: [{citing, cited, creation, timespan}]
```

## ERROR HANDLING
- Seed not found: try alternative ID types (DOI → title search)
- >500 citations: note truncation, focus on top-cited
- vis.js CDN down: fall back to static table
- Rate limited: smaller batches with delays
- Circular citations: mark as bidirectional

## TOKEN BUDGET
- Main: ~5K (seed resolution)
- Network subagent: ~20-40K
- Visualization subagent: ~10K
- Total: ~35-55K
- LIMIT depth to 2 levels from seed to keep manageable

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
- stat-label text in the stats bar should be Chinese (e.g., "论文数量" not "Papers")
- Badge text should be Chinese (e.g., "核心论文" not "KEY PAPER", "桥梁论文" not "BRIDGE")

## REPORT DESIGN
When writing the HTML report, read and follow the design system in `assets/report-template.md` (in the paperskills root directory) EXACTLY.
Do NOT use Tailwind CDN. Use the custom CSS variables, Crimson Pro font, and academic book aesthetic defined there.
