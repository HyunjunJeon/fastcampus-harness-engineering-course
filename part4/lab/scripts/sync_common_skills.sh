#!/usr/bin/env bash
# Synchronize common skill folders into tool-specific skill locations.

set -euo pipefail

MODE="sync"
if [[ "${1:-}" == "--check" ]]; then
  MODE="check"
elif [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'USAGE'
Usage:
  bash scripts/sync_common_skills.sh          # create/update managed links
  bash scripts/sync_common_skills.sh --check  # verify links without changing files
USAGE
  exit 0
elif [[ "${1:-}" != "" ]]; then
  echo "[skills-sync] unknown option: $1" >&2
  exit 2
fi

cd "$(dirname "$0")/.."

SOURCE_DIR="common_skills"
TARGET_DIRS=(".agents/skills" ".claude/skills")
STATUS=0

fail() {
  echo "[skills-sync] $*" >&2
  STATUS=1
}

is_managed_common_link() {
  local link_target="$1"
  case "$link_target" in
    *common_skills/*) return 0 ;;
    *) return 1 ;;
  esac
}

source_skill_exists() {
  local skill_name="$1"
  [[ -d "$SOURCE_DIR/$skill_name" ]]
}

ensure_target_dir() {
  local target_dir="$1"

  if [[ -d "$target_dir" ]]; then
    return 0
  fi

  if [[ "$MODE" == "check" ]]; then
    fail "missing target directory: $target_dir"
    return 1
  fi

  mkdir -p "$target_dir"
}

preflight_conflicts() {
  local target_dir="$1"
  local skill_dir
  local skill_name
  local link_path
  local expected_target
  local current_target

  while IFS= read -r -d '' skill_dir; do
    skill_name="$(basename "$skill_dir")"
    link_path="$target_dir/$skill_name"
    expected_target="../../common_skills/$skill_name"

    if [[ -L "$link_path" ]]; then
      current_target="$(readlink "$link_path")"
      if [[ "$current_target" == "$expected_target" ]]; then
        continue
      fi
      if is_managed_common_link "$current_target"; then
        continue
      fi
      fail "refusing to replace unmanaged link: $link_path -> $current_target"
      continue
    fi

    if [[ -e "$link_path" ]]; then
      fail "refusing to replace existing non-link path: $link_path"
    fi
  done < <(find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
}

remove_stale_managed_links() {
  local target_dir="$1"
  local entry
  local skill_name
  local current_target

  while IFS= read -r -d '' entry; do
    skill_name="$(basename "$entry")"
    if source_skill_exists "$skill_name"; then
      continue
    fi

    current_target="$(readlink "$entry")"
    if ! is_managed_common_link "$current_target"; then
      continue
    fi

    if [[ "$MODE" == "check" ]]; then
      fail "stale managed link: $entry -> $current_target"
    else
      rm "$entry"
      echo "[skills-sync] removed stale link: $entry"
    fi
  done < <(find "$target_dir" -mindepth 1 -maxdepth 1 -type l -print0)
}

sync_skill_to_target() {
  local skill_dir="$1"
  local target_dir="$2"
  local skill_name
  local link_path
  local expected_target
  local current_target

  skill_name="$(basename "$skill_dir")"
  link_path="$target_dir/$skill_name"
  expected_target="../../common_skills/$skill_name"

  if [[ -L "$link_path" ]]; then
    current_target="$(readlink "$link_path")"
    if [[ "$current_target" == "$expected_target" ]]; then
      return 0
    fi

    if is_managed_common_link "$current_target"; then
      if [[ "$MODE" == "check" ]]; then
        fail "link drift: $link_path -> $current_target (expected $expected_target)"
        return 0
      fi

      rm "$link_path"
      ln -s "$expected_target" "$link_path"
      echo "[skills-sync] updated link: $link_path -> $expected_target"
      return 0
    fi

    fail "refusing to replace unmanaged link: $link_path -> $current_target"
    return 0
  fi

  if [[ -e "$link_path" ]]; then
    fail "refusing to replace existing non-link path: $link_path"
    return 0
  fi

  if [[ "$MODE" == "check" ]]; then
    fail "missing link: $link_path -> $expected_target"
    return 0
  fi

  ln -s "$expected_target" "$link_path"
  echo "[skills-sync] created link: $link_path -> $expected_target"
}

if [[ ! -d "$SOURCE_DIR" ]]; then
  fail "missing source directory: $SOURCE_DIR"
  exit "$STATUS"
fi

for target_dir in "${TARGET_DIRS[@]}"; do
  ensure_target_dir "$target_dir" || continue
  if [[ "$MODE" == "sync" ]]; then
    preflight_conflicts "$target_dir"
  fi
done

if [[ "$STATUS" -ne 0 ]]; then
  exit "$STATUS"
fi

for target_dir in "${TARGET_DIRS[@]}"; do
  ensure_target_dir "$target_dir" || continue
  remove_stale_managed_links "$target_dir"

  while IFS= read -r -d '' skill_dir; do
    sync_skill_to_target "$skill_dir" "$target_dir"
  done < <(find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
done

if [[ "$STATUS" -ne 0 ]]; then
  if [[ "$MODE" == "check" ]]; then
    echo "[skills-sync] check failed; run: bash scripts/sync_common_skills.sh" >&2
  fi
  exit "$STATUS"
fi

echo "[skills-sync] ${MODE} passed"
