# 04-02 훅 설정 예시

[../../plan.md](../../plan.md) 04-02 진행 흐름의 4단계(짧은 실습)에서 사용. 코드 변경 후 lint·type-check·test를 자동으로 강제하는 PostToolUse 훅 예시.

## 언어 분기

| 언어 | 파일 | 실행 명령 |
| --- | --- | --- |
| **JS/TS** | [hooks-js.json](hooks-js.json) | `npm run lint && npx tsc --noEmit && npm test` |
| **Python** | [hooks-python.json](hooks-python.json) | `ruff check . && mypy . && pytest -q` |

수강생 프로젝트 언어에 맞춰 **하나만 시연**. 두 언어를 모두 보여주면 훅 개념보다 도구 차이에 시간을 빼앗긴다.

## 훅 블록 구조 한눈에

```json
{
  "hooks": {
    "<이벤트 이름>": [
      {
        "matcher": "<어떤 도구 호출에 발동할지 정규식>",
        "hooks": [
          { "type": "command", "command": "<실행할 셸 명령>" }
        ]
      }
    ]
  }
}
```

- **이벤트 이름**: `PostToolUse`(도구 호출 직후), `Stop`(세션 종료 직전) 등. 우리 시나리오는 `PostToolUse`.
- **matcher**: `Edit|Write` 처럼 파일 변경 도구만 잡는 패턴이 가장 흔하다.
- **command**: 실패하면(exit code ≠ 0) 훅이 작업을 막는다.

> (촬영일 기준 공식 문서 확인) 이벤트 이름과 키 위치는 버전에 따라 다를 수 있다. https://code.claude.com/docs/en/hooks 에서 현재 키 이름을 한 번 더 검증한다.

## 우회 가이드 — 훅이 정상 작업까지 막을 때

수강생 README에 다음 한 줄을 남기게 한다.

> "lint·test가 임시로 실패하는 동안 작업을 이어가야 할 때는 `.claude/settings.json`의 hooks 블록을 일시적으로 빈 객체(`{}`)로 두고 작업한다. 작업이 끝나면 반드시 되돌린다."

## Codex 동등 효과

Claude Code의 `hooks`와 동일한 이름의 키가 Codex에 없을 수 있다. [codex-equivalent.md](codex-equivalent.md) 참조.

## 강사가 챙길 자산

- **훅이 막아주는 케이스 1개** 시연 — 일부러 lint 에러가 나는 코드를 Edit 도구로 저장 → 훅이 작업 차단.
- **훅을 임시로 풀어 우회하는 케이스 1개** 시연 — 우회 후 다시 복원하는 흐름까지.
- (촬영일 기준) hooks 이벤트 이름·matcher 문법을 공식 문서로 한 번 더 확인.
