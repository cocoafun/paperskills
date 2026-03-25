Recommend target journals for "$ARGUMENTS".

Input can be:
- Manuscript file path → read and analyze
- Abstract text → use directly
- Topic description → search based on topic

## MAIN FLOW

```
Main Session — coordination
  │
  ├── STEP 1: Extract manuscript profile (self)
  ├── STEP 2: Subagent → find similar papers + analyze venue distribution
  ├── STEP 3: Enrich journal metadata (self)
  └── STEP 4: Present ranked recommendations
```

## STEP 1: Manuscript Profile (self)

If file path given, read with Read tool. Extract:
- **Discipline**: law, CS, medicine, psychology, etc.
- **Sub-field**: criminal law theory, NLP, oncology, etc.
- **Methodology**: theoretical, empirical, mixed, review, meta-analysis
- **Scope**: country-specific, comparative, universal
- **Length**: word count estimate
- **Keywords**: 5-10 key terms
- **Language**: English, German, Turkish, etc.
- **Reference profile**: what journals do the references cite? (candidate journals)

## STEP 2: Find Similar Papers (subagent)

Launch subagent:

```
TASK: Find journals where similar research is published.

MANUSCRIPT PROFILE:
- Keywords: {keywords}
- Discipline: {discipline}
- Methodology: {methodology}
- Language: {language}

### Semantic Scholar — find similar papers
For 3 keyword combinations:
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={keywords}&limit=50&fields=title,venue,year,citationCount,externalIds
→ Extract venue from each result

### OpenAlex — venue analysis
WebFetch: https://api.openalex.org/works?search={keywords}&per_page=50&sort=cited_by_count:desc&mailto=paperskills@example.com
→ Group by venue, count papers per venue

### OpenAlex — journal details for top 15 venues
WebFetch: https://api.openalex.org/sources?filter=display_name.search:{journal_name}&mailto=paperskills@example.com
→ Gets: works_count, cited_by_count, h_index, type, is_oa, country

OUTPUT:
| Journal | Papers Found | Avg Citations | H-Index | OA? | Country | Scope Match (1-5) |
```

## STEP 3: Enrich Journal Data (self)

For top 10 journals:

### OpenAlex Sources
```
WebFetch: https://api.openalex.org/sources/{source_id}?mailto=paperskills@example.com
→ h_index, works_count, cited_by_count, is_oa, homepage_url, issn
```

### CrossRef Journals (if ISSN available)
```
WebFetch: https://api.crossref.org/journals/{issn}
→ Publication frequency, subject coverage
```

## STEP 4: Present Recommendations

```
## Recommended Journals

### Tier 1: Best Match (scope + impact)
1. **Journal of X** (H-index: 85, OA: Yes)
   - Scope match: 5/5 — publishes exactly this type of work
   - Similar papers found: 12 in last 3 years
   - Notable: published {related paper} closely related to yours

### Tier 2: Good Alternative
...

### Tier 3: Specialized/Niche
...

### Language-Specific Options (if non-English manuscript)
...
```

For each journal:
- Scope alignment explanation
- Recent similar papers found there
- Impact metrics (h-index, citation rate)
- Open access status
- Homepage URL

## STEP 5: Next Actions

- "Format manuscript for a specific journal's guidelines?"
- "Check if your references match what these journals typically cite?"
- "Draft a cover letter for one of these?"

## ERROR HANDLING
- Manuscript too short: ask for additional keywords/discipline
- Journal not in OpenAlex: fall back to CrossRef ISSN
- Non-English journals: less coverage, note limitation

## TOKEN BUDGET
- Main: ~5K (profile + presentation)
- Similar papers subagent: ~15-20K
- Journal enrichment: ~5-10K
- Total: ~25-35K

## REPORT DESIGN
When writing the HTML report, follow the design system in /report-template EXACTLY.
Do NOT use Tailwind CDN. Use the custom CSS variables, Crimson Pro font, and academic book aesthetic defined there.
