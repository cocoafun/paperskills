# PaperSkills for Codex

Academic research skills library for OpenAI Codex. Each skill is a standalone `.md` file that handles one research task using public APIs (Semantic Scholar, OpenAlex, CrossRef, Unpaywall, etc.).

## Quick Install

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.codex/INSTALL.md
```

## Manual Installation

### Prerequisites

- OpenAI Codex CLI

### Steps

1. Create the skills directory if needed:
   ```bash
   mkdir -p ~/.agents/skills
   ```

2. Link the repository `skills/` directory into Codex's skills path:
   ```bash
   ln -s /path/to/paperskills/skills ~/.agents/skills/paperskills
   ```

3. Restart Codex.

## How It Works

Codex scans `~/.agents/skills/` at startup and loads matching skills on demand. PaperSkills becomes visible through a single symlink:

```text
~/.agents/skills/paperskills/ -> /path/to/paperskills/skills/
```

## Available Skills

| Skill | Description | Token Budget |
|-------|-------------|--------------|
| `lit-search` | Search academic literature across Semantic Scholar, OpenAlex, PubMed, arXiv | 15–25K |
| `cite-verify` | Verify all citations in a manuscript against CrossRef / Semantic Scholar / OpenAlex | 25–65K |
| `citation-network` | Build and visualize citation networks from seed papers with HTML report | 35–55K |
| `research-gap` | Analyze research gaps (temporal, methodological, thematic, application) | 55–85K |
| `peer-review` | Academic peer review with 8-criteria scoring and radar chart report | 35–60K |
| `journal-match` | Recommend target journals for manuscript submission | 25–35K |
| `abstract` | Generate abstracts in multiple formats (IMRaD, thematic, extended, short) | 10–20K |
| `report-template` | Design system specification for all HTML reports (academic book aesthetic) | — |

## Usage

Once installed, ask Codex for a research task in natural language, for example:

```text
帮我检索关于大模型支持文献综述写作的文献，用 lit-search。
```

Or name the skill explicitly:

```text
Use cite-verify to check all citations in my manuscript draft.md
```

Skills can be composed for multi-step workflows, e.g.:

1. `lit-search` → find relevant papers
2. `research-gap` → identify gaps in the field
3. `peer-review` → critique a draft manuscript
4. `cite-verify` → verify all references before submission

All report-generating skills follow the `report-template` design system and output self-contained HTML files.

## Project-Local Installation

If you only want PaperSkills in one project, create a local skills link:

```bash
mkdir -p .agents/skills
ln -s /path/to/paperskills/skills .agents/skills/paperskills
```

## Updating

If `paperskills` is a git checkout, pull the latest changes in that repository. The symlink continues to point at the updated `skills/` directory.

## Troubleshooting

### Skills not showing up

1. Verify the symlink: `ls -la ~/.agents/skills/paperskills`
2. Check skills exist: `ls /path/to/paperskills/skills`
3. Restart Codex, since skills are discovered at startup

### Local project install not working

1. Verify `.agents/skills/paperskills` points to the repository `skills/` directory
2. Start Codex from that project directory
