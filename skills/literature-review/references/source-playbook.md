# Source Playbook

Use this reference when turning a review brief into an evidence set.

## Source selection by domain

- Biomedicine: PubMed, PubMed Central, Cochrane, bioRxiv, medRxiv
- Computer science and AI: arXiv, ACL Anthology, Semantic Scholar, OpenAlex
- Economics, management, and social science: Crossref, OpenAlex, SSRN, journal pages
- General science: Semantic Scholar, OpenAlex, Crossref, publisher pages

## Source selection by language

- Chinese-language literature: CNKI first, then Wanfang Data, VIP/CQVIP, Airiti Library when regionally relevant, plus journal or university repository pages.
- Mixed Chinese and English topics: search both Chinese and English databases. Do not assume English-only coverage is sufficient.
- If the user explicitly wants Chinese theses or dissertations, include CNKI dissertation search and relevant university repositories when accessible.

Prefer sources with stable metadata, abstracts, and durable links.

## Minimum evidence bar

- `quick`: 6-10 core papers
- `standard`: 12-20 papers
- `deep`: 20-40 papers

If coverage is weaker than the target mode, say so explicitly.

## Retrieval workflow

1. Start with the normalized topic and review questions.
2. Build 2-4 query variants from `concept_groups` or `keywords`.
3. If the target corpus may include Chinese papers, create parallel Chinese query variants, including key discipline terms, common translated titles, and known local terminology.
4. Search at least 2 complementary sources. For Chinese topics, at least 1 Chinese academic database should be included unless the user explicitly excludes it.
5. Use citation chaining from 2-3 anchor papers if the topic is mature.
6. Record search date, query string, language, and source for each batch.

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
- For Chinese retrieval, test both exact Chinese terms and shorter discipline-native expressions instead of translating English phrases literally.

Example:

```text
("large language model" OR LLM OR "foundation model")
AND ("literature review" OR "related work generation" OR "evidence synthesis")
AND (evaluation OR factuality OR grounding)
```

Chinese example:

```text
("大语言模型" OR LLM OR "生成式人工智能")
AND ("文献综述" OR "相关工作生成" OR "证据综合")
AND ("评价" OR "事实性" OR "可追溯性" OR "检索增强")
```

## Coverage notes

In the final review, state at least:

- what sources were searched
- the search cutoff date
- which languages were searched
- whether preprints were included
- whether the draft is based on abstracts only, full texts, or mixed evidence
