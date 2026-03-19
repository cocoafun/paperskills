#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/prompts"

SKILLS=(
  "using-paperskills"
  "research-scoping"
  "research-design"
  "paper-drafting"
  "revision-planning"
)

echo "=== PaperSkills Skill Triggering Tests ==="
echo ""

"$SCRIPT_DIR/run-check.sh"

PASSED=0
FAILED=0

for skill in "${SKILLS[@]}"; do
  prompt_file="$PROMPTS_DIR/${skill}.txt"
  echo "Testing: $skill"
  if "$SCRIPT_DIR/run-test.sh" "$skill" "$prompt_file" 300; then
    PASSED=$((PASSED + 1))
  else
    FAILED=$((FAILED + 1))
  fi
  echo ""
  echo "---"
  echo ""
done

echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ "$FAILED" -gt 0 ]; then
  exit 1
fi
