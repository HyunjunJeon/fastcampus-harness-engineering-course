"""PreToolUse 훅에서 호출되는 위험 명령 차단 정책.

stdin으로 들어오는 Claude Code 또는 Codex 훅 페이로드(JSON)를 읽어,
DENY_PATTERNS에 매칭되면 deny 결정을 돌려보냅니다.

이것은 편의 장치이지 최종 보안 경계가 아닙니다.
실제 보안은 권한 설정, 샌드박스, 브랜치 보호, CI가 함께 책임집니다.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class DenyRule:
    pattern: str
    reason: str


DENY_RULES = [
    DenyRule(r"\brm\s+-rf\s+/", "Refusing to delete the filesystem root."),
    DenyRule(r"\brm\s+-rf\s+\.git\b", "Refusing to delete Git history metadata."),
    DenyRule(
        r"\bchmod\s+-R\s+777\b", "Refusing broad world-writable permission changes."
    ),
    DenyRule(
        r"\bcat\s+\.env\b", "Protected path: .env files must not be read by an agent."
    ),
    DenyRule(r"\bprintenv\b", "Environment dumping may expose secrets."),
    DenyRule(
        r"\bcurl\b.*\|\s*sh\b", "Piping remote scripts into a shell requires review."
    ),
    DenyRule(
        r"\bgit\s+push\s+--force(?:\s|-with-lease)?\b.*\b(?:main|master|prod)\b",
        "Force pushing to a protected branch requires human approval.",
    ),
    DenyRule(r"\bgit\s+push\b", "pushing code requires explicit human approval."),
    DenyRule(
        r"\bgit\s+(?:reset\s+--hard|clean\s+-fd|checkout\s+--)\b",
        "This command rewrites or discards local history/files and requires human approval.",
    ),
    DenyRule(
        r"\bterraform\s+apply\b", "Infrastructure changes require human approval."
    ),
    DenyRule(
        r"\bkubectl\s+delete\b", "Cluster deletion commands require human approval."
    ),
]

PROTECTED_PATH_PATTERNS = (
    r"(^|/)\.env(?:\.|$)",
    r"(^|/)secrets/",
    r"\.pem$",
    r"\.key$",
    r"(^|/)credentials\.json$",
    r"(^|/)service-account.*\.json$",
)


def payload_text(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False)


def tool_input(payload: dict[str, object]) -> dict[str, object]:
    value = payload.get("tool_input")
    return value if isinstance(value, dict) else {}


def candidate_paths(payload: dict[str, object]) -> list[str]:
    data = tool_input(payload)
    paths: list[str] = []
    for key in ("file_path", "path", "target_file"):
        value = data.get(key)
        if isinstance(value, str):
            paths.append(value)
    return paths


def protected_path_reason(payload: dict[str, object]) -> str | None:
    for path in candidate_paths(payload):
        normalized = path
        while normalized.startswith("./"):
            normalized = normalized[2:]
        for pattern in PROTECTED_PATH_PATTERNS:
            if re.search(pattern, normalized):
                return f"Protected path: {path} requires human approval."
    return None


def is_denied(payload: dict[str, object]) -> str | None:
    path_reason = protected_path_reason(payload)
    if path_reason:
        return path_reason

    text = payload_text(payload)
    for rule in DENY_RULES:
        if re.search(rule.pattern, text):
            return rule.reason
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    reason = is_denied(payload)

    if reason:
        # 신 형식(permissionDecision)을 우선 쓰고, 함께 stderr로 사람 친화 메시지를 남깁니다.
        # 레거시 형식(decision: block)을 받는 환경에서도 인식되도록 두 키를 모두 포함합니다.
        # exit code 2 도 함께 반환해 형식 무관한 폴백을 확보합니다.
        decision = {
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
            # 레거시 호환:
            "decision": "block",
            "reason": reason,
        }
        print(json.dumps(decision, ensure_ascii=False))
        print(reason, file=sys.stderr)
        return 2

    print(json.dumps({"permissionDecision": "allow"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
