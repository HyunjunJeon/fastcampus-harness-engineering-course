# 프로젝트 규칙 (Claude Code 용)

이 파일의 규칙은 모든 작업 요청에 항상 적용됩니다.

## 작업 흐름

1. 변경 계획을 먼저 한국어로 정리합니다.
2. 위험 명령(삭제, 배포, 비밀 파일 접근)은 멈춰서 사람의 승인을 요청합니다.
3. 코드를 바꿨다면 `bash scripts/agent_verify.sh`가 통과해야 작업을 끝낼 수 있습니다.
4. 문서가 영향받는 변경이라면 `docs/api-contract.md` 또는 `docs/architecture.md`를 함께 갱신합니다.
5. 완료 보고는 변경 파일·검증 결과·문서 갱신 여부·남은 위험 4가지를 포함합니다.

## 사용해야 하는 스킬

- 디버깅이 필요할 때는 `workflows/debug-loop/SKILL.md`를 따른다.
- PR/diff 리뷰가 필요할 때는 `workflows/pr-review/SKILL.md`를 따른다.
- 코드 변경 뒤 문서가 영향받았다면 `workflows/doc-sync/SKILL.md`를 따른다.

## 금지

- `git push --force` 또는 보호 브랜치 직접 push.
- `.env`, secret, credential 파일 읽기.
- 광범위한 리팩터링과 무관한 파일 다량 수정.
