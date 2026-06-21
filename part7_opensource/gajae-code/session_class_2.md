@part7_opensource/gajae-code/  

1. 멀티 agents
2. 다양한 hooks
3. Agent skills 

각각을 어떻게 이용하고, 이 Harness 시스템을 활용하여 작업을 어떤식으로 진행하게 되는지 구체적이고 꼼꼼하게 소스코드를 읽고 파악된 내용을 기반으로 답변해주세요.

---

0. 전체 그림 — gajae-code는 "하네스"다
먼저 위치를 잡겠습니다. AI_AGENT_HARNESS_VIEW.md가 잘 정리하듯, GJC(gjc)는 "LLM을 호출하는 wrapper"가 아니라 agent가 실제 개발 작업을 수행하도록 model·tool·state·workflow·multi-agent를 묶어주는 실행 환경입니다. 우리가 평소 쓰는 Claude Code 같은 도구를 GJC는 직접 구현했고, 그래서 멀티 에이전트·hooks·skills가 설정 파일이 아니라 런타임 코드로 존재합니다.

세 주제가 하네스 안에서 맡는 역할:

주제	하네스에서의 역할	정본 소스
멀티 에이전트	한 작업을 역할별 subagent로 분해·위임하고, lifecycle·격리·증거를 가진 "소유된 작업"으로 관리	task/agents.ts, task/index.ts, task/executor.ts
Hooks	워크플로 게이트를 "프롬프트 약속"이 아니라 세션 종료/입력을 차단하는 런타임 술어로 강제	hooks/native-skill-hook.ts, extensibility/hooks/
Agent Skills	요구사항·계획·실행·완료를 단계별 SKILL.md로 캡슐화하고 .gjc/ 상태와 연결	defaults/gjc/skills/, tools/skill.ts
이제 각각을 소스 기반으로 깊이 들어갑니다.

1. 멀티 에이전트 — 역할 위임과 병렬 오케스트레이션
1.1 역할 에이전트는 "프롬프트 + 프론트매터 권한 선언"이다
GJC는 빌드 시점에 8개 역할 에이전트를 바이너리에 임베드합니다. task/agents.ts:48-68의 EMBEDDED_AGENT_DEFS가 정본입니다:


executor · architect · planner · critic · explore · plan · reviewer · task(숨김)
각 에이전트는 마크다운 파일 하나입니다. 핵심은 YAML 프론트매터가 그 에이전트의 권한 헌장이라는 점입니다. frontmatter.md가 스키마를 보여줍니다 — name, description, tools, spawns, model, thinking-level, blocking, hide, forkContext, bashAllowedPrefixes.

제가 직접 읽은 두 에이전트로 대비하면 권한 분리가 명확해집니다:

executor (executor.md) — 쓰기 가능한 구현자

프론트매터에 tools/bashAllowedPrefixes 선언이 없음 → 모든 도구 + 무제한 bash
forkContext: allowed (부모 대화 스냅샷을 배경으로 받을 수 있음)
<ultragoal_red_team_mode> 블록을 내장 — ultragoal 완료 게이트에서 "QA/레드팀"으로 호출되면 happy-path가 아니라 깨뜨리기를 시도하고 executorQa.adversarialCases 증거를 제출
architect (architect.md) — 읽기 전용 리뷰어

tools: read, search, find, lsp, ast_grep, web_search, bash, report_finding
bashAllowedPrefixes: [gjc ralplan --write, gjc state] → bash가 있지만 워크플로 CLI 영속화에만 허용
blocking: true (동기 실행), thinking-level: high
산출물: CLEAR/WATCH/BLOCK + APPROVE/COMMENT/REQUEST CHANGES 판정
★ Insight ─────────────────────────────────────

프론트매터 선언이 진짜 코드로 강제됩니다. 워크플로 검증에 따르면 tools 배열이 있으면 executor.ts:582-601에서 그것만 toolNames로 쓰고, bashAllowedPrefixes는 ToolSession으로 전달돼 bash.ts의 #prepareBashExecution()이 allowlist 밖 명령에 ToolError를 던집니다. 즉 "architect는 읽기 전용"은 프롬프트의 부탁이 아니라 bash 도구가 거부하는 런타임 불변식입니다. 빈 bashAllowedPrefixes(executor)는 무제한을 의미합니다.
─────────────────────────────────────────────────

1.2 위임은 task 도구로, 모니터링은 subagent 도구로
여기서 워크플로 검증이 중요한 정정을 줬습니다 — 두 개의 다른 도구가 있습니다:

task 도구 (task/index.ts:353+) — 부모가 subagent를 스폰할 때 호출. 파라미터: { agent, tasks:[{id, description, assignment, inheritContext?}], context?, schema?, spawnPlan?, isolated? }
subagent 도구 (tools/subagent.ts) — 이미 돌고 있는 subagent를 관찰/취소
task 도구는 자동으로 켜지지 않습니다. 부모 에이전트의 프론트매터에 spawns가 선언돼 있을 때만 executor.ts:586-601이 toolNames에 task를 주입하고, 최대 재귀 깊이(task.maxRecursionDepth 기본 2)에 도달하면 task를 제거해 무한 중첩을 막습니다.

1.3 subagent는 "소유된 작업"이다 — lifecycle·격리·구조화된 yield
평범한 도구는 "model이 텍스트를 내면 끝"이지만, GJC는 subagent를 AI_AGENT_HARNESS_VIEW.md §11대로 lifecycle을 가진 관리 작업으로 다룹니다:

runSubprocess는 OS 프로세스가 아니다 — 같은 프로세스 내 자식 AgentSession입니다(executor.ts). 자식은 자기 turn loop·자기 도구셋(부모 전용 도구는 필터)을 갖고 독립 실행하며, 이벤트를 onProgress 콜백으로 부모에 스트리밍합니다.

하드 스폰 게이트 (spawn-gate.ts) — 제가 직접 읽은 코드입니다. DEFAULT_SPAWN_THRESHOLD = 4. childCount > 4이면 완전한 SpawnPlanReceipt(whyParallel/whyNotLocal/independence/expectedReceiptShape/maxInlineTokens)를 코드가 요구하고, 빠지면 거부합니다. 큰 fan-out의 비용 정당화를 런타임이 강제하는 것입니다(정확히 4개는 통과, 5개부터 영수증 필요).

AsyncJobManager (async/job-manager.ts) — async bash 잡과 task 잡을 한 레지스트리에서 관리. maxRunningJobs 기본 15, ownerId 스탬프(subagent가 부모 잡을 취소 못 함). top-level 세션만 이 싱글톤을 소유·정리하고 subagent는 상속만 합니다.

구조화된 yield 완료 계약 — subagent는 requireYieldTool: true로 생성됩니다. 숨은 yield 도구의 schema-valid 호출이 있어야 런이 "성공"으로 종료. 즉 **"모델이 말을 멈췄다"가 아니라 "명시적으로 제출된 schema-valid 결과"**가 성공 기준입니다.

receipt-only 응답 — 제가 architect.md에서 직접 확인한 가장 인상적인 패턴입니다. architect는 리뷰 전문을 부모 컨텍스트에 붙여넣지 않습니다. 대신:


gjc ralplan --write --stage architect --stage_n <N> --artifact "<full review markdown>" --json
로 디스크에 영속화하고, 호출자에겐 {run_id, path, sha256, stage, stage_n} + 압축 판정만 돌려줍니다(architect.md:87-91). 그래서 최대 5패스를 돌아도 부모 컨텍스트가 receipt 단위로만 증가합니다.

1.4 진짜 병렬 — team 스킬(tmux)
위 task 위임은 한 프로세스 내 자식 세션입니다. 별도 OS 프로세스로 도는 진짜 병렬 워커는 team 스킬이 담당합니다(AI_AGENT_HARNESS_VIEW.md §12):

tmux 백엔드, 기본 워커 3개 / 최대 20개(team-runtime.ts:42-43)
워커 상호작용은 37개 verb의 GJC_TEAM_API_OPERATIONS
단일 writer lease + O_EXCL 배타 생성(fs.open(path,'wx'))으로 race-free task claiming, claim lease 하드코딩 30분
상태는 공유 파일시스템(.gjc/state/team/)에 살므로 로컬 tmux + 공유 FS 전제 (멀티머신 아님)
제어는 scrollback이 아니라 상태 계약으로 — coordinator-mcp가 15개 gjc_coordinator_* 도구를 노출하고, raw tmux 출력은 "bounded advisory"로 강등됩니다
2. Hooks — "정의된 것"과 "살아있는 것"을 구분하라
여기가 GJC에서 가장 오해받기 쉬운 부분입니다. GJC는 "hook"이라는 단어를 세 군데서 다르게 씁니다(AI_AGENT_HARNESS_VIEW.md §20).

★ Insight ─────────────────────────────────────

핵심 통찰: 사용자가 코드로 동작을 짜는 **화려한 24~25개 이벤트 hook API는 이 공개 OSS 빌드에서 "휴면"**이고, GJC를 실제로 "운영 가능"하게 만드는 살아있는 메커니즘은 단 2개 이벤트(UserPromptSubmit/Stop)에 durable 상태 검증을 묶은 fail-closed 게이트 훅입니다. 화려함이 아니라 작고 강제되는 2개가 진짜 엔진입니다.
─────────────────────────────────────────────────

2.1 ① 확장 hook API — 정의됐으나 공개 빌드에서 휴면
extensibility/hooks/types.ts의 in-process TypeScript SDK입니다. pi.on(event, handler)로 구독합니다.

25개 typed 이벤트: 세션 생명주기(session_start, session_before_compact, session.compacting, session_shutdown…) + 에이전트/턴(before_agent_start, agent_start/end, turn_start/end) + tool_call + tool_result + context 등
결정 의미: tool_call은 {block?, reason?}로 도구 실행 전 차단, context는 LLM 메시지 배열 재작성, session_before_*는 {cancel?}로 전이 취소
⚠️ 그러나 공개 빌드에서 휴면: --hook 플래그가 파싱되지 않고, HookRunner는 테스트에만 등장합니다. 워크플로 검증이 이 부분을 정밀화해줬는데, **살아있는 쌍둥이는 별개의 Extensions 서브시스템(ExtensionRunner)**입니다 — agent-session.ts:2963-3032에서 this.#extensionRunner.emit(...)로 agent_start/agent_end/tool_call/tool_result 등을 매 턴 실제로 발화합니다. 즉 이벤트 파이프라인 자체는 살아있고, 그것을 구독하는 사용자 pi.on 로더만 휴면입니다.
→ 강의 관점에서는 이 패키지를 **"레퍼런스 SDK 계약(설계 의도)"**으로, 라이브 구현은 extensions로 설명하는 게 정확합니다.

2.2 ② 네이티브 스킬 훅 — 살아있는 게이트 (제가 직접 읽음)
hooks/native-skill-hook.ts가 워크플로 게이트의 "런타임이 검증·차단한다"의 실제 구현입니다. 제가 전체를 읽었고, 이벤트는 정확히 2개입니다 — GjcNativeHookEventName = "UserPromptSubmit" | "Stop".

UserPromptSubmit 훅 = 활성화 + 우회 차단 (:171-223):

recordSkillActivation()로 프롬프트의 키워드를 탐지해 스킬 활성화 → additionalContext로 주입(soft, block 아님)
그런데 buildActiveUltragoalPromptContext() 결과가 BLOCK_ULTRAGOAL_COMPLETION:으로 시작하면 decision: "block"을 반환 → "goal complete"·"skip verification" 같은 우회 프롬프트를 정규식으로 탐지해 차단
Stop 훅 = loop-until-done의 실체 (:225-235):

buildSkillStopOutput()이 durable 상태(mode-state phase, ultragoal plan/ledger, crystallized spec 파일)가 완료를 증명할 때만 stop을 허용
아니면 decision:"block"으로 세션 종료를 막고 오케스트레이터가 에이전트를 재개. "loop until done"이 프롬프트 지시가 아니라 세션 종료를 검증 상태에 묶은 런타임 차단으로 구현된 것입니다.
fail-closed 편향 (:264-305): malformed JSON 입력은 항상 block, Stop dispatch 에러도 fail-closed(block). 손상·조작된 상태 파일이 세션을 몰래 풀 수 없습니다. (UserPromptSubmit 에러만 fail-open)

키워드 정의는 제가 직접 읽은 skill-keywords.ts에 10개가 있습니다 — $deep-interview/deep interview/interview me/don't assume→deep-interview, $ralplan/consensus plan→ralplan(우선순위 9로 최고), $ultragoal/ultragoal, $team/coordinated team.

2.3 ③ 호스트 통합 — Codex에 노출(expose) + Claude를 소비(consume)
GJC는 외부 runner이므로 자기 게이트 훅을 호스트에 노출하고, 호스트가 정의한 훅을 소비합니다:

EXPOSE(Codex): codex-native-hooks-config.ts가 ~/.codex/hooks.json에 2개 managed 엔트리(UserPromptSubmit/Stop)를 주입. 두 엔트리 모두 command는 "gjc codex-native-hook". → 즉 §2.2의 2-이벤트 게이트를 Codex 세션에서 강제하는 통로입니다.
CONSUME(Claude): capability/hook.ts가 Claude Code 훅을 파일 기반 pre/post 도구 스크립트("pre"|"post")로 발견. 단 프로젝트 .claude만 읽고 ~/.claude는 의도적으로 무시.
★ Insight ─────────────────────────────────────

여기서 PreToolUse/PostToolUse의 정체가 드러납니다 — 그건 GJC 내부 이벤트 이름이 아닙니다(GJC 내부는 tool_call/tool_result). 그것들은 GJC가 소비하는 Claude Code 호스트 규약이고, GJC가 노출하는 Codex 규약은 UserPromptSubmit/Stop입니다. 비대칭이 핵심: EXPOSE는 Codex의 이벤트 훅을, CONSUME은 Claude의 파일 기반 pre/post 훅을 다룹니다 — 이름만 비슷한 다른 개념입니다. 그리고 지금 이 세션에서 매 도구 호출마다 보이는 PreToolUse:Bash hook… 메시지들이 바로 이 호스트 훅 메커니즘의 실제 동작 예시입니다.
─────────────────────────────────────────────────

표면	이벤트	상태	강제 수준
확장 hook API (pi.on)	25개	공개 빌드 휴면 (라이브 쌍둥이=ExtensionRunner emit)	(설계상) tool_call block
네이티브 스킬 훅	2개 (UserPromptSubmit/Stop)	LIVE	TS 코드 강제
호스트 통합	Codex 2 expose / Claude pre·post consume	LIVE	호스트 프로토콜
3. Agent Skills — 워크플로를 캡슐화한 단계별 프롬프트 + 상태
3.1 스킬의 형식과 발견 경로
스킬은 SKILL.md 파일 하나 + YAML 프론트매터입니다(name, description 등). GJC는 두 종류를 구분합니다:

kind: "skill" — 사용자 노출(슬래시 /skill:<name>, listing 가능). 공개 표면은 정확히 4개.
kind: "skill-fragment" — 부모 스킬에 종속, 사용자 비노출. 등록을 먹이는 getEmbeddedDefaultGjcSkills()가 kind==="skill"만 필터하므로 fragment는 구조적으로 listing에서 누락됩니다(총 4개: deep-interview×3 + ultragoal×1).
발견 경로는 제가 읽은 native-skill-hook.ts:57-91의 config 병합에서 드러납니다 — .gjc/config.yml의 skills.* 플래그(enablePiUser/enablePiProject/enableCodexUser/enableClaudeUser/enableClaudeProject/customDirectories/ignoredSkills/includeSkills)로 사용자/프로젝트/Codex/Claude 디렉터리를 켜고 끕니다. 그리고 무엇을 끄든 4개 번들 기본 스킬은 withEmbeddedDefaultGjcSkills()가 항상 재주입합니다(AI_AGENT_HARNESS_VIEW.md §5).

3.2 skill 도구 — 동일 턴 체이닝 (제가 직접 읽음)
스킬을 어떻게 "실행"하는가? 제가 tools/skill.ts와 prompts/tools/skill.md를 전부 읽었습니다. 메커니즘:

에이전트가 skill({name, args})를 호출
phase 가드: 호출자의 current_phase가 terminal 집합(complete/completed/handoff/failed/cancelled/canceled/inactive)이 아니면 거부(:107-113). 같은 스킬로의 재귀도 거부.
원자적 handoff: runNativeStateCommand(["handoff", "--mode", caller, "--to", callee, ...])를 in-process로 실행해 .gjc/state/에서 caller를 강등·callee를 승격(:120)
콜리의 SKILL.md를 컨텍스트에 주입: buildSkillPromptMessage()로 메시지를 만들고 sendCustomMessage(..., { triggerTurn: false })로 보냅니다(:142-151). 워크플로 검증에 따르면 triggerTurn: false가 핵심 — 새 턴을 트리거하지 않고 현재 에이전트 루프에 user-attribution 메시지로 콜리 SKILL.md를 끼워넣어 같은 턴에 이어 실행합니다.
★ Insight ─────────────────────────────────────

스킬 호출은 subagent를 띄우는 게 아닙니다 — 같은 세션 내 "동일 턴 핸드오프"입니다. 그래서 A → B → C 체인은 A가 skill(B)를 호출하고, B의 다음 턴이 skill(C)를 호출하는 식으로 진행됩니다. 이것이 §1의 멀티 에이전트(별도 자식 세션)와 결정적으로 다른 점입니다: 스킬 = 프롬프트 컨텍스트 교체(같은 두뇌가 새 역할), 서브에이전트 = 별도 두뇌 위임. skill.md의 critical 규칙 — "이미 실행 중인 스킬을 자신에게 상기시키려 호출하지 마라(현재 SKILL.md는 이미 컨텍스트에 있다)" — 이 구분을 정확히 강제합니다.
─────────────────────────────────────────────────

3.3 4개 번들 워크플로 스킬 — 각각이 하는 일
AGENTS.md가 "정확히 4개의 기본 워크플로 스킬"을 공개 표면으로 못박습니다. AI_AGENT_HARNESS_VIEW.md §9의 검증 결과로 정리하면:

스킬	Phase	하는 일	.gjc/ 산출물	코드가 강제하는 것
deep-interview	모호함 해소	가장 약한 차원에 질문 1개씩 → 모호함 점수가 임계치(0.05 기본) 이하로 떨어질 때까지 루프. 끝에 4지 선택(ralplan/ultragoal/team/재인터뷰)	.gjc/specs/deep-interview-{slug}.md (sha256 + JSONL ledger)	비단조 채점 불변식 위반 시 저장 거부(fail-closed), spec 파일 영속화
ralplan	합의·계획	Planner(지속형 resume) → Architect(매 패스 신규) → Critic(매 패스 신규, OKAY/ITERATE/REJECT) 루프, 최대 5회	.gjc/plans/.../pending-approval.md + ADR	content-addressed 멱등 ledger, 승인 게이트(--interactive 없으면 실행 없이 정지). "5회"는 프롬프트 규율이며 코드는 1..999 허용
ultragoal	목표 실행	brief를 @goal 구분자로 분할 → goals.json → 순차·단일 활성 스케줄로 한 골씩 실행 → 11단계 완료 게이트	.gjc/ultragoal/의 brief.md + goals.json + ledger.jsonl	validateCompletionQualityGate가 {architectReview, executorQa, iteration} 구조 + 암호학적 completion receipt 강제. status 손편집은 무효
team	tmux 병렬	워커 3~20개를 tmux로 띄워 공유 task list로 병렬 실행	.gjc/state/team/	단일 writer lease, O_EXCL claim, 37 verb API
routing 규칙(AGENTS.md): "요청을 만족하는 가장 작은 워크플로를 써라." 모호하면 deep-interview, 계획 합의가 필요하면 ralplan, 지속 다중 목표면 ultragoal, 병렬 실행이 필요하면 team.

★ Insight ─────────────────────────────────────

"11단계 완료 게이트"가 GJC 하네스 철학의 정수입니다. SKILL.md 산문은 11단계(표적 검증 → ai-slop-cleaner 청소 → 재검증 → architect 리뷰 → executor 레드팀 → 증거 표면화 → coverage matrix → 최종 코드리뷰 → blocker 기록 → clean까지 루프 → complete 체크포인트)를 지시하지만, runtime의 validateCompletionQualityGate가 강제하는 건 "11단계를 밟았다"가 아니라 구조적으로 유효한 quality gate JSON + 비어있지 않은 iteration.evidence + 암호학적 receipt입니다. receipt는 plan 스냅샷의 sha256("plan generation")을 담아, 이후 goals가 바뀌면 재유도된 generation이 달라져 receipt가 staleness-무효화됩니다. "goals.json의 status를 손으로 고치는 것만으로는 완료가 인정되지 않는다" — 이것이 §2의 Stop 훅과 합쳐져 "모델의 완료 주장을 증거로 게이팅"하는 하네스의 백본입니다.
─────────────────────────────────────────────────

4. 통합 — 이 셋으로 실제 작업이 어떻게 진행되는가
이제 세 축이 하나의 작업 흐름으로 합쳐지는 모습입니다. 워크플로의 통합 서사를 소스 라인과 함께 재구성하면 — "Stripe 결제 처리 기능을 만들어줘" 같은 복합 요청의 end-to-end:


flowchart TD
  U["사용자 프롬프트"] --> H1["① UserPromptSubmit 훅<br/>키워드 탐지 → 스킬 활성화<br/>(우회 프롬프트면 block)"]
  H1 --> SP["② 컨텍스트 조립<br/>system-reminder · 활성 스킬 · 도구셋<br/>(ExtensionRunner: before_agent_start emit)"]
  SP --> M["③ 모델 호출 (스트리밍 턴)"]
  M --> Skill["④ skill 도구<br/>deep-interview→ralplan 동일 턴 체이닝<br/>(.gjc/state handoff 원자적)"]
  Skill --> Task["⑤ task 도구<br/>planner/architect/critic subagent 스폰<br/>(자식 AgentSession, receipt-only)"]
  Task --> H2["⑥ tool_call/tool_result emit<br/>+ 메시지 persist"]
  H2 --> UG["⑦ ultragoal 실행<br/>골 순차 + executor subagent 위임"]
  UG --> Stop["⑧ Stop 훅<br/>active_verified_complete?<br/>아니면 block → 재개"]
  Stop -->|"all complete"| Done["완료 receipt"]
  Stop -->|"미완"| M
단계별로 어느 메커니즘이 발화하는가:

UserPromptSubmit 훅(②번 hook) — 프롬프트가 "interview me" 같은 키워드면 deep-interview를 seed하고 additionalContext 주입. "goal complete" 같은 우회면 block. (native-skill-hook.ts:171-223)

컨텍스트 조립 — #buildSystemPromptForAgentStart()가 메모리 백엔드 훅 + before_agent_start 이벤트(ExtensionRunner emit) + system-reminder 기여자를 모읍니다. (이 세션에서 매 턴 보이는 <system-reminder>들이 정확히 이 메커니즘)

skill 도구(③ Agent Skills) — 모델이 복잡도를 판단해 deep-interview로 요구사항을 결정하고, 끝나면 skill("ralplan")을 동일 턴 체이닝. 핸드오프가 .gjc/state에서 원자적으로 일어남.

task 도구(① 멀티 에이전트) — ralplan이 planner(지속형)→architect(신규)→critic(신규) subagent를 각각 task로 스폰. 각 역할은 bashAllowedPrefixes로 읽기 전용이 강제되고, 전문 리뷰는 영속화 후 receipt만 부모에 반환. Critic 승인 시 pending-approval.md.

ultragoal 실행 — 승인되면 skill("ultragoal") 체이닝. 골을 순차로 실행하며 각 골에서 executor subagent를 위임(필요시 worktree 격리). 11단계 게이트에서 ai-slop-cleaner fragment가 변경 파일만 검사(read-only), executor가 레드팀.

Stop 훅(② hook) — 사용자가 멈추려 하면 buildSkillStopOutput()이 ultragoal에 미완 골이 있는지 검사. 있으면 decision:"block" + stopReason: gjc_ultragoal_verification_<state>로 종료를 막고 에이전트를 재개. 모든 골이 receipt로 증명될 때만 stop 허용.

★ Insight ─────────────────────────────────────

세 축의 분업이 명확합니다: Skills는 무엇을 어떤 순서로 할지(워크플로 절차)를, 멀티 에이전트는 누가 할지(역할별 격리 실행)를, Hooks는 언제 멈춰도 되는지(완료/우회의 런타임 게이팅)를 담당합니다. 그리고 이 셋을 묶는 접착제는 전부 .gjc/ 디스크 상태입니다 — 스킬 핸드오프도, 서브에이전트 receipt도, Stop 훅의 완료 판정도 모두 대화(transcript) 밖의 tamper-evident 상태 파일을 읽고 씁니다. 그래서 세션을 재개해도 transcript 재생 없이 .gjc/state에서 phase·active-skill·goal을 복원할 수 있고, 이것이 GJC가 표방하는 **"검토 가능(auditable)·재개 가능(resumable)·운영 가능(operable)"**의 실제 구현입니다.

5. 정리 — 강의/실무에서 강조할 핵심
멀티 에이전트 = 8개 임베드 역할 에이전트 + task 위임. 권한은 프론트매터(tools/bashAllowedPrefixes)로 선언되고 bash 도구가 코드로 강제. subagent는 lifecycle·구조화된 yield·receipt-only 응답·스폰 게이트(>4)를 가진 "소유된 작업". 진짜 병렬은 team(tmux, 3~20워커).

Hooks = 화려한 24-이벤트 API는 공개 빌드 휴면, 실제 엔진은 단 2개(UserPromptSubmit/Stop)에 durable 상태 검증을 묶은 fail-closed 게이트. Stop 훅이 "loop-until-done"의 실체. PreToolUse/PostToolUse는 GJC 내부가 아니라 호스트(Claude) 규약이고 GJC는 Codex에 노출/Claude를 소비.

Agent Skills = SKILL.md + 프론트매터. skill 도구는 subagent가 아니라 동일 턴 컨텍스트 핸드오프(.gjc/state 원자적 전이). 공개 4개(deep-interview/ralplan/ultragoal/team) + 숨은 fragment 4개. "프롬프트가 절차를 돌리고 런타임이 receipt로 봉인"하는 split이 일관된 패턴.

이미 저장소에 AI_AGENT_HARNESS_VIEW.md라는 소스 검증된 정밀 분석(§3 기준 ~152개 주장 중 ~146 confirmed)이 있으니, 더 깊이 들어갈 땐 멀티 에이전트는 §11~12, Hooks는 §20, Skills/워크플로 게이트는 §9를 정본으로 보시면 됩니다. 제 답변은 그 문서를 제가 직접 읽은 9개 소스 파일(agents.ts, native-skill-hook.ts, skill.ts, spawn-gate.ts 등) + 7개 워크플로 에이전트의 독립 검증으로 교차 확인한 결과입니다.

궁금하신 부분을 더 파고들까요? 예를 들어 — ralplan의 Planner-resume vs Architect-respawn 메커니즘, ultragoal 완료 receipt의 sha256 staleness 무효화, 또는 team 스킬의 37 verb tmux 프로토콜 중 하나를 골라 코드 레벨로 더 깊이 트레이스할 수 있습니다.
