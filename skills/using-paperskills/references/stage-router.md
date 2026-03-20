# Stage Router

Use this reference to map a research request to the right PaperSkills stage or stage chain.

## Stage selection

### `research-scoping`

Use when:

- the topic is broad or fuzzy
- the user is unsure what exact question to ask
- the request mixes too many goals at once

Typical prompts:

- `我想研究 AI 在运营管理里的应用，帮我收敛选题。`
- `Help me refine this thesis topic before I search papers.`

### `paper-tracker`

Use when:

- the user wants papers from a recent time window
- the user wants a reading shortlist
- the user asks for a trend scan by journal, author, or keyword

### `literature-review`

Use when:

- the user wants a related-work draft
- the user wants thematic synthesis or research gaps
- the request is about multi-paper evidence integration

### `research-design`

Use when:

- the user already has a topic or gaps and wants a study plan
- the user asks for research questions, hypotheses, methods, or data logic

### `paper-drafting`

Use when:

- the user wants an outline, section plan, or manuscript draft
- the user already has enough evidence or a structured brief

Important:

- `paper-drafting` is not the starting point when the user asks for a full paper from only a topic and no evidence corpus.
- In that case, route to the earliest missing upstream stage and continue the workflow instead of stopping after diagnosis.

### `manuscript-finalization`

Use when:

- the user already has a working draft and wants a finished manuscript
- the target artifact is `undergraduate thesis`, `submission-ready manuscript`, or `完整终稿`
- the workflow must not stop at a draft package

### `peer-review`

Use when:

- the user provides one paper and wants critique
- the user asks for recommendation labels or reviewer comments

### `revision-planning`

Use when:

- the user has review feedback and needs an action plan
- the user asks how to revise for resubmission or rebuttal

## Ambiguous cases

- If the user asks for a paper draft but has no clear topic boundary, start with `research-scoping`.
- If the user asks for hypotheses without any evidence base, route to `research-design` and explicitly mark evidence risk.
- If the user asks for a literature review and also a proposal, start with `literature-review` unless the topic itself is still vague.
- If the user asks for recent papers and a gap analysis in one request, use `paper-tracker` first, then `literature-review`.
- If the user asks for a complete paper, thesis chapter, or proposal from only a title or topic, use a staged chain rather than a single stage.
- If the user asks for a complete paper from a topic in a fast-moving area and gives no source list, prefer `research-scoping -> paper-tracker -> literature-review -> research-design -> paper-drafting -> manuscript-finalization`.
- If the user asks for a complete paper from a topic in a slower-moving area and gives no source list, prefer `research-scoping -> literature-review -> research-design -> paper-drafting -> manuscript-finalization`.
- If the user asks for a non-empirical undergraduate thesis or conceptual full paper from a topic and no completed study exists, prefer `research-scoping -> literature-review -> paper-drafting -> manuscript-finalization`.
- If the user asks for a non-empirical undergraduate thesis or conceptual full paper from only a title, and the topic depends on current platform behavior, product pages, policy updates, or a weak starting corpus, prefer `research-scoping -> paper-tracker -> literature-review -> paper-drafting -> manuscript-finalization`.

## Multi-stage routing patterns

### Early idea to proposal

Use:

- `research-scoping -> literature-review -> research-design -> paper-drafting`

When:

- the user has a broad topic
- the target artifact is a proposal or structured draft
- no evidence ledger has been provided

### Topic to full paper draft

Use:

- `research-scoping -> paper-tracker -> literature-review -> research-design -> paper-drafting -> manuscript-finalization`

When:

- the user asks for "完整写一篇论文", "完整撰写", "full paper", or similar
- the input is only a topic, title, or short brief
- recency or candidate-paper discovery is still missing
- the final requested artifact is a completed manuscript rather than only a working draft

### Topic to full non-empirical thesis

Use:

- `research-scoping -> literature-review -> paper-drafting -> manuscript-finalization`

When:

- the user asks for an undergraduate thesis, thesis-style full paper, or complete conceptual manuscript
- no completed empirical study is available
- the defensible end state is a finished non-empirical manuscript rather than a draft outline

Additional routing discipline:

- Do not preset the run as evidence-backed before retrieval. If there is no verified corpus yet, set the handoff evidence state to `needs-retrieval` or equivalent.
- If the topic includes live products, policies, or platform features, preserve at least one retrieval step before synthesis so the later review is not forced to invent a corpus.
- If multiple stages are executed in one turn, finish and persist the current stage package before creating the next one. Do not precreate the full chain and backfill artifacts at the end.
- Use the actual stage position in the chosen chain for `--index`; example numbers in individual skills are not a universal numbering scheme.

Manuscript-type rule:

- If no data, experiment results, fieldwork findings, or finished empirical tables are provided, the downstream artifact should default to `conceptual-paper`, `literature-review-paper`, or `proposal-style-manuscript`, not `empirical-paper`.

## Manuscript-type routing

Before routing a full-paper request, classify the most defensible manuscript type:

- `literature-review-paper`
  Use when the contribution is mainly synthesis, related work, or gap identification.
- `conceptual-paper`
  Use when the contribution is a framework, mechanism explanation, proposition set, or governance model.
- `proposal-style-manuscript`
  Use when the user wants a paper-like full draft but no completed study results are available.
- `empirical-paper`
  Use only when completed data, methods, and results are already available.

If the request only provides a topic, never assume `empirical-paper` by default.

### Recent-papers-led review

Use:

- `paper-tracker -> literature-review`

When:

- the user explicitly wants a recent-paper sweep before synthesis
- the request mentions a recent time window, reading shortlist, or trend scan

## Output discipline

Before handing off, state:

- the immediate next stage
- the planned stage chain when applicable
- why that stage is appropriate
- what evidence or inputs are already available
- what still needs to be inferred
- whether retrieval is still required before a review can be considered complete
- whether the current stage artifact has already been committed locally before downstream work begins
