# Part 3 시연 자산

Part 3 강의에서 화면에 띄우거나 수강생이 따라 실행할 자산 모음. [../plan.md](../plan.md)의 각 세션이 여기 자산을 가리킨다.

자산은 두 종류로 갈린다.

- **읽고 따라 이야기하는 자산**: 시나리오·양식·시드 질문·패턴 정리. 단일 `.md` 파일.
- **화면에 띄우거나 실행하는 자산**: 설정 파일·코드. 폴더 + 내부 `README.md`.

## 인덱스 (12개 세션 모두 자산 보유)

| 세션 | 자산 | 유형 | 강의 중 사용처 |
| --- | --- | --- | --- |
| 01-01 | [01-01-incident-scenario.md](01-01-incident-scenario.md) | 시나리오 + 양식 | 사고 시연 / 매트릭스 양식 |
| 01-02 | [01-02-claude-code-settings/](01-02-claude-code-settings/) | 설정 + 강도 분기 | `settings.json` 3단계(strict/medium/loose) |
| 01-03 | [01-03-codex-config/](01-03-codex-config/) | 설정 + 모드 분기 | `config.toml` 두 모드 비교 |
| 02-01 | [02-01-epic-workflow-template.md](02-01-epic-workflow-template.md) | 양식 + 정의 | EPIC 4단계 체크리스트 |
| 02-02 | [02-02-diff-traps/](02-02-diff-traps/) | 가짜 diff 예시 4개 | diff 함정 4가지 시연 |
| 02-03 | [02-03-pr-handoff/](02-03-pr-handoff/) | 시나리오 + 양식 | 가짜 충돌 시나리오 + PR 핸드오프 노트 |
| 03-01 | [03-01-mcp-security-patterns.md](03-01-mcp-security-patterns.md) | 패턴 정리 | MCP 보안 위험 패턴 3가지 |
| 03-02 | [03-02-basic-mcp-server/](03-02-basic-mcp-server/) | 실행 코드 + 등록 가이드 | 기본 MCP 서버 생성·클라이언트 연동 시연 |
| 03-03 | [03-03-mcp-shared/](03-03-mcp-shared/) | 등록 가이드 + `.env` 분리 | Codex 등록 + 양쪽 호출 비교 |
| 04-01 | [04-01-done-definition-template.md](04-01-done-definition-template.md) | 양식 + 실패 테스트 예시 | 완료 기준 + 실패하는 테스트 1개 |
| 04-02 | [04-02-hooks-examples/](04-02-hooks-examples/) | 설정 + 언어 분기 | 훅 설정 시연 |
| 04-03 | [04-03-debug-question-seeds.md](04-03-debug-question-seeds.md) | 시드 질문 + 실패 케이스 | 디버깅 카탈로그 시작 |

## 자산 작성 규칙

1. 옵션 키·버전이 자주 변하는 항목은 본문 끝에 "(촬영일 기준 공식 문서 확인)" 표기를 둔다.
2. 코드 자산은 *가능한 한 작게* — 도구 1~2개, 50줄 이내 권장.
3. 시나리오 자산은 강사가 그대로 읽는 *대본*으로 쓰지 말고, *상황과 키 포인트*만 적는다. 강사의 즉흥 여지를 남긴다.
4. 언어 분기(JS/Python 등)가 필요한 자산은 같은 도구의 두 언어 버전을 같은 폴더에 둔다. 강의에서는 *하나만* 시연한다 — 둘 다 보여주면 도구 차이에 시간을 빼앗긴다.
5. 모든 폴더형 자산은 내부 `README.md` 진입점 의무. plan.md에서 자산을 가리킬 때 폴더 README 한 군데만 가리키면 된다.
