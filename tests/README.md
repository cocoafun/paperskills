# PaperSkills Tests

This repository currently includes two lightweight test groups:

- `skill-triggering`: validates that key skills have valid frontmatter, support files, and prompt fixtures, and includes a live Codex CLI runner
- `workflow-smoke`: validates that cross-skill workflow examples and core artifacts exist, and includes a live Codex CLI runner for multi-stage prompts

The static checks run through `tests/test_support/validate_paperskills.py`.

The live Codex tests:

- create a temporary project under `tests/artifacts/`
- symlink the repository `skills/` into `.agents/skills/paperskills`
- generate an `AGENTS.md` that enumerates the local skills
- run `codex exec --json`
- analyze the resulting JSONL log for evidence that the expected skill files were actually used
