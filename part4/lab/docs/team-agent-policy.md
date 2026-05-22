# Team Agent Policy

이 문서는 한 Git 저장소에서 사람과 AI Agent가 함께 일할 때의 운영 기준입니다. 코드는 Agent가 작성할 수 있지만, 목표와 금지선과 승인 기준은 사람이 정합니다. Agent가 작성한 Python 훅 구현도 운영 산출물이므로 리뷰 대상입니다.

## 역할 분리

| 영역 | 사람이 정한다 | Agent가 수행한다 | 증거 |
|---|---|---|---|
| 작업 시작 | 목표, 제외 범위, 완료 기준 | 변경 계획 작성 | 작업 계획 요약 |
| 파일 변경 | 승인된 범위 | 코드·문서 수정, diff 요약 | Git diff, 변경 파일 목록 |
| 검증 | 통과해야 할 명령 | 검증 명령 실행, 실패 수정 제안 | `agent_verify.sh` 출력 |
| 위험 행동 | 허용/승인/차단 기준 | 명령 실행 전 Python 훅으로 정책 확인 | 정책표, hook 결과 |
| PR/merge | 리뷰 기준, required check | PR 설명 초안, 실패 수정 | CI check, 리뷰 코멘트 |
| 훅 구현 | 입력, 결정, 실패 행동의 기대값 | 정책을 코드로 구현 | 시뮬레이션 결과, 코드 리뷰 메모 |

## 명령 정책

| 분류 | 예시 | 기본 행동 | 사람의 판단 기준 |
|---|---|---|---|
| 자동 허용 | `git diff`, `python -m pytest`, `bash scripts/agent_verify.sh --docs-only` | 실행 가능 | 읽기/검증 중심이고 되돌리기 쉬운가 |
| 승인 필요 | `git push`, dependency 설치, 외부 API 호출 | 멈추고 확인 | 저장소 밖에 영향을 주는가 |
| 기본 차단 | `.env` 읽기, 토큰 출력, `rm -rf /`, 보호 브랜치 force push, 운영 배포 | 실행 금지 | 비밀·데이터·운영 환경을 위험하게 하는가 |

## 실습 운영 기준

- 위험 명령은 실제로 실행하지 않고 hook payload로만 시뮬레이션합니다.
- Python 훅 구현은 입력, 결정, 실패 행동 기준으로 리뷰합니다.
- 로컬 hook 결과만으로 완료를 선언하지 않습니다.
- 사람이 직접 실행할 수 있는 검증 명령은 항상 남깁니다.
- PR에서 볼 증거는 "무엇을 바꿨는가", "어떤 검증을 통과했는가", "무엇은 사람이 승인해야 하는가"입니다.

## Python 훅 리뷰 기준

| 질문 | 확인할 파일 | 기대 |
|---|---|---|
| 위험 명령을 실제 실행 전에 막는가 | `scripts/risky_command_policy.py` | deny JSON과 exit code 2가 나온다 |
| 허용 가능한 읽기/검증 명령은 통과하는가 | `scripts/risky_command_policy.py` | allow 결정이 나온다 |
| 파일 변경 뒤 너무 무거운 검사를 돌리지 않는가 | `scripts/post_file_change_hook.py` | 작업 중 검증은 빠른 피드백 중심이다 |
| Agent가 검증 실패를 무시하고 끝내지 않는가 | `scripts/stop_verify_hook.py` | 실패 시 계속 작업하게 만든다 |
| 사람과 CI가 같은 명령을 쓰는가 | `scripts/agent_verify.sh` | 로컬과 CI의 검증 진입점이 같다 |

## 1주일 도입 방식

1. 1-2일차: Agent가 정책 위반 가능성을 보고서로만 남깁니다.
2. 3-4일차: 위험 명령은 `PreToolUse`에서 차단하고, 검증 실패는 Stop hook으로 한 번 더 작업하게 합니다.
3. 5일차 이후: GitHub Rulesets에서 required status check와 보호 브랜치 정책을 켭니다.
