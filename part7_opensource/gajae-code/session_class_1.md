@part7_opensource/gajae-code/ 에서 

사용자 PC 에 설치 시 활용되는 "루트부터 읽기: `CLAUDE.md`·`AGENTS.md`·`.mcp.json`" 등은 어디에 있고 어떤 내용을 담고 있나요?

---

핵심까지 다 확인했습니다. 질문하신 "루트부터 읽기: CLAUDE.md·AGENTS.md·.mcp.json"는 사실 두 개의 서로 다른 층위를 가리키는데, 이 둘을 구분하는 게 답의 핵심입니다.

★ Insight ─────────────────────────────────────

같은 파일명(CLAUDE.md/AGENTS.md/.mcp.json)이 저장소 자체의 계약서(이 repo에서 작업할 때 읽히는 것)와, gjc가 사용자 PC에서 실행될 때 사용자의 작업 폴더에서 발견·로드하는 대상이라는 두 역할을 동시에 합니다.
"설치 시 활용된다"는 후자입니다 — 코드는 discovery/ 모듈에 있고, 정적 파일이 아니라 **런타임 스캐너(provider)**입니다.
이 구조는 "capability registry + self-registering provider" 패턴이라, 한 줄의 import "./claude"만으로 provider가 레지스트리에 자기를 등록합니다.
─────────────────────────────────────────────────
1. 층위 A — gajae-code 저장소 자체의 루트 계약 파일
이건 "사용자 PC 설치"용이 아니라, 이 repo를 코딩 에이전트가 다룰 때 읽는 파일입니다.

파일	위치	내용
CLAUDE.md	gajae-code 루트 (5.2KB)	"Read AGENTS.md first" → AGENTS.md로 위임. GitNexus 위키 우선 탐색 규칙
AGENTS.md	gajae-code 루트 (13.7KB)	실제 권위 계약서 — 워크플로 라우팅, 코딩 규칙, 검증 절차
참고: .mcp.json은 이 루트에 존재하지 않습니다 (ls 확인). 즉 "루트부터 읽기" 목록의 .mcp.json은 저장소 산출물이 아니라, 아래 런타임 스캐너가 사용자 환경에서 찾는 대상일 뿐입니다.

2. 층위 B — "설치 시 활용되는" 실체: discovery 모듈
질문하신 동작의 코드는 전부 여기에 있습니다:

📁 packages/coding-agent/src/discovery/

index.ts가 각 provider를 import하면, provider 파일들이 로드되는 즉시 registerProvider(...)로 capability registry에 자신을 등록합니다. gjc가 사용자 PC에서 세션을 시작할 때(시동 스캔, AI_AGENT_HARNESS_VIEW.md:132의 "deadline-raced 시동") 이 provider들이 사용자의 cwd·상위 디렉토리·홈을 훑어 설정 파일을 끌어옵니다.

세 파일별 담당 provider
대상	담당 파일	우선순위	스캔 경로
CLAUDE.md	claude.ts	80	프로젝트 한정 <cwd>/.claude/CLAUDE.md
AGENTS.md (루트형)	agents-md.ts	10	cwd→repoRoot/home까지 위로 walk-up하며 각 디렉토리의 AGENTS.md
AGENTS.md (.agent형)	agents.ts	70	.agent/·.agents/ 의 AGENTS.md (프로젝트 walk-up + 사용자 홈 ~/)
.mcp.json	mcp-json.ts	5 (fallback)	<cwd>/mcp.json, <cwd>/.mcp.json
각 provider가 실제로 읽는 내용:

claude.ts — 단순히 CLAUDE.md만이 아니라 .claude/ 디렉토리 전체를 capability별로 로드합니다: CLAUDE.md(컨텍스트), .claude/.mcp.json(MCP 서버, claude.ts:45-82), skills/, commands/, hooks/pre·post/, tools/, settings.json, SYSTEM.md.
⚠️ 중요한 의도된 동작: 사용자 홈(~/.claude)은 일부러 무시합니다 (claude.ts:1-7 docstring). 사용자의 전역 Claude 설정이 gjc 세션에 주입되지 않도록 한 격리 결정입니다.
mcp-json.ts — Claude Desktop 포맷(mcpServers 키, mcp-json.ts:23-52)을 파싱해 command/args/env/url/auth/oauth 등을 정규 MCPServer 객체로 변환하고, ${ENV_VAR}를 expandEnvVarsDeep로 치환합니다. 우선순위 5라서 도구별 provider가 못 찾았을 때의 최후 fallback입니다.
agents-md.ts — dot-디렉토리(.codex 등)는 건너뛰고(agents-md.ts:36) 순수 루트형 AGENTS.md만, cwd에서 위로 올라가며 수집합니다.
3. "루트부터 읽기"라는 표현의 실체 = 정렬 순서
발견된 AGENTS.md/CLAUDE.md들은 system-prompt.ts의 loadProjectContextFiles에서 depth 내림차순으로 정렬됩니다 (system-prompt.ts:266-274):

"Sort by depth (descending): higher depth (farther from cwd) comes first, so files closer to cwd appear last/more prominent."

즉 루트(상위)에서 시작해 아래로 내려오며 읽되, cwd에 가장 가까운 파일이 맨 마지막에 와서 가장 강하게 작용합니다. 이게 사용자가 말한 "루트부터 읽기"의 정확한 메커니즘입니다 — 멀리 있는 일반 규칙 → 가까운 구체 규칙 순으로 누적되어, 가까운 파일이 덮어쓰는(override) 효과를 냅니다.

한 가지 주의할 점 (소스 읽을 때 헷갈릴 수 있음)
claude.ts의 주석에 "Anthropic Code project provider", `.Anthropic model/` 같은 표현이 보이는데, 이건 배포본 생성 과정의 문자열 치환 아티팩트입니다. 실제 동작 코드는 CONFIG_DIR = ".claude" (claude.ts:35)로 정상이니, 주석이 아니라 상수/로직을 기준으로 보시면 됩니다.

요약하면 — 질문하신 "설치 시 활용되는 루트부터 읽기" 로직은 정적 파일이 아니라 packages/coding-agent/src/discovery/의 provider 코드(claude.ts·agents.ts·agents-md.ts·mcp-json.ts)이고, gjc가 사용자 PC에서 실행될 때 사용자의 cwd→상위→홈을 훑어 .claude/CLAUDE.md·AGENTS.md·.mcp.json을 발견한 뒤 system-prompt.ts에서 depth 순으로 시스템 프롬프트에 병합합니다.

더 깊이 보고 싶은 부분이 있으신가요? 예를 들어 ① 발견된 MCP 서버가 실제로 연결되는 흐름(MCPManager), ② .codex/.cursor/.gemini 등 타 에이전트 설정까지 흡수하는 provider들, ③ 시동 스캔 데드라인(STARTUP_SCAN_DEADLINE_MS) 동작 중 하나를 더 파볼 수 있습니다.

===

실제로 만들어지는 MD 파일의 내용, 그리고 MCP 서버는 어떤 것들이 연결되는지,
그것들이 어떻게 사용되는지도 알려주세요.

---

핵심 메커니즘을 모두 확인했습니다. 정리해서 세 갈래로 답하겠습니다.

★ Insight ─────────────────────────────────────

MD 파일은 디스크에 미리 존재하는 게 아니라 빌드 시점에 바이너리에 임베드됩니다. import ... with { type: "text" } 구문(gjc-defaults.ts:3-12)으로 SKILL.md 텍스트가 실행 파일 안에 박히고, 설치 시 사용자 디스크로 "풀어놓습니다(materialize)".
MCP는 "다 연결"하지 않습니다 — 1급 네이티브 기능이 있는 서버(Exa·브라우저)는 일부러 연결 대상에서 제외하고, URL에서 API 키만 뽑아 내장 도구로 대체합니다.
연결 lifecycle은 Anthropic prompt-cache 안정성을 위해 도구 배열을 항상 이름순 정렬하는 등, 토큰 비용 최적화가 코드 곳곳에 박혀 있습니다.
─────────────────────────────────────────────────
A. 실제로 만들어지는 MD 파일
설치 진입점은 cli/setup-cli.ts:375의 installDefaultGjcDefinitions()이고, 본체는 defaults/gjc-defaults.ts:150-188입니다.

대상 경로: getAgentDir() = ~/.gjc/agent (dirs.ts:269). 설정 루트는 ~/.gjc고, 에이전트 산출물은 그 아래 agent/입니다.

써지는 파일 (총 8개 — 스킬 4 + 프래그먼트 4):

파일 (~/.gjc/agent/ 기준)	종류	내용(frontmatter description)
skills/deep-interview/SKILL.md	스킬	소크라테스식 심층 인터뷰 — 수학적 모호성 게이팅으로 실행 승인 전 요구사항 확정 (pipeline: [deep-interview, plan], handoff-policy: approval-required, level 3)
skills/ralplan/SKILL.md	스킬	합의 기반 플래닝 진입점 — 모호한 team/ultragoal 요청을 실행 전 자동 게이팅 (level 4)
skills/team/SKILL.md	스킬	멀티 워커 tmux 팀 오케스트레이션
skills/ultragoal/SKILL.md	스킬	repo-native 다중 목표 플랜을 goal mode 산출물로 생성·실행
skill-fragments/deep-interview/auto-research-greenfield.md	프래그먼트	deep-interview의 on-demand 조각
skill-fragments/deep-interview/auto-answer-uncertain.md	프래그먼트	〃
skill-fragments/deep-interview/lateral-review-panel.md	프래그먼트	〃
skill-fragments/ultragoal/ai-slop-cleaner.md	프래그먼트	ultragoal의 조각
★ Insight ─────────────────────────────────────

"skill" vs "skill-fragment" 분리가 핵심 설계입니다. SKILL.md는 항상 로드되지만, 프래그먼트는 워크플로 중 필요할 때만 에이전트가 읽습니다 — 이게 첫 답변에서 본 AI_AGENT_HARNESS_VIEW.md:287의 "완료 게이트 hook에서 on-demand 로드"입니다. 상시 컨텍스트를 작게 유지하는 토큰 절약 패턴입니다.
네 스킬 모두 frontmatter에 source: "forked from upstream ... rebranded for GJC"라고 적혀 있어, 상위 오픈소스 스킬을 포크해 GJC 브랜드로 재작성한 것임을 솔직히 밝힙니다.
─────────────────────────────────────────────────
멱등성(idempotency) 로직 (gjc-defaults.ts:161-168):

--check: 디스크와 비교만 → missing/matching/different
파일이 이미 있고 --force가 아니면 → skipped (사용자 수정본 보존)
없거나 --force → Bun.write()로 덮어씀 → written
즉 사용자가 손댄 스킬을 함부로 덮어쓰지 않는 게 기본값입니다.

B. 연결되는 MCP 서버 — "무엇을 연결하고, 무엇을 일부러 빼는가"
설정 로딩은 runtime-mcp/config.ts:95의 loadAllMCPConfigs()입니다. 첫 답변에서 본 discovery provider들(.mcp.json, .claude/.mcp.json, codex/cursor/gemini 등)이 모은 서버 목록을 받아 두 단계 필터를 거칩니다:

1) 비활성 제거
enabled === false이거나 사용자의 ~/.gjc disabled 목록(config.ts:109-117)에 있으면 스킵.

2) 네이티브 기능과 겹치는 서버 제거 (핵심)
필터	기본값	동작
filterExa	true	Exa MCP 서버를 연결 목록에서 제거하고 URL/args/env에서 exaApiKey만 추출 (config.ts:221-245)
filterBrowser	false	puppeteer/playwright/browserbase 등 브라우저 MCP 제거 (config.ts:282-334)
Exa가 특별한 이유: gjc는 Exa를 일반 MCP 서버로 붙이는 대신, exa/ 디렉토리에 22개 1급 네이티브 도구를 직접 구현해 두었습니다 (exa/index.ts:1-18):

검색 4종(search/deep/code/crawl) + LinkedIn 1 + 회사조사 1 + researcher 2 + websets 14
이 네이티브 도구가 추출한 API 키로 https://mcp.exa.ai/mcp·https://websetsmcp.exa.ai/mcp에 클라이언트로 직접 호출 (exa/types.ts:9-10)
★ Insight ─────────────────────────────────────

이건 "MCP는 범용 확장 통로, 자주 쓰는 건 네이티브로 내재화"라는 이중 전략입니다. 사용자가 .mcp.json에 Exa를 적어두면 gjc가 조용히 가로채 자기 네이티브 구현으로 라우팅합니다 — MCP 핸드셰이크/스키마 협상 왕복을 줄여 시동을 빠르게 합니다.
isExaMCPServer는 이름("exa")·URL 패턴(mcp.exa.ai)·stdio args(mcp-remote 경유)까지 3중으로 판별(config.ts:147-170)해, 사용자가 어떤 형식으로 적든 잡아냅니다.
─────────────────────────────────────────────────
정리하면 연결되는 것: .mcp.json/.claude/.mcp.json 등에 적힌 사용자 정의 MCP 서버 중, Exa·(옵션)브라우저를 제외한 나머지 전부. 연결 안 하고 네이티브로 대체되는 것: Exa(항상), 브라우저(옵션).

C. 연결 lifecycle — MCPManager
discoverAndConnect()(manager.ts:323) → connectServers()가 모든 서버를 병렬 연결합니다. 주목할 설계:

공격적 시동 타임아웃 — 기본 250ms, 설정값 있으면 최대 1500ms (manager.ts:60-73). 시동을 막지 않으려고 짧게 끊습니다.
타임아웃 시 캐시 폴백 — 제때 안 붙은 서버는 DeferredMCPTool로 이전 세션 캐시 도구를 먼저 노출하고, 실제 연결은 백그라운드에서 마저 진행(manager.ts:532-599). → 첫 응답이 빨라집니다.
자동 재연결 — transport가 끊기면 onClose가 reconnectServer()를 트리거, [500,1000,2000,4000]ms 백오프로 재시도(manager.ts:890-930). 재연결 중에도 낡은 도구를 등록에 남겨둬 선택 상태를 유지.
OAuth 자동 갱신 — 만료 5분 전 또는 401 시 토큰 리프레시(manager.ts:1248-1251).
이름순 안정 정렬 — sortMCPToolsByName()(manager.ts:116-119). 연결 순서가 비결정적이어도 도구 배열 바이트가 동일하게 유지되어 Anthropic prompt-cache 브레이크포인트가 깨지지 않습니다 — 직접적인 토큰 비용 절감.
프로세스 전역 싱글톤 — top-level 세션만 소유하고 subagent는 상속만(첫 답변의 소유권 게이트 불변식과 동일).
D. 그래서 런타임에서 어떻게 쓰이나
연결된 MCP가 에이전트에게 노출되는 4가지 통로:

통로	메커니즘
도구	서버 도구가 MCPTool로 감싸져 mcp__<서버>_<도구> 이름의 CustomTool이 됨 (manager.ts:505, :619) → 일반 내장 도구와 동일하게 호출
시스템 프롬프트	getServerInstructions()(manager.ts:1214)로 각 서버의 instructions를 모아 프롬프트에 주입
resources / prompts	list_changed 알림 구독, 리소스 읽기/프롬프트 실행(manager.ts:1178, :1200) — MCP 프롬프트는 슬래시 커맨드로도 노출
roots	서버가 roots/list를 물으면 현재 cwd를 file URL로 반환(manager.ts:681-690) → 서버가 작업 폴더를 인지
그리고 materialize된 MD 스킬은 이 도구 계층과 별개로, 워크플로 단계 언어로 소비됩니다 — 사용자가 /deep-interview 같은 스킬을 부르면 에이전트가 ~/.gjc/agent/skills/...의 SKILL.md 지시를 따르고, 필요 시점에 skill-fragments/의 조각을 추가로 읽습니다.

전체 흐름을 한 줄로: 설치 시 installDefaultGjcDefinitions가 임베드된 8개 MD를 ~/.gjc/agent에 풀어놓고 → 세션 시동 시 discovery가 사용자 .mcp.json을 모아 Exa/브라우저는 네이티브로 가로채고 나머지는 MCPManager가 병렬·캐시폴백·자동재연결로 붙인 뒤 → 도구·프롬프트·리소스·roots 네 통로로 에이전트에 공급합니다.

다음으로 들어가 볼 만한 갈래: ① 가로챈 Exa 네이티브 22개 도구의 실제 호출 흐름(exa/mcp-client.ts), ② DeferredMCPTool의 캐시-우선 노출이 실제 호출 시 어떻게 실연결로 승격되는지, ③ MD 스킬 프래그먼트가 "완료 게이트"에서 로드되는 정확한 트리거. 어느 쪽을 볼까요?


===

CLAUDE.md 또는 AGENTS.md 에 덮어쓰기 하는 내용은 없나요?

---

독립 grep으로 이미 강한 결론이 나왔고, 워크플로는 제가 아직 직접 안 본 차원(config-writer, hook, 메모리/learnings, 스캐폴드 템플릿)을 마저 검증 중입니다. 우선 확정된 부분을 정리해 드립니다.

★ Insight ─────────────────────────────────────

결정적 신호: 소스 트리(테스트 제외)에서 AGENTS.md/CLAUDE.md 문자열과 Bun.write/writeFile/.write(가 같은 파일 안에 공존하는 경우가 0건입니다. 즉 이 두 파일을 프로그램이 직접 써넣는 경로가 없습니다.
path.join(..., "AGENTS.md"/"CLAUDE.md")가 등장하는 곳은 전부 discovery/(읽기 provider)와 commit/agentic(컨텍스트로 읽어서 커밋 메시지에 반영)뿐 — 전부 읽기 전용입니다.
/init은 코드가 아니라 프롬프트입니다. 파일을 직접 쓰는 게 아니라 LLM에게 "AGENTS.md를 만들라"고 지시합니다.
─────────────────────────────────────────────────
잠정 결론 (grep 기준, 워크플로 검증 대기 중)
자동으로 CLAUDE.md/AGENTS.md를 덮어쓰는 코드는 없습니다. 그 파일들이 써지는 경로는 딱 두 가지인데, 둘 다 "프로그램의 자동 덮어쓰기"가 아닙니다:

/init 슬래시 커맨드 — LLM 주도(model-driven)
prompts/agents/init.md는 frontmatter가 name: init, description: Generate AGENTS.md for current codebase인 프롬프트입니다. 본문은:

"Generate AGENTS.md by launching multiple explore agents in parallel ... then synthesize findings into a single file."

즉 gjc가 Bun.write로 쓰는 게 아니라, 에이전트가 자기 Write 도구로 AGENTS.md(제목은 "Repository Guidelines")를 생성합니다. 사용자 권한 승인을 거치는 일반 파일 쓰기이고, 대상은 AGENTS.md만 (CLAUDE.md는 /init 대상이 아님).

에이전트의 범용 Write/Edit 도구 — 역시 LLM 주도
AGENTS.md/CLAUDE.md를 특별 취급하지 않고 일반 파일과 동일하게 다룹니다. 모델이 명시적으로 편집할 때만, 사용자 승인을 거쳐 덮어씁니다.

→ 첫 답변들에서 본 materialize(installDefaultGjcDefinitions)는 SKILL.md만 쓰지, CLAUDE.md/AGENTS.md는 절대 건드리지 않습니다. discovery provider도 전부 읽기 전용입니다.

지금 워크플로가 마저 확인하는 것은 제가 grep으로 직접 안 본 사각지대입니다 — ① config-writer.ts나 capability/instruction.ts의 write-back, ② hook이 자동으로 context 파일을 쓰는지, ③ "memory/learnings"류 기능이 AGENTS.md에 append하는지, ④ 숨겨진 스캐폴드 템플릿. 5개 차원 × 후보별 적대적 검증이 끝나면 이 잠정 결론을 확정하거나 보강해서 최종 정리해 드리겠습니다. (백그라운드 작업이라 완료되면 자동으로 이어서 답합니다.)

