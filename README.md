# PaperSkills

Academic research skills for Claude Code, Cursor, and Codex.

[中文说明](./README.zh-CN.md) | [Project homepage](https://www.paperskills.com/)

## Why This Exists

If you have ever spent an afternoon rewriting the same literature-search prompt, checking whether a citation is real, or asking an AI reviewer to be "more rigorous" for the fifth time, you have already felt the problem.

AI is becoming part of everyday research work, but the useful know-how is still unevenly distributed. Some labs have internal prompt libraries, review rubrics, paper-tracking routines, and citation-checking workflows. Many researchers are still stitching those steps together from scratch, one chat at a time.

PaperSkills tries to close that gap.

It is not another pile of loose prompts. It is an open, agent-native skill library that turns repeatable academic tasks into callable workflows: topic framing, literature search, research-gap analysis, abstract writing, citation verification, peer review, journal matching, citation-network mapping, and paper tracking.

The goal is simple:

**Spend less time rebuilding the research workflow, and more time doing the research.**

## What PaperSkills Does

PaperSkills gives AI coding agents a practical research-workflow layer.

Instead of explaining the whole process every time, you can invoke a skill directly:

```text
/lit-search foundation models for scientific discovery
/peer-review draft.md
/cite-verify my-manuscript.md
/paper-tracker track new Nature papers in the last month
```

Each skill is designed around one research job. It defines the task, the expected inputs, the workflow, the report shape, and the public data sources to use when verification or search is needed.

This makes PaperSkills useful in three ways:

- For researchers: reduce repeated prompt engineering and get more structured outputs.
- For students: learn what a serious research workflow looks like by using it.
- For builders: extend the library with new skills, templates, reports, and agent integrations.

## Available Skills

| Skill | What it helps with | Token Budget |
|-------|--------------------|--------------|
| `/topic-framing` | Converge from a fuzzy idea to a concrete research question or paper title | 15-25K |
| `/lit-search` | Search literature across Semantic Scholar, OpenAlex, PubMed, arXiv, and related sources | 15-25K |
| `/abstract` | Generate abstracts in IMRaD, thematic, extended, and short formats | 10-20K |
| `/cite-verify` | Verify citations against CrossRef, Semantic Scholar, OpenAlex, and other public sources | 25-65K |
| `/citation-network` | Build and visualize citation networks with an interactive HTML report | 35-55K |
| `/research-gap` | Analyze temporal, methodological, thematic, and application-level research gaps | 55-85K |
| `/peer-review` | Review a draft with structured academic criteria, scoring, and report output | 35-60K |
| `/paper-tracker` | Track new papers by journal, author, venue, keyword, institution, or time window | 15-30K |
| `/journal-match` | Recommend suitable target journals for a manuscript | 25-35K |

## Recommended Workflow

PaperSkills can be used one skill at a time, but it is most useful when the skills are chained into a research process:

1. `/topic-framing` - sharpen the idea and research question
2. `/lit-search` - find relevant literature
3. `/research-gap` - identify what is still missing
4. `/abstract` - draft or reshape the abstract
5. `/peer-review` - stress-test the manuscript
6. `/cite-verify` - verify references before submission
7. `/journal-match` - choose target journals
8. `/paper-tracker` - keep watching the field after the first pass

You can also use the router entry point for guided dispatch:

```text
/paperskills help me search papers about LLM-assisted literature review writing
```

## Design Principles

- `Skill-first`: each skill solves one clear research task.
- `Agent-native`: built for Claude Code, Cursor, Codex, and similar coding agents.
- `Composable`: skills can run alone or as part of a larger workflow.
- `Open stack`: search and verification prefer public, inspectable data sources.
- `Practical over fancy`: optimize for recurring research work, not demos.
- `Readable by humans`: every skill should be understandable and editable.

## Installation

### Claude Code

#### Global install

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.claude/skills/paperskills
cd ~/.claude/skills/paperskills && ./setup
```

#### Single-project install

```bash
mkdir -p .claude/skills
ln -s /path/to/paperskills .claude/skills/paperskills
cd .claude/skills/paperskills && ./setup
```

`./setup` creates sibling links such as `.claude/skills/peer-review` and `.claude/skills/shared`, so report-generating skills can read shared assets. Re-run `./setup` after updating PaperSkills.

### Cursor

Cursor does not currently discover `SKILL.md` files natively. The practical install path is to add PaperSkills as a project-local prompt library and point Cursor Rules at it.

Tell Cursor:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.cursor/INSTALL.md
```

Or follow the manual steps in [`.cursor/INSTALL.md`](.cursor/INSTALL.md).

### Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.codex/INSTALL.md
```

Or install manually:

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.agents/skills/paperskills
cd ~/.agents/skills/paperskills && ./setup
```

`./setup` also links the shared assets directory required by report-generating skills.

## Language Support

Report-generating skills support English and Chinese output. Language is auto-detected from manuscript content, or can be explicitly requested:

```text
Generate the report in Chinese.
```

Currently supported report skills include:

- `cite-verify`
- `citation-network`
- `journal-match`
- `research-gap`
- `peer-review`
- `paper-tracker`

## Project Structure

- `SKILL.md`: project-level router entry
- `skills/`: standalone academic skills
- `assets/`: shared report templates and resources
- `artifacts/`: generated outputs and examples
- `.codex/`: Codex installation notes
- `.cursor/`: Cursor installation notes
- `setup`: link setup script for native skill discovery

## Inspiration

PaperSkills is inspired by open academic AI-writing and agent-workflow projects, including [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) and [hkcanan/katmer-code](https://github.com/hkcanan/katmer-code).

## License

MIT
