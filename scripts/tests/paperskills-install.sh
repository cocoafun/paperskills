#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
INSTALLER="$REPO_ROOT/scripts/paperskills-install.sh"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/paperskills-installer-test.XXXXXX")"

cleanup() {
  if [[ "${KEEP_TEST_TMP:-0}" == "1" ]]; then
    echo "Preserved test directory: $TMP_DIR" >&2
    return
  fi
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_file() {
  [[ -f "$1" ]] || fail "Expected file: $1"
}

assert_not_exists() {
  [[ ! -e "$1" ]] || fail "Expected path not to exist: $1"
}

assert_contains() {
  grep -F -- "$2" "$1" >/dev/null || fail "Expected '$2' in $1"
}

create_commit() {
  local repo="$1"
  local message="$2"
  git -C "$repo" add .
  git -C "$repo" -c user.name=PaperSkills -c user.email=test@paperskills.local commit -q -m "$message"
}

SINGLE_REPO="$TMP_DIR/single-repo"
mkdir -p "$SINGLE_REPO"
git -C "$SINGLE_REPO" init -q
cat > "$SINGLE_REPO/SKILL.md" <<'EOF'
---
name: pinned-skill
description: pinned fixture v1
---
EOF
mkdir -p "$SINGLE_REPO/.hidden"
echo "included" > "$SINGLE_REPO/.hidden/asset.txt"
create_commit "$SINGLE_REPO" "fixture v1"
PINNED_REF="$(git -C "$SINGLE_REPO" rev-parse HEAD)"
sed -i.bak 's/fixture v1/fixture v2/' "$SINGLE_REPO/SKILL.md"
rm "$SINGLE_REPO/SKILL.md.bak"
create_commit "$SINGLE_REPO" "fixture v2"

COLLECTION_REPO="$TMP_DIR/collection-repo"
mkdir -p "$COLLECTION_REPO/skills/alpha-skill" "$COLLECTION_REPO/skills/beta-skill"
git -C "$COLLECTION_REPO" init -q
cat > "$COLLECTION_REPO/skills/alpha-skill/SKILL.md" <<'EOF'
---
name: alpha-skill
description: collection fixture alpha
---
EOF
cat > "$COLLECTION_REPO/skills/beta-skill/SKILL.md" <<'EOF'
---
name: beta-skill
description: collection fixture beta
---
EOF
create_commit "$COLLECTION_REPO" "collection fixture"

REGISTRY="$TMP_DIR/registry.json"
cat > "$REGISTRY" <<EOF
{
  "skills": [
    {
      "id": "pinned-skill",
      "install": {
        "method": "git-clone",
        "url": "$SINGLE_REPO",
        "ref": "$PINNED_REF"
      }
    },
    {
      "id": "collection-fixture",
      "install": {
        "method": "git-clone",
        "url": "$COLLECTION_REPO"
      }
    },
    {
      "id": "sparse-alpha",
      "install": {
        "method": "sparse-checkout",
        "url": "$COLLECTION_REPO",
        "sparse_path": "skills/alpha-skill"
      }
    }
  ],
  "packs": [
    {
      "id": "fixture-pack",
      "skillIds": ["pinned-skill", "collection-fixture", "sparse-alpha", "pinned-skill"]
    }
  ]
}
EOF

echo "Test: strict missing-value validation"
if bash "$INSTALLER" --tool > "$TMP_DIR/missing-value.out" 2>&1; then
  fail "Missing --tool value unexpectedly succeeded"
fi
assert_contains "$TMP_DIR/missing-value.out" "--tool requires a value"

echo "Test: default project scope and commit ref checkout"
PROJECT_DIR="$TMP_DIR/project"
mkdir -p "$PROJECT_DIR"
(
  cd "$PROJECT_DIR"
  bash "$INSTALLER" \
    --tool codex \
    --skills pinned-skill \
    --registry "$REGISTRY"
)
PROJECT_SKILL="$PROJECT_DIR/.codex/skills/pinned-skill"
assert_file "$PROJECT_SKILL/SKILL.md"
assert_contains "$PROJECT_SKILL/SKILL.md" "fixture v1"
assert_file "$PROJECT_SKILL/.hidden/asset.txt"
assert_not_exists "$PROJECT_SKILL/.git"

echo "Test: Cursor project and global skill directories"
CURSOR_PROJECT="$TMP_DIR/cursor-project"
CURSOR_HOME="$TMP_DIR/cursor-home"
mkdir -p "$CURSOR_PROJECT" "$CURSOR_HOME"
(
  cd "$CURSOR_PROJECT"
  bash "$INSTALLER" \
    --tool cursor \
    --skills pinned-skill \
    --registry "$REGISTRY"
)
assert_file "$CURSOR_PROJECT/.cursor/skills/pinned-skill/SKILL.md"
assert_not_exists "$CURSOR_PROJECT/.cursor/rules"
HOME="$CURSOR_HOME" bash "$INSTALLER" \
  --tool cursor \
  --scope global \
  --skills pinned-skill \
  --registry "$REGISTRY"
assert_file "$CURSOR_HOME/.cursor/skills/pinned-skill/SKILL.md"
assert_not_exists "$CURSOR_HOME/.cursor/rules"
assert_contains "$REPO_ROOT/scripts/paperskills-install.ps1" '.cursor\skills'
if grep -F -- '.cursor\rules' "$REPO_ROOT/scripts/paperskills-install.ps1" >/dev/null; then
  fail "PowerShell installer still targets .cursor\\rules"
fi

echo "Test: custom path, pack expansion, sparse checkout, and collection expansion"
CUSTOM_PATH="$TMP_DIR/custom-skills"
bash "$INSTALLER" \
  --tool claude \
  --scope global \
  --path "$CUSTOM_PATH" \
  --skills fixture-pack \
  --registry "$REGISTRY"
assert_file "$CUSTOM_PATH/pinned-skill/SKILL.md"
assert_file "$CUSTOM_PATH/alpha-skill/SKILL.md"
assert_file "$CUSTOM_PATH/beta-skill/SKILL.md"
assert_file "$CUSTOM_PATH/sparse-alpha/SKILL.md"
assert_not_exists "$CUSTOM_PATH/pinned-skill/.git"

echo "Test: existing installation skip and force replacement"
echo "local change" >> "$CUSTOM_PATH/pinned-skill/SKILL.md"
bash "$INSTALLER" --path "$CUSTOM_PATH" --skills pinned-skill --registry "$REGISTRY" > "$TMP_DIR/skip.out"
assert_contains "$CUSTOM_PATH/pinned-skill/SKILL.md" "local change"
assert_contains "$TMP_DIR/skip.out" "Skipped:   1"
bash "$INSTALLER" --path "$CUSTOM_PATH" --skills pinned-skill --registry "$REGISTRY" --force > "$TMP_DIR/force.out"
if grep -F "local change" "$CUSTOM_PATH/pinned-skill/SKILL.md" >/dev/null; then
  fail "--force did not replace the existing skill"
fi
assert_contains "$CUSTOM_PATH/pinned-skill/SKILL.md" "fixture v1"

echo "Test: python fallback"
BIN_DIR="$TMP_DIR/bin"
mkdir -p "$BIN_DIR"
REAL_PYTHON="$(command -v python3 || command -v python)"
cat > "$BIN_DIR/python3" <<'EOF'
#!/usr/bin/env bash
exit 127
EOF
cat > "$BIN_DIR/python" <<EOF
#!/usr/bin/env bash
exec "$REAL_PYTHON" "\$@"
EOF
chmod +x "$BIN_DIR/python3"
chmod +x "$BIN_DIR/python"
PATH="$BIN_DIR:$PATH" bash "$INSTALLER" \
  --path "$TMP_DIR/python-fallback-skills" \
  --skills sparse-alpha \
  --registry "$REGISTRY" > "$TMP_DIR/python-fallback.out"
assert_file "$TMP_DIR/python-fallback-skills/sparse-alpha/SKILL.md"

echo "Test: Git mirror fallback after origin failure"
MIRROR_BIN="$TMP_DIR/mirror-bin"
MIRROR_STATE="$TMP_DIR/mirror-attempts"
MIRROR_LOG="$TMP_DIR/mirror-urls.log"
MIRROR_REGISTRY="$TMP_DIR/mirror-registry.json"
REAL_GIT="$(command -v git)"
mkdir -p "$MIRROR_BIN"
cat > "$MIRROR_BIN/git" <<EOF
#!/usr/bin/env bash
set -euo pipefail
args=("\$@")
is_clone=0
for arg in "\${args[@]}"; do
  [[ "\$arg" != "clone" ]] || is_clone=1
done
if [[ "\$is_clone" == "1" ]]; then
  count=0
  [[ ! -f "$MIRROR_STATE" ]] || count="\$(cat "$MIRROR_STATE")"
  count=\$((count + 1))
  printf '%s' "\$count" > "$MIRROR_STATE"
  for i in "\${!args[@]}"; do
    case "\${args[\$i]}" in
      https://*)
        printf '%s\n' "\${args[\$i]}" >> "$MIRROR_LOG"
        if (( count <= 2 )); then
          exit 1
        fi
        [[ "\${args[\$i]}" == "https://mirror.example/https://github.com/example/pinned-skill.git" ]] || exit 91
        args[\$i]="$SINGLE_REPO"
        ;;
    esac
  done
fi
exec "$REAL_GIT" "\${args[@]}"
EOF
chmod +x "$MIRROR_BIN/git"
cat > "$MIRROR_REGISTRY" <<'EOF'
{
  "skills": [
    {
      "id": "mirror-skill",
      "install": {
        "method": "git-clone",
        "url": "https://github.com/example/pinned-skill.git"
      }
    }
  ],
  "packs": []
}
EOF
PATH="$MIRROR_BIN:$PATH" \
PAPERSKILLS_GIT_CLONE_ATTEMPTS=3 \
PAPERSKILLS_GIT_MIRRORS="https://mirror.example" \
bash "$INSTALLER" \
  --path "$TMP_DIR/mirror-skills" \
  --skills mirror-skill \
  --registry "$MIRROR_REGISTRY" > "$TMP_DIR/mirror.out"
assert_file "$TMP_DIR/mirror-skills/mirror-skill/SKILL.md"
assert_contains "$MIRROR_LOG" "https://github.com/example/pinned-skill.git"
assert_contains "$MIRROR_LOG" "https://mirror.example/https://github.com/example/pinned-skill.git"
assert_contains "$TMP_DIR/mirror.out" "via mirror, Git default (attempt 3/3)"

echo "All PaperSkills installer tests passed."
