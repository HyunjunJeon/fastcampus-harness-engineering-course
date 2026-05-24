#!/usr/bin/env python3
"""Shared utilities for Claude Code and Codex hook scripts.

The scripts in this directory intentionally avoid third-party dependencies so the
same hook package can run in a fresh developer workstation, CI, or an agent sandbox.
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


DEFAULT_POLICY: dict[str, Any] = {
    "version": "2026-05-24",
    "protected_paths": [
        ".env", ".env.*", "**/.env", "**/.env.*", "secrets/**", "**/secrets/**",
        "*.pem", "*.key", "**/*.pem", "**/*.key", "**/id_rsa", "**/id_ed25519"
    ],
    "governed_paths": [
        ".github/workflows/**", ".github/RULESETS.md", ".github/CODEOWNERS",
        ".claude/settings.json", ".codex/hooks.json", ".codex/config.toml", ".codex/rules/**",
        "policy/**", "scripts/*hook*.py", "scripts/risky_command_policy.py",
        "scripts/agent_verify.sh", "docs/team-agent-policy.md", "docs/architecture.md"
    ],
    "deny_command_patterns": [
        {"id": "remove-root", "regex": r"\brm\s+-[^\n;]*r[^\n;]*f[^\n;]*(?:/|~|\$HOME)(?:\s|$)", "reason": "root/home destructive removal is forbidden"},
        {"id": "curl-pipe-shell", "regex": r"\b(curl|wget)\b[^\n;|]*(\||>)\s*(sudo\s+)?(sh|bash|zsh)\b", "reason": "network pipe-to-shell is forbidden"},
        {"id": "chmod-777", "regex": r"\bchmod\s+-R\s+777\b", "reason": "recursive chmod 777 is forbidden"},
        {"id": "force-push", "regex": r"\bgit\s+push\b[^\n;]*(--force\b|-f\b)", "reason": "force push is forbidden; use protected branch workflow"},
        {"id": "secret-read", "regex": r"\b(cat|less|more|head|tail|grep|rg|awk|sed)\b[^\n;]*(\.env|secrets/|id_rsa|id_ed25519|\.pem|\.key)\b", "reason": "reading secrets through agent tools is forbidden"},
        {"id": "disk-format", "regex": r"\b(mkfs|dd\s+if=|diskutil\s+erase|format\s+[A-Z]:)\b", "reason": "disk formatting/destructive block operations are forbidden"}
    ],
    "approval_command_patterns": [
        {"id": "git-push", "regex": r"\bgit\s+push\b", "reason": "pushing code requires explicit human approval"},
        {"id": "release-or-publish", "regex": r"\b(npm\s+publish|pnpm\s+publish|yarn\s+npm\s+publish|twine\s+upload|docker\s+push|gh\s+release\s+create)\b", "reason": "publishing artifacts requires release approval"},
        {"id": "infra-change", "regex": r"\b(terraform\s+apply|pulumi\s+up|kubectl\s+(apply|delete|rollout|scale)|helm\s+(install|upgrade|uninstall)|aws\s+cloudformation\s+(deploy|delete-stack))\b", "reason": "infrastructure changes require operator approval"},
        {"id": "prod-db", "regex": r"\b(psql|mysql|mongosh|redis-cli)\b[^\n;]*(prod|production|staging)", "reason": "shared database access requires approval"},
        {"id": "history-rewrite", "regex": r"\bgit\s+(reset\s+--hard|clean\s+-fdx|rebase\b)", "reason": "history or working-tree rewrite requires approval"},
        {"id": "pr-merge", "regex": r"\bgh\s+pr\s+merge\b", "reason": "PR merge requires repository policy checks"}
    ],
    "docs_sync_rules": [
        {
            "name": "public-api-contract",
            "when_any": ["src/api/**", "app/api/**", "apps/*/api/**", "packages/*/src/api/**", "openapi/**"],
            "require_any": ["docs/api-contract.md", "openapi/**"],
            "local_mode": "warn",
            "ci_mode": "enforce"
        },
        {
            "name": "agent-policy-contract",
            "when_any": ["scripts/*hook*.py", "scripts/risky_command_policy.py", "scripts/agent_verify.sh", "policy/**", ".claude/settings.json", ".codex/hooks.json", ".codex/rules/**"],
            "require_any": ["docs/team-agent-policy.md", "docs/architecture.md"],
            "local_mode": "warn",
            "ci_mode": "enforce"
        }
    ],
    "verification": {
        "exclude_dirs": [".git", "node_modules", ".venv", "venv", "dist", "build", "coverage", ".agent", "__pycache__"],
        "max_output_chars": 6000
    }
}


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError as exc:
        print(f"Invalid hook JSON input: {exc}", file=sys.stderr)
        return {}


def emit_json(obj: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
    sys.stdout.write("\n")


def repo_root(cwd: str | None = None) -> Path:
    candidates = [
        os.environ.get("CLAUDE_PROJECT_DIR"),
        os.environ.get("CODEX_REPO_ROOT"),
        os.environ.get("CODEX_WORKSPACE_ROOT"),
        os.environ.get("GITHUB_WORKSPACE"),
    ]
    for candidate in candidates:
        if candidate:
            p = Path(candidate).expanduser().resolve()
            if p.exists():
                return p

    start = Path(cwd or os.getcwd()).expanduser().resolve()
    try:
        out = subprocess.check_output(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        ).strip()
        if out:
            return Path(out).resolve()
    except Exception:
        pass
    return start


def load_policy(root: Path) -> dict[str, Any]:
    policy_path = Path(os.environ.get("AGENT_POLICY_FILE", "policy/agent-policy.json"))
    if not policy_path.is_absolute():
        policy_path = root / policy_path
    if not policy_path.exists():
        return DEFAULT_POLICY
    try:
        loaded = json.loads(policy_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Could not read policy file {policy_path}: {exc}. Using defaults.", file=sys.stderr)
        return DEFAULT_POLICY
    return deep_merge(DEFAULT_POLICY, loaded)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def rel_to_root(path: str | Path, root: Path) -> str:
    p = Path(str(path)).expanduser()
    try:
        if p.is_absolute():
            return p.resolve().relative_to(root.resolve()).as_posix()
        return PurePosixPath(str(p).replace("\\", "/")).as_posix().lstrip("./")
    except Exception:
        return str(path).replace("\\", "/")


def path_matches(path: str, patterns: Iterable[str]) -> bool:
    normalized = path.replace("\\", "/").lstrip("./")
    for pattern in patterns:
        pat = pattern.replace("\\", "/").lstrip("./")
        if fnmatch.fnmatch(normalized, pat) or fnmatch.fnmatch("/" + normalized, pat):
            return True
        # Make patterns like .env match nested .env when teams expect that behavior.
        if not pat.startswith("**/") and fnmatch.fnmatch(PurePosixPath(normalized).name, pat):
            return True
    return False


def truncate(text: str, limit: int = 6000) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 200] + f"\n... [truncated {len(text) - limit + 200} chars]"


def run_cmd(cmd: list[str], root: Path, timeout: int = 120) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(root),
            text=True,
            capture_output=True,
            timeout=timeout,
            env=os.environ.copy(),
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", (exc.stderr or "") + f"\nTimed out after {timeout}s"
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except Exception as exc:
        return 1, "", repr(exc)


def changed_files_from_git(root: Path, base_ref: str | None = None) -> list[str]:
    commands: list[list[str]] = []
    if base_ref:
        commands.append(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
    env_base = os.environ.get("GITHUB_BASE_REF")
    if env_base:
        commands.append(["git", "diff", "--name-only", f"origin/{env_base}...HEAD"])
    commands.extend([
        ["git", "diff", "--name-only", "--cached"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--name-only", "HEAD~1..HEAD"],
    ])
    seen: list[str] = []
    for cmd in commands:
        code, out, _ = run_cmd(cmd, root, timeout=15)
        if code == 0 and out.strip():
            for line in out.splitlines():
                line = line.strip()
                if line and line not in seen:
                    seen.append(line)
            if seen:
                return seen
    return seen


def log_event(root: Path, name: str, message: str) -> None:
    try:
        log_dir = root / ".agent" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        with (log_dir / f"{name}.log").open("a", encoding="utf-8") as f:
            f.write(f"[{stamp}] {message}\n")
    except Exception:
        pass


def pretool_decision(runtime: str, decision: str, reason: str, *, context: str | None = None) -> dict[str, Any]:
    """Return a PreToolUse-compatible decision for Claude Code or Codex.

    Codex currently supports deny for PreToolUse. Claude Code also supports ask.
    For Codex ask-like cases, return only context/systemMessage and allow the normal
    approval path or Codex Rules to handle escalation.
    """
    if decision == "deny":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
                **({"additionalContext": context} if context else {}),
            }
        }
    if decision == "ask" and runtime == "claude":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": reason,
                **({"additionalContext": context} if context else {}),
            }
        }
    if decision == "ask":
        return {
            "systemMessage": reason,
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": context or reason,
            },
        }
    return {}


def permission_request_decision(reason: str, behavior: str = "deny") -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {
                "behavior": behavior,
                "message": reason,
            },
        }
    }


def top_level_block(reason: str, *, event_name: str | None = None, context: str | None = None) -> dict[str, Any]:
    obj: dict[str, Any] = {"decision": "block", "reason": reason}
    if event_name and context:
        obj["hookSpecificOutput"] = {"hookEventName": event_name, "additionalContext": context}
    return obj


def additional_context(event_name: str, context: str, *, system_message: str | None = None) -> dict[str, Any]:
    obj: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": context,
        }
    }
    if system_message:
        obj["systemMessage"] = system_message
    return obj
