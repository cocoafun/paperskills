#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/prompts"

echo "=== PaperSkills Workflow Smoke Tests ==="
echo ""

"$SCRIPT_DIR/run-check.sh"

TESTS=(
  "idea-to-draft|using-paperskills,research-scoping,paper-drafting|$PROMPTS_DIR/idea-to-draft.txt"
  "full-paper-from-topic|using-paperskills,research-scoping,paper-tracker,literature-review,research-design,paper-drafting|$PROMPTS_DIR/full-paper-from-topic.txt"
  "review-to-revision|using-paperskills,revision-planning|$PROMPTS_DIR/review-to-revision.txt"
)

PASSED=0
FAILED=0

for test_case in "${TESTS[@]}"; do
  IFS='|' read -r name expected prompt_file <<< "$test_case"
  echo "Testing workflow: $name"
  if "$SCRIPT_DIR/run-test.sh" "$name" "$expected" "$prompt_file" 300; then
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
