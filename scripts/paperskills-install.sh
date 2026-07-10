#!/usr/bin/env bash
set -euo pipefail

TOOL="codex"
SKILLS=""
REGISTRY="https://paperskills.com/api/registry"
FORCE="0"

usage() {
  cat <<'USAGE'
PaperSkills installer

Usage:
  paperskills-install.sh --tool codex --skills lit-search,peer-review [--registry URL_OR_PATH] [--force]

Options:
  --tool       claude | codex | cursor | opencode
  --skills     Comma-separated skill ids or pack ids from the PaperSkills registry
  --registry   Registry JSON URL or local path, default https://paperskills.com/api/registry
  --force      Replace existing installed skill directories
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool) TOOL="${2:-}"; shift 2 ;;
    --skills) SKILLS="${2:-}"; shift 2 ;;
    --registry) REGISTRY="${2:-}"; shift 2 ;;
    --force) FORCE="1"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ -z "$SKILLS" ]]; then
  echo "Missing --skills" >&2
  exit 2
fi

case "$TOOL" in
  claude) TARGET_ROOT="$HOME/.claude/skills" ;;
  codex) TARGET_ROOT="$HOME/.codex/skills" ;;
  opencode) TARGET_ROOT="$HOME/.opencode/skills" ;;
  cursor) TARGET_ROOT="$HOME/.cursor/rules" ;;
  *) echo "Unsupported tool: $TOOL" >&2; exit 2 ;;
esac

for cmd in git python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

if [[ "$REGISTRY" == http://* || "$REGISTRY" == https://* ]]; then
  if ! command -v curl >/dev/null 2>&1; then
    echo "Missing required command: curl" >&2
    exit 1
  fi
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

REGISTRY_FILE="$TMP_DIR/registry.json"
case "$REGISTRY" in
  http://*|https://*) curl -fsSL "$REGISTRY" -o "$REGISTRY_FILE" ;;
  *)
    if [[ ! -f "$REGISTRY" ]]; then
      echo "Registry file not found: $REGISTRY" >&2
      exit 1
    fi
    cp "$REGISTRY" "$REGISTRY_FILE"
    ;;
esac

PLAN_FILE="$TMP_DIR/install-plan.json"
SKILLS="$SKILLS" python3 - "$REGISTRY_FILE" "$PLAN_FILE" <<'PY'
import json
import os
import sys

registry_path, plan_path = sys.argv[1], sys.argv[2]
requested = [item.strip() for item in os.environ["SKILLS"].split(",") if item.strip()]

with open(registry_path, encoding="utf-8") as handle:
    registry = json.load(handle)

skills = {skill["id"]: skill for skill in registry.get("skills", [])}
packs = {pack["id"]: pack for pack in registry.get("packs", [])}
expanded = []

for item in requested:
    if item in packs:
        expanded.extend(packs[item].get("skillIds", []))
    else:
        expanded.append(item)

seen = set()
plan = []
missing = []

for skill_id in expanded:
    if skill_id in seen:
        continue
    seen.add(skill_id)
    skill = skills.get(skill_id)
    if skill is None:
        missing.append(skill_id)
        continue

    install = skill.get("install") or {}
    sparse_path = install.get("sparsePath") or install.get("sparse_path")
    plan.append({
        "id": skill_id,
        "method": install.get("method"),
        "url": install.get("url"),
        "ref": install.get("ref") or "",
        "sparsePath": sparse_path,
    })

if missing:
    raise SystemExit("Unknown skill or pack id(s): " + ", ".join(missing))

with open(plan_path, "w", encoding="utf-8") as handle:
    json.dump(plan, handle, ensure_ascii=False)
PY

echo "Installing PaperSkills into $TARGET_ROOT"
mkdir -p "$TARGET_ROOT"

install_skill_dir() {
  local install_id="$1"
  local source_dir="$2"
  local destination="$TARGET_ROOT/$install_id"

  if [[ -e "$destination" && "$FORCE" != "1" ]]; then
    echo "Skip existing $destination. Use --force to replace it."
    return
  fi

  rm -rf "$destination"
  cp -R "$source_dir" "$destination"
  echo "Installed $install_id"
}

clone_with_retry() {
  local skill_id="$1"
  local workdir="$2"
  local sparse_path="$3"
  shift 3

  local attempts="${PAPERSKILLS_GIT_CLONE_ATTEMPTS:-3}"
  local delays=(2 5 10)
  local attempt delay_index delay

  case "$attempts" in
    ''|*[!0-9]*) attempts=3 ;;
  esac
  if (( attempts < 1 )); then
    attempts=1
  fi

  for ((attempt = 1; attempt <= attempts; attempt++)); do
    rm -rf "$workdir"
    if git -c http.version=HTTP/1.1 clone "$@" "$workdir" >/dev/null; then
      if [[ -z "$sparse_path" ]] || (
        cd "$workdir"
        git sparse-checkout set "$sparse_path" >/dev/null
      ); then
        return 0
      fi
    fi

    if (( attempt >= attempts )); then
      echo "Git checkout failed for $skill_id after $attempts attempts." >&2
      return 1
    fi

    delay_index=$((attempt - 1))
    delay="${delays[$delay_index]:-${delays[2]}}"
    echo "Git checkout failed for $skill_id (attempt $attempt/$attempts). Retrying in ${delay}s..." >&2
    sleep "$delay"
  done
}

python3 - "$PLAN_FILE" <<'PY' | while IFS=$'\037' read -r skill_id method url ref sparse_path; do
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    plan = json.load(handle)

for item in plan:
    print("\x1f".join([
        item["id"],
        item.get("method") or "",
        item.get("url") or "",
        item.get("ref") or "",
        item.get("sparsePath") or "",
    ]))
PY
  if [[ "$method" != "sparse-checkout" && "$method" != "git-clone" ]]; then
    echo "Unsupported install method for $skill_id: $method" >&2
    exit 1
  fi

  if [[ -z "$url" ]]; then
    echo "Missing install URL for $skill_id" >&2
    exit 1
  fi

  workdir="$TMP_DIR/checkout-$skill_id"

  if [[ "$method" == "git-clone" ]]; then
    clone_args=(--depth 1)
    if [[ -n "$ref" ]]; then
      clone_args+=(--branch "$ref")
    fi
    clone_with_retry "$skill_id" "$workdir" "" "${clone_args[@]}" "$url"
    source_dir="$workdir"
  else
    if [[ -z "$sparse_path" ]]; then
      echo "Missing sparsePath for $skill_id" >&2
      exit 1
    fi

    clone_args=(--filter=blob:none --sparse --depth 1)
    if [[ -n "$ref" ]]; then
      clone_args+=(--branch "$ref")
    fi
    clone_with_retry "$skill_id" "$workdir" "$sparse_path" "${clone_args[@]}" "$url"
    source_dir="$workdir/$sparse_path"
  fi

  if [[ ! -d "$source_dir" ]]; then
    echo "Install source not found for $skill_id: $source_dir" >&2
    exit 1
  fi

  if [[ -f "$source_dir/SKILL.md" ]]; then
    install_skill_dir "$skill_id" "$source_dir"
    continue
  fi

  collection_root="$source_dir"
  if [[ -d "$source_dir/skills" ]]; then
    collection_root="$source_dir/skills"
  fi

  skill_list_file="$TMP_DIR/${skill_id}-skill-files.txt"
  find "$collection_root" -name SKILL.md -type f | sort > "$skill_list_file"
  skill_count="$(wc -l < "$skill_list_file" | tr -d ' ')"

  if [[ "$skill_count" == "0" ]]; then
    echo "SKILL.md not found for $skill_id at $source_dir" >&2
    exit 1
  fi

  echo "Installing collection $skill_id ($skill_count skills)"
  while IFS= read -r skill_file; do
    child_source="$(dirname "$skill_file")"
    child_id="$(basename "$child_source")"
    install_skill_dir "$child_id" "$child_source"
  done < "$skill_list_file"
done

if [[ "$TOOL" == "cursor" ]]; then
  echo "Cursor uses rules/prompt installation in this MVP. Review imported files under $TARGET_ROOT."
fi

echo "Done."
