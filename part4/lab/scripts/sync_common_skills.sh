#!/usr/bin/env bash
# Synchronize common skill folders into tool-specific skill locations.
#
# Source of truth : common_skills/<skill>/
# Targets         : .agents/skills/<skill>, .claude/skills/<skill>
#
# Targets are regenerated per-OS and are gitignored (only their README.md is
# committed). POSIX uses relative symlinks; Windows uses directory junctions
# (mklink /J), which need no administrator rights or Developer Mode.

set -euo pipefail

MODE="sync"
case "${1:-}" in
  "--check") MODE="check" ;;
  "-h"|"--help")
    cat <<'USAGE'
Usage:
  bash scripts/sync_common_skills.sh          # create/update managed links
  bash scripts/sync_common_skills.sh --check  # verify links without changing files
USAGE
    exit 0
    ;;
  "") ;;
  *) echo "[skills-sync] unknown option: $1" >&2; exit 2 ;;
esac

cd "$(dirname "$0")/.."

SOURCE_DIR="common_skills"
TARGET_DIRS=(".agents/skills" ".claude/skills")
STATUS=0

case "${OSTYPE:-}" in
  msys*|cygwin*|win32*) IS_WINDOWS=1 ;;
  *) IS_WINDOWS=0 ;;
esac

# Absolute base path for Windows. PowerShell (not cmd) is used to create
# junctions because cmd's mklink cannot handle non-ASCII directory paths.
WIN_BASE=""
if [[ "$IS_WINDOWS" -eq 1 ]]; then
  WIN_BASE="$(pwd -W)"
fi

fail() { echo "[skills-sync] $*" >&2; STATUS=1; }

# Does a link target string resolve into common_skills/<skill_name>?
# Matches both POSIX "../../common_skills/x" and Windows "/c/.../common_skills/x".
points_to_source() {
  case "$1" in
    */common_skills/"$2") return 0 ;;
    *) return 1 ;;
  esac
}

# A "dead text-file link": a git symlink checked out as plain text on a machine
# with core.symlinks=false. It is a tiny regular file whose body is the target.
is_dead_text_link() {
  local path="$1" name="$2"
  [[ -f "$path" && ! -L "$path" ]] || return 1
  [[ "$(wc -c <"$path")" -lt 256 ]] || return 1
  grep -q "common_skills/$name" "$path" 2>/dev/null
}

remove_link() {
  local link_path="$1"
  if [[ "$IS_WINDOWS" -eq 1 && -d "$link_path" && -L "$link_path" ]]; then
    # .Delete() removes only the junction (reparse point), never its target.
    powershell -NoProfile -Command \
      "(Get-Item -LiteralPath '$WIN_BASE/$link_path' -Force).Delete()" >/dev/null 2>&1 || true
  else
    rm -f "$link_path"
  fi
}

create_link() {
  local link_path="$1" name="$2"
  if [[ "$IS_WINDOWS" -eq 1 ]]; then
    powershell -NoProfile -Command \
      "New-Item -ItemType Junction -Path '$WIN_BASE/$link_path' -Target '$WIN_BASE/$SOURCE_DIR/$name' -Force" \
      >/dev/null
  else
    ln -s "../../$SOURCE_DIR/$name" "$link_path"
  fi
}

ensure_target_dir() {
  local target_dir="$1"
  [[ -d "$target_dir" ]] && return 0
  if [[ "$MODE" == "check" ]]; then
    fail "missing target directory: $target_dir"
    return 1
  fi
  mkdir -p "$target_dir"
}

# Sync one source skill into one target directory.
sync_skill_to_target() {
  local name="$1" target_dir="$2"
  local link_path="$target_dir/$name"

  if [[ -L "$link_path" ]]; then
    local target; target="$(readlink "$link_path")"
    if points_to_source "$target" "$name"; then
      return 0  # already a correct managed link
    fi
    if [[ "$MODE" == "check" ]]; then
      fail "link drift: $link_path -> $target"
      return 0
    fi
    remove_link "$link_path"; create_link "$link_path" "$name"
    echo "[skills-sync] updated link: $link_path"
    return 0
  fi

  if is_dead_text_link "$link_path" "$name"; then
    if [[ "$MODE" == "check" ]]; then
      fail "dead text-file link (symlink not materialized): $link_path"
      return 0
    fi
    rm -f "$link_path"; create_link "$link_path" "$name"
    echo "[skills-sync] replaced dead text link: $link_path"
    return 0
  fi

  if [[ -e "$link_path" ]]; then
    fail "refusing to replace existing non-managed path: $link_path"
    return 0
  fi

  if [[ "$MODE" == "check" ]]; then
    fail "missing link: $link_path"
    return 0
  fi
  create_link "$link_path" "$name"
  echo "[skills-sync] created link: $link_path"
}

# Remove managed links in a target whose source skill no longer exists.
remove_stale_links() {
  local target_dir="$1" entry name target
  while IFS= read -r -d '' entry; do
    [[ -L "$entry" ]] || continue
    name="$(basename "$entry")"
    [[ -d "$SOURCE_DIR/$name" ]] && continue
    target="$(readlink "$entry")"
    points_to_source "$target" "$name" || continue
    if [[ "$MODE" == "check" ]]; then
      fail "stale managed link: $entry -> $target"
    else
      remove_link "$entry"
      echo "[skills-sync] removed stale link: $entry"
    fi
  done < <(find "$target_dir" -mindepth 1 -maxdepth 1 -print0)
}

if [[ ! -d "$SOURCE_DIR" ]]; then
  fail "missing source directory: $SOURCE_DIR"
  exit "$STATUS"
fi

for target_dir in "${TARGET_DIRS[@]}"; do
  ensure_target_dir "$target_dir" || continue
  remove_stale_links "$target_dir"
  while IFS= read -r -d '' skill_dir; do
    sync_skill_to_target "$(basename "$skill_dir")" "$target_dir"
  done < <(find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
done

if [[ "$STATUS" -ne 0 ]]; then
  [[ "$MODE" == "check" ]] && echo "[skills-sync] check failed; run: bash scripts/sync_common_skills.sh" >&2
  exit "$STATUS"
fi

echo "[skills-sync] ${MODE} passed"
