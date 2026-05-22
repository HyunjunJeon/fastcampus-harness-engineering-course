# 프로젝트 규칙 (Codex 등 AGENTS.md 활용 에이전트 호환용)

이 파일은 `CLAUDE.md`와 동일한 내용을 Codex 및 AGENTS.md를 읽는 다른 에이전트들이 활용할 수 있도록 미러링한 것입니다. 두 파일이 어긋나면 그 자체로 버그이므로, 변경 시 양쪽을 함께 수정합니다.

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

## Codex 환경 메모

- `codex features list`에서 `hooks` flag가 `stable, true`로 확인되어 별도 활성화 없이 `.codex/hooks.json` 또는 `.codex/config.toml`의 `[hooks]` 섹션이 동작합니다. 실제 환경에서도 똑같이 동작하는지 꼭 확인해야합니다.
- `.codex/hooks.json`의 PreToolUse는 Bash, `apply_patch`(파일 편집), MCP 도구 호출을 가로챕니다. 단 WebSearch 같은 non-shell/non-MCP 호출은 가로채지 않으므로, 같은 정책을 Stop 훅과 CI에서도 다시 강제하는 3중 안전망을 유지합니다.
