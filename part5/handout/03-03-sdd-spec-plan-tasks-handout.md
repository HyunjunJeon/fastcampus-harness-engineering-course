# Session 3-3 - SDD로 Spec / Plan / Tasks 확정하기

SDD는 복잡하게 문서를 많이 쓰는 것이 아니라 agent가 추측하지 못하게 작업의 계획을 고정하도록 하는 방식입니다.

- spec은 무엇과 왜를 적습니다.
- plan은 어떻게, 어떤 파일, 어떤 위험을 적습니다.
- tasks는 실행 가능한 체크리스트로 둡니다.
- acceptance criterion은 task, test, manual QA, eval까지 traceability 표로 연결합니다.
- GitHub Spec-Kit(SDD): https://github.com/github/spec-kit/blob/main/spec-driven.md

---
*SDD**는 GitHub Spec Kit 문맥의 **Specification-Driven Development, 명세 주도 개발**입니다. 한 문장으로 정리하면, **코드를 진실의 원천으로 보지 않고, 명세·계획·계약·테스트를 진실의 원천으로 삼아 코드를 그 산출물로 생성·검증·재생성하는 개발 방식**입니다.

## 1. SDD란 무엇인가

전통적 개발에서는 보통 PRD, 요구사항 문서, 설계 문서가 “코딩 전 참고자료” 역할을 하고, 실제로 시간이 지나면 코드를 중심으로 시스템이 진화합니다. GitHub Spec Kit 문서는 이 관계를 뒤집어, **명세가 코드를 섬기는 것이 아니라 코드가 명세를 섬긴다**고 설명합니다. PRD는 구현 가이드가 아니라 구현을 발생시키는 원천이고, 기술 계획은 코딩을 돕는 부속 문서가 아니라 코드를 산출하는 정밀한 정의가 됩니다. ([GitHub][1])

따라서 SDD의 핵심 명제는 다음입니다.

> **Intent → Specification → Plan → Tasks → Tests/Contracts → Code → Runtime Feedback → Specification**

즉 “코드 먼저”가 아니라 **의도 먼저, 명세 먼저, 검증 먼저**입니다. GitHub 문서는 이를 “specification이 primary artifact이고 code는 특정 언어·프레임워크로 표현된 결과”라고 설명하며, 유지보수도 코드를 직접 고치는 행위라기보다 명세와 구현 계획을 진화시키는 행위로 재정의합니다. ([GitHub][1])

이 점에서 SDD는 단순한 문서화 방법론이 아닙니다. 핵심은 **명세를 실행 가능한 개발 입력으로 만드는 것**입니다. 명세가 충분히 정밀하고, 검증 가능하고, 일관되면 AI 에이전트나 코드 생성 도구가 이를 읽고 계획·작업·테스트·코드를 생성할 수 있습니다. GitHub Spec Kit 문서도 “명세와 구현 계획이 코드를 생성하면 gap은 사라지고 transformation만 남는다”고 표현합니다. ([GitHub][1])

## 2. SDD가 기존 개발과 다른 지점

기존 방식은 대체로 다음 구조입니다.

```text
요구사항 → 설계 → 코드 → 테스트 → 문서 갱신, 보통 누락됨
```

SDD는 다음 구조에 가깝습니다.

```text
명세 → 구현 계획 → 계약/API/데이터모델/테스트 → 작업 단위 → 코드 생성/수정 → 검증 → 명세 갱신
```

차이는 “문서가 있느냐 없느냐”가 아니라 **권위의 위치**입니다. 기존에는 최종 권위가 코드에 있고, 문서는 뒤처지기 쉽습니다. SDD에서는 명세가 최종 권위이고, 코드는 그 명세를 만족하는 한 구현체입니다. 이 때문에 같은 명세에서 성능 우선 구현, 유지보수성 우선 구현, 비용 우선 구현 등 여러 구현 경로를 탐색할 수 있습니다. GitHub 문서도 “같은 명세에서 여러 구현 접근을 생성해 성능·유지보수성·사용자 경험·비용을 탐색한다”는 원칙을 제시합니다. ([GitHub][1])

AI 시대에 이 차이가 중요해진 이유는 LLM이 “마음 읽기”를 못 하기 때문입니다. GitHub Blog는 모호한 프롬프트가 모델에게 수많은 암묵 요구사항을 추측하게 만들며, 명확한 명세·기술 계획·작업 단위가 있어야 무엇을, 어떻게, 어떤 순서로 만들지 알 수 있다고 설명합니다. ([The GitHub Blog][2])

## 3. 어떻게 구현해야 하나

실무적으로는 Spec Kit 같은 도구를 쓰든, 자체 프로세스를 만들든 다음 산출물 체계를 갖춰야 합니다.

### 3.1 프로젝트 헌법을 먼저 만든다

SDD에서는 팀의 불변 원칙을 먼저 정의해야 합니다. 예를 들면 다음과 같습니다.

```text
- 테스트 우선
- 공개 API는 계약 문서와 동기화
- 보안·개인정보 요구사항은 기능 요구사항과 동일한 우선순위
- 불필요한 추상화 금지
- 성능 목표는 수치로 명시
- 모든 요구사항은 추적 가능한 ID를 가진다
```

GitHub Spec Kit도 `/speckit.constitution` 명령으로 프로젝트의 지배 원칙과 개발 가이드라인을 만들고, 이 원칙이 이후 specification, planning, implementation 단계에 참조된다고 설명합니다. ([GitHub][3])

### 3.2 기능 명세는 “WHAT/WHY”에 집중한다

초기 명세는 기술 스택을 정하는 문서가 아니라 **사용자 문제, 목표, 성공 기준, 경계 조건**을 정의하는 문서여야 합니다.

좋은 `spec.md`에는 최소한 다음이 있어야 합니다.

| 항목        | 내용                     |
| --------- | ---------------------- |
| 문제 정의     | 왜 이 기능이 필요한가           |
| 사용자/행위자   | 누가 사용하는가               |
| 사용자 여정    | 어떤 상황에서 어떤 흐름으로 사용하는가  |
| 기능 요구사항   | 시스템이 반드시 해야 하는 것       |
| 비기능 요구사항  | 성능, 보안, 접근성, 감사, 가용성   |
| 수용 기준     | 완료 여부를 판단하는 관찰 가능한 조건  |
| 예외/엣지 케이스 | 실패, 권한 없음, 중복, 동시성, 장애 |
| 제외 범위     | 이번에 만들지 않는 것           |
| 모호성 표시    | 아직 결정되지 않은 사항          |

Spec Kit의 `/speckit.specify`도 “무엇을 만들고 왜 만드는지”를 설명하되, 이 단계에서는 기술 스택에 집중하지 말라고 안내합니다. ([GitHub][3])

### 3.3 모호성을 강제로 드러낸다

SDD에서 가장 중요한 실천 중 하나는 AI가 그럴듯하게 추측하지 못하게 하는 것입니다. GitHub 문서는 템플릿이 `[NEEDS CLARIFICATION]` 같은 표시를 요구해 불명확한 요구를 추측하지 않고 질문으로 남기게 한다고 설명합니다. ([GitHub][1])

예를 들어 나쁜 명세는 이렇습니다.

```text
사용자는 로그인할 수 있어야 한다.
```

SDD식 명세는 최소한 이렇게 바뀌어야 합니다.

```text
FR-001: 사용자는 이메일과 비밀번호로 로그인할 수 있어야 한다.
FR-002: 비밀번호는 최소 12자 이상이어야 한다.
FR-003: 로그인 실패가 5회 연속 발생하면 계정은 15분간 잠긴다.
FR-004: SSO 지원 여부는 [NEEDS CLARIFICATION: OAuth, SAML, 사내 IdP 중 무엇인가?]
AC-001: 유효한 계정으로 로그인하면 2초 이내에 대시보드로 이동한다.
AC-002: 잘못된 비밀번호 입력 시 사용자는 인증 실패 메시지를 본다.
```

핵심은 “문장 수를 늘리는 것”이 아니라 **판정 가능한 조건으로 바꾸는 것**입니다.

### 3.4 기술 계획은 “HOW”를 명시하되 요구사항과 추적 가능해야 한다

`plan.md`에서는 기술 스택, 아키텍처, 데이터 모델, API, 저장소 구조, 외부 의존성, 보안 정책, 배포 전략을 정합니다. 단, 모든 기술 결정은 요구사항과 연결되어야 합니다.

예를 들어:

```text
Decision D-003: Redis를 presence 저장소로 사용한다.
Rationale: FR-012의 실시간 접속 상태 표시와 NFR-004의 500ms 이내 상태 반영을 만족하기 위함.
Linked Requirements: FR-012, NFR-004
Alternatives: PostgreSQL polling, WebSocket in-memory map
Rejected because: 서버 재시작 및 수평 확장 시 상태 일관성 문제가 있음.
```

GitHub Spec Kit의 `/speckit.plan`은 feature requirements, user stories, acceptance criteria를 분석하고, 비즈니스 요구를 기술 아키텍처와 구현 세부사항으로 변환하며, 데이터 모델·API 계약·테스트 시나리오 같은 보조 문서를 생성한다고 설명합니다. ([GitHub][1])

### 3.5 계약과 테스트를 코드보다 먼저 만든다

SDD는 TDD/BDD/Contract-first 개발과 강하게 연결됩니다. 기능 명세에서 바로 다음 산출물이 나와야 합니다.

```text
spec.md
 ├─ contracts/openapi.yaml
 ├─ data-model.md
 ├─ acceptance-scenarios.feature
 ├─ integration-tests/
 ├─ e2e-tests/
 └─ tasks.md
```

GitHub 문서도 domain concepts가 data models가 되고, user stories가 API endpoints가 되며, acceptance scenarios가 tests가 된다고 설명합니다. 또한 테스트 시나리오는 코드 이후가 아니라 명세의 일부로서 구현과 테스트를 함께 생성한다고 봅니다. ([GitHub][1])

이때 테스트는 “나중에 품질 확인”이 아니라 **명세의 실행 가능한 형태**입니다. Cucumber의 BDD 문서도 구체적 예제를 자동화 가능한 방식으로 문서화하고, 이를 executable specification으로 만들어 구현을 가이드한다고 설명합니다. ([cucumber.io][4])

### 3.6 작업 단위는 작고 검증 가능해야 한다

`tasks.md`는 “인증 구현” 같은 큰 항목이 아니라, 독립적으로 구현·검토·테스트 가능한 단위여야 합니다.

나쁜 작업:

```text
인증 기능 구현
```

좋은 작업:

```text
T-001: users 테이블에 email, password_hash, locked_until 필드를 추가한다.
T-002: POST /auth/login 계약 테스트를 작성한다.
T-003: 잘못된 비밀번호 5회 입력 시 locked_until이 설정되는 통합 테스트를 작성한다.
T-004: 로그인 성공 시 session token을 발급하는 서비스를 구현한다.
T-005: 잠긴 계정으로 로그인 시 423 Locked 응답을 반환한다.
```

Spec Kit의 `/speckit.tasks`는 plan과 data model, contracts, research 문서를 읽어 구체적인 작업으로 변환하고, 독립 작업에는 병렬화 표시를 붙이며, feature directory에 `tasks.md`를 만든다고 설명합니다. ([GitHub][1])

### 3.7 구현은 명세 검증 루프 안에서 진행한다

구현 단계에서는 AI 에이전트든 인간 개발자든 다음 순서를 지켜야 합니다.

```text
1. 관련 spec/plan/contracts/tasks를 읽는다.
2. 실패하는 테스트 또는 계약 검증을 먼저 만든다.
3. 최소 구현으로 통과시킨다.
4. 리팩터링한다.
5. 명세와 구현의 차이를 분석한다.
6. 차이가 있으면 코드가 아니라 명세 또는 계획도 함께 수정한다.
```

이 흐름은 TDD의 red-green-refactor와 맞닿아 있습니다. Martin Fowler는 TDD를 테스트 작성, 테스트를 통과하는 기능 코드 작성, 리팩터링의 반복으로 설명하며, 테스트를 먼저 생각하는 것이 인터페이스와 구현의 분리를 돕는다고 말합니다. ([martinfowler.com][5])

Spec Kit의 현재 README도 `/speckit.implement`가 constitution, spec, plan, tasks 전제조건을 확인하고, `tasks.md`를 파싱해 의존성과 병렬화 표시를 존중하며 작업을 실행한다고 설명합니다. ([GitHub][3])

### 3.8 운영 피드백을 명세로 되돌린다

SDD는 릴리스에서 끝나지 않습니다. 운영 중 발견한 성능 병목, 보안 취약점, 장애, 사용자 행동 데이터가 다음 명세의 입력이 되어야 합니다.

예를 들어 장애가 발생했다면 단순히 hotfix만 하는 것이 아니라 다음처럼 명세를 바꿔야 합니다.

```text
NFR-009: 주문 생성 API는 결제 게이트웨이 타임아웃 발생 시 idempotency key 기준으로 중복 주문을 생성하지 않아야 한다.
AC-014: 동일 idempotency key로 3회 재시도해도 주문 레코드는 1개만 생성된다.
```

GitHub 문서도 production metrics와 incidents가 hotfix만 유발하는 것이 아니라, 다음 regeneration을 위한 specification update가 되어야 한다고 설명합니다. ([GitHub][1])

## 4. SDD의 본질은 어떤 소프트웨어 공학 이론에 근간하는가

SDD는 완전히 새로운 이론이라기보다, 오래된 소프트웨어 공학 이론들을 **AI 시대에 재조합한 방법론**에 가깝습니다.

### 4.1 요구공학: Requirements Engineering

가장 큰 뿌리는 요구공학입니다. ISO/IEC/IEEE 29148:2018은 시스템·소프트웨어 생명주기 전반에서 요구사항을 산출하는 엔지니어링 활동, 요구사항 프로세스, 요구사항 정보 항목과 형식을 다룹니다. ISO 페이지도 이 표준이 요구사항을 만드는 엔지니어링 활동의 필수 프로세스와 요구사항 관련 산출물의 내용·형식을 규정한다고 설명합니다. ([ISO][6])

SDD는 요구공학의 전통적 목표인 **명확성, 완전성, 검증 가능성, 추적성**을 AI 코드 생성의 입력 조건으로 끌어올린 것입니다. 즉 “좋은 요구사항을 쓰자”에서 멈추지 않고, “좋은 요구사항이 코드·테스트·계약을 산출하게 하자”로 확장합니다.

### 4.2 모델 주도 공학: MDE/MDA

두 번째 뿌리는 Model-Driven Engineering, 특히 OMG의 Model Driven Architecture입니다. OMG는 MDA가 모델로 표현된 소프트웨어 명세를 구조화하는 가이드라인을 제공하고, 비즈니스·애플리케이션 로직을 플랫폼 기술과 분리한다고 설명합니다. 플랫폼 독립 모델은 비즈니스 기능과 행위를 기술 코드와 분리해 문서화하고, 다양한 플랫폼에서 실현될 수 있습니다. ([OMG][7])

SDD도 동일한 철학을 갖습니다.

```text
MDA: Platform-independent model → Platform-specific model → Code
SDD: Product/behavior spec → Technical plan/contracts/tasks → Code
```

차이는 MDA가 UML, MOF, 모델 변환 언어 같은 형식적 모델 생태계에 기반했다면, 현대 SDD는 자연어 명세, 템플릿, AI 에이전트, 코드 생성, 테스트 생성, 리포지토리 워크플로를 결합한다는 점입니다.

### 4.3 형식 명세와 정련: Formal Specification & Refinement

세 번째 뿌리는 형식 명세입니다. 형식 명세의 본질은 “시스템이 무엇을 만족해야 하는지”를 수학적·논리적으로 명확히 쓰고, 구현이 이를 만족하는지 검증하는 것입니다. Leslie Lamport는 TLA+를 프로그램과 시스템, 특히 동시성·분산 시스템을 모델링하기 위한 고수준 언어라고 설명하며, 정확한 설명에는 단순한 수학이 유용하고, TLA+ 도구는 코드에서 찾기 어렵고 수정 비용이 큰 설계 오류를 제거하는 데 유용하다고 설명합니다. ([lamport.azurewebsites.net][8])

SDD는 보통 TLA+만큼 엄격한 수학적 형식성을 요구하지는 않습니다. 그러나 본질은 같습니다.

```text
명세가 먼저 있고,
구현은 명세의 정련(refinement)이며,
검증은 구현이 명세를 만족하는지 확인하는 과정이다.
```

고신뢰 시스템에서는 SDD의 일부 요구사항을 TLA+, Alloy, state machine, temporal logic, property-based testing으로 끌어올릴 수 있습니다. Alloy도 소프트웨어 모델링을 위한 오픈소스 언어와 분석기로 소개되며, 보안 메커니즘 결함 탐지부터 시스템 설계까지 사용됩니다. ([alloytools.org][9])

### 4.4 계약 기반 설계: Design by Contract

네 번째 뿌리는 Design by Contract입니다. Eiffel Software는 Design by Contract를 각 컴포넌트의 기대 행위를 명시적으로 정의·검사·강제하는 방법으로 설명하며, 핵심 구성요소를 preconditions, postconditions, invariants로 설명합니다. ([eiffel.com][10])

SDD에서 API contract, acceptance criteria, invariant, non-functional requirement는 모두 넓은 의미의 계약입니다.

```text
Precondition: 호출 전에 무엇이 참이어야 하는가
Postcondition: 호출 후 무엇이 보장되어야 하는가
Invariant: 시스템 생명주기 동안 무엇이 항상 유지되어야 하는가
```

예를 들어 결제 시스템의 SDD 명세에는 다음과 같은 계약이 들어가야 합니다.

```text
Invariant: 하나의 payment_id는 최대 하나의 성공 결제 상태만 가질 수 있다.
Precondition: capture 요청은 authorized 상태의 payment에 대해서만 가능하다.
Postcondition: capture 성공 후 payment 상태는 captured이며 captured_at이 기록된다.
```

이런 계약은 테스트, 런타임 assertion, API schema, DB constraint, 모니터링 rule로 내려갈 수 있습니다.

### 4.5 TDD, BDD, ATDD, Specification by Example

다섯 번째 뿌리는 테스트 주도·행위 주도 개발입니다. BDD는 사용자 관점의 구체적 예제를 통해 기대 행위를 발견하고, 그 예제를 자동화 가능한 문서로 만들며, 구현을 그 예제가 이끄는 방식입니다. Cucumber 문서는 BDD에서 예제를 자동화 가능한 방식으로 문서화하고, executable specification을 작성해 공유 언어를 만들며 구현을 가이드한다고 설명합니다. ([cucumber.io][4])

SDD는 BDD보다 넓습니다. BDD가 주로 “행위 예제”에 초점을 둔다면, SDD는 다음까지 포함합니다.

```text
- 제품 의도
- 사용자 여정
- 기능 요구사항
- 비기능 요구사항
- 도메인 모델
- API 계약
- 아키텍처 결정
- 작업 분해
- 테스트
- 운영 피드백
```

즉 BDD/ATDD는 SDD 안의 중요한 실행·검증 계층입니다.

### 4.6 애자일과 지속적 피드백

마지막 뿌리는 애자일의 변화 수용과 짧은 피드백 루프입니다. Agile Manifesto 원칙은 늦은 요구사항 변경도 환영하고, 작동하는 소프트웨어를 자주 전달하며, 작동하는 소프트웨어를 진척의 주요 척도로 본다고 말합니다. ([Agile Manifesto][11])

SDD는 애자일을 부정하지 않습니다. 오히려 애자일의 “변화 수용”을 더 체계화합니다. 단, 차이는 있습니다. 애자일이 “작동하는 소프트웨어”를 중심 척도로 삼았다면, SDD는 **작동하는 소프트웨어와 그 소프트웨어를 생성·검증하는 명세의 동기화**를 중심에 둡니다.

## 5. 실무 적용 수준

조직의 성숙도에 따라 SDD는 세 단계로 적용할 수 있습니다.

| 수준                      | 설명                                                | 적합한 상황                         |
| ----------------------- | ------------------------------------------------- | ------------------------------ |
| Level 1: Spec-first     | 코드 전에 명세·수용 기준·계획을 작성하고 사람이 구현                    | 작은 팀, 초기 도입                    |
| Level 2: Spec-anchored  | OpenAPI, Gherkin, 테스트, 데이터 모델 등 실행 가능한 계약을 명세와 연결 | API, SaaS, 엔터프라이즈 기능 개발        |
| Level 3: Spec-as-source | 명세 변경이 계획·작업·테스트·코드 재생성을 유도                       | AI 에이전트 적극 활용, 대규모 제품, 레거시 현대화 |

대부분의 팀은 Level 2부터 시작하는 것이 현실적입니다. 모든 코드를 매번 재생성하려고 하면 위험하지만, API 계약·테스트·작업 단위·수용 기준을 명세에서 파생시키는 것은 즉시 효과가 있습니다.

## 6. SDD 도입 시 흔한 실패

SDD는 명세를 많이 쓰면 성공하는 방법론이 아닙니다. 실패 패턴은 대체로 다음입니다.

첫째, **명세가 추상적 소망에 머무는 경우**입니다. “빠르게 동작해야 한다”는 명세가 아니라 “p95 응답시간 300ms 이하”처럼 판정 가능해야 합니다.

둘째, **명세와 코드가 다시 분리되는 경우**입니다. 코드가 바뀌었는데 spec, plan, contract, tests가 바뀌지 않으면 SDD는 곧 전통적 문서화로 퇴화합니다.

셋째, **AI에게 명세 없이 구현을 맡기는 경우**입니다. 이는 SDD가 아니라 고급 autocomplete입니다.

넷째, **기술 계획이 요구사항과 추적되지 않는 경우**입니다. 기술 선택의 이유가 요구사항 ID와 연결되지 않으면 나중에 변경 영향 분석이 불가능합니다.

다섯째, **운영 피드백이 명세로 돌아오지 않는 경우**입니다. 장애 대응이 hotfix로만 끝나면 다음 생성·수정 사이클에서 같은 문제가 반복됩니다.

## 7. 결론

SDD의 본질은 **“소프트웨어 개발의 중심 산출물을 코드에서 명세로 이동시키는 것”**입니다. 하지만 이 말은 코드가 덜 중요하다는 뜻이 아닙니다. 오히려 코드를 더 엄밀하게 만들기 위해, 코드 이전의 의도·요구·계약·검증 기준을 더 정밀하게 다루자는 뜻입니다.

가장 정확한 정의는 다음입니다.

> **SDD는 요구공학, 모델 주도 공학, 형식 명세, 계약 기반 설계, TDD/BDD, 애자일 피드백 루프를 AI 코드 생성 시대에 맞게 통합한 개발 방법론이다. 명세를 사람이 읽는 문서가 아니라, 계획·테스트·계약·코드를 생성하고 검증하는 실행 가능한 원천으로 취급한다.**

[1]: https://github.com/github/spec-kit/blob/main/spec-driven.md "spec-kit/spec-driven.md at main · github/spec-kit · GitHub"
[2]: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ "Spec-driven development with AI: Get started with a new open source toolkit - The GitHub Blog"
[3]: https://github.com/github/spec-kit "GitHub - github/spec-kit:  Toolkit to help you get started with Spec-Driven Development · GitHub"
[4]: https://cucumber.io/docs/bdd/ "Behaviour-Driven Development | Cucumber"
[5]: https://www.martinfowler.com/bliki/TestDrivenDevelopment.html "Test Driven Development"
[6]: https://www.iso.org/standard/72089.html " ISO/IEC/IEEE 29148:2018 - Systems and software engineering — Life cycle processes — Requirements engineering"
[7]: https://www.omg.org/mda/ "Model Driven Architecture (MDA) | Object Management Group"
[8]: https://lamport.azurewebsites.net/tla/tla.html "My TLA+ Home Page"
[9]: https://alloytools.org/ "alloytools.org"
[10]: https://www.eiffel.com/values/design-by-contract/ "Design by Contract™ - Eiffel Software - The Home of EiffelStudio"
[11]: https://agilemanifesto.org/principles.html "Principles behind the Agile Manifesto"
