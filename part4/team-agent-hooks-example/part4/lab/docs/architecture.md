# Hook Architecture

## 구성 목표

한 파일에 모든 규칙을 넣지 않고, 문서, 스킬, 훅, 정책, 사람 승인을 분리합니다. 규칙은 사람이 이해할 수 있어야 하고, 훅은 반복 가능한 결정을 실행해야 하며, CI와 Rulesets는 로컬 우회를 다시 잡아야 합니다.

## 파일 구조

```text
CLAUDE.md                       # Claude Code 공통 지침
AGENTS.md                       # Codex 공통 지침
docs/team-agent-policy.md       # 사람과 Agent의 운영 계약
docs/architecture.md            # 훅/정책/CI 연결 구조
docs/api-contract.md            # 공개 동작 계약
policy/agent-policy.json        # 기계가 읽는 정책
scripts/risky_command_policy.py # PreToolUse / PermissionRequest 정책 엔진
scripts/post_file_change_hook.py# 파일 변경 후 빠른 검사
scripts/pre_commit_guard.py     # git commit 전 검증
scripts/pre_pr_guard.py         # PR 생성/merge 전 검증
scripts/stop_verify_hook.py     # Agent 종료 전 공통 검증
scripts/agent_verify.sh         # 로컬·훅·CI 단일 검증 진입점
scripts/changed_docs_check.py   # 코드/정책 변경과 문서 동기화 확인
.claude/settings.json           # Claude Code 프로젝트 훅/권한
.codex/hooks.json               # Codex 프로젝트 훅
.codex/rules/default.rules      # Codex sandbox 밖 명령 승인 규칙
.github/workflows/verify.yml    # required status check
.github/RULESETS.md             # GitHub Rulesets 적용 가이드
```

## 이벤트 매핑

| 단계 | Claude Code | Codex | 공통 스크립트 |
|---|---|---|---|
| 작업 시작 전 | `SessionStart`, `UserPromptSubmit` | `SessionStart`, `UserPromptSubmit` | `session_context_hook.py`, `user_prompt_guard.py` |
| 실행 전 위험 검사 | `PreToolUse`, `PermissionRequest` | `PreToolUse`, `PermissionRequest` | `risky_command_policy.py` |
| 파일 변경 후 | `PostToolUse` on `Write/Edit/MultiEdit` | `PostToolUse` on `apply_patch/Edit/Write` | `post_file_change_hook.py` |
| 커밋 전 | `PreToolUse` on `Bash(git commit*)` | `PreToolUse` on `Bash` and script self-filter | `pre_commit_guard.py` |
| PR 전 | `PreToolUse` on `Bash(gh pr create*)` | `PreToolUse` on `Bash` and script self-filter | `pre_pr_guard.py` |
| 종료 전 | `Stop` | `Stop` | `stop_verify_hook.py` |
| 최종 게이트 | GitHub Actions + Rulesets | GitHub Actions + Rulesets | `agent_verify.sh` |

## Claude Code와 Codex의 차이

- Claude Code `PreToolUse`는 `allow`, `deny`, `ask`, `defer`를 표현할 수 있습니다.
- Codex `PreToolUse`는 운영상 `deny` 중심으로 사용하고, 승인 요청은 Codex Rules와 `PermissionRequest`에 맡깁니다.
- 따라서 `risky_command_policy.py`는 같은 정책을 읽지만 `--runtime claude|codex`에 따라 출력 형식만 조정합니다.

## 실패 행동

- protected path 또는 금지 명령: 실행 전 차단합니다.
- governed path: Claude Code는 `ask`, Codex는 context를 추가하고 Rules/CI/CODEOWNERS에서 다시 확인합니다.
- 파일 변경 후 구문 실패: `PostToolUse`에서 block feedback을 주어 Agent가 바로 고치게 합니다.
- Stop 검증 실패: `Stop` hook이 한 번 더 작업을 이어가게 합니다. `stop_hook_active`가 true이면 루프 방지를 위해 추가 차단하지 않습니다.
- CI 실패: merge 불가. Rulesets에서 `verify` status check를 required로 둡니다.
