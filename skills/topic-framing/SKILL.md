---
name: topic-framing
description: Help converge from a fuzzy academic idea to a concrete, researchable paper framing and title through structured dialogue. Produces a one-shot framing card in HTML by default, with Markdown as an explicit fallback.
---

Help the user converge from a fuzzy academic idea to a concrete, researchable paper framing and title. Input: "$ARGUMENTS".

Input may specify:
- **Seed idea**: keyword, topic area, puzzle, case, debate, or half-formed question
- **Goal**: sharpen question, test framing viability, improve literature positioning, or finalize a title
- **Output**: HTML framing card, markdown framing card, or short in-chat framing summary

Examples:
- `frame a paper topic about AI search ads and advertiser strategy`
- `帮我把“平台算法治理”收敛成一个可写论文题目`
- `turn this fuzzy idea into a researchable title and output html`

Do NOT use subagents. Do NOT jump into full literature review, detailed method design, or manuscript drafting. This skill ends at a confirmed academic framing and title.

## MAIN FLOW

```
Main Session — academic framing dialogue
  │
  ├── PHASE 1: Seed Capture — restate the initial idea as a research interest
  ├── PHASE 2: Academic Sharpening — six framing questions, one at a time
  ├── PHASE 3: Literature Positioning — quick scan to test whether the framing is viable
  ├── PHASE 4: Framing Synthesis — question, gap, contribution, boundaries
  ├── PHASE 5: Title Workshop — generate and refine academic title options
  └── PHASE 6: Output Framing Card
```

---

## PHASE 1: Seed Capture

Parse "$ARGUMENTS" as the user's starting point. It may be a keyword, a topic area, a puzzle, a case, or a half-formed question.

Also extract:
- **Language**: follow the user's explicit request; otherwise infer from the prompt
- **Output format**:
  - short answer in chat
  - HTML framing card
  - markdown framing card

If the user does not specify an output format, default to a single-file HTML framing card.

Restate the idea in 2-3 sentences as an academic research interest. Avoid business, product, or project-language. Frame it as:
- a phenomenon worth explaining
- a debate worth clarifying
- a body of literature worth extending, challenging, or connecting

Then ask:

> I understand your current research interest roughly as: "{restatement}".
> Which of these best describes where you are now?
> A) I only have a broad topic or phenomenon
> B) I have a tentative research question
> C) I have several possible academic angles
> D) I mostly need help sharpening the title

Use AskUserQuestion.

Prioritize Phase 2 accordingly:
- A → ask all six questions
- B → focus on Q2-Q6
- C → collect the angles first, then run Q2-Q6 on the strongest
- D → verify Q3-Q6 before moving to titles

---

## PHASE 2: Academic Sharpening — Six Framing Questions

Ask these ONE AT A TIME via AskUserQuestion. Wait for each answer before proceeding.

The goal is not to help the user "start a project." The goal is to identify a researchable academic claim.

### Q1: Research Puzzle

**Ask:** "What is the specific phenomenon, inconsistency, tension, or underexplained pattern that makes this worth studying?"

**Push until you hear:** a genuine scholarly puzzle, such as:
- something the literature assumes but may not fully explain
- two findings, concepts, or trends that do not fit neatly together
- a recurring empirical pattern without a satisfying explanation

Do NOT accept answers that only name a field or topic area.

### Q2: Literature Location

**Ask:** "Which literature or conversation should this paper enter? If you had to place it into 1-2 scholarly conversations, what are they?"

**Push until you hear:** identifiable academic terrain, not a vague domain label.

Good answers sound like:
- "platform governance and algorithmic management"
- "comparative political economy of industrial policy"
- "second-language writing assessment and feedback research"

If the user cannot answer, infer likely literatures from their description and ask them to confirm.

### Q3: Gap or Tension

**Ask:** "Within that literature, what is missing, unresolved, conflated, or insufficiently explained?"

**Push until you hear:** one of the following:
- an empirical gap: a context, case, population, or period not adequately studied
- a theoretical gap: concepts are underspecified, in tension, or poorly integrated
- a methodological gap: existing approaches obscure an important aspect
- a debate gap: the field has competing claims without clear adjudication

Reject weak formulations like "few people studied this" unless the user can explain why that absence matters academically.

### Q4: Core Contribution

**Ask:** "What should this paper contribute to scholarship? Pick the closest:"

Present options:
> A) Explain a phenomenon more convincingly
> B) Clarify or refine a concept
> C) Reconcile or challenge existing theories
> D) Extend a literature to a new case, context, or body of evidence
> E) Compare competing explanations
> F) Synthesize scattered work into a clearer framework
> G) Not sure yet

If G, proceed and infer provisionally after Phase 3.

### Q5: Unit of Analysis and Evidence

**Ask:** "What is the actual object of study here? What will the paper analyze: texts, cases, organizations, policies, experiments, interviews, archives, datasets, or something else?"

**Push until you hear:** a concrete unit of analysis and plausible evidence base.

This is not full method design. It is a sanity check that the framing corresponds to something academically investigable.

### Q6: Boundaries of the Claim

**Ask:** "What should this paper explicitly NOT claim, cover, or try to solve?"

**Push until you hear:** scope boundaries such as:
- time period
- geography or case selection
- disciplinary boundary
- level of explanation
- what kind of causal or normative claim the paper will not make

Strong academic framing depends on disciplined limits.

---

**Smart-skip:** If "$ARGUMENTS" or earlier answers already cover a question clearly, skip it.

**Follow-up rule:** If the user answers vaguely, ask a tighter follow-up instead of moving on. Example:
- "Can you name the exact debate?"
- "What kind of gap is that, theoretically or empirically?"
- "What is the paper actually explaining?"

**Escape hatch:** If the user becomes impatient:
- Say: "We can compress this. I only need the puzzle, the literature, and the contribution to make the title academically sharp."
- Ask the most critical remaining questions, then proceed.

---

## PHASE 3: Literature Positioning

Do a quick scan to test whether the framing is academically viable. This is not a full review. Use it to check:
- whether the question is already saturated
- whether the literature named by the user is the right one
- whether the apparent gap is real, overstated, or needs reframing

### 3a. Generate search queries

Create 3 search queries from the sharpened idea:
1. Direct formulation of the research question
2. Literature-level formulation using the main scholarly conversation
3. Gap-focused query with terms like "review", "debate", "framework", "meta-analysis", or the key theoretical concepts

### 3b. Semantic Scholar scan

For each query:
```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=10&fields=title,authors,year,citationCount,abstract&year=2020-2026
```

### 3c. Interpret positioning

Classify the idea:
- **Saturated:** many recent papers answer essentially the same question
- **Active but open:** established conversation, but the gap still looks defensible
- **Fragmented:** related work exists, but concepts/cases are disconnected
- **Emerging:** only a small body of directly relevant work
- **Poorly framed:** search results suggest the question is too vague or using the wrong vocabulary

Report briefly:

> **Literature snapshot:**
> - Found {N} closely related papers (2020-2026)
> - Most relevant anchor paper: "{title}" ({year}, {citations} citations)
> - Positioning: {classification}
> - Initial judgment: {1-2 sentences on whether the gap framing holds}

If the framing looks weak or saturated, revise the framing before moving on. Typical revisions:
- narrow the phenomenon
- shift from broad topic to specific debate
- move from "study X" to "explain Y in X"
- replace generic novelty claims with a more precise contribution

---

## PHASE 4: Framing Synthesis

Synthesize the conversation into a compact academic framing and present it for confirmation:

```
ACADEMIC FRAMING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Working Question:    {one clear research question}
Research Puzzle:     {what is puzzling or unresolved}
Primary Literature:  {the conversation this paper enters}
Gap / Tension:       {what is missing, unclear, or contested}
Contribution Claim:  {what the paper contributes to scholarship}
Unit of Analysis:    {what is being analyzed}
Scope:               {what is IN}
Non-scope:           {what is OUT}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then ask:

> Does this capture the paper you actually want to write?
> A) Yes — move to title options
> B) The question needs adjustment
> C) The literature positioning is off
> D) The contribution claim is not right yet
> E) The scope is too broad or too narrow

If B/C/D/E: revise and re-present until confirmed.

---

## PHASE 5: Title Workshop

Generate 5 academic title candidates. Each title should:
- reflect the confirmed question and contribution
- signal the paper's intellectual center, not just the topic area
- avoid startup, consulting, or product language
- be concise and credible as a journal or conference paper title

Cover these title styles:

1. **Direct descriptive**
   - states the subject and contribution plainly

2. **Question-driven**
   - foregrounds the research question

3. **Concept-first**
   - highlights the theoretical concept or debate

4. **Case-and-claim**
   - ties the empirical site to the broader contribution

5. **Two-part academic subtitle**
   - short lead phrase + precise explanatory subtitle

Present all 5 via AskUserQuestion:

> Here are 5 candidate titles. Which direction is closest?
> 1. {title}
> 2. {title}
> 3. {title}
> 4. {title}
> 5. {title}
> F) None of these — I want a different emphasis

If F, ask what emphasis is missing:
- stronger theory signal
- sharper empirical focus
- clearer comparative angle
- less ambitious claim
- more conventional journal style

Generate 3 revised options and repeat until the user picks one.

Once one is selected, offer one final refinement pass:

> Final title: "{selected title}"
> Should we tighten wording further, or lock this in?

---

## PHASE 6: Output Framing Card

After the title is confirmed, produce a one-shot framing card.

Default output is a single-file HTML report.

Suggested filename:
`artifacts/{date}-topic-framing-{topic-slug}.html`

For HTML output include:
- header with topic, confirmed title, and date
- executive summary
- framing grid or card layout
- literature snapshot block
- title candidates section with the selected title clearly marked
- methodology / positioning note summarizing how the framing was derived

Required framing fields:
- confirmed title
- working question
- research puzzle
- primary literature
- gap / tension
- contribution claim
- unit of analysis
- scope
- non-scope
- literature snapshot
- candidate titles considered

Suggested HTML structure:

```html
<html lang="{lang}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Topic Framing Card - {short topic}</title>
  </head>
  <body>
    <header>
      <h1>Topic Framing Card</h1>
      <p>{confirmed title}</p>
      <p>{date}</p>
    </header>

    <section>
      <h2>Executive Summary</h2>
      <p>{2-4 sentence synthesis of the framing}</p>
    </section>

    <section>
      <h2>Academic Framing</h2>
      <div>{working question}</div>
      <div>{research puzzle}</div>
      <div>{primary literature}</div>
      <div>{gap / tension}</div>
      <div>{contribution claim}</div>
      <div>{unit of analysis}</div>
      <div>{scope}</div>
      <div>{non-scope}</div>
    </section>

    <section>
      <h2>Literature Snapshot</h2>
      <p>{related papers count, anchor paper, positioning}</p>
    </section>

    <section>
      <h2>Candidate Titles Considered</h2>
      <ol>
        <li>{selected title}</li>
        <li>{title}</li>
        <li>{title}</li>
        <li>{title}</li>
        <li>{title}</li>
      </ol>
    </section>
  </body>
</html>
```

After writing the HTML file:
- Return the exact absolute file path to the user
- Ask whether they want it opened
- Only run `open {file_path}` after the user explicitly confirms

If the user explicitly asks for Markdown, write:

File: `artifacts/{date}-topic-framing-{topic-slug}.md`

```markdown
# Topic Framing Card

**Title:** {confirmed title}
**Date:** {YYYY-MM-DD}

## Executive Summary
{2-4 sentence synthesis of the framing}

## Working Question
{the sharpened research question}

## Research Puzzle
{what is puzzling or unresolved}

## Primary Literature
{which scholarly conversation this paper enters}

## Gap / Tension
{what is missing, unclear, or contested}

## Contribution Claim
{what this paper contributes to scholarship}

## Unit of Analysis
{what is being analyzed}

## Scope
{what is IN}

## Non-scope
{what is explicitly OUT}

## Literature Snapshot
- Related papers found (2020-2026): {N}
- Anchor paper: "{title}" ({year})
- Positioning: {Saturated / Active but open / Fragmented / Emerging / Poorly framed}

## Candidate Titles Considered
1. {title} ← selected
2. {title}
3. {title}
4. {title}
5. {title}
```

Return the framing card content in chat too, even if file write is not available.

---

## STYLE RULES

- Default to academic language, not startup or product language.
- Treat "why this matters to scholarship" as more important than "who would use it tomorrow."
- Prefer "research puzzle", "literature", "theoretical framing", "contribution", and "scope" over "customer", "stakeholder", "solution", or "go-to-market" phrasing.
- Do not pressure the user into false novelty. Help them articulate a defensible, modest, and credible contribution.
- If the user's idea is practice-driven, translate it into an academic puzzle instead of rejecting it.
- If the user is early-stage, tolerate ambiguity but keep forcing movement toward a specific research question.

## ERROR HANDLING

- If the topic is far too broad, narrow to one phenomenon, case, debate, or comparison.
- If the topic is too narrow or trivial, widen from case description to a more general analytical question.
- If the literature scan suggests the user is using the wrong vocabulary, propose better field terms.
- If the gap appears already filled, say so directly and help reposition the question.

## LANGUAGE

- If the user explicitly requests a language, use that language.
- Otherwise infer from the prompt.
- If the user writes mainly in Chinese, conduct the dialogue and final card in Chinese.
- Otherwise, default to English.

When generating in Chinese:
- Set `<html lang="zh">`
- Use Chinese headings and labels
- Keep paper titles, journal names, and API names in original form where appropriate
- Use Chinese punctuation
