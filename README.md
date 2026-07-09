# PaperSkills

<p align="center">
  <img src="./logo-readme.png" alt="PaperSkills logo" width="120" />
</p>

Scenario-based academic workflow skills for AI agents.

[中文说明](./README.zh-CN.md) | [Project homepage](https://www.paperskills.com/)

## What PaperSkills Is

PaperSkills helps researchers decide **which AI-agent skills to use, how to install them, what prompt to start with, and what output to expect** at each stage of a real research project.

It is not just a prompt collection, and it is no longer positioned as only a standalone skill library. The project now has two connected layers:

- A skill distribution layer: install academic skills for Claude Code, Codex, Cursor, OpenCode, and similar agents.
- A research-scenario layer: start from the user's current research situation, then recommend the right skills, prompts, outputs, and next steps.

The goal is simple:

**Make AI-agent research workflows installable, understandable, and usable in actual paper work.**

## Start From A Research Situation

Instead of asking users to browse a long skill list first, PaperSkills is organized around common research moments:

| Situation | Recommended workflow |
|-----------|----------------------|
| I am entering a new field | `/lit-search` + `/citation-network` + `/research-gap` + `/paper-tracker` |
| I have an interest area but no publishable question | `/topic-framing` + `/research-gap` + `/lit-search` |
| I need to synthesize evidence from papers | literature review + PDF exploration + `/cite-verify` + visualization skills |
| I already have a manuscript draft | `/abstract` + `/peer-review` + `/cite-verify` + `/journal-match` |
| I am preparing submission | `/journal-match` + `/peer-review` + `/abstract` + `/cite-verify` |
| I need research figures or artifacts | scientific visualization, figure composition, and web artifact skills |
| I want a lab-specific agent workflow | skill creation, customization, learning, and self-audit skills |

The structured scenario catalog lives in [`registry/scenarios.json`](./registry/scenarios.json), and skill packs live in [`registry/packs.json`](./registry/packs.json).

## Core Skills In This Package

The PaperSkills core package currently maintains these academic paper-workflow skills:

| Skill | What it helps with |
|-------|--------------------|
| `/topic-framing` | Turn a broad interest into a researchable, publishable, executable paper topic |
| `/lit-search` | Search scholarly literature across public academic APIs and organize results |
| `/research-gap` | Extract credible research gaps and contribution space from the literature |
| `/citation-network` | Map key papers, authors, themes, and citation relationships |
| `/abstract` | Compress the question, method, findings, and contribution into a clear abstract |
| `/peer-review` | Simulate academic peer review and identify structure, evidence, contribution, and submission risks |
| `/cite-verify` | Check whether cited sources support manuscript claims and reduce citation risk |
| `/journal-match` | Match a manuscript to journals by topic, method, contribution, and risk |
| `/paper-tracker` | Track topics, authors, journals, and keywords as reusable paper monitoring lists |

The registry can also reference external or future skills for broader scenario packs, such as literature-review, PDF exploration, scientific visualization, figure composition, compute infrastructure, and domain-specific modeling workflows.

## Example Use

You can call a specific skill directly:

```text
/topic-framing I want to study LLM-assisted literature review writing. Help me turn this into publishable research questions.
/lit-search Search recent and highly cited papers about AI-assisted systematic literature reviews.
/peer-review draft.md Please review this manuscript as a journal reviewer and prioritize revision risks.
/cite-verify draft.md Check whether the cited sources actually support the claims in the text.
```

Or use the router entry point:

```text
/paperskills I am entering a new field about AI search advertising. Help me choose the right workflow.
```

## Installation

### Claude Code

```bash
curl -sSL https://paperskills.com/scripts/paperskills-install.sh | bash -s -- \
  --tool claude \
  --skills paperskills-core \
  --registry https://paperskills.com/api/registry
```

### Codex

```bash
curl -sSL https://paperskills.com/scripts/paperskills-install.sh | bash -s -- \
  --tool codex \
  --skills paperskills-core \
  --registry https://paperskills.com/api/registry
```

### Cursor

Cursor uses rules/prompt installation in the current MVP.

```bash
curl -sSL https://paperskills.com/scripts/paperskills-install.sh | bash -s -- \
  --tool cursor \
  --skills paperskills-core \
  --registry https://paperskills.com/api/registry
```

### OpenCode

```bash
curl -sSL https://paperskills.com/scripts/paperskills-install.sh | bash -s -- \
  --tool opencode \
  --skills paperskills-core \
  --registry https://paperskills.com/api/registry
```

PaperSkills keeps skill metadata in a registry so installers and integrations can generate agent-specific commands. See [`registry/skills.json`](./registry/skills.json) for supported platforms and sparse-checkout paths.

## Repository Structure

- [`SKILL.md`](./SKILL.md): router entry point for PaperSkills
- [`skills/`](./skills): core academic workflow skills
- [`registry/`](./registry): skill, scenario, and pack metadata
- [`docs/`](./docs): English and Chinese documentation pages
- [`assets/`](./assets): shared report templates and resources
- [`scripts/`](./scripts): public installer scripts served by the PaperSkills website
- [`setup`](./setup): link setup script for skill discovery

## Design Principles

- `Scenario-first`: users should begin from their research situation, not from a catalog they have to decode.
- `Skill-native`: every workflow remains installable and callable inside real AI agents.
- `Composable`: skills can be used alone or chained into a paper lifecycle.
- `Traceable`: literature search, citation checking, and journal matching should prefer public, inspectable sources.
- `Practical`: optimize for recurring research work, not demo-only interactions.
- `Extensible`: the registry should support core skills, external skills, and future skill packs.

## Language Support

Report-generating skills support English and Chinese output. Language is auto-detected from manuscript content, or can be explicitly requested:

```text
Generate the report in Chinese.
```

## Roadmap

The current MVP focuses on:

- Scenario pages for common research stages
- A registry for skills, packs, and recommended workflows
- Install command generation across agent platforms
- Copyable prompts and expected outputs for each scenario
- Core academic paper skills that can run locally in agent environments

Future work includes external skill packs, saved presets, paper-tracker watchlists, richer agent indexes, and more domain-specific research workflows.

## References And Thanks

PaperSkills is built with gratitude for projects that explored academic skills, AI research writing, and agent-native distribution before it:

- [HughYau/AcademicForge](https://github.com/HughYau/AcademicForge): a major reference for skill registry design, install-command generation, cross-agent packaging, and the idea of making academic skills easy to distribute.
- [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing): a useful map of AI tools and resources for academic research and writing.
- [hkcanan/katmer-code](https://github.com/hkcanan/katmer-code): inspiration for agent workflow organization and research-oriented coding-agent practices.

PaperSkills borrows from those foundations, but its product direction is different: distribution is the infrastructure; scenario-based research workflow guidance is the main experience.

## License

MIT
