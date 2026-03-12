# Common Red Flags

Use this checklist as a prompting aid, not as an excuse to invent flaws.

## Contribution and positioning

- The claimed contribution is broad, but the concrete novelty is narrow or unclear.
- The paper compares against weak or outdated baselines only.
- The related-work positioning does not explain why existing methods are insufficient.

## Method and reasoning

- Key assumptions are unstated or unrealistic.
- Important implementation or algorithmic details are missing.
- The conclusion makes causal or general claims not supported by the method.

## Experiments and evidence

- Experiments do not test the main claimed advantage.
- The paper lacks ablations for components presented as essential.
- Results are close, but uncertainty or variance is not reported.
- Dataset coverage is too narrow for the generality of the claim.
- Efficiency, cost, or usability claims are asserted without direct measurement.

## Writing and presentation

- The problem setup is hard to reconstruct from the introduction.
- Tables and figures are discussed vaguely instead of analytically.
- Limitations are absent or obviously understated.

## Partial-input handling

If the user provides only an abstract or a few sections:

- convert red flags into conditional concerns
- say what evidence would resolve them
- avoid claiming the paper definitely fails on a missing section
