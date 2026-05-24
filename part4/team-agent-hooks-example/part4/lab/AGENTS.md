# Codex 작업 지침

Agent는 코드 작성·수정·검증 실행을 담당합니다. 사람은 목표, 제외 범위, 위험 명령 승인, 완료 기준, 증거 리뷰를 담당합니다.

## 공통 운영 규칙

- 작업 시작 시 목표와 제외 범위를 짧게 정리합니다.
- 구현 뒤 `bash scripts/agent_verify.sh` 결과를 최종 응답 또는 PR 설명에 포함합니다.
- `.env`, `secrets/**`, `*.pem`, `*.key`는 읽거나 수정하지 않습니다.
- 훅, 정책, CI, Rulesets 관련 파일을 바꿀 때는 변경 이유와 검증 증거를 남깁니다.
- 커밋 또는 PR 전에는 diff 요약, 테스트 결과, 남은 리스크를 정리합니다.

자세한 계약은 `docs/team-agent-policy.md`와 `docs/architecture.md`를 따릅니다.
