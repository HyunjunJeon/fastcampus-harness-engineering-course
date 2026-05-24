#!/usr/bin/env python3
"""Inject compact team workflow context at session start or prompt submission."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hook_common import additional_context, emit_json, load_policy, read_stdin_json, repo_root, truncate


def summarize_policy(policy: dict) -> str:
    protected = ", ".join(policy.get("protected_paths", [])[:8])
    governed = ", ".join(policy.get("governed_paths", [])[:8])
    return (
        "Team Agent workflow contract:\n"
        "1. Agent may implement and run verification, but humans own goals, boundaries, approvals, and evidence review.\n"
        "2. Use docs for durable guidance, skills for repeated procedures, hooks for deterministic checks, Rules/permissions for approval boundaries, and CI/Rulesets as the final gate.\n"
        "3. Before commits and PRs, produce evidence: diff summary, commands run, test/verification output, and any policy exceptions.\n"
        f"4. Protected paths include: {protected}.\n"
        f"5. Governed paths include: {governed}.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", choices=["claude", "codex"], default="claude")
    args = parser.parse_args()
    payload = read_stdin_json()
    event_name = str(payload.get("hook_event_name") or "SessionStart")
    root = repo_root(payload.get("cwd"))
    policy = load_policy(root)
    context = summarize_policy(policy)

    # Add a very small pointer to the human-readable documents without flooding context.
    for rel in ("docs/team-agent-policy.md", "docs/architecture.md"):
        path = root / rel
        if path.exists():
            context += f"\nReference: {rel}"
    emit_json(additional_context(event_name, truncate(context, 5000)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
