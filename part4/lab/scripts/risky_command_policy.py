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

DENY_PATTERNS = [
    r"\brm\s+-rf\s+/",
    r"\brm\s+-rf\s+\.git\b",
    r"\bchmod\s+-R\s+777\b",
    r"\bcat\s+\.env\b",
    r"\bprintenv\b",
    r"\bcurl\b.*\|\s*sh\b",
    r"\bgit\s+push\s+--force(\s|-with-lease)?\b.*\b(main|master|prod)\b",
    r"\bterraform\s+apply\b",
    r"\bkubectl\s+delete\b",
]


def is_denied(text: str) -> str | None:
    for pattern in DENY_PATTERNS:
        if re.search(pattern, text):
            return pattern
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    # 페이로드 전체를 텍스트로 만들어 한 번에 매칭합니다.
    blob = json.dumps(payload, ensure_ascii=False)
    matched = is_denied(blob)
    reason = f"Blocked by risky command policy: {matched}" if matched else None

    if matched:
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
