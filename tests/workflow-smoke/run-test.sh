#!/usr/bin/env bash

set -euo pipefail

TEST_NAME="${1:-}"
EXPECTED_SKILLS="${2:-}"
PROMPT_FILE="${3:-}"
TIMEOUT_SECONDS="${4:-300}"

if [ -z "$TEST_NAME" ] || [ -z "$EXPECTED_SKILLS" ] || [ -z "$PROMPT_FILE" ]; then
    echo "Usage: $0 <test-name> <expected-skills> <prompt-file> [timeout-seconds]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
OUTPUT_DIR="${PAPERSKILLS_TEST_OUTPUT_DIR:-$ROOT_DIR/tests/artifacts}/workflow-smoke/${TIMESTAMP}/${TEST_NAME}"
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

echo "=== PaperSkills Workflow Smoke Test ==="
echo "Test: $TEST_NAME"
echo "Expected skills: $EXPECTED_SKILLS"
echo "Prompt file: $PROMPT_FILE"
echo "Project dir: $PROJECT_DIR"
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
  --expected-skills "$EXPECTED_SKILLS"

echo ""
echo "Full log: $LOG_FILE"
