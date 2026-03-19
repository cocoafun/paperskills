# Stage Router

Use this reference to map a research request to the right PaperSkills stage.

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

## Output discipline

Before handing off, state:

- the chosen stage
- why that stage is appropriate
- what evidence or inputs are already available
- what still needs to be inferred
