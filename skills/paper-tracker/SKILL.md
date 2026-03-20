---
name: paper-tracker
description: Track newly published papers from specified journals, venues, keywords, authors, or domains and produce a one-shot report. Use when the user asks for recent papers from the last day, week, or month, wants a reading shortlist, contribution one-liners, trend summaries, or a structured HTML report.
---

# Paper Tracker

One-shot academic paper tracking for recent literature scanning. This skill is for ad hoc reporting, not persistent monitoring.

It is designed to be portable across Claude Code, Codex, VS Code agents, and OpenClaw-style environments because it relies on plain instructions, optional web access, and optional MCP tools instead of a client-specific runtime.

This is a general-purpose skill. It must work for arbitrary domains, journals, venues, authors, labs, and keyword sets. Any journal bundle shipped in `references/` is only an example, not a built-in default scope.

## Use this skill when

- The user wants recent papers from journals, venues, conferences, authors, labs, or keywords.
- The user asks for a "last day / week / month" paper digest.
- The user wants a shortlist such as "10 papers worth reading".
- The user wants both narrative output and structured HTML.

## Do not use this skill for

- Full systematic reviews across many years.
- Citation graph analysis unless the user explicitly asks for it.
- Continuous alerts, scheduled jobs, or persistent tracking state.

## Required inputs

Extract or confirm these fields from the request:

- Time window: `1 day`, `1 week`, `1 month`, or explicit dates.
- Scope: one or more of `domain`, `keywords`, `journals`, `authors`, `institutions`, `venues`.
- Output count: default `10`.
- Output format: `markdown summary` by default, `html` if requested.
- Language: follow the user's language.

If the user does not specify enough scope, infer a reasonable search query from the domain and say what was inferred.

## Core workflow

1. Normalize the request into a search brief.
2. Choose the source strategy based on the brief's `filters`.
3. If the request names journals or venues, resolve them to stable identifiers before searching. Prefer ISSN, publisher code, or known journal homepage over free-text title search.
4. Collect candidate papers published within the requested window across journal, author, and topic retrieval routes as needed.
5. Dedupe by DOI/title and remove clearly irrelevant results.
6. Filter out nonresearch items unless the user explicitly asks for them.
7. Rank for "worth reading" using novelty, venue fit, topic relevance, and practical importance.
8. Produce a report with:
   - A short executive summary
   - `Top N` papers
   - One-sentence contribution for each paper
   - A trend summary for the window
   - A complete paper list if the user asked for it
9. If HTML is requested, render the same content into the template in `assets/report_template.html`.

## Brief-first execution

When local scripts are available, prefer this pipeline:

1. Build a JSON brief following `references/brief-schema.md`.
2. If journals are present, use `scripts/resolve_journals.py` or a known registry to resolve ISSNs.
3. Retrieve raw candidates with `scripts/retrieve_candidates.py`.
4. Dedupe and rank with `scripts/postprocess_papers.py`.
5. If you want one command, use `scripts/run_brief.py`.

This keeps `journals`, `authors`, and `topics/domain` on the same execution path instead of creating separate workflows per input type.

## Source strategy

Prefer primary or near-primary sources. Use the first available option that gives reliable date and venue metadata.

1. Official journal or publisher "latest articles", "early view", "online first", or issue pages.
2. Crossref `journals/{ISSN}/works` endpoints for journal-bounded retrieval.
3. Crossref author or bibliographic query endpoints for author/topic retrieval.
4. Crossref free-text search only as fallback, never as the main journal matcher.
5. Semantic Scholar or other academic search APIs for abstract enrichment.
6. arXiv/SSRN/RePEc only if the user's scope includes working papers or preprints.

Read `references/source-playbook.md` when you need query patterns, ranking heuristics, or date-handling rules.
Read `references/brief-schema.md` when you want a structured handoff into local scripts.
If the request matches the operations-management journal bundle in this repo, you may also read `examples/om-or-journal-registry.md`. Otherwise, build the journal mapping from the user's own journal list.

## Output contract

Default output sections:

1. Request normalization
2. Top papers
3. Trend summary
4. Full list
5. Notes on source coverage and limitations

For each shortlisted paper include:

- Title
- Authors
- Venue or journal
- Publication date if available
- Link
- Why it matters: one sentence
- Confidence note if metadata is incomplete or only weakly verified

If some papers are "online first" and not yet assigned to an issue, say so explicitly.

## Ranking heuristics

Favor papers that satisfy at least two of the following:

- Strong match to the requested topic or journal set
- Clear methodological or managerial contribution
- Likely broad interest within the field
- Novel data, model, or decision framework
- Strong practical relevance

Avoid ranking a paper highly only because the venue is prestigious.
Down-rank items with missing abstracts or unclear contribution unless the title alone is strongly informative.

## Research-item filter

Default behavior is to include research papers only.

Exclude these unless the user asks for them:

- `call for papers`
- editorials
- forewords
- corrigenda / errata
- table of contents pages
- book reviews
- announcements
- forum introductions without substantive research content

If a borderline item is included in the full list, label it as `nonresearch`.

## HTML mode

If the user asks for structured HTML:

- Keep the same content as the markdown report.
- Use semantic sections and tables.
- Keep the HTML self-contained.
- Start from `assets/report_template.html`.

## Example request shapes

- "追踪最近一周运筹与运营管理顶刊的新论文，给我 10 篇值得看的。"
- "Find papers from the past month on supply chain resilience, prioritize Management Science and POM, and output HTML."
- "Summarize the last 7 days of papers by keyword `inventory optimization` and author `X`."

For the journal-list example in this repo, read `references/example-journals.md`.

## Generalization rule

Do not assume:

- a fixed journal list
- a fixed field such as OM/OR
- a fixed ranking preference
- that a bundled journal registry exists for the user's request

When no registry exists, construct the source mapping from the user-provided scope and continue.

## Compatibility note

This skill is intentionally filesystem-first and prompt-first:

- No client-specific APIs are required.
- MCP tools can be used when available, but are optional.
- Web search or direct site access is enough for a manual one-shot run.
- Local scripts are optional accelerators, not mandatory runtime dependencies.

If tool coverage is weak, still produce the report and state the gaps in source coverage.

Do not say a journal has "no new papers" unless the evidence is strong. Distinguish:

- `no verified new papers found`
- `publisher page blocked or inaccessible`
- `metadata found but only nonresearch items`

## Before claiming completion

- Check that the search brief includes the requested time window, scope, output count, and language.
- Distinguish verified paper records from weak metadata matches, blocked sources, or unresolved venue mappings.
- Do not say "no new papers" unless the retrieval evidence supports that claim.
- If contribution summaries rely only on titles or abstracts, mark them as partial or low confidence.
- Use `paperskills:evidence-before-completion` before claiming the tracking report is complete or handoff-ready.

## Downstream handoff

- Recommended next skill: `literature-review`
- Pass forward a tracking brief plus the candidate list or shortlist
- Preserve `language`, `time_window`, `evidence_status`, `target_artifact`, search filters, and source coverage notes
- If the corpus is still weakly verified or heavily metadata-based, say downstream synthesis remains partial
