#!/usr/bin/env bash
set -euo pipefail

MODE="full"
if [[ "${1:-}" == "--fast" ]]; then
  MODE="fast"
  shift || true
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

echo "== agent_verify.sh ($MODE) =="
echo "root: $ROOT"

echo "-- protected files check"
python3 - <<'PY'
import fnmatch
import json
import pathlib
import subprocess
import sys

policy_path = pathlib.Path('policy/agent-policy.json')
if policy_path.exists():
    policy = json.loads(policy_path.read_text(encoding='utf-8'))
else:
    policy = {'protected_paths': ['.env', '.env.*', 'secrets/**', '**/*.pem', '**/*.key']}
patterns = [p.replace('\\', '/').lstrip('./') for p in policy.get('protected_paths', [])]
try:
    tracked = subprocess.check_output(['git', 'ls-files'], text=True, stderr=subprocess.DEVNULL).splitlines()
except Exception:
    tracked = []
bad = []
for p in tracked:
    normalized = p.replace('\\', '/').lstrip('./')
    name = pathlib.PurePosixPath(normalized).name
    for pat in patterns:
        if fnmatch.fnmatch(normalized, pat) or fnmatch.fnmatch(name, pat):
            bad.append(p)
            break
if bad:
    print('Protected files are tracked:', file=sys.stderr)
    for p in bad:
        print(f'- {p}', file=sys.stderr)
    raise SystemExit(1)
PY

echo "-- Python syntax"
python3 -m compileall -q scripts

echo "-- JSON/TOML syntax"
python3 - <<'PY'
import json
import pathlib
import sys
try:
    import tomllib
except Exception:
    tomllib = None

excluded = {'.git', 'node_modules', '.venv', 'venv', 'dist', 'build', 'coverage', '.agent', '__pycache__'}
def skip(path):
    return any(part in excluded for part in path.parts)

for path in pathlib.Path('.').rglob('*.json'):
    if skip(path):
        continue
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        print(f'{path}: JSON error: {exc}', file=sys.stderr)
        raise SystemExit(1)

if tomllib is not None:
    for path in pathlib.Path('.').rglob('*.toml'):
        if skip(path):
            continue
        try:
            tomllib.loads(path.read_text(encoding='utf-8'))
        except Exception as exc:
            print(f'{path}: TOML error: {exc}', file=sys.stderr)
            raise SystemExit(1)
PY

echo "-- shell syntax"
if command -v bash >/dev/null 2>&1; then
  while IFS= read -r -d '' file; do
    bash -n "$file"
  done < <(find scripts -name '*.sh' -type f -print0)
fi

echo "-- docs sync"
if ! python3 scripts/changed_docs_check.py; then
  if [[ "$MODE" == "fast" ]]; then
    echo "docs sync warning ignored in fast mode"
  else
    exit 1
  fi
fi

if [[ "$MODE" != "fast" ]]; then
  echo "-- project tests if available"
  if [[ -f pyproject.toml ]] && command -v pytest >/dev/null 2>&1; then
    pytest
  fi
  if [[ -f package.json ]] && command -v npm >/dev/null 2>&1 && command -v node >/dev/null 2>&1; then
    set +e
    node -e "const fs=require('fs');const pkg=JSON.parse(fs.readFileSync('package.json','utf8'));const s=pkg.scripts||{};process.exit(s.lint?10:(s.test?11:0));"
    rc=$?
    set -e
    if [[ "$rc" == "10" ]]; then
      npm run lint
      if node -e "const s=require('./package.json').scripts||{};process.exit(s.test?0:1)"; then
        CI=true npm test
      fi
    elif [[ "$rc" == "11" ]]; then
      CI=true npm test
    fi
  fi
  if [[ -f go.mod ]] && command -v go >/dev/null 2>&1; then
    go test ./...
  fi
fi

echo "agent_verify.sh: ok"
