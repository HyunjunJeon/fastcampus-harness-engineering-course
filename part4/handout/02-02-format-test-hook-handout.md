# Session 2-2 - 파일 저장 뒤 자동 포맷·테스트 훅 만들기

> 훅을 만드는 첫 목표는 AI가 고친 결과를 사람이 확인하기 쉽게 만드는 것입니다.

## 핵심 내용

- 파일 변경 뒤 확인할 명령을 위험도별로 나눕니다.
- Claude Code와 Codex의 파일 변경 이벤트에 같은 훅 스크립트를 연결합니다.
- 파일 저장 뒤 포맷, 린트, 테스트가 자동으로 도는 것을 확인합니다.
- 실패 시에는 작업 중 훅과 작업 종료 훅의 역할을 나누어 이해합니다.

## 강의 진행 흐름

1. 파일 변경 후 검증을 "작업 후 자동 체크리스트"로 소개합니다.
2. `scripts/post_file_change_hook.py`가 어떤 순서로 포맷·린트·테스트를 실행하는지 봅니다.
3. Claude Code의 `PostToolUse: Edit|Write|MultiEdit`에 훅을 연결합니다.
4. Codex의 `PostToolUse: apply_patch|Edit|Write`에 같은 훅을 연결합니다.
5. 일부러 파일을 수정한 뒤, 자동 포맷과 빠른 테스트가 실행되는지 확인합니다.

## Claude Code를 쓴다면

Claude Code Hooks에서는 파일 변경 후나 작업 종료 시점에 검증 명령을 연결할 수 있습니다. 이 실습에서는 `PostToolUse`에서 파일 편집 도구(`Edit`, `Write`, `MultiEdit`)가 실행된 직후 `post_file_change_hook.py`를 호출합니다.

작업 중에 실행하는 훅은 빠른 피드백용입니다. 
포맷과 짧은 테스트는 여기서 돌리고, 최종 통과 여부는 `Stop` 훅에서 한 번 더 확인합니다.

## Codex를 쓴다면

Codex Hooks에서도 작업 이벤트에 맞춰 확인 명령을 설계할 수 있습니다. 
이 실습에서는 `PostToolUse`에서 `apply_patch`, `Edit`, `Write` 파일 변경 이벤트에 같은 `post_file_change_hook.py`를 연결합니다.

검증 명령은 프로젝트마다 다릅니다. 
이 예제 저장소에서는 `ruff format`, `ruff check`, `python -m pytest -q`를 사용합니다. 
실제 팀에서는 같은 자리에 `npm test`, `pnpm lint`, `git diff --check` 같은 명령을 넣을 수 있습니다.

Codex의 PreToolUse/PostToolUse는 Bash, `apply_patch`(파일 편집), MCP 도구 호출을 모두 가로챕니다. 단 모든 셸 호출이 잡히는 것은 아니며 WebSearch 같은 non-shell/non-MCP 호출은 가로채지 않습니다. 또한 PostToolUse는 이미 실행된 부작용을 되돌리지는 못합니다 — "수정 전 차단"이 필요한 정책은 PreToolUse, "수정 후 보정·검증"은 PostToolUse로 나누어 거는 것이 안전합니다. 강의 시점에 정확한 가로채기 범위는 공식 문서로 다시 확인하세요.

Codex는 레포 루트의 `.codex/` 설정 계층에서 프로젝트 훅을 찾습니다. 이 강의 저장소 전체 안에서 `part4/lab`은 하위 폴더이므로, Codex CLI 실습은 `part4/lab`을 별도 실습 레포로 열거나 복사한 뒤 진행하세요. 처음 실행하면 `/hooks`에서 프로젝트 훅을 검토하고 신뢰해야 실제로 실행됩니다.


## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| 검증 명령을 모르고 자동 실행 | 먼저 명령의 목적과 영향 확인 |
| 큰 테스트 전체를 저장할 때마다 실행 | 저장 후 훅은 빠른 검사, Stop/CI는 전체 검사로 분리 |
| 실패 로그를 덮어쓰기 | 로그를 요약하고 사람 확인 받기 |
| 테스트 성공만 보고 완료 처리 | 문서와 사용법 영향도 함께 확인 |

## 더 알아보기

- 공식 (Claude Code): [Hooks](https://code.claude.com/docs/en/hooks)
- 공식 (Codex): [Hooks](https://developers.openai.com/codex/hooks)

## 실습해보기

실습 레포 위치: `part4/lab/.claude/settings.json`, `part4/lab/.codex/hooks.json`, `part4/lab/scripts/post_file_change_hook.py`, `part4/lab/scripts/agent_verify.sh`, `part4/lab/scripts/stop_verify_hook.py`

파일 변경 직후에는 `post_file_change_hook.py`로 포맷·린트·빠른 테스트를 돌리고, 
진짜 최종 검증은 작업 종료 훅으로 모읍니다.
