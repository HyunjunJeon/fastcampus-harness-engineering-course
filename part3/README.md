# Part 3 세션별 진행안

이 폴더는 Part 3 강의를 촬영/진행할 때 바로 열어볼 수 있도록 세션 단위로 쪼갠 문서다. 각 세션 파일은 `목표`, `준비물`, `진행 순서`, `데모/실습`, `Windows/WSL 주의`, `산출물`, `완료 기준` 순서로 구성한다.

Part 3는 AI 코딩 에이전트에게 더 많은 일을 맡기는 파트다. 핵심은 도구 기능을 많이 외우는 것이 아니라, 권한과 승인 경계, Git 리뷰 흐름, MCP 연결 범위, 테스트 기반 완료 기준을 함께 설계하는 것이다.

## 전체 흐름

1. 작업을 맡기기 전에 위험도와 승인 경계를 먼저 정한다.
2. AI가 만든 변경은 브랜치, diff, 리뷰, PR 흐름 안에서 검토한다.
3. MCP는 편의 기능이 아니라 외부 도구와 데이터에 접근하는 권한 확장으로 다룬다.
4. 완료 기준은 "된 것 같다"가 아니라 테스트, 린트, 타입체크, 재현 절차 같은 검증 증거로 정한다.
5. 실패했을 때는 다시 시키는 것이 아니라 원인 후보, 확인 명령, 최소 수정으로 디버깅한다.

## 세션 목록

### Chapter 1. 안전하게 작업 맡기기: 권한, 승인, 샌드박스

- [Session 1-1. AI에게 어디까지 맡길 것인가: 승인 정책의 기본](./01-01-delegation-policy.md)
- [Session 1-2. Claude Code 권한과 샌드박스 실전 설정](./01-02-claude-permissions-sandbox.md)
- [Session 1-3. Codex 승인 모드와 작업 공간 접근 범위 이해하기](./01-03-codex-approval-workspace.md)

### Chapter 2. Git 브랜치와 리뷰 흐름에 AI 붙이기

- [Session 2-1. Explore -> Plan -> Implement -> Commit 흐름 만들기](./02-01-explore-plan-implement-commit.md)
- [Session 2-2. 브랜치, diff, 리뷰: AI가 만든 변경을 읽는 법](./02-02-branch-diff-review.md)
- [Session 2-3. PR 생성, 코멘트 반영, 충돌 해결까지 한번에 이어가기](./02-03-pr-comments-conflicts.md)

### Chapter 3. MCP로 외부 도구 연결하기

- [Session 3-1. MCP가 왜 중요한가: AI를 코드 밖으로 꺼내기](./03-01-why-mcp-matters.md)
- [Session 3-2. Claude Code에서 Codex 호출 등 주요 MCP 도구 만들어서 연결 실습](./03-02-build-connect-mcp-tools.md)
- [Session 3-3. Claude Code와 Codex에서 같은 MCP를 재사용하는 법](./03-03-reuse-mcp-between-tools.md)

### Chapter 4. 테스트와 검증 루프 만들기

- [Session 4-1. '된 것 같다'라는 추측은 버리고, 정확한 완료 기준 세우기 (TDD)](./04-01-definition-of-done-tdd.md)
- [Session 4-2. 테스트, 린트, 타입체크를 AI 작업의 기본 검증 루프로 묶기](./04-02-test-lint-typecheck-loop.md)
- [Session 4-3. AI가 틀렸을 때 정확히 고치는 디버깅 질문 패턴](./04-03-debugging-question-patterns.md)

## 촬영 공통 규칙

- 제품 기능명, 설정 키, CLI 옵션은 촬영 당일 공식 문서와 로컬 도움말로 다시 확인한다.
- Claude Code와 Codex를 억지로 1:1 대응시키지 않는다. 같은 운영 문제를 해결하는 서로 다른 제어면으로 설명한다.
- 공식 문서 밖 정보는 검증 후보로만 다루고, 실제 적용 전에는 공식 문서, `/help`, `--help`, 작은 실험으로 재확인한다.
- 위험한 작업은 실서비스 저장소가 아니라 샘플 프로젝트, 읽기 전용 모드, 별도 브랜치에서 먼저 실습한다.
- Windows는 `native Windows`, `WSL2`, `Desktop App`, `CLI` 환경을 분리해 설명한다.

## Part 3 전체 산출물

- 개인 위임 정책표
- AI 작업 브랜치 체크리스트
- MCP 연결 판단 카드
- 검증 루프 템플릿
- 디버깅 질문 템플릿
