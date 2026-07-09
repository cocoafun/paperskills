---
name: cite-verify
description: Verify all citations in an academic manuscript against CrossRef, Semantic Scholar, and OpenAlex. Checks existence, metadata accuracy, open access status, and optionally verifies claims against source texts. Generates HTML report.
---

Verify all citations in "$ARGUMENTS".

Resolve file path:
- Filename only: look in current working directory
- Full path: use as-is

## CRITICAL RULE

Every citation must be checked. No "not searched" category.
Result is either "found", "partial match", or "not found".

## MAIN FLOW

```
Main Session — coordination only
  │
  ├── STEP 1: Parse citations from manuscript (self)
  ├── STEP 2: Resolve citations via APIs (subagent, batched)
  ├── STEP 3: Open access check (subagent)
  ├── STEP 4: (optional) Verify claims against full text (subagent)
  └── STEP 5: HTML report
```

## STEP 1: Parse Citations (self)

Read manuscript with Read tool. Extract all references:

### For footnote-style (`[^N]: Author, Title, Year, p.X`)
- Parse each `[^N]:` definition
- Extract: author, title/work, year, page, DOI if present
- Resolve op. cit. / ibid. chains

### For author-year style (`(Smith, 2020, p. 45)` or `Smith (2020)`)
Full text scan required. Regex patterns:
- `(Author, Year)` → `\(([A-Z][a-z]+(?:\s(?:&|and)\s[A-Z][a-z]+)*(?:\set\sal\.)?),?\s*(\d{4})[^)]*\)`
- `Author (Year)` → `([A-Z][a-z]+(?:\s(?:&|and)\s[A-Z][a-z]+)?)\s*\((\d{4})[^)]*\)`
- Extract: author(s), year, page if present
- Then match each to the BIBLIOGRAPHY/REFERENCES section at end of document
- Bibliography entry has full title, journal, DOI → use those for API lookup

### For numbered style (`[1] Author...` or superscript)
- Parse reference list at end
- Match `[N]` or `^N` in text to bibliography entry N

### Auto-detect citation style
Read first 50 lines + last 50 lines of the manuscript to detect:
- `[^N]:` definitions → footnote style
- `References` or `Bibliography` section + `(Author, Year)` in text → author-year
- `[1]`...`[N]` in text + numbered reference list → numbered
- Mixed → handle both

Group by unique work:
```
Smith 2020 → [^3] p.45, [^7] p.89, [^12] p.102
Jones 2019 → [^5] p.234
```

Categorize:
- **Journal article**: has journal name, volume, pages
- **Book**: has publisher, edition
- **Chapter**: has editor, book title
- **Conference**: has proceedings
- **Web/other**: URL, report, thesis

## STEP 2: Resolve via APIs (subagent)

Launch subagent. For each citation, try in order:

```
1. IF DOI present:
   WebFetch: https://api.crossref.org/works/{doi}
   → Confirms existence, gets metadata

2. IF no DOI — search by title:
   WebFetch: https://api.crossref.org/works?query.bibliographic={encoded_title}&query.author={author}&rows=3
   → Match by title similarity + author + year

3. IF CrossRef fails — try Semantic Scholar:
   WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={title} {author}&limit=3&fields=title,authors,year,externalIds,venue

4. Record result:
   - FOUND: metadata matches (title + author + year)
   - PARTIAL: title matches but year/author differs
   - NOT_FOUND: no match in any database
   - FABRICATED: author exists but no such work found — possible hallucinated reference

5. IF FOUND — validate metadata details:
   a. AUTHOR CHECK: Do the authors in manuscript match the API result?
      Watch for: misspelled names, wrong initials, swapped first/last author
   b. YEAR CHECK: Does publication year match?
   c. VENUE CHECK: Does the journal/publisher name match?
   d. PAGE RANGE CHECK: CrossRef returns page info (field: "page").
      Compare manuscript's cited pages against the work's actual page range.
      - If cited "p. 847" but work is pages "1-23" → PAGE OUT OF RANGE
      - If cited "pp. 100-105" but work is pages "95-120" → OK (within range)
      - If CrossRef has no page data: mark as UNCHECKED, not as error
   e. TITLE CHECK: Exact or near-exact title match? Minor differences
      (capitalization, subtitle) are OK. Major mismatch → wrong work.

6. For books (no DOI usually): search OpenAlex by title + author
   WebFetch: https://api.openalex.org/works?search={title}&filter=author.search:{author}&mailto=paperskills@example.com
   Books often lack DOI but OpenAlex has good book coverage.
```

**Batch strategy**: Process in groups of 10. 1-second delay between API calls.

## STEP 3: Open Access Check (subagent)

For each FOUND citation with a DOI:

```
WebFetch: https://api.unpaywall.org/v2/{doi}?email=paperskills@example.com

Extract:
- is_oa: true/false
- best_oa_location.url: PDF link
- oa_status: gold/green/hybrid/bronze/closed
```

## STEP 4: Claim Verification (optional — ask user first)

Only if user agrees (high token cost). For citations with OA PDF:

```
1. WebFetch the PDF URL from Unpaywall
2. Find the cited page/section
3. Read surrounding context (not just the sentence — the full paragraph + neighbors)
4. Analyze with these 5 CRITICAL CHECKS:

CHECK 1 — AUTHOR'S OWN VIEW?
Is the cited passage the author's own thesis, or are they reporting/quoting someone else?
A paper that says "According to Smith, X is true" does NOT mean the paper's author endorses X.

CHECK 2 — CONTEXT: SUPPORT OR CRITIQUE?
Does the source present the idea approvingly, critically, or neutrally?
If the source is criticizing a claim but the manuscript cites it as support → MISMATCH.

CHECK 3 — FAITHFUL PARAPHRASE?
Does the manuscript's summary accurately reflect the source?
Watch for: exaggeration, narrowing, subtle meaning shifts, omitted qualifications.

CHECK 4 — SCOPE MATCH?
Does the source's claim have the same scope as the manuscript suggests?
E.g., source says "in some cases X" but manuscript cites as "X is always true" → PARTIAL.

CHECK 5 — SELF-CITATION CHAINS?
Does the source itself cite another work for this claim?
If so, the original source may be more appropriate to cite.

Per citation result:
- VERIFIED: source supports the claim, author's own view, faithful paraphrase
- PARTIAL: source discusses topic but claim overstated/nuanced/scope differs
- MISMATCH: source says something different, or cited approvingly but source is critical
- ATTRIBUTION: source attributes the idea to someone else — consider citing the original
- UNVERIFIABLE: relevant section not found in accessible text
```

## STEP 5: HTML Report

Write to: reports/{date}-cite-verify-{manuscript}.html

Content:
- Existence verification table (ALWAYS — even without full-text access):
  | # | Ref | Authors | Title | Year | Exists? | Author OK? | Year OK? | Pages OK? | DOI | OA | Notes |
- If claim verification done (STEP 4), add deep analysis table:
  | # | Ref | Author's View? | Faithful? | Scope OK? | Issue | Detail |
- Summary stats:
  - Total references: X
  - Existence confirmed: Y (Z%)
  - Not found / possibly fabricated: N
  - Metadata issues (wrong author/year/pages): M
  - Open access available: P
  - Claims verified (if STEP 4): Q
- Color-coded rows:
  - green = found, all metadata matches
  - yellow = found but metadata issue (wrong year, pages out of range, author mismatch)
  - red = not found in any database (possibly fabricated)
  - orange = FABRICATED flag (author exists, but this specific work does not)
  - blue = attribution issue (STEP 4 only)

After writing the file:
- Return the exact absolute file path to the user
- Ask whether they want it opened
- Only run `open {file_path}` after the user explicitly confirms

## API REFERENCE

### CrossRef — Primary Resolution
```
By DOI: https://api.crossref.org/works/{doi}
By query: https://api.crossref.org/works?query.bibliographic={title}&query.author={author}&rows=3
```

### Semantic Scholar — Fallback
```
https://api.semanticscholar.org/graph/v1/paper/search?query={title+author}&limit=3&fields=title,authors,year,externalIds
```

### DOI Validation
```
https://doi.org/api/handles/{doi}
```

### Unpaywall — OA Check
```
https://api.unpaywall.org/v2/{doi}?email=paperskills@example.com
```

## ERROR HANDLING
- DOI malformed: clean (strip trailing punctuation, spaces), retry
- CrossRef 0 results: try Semantic Scholar
- Both fail: mark NOT_FOUND, flag "may exist outside indexed databases"
- Non-English titles: try both original language AND English translation
- Rate limited: batch with delays, report partial results

## TOKEN BUDGET
- Main: ~3K (parsing + coordination)
- Resolution subagent: ~10-15K per batch of 10
- OA check subagent: ~5K
- Claim verification subagent: ~20-40K (reads PDFs)
- Report: ~5K
- Total: ~25-65K (depends on citation count + claim verification)

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
- stat-label text in the stats bar should be Chinese (e.g., "引用数量" not "References")
- Badge text should be Chinese (e.g., "已验证" not "VERIFIED", "未找到" not "NOT FOUND")

## REPORT DESIGN
When writing the HTML report, read and follow the design system in `assets/report-template.md` (in the paperskills root directory) EXACTLY.
Do NOT use Tailwind CDN. Use the custom CSS variables, Crimson Pro font, and academic book aesthetic defined there.
