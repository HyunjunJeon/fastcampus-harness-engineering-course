#!/usr/bin/env python3
"""Stop hook that keeps the agent working until the shared verifier passes."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from hook_common import emit_json, load_policy, log_event, read_stdin_json, repo_root, run_cmd, top_level_block, truncate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", choices=["claude", "codex"], default="claude")
    parser.add_argument("--timeout", type=int, default=int(os.environ.get("AGENT_STOP_VERIFY_TIMEOUT", "240")))
    args = parser.parse_args()

    payload = read_stdin_json()
    root = repo_root(payload.get("cwd"))
    event_name = str(payload.get("hook_event_name") or "Stop")

    # Avoid infinite continuation loops. Both Claude Code and Codex expose this flag.
    if payload.get("stop_hook_active") is True:
        log_event(root, "stop_verify_hook", "stop_hook_active=true; skipping to avoid loop")
        return 0

    verifier = root / "scripts" / "agent_verify.sh"
    if not verifier.exists():
        reason = "scripts/agent_verify.sh is missing; cannot verify agent output."
        emit_json(top_level_block(reason, event_name=event_name, context=reason))
        return 0

    code, out, err = run_cmd(["bash", str(verifier)], root, timeout=args.timeout)
    if code != 0:
        combined = truncate((out or "") + ("\n" if out and err else "") + (err or ""), 6000)
        reason = (
            "Shared verification failed. Continue working, fix the failures, and run scripts/agent_verify.sh again.\n\n"
            f"Verifier exit code: {code}\n"
            f"Verifier output:\n{combined}"
        )
        log_event(root, "stop_verify_hook", f"verify failed exit={code}")
        emit_json(top_level_block(reason, event_name=event_name, context=reason))
        return 0

    log_event(root, "stop_verify_hook", "verify passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
