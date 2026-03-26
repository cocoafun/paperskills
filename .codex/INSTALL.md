# Installing PaperSkills for Codex

Guide for using PaperSkills with Codex via native skill discovery.

## Quick Install

Tell Codex:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/cocoafun/paperskills/refs/heads/main/.codex/INSTALL.md
```

## Manual Installation

### Prerequisites

- Codex CLI
- Git

### Global Install

```bash
git clone https://github.com/cocoafun/paperskills.git ~/.agents/skills/paperskills
cd ~/.agents/skills/paperskills && ./setup
```

This registers the router skill at `paperskills` and links sibling skills such as `peer-review`, `research-gap`, and `shared`.

### Single-Project Install

```bash
mkdir -p .agents/skills
ln -s /path/to/paperskills .agents/skills/paperskills
cd .agents/skills/paperskills && ./setup
```

Use project-local install when you want PaperSkills available only inside one repository.

## Verify Installation

Start a new Codex session in the target project and ask for a paper workflow task, for example:

```text
Use paperskills to help me review this manuscript.
```

Codex should discover `paperskills/SKILL.md` and then route to the relevant sub-skill.

## Updating

```bash
cd ~/.agents/skills/paperskills && git pull
./setup
```

For project-local installs, run the same commands in `.agents/skills/paperskills`.

## Troubleshooting

### Skills not showing up

1. Check the install path exists: `ls ~/.agents/skills/paperskills`
2. Check linked skills exist after setup: `ls ~/.agents/skills`
3. Restart Codex, because skills are discovered at session start

### Shared assets missing

Run `./setup` again. Report-style skills depend on the linked `shared` directory.
