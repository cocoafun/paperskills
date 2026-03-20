---
name: peer-review
description: Review a single academic paper and produce reviewer-style feedback from the paper text, abstract, or a structured brief. Use when the user asks for 审稿, reviewer comments, 审稿意见, mock peer review, rebuttal-oriented critique, accept/reject recommendation, weak accept, weak reject, or a structured review report in Chinese or English.
---

# Peer Review

One-shot peer review generation for a single paper.

This skill turns a paper draft, abstract, or structured paper brief into:

- a normalized review brief
- a paper-claim summary
- reviewer-style strengths and weaknesses
- major and minor revision suggestions
- a simulated recommendation with confidence notes

This skill is designed for critique and revision planning. It does not replace expert domain review or venue-specific policy checks.

## Use this skill when

- The user wants reviewer-style comments for one paper.
- The user pastes a paper, abstract, or sections and asks for 审稿意见.
- The user wants a mock decision such as `weak accept` or `weak reject`.
- The user wants actionable revision advice before submission or rebuttal.

## Do not use this skill for

- Multi-paper thematic synthesis. Use `literature-review` for that pattern.
- Recent-paper discovery. Use `paper-tracker` for that pattern.
- Pure proofreading or translation without scientific critique.

## Required inputs

Extract or infer these fields from the request:

- Paper title
- Paper content: full text, abstract, or the sections the user provides
- Output language: follow the user's language
- Review style: default `balanced`
- Venue target if the user gives one
- Paper type if visible: `empirical`, `theoretical`, `systems`, `benchmark`, `survey`, `position`, or `method`

If the user provides only an abstract or partial sections, continue, but label the review as partial and reduce confidence.

Read [references/brief-schema.md](references/brief-schema.md) when you want the normalized JSON shape.

## Core workflow

1. Normalize the request into a paper-review brief.
2. Determine evidence completeness: `full-paper`, `partial-paper`, or `abstract-only`.
3. Extract the paper's claimed problem, method, contributions, evidence, and conclusions.
4. Evaluate the paper on:
   - novelty
   - technical soundness
   - empirical quality
   - clarity
   - significance
   - overall risk
5. Identify major issues before minor issues.
6. Produce a reviewer-style report with evidence-linked reasoning.
7. End with a simulated recommendation and a confidence note.

Read [references/review-playbook.md](references/review-playbook.md) for review logic and output discipline.
Read [references/common-red-flags.md](references/common-red-flags.md) when you want a compact checklist of typical weaknesses.

## Brief-first execution

When local files are useful, prefer this flow:

1. Build a JSON brief following [references/brief-schema.md](references/brief-schema.md).
2. Start from [assets/review_template.md](assets/review_template.md).
3. Fill the template with paper-specific judgments and concrete revision advice.
4. Replace all placeholders before finalizing.

Use [examples/short-paper-brief.json](examples/short-paper-brief.json) when only abstract-level information is available.
Use [examples/full-paper-brief.json](examples/full-paper-brief.json) when the paper structure is mostly available.

## Simulated recommendation

Supported recommendation labels:

- `accept`
- `weak accept`
- `borderline`
- `weak reject`
- `reject`

Recommendation rules:

- Use a stronger label only when the evidence in the provided paper text supports it.
- If the paper materials are incomplete, still provide a label if the user asks for it, but mark it as low confidence.
- Do not hide major technical or empirical issues behind a polite tone.
- Do not issue a confident `accept` from abstract-only evidence.

## Evidence rules

- Distinguish explicit paper content from your own inference.
- Do not invent missing baselines, datasets, theorem gaps, or related-work omissions.
- If a criticism depends on a section the user did not provide, phrase it as a risk or a missing verification point.
- Quote or paraphrase the paper only as needed to ground the review.
- When the venue target is unknown, use general peer-review standards rather than venue-specific norms.

## Output contract

Default output sections:

1. Request normalization
2. Paper summary
3. Main strengths
4. Main weaknesses
5. Dimension-by-dimension assessment
6. Major revision requests
7. Minor revision requests
8. Simulated recommendation
9. Confidence and evidence boundary

For each dimension include:

- a short rating such as `strong`, `adequate`, `weak`, or `unclear`
- the reason tied to the paper text
- the main downstream risk for acceptance or revision

## Review modes

Pick one mode based on the user's request or material quality:

- `quick`: short reviewer memo from abstract or selected sections
- `standard`: default full review with strengths, weaknesses, and recommendation
- `deep`: more detailed review with rebuttal-oriented questions and revision priorities

If the user gives no mode, default to `standard`.

## Common failure modes

Avoid these:

- Rewriting the abstract instead of critiquing the paper
- Giving generic praise that is not tied to evidence in the paper
- Claiming novelty is weak without identifying the overlap or missing differentiation
- Calling experiments insufficient without saying what evidence is missing
- Simulating a confident decision when the paper text is incomplete

## Before claiming completion

- Check that the review brief reflects whether the material is `full-paper`, `partial-paper`, or `abstract-only`.
- Tie each major judgment to provided paper evidence, not to invented missing sections.
- If the paper materials are incomplete, lower confidence and mark the review as partial.
- Do not present recommendation language as high confidence when the evidence base is incomplete.
- Use `paperskills:evidence-before-completion` before saying the review is complete or decision-ready.

## Downstream handoff

- Recommended next skill: `revision-planning`
- Pass forward a `reviewer-brief` or structured review output with issue units
- Preserve `language`, `manuscript_type`, `evidence_status`, recommendation confidence, and section-specific concerns
- If the review is based on partial materials, say downstream revision planning is also constrained by that evidence boundary

## Example request shapes

- `帮我审稿这篇论文，给出 major concerns 和 weak reject / weak accept 建议。`
- `Review this paper like a conference reviewer and tell me whether it is borderline or weak accept.`
- `根据这篇论文的摘要和方法部分，生成一份中文审稿意见。`
- `Act as a reviewer for this draft and give actionable revision requests before submission.`
