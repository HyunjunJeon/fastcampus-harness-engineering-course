# Session 2-3 - 위험한 명령을 막는 PreToolUse 정책

> PreToolUse 정책은 Tool 명령이 실행되기 전에 멈춰서 확인하게 만드는 검사

- 명령을 자동 허용, 사람 승인 필요, 기본 차단으로 분류합니다.
- 삭제, 배포, 비밀 파일 접근, 외부 전송은 기본적으로 멈춥니다.
- PreToolUse를 유용한 가드레일로 쓰되 완전한 보안 경계로 믿지 않습니다.

## 강의 진행 흐름

1. `PreToolUse`를 "명령 실행 전 문 앞 검사"로 소개합니다.
2. 위험 명령을 세 계층으로 나눕니다 — 절대 금지(예: `rm -rf /`, `.env` 읽기), 항상 사람 승인(예: 배포, 보호 브랜치 push), 자동 허용(예: `git diff`, 테스트 실행).
3. AI에게 명령 정책표를 만들게 하되 실제 실행은 절대 하지 않습니다.
4. 세 계층의 분류 기준이 사람마다 다를 수 있다는 점을 확인하고, 팀에서 합의해야 한다고 강조합니다.
5. 훅과 정책의 한계를 설명하고, 권한·샌드박스·브랜치 보호·CI가 같이 있어야 비로소 보안 경계가 된다고 정리합니다.

## Claude Code를 쓴다면

Claude Code에서는 `PreToolUse` 같은 이벤트를 통해 위험한 도구 사용 전에 확인할 수 있습니다. 정책을 만들 때는 도구 이름만 보지 말고 실제 명령이 무엇을 바꾸는지 봐야 합니다.

예를 들어 `git diff`는 확인 명령이지만, `git push`는 외부 저장소에 변경을 올리는 명령입니다.

## Codex를 쓴다면

Codex에서도 Hooks와 Rules를 함께 검토해 실행 전 가드레일을 설계합니다. 

PreToolUse는 그 자체로 **완전한 보안 경계가 아니라 가드레일**입니다. 공식 문서는 그 이유를 "Codex가 다른 지원 도구 경로를 통해 동등한 작업을 수행할 수 있기 때문"이라고 설명합니다. 즉 한 가지 도구 호출을 차단해도 같은 결과를 다른 경로로 달성할 수 있는 길이 남아 있다는 뜻입니다. 그래서 PreToolUse 하나만 믿지 말고, 권한·샌드박스·브랜치 보호·CI까지 함께 세팅해야 합니다.

Codex에는 PreToolUse와 비슷한 자리에 **PermissionRequest**라는 별도 훅도 있습니다. PreToolUse는 "이 도구 호출 자체를 차단할 것인가"를 결정하고, PermissionRequest는 "권한 승인 프롬프트를 사용자에게 띄울지"를 결정합니다. 특히 PermissionRequest에서 `allow`를 돌려주면 승인 프롬프트가 아예 건너뛰어지므로, 사람에게 한 번 더 확인받게 하려면 이 자리에서 `deny`나 명시적 프롬프트를 유지해야 합니다.

정책은 "차단"만이 아니라 "어떤 조건이면 승인할 수 있는지"까지 포함해야 실무에서 쓸 수 있습니다.

## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| 명령어 일부만 보고 허용 | 명령의 실제 영향까지 확인 |
| `rm -rf dist`와 `rm -rf /`를 같은 방식으로 설명 | 범위와 되돌리기 가능성을 따로 판단 |
| 비밀 파일 읽기를 편의상 허용 | `.env`, token, key는 기본 차단 |
| 훅만 있으면 안전하다고 믿기 | 권한, 샌드박스, 사람 승인도 함께 사용 |

## Reference

- 공식 (Claude Code): [Hooks](https://code.claude.com/docs/en/hooks)
- 공식 (Claude Code): [Settings](https://code.claude.com/docs/en/settings)
- 공식 (Codex): [Hooks](https://developers.openai.com/codex/hooks)
- 공식 (Codex): [Rules](https://developers.openai.com/codex/rules)


## 실습 내용

실습 레포 위치: `part4/lab/scripts/risky_command_policy.py`, `part4/lab/.claude/settings.json`, `part4/lab/.codex/hooks.json`

차단 패턴을 한 파일에 모아 두고 두 도구의 PreToolUse 훅이 같은 스크립트를 호출하게 만듭니다.

```python
# scripts/risky_command_policy.py (발췌)
DENY_PATTERNS = [
    r"\brm\s+-rf\s+/",
    r"\brm\s+-rf\s+\.git\b",
    r"\bchmod\s+-R\s+777\b",
    r"\bcat\s+\.env\b",
    r"\bcurl\b.*\|\s*sh\b",
    r"\bgit\s+push\s+--force(\s|-with-lease)?\b.*\b(main|master|prod)\b",
]
```

### 차단 결정을 어떻게 표현하는가

Codex 공식 문서는 PreToolUse 차단 결정을 두 가지 형식으로 받습니다.

```json
// 신 형식 (권장)
{ "permissionDecision": "deny", "permissionDecisionReason": "Blocked by risky command policy" }

// 레거시 형식 (호환을 위해 함께 인정)
{ "decision": "block", "reason": "Blocked by risky command policy" }
```

추가로 stdout에 위 JSON을 쓰지 않더라도 **exit code 2**로 종료하고 stderr에 이유를 출력하는 방식도 차단으로 인식됩니다. 우리 `risky_command_policy.py`는 신 형식 JSON을 stdout에 쓰면서 차단 시 exit 2도 함께 반환하도록 만들어, 어느 형식 해석에서도 안전하게 동작하게 둡니다.

### PermissionRequest 훅과의 차이

PreToolUse가 "도구 호출 자체"를 막는 자리라면, PermissionRequest는 "권한 승인 프롬프트를 띄울지"를 결정하는 자리입니다. PermissionRequest의 결정은 다른 모양입니다.

```json
{ "behavior": "allow" }
{ "behavior": "deny", "message": "Blocked: writes outside workspace are not allowed" }
```

같은 정책을 PreToolUse와 PermissionRequest 두 자리에 동시에 거는 것이 가장 안전합니다. 한쪽에서 `allow`가 돌아가면 사용자에게 승인 프롬프트가 뜨지 않고 그대로 진행되므로, 사람 확인을 반드시 받고 싶은 작업은 PermissionRequest 자리에서 `deny`나 명시적 prompt 결정을 유지해야 합니다.

### *마지막 방어선이 아니다*

훅이 deny 결정을 돌려보내도 그것은 마지막 방어선이 아닙니다. 
공식 문서가 짚는 한계 — "Codex는 다른 지원 도구 경로를 통해 동등한 작업을 수행할 수 있다" — 가 그대로 적용됩니다. 같은 정책을 사용자 권한 설정·샌드박스·브랜치 보호 규칙·CI required status check에서 다시 강제해야 사람의 직접 명령과 우회 경로까지 잡힙니다.
