# Part 2 용어집 (수강생용)

본 문서는 Part 2 강의 전반에 등장하는 용어를 다섯 그룹으로 정리한다. 도구별 의미가 다른 용어는 별도 그룹(④)으로 분리해 혼동을 막았다.

> 각 용어 옆 `[2-1]`, `[3-2]` 등은 처음 등장하는 세션 번호.

---

## ① Context Engineering 핵심 개념 (도구 무관)

### 제어면 (control surface) `[2-1]`
지시문이 단순한 글쓰기가 아니라 AI에게 **작업 범위와 위험 범위를 정해주는 인터페이스**라는 강의 명제. 모호한 지시문은 제어면이 되지 못한다.

### WHAT / WHY / HOW `[2-1]`
지시문을 *무엇을 / 왜 / 어떻게*로 구조화하는 강의 프레임. 검증 기준과 금지 사항을 추가하면 실무 지시문이 된다.

### 황금률 (Golden Rule) `[2-1]`
*"동료에게 보여서 헷갈리면 AI도 헷갈린다."* — Anthropic 공식 가이드의 권고.

### 검증 가능 지시문 (verifiable instruction) `[2-1]`
**기계가 자동으로 따랐는지 검사할 수 있는** 형태의 지시문. 예: "200단어 이하로 써라". IFEval(Google 2023)에서 정의·대중화.

### Silent Failure `[2-1]`
AI가 그럴듯한 결과를 만들지만 *실제로는 작동하지 않는* 현상. 검증 기준이 없으면 발견되지 않는다. 강의 시리즈의 핵심 위험 개념.

### 컨텍스트 로트 (context rot) `[3-1]`
컨텍스트 길이가 늘어날수록 모델 성능이 저하되는 현상. **Chroma 2025 보고서**가 18개 주요 모델로 입증.

### Lost in the Middle `[3-1]`
긴 컨텍스트의 **가운데**에 있는 정보를 모델이 흘리는 현상. 처음·끝은 잘 본다. **Stanford 2023 (Liu et al., arXiv:2307.03172)** 연구에서 정의.

### 핸드오프 노트 (handoff note) `[3-1]`
긴 대화를 다음 세션으로 넘기기 위한 요약. 6개 항목: *목표 / 완료 / 남은 작업 / 결정 / 제약 / 검증 / 다음 첫 프롬프트.*

### 손실 압축 (lossy compaction) `[3-2]`
`/compact` 같은 요약 기능이 *정보 일부를 잃는* 성질. Anthropic이 공식 문서에서 *"tool outputs are gone"* 으로 인정.

### 4계층 컨텍스트 모델 `[3-3]`
정보를 (① 즉시 프롬프트 / ② 세션 핸드오프 / ③ 프로젝트 문서 / ④ 외부 공식 문서) 네 계층으로 나누는 강의 프레임. *정보의 성격*에 따라 위치 결정.

### closest-precedence `[2-3]`
하위 폴더의 규칙이 상위 폴더 규칙을 *덮는* 우선순위 원칙. 깊을수록 더 구체적.

---

## ② Claude Code 전용 용어

### CLAUDE.md `[2-2]`
Claude Code가 매 세션 자동 참고하는 프로젝트 메모리 파일. **계층**: 전역(`~/.claude/CLAUDE.md`) → 프로젝트(`./CLAUDE.md`) → 하위 폴더(`./subdir/CLAUDE.md`). 권장 분량 200줄 / 25KB 이내.
1차: [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)

### `/compact` `[3-2]`
현재 대화를 요약해서 이어가는 슬래시 명령. *원본 tool output과 중간 추론은 사라진다.*

### `/clear` (Claude Code) `[3-2]`
**새 대화 시작.** Codex의 `/clear`와 의미가 다르므로 주의.

### `/resume` `[3-2]`
이전 대화 다시 열기. 모든 맥락이 완벽 복원되지는 *않는다.*

### `/memory` `[3-2]`
저장된 사용자/프로젝트 정보 관리. 권장 200줄 / 25KB cap.

### `/fork` `[3-2]`
세션 분기 명령. `CLAUDE_CODE_FORK_SUBAGENT` 환경변수에 따라 동작 달라짐 — 촬영/실습 당일 확인 필요.

### Plan Mode `[2-4]`
변경 *전에* 계획을 사람에게 보여주는 모드. 진단자 패턴의 도구화.

### Skills `[3-3]`
반복 패턴을 코드화한 재사용 가능한 모듈. 4계층 중 ③ 프로젝트 문서의 한 형태.

### claudeMdExcludes `[2-2]`
모노레포 등에서 특정 `CLAUDE.md`를 *제외*하는 설정. 계층 충돌 방지용.

### Prompt Improver `[2-4]`
Anthropic Console 기능. 프롬프트를 자동 진단하고 개선안을 제안.

---

## ③ Codex 전용 용어

### AGENTS.md `[2-3]`
여러 에이전트 도구가 공통으로 읽도록 만든 **오픈 표준 파일**. 그러나 도구별 해석은 같지 않다 (Claude Code는 직접 안 읽음).
1차 (표준): [agents.md](https://agents.md/) / 1차 (Codex): [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)

### AGENTS.override.md `[2-3]`
Codex가 `AGENTS.md`를 *부분 덮어쓸* 때 쓰는 보조 파일. agents.md 표준엔 없는 Codex 고유 의미론.

### codex resume `[3-2]`
Codex의 세션 재개 명령. Claude Code의 `/resume`과 유사하나 동작 차이 가능.

### root → current concatenate `[2-3]`
Codex가 `AGENTS.md`를 **루트부터 현재 폴더 순서로 이어붙이는** 방식. 32KiB cap.

### `/clear` (Codex) `[3-2]`
**터미널 화면 정리** (대화는 유지). Claude Code의 `/clear`와 정반대 의미.

---

## ④ 두 도구에 모두 있지만 의미가 다른 용어 (혼동 주의!)

### `/clear`
| 도구 | 의미 |
|---|---|
| Claude Code | 새 대화 시작 (대화 삭제) |
| Codex | 터미널 화면만 정리 (대화 유지) |

### `/compact`
- 양쪽 모두 존재.
- **공통**: 요약 = 손실.
- **차이**: 동작 세부(무엇을 보존/삭제하는지)는 도구·버전마다 다름. 촬영/실습 당일 `/help`로 확인.

### memory / 메모리
- Claude Code: `/memory` 명령 + `CLAUDE.md` 시스템.
- Codex: 별도 메커니즘. 단순 동등 비교 금지.

---

## ⑤ 학술/연구 핵심 개념 (강사가 카메라 앞에서 인용 가능)

### IFEval `[2-1]`
**Instruction-Following Evaluation.** 지시문을 *기계가 자동 검증 가능한 형태*로 만든 벤치마크. **Google 2023, arXiv:2311.07911.** "verifiable instructions" 용어를 대중화.

### FollowBench `[2-1, 2-4]`
제약을 한 줄씩 누적했을 때 모델 성공률이 *계단처럼 떨어지는* 현상을 측정. **HKUST·Huawei, ACL 2024, arXiv:2310.20410.**

### Plan-and-Solve Prompting `[2-1]`
*"먼저 계획, 그다음 실행"* 으로 두 단계 분해 지시. 누락 단계가 줄어든다. **SMU, ACL 2023, arXiv:2305.04091.**

### Self-Refine `[2-4]`
LLM이 자기 출력을 비판하고 다시 쓰는 패턴. **단, 외부 신호 없으면 효과 제한적.** arXiv:2303.17651.

### LLMs Cannot Self-Correct `[2-4]`
Self-Refine의 한계를 보여주는 후속 연구. 외부 신호(=사람·테스트)가 없으면 자기 교정은 잘 안 된다. arXiv:2310.01798.

### LLM-as-Judge `[2-4]`
LLM에게 다른 LLM 출력을 평가시키는 방법. **self-enhancement bias** — 자기 출력에 후함. arXiv:2306.05685.

### Reflexion `[2-4]`
LLM이 *외부 피드백*을 받아 자기 시도를 개선하는 프레임워크. arXiv:2303.11366.

### Needle in a Haystack (NIAH) `[3-1]`
긴 컨텍스트 어딘가에 묻힌 *바늘*(특정 정보)을 모델이 찾을 수 있는지 평가. [github.com/gkamradt/LLMTest_NeedleInAHaystack](https://github.com/gkamradt/LLMTest_NeedleInAHaystack).

### LongBench / RULER `[3-1]`
긴 컨텍스트 처리 능력을 측정하는 벤치마크 모음.

### RAG (Retrieval-Augmented Generation) `[3-3]`
외부 인덱스에서 정보를 가져와 모델에 주입하는 패턴. **arXiv:2005.11401 (원논문).** 컨텍스트 분리의 자동화 사례 중 하나로 이해할 수 있다.

### Context Engineering `[3-3]`
프롬프트 엔지니어링의 확장 개념. *"무엇을 / 어디에 / 언제* 모델에 주입할 것인가"의 설계. **Anthropic Engineering 블로그**가 표준화된 용어로 사용.

### "Same Task, More Tokens" `[2-2]`
입력 길이가 늘어날수록 *추론 정확도가 저하*되는 현상을 보여주는 연구. system prompt 비대화 회피의 학술 근거.

### Instruction Hierarchy `[2-2]`
OpenAI가 정의한 명령 우선순위 체계. system / developer / user 메시지의 가중치 차등.

---

## 용어집 사용 팁

- 강의 영상 보다가 *모르는 용어*가 나오면 여기서 검색 (Cmd+F / Ctrl+F).
- 용어 옆 `[X-Y]`는 처음 등장하는 세션 — 그 한 장 정리(`handout/0X-0Y-handout.md`)에서 *맥락*을 다시 본다.
- *왜* 그 용어가 중요한지(1차 출처)는 `research/0X-0Y-*-evidence.md`에 있다.
- 도구별 의미가 다른 용어(④ 그룹)는 *외울 가치가 가장 큰* 것들이다 — 두 도구를 함께 쓰는 사람이 가장 많이 사고를 낸다.
