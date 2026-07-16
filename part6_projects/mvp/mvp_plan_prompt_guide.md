# MVP 개발 계획서 생성을 위한 LLM 프롬프트

목표는 단순한 아이디어 설명이 아니라, 개발자가 바로 PRD, SPEC, TASK로 분해할 수 있는 계획서를 얻는 것입니다. 따라서 프롬프트는 기능 목록보다 **운영 루프, 상태 전이, 실패 처리, 보안 불변조건, 화면 범위**를 명확히 요구해야 합니다.

---

## 1. 사용 목적

이 프롬프트는 다음 상황에서 사용합니다.

- 제품 아이디어는 있지만 아직 PRD가 없는 경우
- MVP 범위를 P0/P1/P2로 나눠야 하는 경우
- AI agent, workflow, worker, approval, audit, cost control처럼 상태와 실패 처리가 중요한 제품을 기획하는 경우
- 개발자가 바로 구현 계획으로 옮길 수 있는 계약형 문서가 필요한 경우

이 프롬프트의 출력물은 최종 PRD가 아니라 **PRD 생성 전 계획서**입니다.

---

## 2. 복사용 프롬프트

```markdown
당신은 senior product architect이자 engineering planner입니다.

목표:
아래 제품 아이디어를 바탕으로, PRD를 생성하기 직전 단계의 **MVP 개발 계획서**를 작성하세요.
이 문서는 개발자가 바로 PRD, SPEC, TASK로 분해할 수 있을 만큼 구체적이어야 합니다.

중요한 원칙:
- 특정 기존 제품을 복제하지 마세요.
- 외부 참고 프로젝트명이나 원본 프로젝트명은 문서에 쓰지 마세요.
- 핵심 아이디어만 흡수하고, 우리 제품의 독립적인 MVP 계획으로 작성하세요.
- 기능 목록이 아니라, 실행 가능한 운영 루프와 안전장치를 중심으로 작성하세요.
- 모호한 부분은 합리적으로 가정하되, “가정”이라고 표시하세요.
- P0/P1/P2 범위를 명확히 나누세요.
- P0는 반드시 하나의 핵심 루프가 끝까지 작동하는 것을 목표로 하세요.

제품 아이디어:
[여기에 제품 아이디어를 적으세요]

핵심 워크플로우:
목표 생성
→ 에이전트 등록/고용
→ 이슈 생성/할당
→ heartbeat 실행
→ MCP/context/tool 사용
→ 결과/로그/비용 저장
→ 예산/승인/감사 확인

대상 사용자:
- Primary: single admin / local trusted operator
- Secondary: small team operator, 단 MVP에서는 multi-user/RBAC 제외

기술 제약:
- TypeScript 중심
- Web UI + API
- heartbeat worker는 웹 request handler와 분리
- self-hosted / Docker Compose 우선
- P0는 local trusted mode 기준

반드시 포함할 섹션:

1. 제품 한 줄 정의
2. 설계 원칙
3. MVP 제품 방향
4. Canonical MVP Cut
   - Primary user
   - Primary workflow
   - P0/P1/P2 adapter 범위
   - P0 MCP 범위
   - P0 budget/approval/audit 범위
   - P0 auth actor
5. P0 Golden Path
   - 사용자가 어떤 입력을 넣고
   - 어떤 화면을 지나
   - 어떤 record가 생성되고
   - 어떤 상태로 끝나야 하는지 단계별 작성
6. Canonical State Machines
   - Goal
   - Agent
   - Issue
   - Run
   - Approval
   각 상태 전이는 From / Event / To / Side effect 표로 작성
7. Heartbeat Failure Matrix
   - budget 부족
   - approval 필요
   - MCP 권한 거부
   - MCP 장애
   - adapter timeout
   - adapter schema mismatch
   - worker crash/orphan
   - duplicate running run
   각 실패별 Run status / Issue status / Required records / Retry 기준 작성
8. Security & Governance Invariants
   - budget hard stop
   - approval gate
   - MCP deny-by-default
   - high-risk tool policy
   - secret redaction
   - audit append-only
   - run lock
   - local admin actor
   - adapter boundary
9. 사용자 페르소나
10. 핵심 워크플로우 상세
11. 기능 요구사항
   - Goal Management
   - Agent Registration
   - Issue Management
   - Heartbeat Execution
   - MCP Context Layer
   - Budget & Cost Control
   - Approval Gate
   - Audit Log
12. 화면 요구사항
   - P0 포함 화면과 제외 화면을 분리
13. 데이터 모델 초안
14. API 초안
15. Heartbeat Worker 상세 설계
16. 비기능 요구사항
17. MVP 성공 지표
18. 구현 우선순위
19. Must Have / Should Have / Could Have / Won’t Have
20. 최종 권고
21. 기술 설계 보강 (Implementation-Ready)
    - 인증 & Actor 주입 파이프 (세션 매커니즘, actor 식별 방식)
    - 시크릿 저장소 (암호화 방식, 마스터키 출처, secretRef 포맷)
    - 동시성 잠금 전략 (DB 제약, advisory lock, lease-TTL)
    - 예산 단위/리셋/원자 예약 (통화, 리셋 주기, race condition 방어)
    - Worker ↔ Web 통신 (로그 스트리밍 아키텍처)
    - MCP 자식 프로세스 lifecycle (spawn/재시작/좀비 정리)
    - LLM adapter 범위 확정 (단일 호출 vs agentic loop)
    - 상세 데이터 모델 (핵심 테이블 컬럼 단위 정의)
    - 상태머신 단일 진본 (충돌 없는 하나의 표)
    - Approval self-approval 정책 (single admin 모드에서 의미)

출력 형식:
- 한국어 Markdown
- 표를 적극적으로 사용
- 기능명, 상태명, API path, enum 값은 영어 식별자로 유지
- 추상적인 설명보다 개발자가 바로 구현 판단할 수 있는 계약 중심으로 작성
- “나중에 정하면 됨” 같은 표현 금지
- P0 범위에 없는 기능은 반드시 P1/P2/Out of MVP로 분류
```

---

## 3. 왜 이렇게 물어야 하는가

LLM에게 “MVP 계획을 써줘”라고만 하면 보통 기능 목록과 화면 목록은 잘 나오지만, 개발 착수에 필요한 계약은 빠집니다.

특히 다음 항목이 없으면 PRD 이후 구현 단계에서 해석 차이가 생깁니다.

- 상태가 언제 바뀌는지
- 실패가 어떤 상태로 닫히는지
- 어떤 행동이 승인 전에는 절대 실행되면 안 되는지
- 예산 초과 시 adapter를 호출해도 되는지
- audit event가 누락되어도 mutation을 허용할지
- P0 화면이 어디까지인지

그래서 프롬프트는 기능보다 먼저 아래 여섯 가지를 요구해야 합니다.

```text
Canonical MVP Cut
P0 Golden Path
Canonical State Machines
Heartbeat Failure Matrix
Security & Governance Invariants
P0 Screen Cut
```

이 여섯 가지는 “무엇을 만들 것인가”를 정의합니다. 하지만 MVP 계획서가 여기서 끝나면 **“기획은 끝났는데 구현을 못 시작한다”**는 함정에 빠집니다. 그래서 같은 프롬프트에서 아래 **구현 착수 필수 항목**도 함께 요구해야 합니다 (섹션 2 프롬프트의 21번 섹션).

```text
Secret Store (암호화, 마스터키, secretRef)
Auth & Actor Pipe (세션, actor 주입, CSRF)
Concurrency & Lock (잠금, lease, orphan 복구)
Budget Mechanism (통화, 리셋, 원자 예약)
Worker ↔ Web Streaming (로그 푸시 방식)
MCP Process Lifecycle (spawn, 재시작, 좀비 정리)
LLM Adapter Scope (단일 호출 vs loop)
Detailed Data Model (핵심 테이블 컬럼 정의)
Single Source of Truth State Machine (충돌 없는 표)
Self-Approval Policy (single admin 모드 의미)
```

이 항목들은 “어떻게 만들 것인가”를 정의합니다. 이게 없으면 PRD가 아무리 명확해도 Phase 0 코드 첫 줄을 못 씁니다 (상세는 4.5 체크리스트 참조).

---

## 4. 결과물 검수 체크리스트

LLM이 생성한 문서를 받은 뒤 아래 항목을 확인하도록 개별 세션 서브에이전트를 호출합니다.

| 체크 항목 | 통과 기준 |
| --- | --- |
| P0가 작게 잘렸는가 | 하나의 핵심 운영 루프만 끝까지 검증한다 |
| Golden Path가 있는가 | 샘플 입력, 화면 흐름, 생성 record, 최종 상태가 있다 |
| 상태 전이가 명확한가 | Goal/Agent/Issue/Run/Approval 전이표가 있다 |
| 실패 처리가 닫혀 있는가 | 실패별 Run status, Issue status, audit, retry 기준이 있다 |
| 보안 불변조건이 있는가 | budget, approval, MCP, secret, audit, lock 규칙이 있다 |
| 화면 범위가 과하지 않은가 | P0 포함 화면과 제외 화면이 분리되어 있다 |
| P1/P2가 섞이지 않았는가 | P0 외 기능은 후속 단계로 명확히 내려가 있다 |
| 개발자가 TASK로 쪼갤 수 있는가 | 기능 요구사항, API, 데이터 모델, acceptance criteria가 있다 |

---

## 4.5 구현 착수 전 기술 검수 체크리스트

섹션 4는 “PRD로서 완성되었는가”를 검수합니다. 이 섹션은 한 발 더 나아가 **“이 문서를 보고 바로 코드를 작성할 수 있는가”**를 검수합니다.

기능과 상태 전이가 아무리 명확해도, 아래 항목 중 하나라도 빠지면 Phase 0(skeleton) 코드 첫 줄을 못 씁니다. 각 항목은 “없으면 코딩이 멈추는 이유”를 명시합니다.

> **왜 별도 체크리스트인가?** PRD 검수(섹션 4)는 기획자/PM 관점입니다. 이 체크리스트는 **구현자(engineer) 관점**입니다. 같은 문서를 두 관점에서 두 번 검수해야 “기획은 끝났는데 구현을 못 시작한다”는 함정을 피할 수 있습니다.

| # | 검수 항목 | 통과 기준 | 없으면 코딩이 안 되는 이유 |
| --- | --- | --- | --- |
| 1 | 시크릿 저장소 설계 | 암호화 방식(AES-GCM 등), 마스터키 출처(env), `secretRef` 포맷이 정의됨 | adapter(bearer token, LLM API key) 구현 자체가 불가 |
| 2 | 인증/actor 주입 파이프 | 세션 매커니즘, actor 식별 방식, 모든 mutation에 actor 강제 | audit_events의 actorType/actorId를 채울 수 없음 |
| 3 | 동시성 잠금/lease 전략 | DB 제약(partial unique index), advisory lock, lease-TTL, orphan 복구 | 중복 실행, 데드락, worker crash 후 run이 영구 stuck |
| 4 | 예산 단위/리셋/원자 예약 | 통화(KRW 정수), 리셋 주기(매월 1일 KST), reservation 패턴 | pre-check과 실제 호출 사이 race condition으로 예산 무력화 |
| 5 | LLM adapter 범위 확정 | 단일 호출 vs agentic loop 명시, 토큰 카운트 방식, 실패 처리 | 같은 스펙인데 구현량이 3배 편차 발생 |
| 6 | 로그 스트리밍 아키텍처 | worker↔web push/poll 방식(LISTEN/NOTIFY, Redis 등) 명시 | UI에서 run log를 실시간으로 못 봄 |
| 7 | MCP 자식 프로세스 생명주기 | spawn 단위, 재시작 정책, 좀비 정리, discovery 캐싱 | 프로세스 누수, MCP 서버 다운 시 복구 불가 |
| 8 | 상세 데이터 모델 | goals/issues/runs/audit_events 등 핵심 테이블 컬럼 단위 정의 | 구현자가 FR을 읽고 컬럼을 역추론해야 함 (오류 발생) |
| 9 | 상태머신 단일 진본 | 충돌 없는 하나의 상태표 (같은 entity에 두 표가 없음) | 구현자가 매번 어느 표를 따를지 판단 비용 발생 |
| 10 | 통화 단위 통일 | cents/USD/won 혼용 제거, 모든 필드가 단일 단위 | 예산 비교 로직에서 단위 변환 버그 |
| 11 | Approval self-approval 정책 | single admin 모드에서 approval의 의미 정의 | governance 가치가 자가상쇄되어 의미 없는 기능이 됨 |

### 4.5.1 검수 통과 기준

- **11개 항목 모두 “통과 기준”을 만족**해야 구현 착수 가능
- 1개라도 빠지면 그 항목을 먼저 채운 뒤 Phase 0 진입
- “나중에 정하면 됨”으로 넘긴 항목은 **불가** (이것이 이 체크리스트의 존재 이유)

### 4.5.2 PRD(섹션 4)와의 관계

| 관점 | 체크리스트 | 핵심 질문 |
| --- | --- | --- |
| 기획/PM | 섹션 4 | “무엇을 만들 것인가가 명확한가?” |
| 엔지니어 | 섹션 4.5 | “이걸 보고 오늘 코드를 쓸 수 있는가?” |

PRD가 완벽해 보여도 4.5를 통과 못 하면 “기획 완료, 구현 대기” 상태로 무한정 멈춰 있게 됩니다. 이 함정을 피하려면 두 체크리스트를 **별개로, 순차적으로** 돌려야 합니다.

### 4.5.3 활용 패턴

```text
1. LLM에게 섹션 2 프롬프트로 계획서 생성 (이제 21번 섹션 포함)
2. 섹션 4 체크리스트로 PRD 완성도 검수
3. 빠진 항목이 있으면 LLM에게 보완 요청
4. 섹션 4.5 체크리스트로 구현 착수 준비도 검수
5. 빠진 기술 결정이 있으면 LLM에게 “이 항목을 채워달라”고 후속 프롬프트
6. 두 체크리스트 모두 통과하면 Phase 0 코드 작성 시작
```

이 흐름을 타면 “PRD는 끝났는데 개발이 안 시작된다”는 가장 흔한 MVP 실패 패턴을 피할 수 있습니다.

---

## 5. 사용 팁

제품 아이디어가 아직 모호하다면 프롬프트의 `[여기에 제품 아이디어를 적으세요]` 부분에 다음 네 가지를 함께 넣습니다.

```markdown
문제:
[누가 어떤 문제를 겪는지]

사용자:
[primary user와 secondary user]

핵심 행동:
[사용자가 제품에서 반드시 하게 될 행동]

절대 자동화하면 안 되는 것:
[비용, 권한, 데이터 변경, 배포, secret 사용 등]
```

이 네 가지가 들어가면 LLM이 기능을 과도하게 부풀리지 않고, 제품의 안전한 핵심 루프를 중심으로 계획을 작성할 가능성이 높아집니다.
