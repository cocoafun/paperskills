#!/usr/bin/env bash

set -euo pipefail

SKILL_NAME="${1:-}"
PROMPT_FILE="${2:-}"
TIMEOUT_SECONDS="${3:-300}"

if [ -z "$SKILL_NAME" ] || [ -z "$PROMPT_FILE" ]; then
    echo "Usage: $0 <skill-name> <prompt-file> [timeout-seconds]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
OUTPUT_DIR="${PAPERSKILLS_TEST_OUTPUT_DIR:-$ROOT_DIR/tests/artifacts}/skill-triggering/${TIMESTAMP}/${SKILL_NAME}"
PROJECT_DIR="$OUTPUT_DIR/project"
LOG_FILE="$OUTPUT_DIR/codex-output.jsonl"

if command -v timeout >/dev/null 2>&1; then
  TIMEOUT_BIN="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
  TIMEOUT_BIN="gtimeout"
else
  TIMEOUT_BIN=""
fi

mkdir -p "$PROJECT_DIR/.agents/skills" "$OUTPUT_DIR"
ln -s "$ROOT_DIR/skills" "$PROJECT_DIR/.agents/skills/paperskills"

python3 "$ROOT_DIR/tests/test_support/render_agents_md.py" \
  --skills-root "$PROJECT_DIR/.agents/skills/paperskills" \
  --output "$PROJECT_DIR/AGENTS.md"

cp "$PROMPT_FILE" "$OUTPUT_DIR/prompt.txt"
PROMPT="$(cat "$PROMPT_FILE")"

echo "=== PaperSkills Skill Triggering Test ==="
echo "Skill: $SKILL_NAME"
echo "Prompt file: $PROMPT_FILE"
echo "Project dir: $PROJECT_DIR"
echo "Output dir: $OUTPUT_DIR"
echo ""

if [ -n "$TIMEOUT_BIN" ]; then
  "$TIMEOUT_BIN" "$TIMEOUT_SECONDS" codex exec \
    --json \
    --skip-git-repo-check \
    --color never \
    -C "$PROJECT_DIR" \
    "$PROMPT" \
    > "$LOG_FILE" 2>&1 || true
else
  codex exec \
    --json \
    --skip-git-repo-check \
    --color never \
    -C "$PROJECT_DIR" \
    "$PROMPT" \
    > "$LOG_FILE" 2>&1 || true
fi

echo "=== Results ==="
python3 "$ROOT_DIR/tests/test_support/analyze_codex_skill_log.py" \
  --log "$LOG_FILE" \
  --expected-skills "$SKILL_NAME"

echo ""
echo "Full log: $LOG_FILE"
