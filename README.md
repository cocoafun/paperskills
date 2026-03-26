# PaperSkills

Academic research skills for Claude Code and Codex. Each skill handles one research task using public APIs (Semantic Scholar, OpenAlex, CrossRef, Unpaywall, etc.).

## Install

### Claude Code — global (all projects)

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.claude/skills/paperskills
cd ~/.claude/skills/paperskills && ./setup
```

### Claude Code — single project

```bash
mkdir -p .claude/skills
ln -s /path/to/paperskills .claude/skills/paperskills
cd .claude/skills/paperskills && ./setup
```

`./setup` will create sibling links such as `.claude/skills/peer-review` and `.claude/skills/shared`, so report-generating skills can read the shared report template. Re-run `./setup` after updating PaperSkills.

### Codex

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.codex/INSTALL.md
```

Or manually:

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.agents/skills/paperskills
cd ~/.agents/skills/paperskills && ./setup
```

`./setup` also links the shared assets directory required by report-generating skills.

## Available Skills

| Skill | Description | Token Budget |
|-------|-------------|--------------|
| `/topic-framing` | Converge from fuzzy idea to concrete paper title | 15–25K |
| `/lit-search` | Search literature across Semantic Scholar, OpenAlex, PubMed, arXiv | 15–25K |
| `/abstract` | Generate abstracts in multiple formats (IMRaD, thematic, extended, short) | 10–20K |
| `/cite-verify` | Verify all citations against CrossRef / Semantic Scholar / OpenAlex | 25–65K |
| `/citation-network` | Build and visualize citation networks with interactive HTML report | 35–55K |
| `/research-gap` | Analyze research gaps (temporal, methodological, thematic, application) | 55–85K |
| `/peer-review` | Academic peer review with 8-criteria scoring and radar chart | 35–60K |
| `/journal-match` | Recommend target journals for manuscript submission | 25–35K |

## Usage

Invoke skills directly:

```text
/cite-verify my-manuscript.md
/peer-review draft.md
/lit-search 大模型支持文献综述写作
```

Or use the router for guided dispatch:

```text
/paperskills 帮我检索关于大模型支持文献综述写作的文献
```

## Language Support

Report-generating skills (cite-verify, citation-network, journal-match, research-gap, peer-review) support both English and Chinese output. Language is auto-detected from manuscript content, or can be explicitly requested (e.g., "用中文生成报告").

## Workflow

Skills can be composed for multi-step workflows:

1. `/topic-framing` → converge on a research question
2. `/lit-search` → find relevant papers
3. `/research-gap` → identify gaps in the field
4. `/peer-review` → critique a draft manuscript
5. `/cite-verify` → verify all references before submission

## License

MIT
