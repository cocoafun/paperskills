# Source Playbook

Use this reference when turning a review brief into an evidence set.

## Source selection by domain

- Biomedicine: PubMed, PubMed Central, Cochrane, bioRxiv, medRxiv
- Computer science and AI: arXiv, ACL Anthology, Semantic Scholar, OpenAlex
- Economics, management, and social science: Crossref, OpenAlex, SSRN, journal pages
- General science: Semantic Scholar, OpenAlex, Crossref, publisher pages

Prefer sources with stable metadata, abstracts, and durable links.

## Minimum evidence bar

- `quick`: 6-10 core papers
- `standard`: 12-20 papers
- `deep`: 20-40 papers

If coverage is weaker than the target mode, say so explicitly.

## Retrieval workflow

1. Start with the normalized topic and review questions.
2. Build 2-4 query variants from `concept_groups` or `keywords`.
3. Search at least 2 complementary sources.
4. Use citation chaining from 2-3 anchor papers if the topic is mature.
5. Record search date, query string, and source for each batch.

## Screening rules

- Remove duplicates by DOI first, then title.
- Keep one canonical record with the best metadata.
- Label preprints as `preprint`.
- Down-rank papers with no abstract, unclear venue, or thin topical fit.
- Prefer original research for claims and reviews for orientation.

## Evidence ledger

Track each kept paper with:

- title
- authors
- year
- venue
- DOI or stable URL
- paper type: `review`, `empirical`, `benchmark`, `position`, `preprint`
- relevance note
- confidence note

This can live in markdown bullets or a lightweight table.

## Query design

Use these patterns:

- Synonym expansion with `OR`
- Concept intersection with `AND`
- Restrict by venue or year only after the broad query works

Example:

```text
("large language model" OR LLM OR "foundation model")
AND ("literature review" OR "related work generation" OR "evidence synthesis")
AND (evaluation OR factuality OR grounding)
```

## Coverage notes

In the final review, state at least:

- what sources were searched
- the search cutoff date
- whether preprints were included
- whether the draft is based on abstracts only, full texts, or mixed evidence
