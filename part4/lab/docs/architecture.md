# Team Hook Architecture

이 실습 레포의 목표는 한 팀이 하나의 Git 저장소에서 같은 운영 기준을 공유하는 것입니다. 구조는 세 겹입니다.

## 3중 안전망

```text
사람/Agent의 작업
  -> 로컬 hook: 빠른 피드백
  -> 공통 스크립트: 같은 검증과 정책
  -> CI/Rulesets: 공유 Git 저장소의 최종 게이트
```

## 구성 요소

| 계층 | 파일 | 역할 |
|---|---|---|
| 프로젝트 지시문 | `CLAUDE.md`, `AGENTS.md` | 팀의 기본 작업 방식과 금지 행동 |
| 도구별 hook 설정 | `.claude/settings.json`, `.codex/hooks.json` | Claude Code와 Codex가 같은 스크립트를 호출하게 연결 |
| 공통 정책·검증 | `scripts/risky_command_policy.py`, `scripts/agent_verify.sh` | 위험 명령 분류와 최종 검증 |
| 작업 중 빠른 확인 | `scripts/post_file_change_hook.py` | 파일 변경 뒤 포맷·문서 동기화·빠른 테스트 확인 |
| 종료 전 확인 | `scripts/stop_verify_hook.py` | Agent가 끝났다고 말하기 전에 `agent_verify.sh` 실행 |
| 공유 저장소 게이트 | `.github/workflows/verify.yml`, `.github/RULESETS.md` | PR/merge 전에 같은 기준을 다시 강제 |

## 왜 로컬 hook만으로 부족한가

로컬 hook은 Agent 작업 중 빠른 피드백을 줍니다. 하지만 사람이 직접 파일을 수정하거나, 다른 도구를 쓰거나, 훅이 없는 환경에서 작업하면 우회될 수 있습니다. 그래서 같은 규칙을 CI와 GitHub Rulesets에서 다시 확인합니다.

## 비개발 트랙에서 볼 것

- `docs/team-agent-policy.md`: 사람이 결정할 정책과 승인 기준
- `scripts/agent_verify.sh --docs-only`: 문서·스킬 링크 수준의 저위험 검증
- `scripts/risky_command_policy.py`: Agent가 작성한 정책 구현이 입력에 따라 어떤 결정을 내리는지
- `.github/RULESETS.md`: PR merge 전에 사람이 기대할 저장소 정책

## 개발자 트랙에서 추가로 볼 것

- `app/`, `tests/`: Agent가 실제 코드를 바꾸는 대상
- `scripts/post_file_change_hook.py`: 파일 변경 직후 빠른 검증
- `scripts/stop_verify_hook.py`: 검증 실패 시 Agent 루프를 계속하게 하는 종료 훅
- 전체 `bash scripts/agent_verify.sh`: format, lint, typecheck, tests

## Python 훅 구현의 위치

Python 훅은 정책 문서와 도구 설정 사이의 실행 계층입니다.

```text
팀 정책 문서
  -> Python 훅 구현
  -> Claude/Codex hook 설정
  -> Agent 행동 변화
  -> 검증 로그와 CI 결과
```

따라서 Agent가 Python 훅을 작성했다면, 사람은 코드 스타일보다 먼저 입력과 출력 계약을 봅니다. `cat .env` payload가 deny 되는지, `git diff --stat` payload가 allow 되는지, 검증 실패가 조용히 무시되지 않는지가 핵심입니다.
