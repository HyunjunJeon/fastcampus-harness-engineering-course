# Session 2-4 강사용 근거 자료

본문 대본: [`part2/02-04-instruction-refactor.md`](../../part2/02-04-instruction-refactor.md)
형식 참고: [`part2/research/02-01-what-why-how-evidence.md`](./02-01-what-why-how-evidence.md)
자료 작성일: 2026-04-30 / 검증 기준일: 2026-04-30

이 문서는 세션 2-4 "나쁜 지시문을 고치는 실전 리팩터링" 강의 진행 시, 카메라 앞에서 한두 줄 단정적으로 인용할 수 있는 1차 자료(공식 가이드·검증된 사고 사례·공개 학술 연구) 모음이다. **본문 대본을 부풀리지 않기 위해 따로 분리**했다.

---

## 0. 강의 핵심 명제 (이 자료가 뒷받침하는 단 하나의 주장)

> **"AI는 *진단자(diagnostician)*와 *초안 작성자(draft author)*이지, 규칙 문서의 *최종 결정자*가 아니다. 모호한 지시문을 한 번에 고치게 하지 말고, *진단 → 사람이 선택 → AI가 다시 고치기 → 사람이 검증* 루프로 만든다. 사람의 최종 승인이 품질을 보장한다."**

이 명제에 직접 대응하는 자료는 본문에서 **★** 표시로 강조했다.

---

## 1. 진행 순서 ↔ 자료 매칭 매트릭스 (먼저 한 번 보고 들어가는 표)

| 본문 진행 순서 | 1차 자료 (공식 가이드) | 사고 사례 | 학술 연구 |
|---|---|---|---|
| 1. 나쁜 지시문의 증상 | A1 비대 CLAUDE.md, A2 specificity, ★A3 Plan Mode "explore first" | C1 Gemini 무허가 덮어쓰기 | — |
| 2. 문제 분류 (모호/충돌/구식) | A1 한 줄씩 솎아내기, ★B2 GPT-5 모순 경고 | — | D1 FollowBench |
| 3. ★ AI에게 진단부터 시킨다 | ★A3 Plan Mode, ★A4 Writer/Reviewer, ★A5 Prompt improver, ★B1 GPT-5 metaprompting | C2 Gemini 238GB(자체 진단 사례) | ★D2 LLM-as-Judge, ★D3 Self-Refine |
| 4. 사람이 선택한다 | ★A6 AskUserQuestion(plan mode), ★A4 사람이 리뷰 피드백 전달 | — | ★D4 LLMs cannot self-correct (외부 피드백 필요) |
| 5. 리팩터링 후 검증 | ★A7 verify rock-solid, A8 trust-then-verify gap | — | D5 Reflexion (검증 루프), D3 Self-Refine |

★ = "AI ≠ 최종 결정자, 진단 → 사람 선택 → 재수정 → 검증 루프" 명제 직결 자료

---

## 2. Anthropic / OpenAI 공식 가이드 (A1~A8, B1~B2)

### A1. CLAUDE.md는 비대해지면 무시당한다 — "한 줄씩 솎아내라"

**출처**: Anthropic Claude Code — Best Practices, "Write an effective CLAUDE.md"
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "Keep it concise. For each line, ask: *'Would removing this cause Claude to make mistakes?'* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
>
> "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost in the noise."
>
> "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."

**한국어 (카메라 인용용)**:
> "한 줄 한 줄에 *'이 줄을 빼면 Claude가 실수할까?'* 라고 물어서 아니면 지우세요. 비대한 CLAUDE.md는 무시당합니다. 같은 잘못을 계속하면 — 규칙이 너무 길어서 묻혔다는 뜻입니다."

**세션 내 사용 위치**: 진행 순서 1번(나쁜 지시문 증상), 2번(분류 기준)

---

### A2. 구체성(specificity) — "코드 정리하기" 말고 "2칸 들여쓰기"

**출처**: Anthropic Claude Code — Memory, "Write effective instructions"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30 (200 OK, A1과 동일 best-practices 페이지에서도 재인용됨)

**원문 (영어)** — Best Practices 표:
> "✅ Include / ❌ Exclude
> - Bash commands Claude can't guess / Anything Claude can figure out by reading code
> - Code style rules that differ from defaults / Standard language conventions Claude already knows
> - Architectural decisions specific to your project / Long explanations or tutorials
> - Common gotchas or non-obvious behaviors / Self-evident practices like 'write clean code'"

**한국어**:
> "Claude가 코드만 읽고도 알 수 있는 건 빼세요. 표준 컨벤션, 자명한 모범사례('깔끔하게 짜라'), 자주 바뀌는 정보 — 다 *제외* 후보입니다."

**세션 내 사용 위치**: 진행 순서 1번 — "오래된 명령", "검증 불가능한 태도 지침" 분류 정당화

---

### A3. ★ Plan Mode — "탐색→계획→구현→커밋, 코딩 전에 먼저 분리하라"

**출처**: Anthropic Claude Code — Best Practices, "Explore first, then plan, then code"
**URL**: https://code.claude.com/docs/en/best-practices , https://code.claude.com/docs/en/common-workflows
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "Letting Claude jump straight to coding can produce code that solves the wrong problem. Use Plan Mode to separate exploration from execution."
>
> "The recommended workflow has four phases: Explore → Plan → Implement → Commit"
>
> "Plan Mode instructs Claude to create a plan by analyzing the codebase with read-only operations, perfect for exploring codebases, planning complex changes, or reviewing code safely. In Plan Mode, Claude uses [`AskUserQuestion`](/en/tools-reference) to gather requirements and clarify your goals before proposing a plan."

**한국어 (카메라 인용용)**:
> "Anthropic 공식 가이드는 '바로 코딩으로 넘어가면 *엉뚱한 문제*를 풀게 된다'고 단정합니다. 그래서 Plan Mode는 read-only로 *탐색→계획*을 먼저 시키고, 사용자가 그 계획을 본 다음에야 구현으로 넘어갑니다. — 이게 우리 세션의 *진단 → 사람 선택 → 재수정* 루프와 정확히 같은 패턴입니다."

**세션 내 사용 위치**: 진행 순서 1번(왜 바로 고치면 안 되는가), **3번(진단부터 시킨다) 핵심 ★**, 4번(사람이 선택)

---

### A4. ★ Writer/Reviewer 패턴 — 한 세션이 만들고 다른 세션이 검토한다

**출처**: Anthropic Claude Code — Best Practices, "Run multiple Claude sessions"
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "Beyond parallelizing work, multiple sessions enable quality-focused workflows. **A fresh context improves code review since Claude won't be biased toward code it just wrote.**"
>
> 표 인용:
> | Session A (Writer) | Session B (Reviewer) |
> | `Implement a rate limiter for our API endpoints` | |
> | | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
> | `Here's the review feedback: [Session B output]. Address these issues.` | |

**한국어**:
> "같은 Claude가 자기가 쓴 코드를 검토하면 *자기 편향*이 생깁니다. 그래서 Anthropic은 한 세션이 쓰고 *다른 세션이 검토*한 뒤, 그 피드백을 *사람이* 첫 세션으로 다시 전달하라고 권합니다. — 사람이 가운데서 라우팅하는 구조입니다."

**세션 내 사용 위치**: 진행 순서 3번(AI에게 진단), **4번(사람이 선택해서 다음 세션으로 넘긴다) 핵심 ★**

---

### A5. ★ Prompt improver — Anthropic이 직접 만든 "프롬프트를 AI가 진단·개선" 도구

**출처**: Anthropic Console — "Console prompting tools" (Prompt improver)
**URL**: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompt-improver
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "The prompt improver helps you quickly iterate and improve your prompts through automated analysis and enhancement. It excels at making prompts more robust for complex tasks that require high accuracy."
>
> "The prompt improver enhances your prompts in 4 steps:
> 1. **Example identification**: Locates and extracts examples from your prompt template
> 2. **Initial draft**: Creates a structured template with clear sections and XML tags
> 3. **Chain of thought refinement**: Adds and refines detailed reasoning instructions
> 4. **Example enhancement**: Updates examples to demonstrate the new reasoning process"
>
> 사용 절차(원문):
> "1. Submit your prompt template
> 2. Add any feedback about issues with Claude's current outputs
> 3. Include example inputs and ideal outputs
> 4. **Review the improved prompt**"

**한국어**:
> "Anthropic은 *프롬프트 개선 자체를* 사람-AI 협업 4단계로 정의합니다 — ① 사용자가 현재 프롬프트와 *문제 피드백을* 제출 → ② AI가 분석·재구조화 → ③ AI가 chain-of-thought·예시를 보강 → ④ **사용자가 개선안을 검토**. 마지막 단계는 *언제나 사람*입니다."

**세션 내 사용 위치**: 진행 순서 3번 — **"AI에게 진단부터 시킨다"의 공식적 정당화 ★**, 5번(검증)
**왜 중요한가**: 강의의 "AI는 진단자·초안 작성자" 명제를 Anthropic 자신의 *제품 설계*가 그대로 보여줌

---

### A6. ★ AskUserQuestion — Plan Mode는 "사람에게 물어본 뒤" 계획을 짠다

**출처**: Anthropic Claude Code — Common workflows, "Use Plan Mode for safe code analysis"
**URL**: https://code.claude.com/docs/en/common-workflows
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "In Plan Mode, Claude uses `AskUserQuestion` to gather requirements and clarify your goals before proposing a plan."
>
> "Press `Ctrl+G` to open the plan in your default text editor, where you can edit it directly before Claude proceeds."

**한국어**:
> "Plan Mode의 작동 방식 자체가 — Claude가 먼저 사용자에게 *질문해서* 요구사항을 모으고, 계획안을 보여주고, **사용자가 직접 편집한 뒤에야** 실행으로 넘어갑니다. *사람이 중간에 결정자로* 들어와 있는 구조입니다."

**세션 내 사용 위치**: 진행 순서 4번 — "사람이 선택한다"가 모범 사례인 *공식적* 근거 ★

---

### A7. ★ "Verification rock-solid" — 검증 루프가 단일 최고 레버리지

**출처**: Anthropic Claude Code — Best Practices, "Give Claude a way to verify its work"
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "Include tests, screenshots, or expected outputs so Claude can check itself. **This is the single highest-leverage thing you can do.**"
>
> "Without clear success criteria, it might produce something that looks right but actually doesn't work. **You become the only feedback loop**, and every mistake requires your attention."
>
> "Your verification can also be a test suite, a linter, or a Bash command that checks output. **Invest in making your verification rock-solid.**"

**한국어**:
> "Anthropic이 *단일 최고 레버리지 행동*이라고 표현한 게 검증 루프입니다. 그리고 이 검증이 견고하지 않으면 *사용자 본인이 유일한 피드백 루프*가 된다고 경고합니다 — 매 실수마다 사람이 직접 잡아야 한다는 뜻입니다."

**세션 내 사용 위치**: 진행 순서 5번(리팩터링 후 검증) 핵심 ★

---

### A8. "Trust-then-verify gap" — Anthropic이 직접 명명한 실패 패턴

**출처**: Anthropic Claude Code — Best Practices, "Avoid common failure patterns"
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "**The trust-then-verify gap.** Claude produces a plausible-looking implementation that doesn't handle edge cases.
> > **Fix**: Always provide verification (tests, scripts, screenshots). **If you can't verify it, don't ship it.**"

**한국어**:
> "Anthropic이 직접 이름 붙인 *trust-then-verify gap* — '그럴듯해 보이는 구현이 엣지케이스를 못 잡는다'. 검증할 수 없으면 배포하지 마세요."

**세션 내 사용 위치**: 진행 순서 5번 — before/after diff를 *사람이 읽는* 단계 정당화

---

### B1. ★ GPT-5: AI에게 자기 프롬프트를 진단·개선시켜라 (metaprompting)

**출처**: OpenAI Cookbook — GPT-5 Prompting Guide, "Metaprompting"
**URL**: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "Early testers have found great success using GPT-5 as a meta-prompter for itself."
>
> 권장 메타프롬프트:
> > "give answers from your own perspective - explain what specific phrases could be added to, or deleted from, this prompt to more consistently elicit the desired behavior"

**한국어 (카메라 인용용)**:
> "OpenAI도 같은 결론입니다. 자기 모델에게 *'이 프롬프트에서 어떤 구절을 추가하거나 삭제하면 의도한 결과가 더 잘 나오는지 너의 관점에서 설명해줘'* 라고 물으라고 권합니다. — *AI를 진단자로* 쓰는 게 OpenAI 공식 권장 패턴입니다."

**세션 내 사용 위치**: 진행 순서 3번 — **"AI에게 바로 고치게 하지 말고 진단부터" 명제의 OpenAI 측 근거 ★**
**왜 중요한가**: Anthropic만 인용한다는 인상을 피하면서 동일 결론을 강화

---

### B2. ★ GPT-5: 모순/모호한 지시는 다른 모델보다 *더* 해롭다 — 그래서 진단이 먼저

**출처**: OpenAI Cookbook — GPT-5 Prompting Guide, "Optimizing Intelligence and Instruction-Following"
**URL**: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
**확인일**: 2026-04-30 (200 OK)

**원문 (영어)**:
> "Its careful instruction-following behavior means that poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5 than to other models, as it expends reasoning tokens searching for a way to reconcile the contradictions."

**한국어**:
> "GPT-5처럼 지시를 엄격히 따르는 모델일수록, 모순·모호한 지시문은 *오히려 더 해롭습니다* — 모순을 화해시키느라 추론을 낭비합니다. 그래서 *고치기 전에* 모순부터 진단해야 합니다."

**세션 내 사용 위치**: 진행 순서 2번(문제 분류 — 충돌하는 규칙)

---

## 3. 검증된 사고 사례 (C1~C2)

> 한 번에 큰 변경을 시켰다가 의도하지 않은 결과가 나온 사례. 모두 공식 GitHub Issue에서 1차 출처 확인. 트위터·익명 미디엄·재현 불가능한 회상은 의도적으로 제외.

### C1. Gemini CLI의 무허가 코드 통째 덮어쓰기 — "진단 없이 한 번에 고치기"의 결과

**한 줄 요약 (강사 인용용)**:
> "지시는 '문서 업데이트'였는데, 진단 단계 없이 에이전트가 곧장 surgical edit 도구 대신 `write_file`로 통째 덮어쓰며 기능 코드를 텍스트 요약으로 바꿔놓았습니다."

**무슨 일**: Gemini CLI v0.37.0, gemini-3-flash-preview. 사용자가 문서 파일 업데이트를 요청. 에이전트가 functional 코드까지 high-level text summary로 대체. 정밀 부분 수정(`replace`) 대신 통째 덮어쓰기(`write_file`) 선택. "Engineering Standards", "Contextual Precedence" 위반.

**본 세션 명제와의 연결**: 사용자가 (a) "어떤 부분을" (b) "어떤 도구로" (c) "변경 전 진단부터" 라는 단계 분리를 *지시문에 적지 않았기* 때문에, AI가 *최종 결정자처럼* 행동해 광범위 덮어쓰기를 실행. → 강의의 "진단 → 사람 선택 → AI 재수정" 루프 부재의 직접 사례.

**출처**:
- 공식 GitHub Issue: https://github.com/google-gemini/gemini-cli/issues/24954
- 발생 시점: 2026-04-08
- 확인일: 2026-04-30 (200 OK)

**세션 내 사용 위치**: 진행 순서 1번(나쁜 지시문 증상 — "한 번에 고쳐라"의 결과), 5번 보조

---

### C2. Gemini CLI 238GB 음악 라이브러리 영구 삭제 — 자체 사후 진단 사례

**한 줄 요약**:
> "사용자가 모호한 지시 한 줄을 주자, 에이전트는 진단 없이 인터넷 스니펫을 채택해 사전 합의된 안전 제약을 덮어썼고, 결국 `sudo rm -rf`로 238GB를 영구 삭제했습니다. 사후 *에이전트 자신이* '검증 단계 없이 인터넷 스니펫을 맹목적으로 적용했다'고 자백했습니다."

**무슨 일**: Gemini CLI v0.38.0. 사용자가 사전에 "Copy → integrity 확인 → cleanup → rename"이라는 안전 프로토콜에 합의. 컨테이너 crash 후 사용자가 모호한 추가 지시를 줬고, 에이전트가 Beets 표준 docker-compose 스니펫(`move: yes`)을 무비판적으로 채택. 사용자가 "abort and delete the beets output folder"라고 했을 때 에이전트가 자기가 바꾼 config를 잊고 `sudo rm -rf /mnt/media/music` 실행. 사후 자체 진단: *"검증 단계 없이 인터넷 스니펫을 맹목적으로 적용하고, 시스템 상태를 경험적으로 확인하지 않은 채 파괴적 명령을 실행했다"*.

**본 세션 명제와의 연결**: 가장 흥미로운 점은 — *AI 자신이 사후에는 정확히 진단을 해냈다는 것*. 즉 "AI는 진단자로는 유능하지만, 그 진단을 *행동 직전에* 사람이 확인하지 않으면 무용지물"이라는 강의 명제를 정확히 증명. 사람이 *중간에* 들어왔다면 막을 수 있었던 사고.

**출처**:
- 공식 GitHub Issue (full agent self-report 포함): https://github.com/google-gemini/gemini-cli/issues/25592
- 발생 시점: 2026년 4월
- 확인일: 2026-04-30 (200 OK)

**세션 내 사용 위치**: 진행 순서 3번(AI는 진단자로 유능 — 그러나 사람이 가운데 없으면 무용), 4번(사람이 선택 단계의 필요성)

---

## 4. 학술/업계 연구 (D1~D5)

### D1. FollowBench — 제약을 한 줄씩 더할수록 모델은 *조용히* 일부를 누락한다

**저자/발표**: Yuxin Jiang et al. (HKUST & Huawei), arXiv:2310.20410, ACL 2024
**URL**: https://arxiv.org/abs/2310.20410
**확인일**: 2026-04-30 (200 OK)

**한 줄 핵심**:
> "지시문에 제약이 많아질수록 모델 성공률이 떨어지고, 어떤 제약을 무시했는지 알기 어려워진다."

**연구 요약 (abstract)**:
> "FollowBench comprehensively includes five different types (i.e., Content, Situation, Style, Format, and Example) of fine-grained constraints" — 13개 LLM에 다섯 종류 제약을 한 단계씩 누적해 실험. 결과: 모델은 일부 제약을 누락하기 시작하며, 평가 결과는 *현재 LLM들의 instruction-following 약점*을 드러낸다.

**본 세션 명제와의 연결**: 길고 모호한 지시문에는 *어떤 규칙이 깨졌는지조차 측정 불가능*하다는 객관적 근거. 그래서 ① 한 줄씩 분리해 쓰고 ② 검증 가능한 형태로 쓰고 ③ AI에게 *어떤 제약이 충돌하는지* 진단부터 시켜야 한다.

**카메라 인용용**:
> "ACL 2024에서 발표된 FollowBench 연구는 13개 LLM에서 제약이 늘수록 일부가 *조용히 누락*되며, 그 약점이 객관적으로 드러난다고 보고했습니다. — 그래서 우리는 모호한 지시문을 *한 번에 고치게* 하지 않고, *AI에게 모순부터 짚어달라고* 합니다."

**세션 내 사용 위치**: 진행 순서 2번(문제 분류 정당화)
**한계 명시**: 2023~2024년 평가 모델 기준. 최신 frontier 모델에서는 격차가 줄었을 수 있음 — *경향성*으로만 인용.

---

### D2. ★ LLM-as-a-Judge — AI는 평가자로 80% 인간 일치, 단 편향이 있다

**저자/발표**: Lianmin Zheng et al. (UC Berkeley·Stanford 등), arXiv:2306.05685, NeurIPS 2023 Datasets and Benchmarks Track
**URL**: https://arxiv.org/abs/2306.05685
**확인일**: 2026-04-30 (200 OK)

**한 줄 핵심**:
> "강한 LLM(GPT-4)은 인간 평가자와 80% 이상 일치하지만, position·verbosity·self-enhancement bias가 존재한다."

**연구 요약 (abstract 인용)**:
> "Strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans."
> "Position, verbosity, and self-enhancement biases, as well as limited reasoning ability."

**본 세션 명제와의 연결**: AI를 *판사·진단자*로 쓰는 건 학술적으로 정당화된다(인간 80% 일치). 그러나 *self-enhancement bias*(자기가 쓴 답을 더 좋게 평가) 때문에 **자기가 쓴 지시문을 자기가 최종 승인하는 건 위험**하다 → 강의의 "AI ≠ 최종 결정자, 사람이 검증" 결론과 정확히 일치. Writer/Reviewer 패턴(A4)의 학술적 근거이기도 함.

**카메라 인용용**:
> "NeurIPS 2023의 LLM-as-a-Judge 연구는 강한 모델은 인간 평가자와 80% 이상 일치한다고 보고합니다. *AI를 진단자로 쓰는 건 정당합니다.* 그러나 같은 연구가 *self-enhancement bias* — 자기가 쓴 답을 더 좋게 평가하는 편향 — 도 함께 보고했습니다. 그래서 *최종 승인은 항상 사람*이어야 합니다."

**세션 내 사용 위치**: 진행 순서 3번(AI를 진단자로 정당화), 4번(왜 사람이 결정자) ★
**한계 명시**: 일반 텍스트 평가 벤치마크. 코드/규칙 문서 평가에 그대로 일반화 금지 — *경향성*만 인용.

---

### D3. ★ Self-Refine — "초안 → 자기 피드백 → 개선" 반복은 평균 ~20% 향상

**저자/발표**: Aman Madaan et al. (CMU·Allen AI·Washington 등), arXiv:2303.17651, NeurIPS 2023
**URL**: https://arxiv.org/abs/2303.17651
**확인일**: 2026-04-30 (200 OK)

**한 줄 핵심**:
> "같은 LLM이 (1) 초안을 쓰고 (2) 자기 출력에 피드백을 주고 (3) 그 피드백으로 다시 고치는 반복만으로 7개 작업에서 평균 ~20% 향상."

**연구 요약 (abstract 인용)**:
> "Generate an initial output using an LLMs; then, the same LLMs provides feedback for its output and uses it to refine itself, iteratively."
> "Improvements of ~20% absolute on average in task performance" (GPT-3.5/ChatGPT/GPT-4 포함, 대화 생성·수학 추론 등 7개 작업).

**본 세션 명제와의 연결**: "AI는 진단자이자 초안 작성자"라는 강의 명제의 **학술적 직접 근거**. 단, Self-Refine은 *외부 피드백 없이도* 일부 향상을 보였지만 — D4가 보여주듯 그 한계가 분명하다(외부/사람 피드백이 들어가야 안정적 향상).

**카메라 인용용**:
> "NeurIPS 2023의 Self-Refine 연구는 같은 LLM이 *초안을 쓰고 → 자기 출력을 비판하고 → 다시 고치는* 반복만으로 평균 약 20% 향상을 보고했습니다. 우리 세션의 *진단 → 재수정* 루프와 정확히 같은 구조입니다."

**세션 내 사용 위치**: 진행 순서 3번(AI를 진단자로 활용), 5번(검증 후 재수정) ★
**한계 명시**: 수치(20%)는 발표 시점 모델 기준. 정성 결론(*반복 루프가 향상시킨다*)만 인용 권장.

---

### D4. ★ LLMs는 외부 피드백 없이 자기 답을 못 고친다 — 사람이 *반드시* 들어와야 하는 이유

**저자/발표**: Jie Huang et al. (UIUC·Google), arXiv:2310.01798, ICLR 2024 (Spotlight)
**URL**: https://arxiv.org/abs/2310.01798
**확인일**: 2026-04-30 (200 OK)

**한 줄 핵심**:
> "LLM은 외부 피드백 없이 자기 응답을 self-correct하지 못한다. 때로는 self-correction *후에 성능이 더 나빠진다*."

**연구 요약 (abstract 인용)**:
> "LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction."
> *Intrinsic self-correction* (외부 도움 없이 모델 자기 능력만으로 초안을 수정하는 능력) 가 핵심 조사 대상.

**본 세션 명제와의 연결**: 이 논문 **하나만으로** 강의 명제가 정당화된다. *AI 혼자서 진단하고 자기가 고치게 두면 — 더 나빠질 수 있다*. 그래서 "진단 → **사람이 선택** → AI 재수정 → **사람이 검증**" 루프가 필요하다. D3(Self-Refine)와 표면상 충돌하지만, D3의 향상도 외부적 신호(테스트 케이스, rubric)가 있을 때 안정적이라는 점에서 두 논문은 결국 같은 결론으로 수렴 — *외부 신호(=사람) 없이는 안 된다*.

**카메라 인용용**:
> "ICLR 2024의 'LLMs Cannot Self-Correct Reasoning Yet' 연구는 *외부 피드백이 없으면 LLM이 자기 답을 고치는 데 실패하고, 때로는 더 나빠진다*고 보고했습니다. 그래서 우리는 AI에게 진단만 시키고, *선택은 사람이* 합니다."

**세션 내 사용 위치**: 진행 순서 4번(사람이 선택해야 하는 이유) **핵심 ★**
**한계 명시**: 주로 추론(reasoning) 과제 기준. 단순 형식 교정에는 적용 강도가 다를 수 있음.

---

### D5. Reflexion — 언어적 피드백으로 *반복하면* 학습한다 (HumanEval 91% pass@1)

**저자/발표**: Noah Shinn et al. (Northeastern·MIT 등), arXiv:2303.11366, NeurIPS 2023
**URL**: https://arxiv.org/abs/2303.11366
**확인일**: 2026-04-30 (200 OK)

**한 줄 핵심**:
> "에이전트가 작업 피드백 신호를 *언어로 성찰*해 episodic memory에 저장하면 다음 시도가 좋아진다 — HumanEval에서 GPT-4의 80%를 넘어 91% pass@1 달성."

**연구 요약 (abstract 인용)**:
> "Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials."

**본 세션 명제와의 연결**: 우리 세션의 5번 단계(검증 후 재수정 루프)에 정확히 대응. 한 번에 끝내지 않고 *피드백 → 성찰 → 재시도* 구조가 코드 생성에서도 효과적임을 입증. 단 Reflexion은 외부 *작업 피드백 신호*(unit test pass/fail 등)에 의존 — *외부 신호가 사람에게서 와야 한다*는 점은 D4가 보완.

**카메라 인용용**:
> "NeurIPS 2023의 Reflexion 연구는 에이전트가 *작업 피드백을 언어로 성찰*하고 다음 시도에 반영하면 HumanEval에서 GPT-4의 80%를 넘어 91% pass@1까지 올랐다고 보고했습니다. 한 번에 끝내지 않고 *루프로* 가는 게 학술적으로도 검증된 패턴입니다."

**세션 내 사용 위치**: 진행 순서 5번(검증 후 다시 같은 작업 지시를 해본다)
**한계 명시**: 수치(91%) 인용은 발표 시점 GPT-4 기준. 정성 결론(*반복 루프가 향상*)만 인용 권장.

---

## 5. ★ "AI ≠ 최종 결정자, 사람이 가운데" 명제 직결 모음

> 이 세션이 *다른 프롬프트 강의와 구분되는 유일한 차별점*이 이 명제다. 카메라 앞에서 단정적으로 인용하면 좋은 자료를 한 곳에 모았다.

| 자료 | 한 줄 요지 |
|---|---|
| **A3** Plan Mode 공식 가이드 | "바로 코딩하면 *엉뚱한 문제*를 푼다 — 탐색→계획→구현→커밋으로 분리하라" — Anthropic 공식 |
| **A4** Writer/Reviewer 패턴 | "같은 Claude는 자기 코드에 편향됨 — 다른 세션이 검토, *사람이 라우팅*" — Anthropic 공식 |
| **A5** Prompt improver 4단계 | 마지막 단계가 명시적으로 *"Review the improved prompt (사용자가)"* — Anthropic 제품 설계 자체 |
| **A6** AskUserQuestion | Plan Mode가 *사람에게 먼저 물어본 뒤* 계획안을 제시 — 공식 도구 동작 명세 |
| **B1** GPT-5 metaprompting | "AI에게 자기 프롬프트를 진단·개선시켜라" — OpenAI 공식 권장 |
| **D2** LLM-as-Judge | AI 평가는 인간 80% 일치 (정당성) BUT self-enhancement bias 존재 (왜 사람이 최종) |
| **D4** LLMs cannot self-correct | "외부 피드백 없으면 self-correct 실패, 더 나빠질 수도" — 사람이 *반드시* 들어와야 하는 학술적 근거 |

**강사 권장 인용 시퀀스 (한 호흡 30초)**:
> "Anthropic 공식 가이드는 Plan Mode를 통해 *탐색→계획→구현→커밋*을 분리하고, AskUserQuestion으로 *사람에게 먼저 묻고*, 그 뒤에야 코드를 짭니다. OpenAI도 *AI를 자기 프롬프트의 진단자*로 쓰라고 권합니다. 그리고 ICLR 2024의 'LLMs Cannot Self-Correct' 연구는 *외부 피드백 없이는 자기 답을 고치지 못하고, 때로는 더 나빠진다*고 보고합니다. — 그래서 우리는 AI를 진단자·초안 작성자로만 쓰고, *선택과 검증은 사람이* 합니다."

---

## 6. 인용 시 유의사항 / 한계

1. **Anthropic URL 구조 변경**: `docs.anthropic.com` → `platform.claude.com/docs/en/...`, Claude Code 문서는 `code.claude.com/docs/en/...`로 이전됨(2026-04-30 기준). 옛 URL이 박힌 자료는 갱신 필요.
2. **수치 인용 금지**: D3 Self-Refine의 ~20%, D5 Reflexion의 91% 같은 수치는 *발표 시점 모델 기준*이라 최신 모델에서는 다를 수 있다. 정성 결론(*반복 루프가 효과적*)만 인용.
3. **D2 vs D3/D5 vs D4의 미묘한 관계**: D2는 "AI는 평가자로 어느 정도 신뢰 가능"이라 하고, D3·D5는 "self-feedback이 향상시킨다"고 하지만, D4는 "외부 피드백이 없으면 안 된다"고 한다. *겉보기*에 충돌처럼 보이지만, **공통 결론은 "외부 신호(=사람의 선택과 검증)가 들어올 때만 안정적"**. 강의에서 단일 결론으로 정리할 때는 D4를 *외부 신호 필요성의 증명*으로 위치시키고, D3·D5는 *그 외부 신호가 들어왔을 때 효과 크기 증명*으로 위치시키면 일관성이 유지된다.
4. **사고 사례는 Gemini CLI 두 건만 직접 확보**: 한 번에 큰 변경 → 사고 패턴의 *공식 GitHub Issue 1차 출처*가 확인된 것은 본 자료에서 두 건. 추가 사례는 본 시리즈 02-01-evidence(Replit DB 삭제 등)와 교차 인용 가능.
5. **Anthropic 만 인용 회피**: A1~A8이 Anthropic이라 진영 편중처럼 보일 수 있음. B1·B2(OpenAI)와 D-시리즈(arXiv·NeurIPS·ICLR)를 함께 인용해 *진영 중립성*을 유지할 것.
6. **번역 의미 보존**: 본 문서의 한국어 번역은 강사 인용 편의용. 원문이 모호한 부분은 모호하게 번역. 의역 시 영어 원문 재확인 권장.
7. **본문 대본 미수정**: `02-04-instruction-refactor.md`는 본 작업에서 *수정하지 않았다*. 이 파일은 부록(evidence)으로만 추가된다.

---

## 7. 출처 일람 (URL 한 곳에 모음, 모두 2026-04-30 200 OK)

### 공식 가이드 (Anthropic / OpenAI)
- Anthropic Claude Code Best Practices: https://code.claude.com/docs/en/best-practices
- Anthropic Claude Code Common workflows (Plan Mode): https://code.claude.com/docs/en/common-workflows
- Anthropic Claude Code Memory (CLAUDE.md): https://code.claude.com/docs/en/memory
- Anthropic Console Prompt improver: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/prompt-improver
- OpenAI Cookbook GPT-5 Prompting Guide: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide

### 사고 사례
- Gemini CLI 무허가 코드 덮어쓰기 (Issue #24954): https://github.com/google-gemini/gemini-cli/issues/24954
- Gemini CLI 238GB 삭제 자체 진단 (Issue #25592): https://github.com/google-gemini/gemini-cli/issues/25592

### 학술 연구
- FollowBench (arXiv:2310.20410, ACL 2024): https://arxiv.org/abs/2310.20410
- LLM-as-a-Judge / MT-Bench (arXiv:2306.05685, NeurIPS 2023): https://arxiv.org/abs/2306.05685
- Self-Refine (arXiv:2303.17651, NeurIPS 2023): https://arxiv.org/abs/2303.17651
- LLMs Cannot Self-Correct Reasoning Yet (arXiv:2310.01798, ICLR 2024): https://arxiv.org/abs/2310.01798
- Reflexion (arXiv:2303.11366, NeurIPS 2023): https://arxiv.org/abs/2303.11366
