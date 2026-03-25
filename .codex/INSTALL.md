# PaperSkills for Codex

Academic research skills library for OpenAI Codex. Each skill is a standalone module that handles one research task using public APIs (Semantic Scholar, OpenAlex, CrossRef, Unpaywall, etc.).

## Quick Install

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.codex/INSTALL.md
```

## Manual Installation

### Prerequisites

- OpenAI Codex CLI

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/cocoafun/paperskills.git /path/to/paperskills
   ```

2. Create the skills directory if needed:
   ```bash
   mkdir -p ~/.agents/skills
   ```

3. Link the top-level router:
   ```bash
   ln -s /path/to/paperskills ~/.agents/skills/paperskills
   ```

4. Link each sub-skill for direct invocation:
   ```bash
   ln -s /path/to/paperskills/abstract ~/.agents/skills/abstract
   ln -s /path/to/paperskills/cite-verify ~/.agents/skills/cite-verify
   ln -s /path/to/paperskills/citation-network ~/.agents/skills/citation-network
   ln -s /path/to/paperskills/journal-match ~/.agents/skills/journal-match
   ln -s /path/to/paperskills/lit-search ~/.agents/skills/lit-search
   ln -s /path/to/paperskills/peer-review ~/.agents/skills/peer-review
   ln -s /path/to/paperskills/research-gap ~/.agents/skills/research-gap
   ln -s /path/to/paperskills/topic-framing ~/.agents/skills/topic-framing
   ```

5. Restart Codex.

## How It Works

Codex scans `~/.agents/skills/` at startup and loads matching skills on demand. PaperSkills provides:

- `/paperskills` — smart router that dispatches to the right sub-skill
- `/cite-verify`, `/peer-review`, `/lit-search`, etc. — each sub-skill is independently invocable

```text
~/.agents/skills/
├── paperskills/    -> /path/to/paperskills/       (router)
├── abstract/       -> /path/to/paperskills/abstract/
├── cite-verify/    -> /path/to/paperskills/cite-verify/
├── citation-network/ -> /path/to/paperskills/citation-network/
├── journal-match/  -> /path/to/paperskills/journal-match/
├── lit-search/     -> /path/to/paperskills/lit-search/
├── peer-review/    -> /path/to/paperskills/peer-review/
├── research-gap/   -> /path/to/paperskills/research-gap/
└── topic-framing/  -> /path/to/paperskills/topic-framing/
```

## Available Skills

| Skill | Description | Token Budget |
|-------|-------------|--------------|
| `topic-framing` | Converge from fuzzy idea to concrete paper title | 15–25K |
| `lit-search` | Search academic literature across Semantic Scholar, OpenAlex, PubMed, arXiv | 15–25K |
| `abstract` | Generate abstracts in multiple formats (IMRaD, thematic, extended, short) | 10–20K |
| `cite-verify` | Verify all citations in a manuscript against CrossRef / Semantic Scholar / OpenAlex | 25–65K |
| `citation-network` | Build and visualize citation networks from seed papers with HTML report | 35–55K |
| `research-gap` | Analyze research gaps (temporal, methodological, thematic, application) | 55–85K |
| `peer-review` | Academic peer review with 8-criteria scoring and radar chart report | 35–60K |
| `journal-match` | Recommend target journals for manuscript submission | 25–35K |

## Usage

Once installed, invoke skills directly:

```text
/cite-verify my-manuscript.md
/peer-review draft.md
/lit-search 大模型支持文献综述写作
```

Or use the router for guided dispatch:

```text
/paperskills 帮我检索关于大模型支持文献综述写作的文献
```

Skills can be composed for multi-step workflows:

1. `/topic-framing` → converge on a research question
2. `/lit-search` → find relevant papers
3. `/research-gap` → identify gaps in the field
4. `/peer-review` → critique a draft manuscript
5. `/cite-verify` → verify all references before submission

All report-generating skills follow the shared design system (`shared/report-template.md`) and output self-contained HTML files. Reports support both English and Chinese output — language is auto-detected from manuscript or can be explicitly requested.

## Project-Local Installation

If you only want PaperSkills in one project, create local skills links:

```bash
mkdir -p .agents/skills
ln -s /path/to/paperskills .agents/skills/paperskills
ln -s /path/to/paperskills/abstract .agents/skills/abstract
ln -s /path/to/paperskills/cite-verify .agents/skills/cite-verify
ln -s /path/to/paperskills/citation-network .agents/skills/citation-network
ln -s /path/to/paperskills/journal-match .agents/skills/journal-match
ln -s /path/to/paperskills/lit-search .agents/skills/lit-search
ln -s /path/to/paperskills/peer-review .agents/skills/peer-review
ln -s /path/to/paperskills/research-gap .agents/skills/research-gap
ln -s /path/to/paperskills/topic-framing .agents/skills/topic-framing
```

## Updating

If `paperskills` is a git checkout, pull the latest changes. The symlinks continue to point at the updated directories.

## Troubleshooting

### Skills not showing up

1. Verify symlinks: `ls -la ~/.agents/skills/`
2. Check SKILL.md exists: `ls /path/to/paperskills/*/SKILL.md`
3. Restart Codex, since skills are discovered at startup

### Local project install not working

1. Verify `.agents/skills/` symlinks point to the correct directories
2. Start Codex from that project directory
