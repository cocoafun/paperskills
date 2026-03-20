---
name: literature-review
description: Generate literature reviews and related-work drafts from a user-provided research topic, thesis direction, paper idea, or problem statement. Use when the user asks for 文献综述, related work, state-of-the-art summary, research background, thematic synthesis, research gap analysis, or an evidence-backed review outline in Chinese or English.
---

# Literature Review

One-shot literature review generation from a topic brief.

This skill turns a short request such as a paper topic, research direction, thesis chapter idea, or problem statement into:

- a normalized review brief
- a search and screening plan
- a source shortlist
- a thematic synthesis
- a markdown draft with citations or explicit evidence gaps

This skill is designed to stay portable across Codex-style environments. It works with web search, academic APIs, and optional MCP tools. Local scripts only scaffold structure; they do not replace evidence collection.

## Use this skill when

- The user wants a literature review, related-work section, or state-of-the-art summary.
- The user provides a topic or research direction and wants a first draft of review content.
- The user wants research gaps, theme clustering, or a structured review outline.
- The user wants a review section in Chinese or English with explicit source coverage notes.

## Do not use this skill for

- Last-day or last-week paper tracking. Use `paper-tracker` for that pattern.
- Full quantitative meta-analysis unless the user explicitly asks for statistical pooling.
- Citation verification without review writing. That is a narrower bibliography task.

## Required inputs

Extract or infer these fields from the request:

- Topic or research problem
- Goal: `survey`, `related work`, `thesis chapter`, `research background`, or `gap analysis`
- Review type: default `narrative`
- Time window: default `last 5 years` plus older seminal papers when needed
- Output language: follow the user's language
- Depth: default `standard`
- Citation style: default `APA`

If the request is too broad, narrow it to 2-4 concrete questions and state what was inferred.

Read [references/brief-schema.md](references/brief-schema.md) when you want the normalized JSON shape.

## Core workflow

1. Normalize the request into a review brief.
2. Choose the source strategy by domain and review depth.
3. Run actual retrieval against primary or near-primary sources. Do not skip this step by writing from memory or from a pre-assumed corpus.
4. Record retrieval batches with query string, source, language, and search date.
5. Collect candidate papers from academic indexes first. If the topic also needs live product or policy evidence, keep those official pages in a separate documentation lane.
6. Build an evidence ledger with title, year, venue, link, relevance note, and confidence note.
7. Check the corpus size against the selected review mode.
8. Dedupe and screen the corpus. Label preprints clearly.
9. Cluster the remaining evidence into 3-5 themes or research questions.
10. Write a synthesis-first draft. Do not write an annotated bibliography.
11. Close with research gaps, limitations, and future directions.

Read [references/source-playbook.md](references/source-playbook.md) for retrieval and screening rules.
Read [references/writing-playbook.md](references/writing-playbook.md) for synthesis and drafting rules.

## Brief-first execution

When local files are useful, prefer this pipeline:

1. Build a JSON brief following [references/brief-schema.md](references/brief-schema.md).
2. Render a starter markdown file:

```bash
python3 skills/literature-review/scripts/render_review.py \
  --brief skills/literature-review/examples/topic-brief.json \
  --output draft_review.md
```

3. Fill the scaffold with evidence-backed content from actual sources.
4. Replace all placeholders before finalizing.

Use [assets/review_template.md](assets/review_template.md) when you want a manual template without the script.

## Source strategy

Prefer primary or near-primary sources with stable metadata. For academic retrieval, generic web search is not a primary evidence lane.

1. Domain databases or official academic indexes
2. Structured academic discovery sources such as OpenAlex, Crossref, and Semantic Scholar
3. Official venue, journal, or publisher pages
4. Google Scholar and Baidu Scholar as discovery or citation-chaining layers, then resolve kept items to stable metadata or publisher pages when possible
5. arXiv, bioRxiv, medRxiv when preprints are relevant
6. General web search only for official product, policy, or help-center pages, or for resolving links discovered elsewhere

Academic versus live-documentation lanes:

- When the topic mixes scholarly literature with live product behavior, maintain two explicit lanes: an academic literature lane and a live-documentation lane.
- Official platform pages can support current-state analysis, but they do not replace academic literature retrieval.
- For management, advertising, platform, search, and related social-science topics, start the academic lane with `Crossref`, `OpenAlex`, or `Semantic Scholar`, then use `Google Scholar` or `Baidu Scholar` for expansion and citation chasing when helpful.

Domain defaults:

- Biomedicine: PubMed, PubMed Central, Cochrane, bioRxiv, medRxiv
- Computer science and AI: arXiv, ACL Anthology, Semantic Scholar, OpenAlex
- Social science and management: Crossref, OpenAlex, Semantic Scholar, SSRN, publisher journal pages
- General science: Semantic Scholar, OpenAlex, Crossref, publisher pages

Language-specific defaults:

- If the user asks for Chinese output, Chinese papers, a Chinese thesis chapter, or the topic is clearly centered on Chinese scholarship, add Chinese academic indexes to the front of the search plan.
- If the target artifact is a `中文本科毕业论文`, use at least one Chinese academic lane and one international academic lane when feasible. If either lane is skipped, explain why.
- For Chinese-language literature retrieval, prefer CNKI, Wanfang Data, VIP/CQVIP, Baidu Scholar, Airiti Library when relevant, and institutional journal portals.
- Do bilingual retrieval when the topic spans both Chinese and international scholarship. Use paired Chinese and English query variants instead of searching only one language.
- If Chinese databases return only metadata or partial previews, say so explicitly and avoid overclaiming full-text coverage.
- Record which claims are mainly grounded in Chinese-language literature versus international literature when that distinction matters for the argument.

If Zotero or Semantic Scholar MCP tools are available, use them for seed-paper expansion, citation chaining, and note capture. Otherwise continue with web and public APIs.

For topics involving live products, platform behavior, policy pages, or recent product rollouts, verify at least one live source in the current turn. A cached memory of the product is not a sufficient retrieval record.

## Evidence rules

- Every nontrivial factual claim should be backed by at least one cited source.
- Never invent counts, DOIs, quotations, or comparative findings.
- Distinguish explicit source statements from your own synthesis or inference.
- If the draft is based only on abstracts or metadata, say so directly.
- Include the search cutoff date whenever currency matters.
- If no actual retrieval was performed in the current turn or run, do not mark the stage as `completed`.
- If the corpus does not meet the target mode's minimum evidence bar, state that the review is partial and why.
- If the topic required live platform documentation, do not count official product pages as a substitute for the academic evidence bar.

## Output contract

Default output sections:

1. Request normalization
2. Search strategy and source coverage
3. Retrieval log or search batches
4. Corpus snapshot
5. Thematic synthesis
6. Research gaps and future directions
7. Limitations
8. Working bibliography or references

Do not collapse the output to a synthesis-only essay. The review stage must leave behind enough retrieval and source-coverage structure for `paper-drafting` to reuse without re-deriving the corpus from scratch.

The retrieval log must be concrete enough that another agent can rerun or audit the search. At minimum include:

- source name
- source type such as `academic-index`, `publisher`, `official-platform`, or `industry`
- query string or query description
- search date or cutoff date
- language
- batch result count or a note that counts were not available
- whether high-value hits were resolved to stable metadata, a publisher page, or only a discovery page

When the target artifact is a Chinese undergraduate thesis, the source coverage section should normally state whether Chinese academic databases were searched and what they contributed. If they were not searched, explain the reason briefly instead of leaving the omission implicit.
When both academic literature and official platform documentation are used, report separate kept-source counts for each lane instead of blending them into one undifferentiated total.

For each theme include:

- What the theme is about
- Which papers support it
- Where the literature agrees or conflicts
- What remains unresolved

When the downstream target is an undergraduate thesis, also include:

- which later thesis chapter or section the theme is meant to support
- which sources are foundational theory versus platform documentation versus industry observation

## Review modes

Pick one mode based on the user's goal:

- `quick`: 6-10 core papers, concise synthesis, useful for proposal drafting
- `standard`: 12-20 papers, 3-5 themes, default mode
- `deep`: 20-40 papers, broader coverage, stronger gap analysis

If the user gives no mode, default to `standard`.

Mode minimums:

- `quick`: aim for at least 6 kept sources
- `standard`: aim for at least 12 kept sources
- `deep`: aim for at least 20 kept sources

If the kept corpus is smaller, say the mode target was not met and mark the review as partial or low confidence.
For mixed live-product topics, the academic corpus must still meet the evidence bar on its own; official product pages are auxiliary evidence, not a substitute for review-mode coverage.

## Common failure modes

Avoid these:

- Turning the draft into one-paper-at-a-time summaries
- Mixing retrieval notes with final prose
- Treating preprints and peer-reviewed papers as equivalent without labels
- Stating "the literature shows" when only 1-2 papers support the claim
- Writing a polished conclusion while the evidence base is still thin
- Using generic web search results or product blogs as the main academic literature corpus

## Before claiming completion

- Check that the normalized review brief is complete enough for the requested review mode.
- Check that actual retrieval happened and that the run contains a query log or equivalent retrieval batches.
- Check whether sources were reviewed in full text, abstract only, or metadata only.
- Distinguish source-grounded findings from synthesis and inference.
- If the corpus is thin or partial, mark the output as `partial`, `low confidence`, or equivalent.
- Check that `output.md` includes the search strategy, corpus snapshot, and working bibliography rather than only polished prose.
- Check that at least two scholarly retrieval lanes were actually used when the topic is not scoped to a single specialized index.
- Do not say the stage is handoff-ready if the only "sources" are uncited memory, vague mentions of Google Scholar or Baidu Scholar, a bibliography with no retrieval record, or official platform pages with no academic retrieval lane.
- Use `paperskills:evidence-before-completion` before saying the review is complete or strongly evidence-backed.

## Downstream handoff

- Recommended next skills: `research-design` or `paper-drafting`
- Pass forward a `review-brief` plus the evidence ledger or source shortlist
- Preserve `language`, `manuscript_type`, `evidence_status`, `time_window`, `target_artifact`, and major gaps
- Include a reusable evidence ledger with claim-ready source notes, not just a paragraph summary
- Do not say the workflow is ready for downstream drafting if the synthesis is abstract-based, key evidence is still missing, or the retrieval log is absent

## Example request shapes

- `帮我围绕“基于大语言模型的文献综述自动生成”写一个文献综述初稿。`
- `根据“供应链韧性中的数字孪生优化”生成 related work。`
- `Write a literature review on agentic scientific discovery systems and identify open gaps.`
- `Turn this thesis topic into a review brief, source list, and 3000-word review draft.`

## Local artifact persistence

When persisting local work, keep the evidence ledger and the narrative draft as separate artifacts.

Before writing stage content, ensure the stage package exists:

```bash
python3 skills/using-paperskills/scripts/paperskills_artifacts.py ensure-stage \
  --run-dir artifacts/paperskills/<run-id> \
  --stage literature-review \
  --index <stage-index> \
  --status in_progress
```

- Write `brief.json` for the normalized review brief as soon as the review scope and source plan are stable.
- Save screening notes, theme clustering, and evidence ledger details in `notes.md` or companion files.
- Save the synthesis draft in `output.md`.
- Write `handoff.json` only if the review is explicitly preparing `research-design` or `paper-drafting`.
- Before leaving the stage, call `update-stage` with the final `evidence_status` and handoff readiness. Do not defer all review-stage writes until manuscript drafting or finalization is already underway.
- If the user asked only for one review pass, store it as a standalone run with its own evidence boundary markers.
