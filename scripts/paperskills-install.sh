#!/usr/bin/env bash
set -euo pipefail

TOOL="codex"
SKILLS=""
SCOPE="project"
INSTALL_PATH=""
REGISTRY="${PAPERSKILLS_REGISTRY_URL:-https://paperskills.com/api/registry}"
FORCE="0"

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
  BLUE=$'\033[0;34m'
  CYAN=$'\033[0;36m'
  GREEN=$'\033[0;32m'
  YELLOW=$'\033[1;33m'
  RED=$'\033[0;31m'
  BOLD=$'\033[1m'
  RESET=$'\033[0m'
else
  BLUE=""
  CYAN=""
  GREEN=""
  YELLOW=""
  RED=""
  BOLD=""
  RESET=""
fi

usage() {
  cat <<'USAGE'
PaperSkills installer

Usage:
  paperskills-install.sh --skills <id[,id...]> [options]

Options:
  --tool <tool>          Target tool: claude | codex | cursor | opencode
                         Default: codex
  --skills <ids>         Comma-separated skill IDs or pack IDs (required)
  --scope <scope>        Install scope: global | project
                         Default: project
  --path <directory>     Custom install directory; overrides --scope
  --registry <source>    Registry JSON URL or local path
                         Default: https://paperskills.com/api/registry
  --force                Replace existing installed skill directories
  -h, --help             Show this help

Default paths:
  global:  ~/.codex/skills, ~/.claude/skills, ~/.opencode/skills,
           or ~/.cursor/skills
  project: ./.codex/skills, ./.claude/skills, ./.opencode/skills,
           or ./.cursor/skills

Environment:
  PAPERSKILLS_REGISTRY_URL        Override the default registry URL
  PAPERSKILLS_GIT_CLONE_ATTEMPTS  Git clone attempts (default: 3)
  NO_COLOR                        Disable colored output
USAGE
}

error() {
  printf '%sError:%s %s\n' "$RED" "$RESET" "$*" >&2
}

die() {
  error "$1"
  exit "${2:-1}"
}

require_value() {
  local option="$1"
  local remaining="$2"
  local value="${3:-}"

  if (( remaining < 2 )) || [[ -z "$value" || "$value" == -* ]]; then
    die "$option requires a value." 2
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      require_value "$1" "$#" "${2:-}"
      TOOL="$2"
      shift 2
      ;;
    --skills)
      require_value "$1" "$#" "${2:-}"
      SKILLS="$2"
      shift 2
      ;;
    --scope)
      require_value "$1" "$#" "${2:-}"
      SCOPE="$2"
      shift 2
      ;;
    --path)
      require_value "$1" "$#" "${2:-}"
      INSTALL_PATH="$2"
      shift 2
      ;;
    --registry)
      require_value "$1" "$#" "${2:-}"
      REGISTRY="$2"
      shift 2
      ;;
    --force)
      FORCE="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      error "Unknown option: $1"
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "$SKILLS" ]] || die "--skills is required. Run with --help for usage." 2

case "$TOOL" in
  claude) TOOL_PATH=".claude/skills" ;;
  codex) TOOL_PATH=".codex/skills" ;;
  cursor) TOOL_PATH=".cursor/skills" ;;
  opencode) TOOL_PATH=".opencode/skills" ;;
  *) die "Unsupported tool '$TOOL'. Expected claude, codex, cursor, or opencode." 2 ;;
esac

case "$SCOPE" in
  global|project) ;;
  *) die "Unsupported scope '$SCOPE'. Expected global or project." 2 ;;
esac

if [[ -n "$INSTALL_PATH" ]]; then
  TARGET_ROOT="$INSTALL_PATH"
elif [[ "$SCOPE" == "global" ]]; then
  [[ -n "${HOME:-}" ]] || die "HOME is not set; use --path to choose an install directory."
  TARGET_ROOT="$HOME/$TOOL_PATH"
else
  TARGET_ROOT="$PWD/$TOOL_PATH"
fi

command -v git >/dev/null 2>&1 || die "Required command 'git' was not found."

PYTHON_CMD=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys' >/dev/null 2>&1; then
    PYTHON_CMD="$candidate"
    break
  fi
done
[[ -n "$PYTHON_CMD" ]] || die "Required command 'python3' or 'python' was not found."

if [[ "$REGISTRY" == http://* || "$REGISTRY" == https://* ]]; then
  command -v curl >/dev/null 2>&1 || die "Required command 'curl' was not found."
fi

TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/paperskills-install.XXXXXX")"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

printf '\n%s%sPaperSkills installer%s\n' "$BLUE" "$BOLD" "$RESET"
printf '%sTool:%s     %s\n' "$CYAN" "$RESET" "$TOOL"
printf '%sSkills:%s   %s\n' "$CYAN" "$RESET" "$SKILLS"
printf '%sScope:%s    %s\n' "$CYAN" "$RESET" "$SCOPE"
printf '%sPath:%s     %s\n' "$CYAN" "$RESET" "$TARGET_ROOT"
printf '%sRegistry:%s %s\n\n' "$CYAN" "$RESET" "$REGISTRY"

REGISTRY_FILE="$TMP_DIR/registry.json"
printf '%sLoading registry...%s\n' "$BLUE" "$RESET"
case "$REGISTRY" in
  http://*|https://*)
    if ! curl -fsSL "$REGISTRY" -o "$REGISTRY_FILE"; then
      die "Failed to download registry from $REGISTRY."
    fi
    ;;
  *)
    [[ -f "$REGISTRY" ]] || die "Registry file not found: $REGISTRY"
    cp "$REGISTRY" "$REGISTRY_FILE"
    ;;
esac
printf '%sRegistry loaded.%s\n\n' "$GREEN" "$RESET"

PLAN_FILE="$TMP_DIR/install-plan.json"
if ! SKILLS="$SKILLS" "$PYTHON_CMD" - "$REGISTRY_FILE" "$PLAN_FILE" <<'PY'
import json
import os
import re
import sys

registry_path, plan_path = sys.argv[1], sys.argv[2]
requested = [item.strip() for item in os.environ["SKILLS"].split(",") if item.strip()]

if not requested:
    raise SystemExit("No skill or pack IDs were provided")

try:
    with open(registry_path, encoding="utf-8") as handle:
        registry = json.load(handle)
except (OSError, json.JSONDecodeError) as exc:
    raise SystemExit(f"Invalid registry JSON: {exc}")

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
unsafe = []

for skill_id in expanded:
    if skill_id in seen:
        continue
    seen.add(skill_id)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", skill_id):
        unsafe.append(skill_id)
        continue
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

if unsafe:
    raise SystemExit("Unsafe skill id(s): " + ", ".join(unsafe))
if missing:
    raise SystemExit("Unknown skill or pack id(s): " + ", ".join(missing))

with open(plan_path, "w", encoding="utf-8") as handle:
    json.dump(plan, handle, ensure_ascii=False)
PY
then
  die "Could not create the installation plan."
fi

mkdir -p "$TARGET_ROOT"

SUCCESS=()
SKIPPED=()
FAILED=()

install_skill_dir() {
  local install_id="$1"
  local source_dir="$2"
  local destination="$TARGET_ROOT/$install_id"
  local staging="$TARGET_ROOT/.paperskills-${install_id}.tmp.$$"
  local backup="$TARGET_ROOT/.paperskills-${install_id}.backup.$$"

  if [[ -e "$destination" && "$FORCE" != "1" ]]; then
    printf '%s  SKIP%s %s (already exists; use --force to replace)\n' "$YELLOW" "$RESET" "$install_id"
    SKIPPED+=("$install_id")
    return 0
  fi

  rm -rf "$staging" "$backup"
  if ! cp -R "$source_dir" "$staging"; then
    rm -rf "$staging"
    error "Could not stage $install_id for installation."
    FAILED+=("$install_id")
    return 1
  fi

  find "$staging" -type d -name .git -prune -exec rm -rf {} +

  if [[ -e "$destination" ]]; then
    if ! mv "$destination" "$backup"; then
      rm -rf "$staging"
      error "Could not prepare the existing installation of $install_id for replacement."
      FAILED+=("$install_id")
      return 1
    fi
  fi

  if ! mv "$staging" "$destination"; then
    rm -rf "$staging"
    if [[ -e "$backup" ]]; then
      mv "$backup" "$destination" || true
    fi
    error "Could not move $install_id into $destination."
    FAILED+=("$install_id")
    return 1
  fi

  rm -rf "$backup"
  printf '%s  OK%s   %s\n' "$GREEN" "$RESET" "$install_id"
  SUCCESS+=("$install_id")
  return 0
}

checkout_ref() {
  local repo_dir="$1"
  local ref="$2"

  [[ -n "$ref" ]] || return 0

  if git -C "$repo_dir" checkout --detach "$ref" >/dev/null 2>&1; then
    return 0
  fi

  git -c http.version=HTTP/1.1 -C "$repo_dir" fetch --depth 1 origin "$ref" >/dev/null 2>&1 &&
    git -C "$repo_dir" checkout --detach FETCH_HEAD >/dev/null 2>&1
}

clone_with_retry() {
  local skill_id="$1"
  local workdir="$2"
  local sparse_path="$3"
  local ref="$4"
  shift 4

  local attempts="${PAPERSKILLS_GIT_CLONE_ATTEMPTS:-3}"
  local delays=(2 5 10)
  local attempt delay_index delay

  case "$attempts" in
    ''|*[!0-9]*) attempts=3 ;;
  esac
  (( attempts >= 1 )) || attempts=1

  for ((attempt = 1; attempt <= attempts; attempt++)); do
    rm -rf "$workdir"
    if git -c http.version=HTTP/1.1 clone "$@" "$workdir" >/dev/null 2>&1 &&
      checkout_ref "$workdir" "$ref" &&
      { [[ -z "$sparse_path" ]] || git -C "$workdir" sparse-checkout set "$sparse_path" >/dev/null 2>&1; }; then
      return 0
    fi

    if (( attempt >= attempts )); then
      error "Git checkout failed for $skill_id after $attempts attempt(s)."
      return 1
    fi

    delay_index=$((attempt - 1))
    delay="${delays[$delay_index]:-${delays[2]}}"
    printf '%s  Git checkout failed for %s (attempt %s/%s). Retrying in %ss...%s\n' \
      "$YELLOW" "$skill_id" "$attempt" "$attempts" "$delay" "$RESET" >&2
    sleep "$delay"
  done
}

while IFS=$'\037' read -r skill_id method url ref sparse_path; do
  printf '%sInstalling %s...%s\n' "$CYAN" "$skill_id" "$RESET"

  if [[ "$method" != "sparse-checkout" && "$method" != "git-clone" ]]; then
    error "Unsupported install method for $skill_id: ${method:-<empty>}"
    FAILED+=("$skill_id")
    continue
  fi

  if [[ -z "$url" ]]; then
    error "Missing install URL for $skill_id."
    FAILED+=("$skill_id")
    continue
  fi

  workdir="$TMP_DIR/checkout-$skill_id"

  if [[ "$method" == "git-clone" ]]; then
    if ! clone_with_retry "$skill_id" "$workdir" "" "$ref" --depth 1 "$url"; then
      FAILED+=("$skill_id")
      continue
    fi
    source_dir="$workdir"
  else
    if [[ -z "$sparse_path" ]]; then
      error "Missing sparsePath for $skill_id."
      FAILED+=("$skill_id")
      continue
    fi
    if ! clone_with_retry "$skill_id" "$workdir" "$sparse_path" "$ref" --filter=blob:none --sparse --depth 1 "$url"; then
      FAILED+=("$skill_id")
      continue
    fi
    source_dir="$workdir/$sparse_path"
  fi

  if [[ ! -d "$source_dir" ]]; then
    error "Install source not found for $skill_id: $source_dir"
    FAILED+=("$skill_id")
    continue
  fi

  if [[ -f "$source_dir/SKILL.md" ]]; then
    install_skill_dir "$skill_id" "$source_dir" || true
    continue
  fi

  collection_root="$source_dir"
  [[ ! -d "$source_dir/skills" ]] || collection_root="$source_dir/skills"

  skill_list_file="$TMP_DIR/${skill_id}-skill-files.txt"
  find "$collection_root" -name SKILL.md -type f | sort > "$skill_list_file"
  skill_count="$(wc -l < "$skill_list_file" | tr -d ' ')"

  if [[ "$skill_count" == "0" ]]; then
    error "SKILL.md not found for $skill_id at $source_dir"
    FAILED+=("$skill_id")
    continue
  fi

  printf '%sInstalling collection %s (%s skills)%s\n' "$BLUE" "$skill_id" "$skill_count" "$RESET"
  while IFS= read -r skill_file; do
    child_source="$(dirname "$skill_file")"
    child_id="$(basename "$child_source")"
    if [[ ! "$child_id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]; then
      error "Unsafe child skill id '$child_id' in collection $skill_id."
      FAILED+=("$skill_id/$child_id")
      continue
    fi
    install_skill_dir "$child_id" "$child_source" || true
  done < "$skill_list_file"
done < <("$PYTHON_CMD" - "$PLAN_FILE" <<'PY'
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
)

printf '\n%s%sInstallation summary%s\n' "$BLUE" "$BOLD" "$RESET"
printf '  Installed: %s\n' "${#SUCCESS[@]}"
printf '  Skipped:   %s\n' "${#SKIPPED[@]}"
printf '  Failed:    %s\n' "${#FAILED[@]}"
printf '  Location:  %s\n' "$TARGET_ROOT"

if [[ ${#FAILED[@]} -gt 0 ]]; then
  printf '\n%sFailed items:%s\n' "$RED" "$RESET" >&2
  printf '  - %s\n' "${FAILED[@]}" >&2
  exit 1
fi

printf '\n%sDone.%s\n' "$GREEN" "$RESET"
