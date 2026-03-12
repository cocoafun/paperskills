# Example Journal Set

Use this example when the user asks for a recent report on operations management / operations research journals.

For stable journal identifiers in this example only, see `../examples/om-or-journal-registry.md`.

## Example user request

我想追溯最近一周下述期刊的论文，帮我输出近一周新发的论文的报告和清单。

## Journals

1. Management Science
2. Operations Research
3. Manufacturing & Service Operations Management
4. Production and Operations Management
5. Journal of Operations Management
6. Omega-International Journal of Management Science
7. INFORMS Journal on Computing
8. Annals of Operations Research
9. European Journal of Operational Research
10. International Journal of Production Economics
11. International Journal of Production Research

## Suggested execution

1. Treat the time window as the last 7 days relative to the current date.
2. Resolve the 11 journals to ISSNs first and use Crossref journal endpoints, not free-text container-title search.
3. Prefer official journal or publisher pages to identify newly published papers, but if they are blocked, fall back to Crossref plus Semantic Scholar.
4. Build a candidate pool across all 11 journals.
5. Remove nonresearch items such as `Call for Papers`, editorials, and forum introductions unless the user explicitly wants them.
6. Shortlist 10 papers worth reading across the set, not 10 per journal.
7. Output:
   - Executive summary
   - Top 10 with one-sentence contributions
   - Trend summary for the week
   - Full journal-by-journal list of newly found papers
   - Coverage note distinguishing `no verified item found`, `publisher blocked`, and `only nonresearch item found`

## Suggested ranking bias

Prefer papers that are likely to matter to operations management, OR, analytics, supply chain, production, and decision science readers.
