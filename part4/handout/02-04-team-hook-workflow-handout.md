# Session 2-4 - 팀 개발 규칙을 자동화하는 훅 기반 워크플로우

> 팀 규칙은 문서, 스킬, 훅, 정책, 사람 승인으로 나누어 배치해야 오래 갑니다.

- 팀 규칙을 작업 시작 전, 파일 변경 후, 커밋 전, PR 전으로 나눕니다.
- 안내는 문서, 반복 절차는 스킬, 실행 전후 검사는 훅으로 배치합니다.
- 처음부터 완전 자동화하지 않고 제안, 알림, 일부 자동 실행 순서로 도입합니다.
- Agent OS 관점에서 AI Agent가 코드를 작성하게 두고, 사람은 정책·승인·검증 증거와 Agent 산출물 리뷰 기준을 설계합니다.

## 진행 흐름

1. 팀 규칙이 1개의 파일에 몰릴 때 생기는 유지보수 문제를 설명합니다.
2. 문서, 스킬, 훅, 정책, 사람 승인의 역할을 구분합니다.
3. 작업 시작 전, 파일 변경 후, 커밋 전, PR 전 단계 등 구체적인 워크플로우를 나눕니다.
4. Agent OS에서 사람과 AI Agent의 역할을 나눕니다 
 > Agent는 코드 작성·수정·검증 실행, 사람은 목표·금지선·승인 기준·증거 확인·산출물 리뷰.

## Claude Code를 쓴다면

Claude Code에서는 `CLAUDE.md`, Skills, Hooks, Settings가 서로 다른 역할을 맡습니다. `CLAUDE.md`에는 팀의 기본 작업 방식, Skills에는 반복 업무 절차, Hooks에는 자동 확인 절차, Settings에는 권한과 도구 설정을 둡니다.

한 파일에 모든 규칙을 넣으면 처음에는 편하지만 나중에 유지보수가 어려워집니다.

## Codex를 쓴다면

Codex에서는 `AGENTS.md`, Skills, Hooks, Rules를 함께 설계합니다. `AGENTS.md`는 저장소 공통 지침, Skills는 반복 작업, Hooks는 이벤트 기반 확인, Rules는 sandbox 밖 명령의 허용·승인·차단 기준으로 나누는 방식이 자연스럽습니다.

Codex App을 쓰는 팀은 UI에서 확인 가능한 변경 목록과 CLI 검증 명령을 함께 정리합니다.

## Agent OS 관점에서 사람의 역할

이 세션에서 코드는 사람이 처음부터 직접 작성하는 대상이 아닙니다.
AI Agent가 코드를 만들고 고치며 검증 명령까지 실행합니다. 
사람의 일은 더 앞과 뒤로 이동합니다.

| 사람의 역할 | Agent의 역할 | 남겨야 할 증거 |
|---|---|---|
| 목표와 제외 범위를 정한다 | 구현 후보를 제안한다 | 작업 계획, 제외 범위 |
| 위험 명령의 승인 기준을 정한다 | Python 훅으로 정책을 구현한다 | 허용/승인/차단 표, hook 결과 |
| 완료 기준을 정한다 | 포맷·린트·테스트를 실행한다 | `agent_verify.sh` 결과 |
| PR에서 볼 증거를 정한다 | 변경 diff와 검증 결과를 요약한다 | diff 요약, CI check |

Python 훅 코드를 직접 외워 쓰는 것이 목표는 아니지만, 이 코드는 AI Agent가 만든 실제 운영 산출물이므로 리뷰 대상입니다. 
핵심은 **팀이 어떤 행동을 자동 허용하고 어떤 행동은 멈춰야 하는지**를 정하고, 구현이 그 결정과 맞는지 확인하는 것입니다.

## Python 훅 구현을 리뷰하는 방법

Python 훅 구현은 개발자만 보는 내부 코드가 아닙니다. 
Agent OS 방식에서는 Agent가 작성한 코드가 팀 운영 규칙을 실제로 집행하므로, 사람은 아래 관점으로 구현을 읽습니다.

| 파일 | Agent가 구현한 것 | 사람이 확인할 질문 |
|---|---|---|
| `scripts/risky_command_policy.py` | hook payload를 읽고 위험 패턴이면 deny 결정 반환 | 차단 목록이 팀 정책과 맞는가? 허용해도 되는 명령을 과하게 막지 않는가? |
| `scripts/post_file_change_hook.py` | 파일 변경 뒤 문서 동기화, 포맷, 린트, 빠른 테스트 실행 | 저장할 때마다 돌려도 부담 없는 검사만 들어 있는가? 실패 로그가 사람이 읽을 수 있는가? |
| `scripts/stop_verify_hook.py` | Agent가 멈추기 전에 `agent_verify.sh`를 실행하고 실패 시 계속 작업하게 함 | 무한 루프를 막는 장치가 있는가? 최종 검증 실패가 조용히 묻히지 않는가? |
| `scripts/agent_verify.sh` | 사람·hook·CI가 함께 쓰는 단일 검증 진입점 | 사람이 직접 실행할 수 있는가? CI와 로컬 기준이 같은가? |

비개발 트랙에서는 전체 코드를 한 줄씩 설명하지 않아도 됩니다. 대신 입력, 결정, 실패 시 행동을 확인합니다. 개발자 트랙에서는 정규식, exit code, JSON 출력, subprocess 호출까지 함께 봅니다.

## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| 팀 규칙을 전부 프롬프트에만 쓰기 | 문서, 스킬, 훅, 정책으로 분리 |
| 첫날부터 전부 자동 실행 | 제안과 알림부터 시작 |
| 실패 시 책임자를 정하지 않기 | AI 행동과 사람 확인을 분리 |
| 도구별 설정만 만들고 운영표를 안 만들기 | 단계별 워크플로우 표를 함께 유지 |

## Reference

아래 공식 문서 링크는 촬영일과 강의 운영일에 다시 확인하세요.

- 공식 (Claude Code): [Hooks](https://code.claude.com/docs/en/hooks)
- 공식 (Claude Code): [Settings](https://code.claude.com/docs/en/settings)
- 공식 (Claude Code): [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- 공식 (Codex): [Hooks](https://developers.openai.com/codex/hooks)
- 공식 (Codex): [Rules](https://developers.openai.com/codex/rules)

## 실습

실습 레포 위치: `part4/lab/docs/`, `part4/lab/scripts/`, `part4/lab/.claude/settings.json`, `part4/lab/.codex/hooks.json`, `part4/lab/.github/workflows/verify.yml`

3중 안전망 — 공통 스크립트 한 벌, 도구별 훅 설정 두 벌, CI 한 벌.

```
공통 정책 스크립트
  scripts/risky_command_policy.py
  scripts/post_file_change_hook.py
  scripts/agent_verify.sh
  scripts/stop_verify_hook.py
  scripts/changed_docs_check.py

Claude Code 설정
  .claude/settings.json

Codex 설정
  .codex/hooks.json
  .codex/config.toml

CI 설정
  .github/workflows/verify.yml
```

CI에서는 같은 `agent_verify.sh`를 required status check로 걸어, AI가 만든 PR이든 사람이 만든 PR이든 같은 게이트를 통과하게 합니다. 로컬 PostToolUse 훅에서는 `post_file_change_hook.py`가 저장 직후 빠른 포맷·린트·테스트를 실행하고, Stop 훅에서는 `stop_verify_hook.py`가 `agent_verify.sh`를 호출해 실패 시 에이전트 루프를 한 번 더 이어 가게 합니다. 강의에서는 **GitHub Rulesets** 중심으로 시연합니다(branch protection rule도 같은 옵션을 제공하므로 조직 상황에 맞춰 어느 쪽이든 적용 가능). 우리 `verify.yml`의 `jobs.verify`가 그대로 체크 이름이 되므로 Rulesets 화면에서 같은 문자열로 찾아 required로 켭니다.

같은 자리에서 함께 켜는 6가지 방어 — `Require PR before merging`, `Require status checks to pass`, `Block force pushes`, `Restrict deletions`, `Restrict file paths`(예: `.env`, `secrets/**` 차단), `Require signed commits`(옵션). 자세한 적용 가이드는 `part4/lab/.github/RULESETS.md`를 참고하세요. 챕터 3-2(AI 협업 Git 운영 규칙)에서 본격적으로 다룹니다.

Python 훅 구현 리뷰는 아래 순서로 합니다.

1. 입력: hook payload에서 무엇을 읽는가.
2. 결정: allow, deny, block, 계속 작업 요청을 어떤 조건에서 반환하는가.
3. 실패 행동: stderr, exit code, 로그가 사람이 읽을 수 있는가.
4. 우회 가능성: 로컬 훅으로 못 잡는 경우를 CI와 Rulesets가 다시 잡는가.

비개발 트랙에서는 아래 세 문서를 사람이 읽고 수정할 수 있는 계약서로 다룹니다.

- `docs/team-agent-policy.md` — 사람과 Agent의 역할, 승인 기준
- `docs/architecture.md` — 훅, 스크립트, CI, Rulesets의 연결 구조
- `docs/api-contract.md` — 개발자 트랙에서 코드가 바뀔 때 함께 확인할 공개 동작 계약
