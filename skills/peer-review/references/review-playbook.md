# Review Playbook

Use this reference when converting a paper draft into reviewer-style feedback.

## Review stance

- Evaluate the paper that is actually shown, not the paper you wish existed.
- Prefer concrete, testable criticism over vague severity language.
- Keep the review useful to the author even when the recommendation is negative.
- Separate fatal issues from fixable weaknesses.

## Order of evaluation

1. What problem is the paper solving?
2. What exactly is claimed as the contribution?
3. Does the method match the claim?
4. Does the evidence match the method and contribution?
5. Does the writing make the work reviewable?

If one step is unclear, flag that uncertainty before moving to stronger judgments.

## Dimension guidance

### Novelty

Ask:

- Is the contribution differentiated from standard baselines or known patterns?
- Does the paper explain what is new: method, data, theory, system integration, or evaluation?
- If novelty seems weak, is that because the idea is incremental or because the related-work positioning is incomplete?

Good criticism:

- `The contribution appears incremental because the method combines known components, and the current text does not explain what new capability emerges from that combination.`

Weak criticism:

- `This is not novel.`

### Technical soundness

Ask:

- Are the assumptions reasonable and stated clearly?
- Are the method details sufficient to believe the approach is correct?
- Are causal or theoretical claims stronger than the method can support?

Common signals:

- missing algorithm details
- unclear notation
- unsupported theorem assumptions
- mismatch between optimization objective and claimed outcome

### Empirical quality

Ask:

- Do experiments test the paper's main claims?
- Are baselines appropriate and competitive?
- Are ablations, robustness checks, or sensitivity analyses needed?
- Are metrics aligned with the claimed contribution?

Common signals:

- no strong baseline
- no error analysis
- no statistical uncertainty when results are close
- narrow dataset coverage
- no real comparison for claimed efficiency or practicality

### Clarity

Ask:

- Can a reviewer restate the contribution after one pass?
- Are the paper structure, notation, and tables easy to follow?
- Are claims and limitations stated at the right level of confidence?

### Significance

Ask:

- If the results hold, do they matter?
- Is the practical or scientific impact clear?
- Is the contribution narrow but still valuable?

## Recommendation discipline

Use recommendation labels based on the review you can justify:

- `accept`: strong contribution with no major unresolved weakness in the visible material
- `weak accept`: worthwhile paper with some limitations that do not overturn the core contribution
- `borderline`: mixed case where strengths and weaknesses are tightly balanced
- `weak reject`: promising direction but important evidence or positioning is currently insufficient
- `reject`: core issues in novelty, soundness, or evidence undermine acceptance

Do not force a venue-style scorecard. The label is a simulation, not an official decision.

## Major vs minor issues

Classify as major when the issue could change the recommendation:

- contribution not clearly differentiated
- core method not understandable or not credible
- experiments do not support the central claim
- evaluation omits necessary baseline or robustness evidence

Classify as minor when the issue mainly affects readability or polish:

- wording and notation cleanup
- missing examples
- figure clarity
- organization improvements

## Output discipline

The final review should make these distinctions explicit:

- `The paper states`
- `The provided text does not show`
- `This creates a risk that`
- `I therefore lean toward`

That pattern keeps the review grounded and prevents invented criticism.
