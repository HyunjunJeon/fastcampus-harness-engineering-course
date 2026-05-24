#!/usr/bin/env python3
"""PreToolUse guard for git commit commands."""

from __future__ import annotations

import argparse
import re
import os

from hook_common import emit_json, pretool_decision, read_stdin_json, repo_root, run_cmd, truncate
from risky_command_policy import extract_command


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", choices=["claude", "codex"], default="claude")
    args = parser.parse_args()
    payload = read_stdin_json()
    tool_input = payload.get("tool_input") or {}
    tool_name = str(payload.get("tool_name") or "")
    command = extract_command(tool_name, tool_input)
    if not re.search(r"(^|[;&|]\s*)git\s+commit\b", command):
        return 0

    root = repo_root(payload.get("cwd"))
    verifier = root / "scripts" / "agent_verify.sh"
    code, out, err = run_cmd(["bash", str(verifier), "--fast"], root, timeout=int(os.environ.get("AGENT_PRE_COMMIT_TIMEOUT", "180")))
    if code != 0:
        reason = (
            "Pre-commit verification failed. Do not create the commit yet. "
            "Fix the failures, then rerun scripts/agent_verify.sh --fast.\n\n"
            + truncate(out + err, 5000)
        )
        emit_json(pretool_decision(args.runtime, "deny", reason, context=reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
