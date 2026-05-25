"""Tests for Git operation governance in the PreToolUse hook policy."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "risky_command_policy.py"


def run_policy(payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(SCRIPT)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )


def bash_payload(command: str) -> dict[str, object]:
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }


def write_payload(path: str) -> dict[str, object]:
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": path, "content": "secret"},
    }


def decision(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    return json.loads(result.stdout)


def test_allows_read_only_git_diff() -> None:
    result = run_policy(bash_payload("git diff --stat"))

    assert result.returncode == 0
    assert decision(result)["permissionDecision"] == "allow"


def test_blocks_git_push_until_human_approval() -> None:
    result = run_policy(bash_payload("git push origin feature/docs-hook"))

    assert result.returncode == 2
    body = decision(result)
    assert body["permissionDecision"] == "deny"
    assert "human approval" in str(body["permissionDecisionReason"])


def test_blocks_force_push_to_protected_branch() -> None:
    result = run_policy(bash_payload("git push --force origin main"))

    assert result.returncode == 2
    assert "protected branch" in str(decision(result)["permissionDecisionReason"])


def test_blocks_destructive_history_rewrite() -> None:
    result = run_policy(bash_payload("git reset --hard HEAD~1"))

    assert result.returncode == 2
    assert "rewrites or discards local history" in str(
        decision(result)["permissionDecisionReason"]
    )


def test_blocks_secret_file_write() -> None:
    result = run_policy(write_payload(".env"))

    assert result.returncode == 2
    assert "Protected path" in str(decision(result)["permissionDecisionReason"])
