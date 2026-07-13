<p align="center">
  <img src="./logo-readme.png" alt="PaperSkills" width="80" />
</p>

<h1 align="center">PaperSkills</h1>

<p align="center"><strong>PaperSkills is an AI-agent academic workbench for researchers.</strong></p>

<p align="center">
  Find, combine, and install the Agent Skills your current research task needs
</p>

<p align="center">
  <a href="https://www.paperskills.com/en"><strong>Start from a research scenario</strong></a>
  · <a href="https://www.paperskills.com/en/skills">Browse 349 Skills</a>
  · <a href="./registry/scenarios.json">Scenario catalog</a>
  · <a href="./README.zh-CN.md">中文说明</a>
</p>

## AI tools are everywhere. The hard part is putting them to work in research.

There are more AI tools, agents, and Skills every day. Faced with so many choices, many researchers do not lack tools—they simply do not know what to choose, where to begin, or how to bring those tools into a real research workflow.

- This tool looks powerful, but does it actually fit my research question?
- I found a promising Skill. What should I prepare, and what should I ask first?
- Skills live across different repositories. How do I install them, and will they work with my agent?
- A tool can finish one search, analysis, or writing task. How do I connect those steps into a real research workflow?
- The AI produced an answer. What should I check, and what comes next?

**PaperSkills is here to shorten that path—helping you use AI tools effectively and move your research forward faster.** We select high-quality research Skills from open-source repositories, then organize them into understandable research scenarios, ready-to-use Skill combinations, and install commands you can copy and run. You do not need to study every AI tool first. Tell PaperSkills what you are trying to accomplish, and it will help you find a practical place to start.

## What is in PaperSkills today

| What you can use | Current scale | What it helps with |
| --- | ---: | --- |
| Installable Skills | **349** | Research workflows, writing and editing, research engineering, figures, and visualization |
| Repositories | **13** | PaperSkills Core plus 12 external Skill sources |
| Research scenarios | **12** | What to prepare, which Skills to use, what to ask, and what to expect |
| Scenario groups | **4** | From questions and evidence to computational research, lab infrastructure, and publication |
| Skill Packs | **7** | Reusable combinations of Skills that often work together |
| Agent compatibility | **Broad** | Works with agents that support Skills, with deeper integration for four major agents |

PaperSkills Core is one locally maintained collection with 9 Skills. **It is only one part of the 349 installable Skills, not the whole of PaperSkills.** The other 340 Skills come from 12 external Skill sources.

## Not sure what to choose? That is okay.

### 1. Start from a research scenario

If you do not yet know which Skill you need, do not start by reading the entire catalog. Open the [PaperSkills home page](https://www.paperskills.com/en) and choose the scenario closest to the work in front of you. Each scenario helps you work out:

- What input materials to prepare
- Which Skills to combine
- What Prompt to use at each step
- What intermediate outputs to expect
- Which scenario may come next

The 12 current scenarios are organized into four groups that reflect real research work:

| Scenario group | Workflows included |
| --- | --- |
| From questions to evidence | Literature and evidence, study design and statistics, data-analysis pipelines |
| Computational and disciplinary research | AI and model experiments, life-science data, proteins/molecules/materials, geospatial and physical science |
| Labs, compute, and reusable workflows | Lab automation, compute environments, custom research agents |
| Publication and research communication | Manuscripts and submission, figures and presentations |

A scenario is more than a static list of recommended tools. It connects Skills into a workflow you can follow, showing what to ask, what you should receive, and where to go next. See the full data in [`registry/scenarios.json`](./registry/scenarios.json).

### 2. Already know the task? Use the Skills installer.

Open the [Skills installer](https://www.paperskills.com/en/skills) and:

1. Filter by workflow and methods, writing and editing, research and engineering, or figures and visualization.
2. Select a full collection or choose a single Skill from inside it.
3. Choose macOS / Linux or Windows.
4. Choose one of the agents with first-class integration: Claude Code, Codex, Cursor, or OpenCode.
5. Copy the generated install command and run it in your terminal.

The Skills in PaperSkills are not limited to these four agents. If your agent supports Skills or follows a compatible directory convention, you can usually use them there as well. Claude Code, Codex, Cursor, and OpenCode currently receive the most complete install-command and path integration.

You can also carry a recommended combination directly from a scenario into the installer instead of finding the same Skills again one by one.

## Where these Skills come from

PaperSkills is not limited to the Skills we maintain ourselves. We also curate high-quality Skills from open-source projects we trust. We look for Skills that solve real research problems, explain how they should be used, and fit into practical workflows. For every entry, we keep the source, license, and installation details clear, then bring everything together in one searchable, installable catalog.

| Type | Currently included |
| --- | --- |
| PaperSkills local collection | PaperSkills Core (9 Skills) |
| General agent workflows | Superpowers, Karpathy-Inspired Claude Code Guidelines, Qiushi Skill |
| Research agents and disciplinary tools | Scientific Agent Skills, AI Research Skills, Nature Skills, Claude Science |
| Writing and language | Humanizer, Humanizer ZH, Paper Polish Workflow |
| Research figures and presentation | Scientific Visualization, PosterSkill |

These external sources contribute 340 installable Skills. Together with the 9 Skills in PaperSkills Core, they make up the 349 Skills currently shown in the installer. Each Skill's source, open-source license, and installation details are recorded in [`registry/academicforge-skills.json`](./registry/academicforge-skills.json) and [`registry/skills.json`](./registry/skills.json).

## For maintainers: how the Registry is organized

If you want to understand the data behind the website and installer, start with `registry/`:

```text
registry/
├── skills.json                  # 9 local Skills in PaperSkills Core
├── academicforge-skills.json    # 12 external collections or entries, 340 Skills
├── academicforge-overrides.json # Curated external Skills referenced by scenarios
├── scenarios.json               # 12 research scenarios and their full workflows
└── packs.json                   # 7 reusable Skill Packs
```

The website, scenario pages, and installer all read from this Registry, so a Skill does not need to be maintained in several places:

- Scenarios combine local and external Skills through `skillIds`.
- A collection can be installed as a whole or expanded to install individual Skills.
- The installer uses repository, path, and revision metadata to generate commands for different agents.
- The website and agents can read the same Skill data through structured endpoints.

Agent-facing entry points include [`/SKILL.md`](https://www.paperskills.com/SKILL.md), [`/api/skills`](https://www.paperskills.com/api/skills), and [`/api/scenarios`](https://www.paperskills.com/api/scenarios).

## Repository structure

```text
.
├── SKILL.md                 # PaperSkills agent router
├── skills/                  # Skills maintained by PaperSkills
├── registry/                # Skill, scenario, collection, and source metadata
├── docs/                    # English and Chinese documentation
├── assets/                  # Shared report templates and resources
├── scripts/                 # Cross-agent installers served by the website
└── setup                    # Post-install link setup
```

## Design principles

- **Scenario-first**: understand the researcher's current task before recommending Skills and next steps.
- **Curated**: prioritize high-quality Skills that solve real research problems and work in practical workflows.
- **Agent-native**: work broadly across agents, with deep integration and ready-to-run install commands for Claude Code, Codex, Cursor, and OpenCode.
- **Composable**: use one Skill for a focused task or combine several into a complete research workflow.
- **Traceable**: preserve source repositories, licenses, install paths, scenario steps, and expected outputs.

## References and thanks

The breadth of PaperSkills comes from the many Skill authors and open-source maintainers who turn their experience into reusable tools. We are grateful for their work. The following projects have also shaped how we think about the product and its workflows:

- [HughYau/AcademicForge](https://github.com/HughYau/AcademicForge): an important reference for Skill Registry design, cross-agent distribution, collection installs, and Skill selection.
- [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing): a broad map of tools and resources for AI-assisted academic research and writing.
- [hkcanan/katmer-code](https://github.com/hkcanan/katmer-code): inspiration for research-writing workflows, citation verification, and peer-review reports.

We will keep learning from these projects and their approaches to distribution, tool curation, and workflow design. **PaperSkills is an AI-agent academic workbench for researchers.** When the growing landscape of AI tools feels difficult to navigate, we hope PaperSkills helps you spend less time guessing and move your research forward sooner.

## License

MIT
