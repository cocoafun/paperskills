## Skills
A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. Below is the list of skills that can be used. Each entry includes a name, description, and file path so you can open the source for full instructions when using a specific skill.
### Available skills
- literature-review: Generate literature reviews and related-work drafts from a user-provided research topic, thesis direction, paper idea, or problem statement. Use when the user asks for 文献综述, related work, state-of-the-art summary, research background, thematic synthesis, research gap analysis, or an evidence-backed review outline in Chinese or English. (file: /Users/young/workspace/paper/paperskills/skills/literature-review/SKILL.md)
- paper-drafting: Use when the user wants to turn a structured research brief, literature synthesis, or study design into an outline, section plan, or evidence-backed paper draft. (file: /Users/young/workspace/paper/paperskills/skills/paper-drafting/SKILL.md)
- paper-tracker: Track newly published papers from specified journals, venues, keywords, authors, or domains and produce a one-shot report. Use when the user asks for recent papers from the last day, week, or month, wants a reading shortlist, contribution one-liners, trend summaries, or a structured HTML report. (file: /Users/young/workspace/paper/paperskills/skills/paper-tracker/SKILL.md)
- peer-review: Review a single academic paper and produce reviewer-style feedback from the paper text, abstract, or a structured brief. Use when the user asks for 审稿, reviewer comments, 审稿意见, mock peer review, rebuttal-oriented critique, accept/reject recommendation, weak accept, weak reject, or a structured review report in Chinese or English. (file: /Users/young/workspace/paper/paperskills/skills/peer-review/SKILL.md)
- research-design: Use when the user wants to transform literature gaps or a problem statement into research questions, hypotheses, methods, variables, data plans, or an empirical or theoretical study design. (file: /Users/young/workspace/paper/paperskills/skills/research-design/SKILL.md)
- research-scoping: Use when a research request is broad, fuzzy, or under-scoped and needs to be turned into a concrete question set, boundary, keyword plan, and downstream research brief. (file: /Users/young/workspace/paper/paperskills/skills/research-scoping/SKILL.md)
- revision-planning: Use when the user has review comments, internal critique, or rebuttal feedback and needs a structured revision plan, response strategy, and prioritized task list. (file: /Users/young/workspace/paper/paperskills/skills/revision-planning/SKILL.md)
- using-paperskills: Use when starting any research-oriented conversation to identify the current research stage and route the agent to the correct PaperSkills workflow before answering directly. (file: /Users/young/workspace/paper/paperskills/skills/using-paperskills/SKILL.md)
- writing-paperskills: Use when creating new PaperSkills skills, editing existing ones, or aligning skill design with the repository's workflow, schema, and evidence-discipline conventions. (file: /Users/young/workspace/paper/paperskills/skills/writing-paperskills/SKILL.md)
### How to use skills
- Discovery: The list above is the skills available in this session (name + description + file path). Skill bodies live on disk at the listed paths.
- Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown above, you must use that skill for that turn. Multiple mentions mean use them all. Do not carry skills across turns unless re-mentioned.
- Missing/blocked: If a named skill isn't in the list or the path can't be read, say so briefly and continue with the best fallback.
- How to use a skill (progressive disclosure):
  1) After deciding to use a skill, open its `SKILL.md`. Read only enough to follow the workflow.
  2) When `SKILL.md` references relative paths (e.g., `scripts/foo.py`), resolve them relative to the skill directory listed above first, and only consider other paths if needed.
  3) If `SKILL.md` points to extra folders such as `references/`, load only the specific files needed for the request; don't bulk-load everything.
  4) If `scripts/` exist, prefer running or patching them instead of retyping large code blocks.
  5) If `assets/` or templates exist, reuse them instead of recreating from scratch.
- Coordination and sequencing:
  - If multiple skills apply, choose the minimal set that covers the request and state the order you'll use them.
  - Announce which skill(s) you're using and why (one short line). If you skip an obvious skill, say why.
- Context hygiene:
  - Keep context small: summarize long sections instead of pasting them; only load extra files when needed.
  - Avoid deep reference-chasing: prefer opening only files directly linked from `SKILL.md` unless you're blocked.
  - When variants exist (frameworks, providers, domains), pick only the relevant reference file(s) and note that choice.
- Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best approach, and continue.
