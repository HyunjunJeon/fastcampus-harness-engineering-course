# Session 2-2 강사용 근거 자료

본문 대본: [`part2/02-02-claude-md.md`](../../part2/02-02-claude-md.md)
형식 참고: [`part2/research/02-01-what-why-how-evidence.md`](./02-01-what-why-how-evidence.md)
자료 작성일: 2026-04-30 / 검증 기준일: 2026-04-30

이 문서는 세션 2-2 "CLAUDE.md 잘 쓰기"를 진행할 때 카메라 앞에서 한두 줄 단정적으로 인용할 수 있는 1차 자료(Anthropic 공식 문서·표준 문서·공식 GitHub issue·학술 논문) 모음이다. 본문 대본을 부풀리지 않기 위해 별도 파일로 분리했다.

---

## 0. 강의 핵심 명제 (이 자료가 뒷받침하는 단 하나의 주장)

> **"CLAUDE.md는 *반복 지시*를 줄이는 도구이지 *모든 컨텍스트*를 담는 곳이 아니다. 비대해진 CLAUDE.md는 무시당하고, 계층(전역/프로젝트/하위폴더) 충돌은 모델을 흔든다."**

이 명제에 직접 대응하는 자료는 본문에서 **★** 표시로 강조했다.

---

## 1. 진행 순서 ↔ 자료 매칭 매트릭스 (먼저 한 번 보고 들어가는 표)

| 본문 진행 순서 | 1차 자료 (공식 가이드) | 검증된 사례 | 학술/업계 연구 |
|---|---|---|---|
| 1. 규칙 파일이 필요한 이유 | A1 "재설명을 줄이는 곳", A2 4가지 신호, A6 compaction 후 재주입 | — | — |
| 2. 규칙의 계층 (전역/프로젝트/하위폴더) | A3 위치별 scope 표, A4 로딩 순서 / 충돌 시 임의 선택, A8 AGENTS.md 호환 | C1 monorepo claudeMdExcludes 동기 | ★D2 OpenAI Instruction Hierarchy |
| 3. 좋은 CLAUDE.md 구조 | A5 구체성 3대 예시, A7 "Include vs Exclude" 표, A9 emphasis tuning | — | — |
| 4. 나쁜 규칙을 피한다 | ★A5 "200줄 이하·비대하면 무시", ★A7 "이 줄을 빼면 실수할까?", A4 충돌 임의 해결 | — | ★D1 Same Task, More Tokens |
| 5. 20줄 이하의 초안을 만든다 | A1 `/init`, A5 specificity, A9 검토 루틴 | — | — |

★ = 차별 명제(반복 지시 축소·비대화 회피·계층 충돌 위험) 직결 자료

---

## 2. 공식 가이드 (A1~A9)

### A1. CLAUDE.md는 "다시 설명할 것을 적어두는 곳"

**출처**: Anthropic Claude Code — "How Claude remembers your project", §CLAUDE.md files
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어)**:
> "Treat CLAUDE.md as the place you write down what you'd otherwise re-explain."
>
> "Keep it to facts Claude should hold in every session: build commands, conventions, project layout, 'always do X' rules. If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule instead."

**한국어 (60자 이내, 카메라 인용용)**:
> "CLAUDE.md는 다시 설명할 것을 적어두는 곳입니다."

**세션 내 사용 위치**: 진행 순서 1번 오프닝

---

### A2. CLAUDE.md에 추가해야 할 4가지 신호

**출처**: Anthropic Claude Code — Memory, "When to add to CLAUDE.md"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어)**:
> "Add to it when:
> - Claude makes the same mistake a second time
> - A code review catches something Claude should have known about this codebase
> - You type the same correction or clarification into chat that you typed last session
> - A new teammate would need the same context to be productive"

**한국어 (4신호 그대로 슬라이드용)**:
> "같은 실수를 두 번째 했을 때 / 리뷰가 Claude도 알았어야 할 걸 잡았을 때 / 지난 세션에 한 정정을 또 입력할 때 / 새 팀원에게도 같은 맥락이 필요할 때 — 그게 옮길 신호입니다."

**세션 내 사용 위치**: 진행 순서 1번, "반복 지시를 줄인다"의 직접 정당화

---

### A3. CLAUDE.md 계층 — 위치별 scope와 우선순위

**출처**: Anthropic Claude Code — Memory, "Choose where to put CLAUDE.md files"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어, 표 본문 발췌)**:
> "CLAUDE.md files can live in several locations, each with a different scope. **More specific locations take precedence over broader ones.**"
>
> | Scope | Location | Purpose |
> |---|---|---|
> | **Managed policy** | `/Library/Application Support/ClaudeCode/CLAUDE.md` 등 | Organization-wide instructions |
> | **Project instructions** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions |
> | **User instructions** | `~/.claude/CLAUDE.md` | Personal preferences for all projects |
> | **Local instructions** | `./CLAUDE.local.md` | Personal project-specific (gitignore) |

**한국어 (60자 이내)**:
> "구체적인 위치가 넓은 위치를 이깁니다 — 정책·프로젝트·유저·로컬 4단."

**세션 내 사용 위치**: 진행 순서 2번 — 표 그대로 슬라이드에 옮길 수 있음

---

### A4. ★ 로딩 순서와 충돌 처리 — 모순되면 모델이 임의 선택한다

**출처**: Anthropic Claude Code — Memory, "How CLAUDE.md files load" + "Write effective instructions" §Consistency
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어)**:
> "Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory ... All discovered files are concatenated into context rather than overriding each other."
>
> "**Consistency**: if two rules contradict each other, Claude may pick one arbitrarily. Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and `.claude/rules/` periodically to remove outdated or conflicting instructions."
>
> 디버깅 항목: "Look for conflicting instructions across CLAUDE.md files. If two files give different guidance for the same behavior, Claude may pick one arbitrarily."

**한국어 (60자 이내)**:
> "두 규칙이 충돌하면 Claude는 임의로 하나를 고릅니다."

**세션 내 사용 위치**: 진행 순서 2번(계층 설명 마무리), 4번(나쁜 규칙 — 충돌)

---

### A5. ★ "200줄 이하" + "이 줄을 빼면 Claude가 실수할까?" — 비대화 자체가 무시 원인

**출처**: Anthropic Claude Code — Memory §Write effective instructions + Best Practices §Write an effective CLAUDE.md
**URL**: https://code.claude.com/docs/en/memory , https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30

**원문 (영어, 각 페이지에서)**:
> *(memory 페이지)* "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
>
> *(memory 페이지)* "**Specificity**: write instructions that are concrete enough to verify. For example:
> - 'Use 2-space indentation' instead of 'Format code properly'
> - 'Run `npm test` before committing' instead of 'Test your changes'
> - 'API handlers live in `src/api/handlers/`' instead of 'Keep files organized'"
>
> *(best-practices 페이지)* "Keep it concise. For each line, ask: *'Would removing this cause Claude to make mistakes?'* If not, cut it. **Bloated CLAUDE.md files cause Claude to ignore your actual instructions!**"

**한국어 (60자 이내)**:
> "비대한 CLAUDE.md는 진짜 지시를 무시하게 만듭니다 — 한 줄 단위로 잘라내세요."

**세션 내 사용 위치**: 진행 순서 3번(좋은 구조), 4번(나쁜 규칙 핵심 인용), 5번(검토 단계). **차별 명제 직결 ★**

---

### A6. compaction 이후에도 살아남는 건 프로젝트 루트 CLAUDE.md뿐

**출처**: Anthropic Claude Code — Memory, "Instructions seem lost after `/compact`"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어)**:
> "Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories are not re-injected automatically; they reload the next time Claude reads a file in that subdirectory."
>
> "If an instruction disappeared after compaction, it was either given only in conversation or lives in a nested CLAUDE.md that hasn't reloaded yet."

**한국어 (60자 이내)**:
> "긴 대화가 무너져도 핵심 규칙은 루트 CLAUDE.md에서 다시 살아납니다."

**세션 내 사용 위치**: 진행 순서 1번 — "긴 대화가 무너져도 핵심 규칙은 문서에 남는다"의 공식 출처

---

### A7. "포함 vs 제외" 표 — 그대로 슬라이드 사용 가능

**출처**: Anthropic Claude Code — Best Practices, "Write an effective CLAUDE.md"
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30

**원문 (영어, 표 발췌)**:
> | ✅ Include | ❌ Exclude |
> |---|---|
> | Bash commands Claude can't guess | Anything Claude can figure out by reading code |
> | Code style rules that differ from defaults | Standard language conventions Claude already knows |
> | Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
> | Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
> | Architectural decisions specific to your project | Long explanations or tutorials |
> | Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
> | Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

**한국어 (60자 이내)**:
> "넣을 것: 코드만 봐선 알 수 없는 규칙. 뺄 것: 코드를 읽으면 알 수 있는 모든 것."

**세션 내 사용 위치**: 진행 순서 3번(좋은 구조), 4번(나쁜 규칙) — 본문 대본의 8개 섹션 구조와 1:1 대응 가능

---

### A8. AGENTS.md와 호환하려면 import만 거는 게 공식 권장

**출처**: Anthropic Claude Code — Memory, "AGENTS.md"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30

**원문 (영어)**:
> "Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports it so both tools read the same instructions without duplicating them."
>
> 예시:
> ```markdown
> @AGENTS.md
>
> ## Claude Code
> Use plan mode for changes under `src/billing/`.
> ```

**한국어 (60자 이내)**:
> "AGENTS.md가 이미 있다면, CLAUDE.md에서 `@AGENTS.md`로 import하세요."

**세션 내 사용 위치**: 진행 순서 2번 마무리 — Codex 등 다른 에이전트와의 계층 호환

---

### A9. emphasis 튜닝과 검토 루틴 — "코드처럼 다뤄라"

**출처**: Anthropic Claude Code — Best Practices, "Write an effective CLAUDE.md"
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30

**원문 (영어)**:
> "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost. If Claude asks you questions that are answered in CLAUDE.md, the phrasing might be ambiguous."
>
> "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."
>
> "You can tune instructions by adding emphasis (e.g., 'IMPORTANT' or 'YOU MUST') to improve adherence."

**한국어 (60자 이내)**:
> "CLAUDE.md는 코드처럼 — 행동이 변하는지 보고 다듬으세요."

**세션 내 사용 위치**: 진행 순서 5번(사람 최종 편집 단계), 그리고 세션 완료 기준의 직접 출처

---

## 3. 검증된 사례 (C1)

> 본 세션은 "CLAUDE.md 자체로 인한 사고"를 보도된 1차 출처에서 단정적으로 확인하기 어렵다. C1만 공식 문서가 직접 시인한 *현실 문제 패턴*으로 채택했다. 추가 사례는 본 자료에서 의도적으로 비웠다 — §6 한계 참조.

### C1. 모노레포에서 다른 팀의 CLAUDE.md가 계층을 오염시키는 현실 문제 (Anthropic 공식 시인)

**한 줄 요약 (강사 인용용)**:
> "큰 모노레포에서는 부모 디렉터리에 있는 다른 팀의 CLAUDE.md가 자동으로 끌려와 충돌을 만든다 — 이걸 막으려고 Anthropic이 공식적으로 `claudeMdExcludes` 설정을 만들었습니다."

**무슨 일 / 출처 텍스트 (영어)**:
> "If you work in a large monorepo where other teams' CLAUDE.md files get picked up, use `claudeMdExcludes` to skip them."
>
> "In large monorepos, ancestor CLAUDE.md files may contain instructions that aren't relevant to your work. The `claudeMdExcludes` setting lets you skip specific files by path or glob pattern."

**차별 명제와의 연결**: 계층 충돌이 가설이 아니라 **공식 문서가 별도 설정 항목까지 만들어 인정한 현실 문제**라는 증거. 진행 순서 2번 "계층" 설명을 단순 권고에서 *현실 사고 방지* 차원으로 끌어올림.

**출처**:
- Anthropic Claude Code Memory §"Manage CLAUDE.md for large teams" / §"Exclude specific CLAUDE.md files"
- URL: https://code.claude.com/docs/en/memory
- 확인일: 2026-04-30

**세션 내 사용 위치**: 진행 순서 2번(하위 폴더 규칙 위험성), 4번(충돌 회피 정당화)

---

## 4. 학술/업계 연구 (D1~D2)

### D1. ★ Same Task, More Tokens — 입력이 길어지면 같은 문제도 못 푼다

**저자/발표**: Mosh Levy, Alon Jacoby, Yoav Goldberg, ACL 2024 (arXiv:2402.14848)
**URL**: https://arxiv.org/abs/2402.14848
**확인일**: 2026-04-30

**한 줄 핵심 발견**:
> "기술적 최대 컨텍스트보다 *훨씬 짧은* 길이에서 이미 LLM 추론 성능이 떨어지기 시작한다."

**연구 요약**: 같은 QA 추론 문제에 무관한 텍스트 패딩만 추가해 입력 길이를 변화시킨 통제 실험. 결론은 *모든 모델에서* "기술적 최대값보다 훨씬 짧은 입력 길이에서 추론 성능이 눈에 띄게 저하된다(notable degradation in LLMs' reasoning performance at much shorter input lengths than their technical maximum)". 다음 단어 예측 정확도(perplexity 류)는 추론 성능과 *음의 상관*까지 보였다 — "긴 컨텍스트도 잘 처리한다"는 단순 벤치마크가 거꾸로 신호일 수 있다는 의미.

**카메라 인용용 (60자 이내)**:
> "ACL 2024 연구: 컨텍스트가 *기술적 한계 훨씬 전에* 모델 추론은 이미 무너집니다."

**세션 내 사용 위치**: 진행 순서 4번(비대한 CLAUDE.md = 길어진 system 입력 → 직접적인 성능 저하 근거). A5 "200줄 이하" 권고를 *Anthropic 외부 학술 근거로* 강화.

**한계 명시**:
- QA 추론 도메인 실험. CLAUDE.md(코딩 지시문) 도메인 직접 평가 아님 — *경향성*으로만 인용.
- 2024년 발표 시점 모델 기준. 최신 frontier 모델은 격차가 줄었을 수 있음.
- 특정 % 수치는 인용 금지, *"기술적 한계보다 훨씬 짧은 길이에서 이미 떨어진다"*는 정성 결론만 사용.

---

### D2. ★ The Instruction Hierarchy — LLM은 원래 system/user를 똑같이 본다

**저자/발표**: Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, Alex Beutel (OpenAI), arXiv:2404.13208, 2024
**URL**: https://arxiv.org/abs/2404.13208
**확인일**: 2026-04-30

**한 줄 핵심**:
> "현대 LLM은 개발자의 system 지시와 사용자의 user 지시를 *같은 우선순위로* 다룬다 — 그래서 명시적 계층(우선순위)을 학습시켜야 했다."

**연구 요약**: OpenAI는 system → user → tool output 순으로 명시적 *instruction hierarchy* 를 정의하고, 충돌 시 상위 권한 지시가 하위를 덮어쓰도록 학습 데이터를 생성해 GPT-3.5에 fine-tuning. 결과적으로 prompt injection·jailbreak 강건성이 크게 향상. 핵심 인식은 "기본 LLM은 출처가 다른 지시를 동등하게 본다"는 것.

**카메라 인용용 (60자 이내)**:
> "OpenAI 연구: 모델은 원래 system과 user 지시를 동급으로 봅니다 — 계층은 학습돼야 합니다."

**세션 내 사용 위치**: 진행 순서 2번(계층 자체의 의미). "전역·프로젝트·하위폴더" 계층이 *공짜로 작동하지 않으며*, Anthropic의 "more specific takes precedence" 규칙(A3)도 도구 측 구현이지 모델의 기본 능력이 아니라는 점을 분명히 한다.

**한계 명시**:
- OpenAI 모델·OpenAI 정의 계층(system/user/tool) 기준 연구. Anthropic의 CLAUDE.md 4계층(정책/프로젝트/유저/로컬)과 1:1 매핑 아님.
- "계층 충돌이 모델을 흔든다"는 강의 문장의 *메커니즘 설명* 용으로만 인용. 수치는 인용 금지.

---

## 5. ★ 차별 명제 직결 모음

> 본 세션의 차별 명제는 다음 세 줄로 분해된다:
> (1) CLAUDE.md는 *반복* 지시를 줄이는 도구이지 *모든* 컨텍스트가 아니다.
> (2) 비대해진 CLAUDE.md는 *무시당한다*.
> (3) 계층 충돌은 모델을 *흔든다*.

| 명제 분해 | 자료 | 한 줄 요지 |
|---|---|---|
| (1) 반복을 줄이는 도구 | **A1** | "CLAUDE.md는 다시 설명할 것을 적어두는 곳이다" — 공식 정의 |
| (1) 반복을 줄이는 도구 | **A2** | "같은 실수 두 번째 / 같은 정정 두 번째 — *그때* 옮긴다" — 4가지 신호 |
| (2) 비대화 → 무시 | **A5** | "200줄 이하 / 한 줄 단위로 자르기 / 비대해지면 진짜 지시를 무시" — 공식 명문화 |
| (2) 비대화 → 무시 | **D1** | "기술적 한계보다 훨씬 짧은 입력에서 이미 추론이 무너진다" — ACL 2024 학술 근거 |
| (3) 계층 충돌 | **A4** | "두 규칙이 충돌하면 모델은 임의로 하나를 고른다" — 공식 시인 |
| (3) 계층 충돌 | **C1** | 모노레포 충돌이 현실 문제라 `claudeMdExcludes`가 설정으로 만들어짐 |
| (3) 계층 충돌 | **D2** | "모델은 원래 출처가 다른 지시를 동급으로 본다" — OpenAI 연구 |

**강사 권장 인용 시퀀스 (한 호흡 30초)**:
> "Anthropic 공식 문서는 CLAUDE.md를 *다시 설명할 것을 적어두는 곳*이라고 정의합니다. 같은 문서가 *200줄을 넘기면 이미 길고, 비대해지면 진짜 지시를 무시한다*고 못 박습니다. ACL 2024 연구도 *기술적 한계 훨씬 전에 추론이 떨어진다*고 보여줍니다. 그리고 두 규칙이 충돌하면 — Anthropic 본인 말로 — *모델은 임의로 하나를 고릅니다*. 그래서 우리는 CLAUDE.md를 모든 컨텍스트의 창고가 아니라 *반복 지시 축소 장치*로 다뤄야 합니다."

---

## 6. 인용 시 유의사항 / 한계

1. **"비대한 CLAUDE.md로 인한 보도된 사고" 1차 출처 부재**:
   본 세션 명제를 가장 극적으로 뒷받침할 *고유명사 사고* (예: "X 회사가 비대한 CLAUDE.md 때문에 Y를 망쳤다")는 회사 공식 보도·공식 GitHub issue 수준에서 1차 확인되지 않았다. Reddit/Medium 일화나 트위터 사례는 본 자료의 채택 기준(공식 보도/공식 issue/학술)을 통과하지 못해 의도적으로 제외했다. 진행 순서 4번 "나쁜 규칙" 정당화는 사고 사례 대신 **A5(공식)와 D1(학술)의 조합**으로 가져간다.

2. **C1을 "사례"가 아니라 "공식 시인"으로 사용**:
   C1은 외부 사고 사례가 아니라 *Anthropic 본인이 공식 문서에서 인정한 현실 문제 + 그것을 막기 위해 설정 항목까지 만들었다*는 점이 핵심이다. "어떤 회사가 망했다" 식으로 인용하지 말 것.

3. **D1·D2 수치 인용 금지**:
   D1(Same Task, More Tokens)은 QA 추론 도메인, D2(Instruction Hierarchy)는 OpenAI 모델 기준이다. CLAUDE.md(코딩 지시문) 도메인에 *비례*로 일반화 금지. 정성 결론만 인용.

4. **Anthropic 자료 비중이 높음**:
   세션 주제가 *Claude Code 고유 기능* 인 CLAUDE.md라서 자료 8/11이 Anthropic 공식이다. 이는 자연스러우나, 진영 중립성을 위해 D2(OpenAI)와 D1(중립 학계)를 함께 인용해 *모델 일반의 한계*임을 보여줘야 한다.

5. **"전역" 용어 정합성**:
   본문 대본의 "전역 규칙"은 Anthropic 공식 용어로는 **User instructions (`~/.claude/CLAUDE.md`)** 에 해당. *Managed policy* 와 혼동하지 않도록 슬라이드에서 둘을 분리 표기 권장.

6. **`/init` 흐름 변경 가능성**:
   A1·A9에서 권장한 `/init` 명령은 `CLAUDE_CODE_NEW_INIT=1` 환경에서 multi-phase로 동작이 바뀐다. 강의 시연 환경에서 어떤 모드인지 미리 확인.

7. **번역 보존**:
   원문이 단정적인 곳(예: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!")은 한국어 번역에서도 단정 어조 유지. 의역으로 약화 금지.

---

## 7. 출처 일람 (URL 한 곳에 모음)

### 공식 가이드 (Anthropic)
- Claude Code Memory (CLAUDE.md / 계층 / 충돌 / compaction): https://code.claude.com/docs/en/memory
- Claude Code Best Practices (CLAUDE.md 작성·include/exclude·emphasis): https://code.claude.com/docs/en/best-practices

### 검증된 사례 / 표준 문서
- Anthropic 공식 시인: 모노레포 CLAUDE.md 충돌 → `claudeMdExcludes` 설정 (위 memory 페이지 §"Manage CLAUDE.md for large teams")

### 학술 / 업계 연구
- Same Task, More Tokens (Levy/Jacoby/Goldberg, ACL 2024, arXiv:2402.14848): https://arxiv.org/abs/2402.14848
- The Instruction Hierarchy (Wallace et al., OpenAI, arXiv:2404.13208): https://arxiv.org/abs/2404.13208

### 보조 (자체 연속성)
- 동일 시리즈 세션 2-1 근거 자료: [`02-01-what-why-how-evidence.md`](./02-01-what-why-how-evidence.md) — A8(CLAUDE.md 옮길 신호), A9(작성 규칙), A10(AGENTS.md 표준)이 본 세션 A2/A5/A8과 직접 연결됨
