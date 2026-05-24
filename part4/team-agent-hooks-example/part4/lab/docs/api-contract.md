# API Contract

이 파일은 공개 동작 계약을 기록하는 자리입니다. `policy/agent-policy.json`의 `docs_sync_rules`는 `src/api/**`, `app/api/**`, `openapi/**` 같은 공개 API 경로가 바뀌면 이 파일이나 OpenAPI 문서가 함께 변경되었는지 확인합니다.

## 변경 시 확인할 항목

- 엔드포인트, 메서드, 요청/응답 스키마
- 오류 형식
- 인증/권한 요구사항
- 하위 호환성
- 마이그레이션 노트

프로젝트에 실제 API가 없다면 이 파일은 비어 있어도 됩니다. API가 추가되는 순간부터 PR 증거의 일부가 됩니다.
