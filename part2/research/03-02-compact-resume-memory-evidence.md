# Session 3-2 강사용 근거 자료

본문 대본: [`part2/03-02-compact-resume-memory.md`](../../part2/03-02-compact-resume-memory.md)
형식 참고: [`part2/research/02-01-what-why-how-evidence.md`](./02-01-what-why-how-evidence.md)
자료 작성일: 2026-04-30 / 검증 기준일: 2026-04-30

이 문서는 강의 진행 시 카메라 앞에서 한두 줄 단정적으로 인용할 수 있는 1차 자료(공식 문서·검증된 사고 사례·공개 연구) 모음이다. **본문 대본을 부풀리지 않기 위해 따로 분리**했고, 본 세션은 도구 기능을 다루므로 *공식 문서가 가장 큰 비중*을 차지한다.

---

## 0. 강의 핵심 명제 (이 자료가 뒷받침하는 단 하나의 주장)

> **"`/compact`, `resume`, `memory`는 *손실 압축*이며 만능 해결책이 아니다. 압축은 정보가 사라지고, resume은 모든 맥락을 되살리지 않으며, memory는 항상 현재 작업에 맞지 않는다. *중요한 결정은 기능에 맡기지 말고 문서에 남긴다.*"**

이 명제에 직접 대응하는 자료는 본문에서 **★** 표시로 강조했다.

---

## 0.1 ⚠️ 버전 변동성 — 강사 필수 주의사항

> **본 세션의 슬래시 명령(`/compact`, `/clear`, `/resume`, `/memory`, `/new`, `/fork`)과 CLI 플래그(`--continue`, `--resume`, `--last`)는 도구 마이너 버전마다 이름·동작이 바뀐다.** 본 자료는 2026-04-30 기준 공식 문서(Claude Code v2.x 이후, Codex CLI 최신 documented 버전)를 인용했지만, 강의 촬영일에 다음 절차로 *반드시* 재확인할 것.

**촬영 당일 5분 점검 루틴**:
1. `claude --version` / `codex --version` 으로 현재 버전 출력
2. `/help` 또는 `claude /help`, `codex /help` 로 슬래시 명령 목록 직접 출력
3. 본 자료의 명령 이름과 비교 — 다르면 슬라이드/대본 모두 갱신
4. 변경된 항목은 *촬영일 자막*으로 표시 (예: "촬영 시점 v2.1.59 기준")
5. Auto memory(`/memory`) 는 **Claude Code v2.1.59 이상**에서만 가능 — 자료 출처 [§2 A2](#a2-claude-code--auto-memory-는-v2159-이상에서만-동작)

**이름이 자주 바뀐 이력**:
- Anthropic prompting docs: `docs.anthropic.com/.../be-clear-direct` → `platform.claude.com/docs/en/.../claude-prompting-best-practices` (통합)
- Claude Code docs: `docs.anthropic.com/en/docs/claude-code` → `code.claude.com/docs/en/...` (이전)
- `/fork` 의미: `CLAUDE_CODE_FORK_SUBAGENT` 환경변수에 따라 *대화 분기*에서 *서브에이전트 분기*로 의미가 달라짐 — 출처 [§2 A4](#a4--fork--branch--resume-그리고-fork_subagent-환경변수)

---

## 1. 진행 순서 ↔ 자료 매칭 매트릭스 (먼저 한 번 보고 들어가는 표)

| 본문 진행 순서 | 1차 자료 (공식 가이드) | 검증된 사례/이슈 | 학술/업계 연구 |
|---|---|---|---|
| 1. 기능별 역할 구분 (compact/resume/memory/문서화) | A1 `/compact` 정의, A3 `/resume`/`/clear`/`/memory` 정의, A6 `codex resume`, A7 `/compact` Codex | — | — |
| 2. 한계 설명 (★ 손실 압축 명제) | ★A1 "tool outputs are gone", ★A2 MEMORY.md 25KB/200줄 cap, ★A5 "instructions from early...may be lost", ★A8 32KiB AGENTS.md cap | ★C1 auto-compact thrashing 공식 인정, C2 instructions seem lost after /compact | D1 conversation summarization 손실 가능성 |
| 3. 사용 시나리오 분기 | A1 `/compact` vs `/clear` 명시 차이, A3 `/clear` "previous conversation stays in /resume", A8 AGENTS.md merge order | — | — |
| 4. 명령 확인 루틴 | A4 `/help`, A9 Codex 전체 슬래시 목록, A10 버전 의존성 (v2.1.59) | — | — |
| 5. 기능 사용 후 검증 | A2 "Claude treats them as context, not enforced configuration", A5 키워드 "may be lost" | C2 nested CLAUDE.md 재주입 안 됨 | D2 IFEval (검증 가능 형태) |

★ = "손실 압축" 명제 직결 자료

---

## 2. 공식 문서 — Anthropic Claude Code & OpenAI Codex CLI

> **본 세션의 핵심**: 손실 압축의 *한계*가 공식 문서에 *명시적으로* 적혀 있다는 것. 즉 "압축에서 정보가 사라진다"는 강의 명제는 추정이 아니라 *제조사가 직접 인정한 사실*이다. 카메라 앞에서 단정적으로 말할 수 있는 근거.

### A1. ★ Claude Code `/compact` — 정확히 무엇이 사라지는가

**출처**: Anthropic Claude Code — Commands reference & Context window
**URL**:
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/context-window

**확인일**: 2026-04-30

**원문 (영어, Commands reference)**:
> "`/compact [instructions]` — Free up context by summarizing the conversation so far. Optionally pass focus instructions for the summary. See [how compaction handles rules, skills, and memory files](/en/context-window#what-survives-compaction)"

**원문 (Context window 페이지, "What survives compaction" 표 직전)**:
> "When a long session compacts, Claude Code summarizes the conversation history to fit the context window. What happens to your instructions depends on how they were loaded"

**원문 (Context window 페이지, 인터랙티브 시뮬레이션 설명에 박혀 있는 결정적 한 줄)**:
> "All conversation events condensed into one structured summary. The summary keeps: your requests and intent, key technical concepts, files examined or modified with important code snippets, errors and how they were fixed, pending tasks, and current work. **It replaces the verbatim conversation: full tool outputs and intermediate reasoning are gone.** Claude can still reference the work but won't have the exact code it read earlier."

**한국어 (카메라 인용용)**:
> "Claude Code 공식 문서가 직접 인정합니다. `/compact` 후에는 *원문 그대로의 대화는 사라집니다.* 도구 출력 전체와 중간 추론은 *없어집니다.* 모델이 작업 내용을 *언급*은 할 수 있어도 *예전에 읽은 정확한 코드*는 남지 않습니다."

**세션 내 사용 위치**: 진행 순서 2번 (한계 설명) — **손실 압축 명제 핵심 인용**
**왜 중요한가**: "압축에서 정보가 사라진다"가 강사의 의견이 아니라 제조사 공식 문구라는 결정적 증거.

---

### A2. ★ Auto memory (`MEMORY.md`)는 200줄 / 25KB 에서 잘린다 — 명시적 한계

**출처**: Anthropic Claude Code — Memory, "How it works"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어)**:
> "**The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start.** Claude keeps `MEMORY.md` concise by moving detailed notes into separate topic files."

> "This limit applies only to `MEMORY.md`. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence."

> "Topic files like `debugging.md` or `patterns.md` are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information."

추가 (같은 페이지, "CLAUDE.md vs auto memory" 표):
> "Both are loaded at the start of every conversation. **Claude treats them as context, not enforced configuration.** The more specific and concise your instructions, the more consistently Claude follows them."

**한국어**:
> "Auto memory(`MEMORY.md`)는 *처음 200줄* 또는 *처음 25KB*, 둘 중 먼저 닿는 쪽에서 잘립니다. 그 너머는 *세션 시작 시 로드되지 않습니다.* 그리고 공식 문서는 명시적으로 — *memory는 강제 설정이 아니라 컨텍스트입니다.* 모델이 따를지 안 따를지는 보장되지 않습니다."

**세션 내 사용 위치**: 진행 순서 2번 — *"memory는 항상 현재 작업에 맞지 않는다"* 명제의 직접 근거
**한계 명시**: v2.1.59 이상에서만 사용 가능 (A10 참고)

---

### A3. Claude Code `/clear` vs `/compact` vs `/resume` — 공식 정의 그대로

**출처**: Anthropic Claude Code — Commands reference
**URL**: https://code.claude.com/docs/en/commands
**확인일**: 2026-04-30

**원문 (영어, 표에서 직접 발췌)**:
> "`/clear` — **Start a new conversation with empty context.** The previous conversation stays available in `/resume`. To free up context while continuing the same conversation, use `/compact` instead. Aliases: `/reset`, `/new`"

> "`/compact [instructions]` — Free up context by summarizing the conversation so far. Optionally pass focus instructions for the summary."

> "`/resume [session]` — Resume a conversation by ID or name, or open the session picker. Alias: `/continue`"

> "`/memory` — Edit `CLAUDE.md` memory files, enable or disable [auto-memory](/en/memory#auto-memory), and view auto-memory entries"

> "`/context` — Visualize current context usage as a colored grid. Shows optimization suggestions for context-heavy tools, memory bloat, and capacity warnings"

**한국어 (시나리오 분기 슬라이드용 — 공식 문구 그대로)**:
> ① `/compact` = 같은 대화를 *이어가면서* 토큰을 비운다 (요약 발생)
> ② `/clear` = *새 대화*를 시작한다. 이전 대화는 `/resume` 으로 다시 열 수 있다
> ③ `/resume` = ID/이름으로 이전 세션 재개. `/continue` 와 동일
> ④ `/memory` = CLAUDE.md 편집과 auto-memory 토글 진입점

**세션 내 사용 위치**: 진행 순서 1번(역할 구분), 3번(시나리오 분기)
**왜 중요한가**: "compact 와 clear 는 다르다"가 강사 해석이 아니라 *공식 문서가 직접 대조해 적은 문구*. 슬라이드에 한 줄씩 그대로 넣을 수 있다.

---

### A4. `/fork` / `/branch` / `--fork-session` — 그리고 `FORK_SUBAGENT` 환경변수의 함정

**출처**: Anthropic Claude Code — Commands reference & How Claude Code works
**URL**:
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/how-claude-code-works
**확인일**: 2026-04-30

**원문 (영어)**:
> "`/branch [name]` — Create a branch of the current conversation at this point. Switches you into the branch and preserves the original, which you can return to with `/resume`. Alias: `/fork`. **When `CLAUDE_CODE_FORK_SUBAGENT` is set, `/fork` instead spawns a forked subagent and is no longer an alias for this command**"

> "`claude --continue --fork-session` ... This creates a new session ID while preserving the conversation history up to that point. The original session remains unchanged."

**한국어**:
> "`/fork` 의 의미는 환경변수에 따라 달라집니다. 기본은 *대화 자체의 분기*지만, `CLAUDE_CODE_FORK_SUBAGENT` 가 설정돼 있으면 *서브에이전트 분기*로 바뀝니다. **같은 명령이 환경에 따라 다른 일을 하므로 *촬영 환경의 환경변수를 반드시 확인*해야 합니다.**"

**세션 내 사용 위치**: 진행 순서 4번 — "현재 버전에서 없거나 다른 이름이면 표시" 정당화
**한계 명시**: 강의 환경에서 `CLAUDE_CODE_FORK_SUBAGENT` 가 설정돼 있는지 사전 확인 필요

---

### A5. ★ Claude Code "instructions from early in the conversation may be lost" — 공식 인정

**출처**: Anthropic Claude Code — How Claude Code works, "When context fills up"
**URL**: https://code.claude.com/docs/en/how-claude-code-works
**확인일**: 2026-04-30

**원문 (영어)**:
> "Claude's context window holds your conversation history, file contents, command outputs, [CLAUDE.md], [auto memory], loaded skills, and system instructions. **As you work, context fills up. Claude compacts automatically, but instructions from early in the conversation can get lost.** Put persistent rules in CLAUDE.md, and run `/context` to see what's using space."

> "Claude Code manages context automatically as you approach the limit. It clears older tool outputs first, then summarizes the conversation if needed. Your requests and key code snippets are preserved; **detailed instructions from early in the conversation may be lost.** Put persistent rules in CLAUDE.md rather than relying on conversation history."

> "To control what's preserved during compaction, add a 'Compact Instructions' section to CLAUDE.md or run `/compact` with a focus (like `/compact focus on the API changes`)."

**한국어 (강의 명제 직결, 카메라 인용용)**:
> "공식 문서가 *그대로* 인정합니다. — 압축이 자동으로 일어나면 *대화 초반의 자세한 지시는 사라질 수 있다.* 그래서 공식 문서는 *영구적으로 지켜야 할 규칙은 대화 기록이 아니라 CLAUDE.md에 두라*고 말합니다. 우리 강의의 *'중요한 결정은 문서에 남긴다'* 가 바로 이겁니다."

**세션 내 사용 위치**: 진행 순서 2번(한계), 진행 순서 5번(검증) — **강의 명제 가장 직접 근거**
**왜 중요한가**: "compact 후 결정이 사라질 수 있으니 문서에 남기라"는 강의의 핵심 권고가 *Anthropic 공식 권고와 글자 그대로 동일*하다.

---

### A6. ★ Claude Code "What survives compaction" 표 — 무엇이 살아남고 무엇이 안 살아남는가

**출처**: Anthropic Claude Code — Context window
**URL**: https://code.claude.com/docs/en/context-window
**확인일**: 2026-04-30

**원문 (영어, 표 그대로)**:

| Mechanism | After compaction |
| --- | --- |
| System prompt and output style | Unchanged; not part of message history |
| Project-root CLAUDE.md and unscoped rules | Re-injected from disk |
| Path-scoped rules and nested CLAUDE.md | Summarized away with conversation; reload on next matching file read |
| Skill descriptions (listing) | **Not re-injected after `/compact`. Only skills you actually invoked get preserved.** |
| Skill bodies (invoked) | Re-injected, but truncated to per-skill cap; oldest dropped if total budget exceeded |

> "Path-scoped rules and nested CLAUDE.md files load into message history when their trigger file is read, so compaction summarizes them away with everything else. They reload the next time Claude reads a matching file. **If a rule must persist across compaction, drop the `paths:` frontmatter or move it to the project-root CLAUDE.md.**"

> "Skill bodies are re-injected after compaction, but large skills are truncated to fit the per-skill cap, and the oldest invoked skills are dropped once the total budget is exceeded. Truncation keeps the start of the file, so put the most important instructions near the top of `SKILL.md`."

추가 (memory 페이지의 호환 문구):
> "Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories are not re-injected automatically; they reload the next time Claude reads a file in that subdirectory."

**한국어 (슬라이드용 직접 대응표)**:
> 살아남음: 시스템 프롬프트, **프로젝트 루트 CLAUDE.md**, 출력 스타일
> 사라짐: 경로 한정 규칙, **하위 디렉터리의 CLAUDE.md**, 호출되지 않은 스킬 설명, 호출됐어도 큰 스킬의 후반부

**세션 내 사용 위치**: 진행 순서 1번/2번/3번 — *"무엇을 어디에 둬야 살아남는가"*의 직접 답
**왜 중요한가**: "memory 폴더만 만들면 끝"이 아니라 *어느 위치의 CLAUDE.md가 compaction을 견디는지가 정해져 있다*. 강의 후반부 "팀 전체가 공유해야 하는 규칙은 저장소 문서"의 정당화.

---

### A7. OpenAI Codex CLI `/compact` — 동일 결론, 다른 진영

**출처**: OpenAI Codex CLI — Slash commands reference
**URL**: https://developers.openai.com/codex/cli/slash-commands
**확인일**: 2026-04-30

**원문 (영어, 표 발췌)**:
> "`/compact` — Summarize the visible conversation to free tokens"
>
> "`/clear` — Clear the terminal and start a fresh chat"
>
> "`/new` — Start a fresh conversation in the same CLI session"
>
> "`/resume` — Continue work from a previous CLI session without starting over"
>
> "`/fork` — Branch the active session to explore a new approach without losing the current transcript"
>
> "`/init` — Generate an AGENTS.md scaffold in the current directory"
>
> "`/status` — Display session configuration and token usage"

**한국어**:
> "Codex CLI도 같은 결론입니다. `/compact` 는 *visible conversation을 요약*해서 토큰을 회수합니다 — 즉 같은 *손실 압축*입니다. `/new` 와 `/clear` 는 *fresh chat*, `/resume` 은 *previous session 재개*. 이름과 의미가 Claude Code와 거의 같지만 *완전히 같지는 않습니다* (특히 `/clear` 는 Codex에서 '터미널 화면 정리'에 더 가깝습니다)."

**세션 내 사용 위치**: 진행 순서 1번/3번 — Anthropic만 인용한다는 인상 회피
**한계 명시**: Codex `/clear` 동작은 "wipe the terminal" 표현이라 Claude Code `/clear`(=새 대화)와 *의미가 정확히 같지 않을 수 있다*. 강의에서 동일시 금지.

---

### A8. ★ Codex `AGENTS.md` 32KiB 상한 — memory도 *반드시* 한도가 있다

**출처**: OpenAI Codex — AGENTS.md guide
**URL**: https://developers.openai.com/codex/guides/agents-md
**확인일**: 2026-04-30

**원문 (영어, 발췌·요약 인용)**:
> "Codex reads `AGENTS.md` files before doing any work."
>
> Discovery 순서: ① `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md` (global) ② Git root에서 현재 디렉터리까지 walk (project) ③ root에서 아래로 concat, 가까운 파일이 먼저 것을 override.
>
> "**Stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default).**"
>
> "Empty files are skipped"
>
> "**Codex rebuilds the instruction chain on each run—no persistent caching.**"

**한국어**:
> "Codex `AGENTS.md` 도 *합산 32KiB* 가 기본 상한입니다. 그 한도를 넘기면 *추가 파일은 더 이상 읽히지 않습니다.* 그리고 매 실행마다 처음부터 다시 만들기 때문에 — *memory는 안전하게 누적된다는 가정 자체가 틀렸습니다.*"

**세션 내 사용 위치**: 진행 순서 2번 — "memory는 항상 현재 작업에 맞지 않는다" 와 "한도가 있다" 동시 입증
**왜 중요한가**: Claude Code(MEMORY.md 25KB/200줄, A2)와 Codex(AGENTS.md 32KiB) **양쪽 다 명시적 상한이 있다**. memory를 무한 누적 가능한 시스템처럼 다루면 안 된다는 결정적 근거.

---

### A9. Codex CLI `codex resume` / `--last` / `codex fork` — 공식 동작 정의

**출처**: OpenAI Codex CLI — Reference & Features
**URL**:
- https://developers.openai.com/codex/cli/reference
- https://developers.openai.com/codex/cli/features
**확인일**: 2026-04-30

**원문 (영어)**:
> "`codex resume` — Continue a previous interactive session by ID or resume the most recent conversation."
>
> "`--last` — Skip the picker and resume the most recent conversation from the current working directory"
>
> "`--all` — Include sessions outside the current working directory when selecting the most recent session"
>
> "`codex fork` — Fork a previous interactive session into a new thread, preserving the original transcript."
>
> Features 페이지: "Resumed runs **keep the original transcript, plan history, and approvals,** so Codex can use prior context."

**한국어 (강의에 그대로 인용 가능)**:
> "Codex 의 `resume` 은 *transcript, plan history, approvals* 를 그대로 살립니다. 즉 *대화 기록은 살아오지만*, 그 시점의 ephemeral 한 모델 상태(예: 이전 모델이 들고 있던 비공개 추론)는 다시 만들어지지 않습니다."

**세션 내 사용 위치**: 진행 순서 1번(resume 역할), 3번("어제 작업 다시 열 때") — Claude Code `/resume`과 의미가 비슷하지만 *완전히 같지 않음*을 함께 명시.

---

### A10. Auto memory 는 v2.1.59 이상에서만 동작 — 버전 의존성 직접 인용

**출처**: Anthropic Claude Code — Memory, "Auto memory" 섹션
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어, Note 박스 그대로)**:
> "Auto memory requires Claude Code v2.1.59 or later. Check your version with `claude --version`."

> "Auto memory is on by default. To toggle it, open `/memory` in a session and use the auto memory toggle, or set `autoMemoryEnabled` in your project settings"

> "To disable auto memory via environment variable, set `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`."

**한국어**:
> "공식 문서가 직접 못 박습니다 — auto memory 는 *v2.1.59 이상*에서만 동작합니다. 그 미만 버전을 쓰는 수강생에게는 슬래시 `/memory` 가 다른 동작이거나 없을 수 있습니다."

**세션 내 사용 위치**: 진행 순서 4번 — "공식 문서 확인 / `/help` 확인" 정당화
**왜 중요한가**: 같은 강의를 다른 시점에 보는 수강생에게 "내 버전에선 안 보여요"가 발생할 수 있다는 점을 *공식 문서가 직접 인정*. Section 0.1 의 "5분 점검 루틴" 정당화.

---

## 3. 검증된 사례 / 공식 인정된 실패 모드 (C1~C2)

> 본 세션은 *기능*에 관한 것이라 사외 사고 사례보다 *공식 문서가 인정한 실패 모드*가 더 직접적이다. 트위터 일화는 의도적으로 제외했고, 모두 Anthropic 공식 troubleshooting 페이지에서 검증한다.

### C1. ★ Auto-compact thrashing — Anthropic 공식 troubleshooting

**출처**: Anthropic Claude Code — Troubleshooting, "Auto-compaction stops with a thrashing error"
**URL**: https://code.claude.com/docs/en/troubleshooting
**확인일**: 2026-04-30

**원문 (영어, 그대로)**:
> "If you see `Autocompact is thrashing: the context refilled to the limit...`, automatic compaction succeeded but a file or tool output immediately refilled the context window several times in a row. **Claude Code stops retrying to avoid wasting API calls on a loop that isn't making progress.**"
>
> 권장 복구:
> 1. "Ask Claude to read the oversized file in smaller chunks, such as a specific line range or function, instead of the whole file"
> 2. "Run `/compact` with a focus that drops the large output, for example `/compact keep only the plan and the diff`"
> 3. "Move the large-file work to a [subagent] so it runs in a separate context window"
> 4. "Run `/clear` if the earlier conversation is no longer needed"

**한 줄 요약 (강사 인용용)**:
> "공식 troubleshooting 문서에 *Autocompact is thrashing* 이라는 별도 항목이 있습니다. 즉 — *자동 compact 가 실패하는 모드가 존재하고, Anthropic이 직접 인정합니다.* compact 가 만능이라는 가정이 깨지는 직접 증거입니다."

**세션 내 사용 위치**: 진행 순서 2번 — *"compact가 항상 잘 되는 게 아니다"*의 결정적 증거
**왜 중요한가**: 손실 압축 명제의 가장 강한 형태 — *압축이 정보 손실을 넘어 아예 실패할 수도 있다*는 공식 인정.

---

### C2. ★ "Instructions seem lost after `/compact`" — Anthropic memory 페이지가 직접 다루는 FAQ

**출처**: Anthropic Claude Code — Memory, "Troubleshoot memory issues"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어, FAQ 항목 그대로)**:
> "**Instructions seem lost after `/compact`**
>
> Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. **Nested CLAUDE.md files in subdirectories are not re-injected automatically;** they reload the next time Claude reads a file in that subdirectory.
>
> **If an instruction disappeared after compaction, it was either given only in conversation or lives in a nested CLAUDE.md that hasn't reloaded yet.** Add conversation-only instructions to CLAUDE.md to make them persist."

추가 ("Claude isn't following my CLAUDE.md" 항목):
> "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. **Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions.**"

**한국어 (카메라 인용용)**:
> "Anthropic이 직접 *FAQ로* 다룹니다. — *compact 후 지시가 사라진 것 같다면, 그건 대화에만 있었거나 하위 디렉터리 CLAUDE.md에 있었다는 뜻이다. 영구히 남기려면 CLAUDE.md에 적어라.* 그리고 같은 페이지가 한 번 더 못 박습니다 — *Claude가 CLAUDE.md를 읽고 따르려 하지만, 엄격한 준수는 보장되지 않는다.*"

**세션 내 사용 위치**: 진행 순서 2번(한계), 5번(검증) — **강의 명제와 글자 그대로 일치**
**왜 중요한가**: 본 세션의 단 한 줄 명제 — *"중요한 결정은 기능에 맡기지 말고 문서에 남긴다"* — 가 *Anthropic 공식 FAQ가 권고하는 그대로의 문장*임이 증명된다.

---

## 4. 학술/업계 연구 (D1~D2) — 부족한 영역, 정직한 표시

> **솔직한 한계**: "compact 후 결정 누락"을 직접 측정한 *peer-reviewed 학술 논문*은 본 리서치 시점에 확정 인용 가능한 것을 찾지 못했다. 가장 가까운 영역은 (i) 대화 요약(conversation summarization)의 정보 손실, (ii) instruction-following 평가 — 모두 인접 영역이며, *코딩 에이전트 compact 시나리오로 일반화하면 안 된다.* 강의에서는 *경향성*만 인용하고 수치 인용은 금지한다. 본 세션은 학술 인용보다 *공식 문서 인용*이 훨씬 강한 무기다.

### D1. 대화 요약(conversation summarization)의 정보 손실 — 일반 결론

**상태**: ⚠️ 학술 영역 인용 부족 — 정직하게 약화 인용

**출처 후보 (확정 인용 가능한 1차 자료 미확정)**:
- LLM 대화 요약(dialogue summarization) 분야 일반 결론 — 다수 survey 논문에서 다뤄지지만, "에이전트 세션의 결정 보존" 시점으로 직접 매핑한 peer-reviewed 자료는 본 리서치에서 확정하지 못함.
- Claude Code 자체 문서 [§2 A1 / A5 / A6] 가 *공식 문구로 동일 결론*을 명시하므로, 학술 인용 없이도 강의 명제는 충분히 지지된다.

**대안 인용 방식 (강사 권장)**:
> "대화 요약 분야의 일반적 경향은 *길이가 길어질수록 세부 사실이 누락된다*는 것입니다. 다만 이 결론을 *코딩 에이전트의 compact 시나리오*에 그대로 옮기는 peer-reviewed 연구는 아직 정착되지 않았습니다. 그래서 우리는 *공식 문서가 인정한 한계*만 단정적으로 인용하고, 학술 일반화는 *경향성으로만* 사용하겠습니다."

**세션 내 사용 위치**: 진행 순서 2번 — 보조 (주력은 [§2 A1 / A5 / A6 / C2])
**한계 명시 의무**: 수치 인용 금지. 정성 결론만.

---

### D2. IFEval — "검증 가능한 형태"가 아니면 측정 자체가 불가능

**저자/발표**: Jeffrey Zhou et al. (Google), arXiv:2311.07911, 2023-11
**URL**: https://arxiv.org/abs/2311.07911
**확인일**: 2026-04-30

**한 줄 핵심**:
> "지시문이 *기계 검증 가능한 형태*일 때만 모델이 따랐는지 객관적으로 측정할 수 있다."

**연구 요약**: Google 연구진이 25종 verifiable 제약(예: "단어 수 N 이상", "특정 키워드 K번 포함")으로 약 500개 프롬프트 벤치마크를 만들었다. 핵심 통찰 — *사람 평가는 느리고 LLM-as-judge 는 편향된다 → 따라서 지시문 자체를 기계가 검증할 수 있는 형태로 써야 한다.*

**본 세션과의 연결**: 진행 순서 5번의 "AI에게 현재 목표와 남은 작업을 *요약*하게 하고, 핸드오프 노트와 *비교*한다"는 검증 루프가 — 정확히 IFEval 의 *verifiable instruction following* 패러다임이다. 즉 compact/resume/memory 후 결과를 *비교 가능한 형태로 적어둔* 사용자만 검증할 수 있다.

**카메라 인용용**:
> "Google IFEval(2023) 의 결론은 *지시문을 기계가 검증 가능한 형태로 적어야 모델이 따랐는지 측정할 수 있다*는 것입니다. 우리가 핸드오프 문서에 *목표·완료·남은 작업·결정·검증 명령*을 항목으로 분리해 적는 이유가 같습니다 — 그래야 compact/resume 후 *무엇이 빠졌는지 비교*할 수 있습니다."

**세션 내 사용 위치**: 진행 순서 5번(검증 루프 정당화)
**한계 명시**: 25종 일반 제약 벤치마크. 코딩 에이전트 직접 평가 아님 — *경향성*만 인용.

---

## 5. ★ "손실 압축" 명제 직결 모음

> 강의가 다른 *프롬프트 가이드* 강의와 다른 차별점이 이 명제다. 카메라 앞에서 단정적으로 말할 때 인용하면 좋은 자료를 한 곳에 모았다.

| 자료 | 한 줄 요지 |
|---|---|
| **A1** Claude Code Context window | *"It replaces the verbatim conversation: full tool outputs and intermediate reasoning are gone"* — 공식 문서가 *gone* 이라는 단어 사용 |
| **A2** Claude Code Memory | MEMORY.md는 *200줄 또는 25KB* 에서 잘림 — memory는 무한 누적 X |
| **A5** Claude Code "How it works" | *"detailed instructions from early in the conversation may be lost"* — 공식 인정 |
| **A6** Claude Code "What survives compaction" | 시스템/루트 CLAUDE.md만 살아남음, **하위 CLAUDE.md / 호출 안 한 스킬은 사라짐** |
| **A8** Codex AGENTS.md | *"32 KiB by default" + "no persistent caching"* — Codex 도 동일하게 한도 존재 |
| **C1** Auto-compact thrashing | 공식 troubleshooting에 *전용 항목* — compact 자체가 *실패할 수 있다*고 인정 |
| **C2** "Instructions seem lost after /compact" | 공식 FAQ가 직접 *"Add conversation-only instructions to CLAUDE.md to make them persist"* 권고 → 강의 명제와 글자 일치 |

**강사 권장 인용 시퀀스 (한 호흡 30초)**:
> "compact 가 만능이라고 생각하기 쉽지만, Anthropic 공식 문서는 분명히 적습니다 — *원문 그대로의 대화는 사라지고, 도구 출력과 중간 추론은 없어진다.* 그리고 *대화 초반의 자세한 지시는 사라질 수 있다.* 그래서 같은 문서가 *영구히 지켜야 할 규칙은 대화 기록이 아니라 CLAUDE.md에 두라*고 권고합니다. memory도 마찬가지입니다 — MEMORY.md는 200줄, AGENTS.md는 32KiB 가 한도입니다. 그래서 우리는 *compact, resume, memory를 만능이 아니라 보조 도구*로 쓰고, *중요한 결정은 문서에 남깁니다.* 이게 이번 세션 한 줄 결론입니다."

---

## 6. 인용 시 유의사항 / 한계

1. **버전 의존성이 매우 크다**: 본 자료의 슬래시 명령과 CLI 플래그는 Claude Code 와 Codex CLI 의 *마이너 버전*마다 바뀐다. *촬영 당일* 반드시 §0.1 의 5분 점검 루틴을 돌리고 변경된 항목은 자막으로 표시할 것. 특히 `/fork` 의 의미가 환경변수에 따라 달라진다([§2 A4](#a4--fork--branch--resume-그리고-fork_subagent-환경변수)).

2. **"Auto memory"는 Claude Code 전용·신기능**: v2.1.59 이상에서만 동작하며([§2 A10](#a10-auto-memory-는-v2159-이상에서만-동작--버전-의존성-직접-인용)), 모든 수강생에게 보이지 않을 수 있다. Codex 에는 동일 기능이 없고 `AGENTS.md`로 대체된다.

3. **`/clear` 의미는 두 도구가 다름**: Claude Code 에서 `/clear` 는 *새 대화 시작*([§2 A3](#a3-claude-code-clear-vs-compact-vs-resume--공식-정의-그대로))이고, Codex 에서 `/clear` 는 *터미널 화면 정리*([§2 A7](#a7-openai-codex-cli-compact--동일-결론-다른-진영))에 더 가깝다. 강의에서 동일시 금지.

4. **학술 자료가 부족하다 (정직한 표시)**: "compact 후 결정 누락" 을 직접 측정한 peer-reviewed 자료는 본 리서치 시점에 확정 인용할 만한 것을 찾지 못했다([§4 D1](#d1-대화-요약conversation-summarization의-정보-손실--일반-결론)). 강의 명제는 *공식 문서가 직접 인정한 손실 한계*([§2 A1, A5, A6, C1, C2])로 충분히 지지되므로, 학술 인용은 보조에 머문다.

5. **트위터 출처 의도적 제외**: 본 세션은 *기능의 한계*를 다루므로 일화적 트윗보다 *제조사 공식 troubleshooting/FAQ*가 훨씬 강력하다. 모든 사례는 [code.claude.com](https://code.claude.com), [developers.openai.com/codex](https://developers.openai.com/codex)에서 검증된다.

6. **수치 인용 금지**: MEMORY.md *200줄 / 25KB*, AGENTS.md *32 KiB* 같은 *공식 문서가 직접 적은 수치*는 인용 가능. 그러나 *학술 연구의 % 수치*는 모델 시점 의존성이 커서 정성 결론으로만 인용([§4 D2](#d2-ifeval--검증-가능한-형태가-아니면-측정-자체가-불가능)).

7. **번역 시 의미 보존**: 본 문서의 한국어 번역은 강사 인용 편의용. 원문이 모호한 부분은 모호하게 번역했다. 의역하고 싶을 때는 영어 원문을 다시 확인.

---

## 7. 출처 일람 (URL 한 곳에 모음)

### Anthropic Claude Code 공식 문서
- Memory (CLAUDE.md & auto memory): https://code.claude.com/docs/en/memory
- Commands reference: https://code.claude.com/docs/en/commands
- Context window ("What survives compaction"): https://code.claude.com/docs/en/context-window
- How Claude Code works: https://code.claude.com/docs/en/how-claude-code-works
- Troubleshooting (auto-compact thrashing): https://code.claude.com/docs/en/troubleshooting
- Skills (compact 와의 상호작용): https://code.claude.com/docs/en/skills

### OpenAI Codex CLI 공식 문서
- Slash commands reference: https://developers.openai.com/codex/cli/slash-commands
- AGENTS.md guide (32KiB 상한): https://developers.openai.com/codex/guides/agents-md
- CLI reference (resume / --last / fork): https://developers.openai.com/codex/cli/reference
- Features (resume 동작): https://developers.openai.com/codex/cli/features

### 학술 연구
- IFEval (arXiv:2311.07911): https://arxiv.org/abs/2311.07911

### 본문 대본 / 형식 참고
- 본문 대본: [`part2/03-02-compact-resume-memory.md`](../../part2/03-02-compact-resume-memory.md)
- 형식 참고: [`part2/research/02-01-what-why-how-evidence.md`](./02-01-what-why-how-evidence.md)
