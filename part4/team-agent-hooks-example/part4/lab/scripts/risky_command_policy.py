#!/usr/bin/env python3
"""PreToolUse / PermissionRequest policy gate for risky commands and paths.

This script is shared by Claude Code and Codex. Use --runtime to adapt output to
each tool's currently supported decision surface.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from hook_common import (
    additional_context,
    emit_json,
    load_policy,
    log_event,
    path_matches,
    permission_request_decision,
    pretool_decision,
    read_stdin_json,
    rel_to_root,
    repo_root,
    truncate,
)


def extract_command(tool_name: str, tool_input: Any) -> str:
    if isinstance(tool_input, dict):
        for key in ("command", "cmd", "script", "patch"):
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
    if isinstance(tool_input, str):
        return tool_input
    return ""


def extract_paths(tool_name: str, tool_input: Any, root: Path) -> list[str]:
    paths: list[str] = []
    if isinstance(tool_input, dict):
        for key in ("file_path", "filePath", "path"):
            value = tool_input.get(key)
            if isinstance(value, str):
                paths.append(rel_to_root(value, root))
        # Claude MultiEdit style payloads still carry a top-level file_path.
        command = extract_command(tool_name, tool_input)
    else:
        command = extract_command(tool_name, tool_input)

    # Codex apply_patch payloads normally contain a patch command string.
    for line in command.splitlines():
        stripped = line.strip()
        for marker in ("*** Add File:", "*** Update File:", "*** Delete File:"):
            if stripped.startswith(marker):
                paths.append(rel_to_root(stripped[len(marker):].strip(), root))
        match = re.match(r"diff --git a/(.*?) b/(.*)$", stripped)
        if match:
            paths.append(rel_to_root(match.group(2), root))
    # Deduplicate without changing order.
    seen: list[str] = []
    for p in paths:
        if p and p not in seen:
            seen.append(p)
    return seen


def first_matching_command(command: str, entries: list[dict[str, str]]) -> tuple[str, str] | None:
    for entry in entries:
        pattern = entry.get("regex", "")
        if not pattern:
            continue
        try:
            if re.search(pattern, command, flags=re.IGNORECASE | re.MULTILINE):
                return entry.get("id", "command-policy"), entry.get("reason", "Command blocked by team policy")
        except re.error as exc:
            return "invalid-policy-regex", f"Invalid policy regex {pattern!r}: {exc}"
    return None


def classify(payload: dict[str, Any], policy: dict[str, Any], root: Path) -> tuple[str, str, str]:
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}
    command = extract_command(tool_name, tool_input)
    paths = extract_paths(tool_name, tool_input, root)

    protected_paths = policy.get("protected_paths", [])
    governed_paths = policy.get("governed_paths", [])

    for rel_path in paths:
        if path_matches(rel_path, protected_paths):
            return "deny", "protected-path", f"Protected path '{rel_path}' cannot be read or modified by an agent hook flow. Use a human-reviewed secret/config process."

    deny_match = first_matching_command(command, policy.get("deny_command_patterns", []))
    if deny_match:
        policy_id, reason = deny_match
        return "deny", policy_id, reason

    for rel_path in paths:
        if path_matches(rel_path, governed_paths):
            return "ask", "governed-path", f"Governed path '{rel_path}' is part of team hook/policy/CI controls. Require human review evidence before proceeding."

    approval_match = first_matching_command(command, policy.get("approval_command_patterns", []))
    if approval_match:
        policy_id, reason = approval_match
        return "ask", policy_id, reason

    return "allow", "no-match", ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", choices=["claude", "codex"], default="claude")
    args = parser.parse_args()

    payload = read_stdin_json()
    root = repo_root(payload.get("cwd"))
    policy = load_policy(root)
    event_name = str(payload.get("hook_event_name") or "PreToolUse")
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}
    command = extract_command(tool_name, tool_input)
    paths = extract_paths(tool_name, tool_input, root)
    decision, policy_id, reason = classify(payload, policy, root)

    if decision == "allow":
        return 0

    context = "\n".join([
        f"Team policy id: {policy_id}",
        f"Tool: {tool_name or 'unknown'}",
        f"Paths: {', '.join(paths) if paths else '-'}",
        f"Command: {truncate(command, 1200) if command else '-'}",
        "Expected action: stop and explain the safer alternative, or ask the human to approve the governed operation.",
    ])
    log_event(root, "risky_command_policy", f"{event_name} {decision} {policy_id}: {reason}")

    if event_name == "PermissionRequest":
        if decision == "deny":
            emit_json(permission_request_decision(reason, behavior="deny"))
        # For ask-level cases, stay silent so the normal human permission prompt is shown.
        return 0

    if event_name == "PreToolUse":
        emit_json(pretool_decision(args.runtime, decision, reason, context=context))
        return 0

    # Defensive fallback for accidental wiring to other events.
    emit_json(additional_context(event_name, context, system_message=reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
