# Source Playbook

Use this file only when you need concrete retrieval strategy for recent-paper tracking.

## 1. Search brief

Normalize the request into:

- `window`: explicit dates or relative period
- `topic`: field or keyword cluster
- `source filters`: journals, venues, authors, institutions
- `output size`: usually 10
- `output mode`: markdown or html

## 2. Source priority

For journal tracking, prefer:

1. Journal homepage pages such as `latest articles`, `current issue`, `online first`, `articles in advance`.
2. Publisher pages for the journal.
3. Crossref `journals/{ISSN}/works` queries constrained by date window.
4. Semantic Scholar or similar APIs for abstract/TL;DR enrichment.
5. Crossref free-text queries only as fallback for discovery or ISSN recovery.

For keyword tracking without fixed journals, prefer:

1. Semantic Scholar or Crossref query by keyword + date window
2. Venue filtering after retrieval
3. Official pages to verify borderline items

## 3. Date rules

Use the most specific public date available and name it clearly:

- `published online`
- `accepted article`
- `issue date`
- `created in Crossref`

Do not treat `indexed date` as publication date unless nothing else is available. If you must use it, label it as inferred.

If the source returns only `created` in Crossref, treat it as weak evidence and note that it may reflect metadata registration rather than public publication.

## 4. Dedupe rules

Consider records duplicates if any of the following match:

- DOI
- Same title after lowercasing and punctuation normalization
- Same title plus same first author

Keep the record with the better link and richer metadata.

When the same article appears under print and electronic ISSNs, keep one record and preserve both identifiers only in notes if needed.

## 5. Journal resolution

For journal-bounded requests, resolve each journal to a stable identifier before collecting records:

- ISSN / eISSN
- publisher code or slug
- canonical homepage

Do not rely on `query.container-title` alone. It produces false positives for titles with partial word overlap and can miss journals with punctuation variants.

If a known journal set recurs, maintain a registry file with ISSNs and homepage hints.
If no registry exists, create the mapping on the fly from publisher pages, Crossref journal lookup, or other reliable metadata sources.

## 6. Nonresearch-item filter

Exclude these by default:

- call for papers
- editorials
- forewords
- comments and replies without new empirical or methodological contribution
- corrigenda / errata
- issue introductions

Heuristics:

- If title contains `Call for Papers`, exclude from shortlist and mark `nonresearch`.
- If Crossref `type` is not `journal-article`, exclude unless the user explicitly wants all content.
- If title contains `Forum`, `Editorial`, or `Introduction`, inspect before inclusion.

## 7. Ranking rules

Score each candidate on:

- Relevance to request
- Recency within the requested window
- Contribution clarity from title/abstract
- Audience breadth in the target field
- Practical or methodological distinctiveness

Use venue prestige as a weak tie-breaker, not the main criterion.
Penalize candidates with no abstract, no TL;DR, and an ambiguous title.

## 8. Contribution one-liner

Each shortlisted paper gets one sentence in this shape:

`This paper [proposes/tests/shows/quantifies] ... , which matters because ...`

The sentence should describe contribution, not restate the title.

If metadata is weak, say so rather than inventing a contribution.

## 9. Trend summary

Write 3 to 5 sentences covering:

- Dominant themes in the window
- Methods becoming common
- Managerial or policy angles that appear repeatedly
- Gaps or emerging directions

Only claim a trend if at least two papers support it.

## 10. Coverage statement

End with a short note describing:

- Which sources were checked
- Whether some journals had sparse metadata
- Whether some journal pages were inaccessible or blocked
- Whether preprints were excluded

Use one of these labels for each difficult journal:

- `verified update found`
- `only nonresearch item found`
- `publisher blocked`
- `no verified item found in queried sources`

## 11. Query patterns

Examples for web or API search construction:

- `"Management Science" site:pubsonline.informs.org recent articles`
- `"Operations Research" online first OR latest articles`
- `"inventory optimization" AND "2026" AND journal`
- `container-title:"Management Science" from-pub-date:2026-03-05 until-pub-date:2026-03-12`

When a journal has unstable site structure, query the publisher domain instead of guessing article URLs.

## 12. Failure modes seen in practice

- Publisher anti-bot pages can make official sites unusable from terminal clients.
- Crossref free-text search can confuse unrelated journals with overlapping tokens.
- Some publishers register DOI metadata later than the visible online-first date.
- Some recent records have title-level metadata only, so contribution summaries should be lower confidence.
