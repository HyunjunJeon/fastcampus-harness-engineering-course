# Agent Control Plane MVP Planning

이 문서는 Agent Control Plane MVP의 제품 범위, 핵심 흐름, 데이터 모델, 화면, API, 구현 순서를 정리한 계획서다. 제품의 기준점은 Jira/Linear처럼 이슈를 만들고 할당하고 추적하는 서비스이며, 차이는 작업자가 사람이 아니라 AI Agent라는 점이다.

제품의 중심 루프는 아래 흐름으로 고정한다.

```txt
목표 생성
→ Agent 등록
→ Issue 생성/할당
→ Heartbeat 실행
→ 비용/예산/승인/감사 확인
```

---

## 1. 제품 한 줄 정의

**Jira/Linear형 작업 관리 모델에 AI Agent 작업자, Heartbeat 실행, 비용·승인·감사 통제를 붙인 AI Agent Control Plane.**

이 제품은 AI agent 자체를 만드는 프레임워크가 아니다. 사람이 이슈를 맡아 처리하는 Jira/Linear의 작업 관리 흐름을 가져오되, assignee가 AI Agent로 바뀌었을 때 필요한 실행·권한·비용·승인·감사 계층을 제공하는 운영 서비스다.

---

## 2. MVP 제품 방향

### 2.1 최종 MVP 범위

MVP는 “AI 회사 전체”가 아니라 **AI Agent가 작업자로 배정되는 이슈 처리 루프**에 집중한다. Jira/Linear와 같은 작업 관리 구조를 기본으로 삼되, MVP에서 검증할 제품 가치는 아래 다섯 가지다.

1. **사용자가 목표 또는 프로젝트를 만든다.**
2. **이슈를 만들고 AI Agent에게 할당한다.**
3. **Agent가 heartbeat/run으로 실제 작업을 수행한다.**
4. **결과가 issue comment, run log, 상태 변경으로 남는다.**
5. **비용, 예산 초과, 승인 요청, 감사 로그를 확인한다.**

따라서 MVP의 충분성 기준은 기능 개수가 아니라 **이슈 생성 → Agent 할당 → 실행 → 결과 확인 → 통제 기록**이 끝까지 닫히는지다. 이 루프가 안정적으로 동작하면 MVP로 충분하다.

### 2.2 MVP 범위 고정안

PRD 작성과 구현 범위는 아래 결정을 기준으로 삼는다.

| 구분 | 고정 결정 |
| --- | --- |
| Primary user | single admin / local trusted operator |
| Primary workflow | goal 생성 -> agent 등록 -> issue 생성/할당 -> manual heartbeat -> run log/cost/approval/audit 확인 |
| P0 adapter | `built_in_llm` 또는 `mock_agent`, `http_webhook` |
| P0 adapter infra | adapter registry interface, adapter config validation, heartbeat contract test |
| P1 adapter | `local_process`, local trusted mode 전용 |
| P2 adapter | `agent_api_pull`, external daemon/polling agent용 |
| P0 MCP | stdio local MCP server 등록, tool/resource discovery, agent별 read-first allowlist |
| P0 budget/approval | heartbeat 전 budget hard stop, high-risk MCP tool approval, 모든 결정 audit 기록 |
| P0 auth | 별도 multi-user/RBAC 없음. 모든 user action은 `local_admin` actor로 기록 |

P0의 성공 기준은 다양한 agent runtime을 모두 지원하는 것이 아니다. **하나의 운영 루프가 끝까지 안전하게 돈다는 것을 증명하는 것**이다.

### 2.3 P0 핵심 흐름

P0 PRD는 아래 한 가지 시나리오를 반드시 통과해야 한다.

```txt
1. local_admin이 workspace에 접속한다.
2. goal을 생성한다.
   - title: "Research launch checklist"
   - successCriteria: "요약, 위험, 다음 액션이 issue comment로 남는다."
   - monthlyBudgetCents: 2000
3. `local-docs` stdio MCP server를 등록하고 discovery를 실행한다.
4. `mock_agent` 또는 `built_in_llm` agent를 등록한다.
   - role: Researcher
   - monthlyBudgetCents: 1000
   - allowed MCP tools: read/search 계열만
5. agent를 approve해서 active 상태로 전환한다.
6. goal 아래 issue를 생성하고 agent에게 assign한다.
7. issue detail에서 manual heartbeat를 실행한다.
8. worker가 budget, approval, MCP permission, concurrent run lock을 검사한다.
9. adapter가 결과를 반환한다.
10. 시스템은 run, run_logs, cost_events, issue comment, audit_events를 저장한다.
11. issue는 `in_review` 또는 `completed`가 된다.
12. dashboard와 issue detail에서 run 결과, 비용, 감사 이벤트를 확인할 수 있다.
```

### 2.4 P0 상태 전이 기준

상태 전이는 PRD와 테스트에서 아래 표를 기준으로 삼는다.

#### Goal

| From | Event | To | Side effect |
| --- | --- | --- | --- |
| draft | activate | active | `goal.activated` audit |
| active | pause | paused | 새 heartbeat 차단 |
| paused | resume | active | `goal.resumed` audit |
| active/paused | archive | archived | 새 issue/heartbeat 차단 |

#### Agent

| From | Event | To | Side effect |
| --- | --- | --- | --- |
| draft | submit | pending_approval | `agent.submitted_for_approval` audit |
| pending_approval | approve | active | heartbeat 가능 |
| pending_approval | reject | draft | rejection reason 저장 |
| active | heartbeat_start | running | 동일 agent concurrency check |
| running | heartbeat_finish | active | lastHeartbeatAt 갱신 |
| active/running | pause | paused | 새 run 차단 |
| paused | resume | active | `agent.resumed` audit |
| any except terminated | terminate | terminated | 복구 불가 |

#### Issue

| From | Event | To | Side effect |
| --- | --- | --- | --- |
| open | assign_agent | assigned | `issue.assigned` audit |
| assigned | heartbeat_start | running | running run 생성 |
| running | adapter_succeeded | in_review | comment/run log 저장 |
| running | adapter_completed | completed | completion audit |
| running | adapter_failed | blocked | failed reason 저장 |
| in_review | manual_rerun | running | 새 run 생성 |
| assigned/in_review | cancel | cancelled | 새 run 차단 |

#### Run

| From | Event | To | Side effect |
| --- | --- | --- | --- |
| queued | worker_claimed | running | issue lock 획득 |
| queued | budget_missing | blocked_by_budget | adapter 호출 금지 |
| queued | approval_missing | blocked_by_approval | approval 생성 |
| queued | policy_denied | blocked_by_policy | policy reason 저장 |
| running | adapter_success | succeeded | output/cost/audit 저장 |
| running | adapter_error | failed | error summary 저장 |
| running | cancel | cancelled | best-effort adapter cancel |
| running | orphan_detected | failed | orphan recovery audit |

#### Approval

| From | Event | To | Side effect |
| --- | --- | --- | --- |
| pending | approve | approved | blocked action 재시도 가능 |
| pending | reject | rejected | 관련 run은 blocked/failed 유지 |
| pending | expire | expired | 재요청 필요 |

### 2.5 Heartbeat Failure Matrix

Heartbeat 실패는 반드시 닫힌 상태와 감사 이벤트를 남겨야 한다.

| Failure | Run status | Issue status | Required records | Retry |
| --- | --- | --- | --- | --- |
| Agent inactive/paused | blocked_by_policy | assigned | audit `run.blocked_by_policy` | user action 후 가능 |
| Goal paused/archived | blocked_by_policy | assigned | audit reason | goal resume 후 가능 |
| Agent budget exhausted | blocked_by_budget | assigned | cost summary, audit | budget 변경 후 가능 |
| Issue budget exhausted | blocked_by_budget | assigned | cost summary, audit | budget 변경 후 가능 |
| Approval required | blocked_by_approval | assigned | approval row, audit | approval 후 가능 |
| MCP tool not allowed | blocked_by_policy | assigned | denied tool metadata, audit | permission 변경 후 가능 |
| MCP server unavailable | failed | assigned 또는 in_review | run log, audit | 수동 재실행 |
| Adapter timeout | failed | assigned 또는 in_review | stderr/error summary, audit | 수동 재실행 |
| Adapter schema mismatch | failed | assigned 또는 in_review | raw response metadata, audit | adapter config 수정 후 |
| Worker crash/orphan | failed | assigned 또는 in_review | orphan recovery audit | 수동 재실행 |
| Duplicate running run | blocked_by_policy | 기존 상태 유지 | lock conflict audit | 기존 run 종료 후 |

### 2.6 보안·거버넌스 불변 조건

아래 규칙은 구현 편의 때문에 완화하면 안 된다.

| Invariant | Contract |
| --- | --- |
| Budget hard stop | 예산 잔액이 0 이하이면 adapter를 호출하지 않는다. |
| Approval gate | approval이 필요한 action은 승인 전 실행하지 않는다. |
| MCP deny by default | agent는 명시 허용된 server/tool/resource만 사용할 수 있다. |
| High-risk MCP tools | write/delete/execute/external-send 계열은 P0에서 기본 차단하거나 매 호출 approval을 요구한다. |
| Secret redaction | secret/env/token 값은 UI, run log, audit event에 평문 저장하지 않는다. |
| Audit append-only | 핵심 mutation은 audit event 없이 commit하지 않는다. audit event는 application layer에서 수정/삭제하지 않는다. |
| Run lock | 동일 issue에는 running run이 동시에 2개 이상 존재할 수 없다. |
| Local admin actor | P0의 모든 user action actor는 `local_admin`으로 기록한다. |
| Adapter boundary | P0 adapter는 `mock_agent`/`built_in_llm`/`http_webhook`만 활성화한다. P1/P2 adapter는 UI에 disabled 또는 roadmap으로 표시한다. |

### 2.7 P0 화면 범위

P0는 화면 수를 줄이고 운영 루프 검증에 집중한다.

| Screen | P0 포함 | 핵심 기능 |
| --- | ---: | --- |
| Dashboard | 포함 | active goals, agents, open issues, running runs, pending approvals, budget usage, failed runs |
| Goal Detail | 포함 | goal 정보, issue 목록, 누적 cost, pause/resume/archive |
| Agent Detail / Wizard | 포함 | P0 adapter 등록, MCP permission, budget, approval, test heartbeat |
| Issue Detail | 포함 | issue 상태, assignee, heartbeat 실행, run logs, comments, cost, approvals, audit trail |
| MCP Settings | 포함 | stdio server 등록, discovery, read/search allowlist |
| Approval Queue | 포함 | pending approvals, approve/reject, reason |
| Audit Log | 포함 | 최근 audit list, actor/action/entity/runId filter |
| Cost & Budget 전용 화면 | 제외 | P0에서는 Dashboard/Detail 내 요약으로 충분 |
| Multi-user settings | 제외 | P0는 `local_admin` 단일 actor |

---

## 3. 핵심 제품 판단

### 3.1 반드시 포함할 기능

| 영역           | MVP 포함 여부 | 이유                      |
| ------------ | --------: | ----------------------- |
| 목표 관리        |        포함 | 모든 이슈와 실행의 상위 맥락        |
| Agent 등록/고용  |        포함 | 누가 일하는지 정의해야 함          |
| 이슈 생성/할당     |        포함 | 실행 단위                   |
| Heartbeat 실행 |        포함 | 제품의 실행 엔진               |
| MCP 서버 연동    |        포함 | agent의 지식/도구 확장 핵심      |
| 비용/예산 추적     |        포함 | runaway cost 방지         |
| 승인 게이트       |        포함 | agent autonomy를 안전하게 제어 |
| 감사 로그        |        포함 | 신뢰/운영/디버깅 기반            |
| 대시보드         |        포함 | 현재 상태를 한눈에 보는 운영 화면     |

### 3.2 MVP에서 제외할 기능

| 제외 기능                       | 이유                                   |
| --------------------------- | ------------------------------------ |
| Multi-company               | MVP에서는 단일 workspace로 충분              |
| 복잡한 org chart               | flat agent list + role 정도로 충분        |
| agent 간 자동 위임               | MVP 복잡도 급증                           |
| 플러그인 마켓/동적 플러그인 런타임         | MCP 연동으로 우선 대체                       |
| 회사 import/export            | 초기 운영 루프 검증 이후                       |
| self-organization           | 자동 조직 개편은 후순위                        |
| deep planning               | v2 기능                                |
| cloud sandbox agent         | 비용과 보안 복잡도 큼                         |
| artifacts/work products 고도화 | MVP에서는 텍스트 결과/첨부 수준                  |
| multi-user invite/RBAC      | 초기에는 single admin/local trusted mode |
| 모바일 최적화                     | 반응형 UI 정도만                           |

cloud/sandbox agents, artifacts, memory/knowledge, deep planning, self-organization, cloud deployment, desktop app 등은 운영 루프 검증 이후로 둔다.

---

## 4. 기술 스택 결정

### 4.1 언어 스택

**TypeScript 단일 언어 스택으로 고정.**

MVP 구현 범위에서 TypeScript가 담당하는 영역은 아래와 같다.

| 영역                     | 선택                 |
| ---------------------- | ------------------ |
| Web UI                 | TypeScript + React |
| Web backend/API        | TypeScript         |
| Heartbeat worker       | TypeScript         |
| Agent adapter          | TypeScript         |
| MCP client integration | TypeScript         |
| DB access layer        | TypeScript ORM     |
| CLI/dev scripts        | TypeScript         |

---

### 4.2 Next.js 선택 여부

#### 결론

**MVP 기본안은 Next.js다. 다만 agent 실행과 heartbeat worker는 Next.js Route Handler 안에 넣지 않고, 같은 TypeScript 코드베이스의 별도 Node worker 모듈로 둔다.**

Next.js는 full-stack React framework라서 UI와 API를 한 프로젝트에서 빠르게 만들 수 있다. 공식 문서도 Next.js를 “full-stack web applications”를 만들기 위한 React framework로 설명한다. ([Next.js][3]) 또한 Route Handlers로 Web Request/Response 기반 custom HTTP handler를 만들 수 있다. ([Next.js][4])

다만 Next.js 문서가 명시하듯 Next.js의 backend 기능은 “full backend replacement”가 아니라 frontend를 위한 API layer에 가깝다. ([Next.js][5]) 이 제품은 단순 BFF가 아니라 **scheduler, long-running heartbeat, MCP stdio process, local filesystem access, budget lock**이 필요하다. 따라서 agent runtime은 Next.js 안에 억지로 넣지 않는다. **같은 repo / 같은 DB / 같은 TypeScript domain service를 공유하는 worker**로 분리한다.

#### 추천 구조

```txt
agent-control-plane/
  src/
    app/                  # Next.js App Router UI
    app/api/              # Route Handlers: CRUD/API
    server/
      domain/             # Goal, Agent, Issue, Run, Budget 서비스
      db/                 # Drizzle schema, repositories
      audit/              # 감사 로그 서비스
      mcp/                # MCP client manager
      adapters/           # agent adapter interface
    worker/
      heartbeat-worker.ts # DB-backed heartbeat executor
    shared/
      types.ts
      constants.ts
```

#### 배포 모델

MVP는 **self-hosted Node/Docker**를 기본 배포 모델로 둔다.

```txt
[Browser]
   ↓
[Next.js Web App / API]
   ↓ shared DB
[Postgres]
   ↑
[Heartbeat Worker]
   ↓
[MCP Servers / Agent Adapters / LLM Provider]
```

Next.js는 self-hosting과 standalone output을 지원한다. standalone output은 production deployment에 필요한 파일만 복사하는 방식이다. ([Next.js][6]) 단, 로컬 MCP 서버와 heartbeat worker가 필요한 제품 특성상 Vercel serverless 단독 배포보다 **Docker Compose 또는 단일 VM**이 더 적합하다.

#### 대안: Hono + Vite/React

가장 가벼운 운영형 서버를 원한다면 **Hono + Vite React SPA**가 더 단순하다. Hono는 small, simple, ultrafast web framework이고 Node.js를 포함한 여러 JS runtime에서 동작하며, zero dependency와 first-class TypeScript support를 강조한다. ([hono.dev][7])

다만 “웹 백엔드와 프론트엔드를 하나의 풀스택 프레임워크로 고정”한다는 기준에서는 Next.js가 더 자연스럽다. 따라서 MVP PRD의 기본 스택은 **Next.js + Node worker**로 정의한다.

---

## 5. MCP 연동 방향

### 5.1 MCP의 MVP 내 역할

MCP는 agent에게 아래 능력을 제공한다.

1. 로컬 PC 문서 검색/읽기
2. 사내 문서/노션/구글드라이브 등 외부 서비스 조회
3. 특정 도구 호출
4. issue 수행에 필요한 context pack 생성

MCP 공식 문서는 MCP를 AI application이 local files, databases, tools, prompts 같은 external systems에 연결되도록 하는 open-source standard로 설명한다. ([Model Context Protocol][8]) MCP specification도 Hosts, Clients, Servers 구조와 Resources, Prompts, Tools를 핵심 기능으로 정의한다. ([Model Context Protocol][9])

### 5.2 MVP MCP 범위

| MCP 기능                             | MVP 포함 여부 |
| ---------------------------------- | --------: |
| stdio 기반 local MCP server 등록       |        포함 |
| MCP tools/list, tools/call         |        포함 |
| MCP resources/list, resources/read |        포함 |
| MCP prompts/list                   |        선택 |
| remote Streamable HTTP MCP         |      v1.1 |
| OAuth 기반 remote MCP                |        제외 |
| MCP server marketplace             |        제외 |
| arbitrary MCP tool auto-approval   |        제외 |
| MCP 호출별 audit log                  |        포함 |
| agent별 MCP server/tool allowlist   |        포함 |

MCP TypeScript SDK는 server/client library를 제공하며, Node.js/Bun/Deno에서 동작하고 tools/resources/prompts, stdio, Streamable HTTP 등을 지원한다. ([GitHub][10]) 단, 2026년 7월 1일 현재 SDK main branch의 v2는 beta이며 v1.x가 production supported release로 안내되어 있으므로, MVP는 **v1.x SDK 사용**을 기본으로 둔다. ([GitHub][10])

### 5.3 MCP 보안 원칙

MCP는 강력하지만 위험한 실행 경로를 연다. MCP specification도 arbitrary data access와 code execution path에 따른 security/trust 고려가 필요하며, user consent, data privacy, tool safety를 핵심 원칙으로 둔다. ([Model Context Protocol][9])

MVP는 아래 보안 정책을 기본값으로 둔다.

| 정책                      | 설명                                           |
| ----------------------- | -------------------------------------------- |
| deny by default         | agent는 기본적으로 어떤 MCP server/tool도 사용할 수 없음    |
| explicit allowlist      | agent별 허용 MCP server/tool을 지정                |
| read/write 분리           | read-only tool과 mutation tool을 구분            |
| high-risk tool approval | 파일 삭제, 외부 전송, shell 실행 등은 매 호출 승인 필요         |
| 모든 MCP call 기록          | run log + audit event에 저장                    |
| tool description 불신     | MCP tool description은 untrusted metadata로 간주 |
| local root 제한           | local filesystem MCP는 허용 root directory만 접근  |

---

## 6. 사용자 페르소나

### 6.1 Primary User: Solo Operator

1인 창업자, 개발자, 리서처, 자동화 빌더.

필요한 것:

* 여러 agent가 어떤 일을 하는지 한눈에 보고 싶다.
* 로컬 문서/프로젝트 문서를 agent가 참고하게 하고 싶다.
* agent가 비용을 무한정 쓰지 않게 하고 싶다.
* 실행 전후로 승인하고 감사 로그를 남기고 싶다.

### 6.2 Secondary User: Small Team Operator

2~5명 규모의 작은 팀.

MVP에서는 multi-user/RBAC를 완성하지 않는다. 다만 추후 확장을 위해 모든 mutation에는 `actor`를 남긴다.

---

## 7. MVP 핵심 워크플로우

### 7.1 전체 흐름

```txt
1. 목표 생성
   ↓
2. Agent 고용
   ↓
3. MCP 권한 부여
   ↓
4. 이슈 생성
   ↓
5. Agent 할당
   ↓
6. Heartbeat 실행
   ↓
7. Agent가 MCP context/tool 사용
   ↓
8. 결과/로그/비용 저장
   ↓
9. 예산/승인/감사 확인
```

### 7.2 목표 생성

사용자는 다음 정보를 입력한다.

| 필드              | 설명                              |
| --------------- | ------------------------------- |
| title           | 목표 이름                           |
| description     | 목표 상세 설명                        |
| successCriteria | 완료 기준                           |
| context         | 배경 정보                           |
| monthlyBudget   | 목표 단위 예산                        |
| approvalPolicy  | heartbeat 전 승인 여부, 완료 전 승인 여부   |
| status          | draft, active, paused, archived |

#### 완료 기준

* 사용자는 목표를 생성/수정/보관할 수 있다.
* 모든 issue는 하나의 goal에 연결된다.
* goal detail 화면에서 연결된 issues, runs, cost를 볼 수 있다.

---

### 7.3 Agent 고용

Agent는 실행 주체다. MVP에서는 복잡한 조직도 대신 flat list로 시작한다.

| 필드                    | 설명                                                    |
| --------------------- | ----------------------------------------------------- |
| name                  | Agent 이름                                              |
| role                  | 예: Researcher, Engineer, PM                           |
| description           | 역할 설명                                                 |
| adapterType           | `built_in_llm`, `mock_agent`, `http_webhook`           |
| model/provider config | built-in agent일 때 사용                                  |
| monthlyBudget         | agent별 예산                                             |
| mcpPermissions        | 허용 MCP server/tool                                    |
| status                | pending, active, paused, budget_exhausted, terminated |

#### Agent Adapter MVP Cut

P0에서 완성할 adapter는 두 개로 고정한다. 다만 adapter registry와 config validation 구조는 처음부터 둔다.

| Adapter | 단계 | 설명 |
| --- | ---: | --- |
| `mock_agent` 또는 `built_in_llm` | P0 | 외부 agent 없이 heartbeat, cost, approval, audit 루프를 검증 |
| `http_webhook` | P0 | 외부 agent에게 heartbeat payload 전송 |
| `local_process` | P1 | 로컬 CLI 실행. local trusted mode에서만 허용 |
| `agent_api_pull` | P2 | 외부 daemon/polling agent가 API key로 작업을 가져감 |

MVP의 built-in agent는 범용 autonomous agent가 아니다. 아래 역할만 수행한다.

1. issue와 goal context 읽기
2. 허용된 MCP resource/tool 사용
3. 응답/계획/결과/다음 액션 생성
4. issue comment와 run log 작성
5. 완료 또는 review 요청 상태로 전환

---

### 7.4 이슈 생성/할당

Issue는 agent가 수행할 최소 작업 단위다.

| 필드               | 설명                                                             |
| ---------------- | -------------------------------------------------------------- |
| title            | 이슈 제목                                                          |
| description      | 작업 내용                                                          |
| goalId           | 상위 목표                                                          |
| assigneeAgentId  | 담당 agent                                                       |
| priority         | low, normal, high                                              |
| status           | open, assigned, running, in_review, completed, blocked, cancelled |
| budgetLimit      | issue 단위 최대 비용                                                 |
| mcpContextHints  | 참고할 MCP source 힌트                                              |
| approvalRequired | 실행 전 승인 필요 여부                                                  |

#### 완료 기준

* 사용자는 goal 아래 issue를 생성한다.
* issue는 agent에게 할당된다.
* issue detail에서 heartbeat 실행 버튼을 누를 수 있다.
* issue에는 comments, run history, cost, approvals, audit trail이 연결된다.

---

### 7.5 Heartbeat 실행

Heartbeat는 agent를 깨워 현재 할당된 issue를 처리하게 하는 실행 단위다. 이 MVP에서 heartbeat는 budget check, approval check, MCP context loading, adapter invocation, structured log, cost event, audit event를 생성하는 표준 실행 경로다.

#### MVP heartbeat 실행 조건

Heartbeat는 아래 조건을 모두 만족해야 실행된다.

1. issue status가 `assigned`이거나, 사용자가 명시적으로 재실행을 누른 `in_review`
2. agent status가 `active`
3. agent budget remaining > 0
4. issue budget remaining > 0
5. 필요한 approval이 승인됨
6. agent가 요청한 MCP tool이 allowlist에 있음
7. 동일 issue에 running run이 없음

#### Heartbeat 실행 단계

```txt
1. Run 생성: status = queued
2. DB transaction으로 issue lock 획득
3. budget pre-check
4. approval pre-check
5. MCP context pack 생성
6. agent adapter 호출
7. agent output 저장
8. token/cost event 저장
9. issue 상태 갱신
10. audit event 기록
11. lock release
```

#### Run 상태

| 상태                  | 의미       |
| ------------------- | -------- |
| queued              | 실행 대기    |
| running             | 실행 중     |
| succeeded           | 정상 종료    |
| failed              | 실패       |
| cancelled           | 사용자 취소   |
| blocked_by_budget   | 예산 부족    |
| blocked_by_approval | 승인 필요    |
| blocked_by_policy   | 권한/정책 위반 |

---

## 8. 기능 요구사항

### FR-001 Goal Management

사용자는 goal을 생성, 조회, 수정, pause, archive할 수 있어야 한다.

#### 세부 요구사항

* goal은 title, description, success criteria를 가진다.
* goal별 budget을 설정할 수 있다.
* goal detail에서 연결된 issue 목록을 볼 수 있다.
* goal별 누적 비용을 볼 수 있다.
* goal status가 paused이면 새 heartbeat를 실행할 수 없다.

---

### FR-002 Agent Hiring

사용자는 agent를 등록하고 승인 후 active 상태로 전환할 수 있어야 한다.

#### 세부 요구사항

* agent 생성 시 기본 status는 `pending_approval`.
* admin이 approve해야 `active`.
* agent별 monthly budget을 설정한다.
* agent별 MCP permission을 설정한다.
* agent를 pause/resume/terminate할 수 있다.
* agent 설정 변경은 audit log에 기록된다.

---

### FR-003 Issue Management

사용자는 issue를 만들고 agent에게 할당할 수 있어야 한다.

#### 세부 요구사항

* issue는 반드시 goal에 연결된다.
* issue는 0개 또는 1개의 agent에 할당된다.
* issue status는 open → assigned → running → in_review/completed 흐름을 따른다.
* issue detail에서 run logs와 comments를 확인한다.
* issue별 budget limit을 설정할 수 있다.

---

### FR-004 Heartbeat Execution

사용자는 issue detail 또는 agent detail에서 heartbeat를 실행할 수 있어야 한다.

#### 세부 요구사항

* heartbeat는 manual trigger를 MVP 기본으로 한다.
* scheduled heartbeat는 v1.1로 미룬다.
* heartbeat 실행 전 budget/approval/policy check를 수행한다.
* 실행 중 로그를 UI에서 streaming으로 볼 수 있다.
* heartbeat 결과는 run record로 저장된다.
* 동일 issue에 동시 heartbeat가 실행되지 않아야 한다.

---

### FR-005 MCP Context Layer

사용자는 MCP server를 등록하고 agent별로 사용 권한을 부여할 수 있어야 한다.

#### 세부 요구사항

* stdio MCP server를 등록한다.
* 등록 필드: name, command, args, env, workingDirectory, trustLevel.
* discovery를 실행해 tools/resources/prompts를 가져온다.
* agent별 허용 MCP server/tool을 설정한다.
* heartbeat 중 MCP call은 run log에 저장된다.
* MCP tool call은 budget/cost와 별개로 audit event를 남긴다.
* 위험 tool은 approval이 필요하다.

#### MVP 예시

로컬 문서 MCP server 등록:

```json
{
  "name": "local-docs",
  "transport": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/Documents/project"],
  "trustLevel": "local_trusted"
}
```

Agent 권한:

```json
{
  "agent": "Researcher",
  "allowedMcpServers": ["local-docs"],
  "allowedTools": ["search_files", "read_file"],
  "blockedTools": ["write_file", "delete_file", "execute_command"]
}
```

---

### FR-006 Budget & Cost Control

사용자는 agent, goal, issue 단위 예산을 설정하고 비용을 확인할 수 있어야 한다.

#### 세부 요구사항

* agent monthly budget
* goal budget
* issue budget limit
* run별 estimated cost
* provider/model/token usage 저장
* budget 80% 도달 시 warning
* 100% 초과 시 heartbeat 차단
* budget override는 approval 필요

#### `CostEvent` 필드

| 필드               | 설명             |
| ---------------- | -------------- |
| runId            | 실행 ID          |
| agentId          | agent ID       |
| goalId           | goal ID        |
| issueId          | issue ID       |
| provider         | model provider |
| model            | model name     |
| inputTokens      | input tokens   |
| outputTokens     | output tokens  |
| estimatedCostUsd | 추정 비용          |
| createdAt        | 생성 시각          |

---

### FR-007 Approval Gate

사용자는 위험하거나 비용이 큰 작업을 승인/거절할 수 있어야 한다.

#### Approval이 필요한 경우

| 상황               | MVP 정책                         |
| ---------------- | ------------------------------ |
| agent 생성         | 승인 필요                          |
| agent budget 변경  | 승인 필요                          |
| budget override  | 승인 필요                          |
| 위험 MCP tool call | 승인 필요                          |
| issue 완료 처리      | 선택 정책                          |
| heartbeat 수동 실행  | 기본은 승인 불필요, goal policy로 설정 가능 |

#### Approval 상태

| 상태       | 설명    |
| -------- | ----- |
| pending  | 승인 대기 |
| approved | 승인됨   |
| rejected | 거절됨   |
| expired  | 만료됨   |

---

### FR-008 Audit Log

모든 중요한 mutation은 감사 로그에 남아야 한다.

이 MVP는 mutating actions, heartbeat state changes, cost events, approvals, comments를 durable activity로 기록하기 위해 간단한 append-only audit log를 둔다.

#### 감사 대상

* goal 생성/수정/삭제
* agent 생성/승인/pause/resume/terminate
* issue 생성/할당/status 변경
* heartbeat 시작/종료/실패/취소
* MCP server 등록/수정/삭제
* MCP tool call
* budget warning/hard stop
* approval 생성/승인/거절
* 비용 이벤트 생성

#### `AuditEvent` 필드

| 필드         | 설명                        |
| ---------- | ------------------------- |
| id         | audit event ID            |
| actorType  | user, agent, system, mcp  |
| actorId    | 행위자 ID                    |
| action     | 예: issue.assigned         |
| entityType | goal, agent, issue, run 등 |
| entityId   | 대상 ID                     |
| before     | 변경 전 JSON                 |
| after      | 변경 후 JSON                 |
| metadata   | requestId, ip, runId 등    |
| createdAt  | 생성 시각                     |

---

## 9. 화면 요구사항

P0 화면 범위는 `2.7 P0 화면 범위`를 따른다. 아래 섹션은 최종 정보 구조를 설명하되, P0에서는 Cost & Budget 전용 화면처럼 별도 화면이 꼭 필요하지 않은 항목은 Dashboard/Detail 안의 요약 패널로 흡수한다.

### 9.1 Dashboard

운영자가 가장 먼저 보는 화면.

#### 구성 요소

* Active Goals
* Active Agents
* Open Issues
* Running Heartbeats
* Pending Approvals
* Budget Usage
* Recent Audit Events
* Failed Runs

---

### 9.2 Goal Detail

#### 표시 정보

* goal 설명
* success criteria
* 연결된 issues
* 누적 비용
* 최근 heartbeat 결과
* goal status 변경 버튼

---

### 9.3 Agent Detail

#### 표시 정보

* agent role/description
* adapter config
* monthly budget
* MCP permissions
* assigned issues
* run history
* pause/resume/terminate 버튼

---

### 9.4 Issue Detail

#### 표시 정보

* issue 설명
* goal ancestry
* assignee
* status
* heartbeat 실행 버튼
* run logs
* comments
* cost events
* approvals
* audit trail

---

### 9.5 MCP Settings

#### 표시 정보

* MCP server 목록
* server status: connected, disconnected, error
* discovered tools/resources/prompts
* agent별 permission matrix
* tool 위험도 라벨
* test call 버튼

---

### 9.6 Cost & Budget

P0에서는 전용 화면이 아니라 Dashboard, Goal Detail, Agent Detail, Issue Detail 안의 요약 패널로 제공한다. 전용 화면은 P1 이후로 둔다.

#### 표시 정보

* agent별 비용
* goal별 비용
* issue별 비용
* run별 비용
* budget remaining
* warning/hard stop events

---

### 9.7 Approvals

#### 표시 정보

* pending approval queue
* approval reason
* requested by
* related issue/run/agent
* approve/reject 버튼
* 과거 approval history

---

### 9.8 Audit Log

#### 표시 정보

* 시간순 event table
* actor
* action
* entity
* before/after diff
* runId/requestId filter
* export JSON 버튼

---

## 10. 데이터 모델 초안

### 10.1 Core Tables

```txt
users
workspaces
goals
agents
issues
runs
run_logs
mcp_servers
mcp_capabilities
agent_mcp_permissions
budgets
cost_events
approvals
audit_events
heartbeat_locks
```

### 10.2 핵심 관계

```txt
Workspace 1 ── N Goal
Goal      1 ── N Issue
Agent     1 ── N Issue
Issue     1 ── N Run
Run       1 ── N RunLog
Run       1 ── N CostEvent
Agent     1 ── N AgentMcpPermission
McpServer 1 ── N McpCapability
AnyEntity 1 ── N AuditEvent
AnyEntity 1 ── N Approval
```

---

## 11. API 초안

### Goal

```txt
GET    /api/goals
POST   /api/goals
GET    /api/goals/:goalId
PATCH  /api/goals/:goalId
POST   /api/goals/:goalId/pause
POST   /api/goals/:goalId/archive
```

### Agent

```txt
GET    /api/agents
POST   /api/agents
GET    /api/agents/:agentId
PATCH  /api/agents/:agentId
POST   /api/agents/:agentId/approve
POST   /api/agents/:agentId/pause
POST   /api/agents/:agentId/resume
POST   /api/agents/:agentId/terminate
```

### Issue

```txt
GET    /api/issues
POST   /api/issues
GET    /api/issues/:issueId
PATCH  /api/issues/:issueId
POST   /api/issues/:issueId/assign
POST   /api/issues/:issueId/heartbeat
POST   /api/issues/:issueId/cancel
```

### Run

```txt
GET    /api/runs
GET    /api/runs/:runId
GET    /api/runs/:runId/logs
GET    /api/runs/:runId/events
POST   /api/runs/:runId/cancel
```

### MCP

```txt
GET    /api/mcp/servers
POST   /api/mcp/servers
GET    /api/mcp/servers/:serverId
PATCH  /api/mcp/servers/:serverId
DELETE /api/mcp/servers/:serverId
POST   /api/mcp/servers/:serverId/discover
POST   /api/mcp/servers/:serverId/test
GET    /api/mcp/servers/:serverId/capabilities
POST   /api/agents/:agentId/mcp-permissions
```

### Budget / Approval / Audit

```txt
GET    /api/costs
GET    /api/budgets
PATCH  /api/budgets/:budgetId

GET    /api/approvals
POST   /api/approvals/:approvalId/approve
POST   /api/approvals/:approvalId/reject

GET    /api/audit-events
```

---

## 12. Heartbeat Worker 상세 설계

### 12.1 Worker 책임

```txt
heartbeat-worker.ts
  1. queued run polling
  2. issue execution lock
  3. budget check
  4. approval check
  5. MCP context loading
  6. agent adapter invocation
  7. run log persistence
  8. cost event persistence
  9. issue status update
  10. audit event persistence
```

### 12.2 처리 흐름 예시

```ts
async function executeRun(runId: string) {
  await db.transaction(async (tx) => {
    const run = await tx.runs.lock(runId)
    const issue = await tx.issues.lock(run.issueId)
    const agent = await tx.agents.get(run.agentId)

    assertAgentActive(agent)
    assertNoConcurrentIssueRun(issue.id)
    await assertBudgetAvailable(tx, { agent, issue })
    await assertApprovalsSatisfied(tx, { run, issue, agent })

    await tx.runs.markRunning(runId)
    await tx.audit.log("run.started", { runId, issueId: issue.id })
  })

  const contextPack = await mcpContextBuilder.build({ runId })

  const result = await agentAdapter.invoke({
    runId,
    issue,
    goal,
    agent,
    contextPack,
    budgetRemaining,
  })

  await persistResult(result)
}
```

---

## 13. 비기능 요구사항

### 13.1 Reliability

* 동일 issue에 대해 heartbeat는 동시에 하나만 실행된다.
* worker가 죽어도 running run은 orphan recovery 대상이 된다.
* run status 변경은 audit log와 함께 기록된다.
* MCP server 장애는 전체 app 장애로 전파되지 않는다.

### 13.2 Security

* MCP server/tool은 deny-by-default.
* MCP tool call은 agent permission과 approval policy를 통과해야 한다.
* secret/env는 UI에 평문으로 재노출하지 않는다.
* local filesystem MCP는 root path allowlist를 사용한다.
* 위험 tool은 매 호출 승인 또는 전역 차단한다.
* audit event는 application layer에서 append-only로 취급한다.

### 13.3 Performance

* Dashboard 초기 로드 2초 이내.
* Run log streaming latency 1초 이내.
* Heartbeat pre-check 500ms 이내.
* MCP discovery는 비동기 처리 가능.
* Long-running run은 UI request timeout과 분리.

### 13.4 Observability

* run별 structured logs.
* worker logs.
* MCP call logs.
* cost event logs.
* failed run reason.
* approval decision reason.

---

## 14. 성공 지표

### MVP 성공 기준

| 지표                            |           목표 |
| ----------------------------- | -----------: |
| 목표 생성 → heartbeat 실행까지 완료 가능  |         100% |
| agent 등록 후 issue 할당 가능        |         100% |
| MCP local docs context 사용 가능  | 1개 이상 server |
| run별 로그 확인 가능                 |         100% |
| budget hard stop 동작           |         100% |
| approval gate 동작              |         100% |
| audit event 누락 없는 핵심 mutation |         100% |
| 동일 issue 중복 실행 방지             |         100% |
| local self-host 설치 후 첫 run까지  |    10분 이내 목표 |

---

## 15. 구현 우선순위

### Phase 0 — Project Skeleton

* Next.js App Router
* TypeScript strict mode
* Drizzle ORM
* Postgres
* basic layout
* env config
* audit service skeleton
* single admin actor: `local_admin`

### Phase 1 — Goal / Agent / Issue CRUD + Guardrail Skeleton

* Goal CRUD
* Agent CRUD
* Agent approval
* Issue CRUD
* Issue assignment
* Audit logging
* budget policy skeleton
* approval policy skeleton
* adapter registry interface
* mock or built-in agent adapter

### Phase 2 — Manual Heartbeat MVP

* Run table
* manual heartbeat trigger
* worker loop
* run status
* run logs
* issue execution lock
* budget hard stop pre-check
* approval/policy pre-check
* cost event persistence
* audit event persistence

### Phase 3 — HTTP Webhook Adapter

* HTTP webhook adapter registration
* endpoint/auth/timeout validation
* heartbeat payload delivery
* webhook response parsing
* timeout/non-2xx/schema mismatch failure handling

### Phase 4 — MCP Integration

* MCP server registration
* stdio transport
* discovery
* tool/resource list
* agent permission matrix
* context pack builder
* MCP call audit log

### Phase 5 — Budget / Approval UX

* budget model
* cost event model
* budget warning
* hard stop
* approval queue
* approve/reject flow

### Phase 6 — Dashboard / Hardening

* dashboard cards
* run log streaming
* audit filters
* failure recovery
* MCP error handling
* basic docs/onboarding

---

## 16. 최종 MVP 기능 목록

### Must Have

1. Workspace single admin mode
2. Goal CRUD
3. Agent 등록/승인/중지
4. Issue 생성/할당
5. Manual heartbeat 실행
6. Run log 저장/조회
7. Adapter registry interface
8. Built-in LLM agent adapter 또는 mock-first adapter
9. HTTP webhook agent adapter
10. stdio MCP server 등록
11. MCP tool/resource discovery
12. Agent별 MCP permission
13. MCP context pack 생성
14. Agent/Goal/Issue budget
15. Cost event 저장
16. Budget hard stop
17. Approval queue
18. Audit log
19. Dashboard

### Should Have

1. Run log streaming
2. MCP test call
3. Approval reason
4. Budget warning threshold
5. Orphan run recovery
6. Issue comments
7. Export audit JSON
8. `local_process` adapter, local trusted mode 전용

### Could Have

1. Scheduled heartbeat
2. `agent_api_pull` adapter
3. Remote MCP HTTP transport
4. Simple artifact attachment
5. Multi-user login
6. Goal template
7. Agent template

### Won’t Have in MVP

1. Multi-company
2. Full org chart
3. Plugin runtime
4. Plugin marketplace
5. OAuth MCP
6. Cloud sandbox agents
7. Self-organization
8. Deep planning
9. Autonomous delegation
10. Mobile app
11. Desktop app

---

## 17. 제품명/포지셔닝 제안

MVP 포지셔닝은 범용 agent framework보다 좁게 잡는다.

**추천 포지셔닝**

> “Jira/Linear와 비슷한 작업 관리 도구”에서 출발하되,
> **작업자가 사람이 아니라 AI Agent인 운영 control plane.**

**핵심 메시지**

* 목표 중심으로 agent를 운영한다.
* issue 단위로 agent에게 일을 맡긴다.
* heartbeat로 agent를 깨운다.
* MCP로 agent가 필요한 지식과 도구를 얻는다.
* 비용, 승인, 감사로 runaway autonomy를 막는다.
* Jira/Linear의 협업 기능을 모두 따라가기보다, AI Agent에게 일을 맡겼을 때 필요한 실행·통제·감사 루프를 먼저 완성한다.

---

## 18. 최종 권고

MVP는 아래 스택과 범위로 시작하는 것이 가장 현실적이다.

```txt
Language: TypeScript only
Web: Next.js App Router
Runtime: Node.js self-hosted
Worker: TypeScript heartbeat worker
DB: PostgreSQL + Drizzle ORM
MCP: @modelcontextprotocol/client v1.x
UI: React + Tailwind/shadcn
Realtime logs: SSE
Deployment: Docker Compose first
```

Next.js는 UI/API를 빠르게 만들기 위한 선택으로는 좋다. 다만 이 제품의 본질은 Next.js Route Handler가 아니라 **DB-backed worker, MCP permission layer, budget/approval/audit invariant**다. 따라서 아키텍처의 중심은 Next.js가 아니라 `server/domain`과 `worker/heartbeat`에 둔다.
이 범위는 MVP로 충분하다. 첫 버전의 목표는 Jira/Linear 수준의 협업 제품을 완성하는 것이 아니라, **AI Agent가 이슈를 맡아 실행하고 그 결과와 통제 기록이 남는 한 사이클**을 증명하는 것이다.

[3]: https://nextjs.org/docs "Next.js Docs | Next.js"
[4]: https://nextjs.org/docs/app/getting-started/route-handlers-and-middleware "Getting Started: Route Handlers | Next.js"
[5]: https://nextjs.org/docs/app/guides/backend-for-frontend "Guides: Backend for Frontend | Next.js"
[6]: https://nextjs.org/docs/app/api-reference/config/next-config-js/output "next.config.js: output | Next.js"
[7]: https://hono.dev/docs/ "Hono - Web framework built on Web Standards"
[8]: https://modelcontextprotocol.io/docs/getting-started/intro "What is the Model Context Protocol (MCP)? - Model Context Protocol"
[9]: https://modelcontextprotocol.io/specification "Specification - Model Context Protocol"
[10]: https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md "raw.githubusercontent.com"


---

## 19. 부록: Agent Registration & Adapter System 보강안

**Agent 등록 기능은 MVP에서도 얕게 만들면 안 된다.**
이 제품의 본질은 “내장 agent 하나를 실행하는 도구”가 아니라, **서로 다른 agent runtime을 동일한 운영 모델로 고용·승인·할당·heartbeat·감사하는 control plane**이다.

Agent Registration의 핵심 관점은 “heartbeat를 받을 수 있으면 고용 가능하다”이다. 단, **모든 runtime을 MVP에서 똑같이 지원하지 않는다. adapter contract를 먼저 고정하고 P0 runtime은 작게 시작한다.**

따라서 PRD에서 Agent 등록 기능은 단순 CRUD가 아니라 아래처럼 재정의한다.

---

### 19.1 핵심 방향

Agent 등록은 아래 다섯 가지를 한 번에 설정하는 과정이어야 한다.

```txt
Agent Identity
+ Adapter Binding
+ Runtime Configuration
+ Permission & MCP Policy
+ Budget / Approval / Audit Policy
```

즉, “Agent 등록”은 단순히 이름과 역할을 저장하는 것이 아니라, **이 agent가 어떤 시스템에서 실행되는지, 어떻게 heartbeat를 받는지, 어떤 도구/MCP/secret/workspace에 접근 가능한지, 비용 한도는 얼마인지, 어떤 행위에 승인이 필요한지**를 정의하는 작업이다.

---

### 19.2 MVP에서의 Agent 등록 목표

MVP Agent Registration의 목표는 아래와 같다.

> 다양한 외부 agent runtime을 나중에 수용할 수 있도록 공통 adapter contract를 만들고, P0에서는 작은 adapter 집합으로 이 시스템의 heartbeat 실행 루프를 검증한다.

이 MVP는 agent를 role, permission, budget, adapter binding을 가진 운영 주체로 다룬다. 이 개념은 **작은 운영 루프** 안에서 먼저 검증한다.

---

### 19.3 Agent 등록을 독립 핵심 모듈로 승격

기존 PRD의 `Agent 고용` 섹션은 아래처럼 바꾼다.

#### 기존 표현

```txt
Agent 등록/고용
- name
- role
- adapterType
- budget
- MCP permissions
```

#### 수정 표현

```txt
Agent Registration & Hiring
- Agent Profile
- Adapter Type Selection
- Adapter Capability Discovery
- Runtime / Environment Config
- Secret Binding
- MCP Tool / Resource Permission
- Workspace Binding
- Heartbeat Contract Test
- Budget Policy
- Approval Policy
- Audit / Activity Policy
- Activation Flow
```

---

### 19.4 Agent 등록 UX

#### 19.4.1 Agent 등록 Wizard

Agent 등록은 한 화면 폼이 아니라 **wizard**로 분리한다.

```txt
Step 1. Agent 기본 정보 입력
Step 2. Adapter 유형 선택
Step 3. Adapter 연결 설정
Step 4. Runtime / Workspace / Secret 설정
Step 5. MCP 권한 설정
Step 6. Budget / Approval Policy 설정
Step 7. Heartbeat Test 실행
Step 8. 승인 후 Active 전환
```

---

#### 19.4.2 Step 1 — Agent 기본 정보

#### 입력 필드

| 필드               | 설명                                          |
| ---------------- | ------------------------------------------- |
| name             | Agent 이름. 예: Researcher-01, Claude Engineer |
| role             | 직무. 예: Researcher, Engineer, PM, Designer   |
| title            | 조직 내 직함. 예: Senior Coding Agent             |
| description      | agent가 맡는 일                                 |
| capabilities     | 자연어 또는 tag 기반 능력 설명                         |
| reportsToAgentId | 상위 manager agent. MVP에서는 nullable           |
| goalScope        | 이 agent가 주로 기여할 goal 또는 project             |
| defaultIssueMode | standard, ask, planning                     |

이 MVP의 agent profile은 `name`, `role`, `title`, `reports_to`, `capabilities`, `status`, `permissions`, `budget` 중 P0에 필요한 필드만 단순화해서 가져간다.

---

#### 19.4.3 Step 2 — Adapter 유형 선택

여기가 중요하다. MVP에서 agent를 여러 시스템과 연결하려면, Agent를 직접 실행하는 것이 아니라 **Adapter Contract**를 먼저 정의해야 한다.

#### MVP Adapter Type

| Adapter Type              | MVP 포함 | 설명                                                     |
| ------------------------- | -----: | ------------------------------------------------------ |
| `mock_agent`              |     P0 | 외부 agent 없이 run/cost/approval/audit 루프를 검증              |
| `built_in_llm`            |     P0 | 제품 dogfooding 및 demo용. `mock_agent`와 택일 가능             |
| `http_webhook`            |     P0 | 외부 agent 서버에 heartbeat payload를 POST                   |
| `local_process`           |     P1 | 로컬 CLI/프로세스를 실행. local trusted mode에서만 허용             |
| `agent_api_pull`          |     P2 | 외부 agent가 API key로 이 시스템에서 issue/run을 pull       |
| `mcp_only_tool_agent`     |     선택 | 독립 LLM 없이 MCP tool 실행 전용 agent                         |
| `external_adapter_plugin` | 구조만 준비 | MVP에서는 plugin marketplace는 제외하되 registry 구조는 열어둠       |

P0에서 봐야 할 것은 adapter 수가 아니라 contract다. `local_process`와 `agent_api_pull`은 유용하지만 보안·인증·운영 복잡도가 크므로 PRD에서는 후속 단계로 둔다.

---

### 19.5 Adapter별 등록 요구사항

#### 19.5.1 `http_webhook` Adapter

외부 agent가 HTTP endpoint를 갖고 있는 경우 사용한다.

#### 대표 대상

* OpenClaw 같은 외부 agent 서버
* 직접 만든 FastAPI/Express agent
* n8n/Make/Zapier webhook agent
* 사내 agent gateway
* remote worker bot

#### 등록 필드

| 필드                     | 설명                                 |
| ---------------------- | ---------------------------------- |
| endpointUrl            | heartbeat를 보낼 URL                  |
| method                 | 기본 POST                            |
| authType               | none, bearer, basic, custom_header |
| secretRef              | bearer token 등 secret 참조           |
| timeoutMs              | 요청 timeout                         |
| retryPolicy            | retry 횟수와 backoff                  |
| expectedResponseSchema | 응답 검증 스키마                          |
| supportsStreaming      | SSE/streaming 지원 여부                |
| healthcheckUrl         | 선택                                 |
| heartbeatMode          | push                               |

#### Heartbeat 요청 예시

```json
{
  "type": "heartbeat",
  "runId": "run_123",
  "agent": {
    "id": "agent_123",
    "name": "Researcher",
    "role": "researcher"
  },
  "goal": {
    "id": "goal_123",
    "title": "Build MVP"
  },
  "issue": {
    "id": "issue_123",
    "title": "Research adapter registration design",
    "description": "..."
  },
  "context": {
    "mcpResources": [],
    "recentComments": [],
    "budgetRemainingCents": 1500
  },
  "capabilities": {
    "canCreateIssues": true,
    "canComment": true,
    "canUseMcpTools": ["local-docs.search", "local-docs.read"]
  },
  "callback": {
    "reportStatusUrl": "/api/runs/run_123/status",
    "appendLogUrl": "/api/runs/run_123/logs",
    "reportCostUrl": "/api/runs/run_123/cost-events"
  }
}
```

#### Heartbeat 응답 예시

```json
{
  "status": "succeeded",
  "summary": "조사 완료",
  "issueStatus": "in_review",
  "comment": "Adapter registration should be treated as a first-class module...",
  "cost": {
    "provider": "custom",
    "model": "external-agent",
    "inputTokens": 0,
    "outputTokens": 0,
    "costCents": 0
  },
  "requestedActions": []
}
```

#### MVP 완료 기준

* 사용자는 HTTP endpoint 기반 agent를 등록할 수 있다.
* heartbeat 실행 시 해당 endpoint로 payload가 전송된다.
* endpoint 응답이 run log와 issue comment에 저장된다.
* timeout, non-2xx, schema mismatch는 `failed` run으로 기록된다.
* 모든 요청/응답 metadata는 audit log에 남는다.
* secret 값은 평문으로 재노출되지 않는다.

---

#### 19.5.2 `local_process` Adapter — P1

로컬 PC 또는 self-hosted 서버에서 CLI agent를 실행하는 방식이다. Claude Code, Codex, Cursor/Gemini/bash 계열 agent를 흡수하려면 이 adapter가 필요하다. 다만 실행 권한과 파일 접근 위험이 크므로 P0 필수 범위에서는 제외하고 P1로 둔다.

#### 대표 대상

* Claude Code CLI
* Codex CLI
* Gemini CLI
* OpenCode
* Cursor automation wrapper
* Bash script agent
* 자체 Node.js/TypeScript agent runner

#### 등록 필드

| 필드               | 설명                                                   |
| ---------------- | ---------------------------------------------------- |
| command          | 실행 명령. 예: `claude`, `node`, `pnpm`                   |
| argsTemplate     | heartbeat 시 주입할 인자 템플릿                               |
| workingDirectory | 실행 디렉터리                                              |
| env              | 환경변수. secretRef 사용                                   |
| stdinMode        | none, json, prompt                                   |
| outputMode       | stdout_json, stdout_text, file, streaming            |
| timeoutMs        | 최대 실행 시간                                             |
| killPolicy       | timeout 시 종료 방식                                      |
| allowedExitCodes | 성공으로 간주할 exit code                                   |
| workspaceBinding | 연결할 workspace                                        |
| fileAccessPolicy | read_only, project_write, unrestricted_local_trusted |
| networkPolicy    | allow, deny, restricted                              |

#### CLI heartbeat 입력 방식

P1에서는 두 가지 방식만 지원하면 충분하다.

#### 방식 A — stdin JSON

```txt
worker → command 실행 → stdin으로 heartbeat JSON 전달 → stdout JSON 파싱
```

#### 방식 B — temp file path

```txt
worker → heartbeat payload를 temp file에 저장 → command args에 path 전달
```

예시:

```json
{
  "command": "node",
  "argsTemplate": ["./agents/researcher.js", "--heartbeat", "{{payloadFile}}"],
  "workingDirectory": "/Users/me/projects/acme",
  "stdinMode": "none",
  "outputMode": "stdout_json"
}
```

#### 보안 정책

`local_process`는 위험도가 높으므로 P1에서는 아래 제약을 건다.

| 정책                          | 설명                             |
| --------------------------- | ------------------------------ |
| local_trusted mode에서만 기본 허용 | remote multi-user 환경에서는 기본 비활성 |
| command allowlist           | 사용자가 등록한 명령만 실행                |
| workingDirectory allowlist  | 지정된 workspace 밖 접근 제한          |
| env secretRef               | 민감값은 secret manager에서 주입       |
| timeout 필수                  | 무한 실행 방지                       |
| stdout/stderr 저장            | 감사 및 디버깅                       |
| destructive command warning | bash/sh/rm 등 고위험 명령은 승인 필요     |
| concurrent run 제한           | 동일 agent 동시 실행 제한              |

#### P1 완료 기준

* 사용자는 CLI/process agent를 등록할 수 있다.
* heartbeat 시 command가 실행되고, payload가 전달된다.
* stdout/stderr가 run log로 저장된다.
* JSON output이면 구조화된 결과로 파싱된다.
* timeout 또는 non-zero exit는 실패 run으로 기록된다.
* 실행 경로, command, args, env key 목록은 audit log에 남는다.
* secret 값은 logs/audit에 기록되지 않는다.

---

#### 19.5.3 `agent_api_pull` Adapter — P2

이 방식은 외부 agent가 시스템에 접속해 스스로 일을 가져가는 방식이다.

#### 왜 필요한가

모든 agent가 webhook을 받을 수 있는 것은 아니다. 어떤 agent는 NAT 뒤에 있거나, 로컬 노트북에서 실행되거나, cron/daemon 형태로 주기적으로 서버에 접속한다. 이 경우 시스템이 push하는 것이 아니라 agent가 pull해야 한다.

agent_api_pull 방식에서는 agent auth를 “Bearer API key mapped to one agent and workspace”로 단순화하고, agent가 자기 assigned issues/comments, heartbeat status, cost events만 다루게 한다. 이 PRD에서는 이 방식을 P2로 둔다.

#### 등록 필드

| 필드                 | 설명                                       |
| ------------------ | ---------------------------------------- |
| apiKeyName         | key 이름                                   |
| apiKeyHash         | 저장은 hash만                                |
| allowedScopes      | issue read/write, comment, cost report 등 |
| callbackMode       | pull                                     |
| pollingHintSeconds | 권장 polling 간격                            |
| allowedOrigins     | 선택                                       |
| expiresAt          | 선택                                       |
| revokedAt          | 선택                                       |

#### Agent API 최소 엔드포인트

```txt
GET  /api/agent/me
GET  /api/agent/issues/assigned
POST /api/agent/issues/:issueId/checkout
POST /api/agent/runs/:runId/logs
POST /api/agent/runs/:runId/status
POST /api/agent/runs/:runId/cost-events
POST /api/agent/issues/:issueId/comments
POST /api/agent/issues
```

#### P2 완료 기준

* agent API key는 생성 시 한 번만 평문 노출된다.
* DB에는 hash만 저장된다.
* key는 특정 agent와 workspace에만 연결된다.
* agent는 자기 회사/자기 권한 범위 밖 리소스에 접근할 수 없다.
* agent는 approval gate를 우회할 수 없다.
* agent의 모든 mutation은 actor=`agent`로 audit log에 남는다.

---

#### 19.5.4 `built_in_llm` Adapter

MVP demo와 자체 사용성 검증을 위해 내장 agent 하나는 필요하다. 단, 이 adapter를 제품의 중심으로 만들면 안 된다. 중심은 BYO agent다.

#### 역할

* 외부 agent 없이도 제품을 시연 가능하게 함
* issue를 읽고 comment/summary 생성
* MCP resource/tool을 호출해 context 보강
* 비용 추적 구현 검증
* approval/budget/audit 루프 검증

#### 등록 필드

| 필드            | 설명                                 |
| ------------- | ---------------------------------- |
| provider      | openai, anthropic, local_gateway 등 |
| model         | 모델명                                |
| systemPrompt  | agent 역할 지시                        |
| temperature   | 선택                                 |
| maxTokens     | 선택                                 |
| toolUsePolicy | MCP tool 사용 정책                     |
| costProfile   | 비용 계산 profile                      |

#### MVP 완료 기준

* built-in agent는 issue context를 읽고 응답을 생성한다.
* 허용된 MCP resource/tool만 사용할 수 있다.
* token/cost event를 기록한다.
* budget 초과 시 실행이 차단된다.
* 결과는 issue comment와 run log에 저장된다.

---

#### 19.5.5 `external_adapter_plugin`

이 기능은 MVP에서 완성하지 않아도 된다. 다만 **데이터 모델과 registry 구조는 처음부터 열어두는 것**이 좋다.

따라서 MVP에서도 아래 원칙을 가져간다.

```txt
shared schema는 adapterType을 hardcoded enum으로 닫지 않는다.
server registry가 실제 등록 여부를 검증한다.
UI는 registry metadata를 보고 동적으로 form을 렌더링한다.
```

#### MVP에서는 하지 않을 것

* plugin marketplace
* npm plugin install UI
* third-party plugin sandbox
* remote plugin distribution
* plugin-specific UI contribution

#### MVP에서 할 것

* adapter registry interface 정의
* built-in adapters도 registry에 등록
* adapter type은 string으로 저장
* adapter별 config schema를 registry에서 제공
* unknown adapter type은 server에서 거부
* adapter config validation은 adapter가 담당

---

### 19.6 Agent Adapter Interface

MVP에서 먼저 고정할 것은 아래 TypeScript interface다.

```ts
export type AgentAdapterType =
  | "mock_agent"
  | "built_in_llm"
  | "http_webhook"
  | "local_process"
  | "agent_api_pull"
  | string;

export interface AgentAdapterDefinition<TConfig = unknown> {
  type: AgentAdapterType;
  displayName: string;
  description: string;

  riskLevel: "low" | "medium" | "high";
  heartbeatMode: "push" | "pull" | "process";

  configSchema: unknown; // zod schema 권장
  defaultConfig?: Partial<TConfig>;

  capabilities: {
    supportsStreamingLogs: boolean;
    supportsCostReporting: boolean;
    supportsCancellation: boolean;
    supportsHealthcheck: boolean;
    supportsMcpContextInjection: boolean;
    supportsWorkspaceBinding: boolean;
    supportsSecrets: boolean;
  };

  validateConfig(config: TConfig): Promise<AdapterValidationResult>;

  testConnection?(config: TConfig): Promise<AdapterTestResult>;

  detectModels?(config: TConfig): Promise<AdapterModelInfo[]>;

  invokeHeartbeat?(
    input: HeartbeatInvocationInput,
    config: TConfig
  ): Promise<HeartbeatInvocationResult>;

  cancelRun?(
    input: CancelRunInput,
    config: TConfig
  ): Promise<CancelRunResult>;
}
```

---

### 19.7 Agent Registration Data Model

#### 19.7.1 `agents`

```ts
agents {
  id: uuid
  workspaceId: uuid

  name: text
  role: text
  title: text | null
  description: text | null
  capabilities: text | null

  status:
    | "draft"
    | "pending_approval"
    | "active"
    | "idle"
    | "running"
    | "paused"
    | "error"
    | "budget_exhausted"
    | "terminated"

  reportsToAgentId: uuid | null

  adapterType: text
  adapterConfig: jsonb
  runtimeConfig: jsonb

  contextMode: "thin" | "fat"
  defaultWorkspaceId: uuid | null

  budgetMonthlyCents: integer
  spentMonthlyCents: integer

  permissions: jsonb
  metadata: jsonb

  lastHeartbeatAt: timestamptz | null
  createdAt: timestamptz
  updatedAt: timestamptz
}
```

#### 19.7.2 `agent_api_keys` — P2

```ts
agent_api_keys {
  id: uuid
  agentId: uuid
  workspaceId: uuid

  name: text
  keyHash: text
  scopes: jsonb

  lastUsedAt: timestamptz | null
  expiresAt: timestamptz | null
  revokedAt: timestamptz | null

  createdAt: timestamptz
}
```

#### 19.7.3 `agent_adapter_registrations`

이 테이블은 adapter registry를 DB에 저장하고 UI에서 동적 렌더링하기 위한 용도다.

```ts
agent_adapter_registrations {
  id: uuid

  type: text unique
  displayName: text
  description: text
  source: "built_in" | "local_plugin" | "manual"
  status: "enabled" | "disabled" | "error"

  configSchema: jsonb
  uiSchema: jsonb | null
  capabilityManifest: jsonb

  riskLevel: "low" | "medium" | "high"
  createdAt: timestamptz
  updatedAt: timestamptz
}
```

MVP에서는 built-in adapter만 등록해도 된다. 그러나 이 구조를 두면 나중에 external adapter plugin을 붙일 때 core schema를 갈아엎지 않아도 된다.

#### 19.7.4 `agent_mcp_permissions`

```ts
agent_mcp_permissions {
  id: uuid
  agentId: uuid
  mcpServerId: uuid

  allowedTools: text[]
  deniedTools: text[]
  allowedResources: text[]
  approvalRequiredTools: text[]

  createdAt: timestamptz
  updatedAt: timestamptz
}
```

#### 19.7.5 `agent_config_revisions`

Agent config 변경은 rollback과 audit을 위해 revision을 남겨야 한다.

```ts
agent_config_revisions {
  id: uuid
  agentId: uuid

  revisionNumber: integer
  changedByActorType: "user" | "agent" | "system"
  changedByActorId: text

  before: jsonb
  after: jsonb
  redactedDiff: jsonb

  changeReason: text | null
  createdAt: timestamptz
}
```

---

### 19.8 Agent 등록 상태 머신

Agent는 단순히 `active/inactive`가 아니라 등록과 승인 단계를 가져야 한다.

```txt
draft
  ↓
pending_approval
  ↓ approve
active / idle
  ↓ heartbeat start
running
  ↓ success
idle
  ↓ pause
paused
  ↓ resume
idle
  ↓ error
error
  ↓ recover
idle
  ↓ terminate
terminated
```

#### 상태 정의

| 상태                 | 의미                 |
| ------------------ | ------------------ |
| `draft`            | 설정 중. heartbeat 불가 |
| `pending_approval` | 등록 완료, local admin 승인 대기 |
| `active` / `idle`  | 실행 가능              |
| `running`          | heartbeat 실행 중     |
| `paused`           | 수동 중지 또는 정책 중지     |
| `error`            | 연결/설정/실행 오류        |
| `budget_exhausted` | 예산 소진으로 자동 중지      |
| `terminated`       | 영구 종료. 복구 불가       |

이 MVP에서도 terminated agent는 resume할 수 없다는 불변조건을 유지해야 한다.

---

### 19.9 Agent 등록 시 검증해야 하는 것

Agent 등록 완료 전에는 아래 검증을 통과해야 한다.

#### 19.9.1 Profile Validation

* name 필수
* role 필수
* 동일 workspace 내 name 중복 경고
* reportsTo가 자기 자신이면 거부
* manager tree cycle 거부

#### 19.9.2 Adapter Validation

* adapterType이 registry에 존재해야 함
* adapterConfig가 adapter schema를 통과해야 함
* 필수 secretRef가 존재해야 함
* P1 `local_process`를 활성화한 경우 command가 허용 정책을 통과해야 함
* HTTP endpoint가 URL 형식이어야 함
* P2 `agent_api_pull`을 활성화한 경우 API key가 생성되어야 함

#### 19.9.3 Runtime Validation

* workspace path가 존재해야 함
* workspace 접근 권한 확인
* timeout 설정 필수
* max concurrency 확인
* context mode 확인

#### 19.9.4 MCP Permission Validation

* 지정된 MCP server가 enabled 상태여야 함
* allowedTools가 discovery된 tool 목록에 존재해야 함
* high-risk tool은 approval policy가 있어야 함
* write/delete/execute 계열 tool은 기본 차단

#### 19.9.5 Budget Validation

* monthly budget >= 0
* issue-level budget override 정책 확인
* 0 budget agent는 cost-incurring adapter 실행 불가 또는 warning

#### 19.9.6 Heartbeat Contract Test

등록 마지막 단계에서 반드시 테스트한다.

```txt
1. adapter config validation
2. connection test
3. dry-run heartbeat
4. log collection test
5. cancellation support check, 가능할 경우
6. cost report schema check
```

---

### 19.10 Agent 등록 API

#### 19.10.1 Adapter Registry API

```txt
GET    /api/adapters
GET    /api/adapters/:type
POST   /api/adapters/:type/test-config
POST   /api/adapters/:type/detect-models
POST   /api/adapters/:type/validate-config
```

#### 19.10.2 Agent Registration API

```txt
GET    /api/agents
POST   /api/agents
GET    /api/agents/:agentId
PATCH  /api/agents/:agentId

POST   /api/agents/:agentId/submit-for-approval
POST   /api/agents/:agentId/approve
POST   /api/agents/:agentId/reject

POST   /api/agents/:agentId/test-heartbeat
POST   /api/agents/:agentId/pause
POST   /api/agents/:agentId/resume
POST   /api/agents/:agentId/terminate
```

#### 19.10.3 Agent API Key API — P2

```txt
GET    /api/agents/:agentId/api-keys
POST   /api/agents/:agentId/api-keys
POST   /api/agents/:agentId/api-keys/:keyId/revoke
```

#### 19.10.4 Agent MCP Permission API

```txt
GET    /api/agents/:agentId/mcp-permissions
PUT    /api/agents/:agentId/mcp-permissions
POST   /api/agents/:agentId/mcp-permissions/test
```

---

### 19.11 Agent 등록 화면 구성

#### 19.11.1 Agents List

표시 항목:

| 컬럼              | 설명                            |
| --------------- | ----------------------------- |
| Name            | agent 이름                      |
| Role            | 직무                            |
| Adapter         | http_webhook, local_process 등 |
| Status          | idle, running, paused 등       |
| Assigned Issues | 할당된 이슈 수                      |
| Budget Used     | 월 예산 사용량                      |
| Last Heartbeat  | 마지막 실행 시각                     |
| Health          | 연결 상태                         |

#### 19.11.2 New Agent Wizard

#### Step 1. Profile

* name
* role
* title
* description
* reportsTo
* capabilities

#### Step 2. Adapter

Adapter card 형태로 제공:

```txt
HTTP/Webhook Agent
Local CLI/Process Agent
Agent API Pull Agent
Built-in LLM Agent
```

각 card에는 아래 항목을 보여준다.

* 용도
* 위험도
* 필요한 설정
* supports heartbeat push/pull/process
* supports streaming/cancellation/cost

#### Step 3. Adapter Config

adapterType에 따라 동적 form 렌더링.

예:

`http_webhook`

* endpoint URL
* auth method
* secret
* timeout
* response schema mode

`local_process`

* command
* args
* working directory
* env
* output parser
* timeout

`agent_api_pull`

* API key 생성
* scopes
* polling instruction
* agent bootstrap snippet

#### Step 4. Runtime

* default workspace
* context mode: thin/fat
* max runtime
* concurrency
* retry policy
* cancellation policy

#### Step 5. MCP

* MCP server 선택
* tool allowlist
* resource allowlist
* high-risk tool approval
* context injection mode

#### Step 6. Budget & Approval

* monthly budget
* per-run budget
* issue budget override 허용 여부
* new issue creation 허용 여부
* destructive action approval
* completion approval

#### Step 7. Test

* adapter config validation
* healthcheck
* dry-run heartbeat
* MCP permission test
* sample run log
* expected result preview

#### Step 8. Submit / Approve

* local trusted mode에서는 바로 activate 가능
* governed mode에서는 pending approval 생성
* 승인 후 active 전환

---

### 19.12 Agent Registration에서 반드시 남겨야 하는 Audit Event

| Action                           | 설명                     |
| -------------------------------- | ---------------------- |
| `agent.created`                  | draft 생성               |
| `agent.adapter_configured`       | adapter type/config 설정 |
| `agent.secret_bound`             | secretRef 연결           |
| `agent.mcp_permission_updated`   | MCP 권한 변경              |
| `agent.budget_updated`           | 예산 변경                  |
| `agent.test_heartbeat_started`   | 테스트 실행                 |
| `agent.test_heartbeat_succeeded` | 테스트 성공                 |
| `agent.test_heartbeat_failed`    | 테스트 실패                 |
| `agent.submitted_for_approval`   | 승인 요청                  |
| `agent.approved`                 | 승인                     |
| `agent.rejected`                 | 거절                     |
| `agent.activated`                | active 전환              |
| `agent.paused`                   | 중지                     |
| `agent.resumed`                  | 재개                     |
| `agent.terminated`               | 종료                     |
| `agent.api_key_created`          | API key 생성             |
| `agent.api_key_revoked`          | API key 폐기             |

이 MVP는 activity log와 approval 우회 금지를 P0 원칙으로 가져가고, agent API key는 P2의 agent/workspace 매핑으로 단순화한다.

---

### 19.13 MVP 범위

#### MVP Must Have

```txt
1. Agent Registration Wizard
2. Adapter Registry
3. Built-in adapter metadata
4. mock_agent 또는 built_in_llm demo adapter
5. http_webhook adapter
6. Adapter config validation
7. Test heartbeat
8. Agent MCP permission matrix
9. Agent budget policy
10. Agent approval flow
11. Agent config revision/audit log
```

여기서 중요한 판단은 하나다.

> **Adapter 수는 제한하되, Adapter 구조는 처음부터 확장 가능하게 만든다.**

즉, MVP에서 Claude Code, Codex, Cursor, OpenClaw, Gemini, bash를 각각 완성도 높게 모두 지원하려고 하면 과하다. 대신 아래처럼 흡수한다.

| 실제 시스템             | PRD에서의 수용 단계                              |
| ------------------ | ----------------------------------------- |
| OpenClaw           | P0에서는 `http_webhook`, P2에서 `agent_api_pull` 검토 |
| Claude Code        | P1 `local_process`                         |
| Codex CLI          | P1 `local_process`                         |
| Cursor automation  | P1 `local_process` 또는 P0 `http_webhook` wrapper |
| Gemini CLI         | P1 `local_process`                         |
| Bash script        | P1 `local_process`                         |
| 직접 만든 agent 서버     | P0 `http_webhook`                          |
| 장기 실행 agent daemon | P2 `agent_api_pull`                        |
| 제품 내장 agent        | P0 `mock_agent` 또는 `built_in_llm`          |

이렇게 하면 “다양한 agent 지원”이라는 제품 가치는 유지하면서도 MVP 구현 복잡도는 통제할 수 있다.

---

### 19.14 Agent 등록과 MCP의 관계

Agent 등록 시 MCP 권한은 반드시 함께 설정한다.

```txt
Agent = 실행 주체
Adapter = 실행 방식
MCP = 사용할 수 있는 지식/도구
Permission = 어떤 MCP를 어디까지 쓸 수 있는지
Approval = 위험한 도구를 쓰기 전 누가 승인하는지
Audit = 실제로 무엇을 썼는지 기록
```

예를 들어 local docs를 보는 Research Agent는 아래처럼 등록한다.

```json
{
  "name": "Local Researcher",
  "role": "Researcher",
  "adapterType": "built_in_llm",
  "adapterConfig": {
    "provider": "openai",
    "model": "gpt-5.5"
  },
  "runtimeConfig": {
    "contextMode": "fat",
    "maxRuntimeMs": 300000
  },
  "mcpPermissions": [
    {
      "server": "local-docs",
      "allowedTools": ["search_files", "read_file"],
      "deniedTools": ["write_file", "delete_file", "execute_command"]
    }
  ],
  "budgetMonthlyCents": 2000,
  "approvalPolicy": {
    "requireApprovalForHighRiskTools": true,
    "requireApprovalForBudgetOverride": true
  }
}
```

반대로 Claude Code 계열 Engineer Agent는 아래처럼 등록한다.

```json
{
  "name": "Claude Engineer",
  "role": "Engineer",
  "adapterType": "local_process",
  "adapterConfig": {
    "command": "claude",
    "argsTemplate": ["--print", "--input", "{{payloadFile}}"],
    "workingDirectory": "/Users/me/projects/app",
    "outputMode": "stdout_text",
    "timeoutMs": 900000
  },
  "runtimeConfig": {
    "workspaceBinding": "project-default",
    "fileAccessPolicy": "project_write",
    "maxConcurrentRuns": 1
  },
  "mcpPermissions": [
    {
      "server": "local-docs",
      "allowedTools": ["read_file", "search_files"]
    }
  ],
  "budgetMonthlyCents": 5000
}
```

---

### 19.15 Heartbeat 실행 시 Adapter Resolution

Heartbeat worker는 아래 순서로 agent를 실행한다.

```txt
1. run 생성
2. issue lock
3. agent 조회
4. agent status 확인
5. adapterType 조회
6. adapter registry에서 adapter definition 로드
7. adapterConfig validation
8. budget check
9. approval check
10. MCP permission check
11. context pack 생성
12. adapter.invokeHeartbeat 또는 pull-mode wakeup 생성
13. run logs 저장
14. cost events 저장
15. issue status 갱신
16. audit event 저장
```

의사 코드:

```ts
async function executeHeartbeat(runId: string) {
  const run = await runs.get(runId);
  const agent = await agents.get(run.agentId);

  const adapter = adapterRegistry.require(agent.adapterType);

  await assertAgentCanRun(agent);
  await adapter.validateConfig(agent.adapterConfig);
  await assertBudgetAvailable(agent, run);
  await assertApprovalsSatisfied(agent, run);
  await assertMcpPermissions(agent, run);

  const contextPack = await buildContextPack({
    agent,
    issueId: run.issueId,
    mode: agent.contextMode,
  });

  if (adapter.heartbeatMode === "pull") {
    await createWakeupRequest({ agent, run, contextPack });
    return;
  }

  const result = await adapter.invokeHeartbeat({
    run,
    agent,
    issue,
    goal,
    contextPack,
    callbacks: createRunCallbacks(run),
  }, agent.adapterConfig);

  await persistHeartbeatResult(result);
}
```

---

### 19.16 Agent 등록 PRD 완료 기준

Agent Registration MVP는 아래 기준을 통과해야 한다.

#### Functional

* 사용자는 P0 adapter인 `mock_agent`/`built_in_llm` 또는 `http_webhook`으로 agent를 등록할 수 있다.
* 등록된 agent는 `draft → pending_approval → active` 흐름을 가진다.
* adapter별 config form이 다르게 렌더링된다.
* adapter config는 저장 전 validation된다.
* P0에서는 agent API key 없이 user-triggered heartbeat와 webhook secret만 다룬다.
* agent별 MCP server/tool/resource 권한을 설정할 수 있다.
* agent별 budget을 설정할 수 있다.
* agent 등록/수정/승인/중지/종료는 audit log에 기록된다.
* 등록 직후 test heartbeat를 실행할 수 있다.
* test heartbeat 실패 시 active 전환이 차단된다.
* P0 heartbeat는 `mock_agent`/`built_in_llm` 또는 HTTP 방식으로 분기된다.

#### Security

* unknown adapter type은 서버에서 거부된다.
* secret은 평문 저장되지 않는다.
* P1의 `local_process`는 local trusted/self-hosted mode에서만 기본 허용된다.
* P2의 agent API key는 hash만 저장된다.
* agent는 approval gate를 우회할 수 없다.
* agent는 허용되지 않은 MCP tool을 호출할 수 없다.
* high-risk MCP tool은 승인 없이는 실행되지 않는다.

#### Observability

* agent health status가 표시된다.
* 마지막 heartbeat 시각이 표시된다.
* 마지막 heartbeat 실패 이유가 표시된다.
* adapter test 결과가 저장된다.
* run log에서 adapter invocation payload metadata를 볼 수 있다.
* 비용은 agent/issue/run 단위로 집계된다.

---

### 19.17 최종 PRD 구조 반영안

전체 PRD에서는 Agent 관련 장을 별도 상위 챕터로 분리한다.

```txt
1. Product Overview
2. Core Workflow
3. Goals
4. Agent Registration & Adapter System   ← 독립 핵심 장
5. Issues
6. Heartbeat Execution
7. MCP Integration
8. Budget & Cost
9. Approval & Governance
10. Audit Log
11. UI Requirements
12. Data Model
13. API
14. Non-functional Requirements
15. MVP Scope
16. Roadmap
```

Agent Registration 장 내부는 아래 구조가 좋다.

```txt
4.1 Concept
4.2 Agent Profile
4.3 Adapter Registry
4.4 Supported MVP Adapters
4.5 Adapter Config Schemas
4.6 Agent API Keys (P2)
4.7 Runtime / Workspace Binding
4.8 MCP Permissions
4.9 Budget / Approval Policy
4.10 Heartbeat Contract Test
4.11 Agent State Machine
4.12 Audit Events
4.13 Acceptance Criteria
```

---

### 19.18 최종 판단

Agent 등록은 MVP에서도 **깊게** 가져가야 한다. 
다만 “깊게”의 의미는 모든 외부 agent를 완벽 지원한다는 뜻이 아니다.

정확한 MVP 전략은 이렇다.

```txt
지원 adapter 수는 작게 시작한다.
하지만 adapter registry, config schema, heartbeat contract, MCP permission, budget, approval, audit 구조는 처음부터 제대로 만든다.
```

따라서 MVP에서 Agent 등록은 아래 adapter cut을 1차 기준으로 삼는다.

```txt
P0
1. mock_agent 또는 built_in_llm
2. http_webhook

P1
3. local_process

P2
4. agent_api_pull
```

이렇게 자르면 P0에서 핵심 운영 루프를 검증하면서도, 이후 대부분의 agent system을 포괄할 확장 경로를 남길 수 있다.

* 자체 demo와 기본 agent는 `mock_agent` 또는 `built_in_llm`
* 서버형 agent는 `http_webhook`
* 로컬 CLI agent는 P1 `local_process`
* daemon/polling agent는 P2 `agent_api_pull`

그리고 이 모든 agent는 동일한 운영 루프에 올라간다.

```txt
Agent 등록
→ 승인
→ 이슈 할당
→ heartbeat
→ MCP context/tool 사용
→ 비용 기록
→ 승인/감사 확인
```

이 구조가 있어야 **“다양한 agent를 하나의 운영 루프에서 안전하게 관리한다”**는 방향이 MVP에서도 살아난다.

---

## 20. 기술 설계 보강 (Implementation-Ready)

1~19장은 “무엇을 만들 것인가”를 정의했다. 이 장은 “**어떻게 만들 것인가**”를 채운다.

기존 장들이 `budget hard stop`, `audit append-only`, `run lock` 같은 **불변조건(invariant)**을 선언했다면, 이 장은 그 invariant를 실제로 강제하는 **실행 메커니즘(mechanism)**을 정의한다. invariant 없는 메커니즘은 의미 없고, 메커니즘 없는 invariant는 구현 단계에서 증발한다.

이 장은 **구현 착수 전 반드시 정해져야 할 기술 결정**을 다룬다. 즉, Phase 0 코드를 한 줄도 쓰기 전에 이 결정들이 없으면 코딩이 멈추는 항목들이다.

> **통화 단위 정정**: 기존 장들에 등장하는 `monthlyBudgetCents`, `estimatedCostUsd`, `costCents` 등의 표기는 historical이다. 본 장 20.4에서 **원(KRW) 정수**로 통일하며, 실제 구현에서는 본 장 기준을 따른다.

> **상태머신 정정**: 2.4 Agent 상태표와 19.8 상태머신이 충돌한다. 본 장 20.9에서 **19.8을 단일 진본**으로 채택하며, 2.4는 참조용으로 둔다.

---

### 20.1 인증 & Actor 주입

기존 PRD는 `local_admin` 단일 actor라고만 선언했다. 하지만 actor를 식별하는 **파이프**가 없으면 audit의 `actorId` 컬럼을 채울 수 없고, CSRF/인증 없이 mutation API를 열어두면 2.6 불변조건이 무력화된다.

#### 20.1.1 Single Admin 시드

최초 부팅 시 단일 workspace와 `local_admin` user를 자동 생성한다.

```txt
ACP_BOOTSTRAP_ADMIN_PASSWORD env (필수)
  ↓ 첫 시작 감지 (workspaces 테이블 비어 있음)
  ↓ bcrypt 해시 저장
workspace: default
users: { id, email: "admin@local", role: "local_admin", passwordHash }
```

두 번째 부팅부터는 시드를 건너뛴다. 비밀번호 재설정은 CLI 스크립트(`pnpm bootstrap:reset-admin`)로만 가능하다.

#### 20.1.2 세션 인증

| 항목 | 결정 |
| --- | --- |
| 매커니즘 | 세션 쿠키 (DB-backed session) |
| 쿠키 이름 | `acp_session` |
| 속성 | `httpOnly; secure(prod); sameSite=strict; path=/` |
| 저장 | `sessions` 테이블 (id, userId, expiresAt, createdAt, lastSeenAt) |
| 만료 | 7일 sliding (활동 시 갱신) |
| 무효화 | 로그아웃 / 비밀번호 변경 시 전체 세션 삭제 |

JWT가 아닌 DB 세션을 쓰는 이유: P0는 single admin이라 overhead가 작고, 세션 철회가 즉시 가능해야 2.6 audit invariant를 신뢰할 수 있다.

#### 20.1.3 Actor 주입 파이프

Next.js 미들웨어(`middleware.ts`)가 모든 요청에서 actor를 추출해 Route Handler에 전달한다.

```txt
Request
  ↓ middleware: 쿠키 → sessions 조회 → user 로드
  ↓ actor = { type: "user", id: user.id, role: "local_admin" }
  ↓ request.actor 주입 (또는 header x-acp-actor-id, internal-only)
  ↓ Route Handler: 모든 mutation 호출에 actor 명시 필수
```

Route Handler는 `requireActor(request)` 헬퍼로 actor를 강제한다. actor 없는 mutation은 500이 아니라 401로 거부된다.

#### 20.1.4 Actor 유형

| Actor type | 언제 | actorId |
| --- | --- | --- |
| `user` | 브라우저 요청 | `users.id` |
| `system` | worker 자동 처리 (orphan recovery 등) | `system` 고정값 |
| `agent` | webhook 콜백 / agent API (P2) | `agents.id` |
| `mcp` | MCP 자체 호출 (드묾) | `mcp_servers.id` |

audit event의 `actorType`/`actorId`는 항상 이 값 중 하나로 채워진다. 빈 값은 허용하지 않는다.

#### 20.1.5 CSRF 보호

P0 mutation API는 전부 POST/PATCH/DELETE다. CSRF는 두 겹으로 막는다.

1. `sameSite=strict` 쿠키 (기본 방어)
2. 모든 mutation 요청의 `Origin` 헤더 검증 (허용 host: `127.0.0.1`, `localhost`, 설정된 `ACP_PUBLIC_ORIGIN`)

두 겹 모두 통과해야 mutation이 실행된다.

#### 20.1.6 네트워크 바인딩

| 항목 | 기본값 | 비고 |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | localhost-only |
| `PORT` | `3000` (web), `3001` (worker metrics) | |
| 외부 노출 | 사용자 책임 | reverse proxy + TLS 권장 |

localhost-only 기본값은 2.6 `local_admin actor` invariant와 일치한다. 외부 노출을 원하면 사용자가 reverse proxy와 TLS를 직접 설정해야 하며, 문서에 명시적으로 경고한다.

#### 20.1.7 멱등성 (Idempotency)

중복 호출로 인한 부작용(run 2개 생성, cost event 중복 적립)을 막기 위해 주요 mutation에 idempotency key를 도입한다.

| 엔드포인트 | 멱등 키 | 키 TTL |
| --- | --- | --- |
| `POST /api/issues/:id/heartbeat` | `Idempotency-Key` 헤더 | 24시간 |
| `POST /api/approvals/:id/approve` | `Idempotency-Key` 헤더 | 24시간 |
| `POST /api/approvals/:id/reject` | `Idempotency-Key` 헤더 | 24시간 |
| webhook 콜백 (`/api/runs/:id/logs`) | `X-Run-Callback-Seq` | run 종료 시까지 |

같은 키로 두 번째 요청이 오면 첫 번째 응답을 재반환한다. `idempotency_keys` 테이블에 (key, responseHash, expiresAt)을 저장한다.

---

### 20.2 시크릿 관리 (Secret Store)

PRD 전체에 `secretRef`가 등장하지만 시크릿 값이 어디에 저장되는지는 한 줄도 없었다. 이게 없으면 `http_webhook` bearer token, `built_in_llm` LLM API key, MCP env 값을 어디에도 둘 수 없다.

#### 20.2.1 저장 모델

env에서 주입되는 마스터키로 DB의 시크릿 값을 AES-256-GCM 암호화해 저장한다.

```txt
ACP_SECRET_MASTER_KEY (env, 32 bytes base64)
  ↓ 메모리에만 로드 (시작 시 1회)
  ↓ secretService.encrypt(plaintext) → { ciphertext, iv, tag }
  ↓ secrets 테이블에 저장
```

#### 20.2.2 `secrets` 테이블

```ts
secrets {
  id: uuid                // sec_<ulid>
  workspaceId: uuid

  name: text              // 사람이 읽을 수 있는 이름
  description: text | null

  ciphertext: bytea       // AES-256-GCM ciphertext
  iv: bytea               // GCM nonce (12 bytes)
  tag: bytea              // GCM auth tag (16 bytes)

  // 평문은 어디에도 저장되지 않는다

  lastUsedAt: timestamptz | null
  createdByActorType: text
  createdByActorId: text

  createdAt: timestamptz
  revokedAt: timestamptz | null   // revoke 시에도 row는 보존 (감사)
}
```

#### 20.2.3 `secretRef` 포맷

adapter config 안에서 시크릿 값을 placeholder로 참조한다.

```txt
secretRef := "sec_<id>"
예: "sec_01HZX..."
```

worker가 adapter config를 메모리에 로드할 때 placeholder를 실제 평문으로 치환한다. 이 치환은 **worker 프로세스 메모리 내에서만** 일어나며, 치환된 평문은 DB, audit, run log, UI에 절대 기록되지 않는다.

#### 20.2.4 재노출 정책

| 위치 | 평문 노출 | 비고 |
| --- | --- | --- |
| API 응답 | 금지 | `secrets` 조회 시 메타데이터만 반환 |
| Audit event | 금지 | before/after diff에서 평문 제거 |
| Run log | 금지 | adapter 호출 payload에서 평문 redaction |
| UI | 금지 | 마스킹 표시 (`••••••`) |
| 등록 시 | 1회만 | UI에서 “이 값은 다시 보여주지 않습니다” 경고 |

등록 폼에서 평문을 받아 바로 암호화하고, 프론트엔드에 임시 표시 후 폐기한다.

#### 20.2.5 마스터키 운영

| 항목 | 결정 |
| --- | --- |
| 길이 | 32 bytes (AES-256) |
| 인코딩 | base64 |
| env 변수명 | `ACP_SECRET_MASTER_KEY` |
| 교체 | P0에선 미지원. 교체 스크립트는 P1 |
| 누락 시 | 부팅 즉시 실패 (fail-fast) |

마스터키 없이 부팅하면 worker와 web 모두 시작을 거부한다. 이것이 2.6 `secret redaction` invariant의 실행 메커니즘이다.

#### 20.2.6 사용 예시

`http_webhook` adapter config:

```json
{
  "endpointUrl": "https://agent.example.com/heartbeat",
  "authType": "bearer",
  "secretRef": "sec_01HZX...",
  "timeoutMs": 30000
}
```

worker가 heartbeat를 보낼 때:

```txt
adapter config 로드
  ↓ secretRef 발견
  ↓ secretService.decrypt() 호출 (메모리)
  ↓ Authorization: Bearer <plaintext> 헤더에 주입
  ↓ HTTP 요청 전송
  ↓ 요청 완료 후 메모리에서 plaintext 변수 스코프 종료
```

---

### 20.3 동시성 제어 & 잠금

2.6은 “동일 issue에는 running run이 동시에 2개 이상 존재할 수 없다”고 선언했다. 하지만 12.2의 `tx.runs.lock(runId)`는 의사코드일 뿐, Postgres에서 이 lock을 어떻게 구현하는지가 없었다. 이 결정이 없으면 Phase 2에서 데드락과 중복 실행 이슈가 발생한다.

#### 20.3.1 잠금 전략 개요

세 겹의 잠금을 사용한다. 각각이 보호하는 범위가 다르다.

| 겹 | 매커니즘 | 보호 대상 | 지속 |
| --- | --- | --- | --- |
| 1 | Partial unique index | issue당 running run 1개 강제 | 영구 (DB 제약) |
| 2 | `pg_advisory_xact_lock` | 짧은 critical section 보호 | 트랜잭션 내 |
| 3 | Lease-TTL (`heartbeat_locks`) | worker crash 후 복구 | run 종료 시까지 |

#### 20.3.2 Partial Unique Index (1겹)

`runs` 테이블에 부분 유니크 인덱스를 건다.

```sql
CREATE UNIQUE INDEX runs_one_running_per_issue
  ON runs (issueId)
  WHERE status = 'running';
```

이 인덱스가 있으면 같은 issue에 두 번째 `running` run을 INSERT하려는 순간 DB가 거부한다. 이것이 **가장 강력하고 단순한 동시성 보장**이다. 애플리케이션 로직에 의존하지 않는다.

상태가 `running`이 되는 시점에만 제약이 걸리고, `succeeded`/`failed` 등으로 전환되면 즉시 제약이 풀려 다음 run이 가능하다.

#### 20.3.3 Advisory Lock (2겹)

Partial unique index는 결과적 보장이지만, 두 worker가 동시에 같은 issue를 claim하는 경합 자체는 여전히 발생한다. 이 경합을 짧은 critical section 안으로 가둔다.

```sql
BEGIN;
  SELECT pg_advisory_xact_lock(hashtext(issueId));
  -- 이 안에서만 run 상태 검사 + claim
  UPDATE runs SET status = 'running', claimedAt = now()
    WHERE id = runId AND status = 'queued';
COMMIT;
```

`pg_advisory_xact_lock`은 트랜잭션 종료 시 자동 해제된다. 별도 cleanup이 필요 없다.

#### 20.3.4 Lease-TTL (3겹)

`heartbeat_locks` 테이블로 worker가 run을 실행하는 동안 lease를 유지한다. worker가 죽었을 때 orphan run을 복구하기 위함이다.

```ts
heartbeat_locks {
  id: uuid
  runId: uuid              // FK to runs
  issueId: uuid            // 빠른 조회용 denormalized
  workerId: text           // worker instance 식별자

  leaseUntil: timestamptz  // 만료 시각
  renewCount: integer      // 갱신 횟수 (감사용)

  acquiredAt: timestamptz
  createdAt: timestamptz
}
```

**Lease 정책:**

| 항목 | 값 |
| --- | --- |
| 초기 lease | 60초 |
| 갱신 주기 | 20초마다 `leaseUntil = now() + 60s` |
| 갱신 실패(네트워크 등) | 1회 재시도 후 lease 포기 → run을 orphan로 간주 |
| run 종료 시 | lease row를 delete (또는 `releasedAt` 마킹) |

#### 20.3.5 Worker 멀티 인스턴스 대응

P0는 worker 1개를 기본으로 하되, 멀티 인스턴스에서도 깨지지 않도록 설계한다.

```sql
-- worker가 queued run을 가져올 때
SELECT id FROM runs
  WHERE status = 'queued'
  ORDER BY createdAt
  FOR UPDATE SKIP LOCKED
  LIMIT 1;
```

`SKIP LOCKED`는 다른 worker가 이미 잡은 run을 건너뛴다. 두 worker가 같은 run을 claim하는 일이 없다.

#### 20.3.6 Orphan Recovery

별도 reaper가 30초마다 만료된 lease를 스캔한다.

```txt
reaper loop (30s):
  SELECT runId FROM heartbeat_locks WHERE leaseUntil < now()
    FOR each expired lock:
      1. run.status 확인
      2. 여전히 running이면:
         - run.status → failed
         - failureReason = "orphan_detected"
         - audit event: run.orphan_detected
         - heartbeat_lock row delete
      3. 이미 종료된 run이면:
         - lock row만 delete (cleanup)
```

이것이 2.5 Heartbeat Failure Matrix의 `Worker crash/orphan → failed` 행의 실행 메커니즘이다.

#### 20.3.7 동시성 검증 시나리오

P0에서 반드시 통과해야 하는 동시성 테스트:

1. **중복 heartbeat 버튼 클릭**: 같은 issue에 100ms 간격으로 2회 heartbeat → run 1개만 생성, 두 번째는 `blocked_by_policy` (idempotency + unique index)
2. **멀티 worker 동시 claim**: worker 2개가 같은 queued run을 동시에 `FOR UPDATE` → 1개만 성공, 다른 1개는 no-op
3. **Worker crash 시뮬레이션**: run을 `running`으로 둔 채 worker 강제 종료 → 60초 + 30초 이내에 orphan recovery가 run을 `failed`로 전환
4. **Lease 갱신 실패**: DB 일시 장애로 lease 갱신 실패 → worker가 자발적으로 adapter 취소 시도 후 run 종료

---

### 20.4 예산 & 비용 산정

이것이 이 PRD에서 가장 얕았던 부분이다. 2.6은 `Budget hard stop`을 선언했지만, 예산이 **언제 리셋되는지**, 비용이 **어떻게 산정되는지**, pre-check와 실제 호출 사이에 race가 있을 때 **어떻게 막는지**가 전혀 없었다.

#### 20.4.1 통화 단위 통일 (정정)

**기존 `*Cents`/`*Usd` 표기는 폐기한다.** 모든 통화 필드는 **원(KRW) 정수**로 통일한다.

| 구 분 | 기존 표기 | 정정 표기 |
| --- | --- | --- |
| 월 예산 | `monthlyBudgetCents` | `monthlyBudgetWon` |
| 누적 지출 | `spentMonthlyCents` | `spentMonthlyWon` |
| Run 비용 | `estimatedCostUsd` | `estimatedCostWon` |
| CostEvent 비용 | `costCents` | `costWon` |
| Heartbeat payload | `budgetRemainingCents` | `budgetRemainingWon` |

정수를 쓰는 이유: 부동소수점 오차를 원천 차단. KRW는 소수점이 없는 통화라 정수 표현이 자연스럽다.

> 주의: 환율 변동이 있는 비용(provider가 USD로 청구하는 경우)은 `llm_pricing` 테이블에서 KRW 환산 단가를 관리하고, 환율은 주 1회 갱신한다. 환율 손실은 운영 비용으로 흡수한다.

#### 20.4.2 리셋 주기

**매월 1일 00:00 KST (UTC+9)** 에 예산을 리셋한다.

```txt
매월 1일 00:00:00 KST (= 전월 말 23:00:00 UTC)
  ↓ monthly budget reset job 실행
  ↓ 각 agent/goal의 spentMonthlyWon을 monthly_budget_snapshots로 백업
  ↓ spentMonthlyWon = 0
  ↓ audit event: budget.monthly_reset
```

KST를 선택한 이유: 단일 한국 사용자/팀 맥락에서 자정 리셋이 가장 직관적. UTC 자정과 KST 자정이 다르면 “오늘 100원 썼는데 어제 0시에 리셋됐다”는 혼란이 생긴다.

#### 20.4.3 `monthly_budget_snapshots`

월 마감 이력을 보존한다.

```ts
monthly_budget_snapshots {
  id: uuid
  workspaceId: uuid

  entityType: "agent" | "goal"
  entityId: uuid

  periodYear: integer       // 2026
  periodMonth: integer      // 1~12

  budgetLimitWon: integer
  spentWon: integer
  reservedWon: integer      // 진행 중이던 run의 예약분
  overrunWon: integer       // 초과분 (있다면)

  createdAt: timestamptz
}
```

#### 20.4.4 LLM Pricing Reference

provider 단가를 별도 테이블에서 관리한다. 코드에 하드코딩하지 않는다.

```ts
llm_pricing {
  id: uuid
  provider: text            // "openai", "anthropic", ...
  model: text               // "gpt-4o", "claude-3-5-sonnet", ...

  inputWonPer1kTokens: integer
  outputWonPer1kTokens: integer

  validFrom: timestamptz    // 시점별 단가 변경 대응
  validTo: timestamptz | null

  createdAt: timestamptz
  updatedAt: timestamptz
}
```

비용 산정은 항상 `validFrom <= now() < validTo`인 row를 사용한다. 단가 변경 시 새 row를 insert하고 이전 row의 `validTo`를 채운다.

#### 20.4.5 Reservation 패턴 (race condition 해결)

이게 핵심이다. 단순 pre-check은 race condition에 취약하다.

```txt
시나리오 (race condition):
  T0: agent.spentMonthlyWon = 900, monthlyBudgetWon = 1000
  T1: run A pre-check 통과 (남은 예산 100원)
  T2: run B pre-check 통과 (남은 예산 100원)
  T3: run A adapter 호출 → 80원 소비
  T4: run B adapter 호출 → 80원 소비 → 총 1060원, 예산 초과!
```

이를 막기 위해 **사전 예약(reservation)** 패턴을 쓴다.

```txt
Run 시작 시 (queued → running 전환):
  1. 예상 비용 추정 (최대 토큰 × 단가)
  2. atomic: agent.reservedWon += estimatedCostWon
  3. atomic: agent.spentWon + reservedWon <= monthlyBudgetWon 검사
  4. 실패 시 run → blocked_by_budget
  5. 성공 시 run → running

Run 종료 시 (running → succeeded/failed):
  1. 실제 비용 cost event로 저장
  2. atomic: agent.spentMonthlyWon += actualCostWon
  3. atomic: agent.reservedWon -= estimatedCostWon (release)
```

`reservedWon`은 “현재 running 중인 run들이 예약한 금액”이다. 실제 지출과 별도로 추적한다.

```ts
// atomic하게 예약하는 pseudo-SQL
UPDATE agents
  SET reservedWon = reservedWon + :est
  WHERE id = :agentId
    AND spentMonthlyWon + reservedWon + :est <= monthlyBudgetWon
RETURNING reservedWon;
-- 영향받은 row가 0이면 예약 실패 → blocked_by_budget
```

단일 UPDATE 문으로 원자성을 보장한다.

#### 20.4.6 3단계 예산 우선순위

issue, agent, goal 3단계 예산이 있을 때 차단 기준을 명확히 한다.

```txt
우선순위 (가장 좁은 단위부터):
  1. issue.budgetLimitWon      ← 가장 먼저 검사
  2. agent.monthlyBudgetWon
  3. goal.monthlyBudgetWon     ← 가장 마지막

모두 통과해야 run 실행.
가장 먼저 초과한 단위가 차단 사유로 기록됨.
```

예: issue 예산은 남았지만 agent 월 예산 초과 → `blocked_by_budget`, reason = "agent budget exhausted".

#### 20.4.7 Runtime 초과 대응

Run 도중 LLM 호출이 누적되어 예약액을 초과하면:

| 상황 | 대응 |
| --- | --- |
| 단일 LLM 호출이 예약액 초과 | 호출 결과 저장 후 다음 호출 차단. run은 succeeded (이미 받은 결과는 유효) |
| 다음 heartbeat부터 | pre-check 단계에서 차단 |

P0의 `built_in_llm`은 단일 호출이므로 이 시나리오는 드물지만, reservation이 보호막 역할을 한다.

#### 20.4.8 Warning / Hard Stop / Override

| 임계치 | 동작 |
| --- | --- |
| 80% 도달 | `budget.warning` audit event, dashboard 표시. run은 계속됨 |
| 100% 도달 | 다음 run부터 `blocked_by_budget`. 진행 중 run은 종료 시 까지 허용 |
| Override | approval 필요. 승인 시 `monthlyBudgetWon`을 일시적으로 상향 (정액 추가)하고 `budget.override_approved` audit |

Override는 영구 증액이 아니라 “이번 달 한정 추가 예산”이다. 다음 달 리셋 시 원래 값으로 복귀한다.

---

### 20.5 Worker ↔ Next.js 통신

기존 PRD는 “run log를 UI에서 streaming으로 볼 수 있다”(FR-004)고만 되어 있었다. 하지만 worker와 Next.js가 다른 프로세스일 때 이 streaming을 어떻게 구현하는지가 없었다. Redis를 스택에 추가하지 않기로 했으므로, Postgres 자체 기능으로 해결한다.

#### 20.5.1 아키텍처

```txt
[Browser]
   ↓ SSE (EventSource)
[Next.js /api/runs/:runId/logs/stream]
   ↓ LISTEN run_log_<runId>
[Postgres] ← NOTIFY run_log_<runId>, payload
   ↑ INSERT INTO run_logs
[Heartbeat Worker]
```

worker가 `run_logs`에 row를 insert할 때 같은 트랜잭션(또는 직후)에 `NOTIFY`를 쏜다. Next.js가 채널을 LISTEN하고 있다가 payload를 받으면 SSE로 브라우저에 푸시한다.

#### 20.5.2 채널 네이밍

```txt
channel := "run_log_" + runId
예: run_log_01HZX...
```

run 단위 채널을 쓰는 이유: 전역 채널을 쓰면 모든 SSE 연결이 모든 run의 로그를 받아서 필터링해야 한다. run 단위 채널은 해당 run을 구독한 브라우저만 받는다.

#### 20.5.3 NOTIFY payload

```json
{
  "logId": "log_01HZX...",
  "runId": "run_01HZX...",
  "level": "info",
  "message": "adapter invoked",
  "timestamp": "2026-07-05T12:00:00.000Z"
}
```

payload는 가볍게 유지한다. 상세 내용은 브라우저가 별도 API로 fetch한다 (또는 payload 자체에 포함).

#### 20.5.4 SSE 재개 (Last-Event-ID)

네트워크 끊김 시 브라우저가 `Last-Event-ID` 헤더로 마지막으로 받은 logId를 보낸다.

```txt
[Browser] 연결 끊김
   ↓ 재연결 시 Last-Event-ID: log_01HZX123
[Next.js]
   ↓ SELECT * FROM run_logs WHERE runId = ? AND id > ? ORDER BY createdAt
   ↓ 누락된 로그 먼저 전송
   ↓ 이후 LISTEN으로 실시간 푸시
```

이로써 짧은 끊김 동안 로그가 누락되지 않는다 (13.3 NFR: streaming latency 1초 이내).

#### 20.5.5 Worker Health

worker 자체의 건강 상태를 별도로 추적한다.

```ts
worker_heartbeats {
  id: uuid
  workerId: text            // "worker-1", hostname 등
  lastSeenAt: timestamptz
  runningRunIds: uuid[]     // 현재 처리 중인 run 목록
  metadata: jsonb           // 버전, 메모리 사용량 등

  createdAt: timestamptz
  updatedAt: timestamptz
}
```

worker는 10초마다 이 테이블을 갱신한다. Dashboard가 최근 30초 이내 갱신된 worker가 없으면 경고를 표시한다.

#### 20.5.6 Graceful Shutdown

```txt
worker가 SIGTERM 수신:
  1. 새 run claim 중단
  2. running run 목록 확인
  3. 있으면: 최대 N초(gracefulShutdownMs, 기본 30s) 대기
     - run이 자연 종료하면 정상
     - 시간 초과하면 run을 orphan로 마킹 (orphan recovery가 처리)
  4. 없으면 즉시 종료
```

강제 kill(`SIGKILL`)은 orphan recovery가 60+30초 내에 잡는다.

#### 20.5.7 Worker API 엔드포인트

P0에 필요한 최소 worker 관련 API:

```txt
GET  /api/health/worker       // worker health 상태 (dashboard용)
GET  /api/runs/:runId/logs    // 전체 로그 (페이징)
GET  /api/runs/:runId/logs/stream   // SSE 스트림
```

---

### 20.6 MCP 자식 프로세스 관리

stdio MCP server는 **자식 프로세스**다. 이 프로세스들의 생명주기 관리가 없으면 프로세스 누수, 좀비 프로세스, 재시작 불가 이슈가 발생한다.

#### 20.6.1 프로세스 Lifecycle

```txt
worker 시작
  ↓ MCP 서버별로 자식 프로세스 spawn
  ↓ agent_mcp_permissions에서 해당 server를 쓰는 agent가 있으면 refcount++
  ↓ Worker 종료 시
  ↓ 모든 자식 프로세스에 SIGTERM
  ↓ 5초 대기
  ↓ 살아있으면 SIGKILL
```

#### 20.6.2 프로세스 풀 전략

| 항목 | 결정 |
| --- | --- |
| 단위 | worker 프로세스당 1개 spawn |
| 공유 | 여러 agent가 같은 MCP server를 쓰면 1개 프로세스 공유 (refcount) |
| refcount 0 시 | 즉시 종료하지 않고 5분 대기 (재사용), 이후 shutdown |
| 동시성 | 단일 프로세스 내에서 MCP 요청은 직렬 처리 (P0 단순화) |

P0에선 단일 worker를 기본으로 하므로, MCP 프로세스도 1개씩만 존재한다. 멀티 worker가 되면 worker별로 MCP 프로세스가 생긴다 (P1 최적화 대상).

#### 20.6.3 자동 재시작

```txt
MCP 자식 프로세스 exit 감지:
  ↓ exit code != 0 또는 signal 종료
  ↓ 1회: 즉시 재spawn, audit event: mcp.process_restarted
  ↓ 연속 2회 실패: mcp_servers.status = 'error'
  ↓ 해당 server를 쓰는 agent의 run은 failed (MCP unavailable)
  ↓ dashboard 경고
```

재시도 간격은 1초 고정 (P0 단순화). exponential backoff는 P1.

#### 20.6.4 Discovery 캐싱

매 heartbeat마다 `tools/list`를 치면 느리고 MCP 서버 부하가 크다. 캐싱한다.

```ts
mcp_capabilities {
  id: uuid
  mcpServerId: uuid

  kind: "tool" | "resource" | "prompt"
  name: text                 // tool/resource name
  description: text | null
  inputSchema: jsonb | null  // tool input schema

  discoveredAt: timestamptz
  expiresAt: timestamptz     // TTL 10분
}
```

| 시점 | 동작 |
| --- | --- |
| heartbeat 시작 | `expiresAt > now()`이면 캐시 사용 |
| 만료 또는 수동 refresh | `tools/list` 재호출, `discoveredAt`/`expiresAt` 갱신 |
| MCP 서버 재시작 | 캐시 무효화 (서버가 바뀌었을 수 있음) |

#### 20.6.5 Filesystem MCP Root Allowlist

`local filesystem MCP`의 root path를 우리 쪽에서 검증한다. MCP 서버 자체에 위임하지 않는다.

```ts
mcp_servers {
  // ... 기존 필드
  allowedRoots: text[]      // ["/Users/me/Documents/project", ...]
}
```

```txt
MCP tool call (예: read_file("/etc/passwd"))
  ↓ 우리 wrapper가 path 검증
  ↓ allowedRoots 중 하나의 하위 경로인지 확인
  ↓ 아니면 deny (audit: mcp.tool_denied_path_violation)
  ↓ 맞으면 실제 MCP 서버로 forward
```

path traversal(`../`)도 사전 차단한다.

#### 20.6.6 MCP Call Budget & Audit

MCP tool call은 run log와 별도로 audit event를 남긴다 (FR-005 요구사항).

| 항목 | 기록 위치 |
| --- | --- |
| tool 이름, 인자 | run_logs (level: mcp_call) |
| 응답 요약 | run_logs |
| 호출 자체 | audit_events (action: mcp.tool_invoked) |
| 거부 | audit_events (action: mcp.tool_denied) |
| 승인 필요 | approvals + audit_events |

인자/응답에서 시크릿 패턴이 감지되면 redaction한다 (20.2.4와 연동).

---

### 20.7 `built_in_llm` Adapter 정의

19.5.4는 “issue context 읽고 응답 생성”이라는 한 줄만 있었다. 단일 호출인지 agentic loop인지, 토큰 카운트를 어떻게 할지, 실패를 어떻게 처리할지가 없었다. 이 결정 없이 구현을 시작하면 작업량이 3배 이상 편차가 난다.

#### 20.7.1 P0 범위 확정

| 항목 | P0 | P1 이후 |
| --- | --- | --- |
| LLM 호출 방식 | **단일 호출** (one-shot completion) | agentic loop (multi-turn tool calling) |
| MCP tool 사용 | 사전 주입만 (context pack에 포함) | 런타임 tool 선택/호출 |
| Multi-turn | 미지원 | 지원 |
| Streaming 응답 | 미지원 (동기 대기) | SSE streaming |

P0는 **“issue context + MCP context pack을 한 번에 프롬프트로 조립해 1회 LLM 호출”**이다. 복잡한 tool-calling loop는 P1로 미룬다. 이것이 2.2 “P0는 하나의 운영 루프가 끝까지 안전하게 돈다”는 결정과 일치한다.

#### 20.7.2 프롬프트 구성

```txt
system prompt:
  - agent.role 설명
  - 응답 형식 지시 (JSON schema)
  - 제약: successCriteria에 맞춰 응답할 것

user prompt:
  - goal.title, goal.description, goal.successCriteria
  - issue.title, issue.description
  - issue.comments (최근 N개)
  - MCP context pack (resources/read 결과 요약)
  - budgetRemainingWon (비용 인지)
```

응답은 structured JSON으로 강제한다.

```json
{
  "summary": "조사 요약",
  "risks": ["위험1", "위험2"],
  "nextActions": ["액션1", "액션2"],
  "issueStatus": "in_review",
  "comment": "issue에 남길 코멘트 본문"
}
```

#### 20.7.3 Token 카운트

| 우선순위 | 방법 |
| --- | --- |
| 1순위 | provider API 응답의 `usage` 필드 (정확) |
| 2순위 (fallback) | tiktoken/안측 라이브러리로 추정 |

`built_in_llm`은 provider API를 직접 호출하므로 1순위를 기본으로 한다. webhook adapter처럼 provider 응답이 없는 경우만 추정한다.

#### 20.7.4 실패 처리

| 상황 | 동작 | run status |
| --- | --- | --- |
| 200 OK, schema 통과 | 결과 저장, cost event | `succeeded` |
| 200 OK, schema 불일치 | raw 응답 metadata 저장, retry 1회 | retry 후에도 불일치 → `failed` |
| 429 rate limit | exponential backoff, 최대 3회 | 실패 시 `failed` |
| 5xx server error | retry 1회 (5초 후) | 실패 시 `failed` |
| timeout (60초) | 즉시 실패 | `failed`, reason: adapter_timeout |
| 네트워크 오류 | retry 1회 | 실패 시 `failed` |

retry는 idempotency를 가정한다. provider가 idempotency key를 지원하면 사용한다.

#### 20.7.5 `mock_agent`와의 관계

| 항목 | `mock_agent` | `built_in_llm` |
| --- | --- | --- |
| 외부 의존성 | 없음 | LLM provider API |
| 응답 | 결정적 stub (입력 기반 해시 → 고정 응답) | 실제 LLM 응답 |
| 비용 | 항상 0원 | 실제 토큰 비용 |
| 용도 | CI, 오프라인 데모, E2E 테스트 | 실제 사용, 제품 데모 |
| P0 필수 여부 | 필수 | 필수 (택일 아님) |

둘 다 P0에 포함된다 (2.2 “P0 adapter: built_in_llm 또는 mock_agent, http_webhook”의 모호함을 해소). mock_agent는 offline/CI용, built_in_llm은 실제 사용용이다.

#### 20.7.6 `mock_agent` 응답 스펙

결정적 응답을 위해 입력 해시를 사용한다.

```txt
입력: { issueId, agentId, runId, contextHash }
  ↓ SHA-256 해시
  ↓ 해시 기반으로 미리 정의된 응답 풀에서 선택
  ↓ 항상 같은 입력에는 같은 응답 (재현 가능)
```

응답 풀은 테스트용 fixture 5~10개. 테스트에서 특정 응답이 필요하면 fixture를 직접 주입한다.

---

### 20.8 데이터 모델 보강 (Implementation-Ready Schema)

10.1 Core Tables에 테이블 이름만 있고 상세 스키마가 비어 있었다. 구현자가 FR을 읽고 컬럼을 역추론해야 하는 상태였다. 본 절은 P0 구현에 필요한 컬럼을 TypeScript pseudo-schema로 정의한다.

> 본 절은 19.7 `agents`/`agent_*` 테이블과 **중복해서 정의하지 않는다**. 이미 정의된 테이블은 참조만 하고, 통화 필드(`monthlyBudgetCents` → `monthlyBudgetWon` 등)만 정정한다.

#### 20.8.1 Workspace / Users / Sessions

```ts
workspaces {
  id: uuid
  name: text              // "default"
  slug: text unique       // URL 친화적 식별자
  timezone: text          // "Asia/Seoul" (기본값, KST 리셋에 사용)
  createdAt: timestamptz
  updatedAt: timestamptz
}

users {
  id: uuid
  workspaceId: uuid

  email: text
  role: text              // P0: "local_admin" 고정
  passwordHash: text      // bcrypt

  createdAt: timestamptz
  updatedAt: timestamptz
}

sessions {
  id: uuid                // 쿠키 값 (session token)
  userId: uuid

  expiresAt: timestamptz
  lastSeenAt: timestamptz
  ipHash: text | null     // 감사용 (선택)

  createdAt: timestamptz
}

idempotency_keys {
  id: uuid
  key: text               // 클라이언트가 보낸 Idempotency-Key
  workspaceId: uuid

  endpointPath: text
  responseHash: text
  responseBody: jsonb     // 캐시된 응답 (재반환용)

  expiresAt: timestamptz  // 24시간
  createdAt: timestamptz
}
```

#### 20.8.2 Goals / Issues (통화 KRW 반영)

```ts
goals {
  id: uuid
  workspaceId: uuid

  title: text
  description: text
  successCriteria: text
  context: text | null

  status: text            // draft | active | paused | archived | error (추가)
  approvalPolicy: jsonb   // { requireHeartbeatApproval, requireCompletionApproval }

  monthlyBudgetWon: integer       // 정정: *Cents → *Won
  spentMonthlyWon: integer        // 정정
  reservedWon: integer            // 20.4.5 reservation

  periodAnchorKst: timestamptz    // 예산 주기 기준 시각 (매월 1일 00:00 KST)

  createdById: uuid       // users.id (audit용)
  createdAt: timestamptz
  updatedAt: timestamptz
}

issues {
  id: uuid
  workspaceId: uuid
  goalId: uuid            // FK to goals

  title: text
  description: text

  assigneeAgentId: uuid | null   // FK to agents
  priority: text                 // low | normal | high
  status: text                   // open | assigned | running | in_review | completed | blocked | cancelled

  budgetLimitWon: integer | null  // issue 단위 예산 (nullable)
  spentWon: integer               // issue 단위 누적
  reservedWon: integer            // 20.4.5

  mcpContextHints: jsonb          // [{ server, resource }]
  approvalRequired: boolean

  createdById: uuid
  createdAt: timestamptz
  updatedAt: timestamptz
}
```

#### 20.8.3 Runs / Run Logs

```ts
runs {
  id: uuid
  workspaceId: uuid
  issueId: uuid           // FK to issues
  agentId: uuid           // FK to agents
  goalId: uuid            // denormalized (조회 성능)

  status: text            // queued | running | succeeded | failed | cancelled
                          //      | blocked_by_budget | blocked_by_approval | blocked_by_policy

  triggeredByActorType: text
  triggeredByActorId: text
  triggeredReason: text | null  // "manual" | "rerun" | "test_heartbeat"

  estimatedCostWon: integer     // run 시작 시 예약 금액
  actualCostWon: integer        // 종료 후 실제 (default 0)

  failureReason: text | null
  failureMetadata: jsonb | null

  workerId: text | null         // claim한 worker
  claimedAt: timestamptz | null
  startedAt: timestamptz | null
  finishedAt: timestamptz | null

  createdAt: timestamptz

  -- 20.3.2 partial unique index
  -- CREATE UNIQUE INDEX runs_one_running_per_issue ON runs (issueId) WHERE status = 'running';
}

run_logs {
  id: uuid
  runId: uuid             // FK to runs

  seq: integer            // run 내 순번 (SSE Last-Event-ID용)
  level: text             // info | warn | error | mcp_call | adapter_io
  message: text
  metadata: jsonb | null  // structured payload

  redacted: boolean       // 시크릿 치환 여부
  createdAt: timestamptz
}
```

#### 20.8.4 MCP / Permissions

```ts
mcp_servers {
  id: uuid
  workspaceId: uuid

  name: text              // "local-docs"
  transport: text         // "stdio" (P0 고정)
  command: text           // "npx"
  args: jsonb             // ["-y", "@modelcontextprotocol/server-filesystem", "..."]
  env: jsonb              // env key → secretRef 매핑
  workingDirectory: text | null
  trustLevel: text        // local_trusted | governed

  allowedRoots: text[]    // filesystem MCP 전용 (20.6.5)

  status: text            // connected | disconnected | error | starting
  lastDiscoveredAt: timestamptz | null
  lastError: text | null

  createdAt: timestamptz
  updatedAt: timestamptz
}

mcp_capabilities {
  id: uuid
  mcpServerId: uuid

  kind: text              // tool | resource | prompt
  name: text
  description: text | null
  inputSchema: jsonb | null
  riskLevel: text         // low | medium | high (자체 분류)

  discoveredAt: timestamptz
  expiresAt: timestamptz  // TTL 10분 (20.6.4)
}

-- agent_mcp_permissions: 19.7.4 참조
```

#### 20.8.5 Budget / Cost / Approval / Audit

```ts
cost_events {
  id: uuid
  runId: uuid
  agentId: uuid
  goalId: uuid
  issueId: uuid

  provider: text
  model: text
  inputTokens: integer
  outputTokens: integer

  estimatedCostWon: integer   // 정정: *Usd → *Won
  costWon: integer            // 정정: *Cents → *Won

  pricingSnapshotId: uuid | null   // llm_pricing.id (단가 추적)
  createdAt: timestamptz
}

approvals {
  id: uuid
  workspaceId: uuid

  entityType: text        // agent | issue | run | mcp_tool | budget_override
  entityId: uuid

  reason: text | null
  requestedByActorType: text
  requestedByActorId: text

  status: text            // pending | approved | rejected | expired
  decidedByActorType: text | null
  decidedByActorId: text | null
  decisionReason: text | null
  expiresAt: timestamptz | null   // 24시간 (self-approval 완화용)

  createdAt: timestamptz
  decidedAt: timestamptz | null
}

audit_events {
  id: uuid
  workspaceId: uuid

  actorType: text         // user | agent | system | mcp (20.1.4)
  actorId: text

  action: text            // "issue.assigned", "run.started", ...
  entityType: text        // goal | agent | issue | run | mcp | budget | approval | secret
  entityId: text

  before: jsonb | null
  after: jsonb | null
  redactedFields: text[]  // 시크릿 필드명 (20.2.4)

  metadata: jsonb | null  // { requestId, runId, ip, ... }
  createdAt: timestamptz

  -- 인덱스 (13.x 관측 + 9.8 filter)
  -- CREATE INDEX audit_events_action_idx ON audit_events (action, createdAt DESC);
  -- CREATE INDEX audit_events_entity_idx ON audit_events (entityType, entityId, createdAt DESC);
  -- CREATE INDEX audit_events_run_idx ON audit_events ((metadata->>'runId')) WHERE metadata ? 'runId';
}
```

#### 20.8.6 Worker / Lock / Snapshot (신규)

```ts
heartbeat_locks {
  id: uuid
  runId: uuid             // FK to runs
  issueId: uuid           // 빠른 조회용 (20.3.4)
  workerId: text

  leaseUntil: timestamptz
  renewCount: integer

  acquiredAt: timestamptz
  createdAt: timestamptz

  -- 20.3.6 reaper가 leaseUntil로 스캔
  -- CREATE INDEX heartbeat_locks_lease_idx ON heartbeat_locks (leaseUntil) WHERE leaseUntil > now();
}

worker_heartbeats {
  id: uuid
  workerId: text          // unique
  lastSeenAt: timestamptz
  runningRunIds: uuid[]
  metadata: jsonb

  createdAt: timestamptz
  updatedAt: timestamptz
}

monthly_budget_snapshots {
  id: uuid
  workspaceId: uuid

  entityType: text        // agent | goal
  entityId: uuid

  periodYear: integer
  periodMonth: integer

  budgetLimitWon: integer
  spentWon: integer
  reservedWon: integer
  overrunWon: integer

  createdAt: timestamptz
}

llm_pricing {
  id: uuid
  provider: text
  model: text

  inputWonPer1kTokens: integer
  outputWonPer1kTokens: integer

  validFrom: timestamptz
  validTo: timestamptz | null

  createdAt: timestamptz
  updatedAt: timestamptz
}

secrets {
  -- 20.2.2 참조
}
```

#### 20.8.7 인덱스/제약 요약

성능 NFR(13.3)과 filter 요구사항(9.8)을 만족하기 위한 최소 인덱스:

| 테이블 | 인덱스 | 용도 |
| --- | --- | --- |
| `runs` | partial unique `(issueId) WHERE status='running'` | 동시성 보장 (20.3.2) |
| `runs` | `(status, createdAt)` | worker claim (20.3.5) |
| `run_logs` | `(runId, seq)` | SSE 순서 보장 |
| `audit_events` | `(action, createdAt DESC)` | audit log filter |
| `audit_events` | `(entityType, entityId, createdAt DESC)` | entity별 감사 추적 |
| `heartbeat_locks` | partial `(leaseUntil) WHERE leaseUntil > now()` | reaper 스캔 |
| `mcp_capabilities` | `(mcpServerId, expiresAt)` | 캐시 만료 조회 |
| `cost_events` | `(agentId, createdAt DESC)`, `(goalId, ...)` | 월별 집계 |

#### 20.8.8 마이그레이션 원칙

- Drizzle migration 파일은 PR 단위로 분리 (Phase 0, 1, 2 각각)
- `up`/`down` 모두 작성. `down`은 데이터 보존보다 스키마 롤백에 집중
- P0에선 destructive migration(컬럼 삭제/rename) 금지. additive만 허용
- 통화 필드 rename은 한 번에 일괄 적용 (부분 적용 X)

---

### 20.9 상태머신 통일 (2.4 vs 19.8 충돌 해결)

기존 PRD의 상태머신이 두 곳에서 서로 다르게 정의되어 있었다.

- **2.4**: `draft → pending_approval → active → running → paused → terminated`
- **19.8**: 위에 더해 `idle`, `error`, `budget_exhausted` 포함

구현자가 매번 어느 표를 따를지 판단해야 하는 비용이 발생한다. 본 절은 단일 진본(canonical)을 확정한다.

#### 20.9.1 Agent 상태머신 (단일 진본)

**19.8을 진본으로 채택**한다. 더 풍부한 상태를 포함하며, 2.5 Heartbeat Failure Matrix와 일치한다.

```txt
        submit                approve
draft ─────────▶ pending_approval ─────────▶ active
  ▲                    │                        │
  │ reject             │ expire                 │ heartbeat_start
  │                    ▼                        ▼
  └──────────────  rejected/return           running
                                              │
                            ┌─────────────────┼─────────────────┐
                            │                 │                 │
                  success   │    timeout      │   budget 0     │
                            ▼                 ▼                 ▼
                         idle              error          budget_exhausted
                            │                 │                 │
                            │ recover         │ budget refilled │
                            └─────────────────┴─────────────────┘
                                              │
                                              │ pause / resume / terminate
                                              ▼
                                          paused / terminated
```

#### 20.9.2 통합 상태 전이표 (canonical)

2.4를 대체하는 단일 표다. 기존 2.4는 historical 참조용으로 남기되, 구현은 본 표를 따른다.

| From | Event | To | Side effect | 비고 |
| --- | --- | --- | --- | --- |
| draft | submit | pending_approval | `agent.submitted_for_approval` audit |  |
| pending_approval | approve | active | `agent.approved`, `agent.activated` audit | heartbeat 가능 |
| pending_approval | reject | draft | rejection reason 저장 |  |
| active | heartbeat_start | running | concurrency check (20.3) |  |
| running | heartbeat_finish | idle | lastHeartbeatAt 갱신 | `active` 대신 `idle` 사용 |
| idle | heartbeat_start | running |  |  |
| active/idle/running | pause | paused | 새 run 차단 |  |
| paused | resume | idle | `agent.resumed` audit |  |
| running | adapter_timeout | error | `agent.error` audit, failureReason 저장 | 신규 |
| running | budget_exhausted | budget_exhausted | `agent.budget_exhausted` audit | 신규 |
| error | recover | idle | 수동 복구 액션 | 신규 |
| budget_exhausted | budget_refilled | idle | budget override approval 후 | 신규 |
| any except terminated | terminate | terminated | 복구 불가 (2.6 invariant) |  |

#### 20.9.3 Goal 상태 확장 (error 추가)

기존 2.4 Goal 상태에 `error`가 없었다. 하지만 전체 MCP 서버 장애, 월 예산 산정 불가, 의존 entity corruption 등 goal 단위로 표현해야 할 에러 상황이 존재한다.

| From | Event | To | Side effect | 비고 |
| --- | --- | --- | --- | --- |
| draft | activate | active | `goal.activated` audit |  |
| active | pause | paused | 새 heartbeat 차단 |  |
| paused | resume | active | `goal.resumed` audit |  |
| active/paused | archive | archived | 새 issue/heartbeat 차단 |  |
| active | system_error | error | `goal.error` audit, reason 저장 | **신규** |
| error | recover | active | 수동 복구 | **신규** |

`error` 상태의 goal은 heartbeat를 차단하지만, 이미 생성된 issue/run은 영향받지 않는다.

#### 20.9.4 Issue / Run / Approval 상태머신 (재확인)

2.4의 Issue, Run, Approval 상태표는 19.x 부록과 충돌하지 않으므로 그대로 유효하다. 단, Run 상태에 아래 추가 매핑을 명시한다.

| Run 상태 | 의미 | 다음 가능 상태 |
| --- | --- | --- |
| queued | 실행 대기 | running, blocked_by_*, cancelled |
| running | 실행 중 | succeeded, failed, cancelled |
| succeeded | 정상 종료 | (종단) |
| failed | 실패 | (종단, rerun으로 새 run 생성) |
| cancelled | 사용자 취소 | (종단) |
| blocked_by_budget | 예산 부족 | (재시도 시 새 run) |
| blocked_by_approval | 승인 필요 | approval 후 running, 또는 expired |
| blocked_by_policy | 권한/정책 위반 | (정책 변경 후 새 run) |

#### 20.9.5 Approval self-approval 정책 (single admin 모드)

2.6 Approval gate가 single admin 모드에서 자가상쇄되는 모순을 해결한다.

**P0 정책**: single admin 모드에서 approval은 **확인(confirm) 게이트**로 기능한다.

| 관점 | 해석 |
| --- | --- |
| 보안 | 즉각적 실행을 막고, 2단계 확인(요청 → 승인)으로 실수 방지 |
| 감사 | approval decision 자체가 audit trail에 남아 "왜 승인했는지"를 기록 |
| Self-approval 허용 | 같은 actor가 요청/승인 둘 다 가능. 단 reason 필수 |

이는 multi-user 환경의 분리된 승인(independence)과는 다르지만, P0에서는 "감사 가능한 2단계 확인"으로 governance 가치를 유지한다.

| 항목 | P0 정책 |
| --- | --- |
| Self-approval | 허용 (같은 `local_admin`이 요청+승인) |
| `expiresAt` | 24시간 후 `expired` 자동 전환 |
| `decisionReason` | 승인/거절 시 필수 입력 |
| 영구 분산 승인 | P1+ (외부 슬랙/이메일 채널 승인) |

---

### 20.10 구현 착수 전 Definition of Done

본 장의 결정을 정리한 체크리스트다. 이 항목들이 모두 정해져 있어야 Phase 0 코드를 작성할 수 있다. `mvp_plan_prompt_guide.md`의 "구현 착수 전 기술 검수 체크리스트"(4.5)와 짝꿍이다.

| # | 항목 | 본 장 위치 | 없으면 코딩이 안 되는 이유 |
| --- | --- | --- | --- |
| 1 | 인증 + actor 주입 파이프 | 20.1 | audit actorId를 채울 수 없음 |
| 2 | 시크릿 저장소 (암호화 + 마스터키) | 20.2 | adapter 구현 자체가 불가 |
| 3 | 동시성 잠금 전략 (3겹) | 20.3 | 중복 실행 / 데드락 / orphan 미복구 |
| 4 | 예산 단위/리셋/reservation | 20.4 | race condition으로 예산 무력화 |
| 5 | Worker↔Web 통신 (LISTEN/NOTIFY) | 20.5 | UI에서 run log를 못 봄 |
| 6 | MCP 자식 프로세스 lifecycle | 20.6 | 프로세스 누수 / 재시작 불가 |
| 7 | `built_in_llm` adapter 범위 확정 | 20.7 | 구현량 3배 편차 |
| 8 | 상세 데이터 모델 (컬럼 단위) | 20.8 | 구현자가 FR을 역추론해야 함 |
| 9 | Agent 상태머신 단일 진본 | 20.9 | 두 표(2.4 vs 19.8) 충돌로 매번 판단 |
| 10 | Approval self-approval 정책 | 20.9.5 | governance 가치가 자가상쇄됨 |

#### Phase 0 착수 전 최종 점검

```txt
[ ] ACP_SECRET_MASTER_KEY env 정의 방법이 문서화되어 있는가?
[ ] ACP_BOOTSTRAP_ADMIN_PASSWORD 시드 플로우가 정의되어 있는가?
[ ] Postgres 버전이 advisory lock + LISTEN/NOTIFY를 지원하는가? (9.6+)
[ ] partial unique index가 허용되는 Postgres 버전인가?
[ ] KRW 정수 통화 단위가 모든 스키마에 적용되었는가?
[ ] Agent 상태머신 충돌이 해결되었는가? (20.9)
[ ] mock_agent fixture가 준비되어 있는가? (오프라인 10분 데모용)
[ ] localhost-only 바인딩이 기본값인가?
```

#### Phase 0 → Phase 1 게이트

Phase 0(skeleton)이 끝나고 Phase 1(CRUD)로 넘어가기 전에 통과해야 할 게이트:

```txt
[ ] local_admin 로그인 가능
[ ] workspace/goal/agent/issue 생성 API 동작
[ ] audit_events에 모든 mutation가 기록됨
[ ] secrets 암호화/복호화 라운드트립 성공
[ ] partial unique index가 동일 issue running run을 거부함
[ ] SSE 엔드포인트가 LISTEN/NOTIFY로 빈 스트림을 반환함
```
