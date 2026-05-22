# Session 2-1 - 훅이 프롬프트보다 강한 이유

> 훅은 AI 에이전트 시스템이 일하는 동안 발생하는 라이프사이클 이벤트(세션 시작, 도구 호출 전후, 작업 종료 등)에 우리가 정한 코드를 끼워 넣는 메커니즘입니다. 

> 프롬프트는 모델에게 부탁하는 것이므로 실제 수행을 보장하지 않지만, 훅은 정해진 이벤트에서 시스템이 코드를 실행하게 하므로 반복 규칙을 더 강하게 강제할 수 있습니다.

## Keypoint
1. 언제
 > 이벤트 타이밍
2. 무엇을
 > 코드

알아서, 적절하게
> 쓸 수도 있고 안쓸 수도 있고...
> 무조건 써

## 핵심 내용

- 훅이 "AI에게 부탁하는 규칙"이 아니라 "시스템이 정해진 이벤트에 코드를 실행하는 장치"임을 이해합니다.
- Claude Code와 Codex가 노출하는 라이프사이클 이벤트의 비대칭 모양을 한 표로 봅니다.
- 모든 규칙을 훅으로 만들지 않고 자동화할 가치가 있는 규칙만 고릅니다.(EX> Lint, Formatter 등)
- 훅을 완전한 보안 장치가 아니라 자동 확인 장치로 이해합니다.

1. 프롬프트를 "부탁", 훅을 "Agent 라이프사이클 이벤트에 끼워 넣는 코드"로 구분해 설명합니다.
2. AI 에이전트의 라이프사이클 = 세션 시작 → 사용자 입력 → 모델 추론 → 도구 호출 전 → 도구 실행 → 도구 호출 후 → 모델 추론 → 작업 종료 → 세션 끝. 도구마다 열어 둔 이벤트 지점이 다르고, 훅 설계란 결국 어느 지점에 어떤 검사를 끼울지 정하는 일입니다.
3. Claude Code와 Codex가 노출하는 이벤트를 같은 표에 나란히 보여주고, 비대칭의 모양을 함께 확인합니다.
4. 팀 규칙 예시를 보여주고 AI에게 규칙 분류표를 만들게 합니다. 훅으로 옮길 규칙과 사람 승인이 필요한 규칙을 나눕니다.
5. 훅을 완전한 보안 장치로 오해하지 않도록 한계를 정리하고, 비대칭으로 빠지는 자리를 어떻게 메우는지 확인.
(공통 스크립트 + 도구별 훅 + CI 3중 안전망)

---

## 라이프사이클 이벤트 비교

| 라이프사이클 단계 | Claude Code | Codex |
|---|---|---|
| 세션 시작/종료 | SessionStart, Setup, SessionEnd 등 | SessionStart |
| 사용자 프롬프트 제출 직전 | UserPromptSubmit, UserPromptExpansion | UserPromptSubmit |
| 도구 호출 전 | PreToolUse, PermissionRequest, PermissionDenied | PreToolUse, PermissionRequest |
| 도구 호출 후 | PostToolUse, PostToolUseFailure, PostToolBatch | PostToolUse |
| 작업 종료 | Stop, StopFailure, TeammateIdle | Stop |
| 서브에이전트·태스크 | SubagentStart/Stop, TaskCreated/Completed | (현재 별도 이벤트 없음) |
| 컨텍스트 압축 전후 | PreCompact, PostCompact | (현재 별도 이벤트 없음) |
| 파일·디렉터리·설정 변경 | FileChanged, CwdChanged, ConfigChange 등 | (현재 별도 이벤트 없음) |

Codex는 위 표의 6개 이벤트(SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Stop)를 노출하며, `codex features list`에서 `hooks` flag가 `stable, true`로 확인되어 일반 지원 상태입니다. 
Claude Code는 이보다 훨씬 많은 이벤트를 라이프사이클 곳곳에 노출합니다. 

## 이러한 훅 비대칭이 우리 설계에 미치는 영향

같은 규칙을 두 도구에서 똑같은 자리에 걸 수 없을 수 있습니다. 예를 들어 "컨텍스트 압축 직후 프로젝트 정책을 다시 주입"하는 일은 Claude Code에서는 `PostCompact` 훅으로 처리할 수 있지만 Codex에서는 같은 이벤트가 없어 `SessionStart` 시점의 재주입으로 대체합니다. 서브에이전트 라이프사이클을 가로채는 일도 현재 Claude Code 쪽에서만 가능합니다.

그래서 우리 실습 레포는 같은 정책을 세 곳에 둡니다. 

**공통 스크립트(`scripts/`) + 도구별 훅 설정(`.claude/`, `.codex/`) + CI(`.github/workflows/`)**. 
이벤트 비대칭으로 빠지는 부분을 다른 자리에서 메우기 위해서입니다. 

## 하네스의 3계층 구조

하네스를 크게 3계층으로 분류합니다.

- **Layer 1 — 훅**: 시스템 라이프사이클 이벤트에 끼우는 셸 스크립트, HTTP/MCP 호출, LLM 판단. 도구마다 지원 범위가 다릅니다.
- **Layer 2 — 프롬프트/문서**: CLAUDE.md, AGENTS.md, 스킬 같은 컨벤션 자산.
- **Layer 3 — 에이전트**: 권한 제어와 역할 정의 전체를 포괄

**프롬프트로 애매한 부탁은 하지 않는다. 환경으로 구성한 뒤 지속적으로 주입하여 강제한다**

## Claude Code를 쓴다면

Claude Code의 훅은 라이프사이클 곳곳에 풍부하게 자리를 열어 둡니다. 위 비교표의 여러 단계에 훅을 걸 수 있고, handler 종류도 `command`(셸 명령) 외에 `prompt`(모델에게 짧은 결정 묻기), `agent`(서브에이전트로 검증), HTTP, MCP tool까지 다양합니다. 단, `agent` hook은 실험적 기능이므로 운영 안정성이 중요하면 `command` hook부터 시작하세요. 비개발자에게는 "AI가 행동하기 전후에 자동 체크리스트를 돌리는 기능"으로 이해시키되, 그 체크리스트가 사실은 라이프사이클 어느 지점에 끼우는 코드라는 점을 한 번은 짚어주세요.

처음에는 차단보다 알림과 요약부터 시작하는 편이 안전합니다.

## Codex를 쓴다면

Codex의 훅은 6개 이벤트(SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Stop)를 중심으로 작동하며, `codex features list`에서 `hooks` flag가 `stable, true`로 확인됩니다. 현재 실제 실행되는 handler는 `command` 타입이고, `prompt`와 `agent` 타입은 파싱되지만 실행은 건너뜁니다. PreToolUse는 Bash, apply_patch(파일 편집), MCP 도구 호출까지 가로챕니다 — 단 모든 셸 호출이 잡히는 것은 아니며 WebSearch 같은 non-shell/non-MCP 호출은 가로채지 않습니다.

Rules는 sandbox 밖 명령 실행을 allow / prompt / forbidden으로 제어하는 별도 규칙입니다.
Hooks와 Rules는 강한 운영 제어면이지만, 운영 권한 전체를 맡기는 완전한 보안 경계로 과장하면 안 됩니다.

## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| 모든 규칙을 훅으로 만들기 | **문서, 스킬, 훅, 승인으로 나누기** |
| "항상 조심해"를 안전장치로 믿기 | 위험 작업은 실행 전 정책으로 분류 |
| 훅을 완전한 보안 장치로 설명 | 자동 확인 장치와 보안 경계를 구분 |
| 실패 시 행동을 정하지 않기 | 실패하면 로그 요약 후 멈추게 하기 |

## Reference

- 공식 (Claude Code): [Hooks](https://code.claude.com/docs/en/hooks)
- 공식 (Codex): [Hooks](https://developers.openai.com/codex/hooks)
- 공식 (Codex): [Rules](https://developers.openai.com/codex/rules)

## 실습 내용 소개

실습 레포 위치: `part4/lab/.claude/settings.json`, `part4/lab/.codex/hooks.json`, `part4/lab/.codex/config.toml`

### 같은 정책을 두 도구에 나란히 설정.

같은 정책(Stop 시 verify 실행)이 두 설정 파일에서 어떻게 표현되는지 나란히 띄워 봅니다.

```json
// .claude/settings.json (Claude Code)
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "python ${CLAUDE_PROJECT_DIR}/scripts/stop_verify_hook.py"
      }]
    }]
  }
}
```

```json
// .codex/hooks.json (Codex)
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "python \"$(git rev-parse --show-toplevel)/scripts/stop_verify_hook.py\""
      }]
    }]
  }
}
```

두 도구 모두 같은 Stop 이벤트에 훅 래퍼를 연결하고, 래퍼가 내부에서 같은 `agent_verify.sh`를 호출합니다.
설정 파일 위치, 이벤트 스키마, 환경변수 표기는 다르지만 **"라이프사이클에 코드를 끼워 에이전트 루프에 개입한다"는 메커니즘은 같습니다.**

### handler 종류 차이가 만드는 격차

Claude Code는 `command` 외에 `http`, `mcp_tool`, `prompt`(짧은 모델 평가), `agent`(서브에이전트 검증)를 지원합니다. "코드도 프롬프트다"는 말이 들어맞는 자리가 바로 `prompt`/`agent` 핸들러입니다 — 셸 스크립트가 아니라 모델이 직접 결정 규칙을 평가할 수 있습니다. 다만 운영용 기본값은 재현 가능한 `command` hook으로 두는 편이 안전합니다.

```json
// .claude/settings.json (prompt 핸들러 개념 예시)
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Did the last turn run tests AND lint AND typecheck? Reply {\"ok\": true} only if all three are true. Otherwise reply {\"ok\": false, \"reason\": \"what remains\"}."
      }]
    }]
  }
}
```

Codex에서는 같은 결정 규칙을 짧은 셸 스크립트로 표현해야 합니다.
`prompt`/`agent` handler는 파싱되지만 실행되지 않기 때문입니다.
양쪽 모두 무한 루프 방지를 위해 Stop 훅 입력의 `stop_hook_active` 같은 필드를 확인해야 합니다.

### Codex 환경 확인 명령

훅 활성 상태와 단계는 CLI 한 줄로 확인할 수 있습니다.

```bash
codex features list | grep -E '^(hooks|plugin_hooks)\b'
# hooks         stable             true
# plugin_hooks  under development  false
```

`hooks`가 `stable, true`라면 별도 활성화 없이 `.codex/hooks.json` 또는 `.codex/config.toml`의 `[hooks]` 섹션이 그대로 동작합니다. 다만 프로젝트 훅은 레포 루트의 `.codex/` 계층에서 로드되고, 새 명령 훅은 `/hooks`에서 신뢰해야 실행됩니다. 강의 시점에 이 출력이 달라졌다면(예: `experimental`로 회귀), 같은 자리에서 정정해 주세요.
