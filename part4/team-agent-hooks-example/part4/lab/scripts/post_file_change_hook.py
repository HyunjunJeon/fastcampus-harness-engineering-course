#!/usr/bin/env python3
"""Run cheap, deterministic checks immediately after agent file edits."""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover
    tomllib = None  # type: ignore

from hook_common import (
    emit_json,
    load_policy,
    log_event,
    path_matches,
    read_stdin_json,
    rel_to_root,
    repo_root,
    run_cmd,
    top_level_block,
    truncate,
)
from risky_command_policy import extract_paths


def changed_paths_from_payload(payload: dict[str, Any], root: Path) -> list[str]:
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") or {}
    paths = extract_paths(tool_name, tool_input, root)
    response = payload.get("tool_response") or {}
    if isinstance(response, dict):
        for key in ("filePath", "file_path", "path"):
            value = response.get(key)
            if isinstance(value, str):
                paths.append(rel_to_root(value, root))
    seen: list[str] = []
    for p in paths:
        if p and p not in seen:
            seen.append(p)
    return seen


def validate_json(path: Path) -> str | None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return None
    except Exception as exc:
        return f"{path}: JSON parse failed: {exc}"


def validate_toml(path: Path) -> str | None:
    if tomllib is None:
        return None
    try:
        tomllib.loads(path.read_text(encoding="utf-8"))
        return None
    except Exception as exc:
        return f"{path}: TOML parse failed: {exc}"


def validate_python(path: Path) -> str | None:
    try:
        py_compile.compile(str(path), doraise=True)
        return None
    except Exception as exc:
        return f"{path}: Python compile failed: {exc}"


def validate_shell(path: Path, root: Path) -> str | None:
    code, out, err = run_cmd(["bash", "-n", str(path)], root, timeout=20)
    if code != 0:
        return f"{path}: shell syntax failed:\n{out}{err}"
    return None


def run_project_fast_check(root: Path, timeout: int = 120) -> str | None:
    check = root / "scripts" / "project_fast_check.sh"
    if not check.exists():
        return None
    code, out, err = run_cmd(["bash", str(check)], root, timeout=timeout)
    if code != 0:
        return f"scripts/project_fast_check.sh failed with exit {code}:\n{truncate(out + err)}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", choices=["claude", "codex"], default="claude")
    args = parser.parse_args()
    payload = read_stdin_json()
    event_name = str(payload.get("hook_event_name") or "PostToolUse")
    root = repo_root(payload.get("cwd"))
    policy = load_policy(root)
    paths = changed_paths_from_payload(payload, root)

    if not paths:
        return 0

    protected = [p for p in paths if path_matches(p, policy.get("protected_paths", []))]
    if protected:
        reason = "Agent changed or attempted to change protected paths: " + ", ".join(protected)
        emit_json(top_level_block(reason, event_name=event_name, context=reason))
        return 0

    errors: list[str] = []
    for rel in paths:
        path = root / rel
        if not path.exists() or not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix == ".json":
            err = validate_json(path)
        elif suffix == ".toml":
            err = validate_toml(path)
        elif suffix == ".py":
            err = validate_python(path)
        elif suffix in {".sh", ".bash", ".zsh"}:
            err = validate_shell(path, root)
        else:
            err = None
        if err:
            errors.append(err)

    run_fast = os.environ.get("AGENT_POST_HOOK_FAST_VERIFY", "0") == "1"
    if run_fast:
        err = run_project_fast_check(root)
        if err:
            errors.append(err)

    if errors:
        reason = "Post-file-change checks failed. Fix these before continuing:\n" + truncate("\n\n".join(errors), 5000)
        log_event(root, "post_file_change_hook", reason)
        emit_json(top_level_block(reason, event_name=event_name, context=reason))
        return 0

    log_event(root, "post_file_change_hook", f"checked: {', '.join(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
