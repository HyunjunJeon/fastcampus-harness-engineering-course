#!/usr/bin/env bash
# 단일 검증 진입점. 사람과 GitHub Actions CI는 이 스크립트를 직접 호출하고,
# Claude Code/Codex Stop 훅은 stop_verify_hook.py 래퍼를 통해 호출합니다.
#
# 사용:
#   bash scripts/agent_verify.sh              # 전체 (개발자 트랙)
#   bash scripts/agent_verify.sh --docs-only  # 문서 검사만 (비개발 트랙)

set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

DOCS_ONLY=0
if [[ "${1:-}" == "--docs-only" ]]; then
  DOCS_ONLY=1
fi

cd "$(dirname "$0")/.."

echo "[verify] common skills links"
bash scripts/sync_common_skills.sh --check

echo "[verify] changed docs check"
python scripts/changed_docs_check.py

if [[ "$DOCS_ONLY" -eq 1 ]]; then
  echo "[verify] docs-only mode: skipping code checks"
  exit 0
fi

# 아래 도구들은 개발자 트랙에서만 동작합니다. 도구가 없으면 안내만 출력하고 통과시킵니다.
PY_TARGETS=(scripts tests)
if [[ -d app ]]; then
  PY_TARGETS+=(app)
fi

if command -v ruff >/dev/null 2>&1; then
  echo "[verify] ruff format check"
  ruff format --check "${PY_TARGETS[@]}" || { echo "[verify] ruff format failed"; exit 1; }
  echo "[verify] ruff lint"
  ruff check "${PY_TARGETS[@]}" || { echo "[verify] ruff lint failed"; exit 1; }
else
  echo "[verify] ruff not installed — skipping (install in 개발자 트랙)"
fi

if [[ ! -d app ]]; then
  echo "[verify] app/ not present yet — skipping mypy and pytest"
  exit 0
fi

if command -v mypy >/dev/null 2>&1; then
  echo "[verify] mypy"
  mypy app || { echo "[verify] mypy failed"; exit 1; }
else
  echo "[verify] mypy not installed — skipping"
fi

if command -v pytest >/dev/null 2>&1; then
  echo "[verify] pytest"
  python -m pytest -q -p no:cacheprovider || { echo "[verify] pytest failed"; exit 1; }
else
  echo "[verify] pytest not installed — skipping"
fi

echo "[verify] all checks passed"
