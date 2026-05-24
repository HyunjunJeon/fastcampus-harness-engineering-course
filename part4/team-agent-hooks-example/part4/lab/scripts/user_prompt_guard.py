#!/usr/bin/env python3
"""Lightweight prompt guard and contextual reminder.

This hook is intentionally conservative. It only blocks explicit attempts to bypass
the governance layer, and otherwise adds context for risky workflows.
"""

from __future__ import annotations

import argparse
import re

from hook_common import additional_context, emit_json, read_stdin_json, top_level_block


BYPASS_RE = re.compile(r"\b(ignore|bypass|disable|turn off|skip)\b.{0,40}\b(hook|policy|ruleset|rules|verification|approval)\b", re.I | re.S)
RISKY_RE = re.compile(r"\b(commit|pull request|pr|merge|deploy|release|publish|production|secret|env)\b", re.I)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", choices=["claude", "codex"], default="claude")
    parser.parse_args()
    payload = read_stdin_json()
    event_name = str(payload.get("hook_event_name") or "UserPromptSubmit")
    prompt = str(payload.get("prompt") or "")

    # Allow policy maintenance requests; block only operational bypass requests.
    if BYPASS_RE.search(prompt) and not re.search(r"\b(update|review|improve|design|document)\b.{0,40}\b(policy|hook|rules)", prompt, re.I):
        emit_json(top_level_block(
            "This request asks to bypass team agent governance. Update the policy through review instead of skipping hooks or verification.",
            event_name=event_name,
            context="Bypass attempt blocked by team prompt guard.",
        ))
        return 0

    if RISKY_RE.search(prompt):
        context = (
            "This task touches a governed workflow. Before final response or PR, include: "
            "goal/exclusion summary, changed files, verification commands and output, policy exceptions, and required human approvals."
        )
        emit_json(additional_context(event_name, context))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
