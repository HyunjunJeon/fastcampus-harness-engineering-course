# 복사용 템플릿 모음

사용법:

```text
1. [대괄호] 안을 자신의 프로젝트 내용으로 채운다.
2. 모르는 항목은 비워두지 말고 “가정”으로 적는다.
3. PRD → MVP Scope → Roadmap → SPEC → TASK 순서로 작성한다.
4. 구현 요청에는 반드시 TASK와 validation을 붙인다.
5. 완료 판단은 evidence로 한다.
6. Claude Code / Codex 프롬프트를 실행할 때 Superpowers skill workflow를 확인하고 사용하게 한다.
```

---

# 1. `docs/00-idea.md` 템플릿

````markdown
# Idea

## 1. 아이디어 한 문장

[어떤 서비스를 만들고 싶은지 한 문장으로 적는다]

## 2. 문제

[누가 어떤 상황에서 어떤 문제를 겪는지 적는다]

## 3. 첫 사용자

- Primary user: [첫 사용자의 역할]
- 사용 환경: [혼자 사용 / 팀 사용 / 내부 도구 / 공개 서비스 등]

## 4. 첫 성공 경험

사용자는 처음에 아래 흐름을 성공해야 한다.

```text
[행동 1]
→ [행동 2]
→ [행동 3]
→ [결과 확인]
```

## 5. 반드시 저장되어야 하는 것

- [기록 1]
- [기록 2]
- [기록 3]

## 6. 막아야 하는 위험 행동

- [예: 삭제]
- [예: 결제]
- [예: 외부 발송]
- [예: 권한 변경]
- [예: 개인정보/secret 노출]

## 7. 완료 증거

- [사용자가 볼 수 있는 화면]
- [생성되어야 하는 기록]
- [통과해야 하는 테스트]
- [실패 시 확인 가능한 로그]
````

---

# 2. `docs/01-prd.md` 템플릿

````markdown
# PRD — [제품명]

## 1. 제품 한 줄 정의

[제품을 한 문장으로 정의한다]

## 2. 문제 정의

### 현재 문제

[사용자가 지금 겪는 문제]

### 왜 지금 해결해야 하는가

[이 문제가 중요한 이유]

## 3. 사용자

### Primary User

- 역할: [첫 사용자]
- 상황: [언제 사용하는가]
- 목표: [무엇을 달성하려 하는가]

### Secondary User

- 역할: [후속 사용자]
- P0 포함 여부: [포함 / 제외]

## 4. P0 Golden Path

```text
1. [사용자가 첫 행동을 한다]
2. [시스템이 처리한다]
3. [기록이 저장된다]
4. [사용자가 결과를 확인한다]
5. [실패 시 이유와 다음 행동을 볼 수 있다]
```

## 5. P0에 포함할 것

| 기능 | 이유 | 완료 증거 |
|---|---|---|
| [기능 1] | [왜 P0인지] | [어떻게 확인하는지] |
| [기능 2] | [왜 P0인지] | [어떻게 확인하는지] |

## 6. P1/P2로 미룰 것

| 기능 | 미루는 이유 |
|---|---|
| [기능] | [P0 검증 뒤 가능하기 때문] |

## 7. 이번 MVP에서 하지 않을 것

| 제외 항목 | 이유 |
|---|---|
| [제외 항목] | [복잡도/위험/핵심 흐름과 무관] |

## 8. 핵심 화면

| 화면 | 사용자가 확인할 것 |
|---|---|
| [화면 1] | [상태/결과/버튼/실패 메시지] |
| [화면 2] | [상태/결과/버튼/실패 메시지] |

## 9. 저장해야 할 데이터

| 데이터 | 역할 |
|---|---|
| [데이터 1] | [왜 필요한지] |
| [데이터 2] | [왜 필요한지] |

## 10. 상태 전이

| 대상 | From | Event | To | Side Effect |
|---|---|---|---|---|
| [Entity] | [상태] | [행동] | [상태] | [기록/알림/로그] |

## 11. 실패 상황

| 실패 | 시스템 동작 | 사용자 메시지 | 재시도 가능 여부 |
|---|---|---|---|
| [실패 1] | [어떻게 닫히는지] | [무엇을 보여주는지] | [가능/불가] |
| [실패 2] | [어떻게 닫히는지] | [무엇을 보여주는지] | [가능/불가] |

## 12. 성공 지표

| 지표 | 목표 |
|---|---:|
| Golden Path 완료 가능 | 100% |
| 핵심 실패 메시지 확인 가능 | 100% |
| 필수 기록 생성 | 100% |

## 13. 완료 증거

- [ ] 화면에서 핵심 흐름 확인
- [ ] 테스트 결과 확인
- [ ] 저장 record 확인
- [ ] 실패 상황 확인
- [ ] 남은 위험 정리
````

---

# 3. `docs/02-mvp-scope.md` 템플릿

````markdown
# MVP Scope — [제품명]

## 1. Canonical MVP Cut

| 구분 | 결정 |
|---|---|
| Primary user | [첫 사용자] |
| Primary workflow | [핵심 흐름] |
| P0 platform | [web/local/mobile 등] |
| P0 auth | [없음/local admin/basic login 등] |
| P0 data | [저장해야 할 최소 데이터] |
| P0 validation | [완료 증거] |

## 2. P0 Golden Path

```text
[시작]
→ [핵심 행동]
→ [처리]
→ [저장]
→ [결과 확인]
```

## 3. P0 포함 범위

| 범위 | 포함 이유 | 완료 증거 |
|---|---|---|
| [범위] | [핵심 흐름에 필요] | [확인 방법] |

## 4. P1/P2 범위

| 범위 | 단계 | 미루는 이유 |
|---|---|---|
| [범위] | P1 | [P0 이후 가능] |
| [범위] | P2 | [확장 기능] |

## 5. Out of MVP

| 제외 | 이유 |
|---|---|
| [제외] | [핵심 흐름과 무관 / 위험 / 복잡] |

## 6. 상태 전이

| Entity | From | Event | To | Required Record |
|---|---|---|---|---|
| [대상] | [상태] | [행동] | [상태] | [기록] |

## 7. Failure Matrix

| Failure | Final Status | Required Record | User Message | Retry |
|---|---|---|---|---|
| [실패] | [상태] | [로그/기록] | [메시지] | [가능/불가] |

## 8. Invariants

아래 규칙은 구현 편의 때문에 완화하면 안 된다.

- [ ] [중요 규칙 1]
- [ ] [중요 규칙 2]
- [ ] [중요 규칙 3]

## 9. P0 Screen Cut

| Screen | P0 포함 | 이유 |
|---|---:|---|
| [화면] | 포함 | [핵심 흐름에 필요] |
| [화면] | 제외 | [후순위] |

## 10. 완료 기준

- [ ] Golden Path가 끝까지 된다.
- [ ] 실패 상황이 상태와 기록으로 닫힌다.
- [ ] 사용자가 결과를 확인할 수 있다.
- [ ] 테스트 또는 검증 명령이 있다.
````

---

# 4. `docs/03-roadmap.md` 템플릿

````markdown
# Roadmap — [제품명]

## 1. Roadmap 원칙

이 Roadmap은 일정표가 아니라 구현 의존성 순서표다.

```text
먼저 골격을 만든다.
그다음 핵심 데이터를 저장한다.
그다음 핵심 행동을 구현한다.
그다음 실패와 검증을 붙인다.
마지막으로 운영 화면과 증거를 정리한다.
```

## 2. Phase 목록

| Phase | 이름 | 목표 | 종료 기준 |
|---:|---|---|---|
| 0 | Project Skeleton | [앱 골격] | [실행/lint 통과] |
| 1 | Core Data | [핵심 데이터] | [record 생성 가능] |
| 2 | Core Flow | [핵심 행동] | [Golden Path 가능] |
| 3 | Failure & Safety | [실패/권한/검증] | [실패가 닫힘] |
| 4 | Evidence & Review | [증거/리뷰] | [완료 판단 가능] |

## 3. 의존성

```text
Phase 0
→ Phase 1
→ Phase 2
→ Phase 3
→ Phase 4
```

## 4. SPEC 분해 계획

| SPEC | 연결 Phase | 목적 |
|---|---:|---|
| SPEC-001-core-flow | Phase 1-2 | [핵심 흐름] |
| SPEC-002-ui-shell | Phase 2 | [화면 골격] |
| SPEC-003-validation | Phase 3-4 | [검증/증거] |

## 5. 병렬화 후보

| 작업 | 병렬 가능 여부 | 이유 |
|---|---:|---|
| [컴포넌트 A] | 가능 | 파일 경로가 독립적 |
| [API + DB] | 불가 | 데이터 계약 변경이 필요 |
````

---

# 5. `specs/SPEC-000-template.md` 템플릿

````markdown
# SPEC-[번호] — [기능명]

## 1. Summary

[이 SPEC이 무엇을 구현 가능한 계약으로 고정하는지 설명]

## 2. Scope

포함:

- [포함 1]
- [포함 2]

## 3. Out of Scope

제외:

- [제외 1]
- [제외 2]

## 4. User Flow

```text
1. [사용자 행동]
2. [시스템 처리]
3. [상태 변화]
4. [결과 확인]
```

## 5. Screen Contract

| Screen / Component | Responsibility | State |
|---|---|---|
| [화면/컴포넌트] | [책임] | loading/empty/error/success |

## 6. Data Contract

```ts
export type [Feature]ViewModel = {
  id: string;
  status: "idle" | "loading" | "success" | "failed" | "blocked";
  // 필요한 필드를 추가한다.
};
```

## 7. API or Action Contract

| Action/API | Input | Output | Failure |
|---|---|---|---|
| [행동] | [입력] | [결과] | [실패] |

## 8. State Transition

| From | Event | To | Side Effect |
|---|---|---|---|
| [상태] | [행동] | [상태] | [기록/로그] |

## 9. Failure Handling

| Failure | Final State | User Message | Required Evidence |
|---|---|---|---|
| [실패] | [상태] | [메시지] | [로그/테스트/화면] |

## 10. Safety Rules

- [ ] [규칙 1]
- [ ] [규칙 2]
- [ ] [규칙 3]

## 11. Acceptance Criteria

- [ ] [기준 1]
- [ ] [기준 2]
- [ ] [기준 3]

## 12. Validation Plan

```text
npm run lint
npm run test -- [feature]
```

## 13. Evidence Requirements

- changed files
- validation results
- acceptance pass/fail
- screenshots or screen notes if relevant
- remaining risks
````

---

# 6. `tasks/TASK-000-template.yaml` 템플릿

```yaml
id: TASK-000
title: "[작업 제목]"
spec: SPEC-000-template
status: ready
risk_level: low # low | medium | high
agent_preference: claude # claude | codex
skill: atomic-implementation

depends_on: []
parallel_group: wave-0

allowed_paths:
  - "[수정 허용 경로]"

forbidden_paths:
  - "package.json"
  - "src/db/**"
  - "src/app/api/**"
  - "src/auth/**"
  - "src/worker/**"
  - ".env*"

goal: >
  [이 TASK 하나가 달성해야 하는 결과를 한 문장으로 적는다.]

acceptance:
  - "[완료 기준 1]"
  - "[완료 기준 2]"
  - "[완료 기준 3]"

validation:
  commands:
    - "npm run lint"
    - "npm run test -- [테스트 이름]"

outputs:
  - "[생성/수정될 파일]"
  - "harness/runs/${RUN_ID}/evidence.json"
```

---

# 7. Claude Code UI Scaffold 프롬프트 템플릿

```text
You are working inside an AI Agent Harness.

Read:
- student_superpowers_setup.md
- student_brainstorming_deep_interview_guide.md
- student_deep_interview_trigger_skill.md
- docs/01-prd.md
- docs/02-mvp-scope.md
- specs/[SPEC 파일]
- tasks/[TASK 파일]

Implement only the assigned TASK.
Before editing, check whether a relevant Superpowers skill applies. Use the appropriate brainstorming, planning, scaffold, and verification workflow instead of improvising.


This is UI scaffold work, not backend implementation.
Use typed demo fixtures or existing mocked data.
Do not modify API routes, DB schema, auth, worker code, package dependencies, deployment config, or environment files.
Represent loading, empty, error, success, blocked, and completed states.
Keep components small enough for later Codex atomic tasks.
Run the validation commands from the TASK.

Final response must include:
- changed files
- validation commands and results
- acceptance criteria pass/fail mapping
- forbidden path check
- remaining risks
```

---

# 8. Codex Atomic Implementation 프롬프트 템플릿

```text
You are a Codex implementation worker inside an AI Agent Harness.

Read:
- student_superpowers_setup.md
- student_brainstorming_deep_interview_guide.md
- student_deep_interview_trigger_skill.md
- AGENTS.md or project instructions
- the assigned TASK YAML
- the parent SPEC
- only relevant source files

Implement exactly one TASK.
Before editing, check whether a relevant Superpowers skill applies. Use the appropriate atomic implementation, TDD, review, and verification workflow instead of improvising.

Rules:
- Stay within allowed_paths.
- Do not modify forbidden_paths.
- Do not add dependencies unless the TASK explicitly allows it.
- Do not change public contracts unless the TASK says so.
- Prefer minimal, reviewable diffs.
- Run every validation command from the TASK.
- Produce evidence.json.
- Do not claim success if validation failed.

Final response must include:
- changed files
- validation commands and results
- acceptance criteria pass/fail mapping
- evidence path
- scope check result
- risks
```

---

# 9. `harness/evidence.schema.example.json` 템플릿

```json
{
  "run_id": "2026-07-05T00-00-00Z-TASK-000",
  "task_id": "TASK-000",
  "agent": "codex:task-implementer",
  "skill": "atomic-implementation",
  "changed_files": [],
  "scope_check": {
    "status": "passed",
    "forbidden_paths_touched": [],
    "out_of_scope_paths_touched": []
  },
  "validation": [
    {
      "command": "npm run lint",
      "status": "passed",
      "duration_ms": 0,
      "relevant_output": ""
    }
  ],
  "acceptance": [
    {
      "criterion": "[acceptance criterion]",
      "status": "passed"
    }
  ],
  "merge_recommendation": "mergeable",
  "risks": []
}
```

---

# 10. Review Checklist 템플릿

```markdown
# Review Checklist — [TASK ID]

## 1. Scope

- [ ] changed_files가 allowed_paths 안에 있다.
- [ ] forbidden_paths가 수정되지 않았다.
- [ ] TASK 밖 요구사항이 추가되지 않았다.

## 2. Acceptance

- [ ] acceptance criterion 1: [pass/fail]
- [ ] acceptance criterion 2: [pass/fail]
- [ ] acceptance criterion 3: [pass/fail]

## 3. Validation

| Command | Result | Notes |
|---|---|---|
| npm run lint | [passed/failed] | [note] |
| npm run test -- [name] | [passed/failed] | [note] |

## 4. Evidence

- [ ] evidence.json exists.
- [ ] validation results are recorded.
- [ ] acceptance mapping is recorded.
- [ ] risks are listed.

## 5. Recommendation

- [ ] mergeable
- [ ] needs_review
- [ ] blocked

Reason:

[판단 이유]
```

---

# 11. 점검 체크리스트

```text
[ ] 실습에 사용할 coding agent에 Superpowers를 설치하고 확인했다.
[ ] Superpowers brainstorming으로 아이디어를 design/spec으로 정리했다.
[ ] 아이디어가 여전히 모호한 경우 deep-interview-trigger Skill이 Deep Interview를 발동했다.
[ ] 나는 아이디어를 바로 구현 요청으로 보내지 않았다.
[ ] PRD에 첫 사용자와 첫 성공 경험이 있다.
[ ] MVP Scope에 P0/P1/P2/Out이 있다.
[ ] Roadmap에 phase별 종료 기준이 있다.
[ ] SPEC에 화면, 데이터, 상태, 실패, 검증이 있다.
[ ] TASK는 하나의 AI Agent가 할 수 있을 만큼 작다.
[ ] TASK에 allowed_paths와 forbidden_paths가 있다.
[ ] Claude Code에는 UI scaffold만 맡겼다.
[ ] Codex에는 작은 atomic TASK만 맡겼다.
[ ] validation command를 실행했다.
[ ] evidence를 남겼다.
[ ] 실패나 위험을 숨기지 않았다.
```
