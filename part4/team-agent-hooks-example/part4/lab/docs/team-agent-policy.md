# Team Agent Policy

이 문서는 사람이 읽고 승인하는 운영 계약입니다. 실제 실행은 `policy/agent-policy.json`, `scripts/*.py`, `.claude/settings.json`, `.codex/hooks.json`, `.codex/rules/default.rules`, `.github/workflows/verify.yml`이 담당합니다.

## 역할 분리

| 영역 | 사람이 소유 | Agent가 수행 | 증거 |
|---|---|---|---|
| 목표·제외 범위 | 목표, 금지선, 완료 기준 확정 | 구현 후보 제안 | 작업 계획, 제외 범위 |
| 위험 명령 | 승인 기준, 예외 승인 | 위험 명령 감지, 차단/승인 요청 | hook 로그, 승인 사유 |
| 변경 검증 | 완료 기준 검토 | 포맷, 구문 검사, 테스트 실행 | `scripts/agent_verify.sh` 결과 |
| PR 리뷰 | 증거와 산출물 리뷰 | diff 요약, 검증 결과 요약 | PR 본문, CI check |

## 관리 레벨

| 관리 대상 | 팀/조직 관리 | 프로젝트 관리 | 개인 관리 |
|---|---|---|---|
| 기본 작업 방식 | 조직 Agent 정책, 보안 정책 | `CLAUDE.md`, `AGENTS.md`, `docs/*.md` | 개인 메모, 개인 프롬프트 |
| 반복 절차 | 공통 Skill 템플릿 | `.claude/skills/**`, `.agents/skills/**` | `~/.claude/skills`, `~/.agents/skills` |
| 훅 실행 | 관리형 settings/requirements, 필수 보안 훅 | `.claude/settings.json`, `.codex/hooks.json` | `.claude/settings.local.json`, `~/.codex/hooks.json` |
| 명령 승인 | 조직 차단 정책 | `.codex/rules/default.rules`, Claude permissions | 개인 allow rule |
| 최종 게이트 | GitHub Rulesets, required CI | `.github/workflows/verify.yml` | 없음 |

## 정책 등급

- `protected`: Agent가 읽거나 수정하면 안 되는 경로와 명령입니다. 예: `.env`, `secrets/**`, private key, root 삭제, pipe-to-shell.
- `governed`: 수정은 가능하지만 사람 리뷰와 증거가 필요한 파일입니다. 예: 훅, 정책, CI, Rulesets, GitHub workflow.
- `approval`: Agent가 바로 실행하지 않고 사람 승인이 필요한 명령입니다. 예: push, publish, deploy, infra apply, PR merge.
- `verify`: Agent가 실행해야 하는 검증입니다. 로컬, Stop hook, CI가 같은 `scripts/agent_verify.sh`를 사용합니다.

## 도입 단계

1. 제안: 훅은 경고와 context 추가만 수행합니다.
2. 알림: 위험 명령, governed file 변경, 검증 누락을 사람에게 보이게 합니다.
3. 일부 자동 실행: 구문 검사와 빠른 검증은 저장 직후 실행합니다.
4. 강제 게이트: protected path, 위험 명령, required CI, Rulesets는 차단합니다.

## 예외 처리

예외는 코드 안에 몰래 넣지 않습니다. PR 본문에 다음을 남깁니다.

- 예외가 필요한 이유
- 대체 수단이 불가능한 이유
- 실행한 명령과 결과
- 승인자
- 되돌리는 방법
