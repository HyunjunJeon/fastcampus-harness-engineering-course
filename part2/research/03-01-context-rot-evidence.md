# Session 3-1 강사용 근거 자료

본문 대본: [`part2/03-01-context-rot-new-session.md`](../../part2/03-01-context-rot-new-session.md)
형식 참고: [`part2/research/02-01-what-why-how-evidence.md`](./02-01-what-why-how-evidence.md)
자료 작성일: 2026-04-30 / 검증 기준일: 2026-04-30

이 문서는 강의 진행 시 카메라 앞에서 한두 줄 단정적으로 인용할 수 있는 1차 자료(공식 가이드·검증된 사고 사례·공개 학술 연구) 모음이다. **본문 대본을 부풀리지 않기 위해 따로 분리**했다.

> 청자가 비개발자라는 점을 고려해, 학술 자료의 *수치*는 인용하지 않고 *정성 결론*만 사용한다. 강사가 "연구에 따르면…"이라고 단정할 수 있는 한국어 한 줄을 각 자료 끝에 명시했다.

---

## 0. 강의 핵심 명제 (이 자료가 뒷받침하는 단 하나의 주장)

> **"긴 대화가 망가지는 것은 *도구의 결함*이 아니라 *컨텍스트 관리 실패*다. 모델은 길이가 늘어날수록 중간 정보를 잊고, 오래된 전제를 반복하고, 새 결정을 놓친다. 이 현상은 잘 알려진 메커니즘(lost-in-the-middle, attention degradation, context rot)으로 측정 가능하다."**

이 명제에 직접 대응하는 자료는 본문에서 **★** 표시로 강조했다.

---

## 1. 진행 순서 ↔ 자료 매칭 매트릭스 (먼저 한 번 보고 들어가는 표)

| 본문 진행 순서 | 1차 자료 (공식 가이드) | 사고/사례 | 학술·업계 연구 |
|---|---|---|---|
| 1. 긴 대화가 망가지는 증상 | A1 Anthropic context window 경고, A2 effective context engineering | C1 Anthropic Claudius 정체성 혼란 | ★D1 Lost in the Middle, ★D2 Context Rot (Chroma), D3 Needle in a Haystack |
| 2. 컨텍스트 구성 요소 | A1, A2, ★A3 OpenAI Responses API | — | D1, ★D2 |
| 3. 새 세션 신호 | ★A1 "context fills up, performance degrades", A2 compaction/note-taking/sub-agents | C1 long-context에서 정체성 손실 | ★D2 Context Rot, D4 LongBench |
| 4. 선택지 비교 (계속/압축/새 세션/문서 분리) | ★A1 `/clear`·`/compact` 가이드, A2 3대 기법 | — | ★D2, D5 RULER |
| 5. 핸드오프 노트 | A1 "fresh session has clean context", A2 structured note-taking | — | — |

★ = "긴 대화 = 컨텍스트 관리 실패" 명제 직결 자료

---

## 2. Anthropic / OpenAI 공식 가이드 (A1~A3)

### A1. ★ Anthropic Claude Code Best Practices — "context fills up, performance degrades"

**출처**: Anthropic Claude Code — Best Practices, "Manage context aggressively"
**URL**: https://code.claude.com/docs/en/best-practices
**확인일**: 2026-04-30

**원문 (영어)**:
> "Most best practices are based on one constraint: Claude's context window fills up fast, and **performance degrades as it fills**."
>
> "When the context window is getting full, Claude may start 'forgetting' earlier instructions or making more mistakes. The context window is the most important resource to manage."
>
> "Use `/clear` frequently between tasks to reset the context window entirely... A clean session with a better prompt almost always outperforms a long session with accumulated corrections."
>
> "**The kitchen sink session.** You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information. Fix: `/clear` between unrelated tasks."

**한국어 (카메라 인용용)**:
> "Anthropic 공식 가이드는 *컨텍스트 창이 채워질수록 성능이 떨어진다*고 명시합니다. 이전 지시를 잊거나 실수가 늘기 시작합니다. 그래서 무관한 작업 사이에는 `/clear`로 세션을 비우는 게 *긴 세션에 누적된 수정보다 거의 항상 낫다*고 권장합니다."

**세션 내 사용 위치**: 진행 순서 1번(증상의 정당화), 3번(새 세션 신호), 4번(선택지 비교) — **본 세션 핵심 인용 ★**

**한계**: Claude Code 한정 권고이지만, 같은 원리(transformer attention)가 다른 챗 인터페이스에도 적용된다는 점은 D2 Context Rot에서 멀티 벤더로 검증됨.

---

### A2. ★ Anthropic — Effective Context Engineering for AI Agents (context rot 공식 인정)

**출처**: Anthropic Engineering Blog, "Effective Context Engineering for AI Agents", 2025-09-29
**URL**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**확인일**: 2026-04-30

**원문 (영어)**:
> "Context is a finite resource with diminishing marginal returns."
>
> "As the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases. ... This degradation stems from the transformer architecture's n² pairwise token relationships becoming stretched thin at scale."
>
> Anthropic이 권장하는 long-horizon 3대 기법:
> 1. **Compaction** — 대화 이력을 요약하고 압축된 컨텍스트로 새로 시작 ("architectural decisions, unresolved bugs, and implementation details" 보존)
> 2. **Structured note-taking** — 컨텍스트 창 *바깥에* 영구 메모리 파일을 두어 리셋 후에도 연속성 유지
> 3. **Sub-agent architectures** — 전용 에이전트가 좁은 작업을 수행한 뒤 *요약*만 돌려보냄

**한국어 (카메라 인용용)**:
> "Anthropic이 직접 *컨텍스트 토큰이 많아질수록 모델이 정확히 기억해내는 능력이 떨어진다*고 인정했습니다 — 트랜스포머의 토큰 간 관계가 길이가 늘수록 *얇게 펴지기* 때문입니다. 그래서 권장되는 길게 끌고 가는 방법은 세 가지예요. 압축, 외부 노트, 그리고 서브에이전트."

**세션 내 사용 위치**: 진행 순서 1번(왜 그런가), 4번(압축/새 세션/문서 분리 — 정확히 본문 4개 선택지와 매핑), 5번(노트 = 핸드오프) — **본 세션 핵심 인용 ★**

**왜 중요한가**: 본 세션의 4가지 선택지(계속·압축·새 세션·문서 분리)가 *Anthropic 공식 권고와 1:1로 대응*된다는 것을 보여주는 단일 자료.

---

### A3. ★ OpenAI GPT-5 Prompting Guide — Responses API & 에이전트 eagerness 제어

**출처**: OpenAI Cookbook — GPT-5 Prompting Guide, "Controlling Agentic Eagerness" / "Context Management"
**URL**: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
**확인일**: 2026-04-30

**원문 (영어)**:
> "Use the Responses API with `previous_response_id` to pass back previous reasoning items into subsequent requests. This allows the model to refer to its previous reasoning traces, conserving CoT tokens and eliminating the need to reconstruct a plan from scratch after each tool call."
>
> "Define clear criteria in your prompt for how you want the model to explore the problem space. ... Set fixed tool call budgets, like an absolute maximum of 2 tool calls."

**한국어**:
> "OpenAI도 별개 진영에서 같은 결론을 냅니다. *이전 추론을 매번 재구성하지 않게* 별도 API로 넘기고, *탐색 예산을 명시*해서 컨텍스트가 무한히 부풀지 않도록 통제하라는 것입니다."

**세션 내 사용 위치**: 진행 순서 2번(컨텍스트 구성 요소 — "이전 대화 요약"이 *왜* 필요한지), 3번(새 세션 신호 정당화)

**왜 중요한가**: 본 세션이 Anthropic만 인용한다는 인상을 피하면서 *진영 중립적*으로 동일 결론을 강화.

---

## 3. 검증된 사고/사례 (C1)

> 본 세션은 학술 자료가 강한 영역이라 사고 사례는 *직결되는 한 건*만 둔다. 트위터·익명 미디엄 글은 의도적으로 제외했다.

### C1. Anthropic 자체 사례 — Claudius (Project Vend) 장기 컨텍스트 정체성 손실

**한 줄 요약 (강사 인용용)**:
> "Anthropic이 직접 운영한 'Claudius' 사내 vending shop 실험에서, 장기 운영을 견디지 못한 에이전트가 *자신을 사람으로 착각*하고 보안팀에 신고하기까지 했습니다. Anthropic은 사후 분석에서 'inadequate constraints'와 'scaffolding gaps'를 원인으로 지목했습니다."

**무슨 일**: Anthropic 사내 자율 운영 에이전트 Claudius가 *길어진 컨텍스트*에서 정체성 혼란을 일으킴. 존재하지 않는 사람과 대화 환각, 심슨가족 가상 주소를 방문했다고 주장, 옷을 입고 직접 배달하는 인간이라고 믿음, 정체성 지적을 받자 보안팀에 연락 시도.

**본 세션 명제와의 연결**: "긴 대화에서 모델이 *오래된 전제를 반복하고 새 결정을 놓친다*"는 본문 1번 증상의 직접 사례. 도구 결함이 아니라 *컨텍스트 관리 실패*였다는 점을 Anthropic 자신이 명시.

**출처**: https://www.anthropic.com/research/project-vend-1
**발생 시점**: 2025-03-31 ~ 04-01

**세션 내 사용 위치**: 진행 순서 1번 — *Anthropic 자신의 사례*라 한국 수강생 신뢰성 매우 높음

**한계**: 이 사례 자체는 컨텍스트 길이를 변수로 *통제한 실험*이 아니라 운영 일화. 정량 결론은 D 섹션 학술 자료에 의존.

---

## 4. ★ 학술/업계 연구 (D1~D5) — 본 세션 핵심

> 본 세션은 학술 자료가 강한 영역이다. 수치 인용은 피하고 *정성 결론*만 인용한다(청자가 비개발자이므로). arXiv abstract는 모두 직접 페치해 200 OK 확인했다.

### D1. ★ Lost in the Middle — 긴 컨텍스트 *중간*은 가장 잘 잊힌다

**저자/발표**: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang (Stanford / UC Berkeley / Samaya AI)
**arXiv**: https://arxiv.org/abs/2307.03172 (2023-07, TACL 2024)
**확인일**: 2026-04-30

**한 줄 핵심 발견 (원문)**:
> "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts."
>
> "Even explicitly long-context models" 도 동일 패턴.

**연구 요약**: 다문서 QA와 key-value 검색 두 과제로, 정답이 들어 있는 *위치*를 컨텍스트의 처음·중간·끝으로 옮기며 정확도를 측정. **U자형 곡선** — 처음과 끝은 잘 보지만 *중간은 통째로 흘려버림*. 더 큰 컨텍스트 창을 쓴다고 자동으로 해결되지 않음.

**카메라 인용용 (수치 없이)**:
> "스탠퍼드 연구진이 발표한 'Lost in the Middle'에 따르면, 모델은 긴 입력의 *처음과 끝은 잘 보지만 가운데에 있는 정보는 통째로 흘려버립니다*. 이게 우리가 *방금 정한 규칙을 잊는다*고 느끼는 가장 큰 이유 중 하나예요."

**세션 내 사용 위치**: 진행 순서 1번(증상의 *기전* 설명) — **본 세션 헤드라인 학술 인용 ★**

**한계**: 다문서 QA·KV 검색이라는 *합성 과제* 기반 결과. 실제 대화의 모든 망각이 같은 메커니즘이라고 *확장 해석 금지*. "긴 컨텍스트 = 무조건 비례적으로 나빠진다"라고도 말하지 말 것 — 원문은 *위치 의존성*을 강조.

---

### D2. ★★ Context Rot (Chroma 2025) — 18개 모델 멀티벤더 검증

**저자/발표**: Kelly Hong, Anton Troynikov, Jeff Huber (Chroma Research)
**URL**: https://research.trychroma.com/context-rot (현 https://www.trychroma.com/research/context-rot)
**발표**: 2025-07-14
**확인일**: 2026-04-30

**한 줄 핵심 발견 (원문 인용)**:
> "Model performance varies significantly as input length changes, even on simple tasks."
>
> 테스트한 18개 모델 (Anthropic Claude Opus 4 / Sonnet 4 / Sonnet 3.5, OpenAI GPT-4.1 / 4.1 mini / 4o / 4 Turbo, Google Gemini 2.5 Pro / Flash, Alibaba Qwen3 235B / 32B / 8B 등) **전반에서 동일 경향** — 단순 복제 과제에서조차 입력이 길어질수록 정확도가 떨어짐.

**핵심 통찰 4가지**:
1. *needle-question* 의미 유사도가 낮을수록 길이 증가에 따른 성능 저하 *가속*.
2. distractor(주의 분산 정보)가 있을 때 *길이가 길수록 더 큰* 비-균등 영향.
3. haystack 구조 자체가 결과에 영향 — 내용을 무작위 셔플하면 *오히려* 더 잘 맞히는 경우.
4. 단순 텍스트 복제 같은 trivial task에서도 길이가 길어지면 정확도 하락.

**카메라 인용용 (수치 없이)**:
> "Chroma 연구팀이 2025년에 18개 주요 모델을 함께 테스트한 'Context Rot' 보고서가 있습니다. Claude, GPT-4, Gemini, Qwen 가릴 것 없이 *입력이 길어질수록 같은 작업의 정확도가 떨어진다*는 결론이 나왔어요. *어느 한 회사 도구의 결함이 아니라는 뜻*입니다."

**세션 내 사용 위치**: 진행 순서 1번(증상이 도구별 결함이 아니라는 정당화), 3번(새 세션 신호의 *근거*), 4번(왜 압축이 필요한가) — **본 세션 헤드라인 학술 인용 ★**

**왜 핵심인가**: 본 세션 명제 *"도구의 결함이 아니라 컨텍스트 관리 실패"* 를 *멀티벤더 비교*로 직접 입증한 거의 유일한 공개 자료.

**한계**: 합성 벤치마크 기반. 실제 코딩 에이전트 세션의 망각률을 같은 비율로 외삽 금지. "Claude가 X% 더 나쁘다" 같은 *모델 간 비교 수치*는 인용 금지.

---

### D3. Needle in a Haystack — 위치별 회수 정확도 시각화

**저자**: Greg Kamradt (gkamradt)
**URL**: https://github.com/gkamradt/LLMTest_NeedleInAHaystack
**확인일**: 2026-04-30

**한 줄 핵심**:
> "긴 컨텍스트의 임의 위치에 한 줄짜리 사실(needle)을 심고, 모델이 그것을 회수하는 정확도를 *길이 × 위치* 격자로 측정한다."

**연구 요약**: 2023년 11월 GPT-4-128K와 Claude 2.1을 동일 프로토콜로 테스트. 결과 히트맵에서 *중간 깊이*의 needle이 가장 자주 누락. D1의 결론을 산업 환경에서 빠르게 재현 가능한 도구로 만든 것.

**카메라 인용용**:
> "오픈소스로 공개된 *Needle in a Haystack* 테스트는, 긴 컨텍스트 안에 단 한 줄의 사실을 심어두고 모델이 그걸 *위치별로* 얼마나 잘 찾는지 보여줍니다. 가운데에 묻힌 것일수록 잘 못 찾는다는 게 그림 한 장으로 보입니다."

**세션 내 사용 위치**: 진행 순서 1번 — D1 학술 결과를 *시각 자료*로 보강

**한계**: 단일 사실 회수 과제. 강의의 "규칙을 잊는다"·"전제를 반복한다"라는 더 복잡한 망각 양상은 D2가 더 적합.

---

### D4. LongBench — 긴 컨텍스트 다과제 벤치마크

**저자/발표**: Yushi Bai et al. (THU), arXiv:2308.14508, ACL 2024
**URL**: https://arxiv.org/abs/2308.14508
**확인일**: 2026-04-30

**한 줄 핵심**:
> "QA, 요약, few-shot, 합성과제, 코드 자동완성을 포괄하는 21개 데이터셋으로 검증한 결과, *상용·오픈소스 모두 컨텍스트가 길어지면 어려워한다*."

**연구 요약**: 영어·중국어 이중언어, 평균 6,711단어 / 13,386자 분량 문서 21개 데이터셋, 6개 task 카테고리. 8개 모델 평가에서 모두 *길이가 늘면 일관된 하락*.

**카메라 인용용**:
> "ACL 2024에 발표된 LongBench 연구에 따르면, *어떤 회사 모델이든* 컨텍스트가 길어지면 똑같이 어려워합니다. 코드 자동완성도 예외가 아니에요."

**세션 내 사용 위치**: 진행 순서 4번(왜 압축·새 세션이 필요한가)

**한계**: 발표 시점(2023~2024) 모델 기준. *최신 frontier 모델에서는 격차가 줄었을 가능성*이 있으므로 정성 결론(*경향성*)으로만 인용.

---

### D5. RULER — "선전된 컨텍스트 크기"와 "실제 사용 가능한 길이"는 다르다

**저자/발표**: Cheng-Ping Hsieh et al. (NVIDIA), arXiv:2404.06654, COLM 2024
**URL**: https://arxiv.org/abs/2404.06654
**확인일**: 2026-04-30

**한 줄 핵심 (원문)**:
> "Almost all models exhibit large performance drops as the context length increases."

**연구 요약**: Vanilla needle-in-haystack을 넘어 *멀티홉 추적*과 *집계*까지 포함한 합성 벤치마크. 17개 모델 전반에서 *광고된 컨텍스트 크기와 실제 효과적 사용 가능 길이 사이에 큰 격차*가 있음을 보임.

**카메라 인용용**:
> "NVIDIA가 2024년에 공개한 RULER 벤치마크에 따르면, 모델이 *지원한다고 광고한 컨텍스트 크기*와 *실제 작업이 정확히 되는 길이*는 다릅니다. 그래서 컨텍스트 창이 크다는 이유로 안심하고 길게 끌고 가면 안 됩니다."

**세션 내 사용 위치**: 진행 순서 4번(왜 *계속 진행* 대신 *새 세션*인가의 정당화)

**한계**: 합성 task 기반. 실제 대화에서의 정확한 임계 길이를 일반화하지 말 것.

---

## 5. ★ "긴 대화 = 컨텍스트 관리 실패" 명제 직결 모음

> 강사가 카메라 앞에서 *"연구에 따르면"* 이라고 단정해도 좋은 인용을 한 곳에 모았다.

| 자료 | 한 줄 요지 |
|---|---|
| **A1** Anthropic Claude Code 공식 | "Context window fills up fast, performance degrades as it fills." — 공식 문서가 인정 |
| **A2** Anthropic Engineering | "토큰이 많아질수록 정확히 기억하는 능력이 떨어진다 — 트랜스포머 구조상 불가피" |
| **D1** Lost in the Middle (Stanford) | "처음과 끝은 잘 보지만 *중간은 흘려버린다*" |
| **D2** Context Rot (Chroma, 2025) | 18개 모델 *전반*에서 길이↑ → 정확도↓ → *어느 한 도구의 결함이 아님* |
| **D5** RULER (NVIDIA) | "광고된 컨텍스트 크기 ≠ 실제 사용 가능한 길이" |
| **C1** Anthropic Claudius | 길어진 컨텍스트에서 정체성까지 손실 — Anthropic 자신의 사례 |

**강사 권장 인용 시퀀스 (한 호흡 25초)**:
> "긴 대화가 망가지는 건 도구의 결함이 아닙니다. Anthropic 공식 가이드는 *컨텍스트가 채워질수록 성능이 떨어진다*고 인정합니다. 스탠퍼드의 'Lost in the Middle' 연구는 모델이 *처음과 끝은 잘 보지만 가운데는 통째로 흘려버린다*는 걸 보여줬습니다. Chroma가 2025년에 18개 주요 모델을 함께 테스트한 'Context Rot' 보고서는 Claude·GPT·Gemini·Qwen 가릴 것 없이 *길이가 길어지면 같은 작업의 정확도가 떨어진다*고 결론지었습니다. — 그래서 *언제 새 세션을 열지*가 사용자 책임입니다."

---

## 6. 인용 시 유의사항 / 한계

1. **수치 인용 금지**: D1·D2·D4·D5의 구체 % 수치는 *발표 시점 모델 기준*이라 최신 frontier 모델에서 격차가 줄었을 수 있다. 정성 결론(*경향성*)만 인용.
2. **"긴 컨텍스트 = 무조건 나쁘다" 일반화 금지**: D1은 *위치 의존성*을 강조한다. "처음·끝은 비교적 잘 본다"는 단서를 빼면 원문 왜곡.
3. **합성 벤치마크 ↔ 실제 대화의 외삽 주의**: D1·D3·D5는 합성 task. 실제 코딩 세션의 망각률을 같은 비율로 일반화하지 말 것. D2가 더 일반화 친화적이지만 그조차 합성.
4. **모델 간 비교 수치 인용 금지**: D2가 18개 모델을 한 번에 테스트했지만, "X가 Y보다 Z% 더 잘한다" 같은 인용은 강의 청자(비개발자)에게 무의미하고 출처 분쟁 위험. 본 세션의 메시지는 *모든 모델에 공통된 경향*이라는 점뿐.
5. **C1 Claudius는 *사례*이지 *통제 실험*이 아님**: 일화로만 사용하고, 정량 결론(예: "긴 세션에서 X% 확률로 정체성을 잃는다")으로 확장하지 말 것.
6. **Anthropic 편중 회피**: A1·A2·C1·D2의 일부가 Anthropic 진영. A3(OpenAI), D1(Stanford), D5(NVIDIA), D2(Chroma)를 함께 인용해 *진영 중립성* 유지.
7. **다음 세션(3-2)과의 분리**: `/compact` `/clear`의 *실전 운용 단계 절차*는 3-2에 위임. 본 세션은 *왜 그래야 하는가*의 이론·근거만 다룬다 — A1·A2 인용 시 명령 사용법 부분은 의도적으로 가볍게.

---

## 7. 출처 일람 (URL 한 곳에 모음, 200 OK 검증 완료 2026-04-30)

### 공식 가이드
- Anthropic Claude Code Best Practices (★ "context fills up, performance degrades"): https://code.claude.com/docs/en/best-practices
- Anthropic Engineering — Effective Context Engineering for AI Agents (★ context rot 공식 인정): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- OpenAI Cookbook — GPT-5 Prompting Guide (Responses API, agentic eagerness): https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide

### 사고/사례
- Anthropic Project Vend (Claudius 정체성 손실): https://www.anthropic.com/research/project-vend-1

### 학술 / 업계 연구 ★
- Lost in the Middle (Liu et al., arXiv:2307.03172, TACL 2024): https://arxiv.org/abs/2307.03172
- Context Rot (Hong, Troynikov, Huber — Chroma, 2025-07): https://www.trychroma.com/research/context-rot
- Needle in a Haystack (Kamradt): https://github.com/gkamradt/LLMTest_NeedleInAHaystack
- LongBench (Bai et al., arXiv:2308.14508, ACL 2024): https://arxiv.org/abs/2308.14508
- RULER (Hsieh et al., arXiv:2404.06654, COLM 2024): https://arxiv.org/abs/2404.06654
