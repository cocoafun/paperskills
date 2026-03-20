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
3. Collect candidate papers from primary or near-primary academic sources.
4. Build an evidence ledger with title, year, venue, link, relevance note, and confidence note.
5. Dedupe and screen the corpus. Label preprints clearly.
6. Cluster the remaining evidence into 3-5 themes or research questions.
7. Write a synthesis-first draft. Do not write an annotated bibliography.
8. Close with research gaps, limitations, and future directions.

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

Prefer primary or near-primary sources with stable metadata:

1. Domain databases or official indexes
2. OpenAlex, Crossref, Semantic Scholar
3. Official venue or journal pages
4. arXiv, bioRxiv, medRxiv when preprints are relevant
5. Google Scholar only as a fallback discovery layer

Domain defaults:

- Biomedicine: PubMed, PubMed Central, Cochrane, bioRxiv, medRxiv
- Computer science and AI: arXiv, ACL Anthology, Semantic Scholar, OpenAlex
- Social science and management: Crossref, OpenAlex, SSRN, publisher journal pages
- General science: Semantic Scholar, OpenAlex, Crossref, publisher pages

If Zotero or Semantic Scholar MCP tools are available, use them for seed-paper expansion, citation chaining, and note capture. Otherwise continue with web and public APIs.

## Evidence rules

- Every nontrivial factual claim should be backed by at least one cited source.
- Never invent counts, DOIs, quotations, or comparative findings.
- Distinguish explicit source statements from your own synthesis or inference.
- If the draft is based only on abstracts or metadata, say so directly.
- Include the search cutoff date whenever currency matters.

## Output contract

Default output sections:

1. Request normalization
2. Search strategy and source coverage
3. Corpus snapshot
4. Thematic synthesis
5. Research gaps and future directions
6. Limitations
7. Working bibliography or references

For each theme include:

- What the theme is about
- Which papers support it
- Where the literature agrees or conflicts
- What remains unresolved

## Review modes

Pick one mode based on the user's goal:

- `quick`: 6-10 core papers, concise synthesis, useful for proposal drafting
- `standard`: 12-20 papers, 3-5 themes, default mode
- `deep`: 20-40 papers, broader coverage, stronger gap analysis

If the user gives no mode, default to `standard`.

## Common failure modes

Avoid these:

- Turning the draft into one-paper-at-a-time summaries
- Mixing retrieval notes with final prose
- Treating preprints and peer-reviewed papers as equivalent without labels
- Stating "the literature shows" when only 1-2 papers support the claim
- Writing a polished conclusion while the evidence base is still thin

## Before claiming completion

- Check that the normalized review brief is complete enough for the requested review mode.
- Check whether sources were reviewed in full text, abstract only, or metadata only.
- Distinguish source-grounded findings from synthesis and inference.
- If the corpus is thin or partial, mark the output as `partial`, `low confidence`, or equivalent.
- Use `paperskills:evidence-before-completion` before saying the review is complete or strongly evidence-backed.

## Downstream handoff

- Recommended next skills: `research-design` or `paper-drafting`
- Pass forward a `review-brief` plus the evidence ledger or source shortlist
- Preserve `language`, `manuscript_type`, `evidence_status`, `time_window`, `target_artifact`, and major gaps
- Do not say the workflow is ready for downstream drafting if the synthesis is abstract-based or key evidence is still missing

## Example request shapes

- `帮我围绕“基于大语言模型的文献综述自动生成”写一个文献综述初稿。`
- `根据“供应链韧性中的数字孪生优化”生成 related work。`
- `Write a literature review on agentic scientific discovery systems and identify open gaps.`
- `Turn this thesis topic into a review brief, source list, and 3000-word review draft.`
