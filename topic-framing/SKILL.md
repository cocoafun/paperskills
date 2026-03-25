---
name: topic-framing
description: Help converge from a fuzzy research idea to a concrete, researchable paper title through structured dialogue. Covers problem sharpening, landscape check, and title workshop.
---

Help the user converge from a fuzzy research idea to a concrete, researchable paper title. Input: "$ARGUMENTS".

Do NOT use subagents — do this yourself directly.
Do NOT enter literature review, method design, or manuscript writing. This skill ends at a confirmed title.

## MAIN FLOW

```
Main Session — conversational convergence
  │
  ├── PHASE 1: Seed Capture — understand the raw idea
  ├── PHASE 2: Problem Sharpening — six forcing questions (one at a time)
  ├── PHASE 3: Landscape Check — quick literature scan for positioning
  ├── PHASE 4: Boundary Setting — scope, non-scope, contribution type
  ├── PHASE 5: Title Workshop — generate & refine candidate titles
  └── OUTPUT: Framing Card (markdown) + next-step suggestions
```

---

## PHASE 1: Seed Capture

Parse "$ARGUMENTS" as the user's initial idea. It may be anything from a single keyword to a paragraph.

Restate the idea in your own words (2-3 sentences), then immediately ask:

> I understand your interest is roughly: "{restatement}".
> Before we sharpen this, tell me more:
> A) I have a vague direction but no specific question yet
> B) I have a question in mind but I'm not sure it's the right one
> C) I have a question and want help refining the title
> D) I'm choosing between several possible angles

Use AskUserQuestion. The answer determines which Phase 2 questions to prioritize:
- A → ask all six questions
- B → skip Q1, focus Q2-Q6
- C → skip Q1-Q3, focus Q4-Q6
- D → collect all angles first, then run Q2-Q6 on the strongest

---

## PHASE 2: Problem Sharpening — Six Forcing Questions

Ask these **ONE AT A TIME** via AskUserQuestion. Wait for each answer before proceeding.
Push for specificity — vague answers get follow-up pushes.

### Q1: Core Curiosity

**Ask:** "What specific phenomenon, contradiction, or observation made you interested in this? Not the field — the thing that made you think 'someone should study this.'"

**Push until you hear:** A concrete trigger — something they read, experienced, noticed, or found surprising. Not "I'm interested in X" but "I noticed that X does Y, which seems wrong/unexplained/underexplored."

### Q2: Knowledge Gap

**Ask:** "What do we NOT know yet about this? What question, if answered, would change how researchers or practitioners think about this topic?"

**Push until you hear:** A gap that is:
- Specific enough to study (not "we don't understand X well enough")
- Genuinely unresolved (not already answered in existing literature)
- Consequential (answering it matters to someone)

### Q3: Intended Contribution

**Ask:** "What type of contribution do you envision? Pick the closest:"

Present options:
> A) Empirical — new data, experiments, observations
> B) Theoretical / Conceptual — new framework, model, or lens
> C) Methodological — new approach, tool, or technique
> D) Review / Synthesis — organizing and connecting existing knowledge
> E) Applied / Practical — solving a real-world problem with existing theory
> F) Not sure yet

If F: that's fine — proceed, and revisit after Phase 3.

### Q4: Who Cares

**Ask:** "If this paper were published tomorrow, who would read it and what would they do differently? Name a specific type of researcher or practitioner."

**Push until you hear:** A concrete audience and a concrete use. Not "people in field X" but "NLP researchers building multilingual models would reconsider their data selection strategy."

**Red flags:** "Everyone in my field." "The general public." These mean the contribution isn't sharp enough yet.

### Q5: Feasibility Check

**Ask:** "What data, methods, or resources do you have access to (or could reasonably obtain) for this study? What's realistic given your timeline?"

**Push until you hear:** Specifics — datasets, equipment, participant access, time horizon. This grounds the idea in reality.

**If infeasible:** Flag it directly. "This sounds like a 3-year project. Can we find a version that's achievable in your timeframe?"

### Q6: What This Is NOT

**Ask:** "What should this paper explicitly NOT try to do? What's out of scope?"

**Push until you hear:** Clear boundaries. Good research is defined as much by what it excludes as what it includes.

---

**Smart-skip:** If the user's "$ARGUMENTS" or earlier answers already cover a question, skip it. Only ask questions whose answers aren't yet clear.

**Escape hatch:** If the user expresses impatience:
- Say: "I hear you — these questions are the difference between a focused paper and a wandering one. Two more, then we converge."
- Ask the 2 most critical remaining questions, then proceed to Phase 3.
- If the user pushes back a second time, proceed immediately.

---

## PHASE 3: Landscape Check

Do a quick literature scan to position the idea. This is NOT a full literature review — just enough to confirm the gap exists and the framing is viable.

### 3a. Semantic Scholar — check if the question is already answered

Generate 3 search queries from the user's sharpened idea:
1. Core question (direct)
2. Broader field + methodology
3. Key terms + "review OR survey OR meta-analysis"

For each query:
```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=10&fields=title,authors,year,citationCount,abstract&year=2020-2026
```

### 3b. Assess positioning

From the results, determine:
- **Saturated:** >50 recent papers on nearly identical question → suggest narrowing or differentiation
- **Active:** 10-50 papers, clear gap remains → good positioning, proceed
- **Emerging:** <10 papers → opportunity, but verify the question is tractable
- **Novel:** 0 papers → either genuinely new or poorly framed — help user distinguish

Report findings briefly:

> **Landscape snapshot:**
> - Found {N} closely related papers (2020-2026)
> - Most cited: "{title}" ({year}, {citations} citations)
> - Positioning: {Saturated/Active/Emerging/Novel}
> - {1-sentence assessment of gap validity}

If saturated, suggest a differentiation angle via AskUserQuestion before proceeding.

---

## PHASE 4: Boundary Setting

Synthesize Phases 1-3 into a structured problem frame. Present to the user for confirmation:

```
RESEARCH FRAMING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Research Question:  {one clear question}
Contribution Type:  {Empirical / Theoretical / Methodological / Review / Applied}
Target Audience:    {who reads this}
Scope:              {what's IN}
Non-scope:          {what's explicitly OUT}
Key Assumption:     {the premise that must hold for this to work}
Gap Evidence:       {1-sentence summary of why this hasn't been done}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Use AskUserQuestion:
> Does this framing capture your intent? What would you adjust?
> A) This is right — proceed to title options
> B) The question needs adjustment (tell me what)
> C) The scope is too broad / too narrow
> D) I want to rethink the contribution type

If B/C/D: revise and re-present. Loop until confirmed.

---

## PHASE 5: Title Workshop

Generate **5 candidate titles** in different styles. Each title should:
- Reflect the confirmed research question
- Be specific enough to set expectations
- Be concise (aim for under 15 words)

### Title styles to cover:

1. **Descriptive** — states what the paper does
   _Example: "A Survey of Fairness Metrics in Clinical NLP Systems"_

2. **Question-form** — poses the research question directly
   _Example: "Does Prompt Length Affect Reasoning Quality in Large Language Models?"_

3. **Finding-forward** — leads with the key claim or finding
   _Example: "Shorter Prompts, Better Reasoning: Evidence from Controlled LLM Experiments"_

4. **Scope-signal** — emphasizes the boundary or context
   _Example: "Fairness Beyond English: Evaluating Multilingual Bias in Clinical NLP"_

5. **Two-part** — catchy phrase + clarifying subtitle
   _Example: "Less Is More: How Prompt Compression Improves Chain-of-Thought Reasoning"_

Present all 5 via AskUserQuestion:

> Here are 5 title candidates. Pick one to refine, or mix and match:
> 1. {title}
> 2. {title}
> 3. {title}
> 4. {title}
> 5. {title}
> F) None of these — let me describe what I want

If F: ask what's missing, generate 3 more. Repeat until the user picks one.

Once selected, offer one round of refinement:
> Final title: "{selected title}"
> Want to adjust wording, or is this locked in?

---

## OUTPUT: Framing Card

After the title is confirmed, write a framing card to the artifacts directory:

File: `artifacts/{date}-topic-framing-{topic-slug}.md`

```markdown
# Topic Framing Card

**Title:** {confirmed title}
**Date:** {YYYY-MM-DD}

## Research Question
{the sharpened research question}

## Contribution Type
{Empirical / Theoretical / Methodological / Review / Applied}

## Target Audience
{who reads this and what they gain}

## Scope
{what's IN}

## Non-scope
{what's explicitly OUT}

## Key Assumption
{the premise that must hold}

## Gap Evidence
{why this hasn't been done — with paper counts from landscape check}

## Landscape Snapshot
- Related papers found (2020-2026): {N}
- Most cited related work: "{title}" ({year})
- Positioning: {Saturated/Active/Emerging/Novel}

## Candidate Titles Considered
1. {title} ← selected
2. {title}
3. {title}
4. {title}
5. {title}
```

Open the file after writing: `open {file_path}`

---

## NEXT ACTIONS

After delivering the framing card, suggest:

- "Ready to scan the literature? → /lit-search {title keywords}"
- "Want to check if the gap holds up? → /research-gap {topic}"
- "Need to draft an abstract? → /abstract {title}"

---

## ERROR HANDLING

- Idea too vague after all questions: summarize what IS clear, suggest the user talk to their advisor or co-authors, and offer to restart when they have more clarity.
- Idea already well-studied (saturated): help find a differentiation angle — different context, population, method, or theoretical lens.
- Idea too ambitious: help decompose into 2-3 smaller papers and frame the first one.
- User keeps changing direction: after 3 major pivots, pause and say: "We've explored several directions. Let me list them so you can pick the one that excites you most." Present all explored angles for selection.

## TOKEN BUDGET
- Total: ~15-25K (conversational, no subagents)
- Landscape check: ~3-5K
- Most tokens spent on interactive Q&A
