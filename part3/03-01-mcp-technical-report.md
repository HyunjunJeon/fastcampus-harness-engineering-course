# MCP(Model Context Protocol) — 도구 호출의 기본 구조부터 생태계까지

## 0. 요약 (TL;DR)

- **MCP는 도구 호출 그 자체가 아니다.** 도구 호출(function/tool calling)은 2023년에 이미 LLM 공급사들이 각자의 포맷으로 도입한 메커니즘이다. MCP는 그 위에 얹히는 **"AI 애플리케이션 ↔ 외부 도구"의 표준 연결면**이다.
- **MCP는 LSP(Language Server Protocol)에서 영감을 받았다.** LSP가 *언어 × 에디터*의 통합 비용을 `M×N → M+N` 으로 줄였듯, MCP는 *모델 × 도구*의 통합 비용을 줄인다. 공식 스펙도 이 비유를 명시한다.
- **세 가지 1급 시민**: `Tools`(에이전트가 호출), `Resources`(에이전트가 읽음), `Prompts`(사용자/에이전트가 불러쓰는 템플릿). 거기에 클라이언트 측 프리미티브 `Sampling / Elicitation / Roots`가 결합되어 서버가 호스트를 거꾸로 활용할 수 있다.
- **트랜스포트는 두 개**: `stdio`(로컬 프로세스, 1:1), `Streamable HTTP`(원격, N:1, OAuth 권장).
- **2024-11-25 Anthropic이 오픈소스로 공개.** 약 6개월 만에 OpenAI, Google DeepMind, GitHub, Microsoft가 합류했고, 2025년 중반에는 IDE·SaaS·인프라 공급사가 자체 공식 MCP 서버를 운영하는 단계로 진입했다.
- **현재 가장 잘 쓰이는 사례**는 ① IDE/에이전트 통합(Claude Code · Cursor · VS Code · Zed), ② 깃 호스팅(GitHub MCP), ③ 이슈/관측성(Linear · Sentry · Atlassian), ④ 브라우저 자동화(Playwright · Puppeteer), ⑤ 디자인(Figma MCP), ⑥ 결제/인프라(Stripe · Cloudflare), ⑦ 게이트웨이(Docker MCP Gateway) 이다.

---

## 1. 도구 호출의 기본 구조 — MCP 이전과 이후

### 1.1. LLM 도구 호출이 무엇이었는가

GPT-3.5/4 시대(2023)에 OpenAI가 `function_call`을, 이어 Anthropic이 `tool_use`를 도입하면서 LLM은 "텍스트만 뱉는 모델"에서 "구조화된 호출을 생성하는 모델"로 바뀌었다. 메커니즘 자체는 단순하다.

```
[1] 호스트 → 모델: 메시지 + 사용 가능한 tools 스펙(JSON Schema)
[2] 모델 → 호스트: tool_use 블록 { name, arguments }
[3] 호스트 → 외부 시스템: 실제 함수/API 호출
[4] 호스트 → 모델: tool_result 블록 { content }
[5] 모델 → 호스트: 다음 응답(텍스트 또는 추가 tool_use)
```

핵심은 모델이 `[3]`을 *직접 하지 않는다*는 점이다. 모델은 "이 도구를 이 인자로 부르고 싶다"는 **의도만 표현**하고, 실제 실행은 **호스트(애플리케이션)가 책임진다**. 이 분리가 권한·감사·승인 인터페이스의 근거가 된다 — 강의 3-1에서 강조하는 "쓰기 권한이 필요한가?", "누가 인증 정보를 관리하는가?" 같은 질문이 가능한 이유다.

### 1.2. MCP 이전의 문제 — M×N

도구 호출 자체는 표준화됐지만 *"어떤 도구를 어디서 어떻게 가져오느냐"*는 표준이 없었다.

- Claude를 GitHub에 연결하려면 Anthropic SDK 위에 GitHub용 어댑터를 짠다.
- 같은 일을 ChatGPT에서 하려면 OpenAI Plugin 형태로 다시 짠다.
- Cursor에서 또 하려면 Cursor 전용 통합을 짠다.

도구 N개 × 호스트 M개 = `M×N` 어댑터. 이게 LSP 이전의 IDE × 언어 통합과 정확히 같은 문제 구조다.

### 1.3. MCP의 한 줄짜리 정의

> **MCP는 도구 호출 메시지를 표준화한 게 아니라, "호스트가 어떤 도구를 발견하고, 그 도구의 스키마를 어떻게 협상하고, 어떻게 실행 요청을 주고받느냐"를 표준화한 것이다.**

도구 호출 *결과*는 여전히 모델 측 tool_use/tool_result 흐름에 들어간다. MCP는 그 *공급선*을 갈아끼운 것이다.

```
[모델 ↔ 호스트]  ← 여전히 각 LLM 공급사 포맷(tool_use 등)
[호스트 ↔ 도구]  ← 여기를 MCP가 표준화
```

---

## 2. MCP의 데이터 레이어 — 다양한 도구 개발의 시작점

공식 스펙은 MCP를 두 개의 레이어로 정의한다.

| 레이어 | 역할 |
|---|---|
| **Data layer** | JSON-RPC 2.0 메시지 구조, 라이프사이클, 프리미티브 |
| **Transport layer** | stdio · Streamable HTTP, 메시지 프레이밍, 인증 |

도구를 만든다는 것은 곧 *데이터 레이어*에 구현체를 끼우는 일이다. 호스트가 어떤 트랜스포트로 들어오든, 데이터 레이어의 JSON-RPC 메시지는 동일하다.

### 2.1. 참여자 세 종류

- **Host**: AI 애플리케이션 자체 — Claude Code, Claude Desktop, VS Code, Cursor, ChatGPT 등.
- **Client**: 호스트 내부의 *서버 1개당 1개*씩 만들어지는 연결 객체.
- **Server**: 도구/리소스/프롬프트를 제공하는 프로그램. 로컬(stdio)일 수도, 원격(HTTP)일 수도 있다.

> "MCP server"라는 단어는 *어디서 실행되는지*와 무관하다. 같은 머신의 자식 프로세스든, 원격 SaaS 엔드포인트든, 공급하는 쪽이면 모두 서버다.

### 2.2. 라이프사이클 — `initialize` 핸드셰이크

MCP는 **stateful 프로토콜**이다. 첫 메시지는 항상 `initialize`이고, 여기서 양쪽이 **capability negotiation**을 한다.

```json
// Client → Server
{
  "jsonrpc": "2.0", "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": { "elicitation": {} },
    "clientInfo": { "name": "example-client", "version": "1.0.0" }
  }
}
```

```json
// Server → Client
{
  "jsonrpc": "2.0", "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools":     { "listChanged": true },
      "resources": {}
    },
    "serverInfo": { "name": "example-server", "version": "1.0.0" }
  }
}
```

핸드셰이크에서 결정되는 것:
1. **버전 호환성**: 양쪽이 합의된 `protocolVersion`이 없으면 즉시 연결 종료. (강의 시연 시 자주 보이는 *"Server failed to start"*의 한 원인.)
2. **무엇을 제공/요청할 수 있나**: 서버는 자기가 `tools / resources / prompts` 중 어떤 것을 제공할지, 클라이언트는 자기가 `sampling / elicitation / roots` 중 무엇을 처리할 수 있는지 선언한다.
3. **변경 알림 지원 여부**: `"listChanged": true` 가 있어야만 서버가 나중에 `notifications/tools/list_changed` 같은 푸시를 보낼 수 있다.

### 2.3. 서버 프리미티브 세 종류

| 프리미티브 | 누가 부르나 | 무엇을 위해 |
|---|---|---|
| **Tools** | 모델(에이전트)이 호출 | 액션 — DB 쿼리, 파일 쓰기, API POST |
| **Resources** | 호스트/모델이 *읽음* | 컨텍스트 — 파일 내용, 스키마, 로그 스냅샷 |
| **Prompts** | 사용자/호스트가 선택 | 재사용 가능한 슬래시 커맨드/템플릿 |

세 가지 모두 표준화된 디스커버리 메서드를 갖는다.

- `tools/list` → `tools/call`
- `resources/list` → `resources/read`
- `prompts/list` → `prompts/get`

**도구 개발자 입장에서의 의미**: 만들 도구가 *"부수효과가 있는가, 단순 조회인가, 시스템 프롬프트에 가까운가"* 셋 중 하나에 맞춰 위치를 정해야 한다.
- 결과를 *컨텍스트로 주입*하고 싶다면 `Resource`(예: `db://schema/users`)가 더 적합하다 — 호스트는 이를 토큰 제한 안에서 미리 읽어둘 수 있다.
- 호스트의 슬래시 명령으로 노출하고 싶다면 `Prompt`로 만든다 (예: `/qa` → "QA 모드 시작").
- 모델이 **자율 판단으로 호출**할 액션이면 `Tool` 이다.

이 구분이 흐려진 서버가 가장 흔한 안티패턴이다 — 모든 걸 `tool`로만 노출하면 호스트가 매번 LLM 토큰을 써서 조회를 해야 한다.

### 2.4. 클라이언트 프리미티브 — 양방향성

현행 스펙(`2025-11-25`)이 명시하는 세 가지:

- **Sampling**: *서버가 호스트의 LLM을 거꾸로 빌려 쓰는* 메서드 (`sampling/createMessage`). 서버 안에서 LLM SDK를 임포트하지 않아도 모델 호출이 가능해진다. `2025-11-25` 부터는 sampling 요청 안에서 `tools` / `toolChoice` 를 함께 보낼 수 있어, 서버가 *도구 사용까지 포함된 LLM 호출*을 위임할 수 있다.
- **Elicitation**: *서버가 사용자에게 직접 추가 질문을 던지는* 메서드 (`elicitation/create`). 승인·확인·누락된 인자 채우기에 쓰인다. `2025-11-25` 에서는 **URL elicitation**(브라우저로 외부 인증/동의 페이지를 열고 결과를 받기)이 추가됐다.
- **Roots**: 서버가 *"내가 작업할 수 있는 경로/URI 범위가 어디까지인가"*를 클라이언트에 묻는 메커니즘. 파일시스템 권한 경계가 여기서 만들어진다.

`★ Insight ─────────────────────────────────────`
"호스트가 서버를 부른다"의 단방향만 생각하기 쉽지만, MCP는 서버→호스트 호출도 표준화돼 있다. Sampling/Elicitation을 갖춘 서버는 *호스트의 LLM·사용자·파일시스템을 빌려 쓰는* 미니 에이전트가 될 수 있다. Part 3-2의 Ouroboros 사례가 이걸 극단적으로 활용한 구조다.
`─────────────────────────────────────────────────`

### 2.5. 트랜스포트 두 가지

| 트랜스포트 | 언제 |
|---|---|
| **stdio** | 호스트가 *자식 프로세스로 띄우는* 로컬 서버. 1:1 연결, 네트워크 오버헤드 없음. CLI 도구·로컬 파일 접근·로컬 DB 접속에 적합. |
| **Streamable HTTP** | 원격 SaaS·다중 사용자 서버. POST 기반에 옵션으로 Server-Sent Events 스트리밍. 인증은 표준 HTTP — bearer 토큰·API 키·**OAuth(권장)**. |

`Streamable HTTP`는 `2025-03-26` 스펙부터 도입된 트랜스포트로, 이전의 `HTTP+SSE`(별도 두 엔드포인트)를 단일 엔드포인트로 통합한 것이다. 기존 SSE 트랜스포트만 지원하는 호스트도 한동안 공존한다 — Codex/Claude Code 모두 두 가지를 모두 받는다.

```
stdio          : 한 줄 한 줄 JSON-RPC (line-delimited)
Streamable HTTP: POST /mcp   + SSE 응답 스트림
```

### 2.6. 알림(Notifications)

JSON-RPC에서 `id`가 없는 메시지 = 응답 불요. MCP는 이걸로 *상태 변경 푸시*를 한다.

- `notifications/tools/list_changed` — 사용 가능한 도구 목록이 바뀜
- `notifications/resources/updated` — 특정 리소스 내용 갱신
- `notifications/progress` — 장시간 작업 진행률

호스트는 알림을 받자마자 `tools/list`를 다시 부르는 식으로 리프레시 한다 — *폴링이 아니라 이벤트 기반*이라는 점이 LSP 와 같다.

---

## 3. MCP로 무엇까지 가능한가 — 히스토리

### 3.1. 출시와 초기 합류

| 날짜 | 사건 |
|---|---|
| **2024-11-25** | Anthropic이 MCP를 오픈소스로 공개. 저자는 **David Soria Parra**와 **Justin Spahr-Summers**. 동기는 *"가장 똑똑한 모델도 정보 사일로 뒤에 갇혀 있다"*. |
| 2024-11 | 초기 레퍼런스 서버 6종: **Google Drive · Slack · GitHub · Git · Postgres · Puppeteer**. |
| 2024-11 | 초기 통합 파트너: **Block · Apollo**(엔터프라이즈 어답터), **Zed · Replit · Codeium · Sourcegraph**(개발툴). |
| 2025-03 | **OpenAI**가 MCP 공식 채택 발표 — Agents SDK/ChatGPT desktop. |
| 2025-04 | **Google DeepMind**가 Gemini SDK에서 MCP 지원 공식화. |
| 2025-05~06 | GitHub·Microsoft가 공동 작업한 **GitHub MCP Server** 정식 출시. |
| 2025-06-18 | 직전 안정 revision. Streamable HTTP·OAuth·Elicitation·구조화 출력(`structuredContent`)이 정식 포함. |
| 2025-하반기 | **MCP Registry** (`registry.modelcontextprotocol.io`) 공개 — 서드파티 서버 발견·메타데이터 표준화. |
| **2025-11-25** | **현행 스펙.** 주요 변경: (1) **OAuth/OIDC Discovery** 및 incremental scope consent(`WWW-Authenticate`) — 인증 흐름이 본격적인 엔터프라이즈 수준으로 확장. (2) Tools·Resources·Prompts 에 **icons 메타데이터** 추가. (3) Sampling 에 **`tools` / `toolChoice`** 인자 — 서버가 도구 사용까지 포함된 LLM 호출을 호스트에 위임 가능. (4) **URL mode elicitation** — 외부 동의 페이지 흐름 표준화. (5) **OAuth Client ID Metadata Documents** 권장 — 동적 클라이언트 등록 부담 감소. (6) **실험적 `Tasks` 프리미티브** — durable execution / 폴링 / 지연 결과 회수. (7) Elicitation 스키마가 JSON Schema 2020-12 정렬, default 값 지원, single/multi-select enum. (8) stdio 서버가 `stderr` 를 일반 로깅 채널로 사용해도 됨이 명문화. (9) Streamable HTTP 의 잘못된 `Origin` 헤더는 `HTTP 403` 으로 응답 필수. (10) 도구 입력 검증 오류는 *Protocol Error* 가 아니라 *Tool Execution Error* 로 반환해 모델이 자기 교정 가능하게 함. |

> 약 6개월 만에 *경쟁 LLM 공급사 전원이 같은 프로토콜을 채택*했다는 점이 MCP의 특이성이다. AI 분야에서 "표준"이 이렇게 빨리 자리잡은 사례는 드물다.

### 3.2. 무엇이 가능해졌나 — 카테고리별

스펙 자체는 "도구 호출 + 컨텍스트 주입"만 정의하지만, *그 단순함이 외연을 폭발시켰다*. 작성일 기준 실제로 활용되는 사용처를 묶으면 다음과 같다.

1. **에이전트 ↔ 에이전트 호출**
   - 한 에이전트(Claude Code)에서 다른 에이전트(Codex CLI)를 MCP 서버로 노출해 호출. → Session 3-2 실습.
   - 메타-에이전트가 자식 에이전트를 spawn 하고 그 결과를 회수.

2. **코드 호스팅 / 이슈 트래커**
   - GitHub MCP — PR 만들기, 코드 리뷰 댓글 가져오기, Actions 로그 조회.
   - Linear / Jira(Atlassian) — 이슈 생성/이동/필드 업데이트.
   - GitLab — 아카이브 됐지만 커뮤니티 포크 다수.

3. **데이터베이스 / 데이터 웨어하우스**
   - Postgres / SQLite / DuckDB / Snowflake / BigQuery 용 MCP 서버.
   - 쓰기 가능 / 읽기 전용 모드를 강제하는 것이 안전 패턴 (Session 3-1의 "위험한 시그니처" 논의와 직결).

4. **브라우저 자동화 / UI 검증**
   - **Playwright MCP** (Microsoft) — 현재 가장 활발하게 쓰이는 서버 중 하나. UI 회귀 확인에 결합.
   - Puppeteer MCP — Anthropic 초기 레퍼런스.

5. **디자인 도구**
   - **Figma Dev Mode MCP** — Figma 공식. *Claude Code generates an entire web app from a Figma design* 시연이 가능하게 한 핵심 구성요소.

6. **모니터링 / 관측성**
   - **Sentry MCP** (Sentry 공식) — 이슈를 컨텍스트로 끌어와 디버깅.
   - Grafana / Datadog 비공식 서버 다수.

7. **결제 / SaaS / 인프라**
   - **Stripe MCP** — 결제·고객·구독 데이터 조회/생성.
   - **Cloudflare MCP** — Workers·DNS·KV 조작. 원격 MCP(Streamable HTTP) 형태.
   - **Notion MCP**·**Slack MCP** — 메모/메시징 통합.

8. **로컬 시스템 / CLI 래핑**
   - Filesystem (Anthropic 레퍼런스) — 경로 화이트리스트로 접근 제한.
   - Memory — 지식 그래프 기반 영속 메모리.
   - Sequential Thinking — 모델 자기성찰 보조 도구.
   - 거의 모든 CLI 명령(예: `kubectl`, `aws`, `gcloud`)이 비공식 MCP 래퍼로 존재.

9. **MCP 게이트웨이 — "여러 MCP 서버를 하나로 묶기"**
   - **Docker MCP Gateway / Toolkit** — 컨테이너로 격리된 여러 MCP 서버를 단일 엔드포인트로 노출. Session 3-3의 *"하나의 MCP를 여러 도구에서 재사용"* 시나리오의 표준 후보.
   - 다른 형태: Smithery, Cline의 marketplace, Open WebUI MCPO.

### 3.3. 지금 가장 성숙도가 높은 사례 (작성일 기준 체감)

- **GitHub MCP Server**: GitHub/Microsoft가 직접 운영. PR-driven workflow의 표준 채널이 됐다.
- **Sentry MCP**: 원격 MCP(Streamable HTTP + OAuth)의 모범 사례 — 인증·다중 사용자·실서비스 사이드이펙트가 모두 들어 있는 흔치 않은 사례.
- **Playwright MCP**: 에이전트가 *실제 브라우저로 UI 확인을 하는* 가장 깔끔한 통로. UI 자동화의 "GitHub Copilot 모먼트"라 평가된다.
- **Figma Dev Mode MCP**: 디자인→코드 흐름을 진짜로 만들어낸다. 사내 디자인 시스템과 결합 시 효과가 가장 크다.
- **Docker MCP Gateway**: "팀 전체에 같은 도구 묶음을 같은 방식으로" 배포하는 표준화의 첫 후보.

---

## 4. 보안·신뢰 모델 — 강의 3-1과 직결되는 부분

스펙은 *프로토콜 수준에서는 보안을 강제하지 않는다*고 명시하고, 호스트에 다음 의무를 부여한다.

1. **User Consent and Control** — 데이터 접근/도구 실행 전 명시적 동의.
2. **Data Privacy** — 호스트가 사용자 데이터를 서버에 노출하기 전 명시적 동의.
3. **Tool Safety** — *"도구 설명(어노테이션)조차 신뢰할 수 없는 입력으로 취급하라"*. 도구 호출은 곧 임의 코드 실행이다.
4. **LLM Sampling Controls** — 서버가 호스트 LLM을 빌려 쓸 때, 사용자가 *프롬프트와 결과 가시성*을 통제해야 한다.

강의 3-1의 "MCP 서버를 위험도별로 분류" / "위험한 도구 시그니처" / "연결 전 질문" 블록은 정확히 이 보안 원칙을 학습용으로 풀어쓴 것이다. 매핑하면:

| 강의 항목 | 스펙상의 근거 |
|---|---|
| 읽기 전용 / 쓰기 가능 분류 | Tool Safety — 부수효과 명시 의무 |
| 인증 정보 필요 | OAuth 권장(Streamable HTTP) + Host의 secret 분리 책임 |
| 임의 SQL 실행 도구 금지 | Tool annotations are untrusted — 화이트리스트·enum·preset로 좁히기 |
| 연결 전 5가지 질문 | User Consent and Control — 호스트가 보여줄 UX 의무 |

---

## 5. Session 3-1에 그대로 쓰는 핵심 메시지 5가지

1. **MCP는 도구 호출이 아니라, 도구 호출의 *공급선*을 표준화한 프로토콜이다.**
2. **LSP에서 영감을 받아 `M×N → M+N`을 해결한다** — 이 비유 하나로 도입 동기가 모두 설명된다.
3. **세 가지 서버 프리미티브(Tools/Resources/Prompts) 중 어디에 도구를 둘지가 곧 도구 설계다.** 모두 Tool로 만들면 호스트는 매번 LLM 토큰을 써서 조회하게 된다.
4. **트랜스포트는 두 가지뿐이지만 의미가 다르다** — stdio는 *로컬 권한 확장*, Streamable HTTP는 *외부 SaaS 확장*. 위험도와 인증 모델이 다르다.
5. **연결 = 권한 확장이다.** 시야를 넓힌 만큼 데이터 노출·외부 비용·쓰기 권한·감사 로그가 따라온다. "연결 전 질문 5가지"는 이 비대칭을 강제로 의식하게 만드는 장치다.

---

## 6. 참고 — 공식 문서 진입점

> 강의 촬영일에 한 번 더 확인할 것. 페이지 구조는 자주 바뀐다.

- MCP 공식 사이트: `https://modelcontextprotocol.io/`
- 스펙(현행): `https://modelcontextprotocol.io/specification/2025-11-25`
- 스펙(`latest` 별칭): `https://modelcontextprotocol.io/specification/latest`
- 스펙 변경 로그(`2025-06-18 → 2025-11-25`): `https://modelcontextprotocol.io/specification/2025-11-25/changelog`
- 아키텍처 개요: `https://modelcontextprotocol.io/docs/concepts/architecture`
- 레퍼런스 서버: `https://github.com/modelcontextprotocol/servers`
- MCP Registry: `https://registry.modelcontextprotocol.io/`
- MCP Inspector(디버깅 도구): `https://github.com/modelcontextprotocol/inspector`
- Anthropic 출시 발표(2024-11-25): `https://www.anthropic.com/news/model-context-protocol`
- Claude Code 측 MCP 문서: `https://docs.claude.com/` 의 MCP 섹션 (촬영일 확인)
- Codex 측 MCP/config 문서: `https://developers.openai.com/codex/` 의 MCP 섹션 (촬영일 확인)

각 벤더 공식 MCP 서버는 해당 벤더의 공식 docs에서 검색할 것 — Sentry, Stripe, Cloudflare, Figma, GitHub, Notion 등.
