#!/usr/bin/env bash
set -euo pipefail

# Intentionally cheap checks only. This script is safe to run after frequent file edits.
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

python3 -m compileall -q scripts

if command -v bash >/dev/null 2>&1; then
  while IFS= read -r -d '' file; do
    bash -n "$file"
  done < <(find scripts -name '*.sh' -type f -print0)
fi

python3 - <<'PY'
import json
import pathlib
import sys

excluded = {'.git', 'node_modules', '.venv', 'venv', 'dist', 'build', '.agent'}
for path in pathlib.Path('.').rglob('*.json'):
    if any(part in excluded for part in path.parts):
        continue
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        print(f'{path}: {exc}', file=sys.stderr)
        raise SystemExit(1)
PY
