# PaperSkills for Codex

Guide for using PaperSkills with OpenAI Codex via native skill discovery.

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

Codex scans `~/.agents/skills/` at startup, reads `SKILL.md` frontmatter, and loads matching skills on demand. PaperSkills becomes visible through a single symlink:

```text
~/.agents/skills/paperskills/ -> /path/to/paperskills/skills/
```

The `using-paperskills` skill acts as the entry point. It detects the current research stage and routes the task to the right downstream skill before drafting content.

## Usage

Once installed, ask Codex for a research task in natural language, for example:

```text
我想研究大模型如何支持文献综述写作，请使用 paperskills 从阶段判断开始，最终帮我形成一版 proposal。
```

Or name the entry skill explicitly:

```text
Use using-paperskills and continue with the appropriate PaperSkills workflow for my paper-writing task.
```

Typical downstream routing includes:

- `research-scoping` for broad or fuzzy topics
- `literature-review` for related work and gap analysis
- `research-design` for questions, methods, and study plans
- `paper-drafting` for outlines and manuscript drafting
- `peer-review` for reviewer-style critique
- `revision-planning` for revision roadmaps

## Project-Local Installation

If you only want PaperSkills in one project, create a local `AGENTS.md` and local skills link:

```bash
mkdir -p .agents/skills
ln -s /path/to/paperskills/skills .agents/skills/paperskills
python3 /path/to/paperskills/tests/test_support/render_agents_md.py \
  --skills-root ./.agents/skills/paperskills \
  --output ./AGENTS.md
```

This mirrors the repository's own smoke-test setup and makes the PaperSkills library discoverable within that project.

## Updating

If `paperskills` is a git checkout, pull the latest changes in that repository. The symlink continues to point at the updated `skills/` directory.

## Troubleshooting

### Skills not showing up

1. Verify the symlink: `ls -la ~/.agents/skills/paperskills`
2. Check skills exist: `ls /path/to/paperskills/skills`
3. Restart Codex, since skills are discovered at startup

### Local project install not working

1. Verify `AGENTS.md` exists in the project root
2. Verify `.agents/skills/paperskills` points to the repository `skills/` directory
3. Start Codex from that project directory
