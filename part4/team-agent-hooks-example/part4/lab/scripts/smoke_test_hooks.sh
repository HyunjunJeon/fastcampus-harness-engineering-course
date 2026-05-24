#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

payload_rm='{"hook_event_name":"PreToolUse","cwd":"'"$ROOT"'","tool_name":"Bash","tool_input":{"command":"rm -rf /"}}'
out="$(printf '%s' "$payload_rm" | python3 scripts/risky_command_policy.py --runtime claude)"
echo "$out" | grep -q '"permissionDecision":"deny"'

payload_push='{"hook_event_name":"PreToolUse","cwd":"'"$ROOT"'","tool_name":"Bash","tool_input":{"command":"git push origin feature"}}'
out="$(printf '%s' "$payload_push" | python3 scripts/risky_command_policy.py --runtime codex)"
echo "$out" | grep -q 'pushing code requires explicit human approval'

payload_env='{"hook_event_name":"PreToolUse","cwd":"'"$ROOT"'","tool_name":"Write","tool_input":{"file_path":"'"$ROOT"'/.env","content":"x"}}'
out="$(printf '%s' "$payload_env" | python3 scripts/risky_command_policy.py --runtime claude)"
echo "$out" | grep -q 'Protected path'

echo "smoke_test_hooks.sh: ok"
