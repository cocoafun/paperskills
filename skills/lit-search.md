Search academic literature for "$ARGUMENTS".

Do NOT use subagents — do this yourself directly.

## STEP 1: Generate Search Queries

From "$ARGUMENTS", generate 3-5 search variants:
- Original query as-is
- Synonyms / related terms
- Broader category
- More specific sub-topic
- If non-English: English equivalent too

## STEP 2: Detect Discipline

Infer from query keywords:
- Medical/bio terms → include PubMed
- CS/math/physics → include arXiv
- Social sciences/humanities → Semantic Scholar + OpenAlex only
- Unclear → search Semantic Scholar + OpenAlex (always)

## STEP 3: Search APIs (parallel WebFetch calls)

### Semantic Scholar (always)
```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=20&fields=title,authors,year,venue,citationCount,abstract,externalIds,openAccessPdf
```

### OpenAlex (always)
```
WebFetch: https://api.openalex.org/works?search={query}&per_page=20&sort=cited_by_count:desc&mailto=paperskills@example.com
```

### PubMed (biomedical only)
```
WebFetch: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmax=20&retmode=json
Then: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid_list}&retmode=json
```

### arXiv (CS/math/physics only)
```
WebFetch: https://export.arxiv.org/api/query?search_query=all:{query}&max_results=20&sortBy=relevance
```
Response is Atom XML — parse `<entry>` elements.

## STEP 4: Deduplicate and Merge

1. Normalize DOIs (lowercase, strip URL prefix)
2. Group by DOI — keep richest metadata
3. No DOI: fuzzy match by title (>80% similarity)
4. Keep one record per paper

## STEP 5: Rank and Present

Sort by: relevance score × log(citationCount + 1)

Display:

| # | Authors | Title | Year | Venue | Cites | DOI | OA |
|---|---------|-------|------|-------|-------|-----|----|
| 1 | Smith, Jones | Deep learning for... | 2023 | Nature | 1,204 | 10.1038/... | PDF |

Show top 20. For each with abstract, show first 100 words.

## STEP 6: Offer Next Actions

- "Expand any of these? I can fetch full details + references."
- "Build a citation network? (/citation-network DOI1 DOI2)"
- "Generate a literature review outline from these?"
- "Save results to file? (markdown table)"

## ERROR HANDLING
- 429: wait 60s, retry. If persistent, skip that API.
- 0 results on all APIs: suggest broader terms
- Non-Latin script: try transliterated version
- arXiv XML parse error: skip, note in output

## TOKEN BUDGET
- Direct execution (no subagent): ~15-25K total
- API responses: ~1-2K per call
- Abstract display: ~5K if all 20 shown
