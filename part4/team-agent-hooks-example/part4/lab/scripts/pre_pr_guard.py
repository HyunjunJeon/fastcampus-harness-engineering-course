#!/usr/bin/env python3
"""PreToolUse guard for PR creation/readiness commands."""

from __future__ import annotations

import argparse
import re
import os

from hook_common import emit_json, pretool_decision, read_stdin_json, repo_root, run_cmd, truncate
from risky_command_policy import extract_command


PR_PATTERNS = [
    r"(^|[;&|]\s*)gh\s+pr\s+create\b",
    r"(^|[;&|]\s*)gh\s+pr\s+ready\b",
    r"(^|[;&|]\s*)gh\s+pr\s+merge\b",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", choices=["claude", "codex"], default="claude")
    args = parser.parse_args()
    payload = read_stdin_json()
    tool_input = payload.get("tool_input") or {}
    tool_name = str(payload.get("tool_name") or "")
    command = extract_command(tool_name, tool_input)
    if not any(re.search(p, command) for p in PR_PATTERNS):
        return 0

    root = repo_root(payload.get("cwd"))
    failures: list[str] = []

    code, out, err = run_cmd(["git", "status", "--short"], root, timeout=15)
    if code == 0 and out.strip():
        failures.append("Working tree has uncommitted changes. Commit or intentionally discard them before PR operations:\n" + out)

    verifier = root / "scripts" / "agent_verify.sh"
    code, out, err = run_cmd(["bash", str(verifier)], root, timeout=int(os.environ.get("AGENT_PRE_PR_TIMEOUT", "300")))
    if code != 0:
        failures.append("scripts/agent_verify.sh failed:\n" + truncate(out + err, 5000))

    docs = root / "scripts" / "changed_docs_check.py"
    if docs.exists():
        code, out, err = run_cmd(["python3", str(docs)], root, timeout=60)
        if code != 0:
            failures.append("scripts/changed_docs_check.py failed:\n" + truncate(out + err, 3000))

    if failures:
        reason = "PR guard failed. Fix the following before creating/merging the PR:\n\n" + truncate("\n\n".join(failures), 7000)
        emit_json(pretool_decision(args.runtime, "deny", reason, context=reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
