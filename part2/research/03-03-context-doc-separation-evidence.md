# Session 3-3 강사용 근거 자료

본문 대본: [`part2/03-03-context-doc-separation.md`](../../part2/03-03-context-doc-separation.md)
원본 기획서: [`docs/part2-session-plan.md`](../part2-session-plan.md)
자료 작성일: 2026-04-30 / 검증 기준일: 2026-04-30

이 문서는 **Part 2 종합 마무리 세션**(3-3)의 카메라 인용용 1차 자료 모음이다. 본 세션은 2-1(WHAT/WHY/HOW), 2-2(CLAUDE.md), 2-3(AGENTS.md), 3-1(공식 문서), 3-2(좋은 질문)을 한 프레임으로 묶기 때문에, 자료 선정도 *4계층 분리*라는 통합 명제에 직접 매칭되도록 정렬했다.

---

## 0. 강의 핵심 명제 (이 자료가 뒷받침하는 단 하나의 주장)

> **"긴 프롬프트를 더 길게 만들지 말고, 정보의 *성격*에 맞춰 4개 층(즉시 프롬프트 / 세션 핸드오프 / 프로젝트 문서 / 외부 공식 문서)으로 분리한다. 이 분리가 컨텍스트 관리이며, 컨텍스트 엔지니어링의 본질이다."**

이 명제에 직접 대응하는 자료는 본문에서 **★** 표시로 강조했다.

---

## 1. 진행 순서 ↔ 자료 매칭 매트릭스 (먼저 한 번 보고 들어가는 표)

| 본문 진행 순서 | 공식 가이드 | 검증된 사례 / 업계 발표 | 학술/업계 연구 |
|---|---|---|---|
| 1. 4개 층으로 나눈다 | ★A1 Anthropic Context Engineering, A2 Context Window 가이드 | ★B1 Cognition "Don't Build Multi-Agents" | ★D1 Lost-in-the-Middle |
| 2. 정보 위치 판단 | ★A3 CLAUDE.md memory 가이드, A6 Best Practices(쓸 것/뺄 것 표), A7 Skills 온디맨드 로딩 | — | D2 RAG 원논문(파라메트릭 vs 비파라메트릭) |
| 3. 긴 프롬프트 분해 | A4 Prompting best practices(XML 분리), A2 Context Window | B1 Cognition 멀티에이전트 실패 사례 | D3 RAG Survey(Naive/Advanced/Modular) |
| 4. 최종 작업 루프 | ★A5 Effective Harnesses for Long-Running Agents, A3 CLAUDE.md(`/compact` 후 재주입) | — | D1 Lost-in-the-Middle |
| 5. Part 2 종합 실습 | ★A8 AGENTS.md 표준, A6 Best Practices(verify your work), A3 memory 4신호 | — | — |

★ = "4계층 분리 = 컨텍스트 엔지니어링" 명제 직결 자료

---

## 2. 공식 가이드 (A1~A8)

### A1. ★ Anthropic — Effective Context Engineering for AI Agents (4계층 분리의 *공식 정의*)

**출처**: Anthropic Engineering Blog
**URL**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**확인일**: 2026-04-30

**원문 (영어)**:
> "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."
>
> "Context engineering represents the natural progression of prompt engineering... managing the entire context state across multi-turn agent interactions rather than optimizing single prompts."
>
> "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases." (이 현상을 Anthropic이 *context rot* 이라고 명명)
>
> 컨텍스트 구성 요소(원문 그대로):
> - **System prompts** — "the Goldilocks zone between two common failure modes" (지나치게 구체적이거나 지나치게 모호한 두 실패 사이의 골디락스 영역)
> - **Tools** — "self-contained, robust to error, and extremely clear with respect to their intended use"
> - **Examples** — "examples are the 'pictures' worth a thousand words"
> - **Retrieval / just-in-time** — "dynamically load data via tools rather than pre-processing all context"
>
> 총 원칙: "find the *smallest possible* set of high-signal tokens that maximize the likelihood of some desired outcome"

**한국어 (카메라 인용용)**:
> "Anthropic이 직접 정의합니다 — *컨텍스트 엔지니어링*은 토큰을 더 많이 욱여넣는 일이 아니라, *원하는 결과를 만들 가장 작은 고신호 토큰 집합을 큐레이션하는 일*입니다. 그래서 시스템 프롬프트, 도구, 예시, 검색은 같은 통에 섞이지 않고 *각자 다른 위치*에 놓여야 합니다."

**세션 내 사용 위치**: 진행 순서 1번 — 4계층 모델의 *공식 정의 인용*. 강의 차별 명제(*'더 길게 쓰지 말고 분리하라'*)의 1차 출처.
**왜 중요한가**: Part 2 마무리 세션에서 "4계층 분리"라는 강의 고유 프레임이 Anthropic의 공식 입장과 *동일 결론*임을 보여주는 단 하나의 자료.

---

### A2. Anthropic — Context Windows ("context rot"의 공식 진단)

**출처**: Anthropic Platform Docs — Context windows
**URL**: https://platform.claude.com/docs/en/docs/build-with-claude/context-windows
**확인일**: 2026-04-30

**원문 (영어)**:
> "A larger context window allows the model to handle more complex and lengthy prompts, but more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*. This makes curating what's in context just as important as how much space is available."
>
> "Claude achieves state-of-the-art results on long-context retrieval benchmarks like MRCR and GraphWalks, but these gains depend on what's in context, not just how much fits."

**한국어**:
> "Anthropic 공식 문서가 인정합니다 — *컨텍스트 창이 크다고 무조건 좋지 않다.* 토큰이 늘수록 정확도와 회상률이 떨어지는 *context rot* 현상이 있고, 이 때문에 *얼마나 들어가느냐*보다 *무엇을 넣느냐*가 더 중요합니다."

**세션 내 사용 위치**: 진행 순서 1번(왜 4층으로 나누는가), 3번(긴 프롬프트를 분해해야 하는 *공식적* 이유)
**왜 중요한가**: 강의의 "긴 프롬프트를 더 길게 만들지 말라"가 단순 의견이 아닌 *공식 문서가 명명한 현상(context rot)* 임을 입증.

---

### A3. ★ Anthropic — How Claude Remembers Your Project (CLAUDE.md = 프로젝트 문서 계층의 1차 정의)

**출처**: Anthropic Claude Code Docs — Memory
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어)**:
> "Each Claude Code session begins with a fresh context window. Two mechanisms carry knowledge across sessions: CLAUDE.md files (instructions you write to give Claude persistent context) and Auto memory (notes Claude writes itself...)."
>
> CLAUDE.md 작성 4신호:
> - "Claude makes the same mistake a second time"
> - "A code review catches something Claude should have known about this codebase"
> - "You type the same correction or clarification into chat that you typed last session"
> - "A new teammate would need the same context to be productive"
>
> 4계층 위치:
> | Scope | Location | Purpose |
> | Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` 등 | Organization-wide instructions |
> | Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions |
> | User | `~/.claude/CLAUDE.md` | Personal preferences |
> | Local | `./CLAUDE.local.md` | Per-machine, gitignored |
>
> 컴팩션 대응:
> > "Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session."
>
> 세션 모델:
> > "Each Claude Code session begins with a fresh context window."

**한국어**:
> "Claude Code 세션은 *매번 빈 컨텍스트로 시작*합니다. 그래서 세션을 가로질러 살아남아야 하는 정보는 대화에 남기는 게 아니라 CLAUDE.md에 적어야 합니다. — *지난 세션에 했던 똑같은 정정을 또 입력하고 있다면*, 그 줄은 대화가 아니라 CLAUDE.md로 옮겨야 한다는 신호입니다."

**세션 내 사용 위치**: 진행 순서 2번(정보 위치 판단), 4번(다음 세션을 어떻게 시작하는가), 5번(작업 전 규칙 문서를 읽게 한다)
**왜 중요한가**: 강의의 "프로젝트 문서 계층"이 *왜 대화와 분리되어야 하는지*를 공식 문서가 직접 답한다 — 세션은 매번 새로 시작되기 때문.

---

### A4. Anthropic — Prompting Best Practices: XML 태그 분리 (즉시 프롬프트 내부의 미시 분리)

**출처**: Anthropic Platform Docs — Claude prompting best practices
**URL**: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices
**확인일**: 2026-04-30

**원문 (영어)**:
> "XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs. Wrapping each type of content in its own tag (e.g. `<instructions>`, `<context>`, `<input>`) reduces misinterpretation."

**한국어**:
> "한 프롬프트 안에 *지시·맥락·예시·입력값*이 섞이면, 각각을 자기 태그로 감싸세요. 4계층 분리가 세션 단위 분리라면, XML 태그 분리는 한 메시지 안의 분리입니다 — *원리는 같습니다.*"

**세션 내 사용 위치**: 진행 순서 3번 — 긴 프롬프트를 *지금 요청 / 프로젝트 규칙 / 배경 / 외부 링크 / 환경*으로 분해할 때의 *형식적* 정당화.
**왜 중요한가**: 4계층 분리 명제를 한 메시지 단위로 압축한 공식 가이드. 본문 진행 순서 3번이 단순한 정리정돈이 아니라 *Anthropic이 권장하는 형식*임을 보여준다.

---

### A5. ★ Anthropic — Effective Harnesses for Long-Running Agents (세션 핸드오프 계층의 1차 정의)

**출처**: Anthropic Engineering Blog
**URL**: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**확인일**: 2026-04-30

**원문 (영어)**:
> "each new session begins with no memory of what came before"
>
> "a coding agent that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session"
>
> "a `claude-progress.txt` file that keeps a log of what agents have done"
>
> "The key insight here was finding a way for agents to quickly understand the state of work when starting with a fresh context window, which is accomplished with the `claude-progress.txt` file alongside the git history."

또한 Context windows 페이지가 같은 글을 가리키며 다음 추천을 함:
> "For agents that span multiple sessions, design your state artifacts so that context recovery is fast when a new session starts."

**한국어 (카메라 인용용)**:
> "Anthropic 엔지니어링 블로그가 직접 권합니다 — 다중 세션 에이전트는 *상태 산출물(state artifacts)을 설계*해서 새 세션이 시작될 때 빠르게 컨텍스트를 복구하게 만들어야 합니다. *대화에 의지하지 마세요. 다음 세션은 빈 채로 시작합니다.*"

**세션 내 사용 위치**: 진행 순서 1번(세션 핸드오프 계층의 정의), 4번(긴 세션은 핸드오프 노트로 끝낸다), 5번(작업 후 핸드오프 노트를 남긴다)
**왜 중요한가**: 강의 4계층 중 *세션 핸드오프*는 강의 고유 용어처럼 보일 수 있지만, Anthropic이 동일 개념(state artifacts, claude-progress.txt)을 *공식 권장 패턴*으로 발표한 1차 자료. 진행 순서 5번의 "검증 결과와 핸드오프 노트를 남긴다"의 직접적 출처.

---

### A6. Anthropic — Claude Code Best Practices ("CLAUDE.md에 *넣을 것 / 빼야 할 것* 표")

**출처**: Anthropic Claude Code Docs — Best Practices
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30

**원문 (영어)**:
> "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."
>
> "CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, use skills instead. Claude loads them on demand without bloating every conversation."
>
> "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
>
> 포함/배제 표(원문 그대로):
> | ✅ Include | ❌ Exclude |
> |---|---|
> | Bash commands Claude can't guess | Anything Claude can figure out by reading code |
> | Code style rules that differ from defaults | Standard language conventions Claude already knows |
> | Testing instructions and preferred test runners | **Detailed API documentation (link to docs instead)** |
> | Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
> | Architectural decisions specific to your project | Long explanations or tutorials |
> | Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
> | Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

**한국어**:
> "Anthropic 공식 표가 직접 4계층 분리를 가르칩니다 — *상세한 API 문서는 CLAUDE.md에 넣지 말고 공식 문서로 링크*하세요. *자주 바뀌는 정보*도 빼세요. CLAUDE.md가 비대해지면 Claude는 진짜 지시까지 무시합니다."

**세션 내 사용 위치**: 진행 순서 2번 — 본문의 정보 위치 판단 기준이 *Anthropic 공식 표*와 그대로 일치한다는 근거.
**왜 중요한가**: "공식 문서 링크와 확인 날짜로 둔다"라는 강의 권고가 Anthropic이 *Detailed API documentation (link to docs instead)* 라고 명문화한 항목과 동일.

---

### A7. ★ Anthropic — Skills (온디맨드 로딩 = 4계층 분리의 *물리적 구현*)

**출처**: Anthropic Claude Code Docs — Skills
**URL**: https://code.claude.com/docs/en/skills
**확인일**: 2026-04-30

**원문 (영어)**:
> "Create a skill when you keep pasting the same playbook, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. Unlike CLAUDE.md content, **a skill's body loads only when it's used, so long reference material costs almost nothing until you need it.**"
>
> "Reference content adds knowledge Claude applies to your current work... runs inline so Claude can use it alongside your conversation context."
>
> "Task content gives Claude step-by-step instructions for a specific action, like deployments, commits, or code generation."
>
> Memory 페이지의 정리:
> > "Rules load into context every session or when matching files are opened. For task-specific instructions that don't need to be in context all the time, use skills instead, which only load when you invoke them or when Claude determines they're relevant to your prompt."

**한국어**:
> "Anthropic은 *항상 로딩되는 CLAUDE.md*와 *필요할 때만 로딩되는 Skill*을 의도적으로 분리합니다 — '같은 체크리스트를 또 붙여 넣고 있다면 그건 대화가 아니라 Skill로 옮길 신호'입니다. *길고 자주 안 쓰는 자료는 0 비용으로 둘 곳이 따로 있습니다.*"

**세션 내 사용 위치**: 진행 순서 2번(길고 자주 바뀌는 배경 자료 → 별도 문서), 3번(긴 프롬프트 분해의 종착지)
**왜 중요한가**: 강의의 "4계층 분리"가 단순 권고가 아니라 Claude Code 제품 *내부 구조 그 자체*임을 보이는 자료. *Always-loaded(CLAUDE.md) vs On-demand(Skill)* 의 공식 구분.

---

### A8. agents.md — AGENTS.md 오픈 표준 ("README for agents")

**출처**: agents.md (오픈 표준)
**URL**: https://agents.md/
**확인일**: 2026-04-30

**원문 (영어)**:
> "A simple, open format for guiding coding agents."
>
> "Think of AGENTS.md as a **README for agents**: a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project."
>
> "AGENTS.md complements README by containing the extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README or aren't relevant to human contributors."
>
> "anything you'd tell a new teammate belongs here too."

또한 Anthropic memory 페이지가 명시:
> "Claude Code reads CLAUDE.md, not AGENTS.md. If your repository already uses AGENTS.md for other coding agents, create a CLAUDE.md that imports it so both tools read the same instructions without duplicating them."

**한국어**:
> "AGENTS.md는 *에이전트를 위한 README* — README가 사람을 위한 빠른 시작이라면, AGENTS.md는 에이전트가 *반복해서* 필요한 빌드 단계, 테스트, 규칙을 두는 자리입니다. README를 어지럽히지 않으면서도 에이전트에게는 필수인 정보를 분리해 둘 수 있습니다."

**세션 내 사용 위치**: 진행 순서 5번 — Part 2 종합 실습에서 작업 전 규칙 문서를 읽게 만드는 자리. AGENTS.md 사용자에게도 동일 4계층 모델이 적용됨을 보임.

---

## 3. 검증된 사례 / 업계 발표 (B1)

### B1. ★ Cognition AI — "Don't Build Multi-Agents" (분리 실패가 실제로 어떻게 무너지는지)

**출처**: Cognition AI Blog (Devin 제작사)
**URL**: https://cognition.ai/blog/dont-build-multi-agents
**확인일**: 2026-04-30

**한 줄 요약 (강사 인용용)**:
> "Devin을 만든 Cognition은 *멀티 에이전트 분리*를 시도했다가 명시적으로 실패를 보고했습니다 — 작업이 여러 에이전트에 흩어지자 *컨텍스트가 충분히 공유되지 않아* 작은 모델이 큰 모델의 의도를 미세한 모호함에서 잘못 해석했습니다."

**무슨 일**: Cognition은 멀티 에이전트로 작업을 분산하면 효율이 좋아질 거라 가정하고 시스템을 만들었는데, 실제로는 결정이 분산되면서 *충돌하는 결정*과 *컨텍스트 단절*로 결과가 나빠졌다. 글의 결론은 두 원칙으로 압축됨.

**원문 (영어)**:
> "**Principle 1**: Share context, and share full agent traces, not just individual messages."
>
> "**Principle 2**: Actions carry implicit decisions, and conflicting decisions carry bad results."
>
> "The decision-making ends up being too dispersed and context isn't able to be shared thoroughly enough between the agents."
>
> "the small model would misinterpret the instructions of the large model and make an incorrect edit due to the most slight ambiguities in the instructions."
>
> "Context engineering... is about doing this automatically in a dynamic system. It takes more nuance and is effectively the **#1 job of engineers building AI agents**."

**4계층 분리 명제와의 연결**:
강의의 4계층 분리는 *정보의 성격*에 따른 분리이지 *작업의 분산*이 아니다. Cognition의 사례는 "*잘못된 분리*(작업 분산)는 실제로 실패한다"를 보임으로써, 강의가 권장하는 분리(같은 정보를 *반복하지 않을 곳*에 놓는 분리)와 *대조*된다. — 진행 순서 1번에서 "긴 프롬프트를 잘게 쪼갠다고 다 좋은 게 아니다, *어떤 축으로* 쪼개느냐가 핵심"이라는 메시지의 정당화.

**세션 내 사용 위치**: 진행 순서 1번(분리의 *축*을 잘못 잡으면 실패한다는 반례), 3번(긴 프롬프트 분해의 *원칙* 보강)
**왜 중요한가**: Anthropic 외 진영(Cognition AI)이 동일 결론을 *반대 사례*로 공개 발표 → 진영 중립성 확보. "*컨텍스트 엔지니어링은 AI 에이전트 엔지니어의 #1 업무*"라는 카메라 인용 줄을 직접 가져갈 수 있음.

---

## 4. 학술/업계 연구 (D1~D3)

### D1. ★ Lost in the Middle — 위치가 정확도를 결정한다

**저자/발표**: Liu et al., "Lost in the Middle: How Language Models Use Long Contexts", arXiv:2307.03172, TACL 2024
**URL**: https://arxiv.org/abs/2307.03172
**확인일**: 2026-04-30

**한 줄 핵심 발견**:
> "관련 정보가 *컨텍스트의 중간*에 놓이면 정확도가 급격히 떨어진다 — 같은 정보라도 처음과 끝에 있을 때 가장 잘 활용된다."

**원문 (영어)**:
> "performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models."
>
> "performance can degrade significantly when changing the position of relevant information"

**한국어 (카메라 인용용)**:
> "TACL 2024에서 발표된 *Lost in the Middle* 연구에 따르면, 같은 정보라도 *어디에 두느냐*에 따라 모델이 그것을 활용하는 정확도가 달라집니다 — 중간에 묻힌 정보는 거의 사라집니다. 그래서 우리는 정보를 *섞어 한 통에 두지 않고* 4개 위치로 분리합니다."

**세션 내 사용 위치**: 진행 순서 1번(왜 분리가 필요한가의 *학술적 근거*), 4번(세션이 길어졌을 때 핸드오프로 빼야 하는 이유)
**왜 중요한가**: 강의의 *4계층 분리*는 직관이 아니라 측정 가능한 효과 — "위치가 결과를 바꾼다"는 정량 연구의 직접 인용 자료.
**한계 명시**: 2023년 발표 시점 모델 기준. 최신 frontier 모델에서 격차가 줄었을 수 있음 — *경향성*만 인용.

---

### D2. RAG 원논문 — 파라메트릭 vs 비파라메트릭 메모리 분리 (외부 공식 문서 계층의 학술적 뿌리)

**저자/발표**: Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", arXiv:2005.11401, NeurIPS 2020
**URL**: https://arxiv.org/abs/2005.11401
**확인일**: 2026-04-30

**한 줄 핵심**:
> "지식을 *모델 파라미터(in-context learning) 안에 욱여넣지 말고 외부 비파라메트릭 메모리(검색 가능한 인덱스)로 분리*하면, 더 사실적이고 다양한 응답을 만든다."

**원문 (영어)**:
> "Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited."
>
> "Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue."
>
> RAG 모델은 "more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline" 를 생성.

**한국어**:
> "RAG 원논문이 학술적으로 정당화한 게 정확히 우리가 4계층에서 하는 일입니다 — *지식을 모델 안에 다 넣으려 하지 말고 외부 인덱스로 분리*해라. 강의의 '외부 공식 문서 계층'은 RAG의 비파라메트릭 메모리와 구조적으로 같은 분리입니다."

**세션 내 사용 위치**: 진행 순서 2번 — *왜 공식 문서 링크는 대화나 CLAUDE.md에 박지 않고 외부에 둔 채 그때그때 가져오는가*의 학술적 근거.
**한계 명시**: 본 논문은 *프롬프트 분리*가 아닌 *학습된 지식과 외부 인덱스의 분리*를 제안한 1차 출처. 강의 맥락(즉시 프롬프트/문서/외부 링크)에 *비유적*으로 인용 — 동일 원리로 일반화 금지.

---

### D3. RAG Survey — Naive / Advanced / Modular (분리 패턴은 진화한다)

**저자/발표**: Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey", arXiv:2312.10997
**URL**: https://arxiv.org/abs/2312.10997
**확인일**: 2026-04-30

**한 줄 핵심**:
> "RAG는 *Naive → Advanced → Modular* 세 단계로 진화했고, 진화의 방향은 *더 잘게 분리하기*다."

**원문 (영어)**:
> "Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes."
>
> "RAG synergistically merges LLMs' intrinsic knowledge with the vast, dynamic repositories of external databases."
>
> "the tripartite foundation of RAG frameworks, which includes the retrieval, the generation and the augmentation techniques."
>
> "continuous knowledge updates and integration of domain-specific information"

**한국어**:
> "이 분야의 서베이 논문은 RAG가 *Naive → Advanced → Modular* 로 진화했다고 정리합니다 — 진화의 방향은 *더 잘게 모듈화하기*입니다. 강의의 4계층 분리도 같은 흐름 — 더 길게가 아니라 *더 잘 나누기*."

**세션 내 사용 위치**: 진행 순서 3번 — 긴 프롬프트 분해가 단발 권고가 아니라 *분야 전체의 진화 방향*임을 보강.
**한계 명시**: 서베이 논문이라 1차 측정 결과가 아닌 *분야 정리*. 인용 시 *경향성*만 사용.

---

## 5. ★ 4계층 분포표 (각 계층에 매칭된 자료가 무엇인가)

> 강의 차별 명제는 *정보의 성격에 따라 4개 위치로 분리*다. 카메라 앞에서 각 계층을 정당화할 때 인용 가능한 자료를 정리했다.

| 계층 | 무엇을 두는가 | 핵심 1차 자료 |
|---|---|---|
| **① 즉시 프롬프트** | 지금 한 번만 필요한 요청 | A1 Anthropic Context Engineering(*smallest possible high-signal tokens*) / A4 Prompting best practices(XML 분리) / D1 Lost-in-the-Middle(위치가 정확도를 바꾼다) |
| **② 세션 핸드오프** | 다음 세션이 이어가기 위한 요약 | ★A5 Effective Harnesses for Long-Running Agents(`claude-progress.txt`, state artifacts) / A3 Memory("each new session begins with a fresh context window") / B1 Cognition(*share full agent traces*) |
| **③ 프로젝트 문서 (CLAUDE.md / AGENTS.md)** | 매번 지켜야 할 규칙·명령·결정 | ★A3 Memory(4신호, 위치 표) / A6 Best Practices(✅Include / ❌Exclude 표) / A8 agents.md(*README for agents*) |
| **④ 외부 공식 문서** | 자주 바뀌는 제품 기능·API | A6 Best Practices(*"Detailed API documentation (link to docs instead)"*) / A7 Skills(*on-demand 로딩, 항상 로딩되는 CLAUDE.md와 분리*) / D2 RAG 원논문(파라메트릭 vs 비파라메트릭) / D3 RAG Survey |

**강사 권장 인용 시퀀스 (한 호흡 30초)**:
> "긴 프롬프트를 더 길게 만들지 마세요. Anthropic 공식 정의가 그렇습니다 — 컨텍스트 엔지니어링은 *원하는 결과를 만들 가장 작은 고신호 토큰 집합을 큐레이션*하는 일입니다. 그래서 정보를 4개 위치에 나눠 둡니다. *지금 한 번만* 필요하면 즉시 프롬프트, *다음 세션이 이어받아야* 하면 핸드오프 노트, *매번 지켜야 할 규칙*이면 CLAUDE.md/AGENTS.md, *자주 바뀌는 제품 기능*이면 외부 공식 문서 링크. — 이게 컨텍스트 엔지니어링이고, Cognition AI는 이걸 *AI 에이전트 엔지니어의 1순위 업무*라고 표현했습니다."

---

## 6. 인용 시 유의사항 / 한계

1. **"Context Engineering" 용어의 학술 외 위치**: A1 Anthropic 글과 B1 Cognition 글은 *엔지니어링 블로그*로, 동료 검토를 거친 학술 자료가 아니다. 그러나 두 회사가 *각자의 관점에서 동일 결론*에 도달했다는 점에서 강한 산업계 증거. 카메라에서는 "*Anthropic이 정의한…*", "*Cognition이 발표한…*"으로 출처를 분명히 한다.
2. **D2 RAG 원논문은 비유**: RAG는 모델 학습된 지식과 외부 인덱스의 분리를 다루며, 강의의 "프롬프트와 외부 공식 문서의 분리"는 *동일 원리의 다른 적용*이다. *구조적 비유*로만 인용한다 — "RAG 논문이 4계층 분리를 입증했다"고는 인용하지 않는다.
3. **D1 Lost-in-the-Middle 시점 한계**: 2023년 발표. 최신 frontier 모델에서는 격차가 줄었을 수 있다. 정량 수치는 인용하지 않고 *위치가 결과를 바꾼다*는 정성 결론만 사용한다.
4. **Trust 'Cognition' 인용 시**: B1은 *Devin* 제작사의 공개 발표. Devin 제품 자체에 대한 호불호와 분리해, "*컨텍스트 공유 실패가 어떻게 무너지는지에 대한 1차 케이스 스터디*"로만 인용.
5. **A7 Skills**는 Claude Code 신기능. Codex/AGENTS.md 사용자 입장에서는 *동등한 메커니즘이 없을 수도* 있다 — 강의에서 "Anthropic은 이걸 제품 구조로 못 박았다"는 정도로만 사용하고, "당신도 반드시 Skills를 써야 한다"고 말하지 않는다.
6. **트위터/익명 미디엄 글 제외**: 본 자료는 회사 공식 블로그, 공식 docs, arXiv, 오픈 표준 사이트만 채택했다.
7. **번역 보존**: 한국어 인용은 카메라 편의용. 의역이 모호한 부분은 모호하게 두었으니 영어 원문을 항상 우선한다.

---

## 7. 출처 일람 (URL 한 곳에 모음)

### 공식 가이드
- Anthropic — Effective Context Engineering for AI Agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic — Effective Harnesses for Long-Running Agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic Platform Docs — Context Windows: https://platform.claude.com/docs/en/docs/build-with-claude/context-windows
- Anthropic Platform Docs — Prompting Best Practices: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic Claude Code Docs — Memory (CLAUDE.md): https://code.claude.com/docs/en/memory
- Anthropic Claude Code Docs — Best Practices: https://code.claude.com/docs/en/best-practices
- Anthropic Claude Code Docs — Skills: https://code.claude.com/docs/en/skills
- agents.md (오픈 표준): https://agents.md/

### 업계 발표
- Cognition AI — Don't Build Multi-Agents: https://cognition.ai/blog/dont-build-multi-agents

### 학술 연구
- Lost in the Middle (arXiv:2307.03172): https://arxiv.org/abs/2307.03172
- RAG 원논문 (arXiv:2005.11401): https://arxiv.org/abs/2005.11401
- RAG Survey (arXiv:2312.10997): https://arxiv.org/abs/2312.10997
