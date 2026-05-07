# Session 2-3 강사용 근거 자료

본문 대본: [`part2/02-03-agents-md.md`](../../part2/02-03-agents-md.md)
형식 기준: [`part2/research/02-01-what-why-how-evidence.md`](./02-01-what-why-how-evidence.md)
자료 작성일: 2026-04-30 / 검증 기준일: 2026-04-30 (모든 URL은 `curl -L -o /dev/null -w '%{http_code}'`로 200 OK 확인)

이 문서는 강의 진행 시 카메라 앞에서 인용할 수 있는 1차 자료(공식 가이드/표준·공개 저장소 사례·관련 연구)를 모은 것이다. 본 세션은 학술 연구가 직접 매칭되는 영역이 *적은* 주제이므로, 분량을 강제로 늘리지 않고 정직하게 표시했다.

---

## 0. 강의 핵심 명제 (이 자료가 뒷받침하는 단 하나의 주장)

> **"AGENTS.md는 오픈 표준이지만, Claude Code와 Codex가 그것을 *완전히 동일하게* 처리하지는 않는다. 도구를 1:1 대응시키지 말고, 공통 규칙은 `AGENTS.md` / 도구 전용 운영 팁은 별도 파일(`CLAUDE.md` 등)로 분리한다. 하위 폴더 `AGENTS.md`가 더 구체적인 규칙을 담을 수 있다."**

이 명제에 직접 대응하는 자료는 **★** 표시로 강조했다. 핵심 증거 두 가지를 미리 적어둔다:

- ★ Claude Code 공식 문서는 *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`"* 라고 **명시**한다(자료 A3).
- ★ OpenAI Codex 공식 문서는 *"Codex reads `AGENTS.md` files before doing any work"* 라고 **명시**한다(자료 A2).
- 둘은 같은 문제를 풀지만, **읽는 파일과 병합 규칙이 다르다.**

---

## 1. 진행 순서 ↔ 자료 매칭 매트릭스 (먼저 한 번 보고 들어가는 표)

| 본문 진행 순서 | 공식 가이드/표준 | 검증된 사례 | 학술/업계 연구 |
|---|---|---|---|
| 1. AGENTS.md 역할 정의 | A1 agents.md 표준, A2 Codex 공식, ★A3 Claude Code 공식 | B1 openai/codex 루트 AGENTS.md | — |
| 2. CLAUDE.md ↔ AGENTS.md 관계 | ★A3 Claude Code 공식("reads CLAUDE.md, not AGENTS.md"), A4 import 패턴 | — | — |
| 3. 좋은 AGENTS.md 목차 | A1 agents.md 권장 섹션, A2 Codex 권장 사용처, A5 검증 가능성 | B1 openai/codex 루트 AGENTS.md(실제 목차) | — |
| 4. 하위 폴더 규칙 | ★A1 "closest takes precedence", ★A2 Codex 병합 순서 | ★B2 codex-rs/tui/.../AGENTS.md(루트보다 좁은 범위) | — |
| 5. 공통 지시문 교차 검토 | ★A3 Claude Code의 권장 import 패턴, A6 specificity 가이드 | — | C1 IFEval(검증 가능 지시문) |

★ = "도구마다 처리 방식이 다르다 / 공통 vs 전용을 분리하라" 명제 직결 자료

---

## 2. 공식 가이드 / 표준 (A1~A6)

### A1. agents.md 오픈 표준 — "에이전트를 위한 README"

**출처**: agents.md (오픈 표준 사이트)
**URL**: https://agents.md/
**확인일**: 2026-04-30 (HTTP 200)

**원문 (영어)**:
> "A simple, open format for guiding coding agents, used by over 60k open-source projects."
>
> "Think of AGENTS.md as a README for agents: a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project."
>
> "Why not just put this in README? ... README.md files are for humans: quick starts, project descriptions, and contribution guidelines. AGENTS.md complements this by containing the extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README or aren't relevant to human contributors."
>
> *(Monorepos)* "place another AGENTS.md inside each package. Agents automatically read the nearest file in the directory tree, so the closest one takes precedence."

**한국어 (60자 이내)**:
> "에이전트용 README. 가까운 파일이 우선한다."

**세션 내 사용 위치**: 진행 순서 1번(역할 정의), 3번(목차), 4번(하위 폴더 우선순위)

**왜 중요한가**: 표준이 *어떤 한 회사의 자체 규약*이 아니라, 60k+ 저장소가 채택한 공개 포맷이라는 객관적 사실. 다만 **표준이 강제하는 의미론은 매우 얇고**, 도구별 해석 차이는 표준 외부에서 결정된다 — 이게 본 세션의 핵심.

---

### A2. ★ OpenAI Codex 공식 문서 — AGENTS.md 병합 순서

**출처**: OpenAI Codex Documentation, "AGENTS.md"
**URL**: https://developers.openai.com/codex/guides/agents-md
**확인일**: 2026-04-30 (HTTP 200)

**원문 (영어)**:
> "Codex reads `AGENTS.md` files before doing any work. By layering global guidance with project-specific overrides, you can start each task with consistent expectations, no matter which repository you open."
>
> *(Global scope)* "In your Codex home directory (defaults to `~/.codex`, unless you set `CODEX_HOME`), Codex reads `AGENTS.override.md` if it exists. Otherwise, Codex reads `AGENTS.md`."
>
> *(Project scope)* "Starting at the project root (typically the Git root), Codex walks down to your current working directory ... In each directory along the path, it checks for `AGENTS.override.md`, then `AGENTS.md`."
>
> *(Merge order)* "Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later."
>
> "Codex stops searching once it reaches your current directory, so place overrides as close to specialized work as possible."

**한국어 (60자 이내)**:
> "Codex는 루트→현재 폴더 순으로 AGENTS.md를 이어 붙인다."

**세션 내 사용 위치**: 진행 순서 1번(역할), 3번(목차), 4번(하위 폴더 — *가장 직접적인 근거*)

**왜 중요한가**: Codex가 `AGENTS.override.md`라는 별도 파일까지 인식한다는 사실은 agents.md 표준 원문에는 없다. **표준은 같은데 도구별 의미론이 더해진다**는 본 세션 명제의 직접 증거.

---

### A3. ★ Claude Code 공식 문서 — "Claude Code reads CLAUDE.md, not AGENTS.md"

**출처**: Anthropic Claude Code — Memory ("How Claude remembers your project"), 섹션 "AGENTS.md"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30 (HTTP 200)

**원문 (영어)** *(섹션 「AGENTS.md」 통째 인용)*:
> "Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repository already uses `AGENTS.md` for other coding agents, create a `CLAUDE.md` that imports it so both tools read the same instructions without duplicating them. You can also add Claude-specific instructions below the import. Claude loads the imported file at session start, then appends the rest:"
>
> ```markdown CLAUDE.md
> @AGENTS.md
>
> ## Claude Code
>
> Use plan mode for changes under `src/billing/`.
> ```

**한국어 (60자 이내)**:
> "Claude Code는 AGENTS.md가 아니라 CLAUDE.md를 읽는다. import로 연결하라."

**세션 내 사용 위치**: 진행 순서 2번 (CLAUDE.md ↔ AGENTS.md 관계 — **이 한 줄이 본 세션 명제의 가장 직접적 증거**), 5번(교차 검토 권장 패턴)

**왜 중요한가**: 카메라 앞에서 단정적으로 인용 가능한 *유일한* 1차 출처. "Anthropic 공식 문서는 Claude Code가 AGENTS.md를 *직접* 읽지는 않는다고 명시한다 — 그래서 import 한 줄로 연결한다"는 것이 본 세션의 핵심 메시지를 그대로 만든다.

---

### A4. Claude Code의 import 메커니즘 — `@path` 한 줄로 AGENTS.md 흡수

**출처**: Anthropic Claude Code — Memory, 섹션 "Import additional files"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30 (HTTP 200)

**원문 (영어)**:
> "CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them."
>
> "Both relative and absolute paths are allowed. ... Imported files can recursively import other files, with a maximum depth of five hops."

**한국어 (60자 이내)**:
> "CLAUDE.md는 @경로 한 줄로 다른 파일을 시작 시 흡수한다."

**세션 내 사용 위치**: 진행 순서 2번 (공통 규칙=AGENTS.md / Claude 전용=CLAUDE.md 분리 권장 패턴의 *기술적 근거*)

---

### A5. 검증 가능한 구체성 — "코드 정리하기" 말고 "2칸 들여쓰기"

**출처**: Anthropic Claude Code — Memory, 섹션 "Write effective instructions / Specificity"
**URL**: https://code.claude.com/docs/en/memory
**확인일**: 2026-04-30 (HTTP 200)

**원문 (영어)**:
> "Specific, concise, well-structured instructions work best."
>
> "**Specificity**: write instructions that are concrete enough to verify. For example:
> - 'Use 2-space indentation' instead of 'Format code properly'
> - 'Run `npm test` before committing' instead of 'Test your changes'
> - 'API handlers live in `src/api/handlers/`' instead of 'Keep files organized'"
>
> "**Size**: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."

**한국어 (60자 이내)**:
> "검증 가능할 만큼 구체적으로, 200줄 안으로."

**세션 내 사용 위치**: 진행 순서 3번(목차 작성 시 항목별 구체화 기준), 5번(교차 검토 시 너무 모호한 규칙 제거)

---

### A6. Claude Code Best Practices — CLAUDE.md 작성 원칙

**출처**: Anthropic Claude Code — Best Practices
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30 (HTTP 200)

**원문 (영어)** *(02-01 evidence A9에서 인용된 동일 출처)*:
> "Keep it concise. For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

**한국어 (60자 이내)**:
> "비대해지면 무시당한다. 한 줄씩 '필요한가?'를 물어라."

**세션 내 사용 위치**: 진행 순서 3번(목차 슬림화), 5번(교차 검토에서 "너무 강한 규칙이 정상 작업을 막는지" 점검 기준)

---

## 3. 검증된 사례 (B1~B2)

> 본 섹션은 *공개 저장소의 실제 AGENTS.md*를 1차 자료로 인용한다. AGENTS.md 작성 사고나 도구 간 해석 충돌 사례는 본 리서치 시점에 1차 출처(공식 issue/공식 보도)로 확인된 것이 매우 적었다 — 정직하게 표시한다(6장 참고).

### B1. openai/codex 저장소의 루트 AGENTS.md — "공통 규칙"의 실제 모습

**출처**: GitHub openai/codex, 루트 `AGENTS.md`
**URL**: https://github.com/openai/codex/blob/main/AGENTS.md (raw: https://raw.githubusercontent.com/openai/codex/main/AGENTS.md)
**확인일**: 2026-04-30 (HTTP 200)

**원문 (영어, 도입부 그대로)**:
> "# Rust/codex-rs
>
> In the codex-rs folder where the rust code lives:
>
> - Crate names are prefixed with `codex-`. For example, the `core` folder's crate is named `codex-core`
> - When using format! and you can inline variables into {}, always do that.
> - Install any commands the repo relies on (for example `just`, `rg`, or `cargo-insta`) if they aren't already available before running instructions here.
> - Never add or modify any code related to `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR` or `CODEX_SANDBOX_ENV_VAR`."

실제 섹션 구성: Rust 컨벤션 → TUI style → TUI code → ratatui 사용법 → text wrapping → tests(snapshot/assertions/integration) → app-server API.

**한국어 (60자 이내)**:
> "OpenAI 자신이 쓰는 AGENTS.md는 빌드/스타일/테스트/금지 영역으로 구성된다."

**세션 내 사용 위치**: 진행 순서 1번(역할 정의 — *AGENTS.md를 만드는 곳이 직접 쓰는 모습*), 3번(목차 예시), 본문 산출물의 「Project Overview/Commands/Working Rules/Do Not」 정당화

**왜 중요한가**: agents.md 표준 사이트가 권장하는 섹션 구성과, 본문 산출물 템플릿이 **OpenAI 자신의 AGENTS.md**에서도 동일한 골격으로 나타난다는 객관 증거.

---

### B2. ★ openai/codex의 *나중에* 등장하는 nested AGENTS.md — 더 깊을수록 더 좁다

**출처**: GitHub openai/codex, `codex-rs/tui/src/bottom_pane/AGENTS.md`
**URL**: https://raw.githubusercontent.com/openai/codex/main/codex-rs/tui/src/bottom_pane/AGENTS.md
**확인일**: 2026-04-30 (HTTP 200)

(같은 저장소에 `codex-rs/thread-store/src/remote/AGENTS.md`도 존재 — 둘 다 GitHub Tree API로 확인. 즉 openai/codex는 루트 + nested 2개 = 최소 3개의 AGENTS.md를 운용 중.)

**원문 (영어, 전문 인용)**:
> "# TUI bottom pane (state machines)
>
> When changing the paste-burst or chat-composer state machines in this folder, keep the docs in sync:
>
> - Update the relevant module docs (`chat_composer.rs` and/or `paste_burst.rs`) so they remain a readable, top-down explanation of the current behavior.
> - Update the narrative doc `docs/tui-chat-composer.md` whenever behavior/assumptions change ...
> - Keep implementations/docstrings aligned unless a divergence is intentional and documented."

**한국어 (60자 이내)**:
> "하위 폴더 AGENTS.md는 그 폴더 한정의 *훨씬 좁은* 규칙만 담는다."

**세션 내 사용 위치**: 진행 순서 4번 (하위 폴더 규칙 설계 — *루트는 전체 공통 / 하위는 그 폴더 한정*이라는 본문 메시지의 *실제 작동 사례*)

**왜 중요한가**: 본문 4번이 추상적으로 말한 "더 깊은 AGENTS.md가 더 구체적인 규칙을 담을 수 있다"가, 본 표준을 *만든 회사*의 저장소에서 **실제로 그렇게 운용되고 있음**을 보여주는 1차 증거. 게다가 이 nested 파일은 빌드/테스트 같은 루트 공통 규칙을 *반복하지 않는다* — "공통 vs 전용 분리"의 모범 사례.

---

## 4. 학술 / 업계 연구 (C1)

> 본 세션 주제(tool-agnostic instructions, multi-agent shared specifications)에 *직접* 매칭되는 학술 연구는 본 리서치 시점에 1차 출처로 충분히 확보되지 않았다. 분량을 늘리기 위해 약한 매칭을 끼워 넣지 않고, **간접 매칭 1건만** 수록한다.

### C1. IFEval — 지시문이 검증 가능할 때만 도구 간 비교가 가능하다

**저자/발표**: Jeffrey Zhou et al. (Google), arXiv:2311.07911, 2023-11
**URL**: https://arxiv.org/abs/2311.07911
**확인일**: 2026-04-30 (02-01 evidence D1과 동일 출처 재사용)

**한 줄 핵심**:
> "지시문이 *기계가 자동 검사 가능한* 형태일 때만, 모델·도구가 그 지시를 따랐는지 객관 측정할 수 있다."

**본 세션과의 연결**: 진행 순서 5번이 "같은 작업을 Claude Code와 Codex에 시켜 계획이 비슷하게 나오는지 본다"고 말한다. 이 *교차 검토*가 자의적 인상이 아니라 객관 비교가 되려면, AGENTS.md의 항목이 IFEval 식 *verifiable* 형태로 적혀 있어야 한다(예: "테스트 명령은 `pnpm test`" 식). 본 세션의 5번 항목이 의미를 가지려면 3번에서 검증 가능한 형태로 작성되어 있어야 한다는 정당화.

**한국어 (60자 이내)**:
> "검증 가능한 형식이어야 도구 간 객관 비교가 성립한다."

**세션 내 사용 위치**: 진행 순서 5번(교차 검토 정당화), 3번(목차 작성 시 항목 형식)

**한계 명시**: IFEval은 일반 instruction-following 벤치마크이며 *코드 에이전트의 AGENTS.md 준수율*을 직접 측정하지 않는다. 정성 결론(*경향성*)만 인용 가능.

---

## 5. ★ "도구마다 처리 방식이 다르다" 명제 직결 모음

> 강의 명제를 단정적으로 말할 때 한 호흡에 인용하기 좋은 자료를 한 표에 모았다.

| 자료 | 한 줄 요지 |
|---|---|
| **A1** agents.md 표준 | "Agents automatically read the nearest file ... the closest one takes precedence." — 표준의 의미론은 *얇다*(가까운 파일 우선만 명시) |
| **A2** Codex 공식 | Codex는 `AGENTS.override.md`까지 인식하고 *루트→하위* 순서로 *concatenate*한다 — 표준 위에 도구 고유 규칙이 얹힘 |
| **A3** Claude Code 공식 | "Claude Code reads `CLAUDE.md`, not `AGENTS.md`." — *완전히 동일하지 않다*는 가장 직접적 1차 증거 |
| **A4** Claude Code import | `@AGENTS.md` 한 줄로 둘을 연결하는 *공식 권장 패턴* — 본 세션 산출물의 골격 |
| **B2** openai/codex nested | "TUI bottom pane (state machines)" — 같은 저장소의 nested AGENTS.md가 *훨씬 좁은 범위*만 담는 모범 사례 |

**강사 권장 인용 시퀀스 (한 호흡 25초)**:
> "AGENTS.md는 60k 이상 저장소가 채택한 오픈 표준입니다. 그런데 표준이 의미하는 건 의외로 얇아요 — '가까운 파일이 우선한다' 정도입니다. OpenAI Codex 공식 문서는 *루트에서 현재 폴더까지 이어 붙이고, `AGENTS.override.md`도 인식한다*고 따로 명시합니다. 반면 Anthropic Claude Code 공식 문서는 한 줄을 박아두었습니다 — *Claude Code는 AGENTS.md가 아니라 CLAUDE.md를 읽는다.* 그래서 권장 패턴은, 공통 규칙은 AGENTS.md에 두고, CLAUDE.md는 그것을 `@AGENTS.md` 한 줄로 import한 다음 Claude 전용 팁만 아래에 붙이는 겁니다."

---

## 6. 인용 시 유의사항 / 한계

1. **학술 연구 매칭 빈약 — 정직하게 표시**: 본 세션의 핵심(tool-agnostic 공통 지시문, 다중 에이전트 공유 스펙)은 *학술 연구 주제로는 너무 신생*이다. IFEval(C1)을 간접 매칭으로만 인용했고, 분량을 늘리려고 약한 연구를 끼워 넣지 않았다.

2. **도구 간 해석 차이 사례의 1차 출처 부족**: "AGENTS.md를 두 도구가 다르게 해석해 사고가 났다"는 *재현 가능한* 공식 issue를 본 리서치 시점에 1건도 확정하지 못했다. 본 자료는 대신 **공식 문서의 명시적 차이**(A2 vs A3)를 1차 증거로 사용한다.

3. **표준 사이트의 "60k 저장소" 수치**: agents.md 자체 발표값이며 독립 검증된 수치가 아니다. 카메라 인용 시 *"표준 사이트 자체 발표 기준"*을 붙일 것.

4. **도구를 1:1 대응시키지 말 것**: A2와 A3은 *같은 표준을 다르게 해석한다*. 강의에서 "Claude Code = Codex"라고 단정하면 이 자료들과 정면 충돌. 항상 "공통 부분과 도구별 차이"로 분리해 말할 것.

5. **트위터/익명 출처 제외**: 본 자료는 (a) 표준 사이트 (b) 공식 도구 문서 (c) 공개 저장소의 실제 파일 (d) arXiv 등록 논문만 사용했다.

6. **본문 산출물 템플릿의 위치**: 본문이 제시하는 `Project Overview / Commands / Working Rules / Do Not` 골격은 agents.md 표준 권장 섹션(A1)과 OpenAI 자신의 AGENTS.md(B1)에서 모두 관찰된다 — 이건 임의 선택이 아니라 *수렴된 관행*이라고 말해도 무방.

---

## 7. 출처 일람 (URL 한 곳에 모음 — 모두 2026-04-30 200 OK 확인)

### 공식 가이드 / 표준
- agents.md 오픈 표준: https://agents.md/
- OpenAI Codex AGENTS.md 공식: https://developers.openai.com/codex/guides/agents-md
- Anthropic Claude Code Memory(섹션 "AGENTS.md", "Import additional files", "Specificity"): https://code.claude.com/docs/en/memory
- Anthropic Claude Code Best Practices: https://code.claude.com/docs/en/best-practices

### 검증된 사례 (공개 저장소의 실제 AGENTS.md)
- openai/codex 루트 AGENTS.md: https://github.com/openai/codex/blob/main/AGENTS.md
- openai/codex nested(좁은 범위 예시): https://raw.githubusercontent.com/openai/codex/main/codex-rs/tui/src/bottom_pane/AGENTS.md
- openai/codex nested(추가 1건): https://raw.githubusercontent.com/openai/codex/main/codex-rs/thread-store/src/remote/AGENTS.md

### 학술 연구
- IFEval (arXiv:2311.07911) — 간접 매칭: https://arxiv.org/abs/2311.07911
