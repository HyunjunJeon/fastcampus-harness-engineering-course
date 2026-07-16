# 수강생용 AI Agent MVP 개발 프로세스 키트

## 이 자료의 목적

이 자료는 특정 예제 프로젝트에만 쓰는 문서가 아니다. 
수강생이 자신의 아이디어로 아래 4단계를 그대로 따라 할 수 있게 만든 **범용 실습 키트**다.

1. PRD를 쓰고 MVP 범위를 자른다.
2. ROADMAP과 작업 단위를 SPEC으로 쪼갠다.
3. Claude Code로 화면 골격과 컴포넌트를 만든다.
4. Codex로 잘게 나뉜 구현 작업을 병렬 처리하고 검증한다.

이 수업의 핵심은 

1) 목표를 검증 가능한 형태로 고정하고,
2) AI Agent가 안전하게 일할 수 있는 작업 단위와 검증 장치를 만드는 법이다.

수강생은 실습 전에 **Superpowers**를 설치해야 한다. 
이 수업의 프로세스는 Superpowers의 brainstorming, planning, TDD, subagent-driven development, review, verification 철학과 함께 사용할 때 가장 안정적으로 작동한다.

---

## 1. 전체 흐름 한 장 요약

```text
Superpowers 설치
  - 사용하는 agent harness마다 별도 설치한다.
  - Claude Code / Codex / Cursor 등 실습 도구에 먼저 설치한다.
  ↓
Brainstorming
  - 기본은 Superpowers brainstorming으로 아이디어를 design/spec으로 정리한다.
  - 아이디어가 여전히 모호하면 grill-me-mvp 를 통해 Interview 를 진행한다.
  ↓
아이디어
  ↓
PRD
  - 누구의 어떤 문제인가?
  - 첫 성공 경험은 무엇인가?
  - 완료 증거는 무엇인가?
  ↓
MVP Scope
  - P0에서 반드시 할 것
  - P1/P2로 미룰 것
  - 이번에 하지 않을 것
  ↓
Roadmap
  - 어떤 순서로 만들 것인가?
  - 무엇이 먼저 만들어져야 하는가?
  ↓
SPEC
  - 기능을 구현 가능한 계약으로 쓴다.
  - 화면, 데이터, API, 상태, 실패, 검증을 고정한다.
  ↓
TASK
  - AI Agent 하나가 할 수 있는 작은 작업으로 나눈다.
  - allowed_paths / forbidden_paths / validation을 넣는다.
  ↓
Claude Code
  - 큰 맥락을 읽고 화면 구조와 컴포넌트 경계를 만든다.
  ↓
Codex
  - 작은 TASK를 병렬 구현한다.
  - validation과 evidence를 남긴다.
  ↓
Review
  - 코드가 아니라 증거를 보고 완료 판단한다.
```

---

## 2. 단계 1 — PRD를 쓰고 MVP 범위를 자르기

### 2.1 목표

아이디어를 바로 구현 요청으로 보내지 않고, 먼저 아래 질문에 답한다.

PRD를 작성해달라고 요청하기 전에 Superpowers `brainstorming`을 먼저 사용한다. 답변할수록 사용자, 범위, 성공 기준이 더 흐려지면 `grill-me-mvp` Skill로 더 딥하게 물어보도록 하는 Interview 스킬을 실행해서 요구사항을 더 깊게 정리한다.

```text
누가?
어떤 문제를?
어떤 첫 성공 경험으로?
어떤 증거를 통해 해결됐다고 볼 것인가?
```

### 2.2 좋은 PRD의 기준

좋은 PRD는 길어서 좋은 문서가 아니다. 
**AI가 작업 시 임의 판단으로 범위를 부풀리지 못하게 만드는 문서**가 좋은 PRD다.

| 항목 | 좋은 PRD | 나쁜 PRD |
|---|---|---|
| 문제 | 누가 어떤 상황에서 무엇 때문에 막히는지 구체적 | “편하게 관리하고 싶다” |
| 사용자 | 첫 사용자가 한 명 또는 한 역할로 선명함 | 모든 사람이 쓸 수 있음 |
| 성공 기준 | 사용자가 확인할 수 있는 결과가 있음 | 잘 작동하면 됨 |
| 범위 | P0/P1/P2/Out이 분리됨 | 기능 목록만 많음 |
| 실패 | 실패 시 상태와 메시지가 있음 | 성공 흐름만 있음 |
| 검증 | 화면, 테스트, 기록, evidence가 있음 | 완료되면 알려줘 |

### 2.3 PRD 작성 순서

1. 아이디어를 한 문장으로 쓴다.
2. 사용자를 하나로 좁힌다.
3. 사용자가 처음 성공해야 하는 행동 하나를 고른다.
4. 그 행동이 끝났다는 증거를 정한다.
4. P0에서 하지 않을 것을 적는다.
5. 실패했을 때 어떻게 보여줄지 정한다.
7. AI에게 PRD 초안을 만들게 한다.
8. 사람이 P0/P1/P2/Out을 다시 자른다.

### 2.4 수강생용 PRD 프롬프트

아래를 복사해서 자신의 아이디어로 채운다.

```markdown
당신은 senior product manager이자 MVP scope cutter입니다.

목표:
아래 아이디어를 바탕으로 개발 착수 전 PRD 초안을 작성하세요.
이 PRD는 AI Agent가 구현 작업을 시작하기 전, 목표와 범위를 고정하기 위한 문서입니다.

제품 아이디어:
[내 아이디어를 적으세요]

첫 사용자:
[누가 처음 사용할지 적으세요]

사용자가 처음 성공해야 하는 행동:
[예: 할 일 생성 → 담당자 지정 → 완료 상태 확인]

반드시 남아야 하는 완료 증거:
[예: 화면에서 상태 확인, DB record 생성, 테스트 통과, 로그 저장]

위험하거나 막아야 하는 행동:
[예: 결제, 삭제, 외부 발송, 개인정보 조회, 권한 변경]

반드시 포함할 섹션:
1. 제품 한 줄 정의
2. 문제 정의
3. 첫 사용자
4. P0 Golden Path
4. P0에 포함할 것
5. P1/P2로 미룰 것
7. 이번 MVP에서 하지 않을 것
8. 핵심 화면
9. 저장해야 할 데이터
10. 상태 전이
11. 실패 상황과 사용자 메시지
12. 완료 증거
13. 성공 지표

작성 규칙:
- 추상적인 표현을 피하세요.
- “나중에 정한다”라고 쓰지 마세요.
- P0는 하나의 핵심 흐름이 끝까지 작동하는 것을 기준으로 자르세요.
- 각 요구사항에는 검증 방법을 붙이세요.
```

### 2.5 MVP Scope 자르기 기준

MVP는 기능을 적게 넣는 것이 아니라, **하나의 흐름을 끝까지 닫는 것**이다.

| 분류 | 의미 | 예시 |
|---|---|---|
| P0 | 없으면 첫 성공 흐름이 성립하지 않음 | 로그인, 핵심 생성, 핵심 실행, 결과 확인 |
| P1 | 있으면 좋지만 P0 검증 뒤에 가능 | 알림, 필터, 통계, 자동화 |
| P2 | 확장 기능 | 팀 관리, 고급 권한, 외부 연동 |
| Out | 이번 제품 방향과 맞지 않거나 너무 위험 | 마켓플레이스, 복잡한 AI 자율 실행 |

### 2.6 단계 1 완료 기준

```text
[ ] 제품 한 줄 정의가 있다.
[ ] 첫 사용자가 하나로 좁혀져 있다.
[ ] P0 Golden Path가 있다.
[ ] P0/P1/P2/Out이 분리되어 있다.
[ ] 실패 상황이 최소 3개 이상 있다.
[ ] 완료 증거가 화면/테스트/기록 중 최소 2개 이상으로 정의되어 있다.
```

---

## 3. 단계 2 — ROADMAP과 SPEC, TASK로 쪼개기

### 3.1 목표

PRD는 “무엇을 왜 만들지”를 설명한다. 하지만 AI Agent가 바로 구현하기에는 아직 크다.

그래서 다음 순서로 쪼갠다.

```text
PRD
→ MVP Scope
→ Roadmap
→ SPEC
→ TASK
```

### 3.2 문서별 역할

| 문서 | 역할 | 질문 |
|---|---|---|
| PRD | 왜 만들고 무엇이 성공인지 | 이 제품은 왜 필요한가? |
| MVP Scope | 이번 버전에 할 것/안 할 것 | P0는 어디까지인가? |
| Roadmap | 어떤 순서로 만들지 | 무엇을 먼저 만들어야 하는가? |
| SPEC | 기능을 구현 가능한 계약으로 고정 | 화면/데이터/API/상태/실패는 무엇인가? |
| TASK | AI Agent 하나가 수행할 최소 작업 | 어떤 파일을 바꾸고 어떻게 검증하는가? |

### 3.3 Roadmap 작성 기준

Roadmap은 일정표가 아니라 **의존성 순서표**다.

좋은 Roadmap 예:

| Phase | 목표 | 종료 기준 |
|---:|---|---|
| 0 | 프로젝트 골격 | 앱 실행, lint 통과 |
| 1 | 핵심 데이터와 기본 화면 | 핵심 record 생성 가능 |
| 2 | 핵심 행동 구현 | 사용자가 첫 성공 흐름을 수행 가능 |
| 3 | 실패/권한/검증 | 실패가 상태와 메시지로 닫힘 |
| 4 | 운영 화면과 완료 증거 | 사용자가 결과와 기록을 확인 가능 |

나쁜 Roadmap 예:

```text
1주차: 프론트
2주차: 백엔드
3주차: 테스트
```

왜 나쁜가:

- 사용자 흐름 기준이 아니다.
- 완료 기준이 없다.
- 실패 처리와 검증이 뒤로 밀린다.

### 3.4 SPEC 작성 기준

SPEC은 기능 설명이 아니라 **구현 계약**이다.

SPEC에는 최소한 아래가 있어야 한다.

```text
1. Summary
2. Scope
3. Out of Scope
4. User Flow
4. Screen Contract
5. Data Contract
7. API or Action Contract
8. State Transition
9. Failure Handling
10. Security / Safety Rules
11. Acceptance Criteria
12. Validation Plan
13. Evidence Requirements
```

### 3.5 TASK 작성 기준

TASK는 AI Agent 하나가 수행할 수 있어야 한다.

좋은 TASK는 다음을 가진다.

```text
- 하나의 명확한 결과
- 수정 가능한 파일 목록 allowed_paths
- 수정 금지 파일 목록 forbidden_paths
- acceptance criteria
- validation commands
- expected outputs
```

나쁜 TASK:

```text
대시보드 전체 만들어줘.
```

좋은 TASK:

```text
대시보드에 오늘 생성된 작업 5개를 보여주는 TaskListCard 컴포넌트를 만든다.
API, DB, 인증은 건드리지 않는다.
테스트에서 empty/loading/with-data 상태를 확인한다.
```

### 3.6 단계 2 완료 기준

```text
[ ] Roadmap이 phase별 종료 기준을 가진다.
[ ] SPEC이 화면, 데이터, 상태, 실패, 검증을 포함한다.
[ ] TASK가 AI Agent 하나에게 맡길 만큼 작다.
[ ] 각 TASK에 allowed_paths / forbidden_paths가 있다.
[ ] 각 TASK에 validation command가 있다.
[ ] 병렬 가능한 TASK와 순차 실행할 TASK가 구분되어 있다.
```

---

## 4. 단계 3 — Claude Code로 화면 골격과 컴포넌트 만들기

### 4.1 목표

Claude Code는 전체 맥락을 읽고 구조를 잡는 데 강하다. 그래서 이 단계에서는 **기능 완성**보다 **화면 골격과 컴포넌트 경계**를 만든다.

```text
Claude Code에게 맡길 것:
- 라우트 구조
- 페이지 skeleton
- 컴포넌트 분리
- 상태별 UI
- demo fixture
- 후속 Codex task로 나눌 수 있는 경계
```

```text
Claude Code에게 맡기지 말 것:
- DB schema 변경
- auth 변경
- 결제/배포 설정 변경
- 큰 backend 구현
- package dependency 추가
```

### 4.2 UI Scaffold TASK 예시

```yaml
id: TASK-UI-001
title: "Create core feature UI shell"
spec: SPEC-002-ui-shell
status: ready
risk_level: low
agent_preference: claude
skill: ui-scaffold

allowed_paths:
  - "src/app/[feature]/page.tsx"
  - "src/components/[feature]/**"
  - "src/lib/demo/[feature]-fixtures.ts"
  - "tests/ui/[feature]-shell.test.tsx"

forbidden_paths:
  - "package.json"
  - "src/db/**"
  - "src/app/api/**"
  - "src/auth/**"
  - "src/worker/**"

goal: >
  Create a non-mutating UI shell for the core P0 feature using typed demo fixtures.

acceptance:
  - "Page renders with demo fixture data"
  - "Primary action area is visible"
  - "Loading, empty, error, success, and blocked states are represented"
  - "Component boundaries are clear enough for parallel follow-up tasks"
  - "No API, DB, auth, worker, or package dependency is changed"

validation:
  commands:
    - "npm run lint"
    - "npm run test -- [feature]-shell"
```

### 4.3 Claude Code 프롬프트

```text
You are working inside an AI Agent Harness.

Read:
- docs/01-prd.md
- docs/02-mvp-scope.md
- specs/SPEC-002-ui-shell.md
- tasks/TASK-UI-001.yaml

Implement only TASK-UI-001.

This is UI scaffold work, not backend implementation.
Use typed demo fixtures.
Do not modify API routes, DB schema, auth, worker code, package dependencies, or deployment config.
Represent loading, empty, error, success, blocked, and completed states.
Keep components small enough for later Codex atomic tasks.
Run the validation commands from the TASK.
Report changed files, validation results, acceptance mapping, and remaining risks.
```

### 4.4 단계 3 완료 기준

```text
[ ] 화면 skeleton이 있다.
[ ] 핵심 action 영역이 있다.
[ ] loading/empty/error/success/blocked 상태가 있다.
[ ] demo fixture 또는 mock data가 있다.
[ ] 컴포넌트가 후속 작업으로 나뉠 수 있다.
[ ] forbidden_paths가 수정되지 않았다.
[ ] validation 결과가 있다.
```

---

## 5. 단계 4 — Codex로 병렬 구현과 검증 자동화

### 5.1 목표

Codex는 작은 TASK를 병렬로 처리하는 worker로 사용한다.

```text
Codex에게 맡길 것:
- 작고 독립적인 component 구현
- unit/component test 작성
- validation command 실행
- evidence 생성
- 실패 수리
- review 보조
```

```text
Codex에게 바로 맡기면 위험한 것:
- 큰 기능 전체
- DB/API/UI를 한 번에 건드리는 작업
- 파일 경로 제한 없는 작업
- validation 없는 작업
- 권한/결제/배포/secret 관련 작업
```

### 5.2 병렬 실행 가능한 TASK 기준

| 기준 | 병렬 가능 |
|---|---:|
| allowed_paths가 겹치지 않는다 | 가능 |
| 같은 type/interface를 서로 바꾸지 않는다 | 가능 |
| 같은 테스트 파일을 수정하지 않는다 | 가능 |
| 하나가 다른 하나의 결과를 기다리지 않는다 | 가능 |
| 같은 DB schema/API contract를 수정한다 | 불가 |
| 같은 페이지 파일을 동시에 수정한다 | 불가 |

### 5.3 Codex TASK 예시

```yaml
id: TASK-CX-001
title: "Implement StatusSummaryCard component"
spec: SPEC-002-ui-shell
status: ready
risk_level: low
agent_preference: codex
skill: atomic-implementation

parallel_group: wave-1-components

depends_on:
  - TASK-UI-001

allowed_paths:
  - "src/components/[feature]/StatusSummaryCard.tsx"
  - "tests/components/StatusSummaryCard.test.tsx"
  - "harness/runs/${RUN_ID}/evidence.json"

forbidden_paths:
  - "package.json"
  - "src/db/**"
  - "src/app/api/**"
  - "src/auth/**"
  - "src/worker/**"

goal: >
  Implement a presentational status summary component using the existing ViewModel contract.

acceptance:
  - "Renders all statuses defined in the SPEC"
  - "Shows a clear message for failed or blocked states"
  - "Has tests for empty, success, failed, and blocked states"
  - "Does not change public ViewModel contract"
  - "Does not touch forbidden paths"

validation:
  commands:
    - "npm run lint"
    - "npm run test -- StatusSummaryCard"
```

### 5.4 Evidence 예시

```json
{
  "run_id": "2026-07-05T00-00-00Z-TASK-CX-001",
  "task_id": "TASK-CX-001",
  "agent": "codex:task-implementer",
  "skill": "atomic-implementation",
  "changed_files": [
    "src/components/feature/StatusSummaryCard.tsx",
    "tests/components/StatusSummaryCard.test.tsx"
  ],
  "scope_check": {
    "status": "passed",
    "forbidden_paths_touched": [],
    "out_of_scope_paths_touched": []
  },
  "validation": [
    {
      "command": "npm run lint",
      "status": "passed"
    },
    {
      "command": "npm run test -- StatusSummaryCard",
      "status": "passed"
    }
  ],
  "acceptance": [
    {
      "criterion": "Renders all statuses defined in the SPEC",
      "status": "passed"
    }
  ],
  "merge_recommendation": "mergeable",
  "risks": []
}
```

### 5.5 Hook으로 막아야 하는 것

| Hook | 막는 것 |
|---|---|
| prompt-intake | TASK 없이 구현 시작 |
| pre-tool-guard | 위험 명령, dependency install, migration |
| diff-scope-check | allowed_paths 밖 수정 |
| dependency-guard | 승인 없는 package 변경 |
| evidence-gate | evidence 없는 완료 선언 |

### 5.6 단계 4 완료 기준

```text
[ ] 최소 3개 TASK가 병렬 실행 가능하게 나뉘어 있다.
[ ] 각 TASK의 allowed_paths가 겹치지 않는다.
[ ] 각 TASK가 validation command를 가진다.
[ ] 각 실행이 evidence.json을 남긴다.
[ ] 최소 1개 실패 또는 차단 사례를 설명할 수 있다.
[ ] review 결과가 mergeable / needs_review / blocked 중 하나로 정리된다.
```
---

## 9. 중요한 것 리마인드

1. 실습에 사용할 coding agent(Claude Code 또는 Codex)에는 먼저 Superpowers를 설치한다.
2. 아이디어를 PRD 로 작성한 뒤, 바로 구현하라는 요청으로 보내지 않는다.
3. P0는 하나의 핵심 흐름이 끝까지 되는 것이다.
4. 완료 증거를 먼저 정한다.
4. SPEC은 기능 설명이 아니라 구현 계약이다.
5. TASK는 AI Agent 하나가 할 수 있을 만큼 작아야 한다.
7. allowed_paths와 forbidden_paths 없이 구현을 맡기지 않는다.
8. Claude Code는 구조와 화면 골격에 활용해본다.
9. Codex는 작은 구현과 검증 병렬화에 활용해본다.
10. Hook은 부탁이 아니라 강제 장치라는 것을 이용해서, 이 프로젝트에 어울리는 훅을 설정한다.
11. 완료는 말이 아니라 evidence로 판단한다.
