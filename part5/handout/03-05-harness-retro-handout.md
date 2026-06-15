# Session 3-5 - Harness 를 발전시키기 위해서

좋은 하네스는 `실패를 기반으로 계속 깎아나가야`합니다.  
실패를 기록하고 같은 실패를 막도록 Agent 를 구성하기도 하면서 "지속적으로" 발전시켜나가야합니다.

- 실패를 모델 실패, 컨텍스트 실패, 하네스 실패로 나눕니다.
- 하나의 실패를 skill/hook(eval) 의 개선으로 나누어서 연결합니다.

---

좋은 **AI Agent Harness**는 “프롬프트 몇 줄”이 아니라, **모델을 둘러싼 제어·관찰·평가·개선 시스템**입니다. 핵심은 `실패를 계속 저장하고, 같은 실패가 다시 발생하지 않도록` **trace → failure label → eval case → harness/model/context patch → release gate**로 연결하는 것입니다.

가장 중요한 설계 원칙은 이겁니다.

> **실패는 로그가 아니라 자산이다.**
> 단, 자산이 되려면 “재현 가능하고, 원인 분류가 가능하고, 다음 배포를 막을 수 있는 테스트”가 되어야 한다.

Anthropic도 agent eval을 늦게 만들면 운영 중 사용자 신고에 의존하는 reactive loop에 빠지고, 반대로 실패를 테스트 케이스로 바꾸면 회귀를 막고 개선 속도가 빨라진다고 설명합니다. 또한 초기에 수백 개가 아니라 **실제 실패에서 뽑은 20~50개 단순 task**만으로도 충분히 시작할 수 있다고 권장합니다. ([Anthropic][1]) ([Anthropic][1])

---

## 1. 먼저 Harness의 범위를 넓게 잡아야 합니다

여기서 Harness는 다음 전부를 포함합니다.

| 계층                    | 포함 요소                                                                        |
| --------------------- | ---------------------------------------------------------------------------- |
| Model layer           | 모델 선택, temperature, reasoning depth, tool-use 능력, instruction following      |
| Prompt / policy layer | system prompt, developer instruction, policy, refusal/clarification 기준       |
| Context layer         | RAG, memory, user profile, session state, tool 결과, 압축/요약, freshness          |
| Tool layer            | tool schema, argument validation, idempotency, permissions, sandbox, retries |
| Control-flow layer    | planner, router, verifier, retry loop, fallback, human-in-the-loop           |
| Eval layer            | graders, golden dataset, regression suite, online eval, release gate         |
| Observability layer   | trace, span, cost, latency, token, tool call, context snapshot, feedback     |

OpenAI의 Agents SDK tracing 문서도 agent run에서 **LLM generation, tool call, handoff, guardrail, custom event**를 포괄적으로 수집한다고 설명합니다. OpenAI의 agent workflow evaluation 역시 trace, grader, dataset, eval run을 함께 써서 agent 품질을 개선하는 구조를 권장합니다. ([OpenAI GitHub Pages][2]) ([OpenAI 개발자][3])

즉, 실패가 났을 때 “모델이 멍청했다”로 끝내면 안 됩니다. 같은 실패라도 원인이 전혀 다를 수 있습니다.

---

## 2. 실패 분류는 “주 원인 + 보조 원인”으로 저장해야 합니다

말씀하신 세 분류는 매우 좋습니다. 다만 실제 운영에서는 하나의 실패가 복합 원인인 경우가 많으므로, **primary_failure_type**과 **contributing_factors**를 따로 두는 편이 좋습니다.

### A. 모델 실패

모델이 **필요한 정보와 적절한 도구를 받았는데도** 잘못 판단한 경우입니다.

예시:

| 증상                          | 가능한 개선                                                      |
| --------------------------- | ----------------------------------------------------------- |
| 명백한 추론 오류                   | 더 강한 모델, task decomposition, verifier 추가                    |
| 지시 불이행                      | instruction hierarchy 정리, few-shot 추가, policy test 추가       |
| tool argument hallucination | tool schema 명확화도 필요하지만, oracle context에서도 틀리면 model failure |
| 과잉 행동 / 과잉 자동화              | “ask-before-act”, destructive action approval, planner 제약   |
| 불필요한 검색 / 검색 누락             | search decision eval, router 개선, search/no-search 양방향 테스트   |
| 불확실성 표현 실패                  | confidence calibration, “모르면 모른다” judge, abstention policy  |

Anthropic은 검색을 해야 하는 query와 검색하지 않아야 하는 query를 모두 eval에 넣어 under-triggering과 over-triggering을 함께 잡는 사례를 설명합니다. 이런 식으로 모델 행동의 trade-off를 양방향으로 테스트해야 합니다. ([Anthropic][1])

### B. 컨텍스트 실패

모델 자체는 합리적으로 행동했지만, **잘못된 정보·부족한 정보·오래된 정보·오염된 memory** 때문에 실패한 경우입니다.

예시:

| 증상                        | 가능한 개선                                                             |
| ------------------------- | ------------------------------------------------------------------ |
| RAG가 관련 문서를 못 찾음          | chunking, query rewriting, reranking, metadata filter 개선           |
| 오래된 문서를 근거로 답함            | freshness score, TTL, source priority, stale-context detector      |
| memory가 틀린 선호를 주입함        | memory write policy, decay, user-confirmed memory만 사용              |
| context window에서 핵심 정보 누락 | context packing, salience scoring, long-context eval               |
| tool 결과가 모호함              | tool output schema에 confidence/source/timestamp 포함                 |
| 여러 context가 충돌            | conflict resolver, source hierarchy, “conflict detected” 응답 policy |

LangChain은 trace와 feedback이 있어야 agent가 본 것, 한 것, 그 결과를 바탕으로 **model, harness, context 중 무엇을 개선해야 하는지** 알 수 있다고 설명합니다. 특히 context layer는 retrieved docs, memory, user preferences, tool results, prior turns, environment state에 민감하므로 별도 개선 루프로 다뤄야 합니다. 

### C. 하네스 실패

모델이 아니라 **모델 주변의 제어 시스템** 때문에 실패한 경우입니다. 실제 production agent에서는 이 비중이 상당히 큽니다.

예시:

| 증상                             | 가능한 개선                                                              |
| ------------------------------ | ------------------------------------------------------------------- |
| tool schema가 애매해서 잘못 호출        | schema 설명, enum, required field, examples 강화                        |
| tool call은 맞았지만 permission이 과함 | least privilege, approval gate, sandbox                             |
| retry가 같은 실수를 반복               | retry에 새로운 evidence/context 추가, max loop, failure-aware retry       |
| evaluator가 정답을 오판              | deterministic grader 우선, LLM judge human calibration                |
| eval 환경이 production과 다름        | prod-like sandbox, versioned env, clean state                       |
| state contamination            | run별 isolated workspace, cache reset, fixture cleanup               |
| trace가 불완전해 원인 추적 불가           | full trajectory capture, prompt/context/tool snapshot 저장            |
| guardrail이 너무 강하거나 약함          | policy eval, blocked/allowed 양방향 테스트                                |
| timeout/rate limit 때문에 task 실패 | budget-aware planner, partial result protocol, graceful degradation |

Anthropic은 eval harness가 production agent와 비슷하게 동작해야 하고, 각 trial은 깨끗한 환경에서 격리되어야 하며, 공유 state나 resource exhaustion이 eval 결과를 왜곡할 수 있다고 지적합니다. grader도 deterministic grader를 우선하고, LLM judge는 사람 평가와 calibration해야 하며, 너무 rigid한 grader는 valid solution을 실패로 오판할 수 있습니다. ([Anthropic][1]) ([Anthropic][1])

---

## 3. 실패 저장 스키마는 “분석용”이 아니라 “재현·회귀방지용”이어야 합니다

실패 DB는 단순히 “이런 문제가 있었다”가 아니라, 나중에 자동으로 eval을 돌릴 수 있어야 합니다.

추천 schema는 아래와 같습니다.

```json
{
  "failure_id": "F-2026-06-14-001",
  "run_id": "trace_abc123",
  "timestamp": "2026-06-14T10:15:00+09:00",

  "agent": {
    "agent_name": "research_agent",
    "agent_version": "v1.8.2",
    "model": "model_name",
    "model_version": "snapshot_or_date",
    "temperature": 0.2,
    "prompt_hash": "sha256:...",
    "tool_schema_version": "tools-2026-06-10",
    "harness_version": "harness-0.14.3"
  },

  "input": {
    "user_request": "...",
    "normalized_task": "...",
    "user_context_snapshot_id": "ctx_123",
    "retrieved_context_ids": ["doc_1", "doc_2"],
    "tool_results_snapshot_ids": ["tool_result_1"]
  },

  "expected": {
    "success_criteria": [
      "정확한 근거 문서 2개 이상 인용",
      "2026년 이후 정보는 최신성 확인",
      "불확실하면 명시"
    ],
    "reference_answer": "...",
    "must_not": ["근거 없는 단정", "권한 없는 tool call"]
  },

  "actual": {
    "final_output": "...",
    "failed_step": "tool_call.search_docs",
    "symptom": "stale_context_used",
    "user_visible_impact": "wrong_answer"
  },

  "classification": {
    "primary_failure_type": "context_failure",
    "contributing_factors": ["harness_failure"],
    "root_cause": "retriever가 최신 정책 문서를 top-k에 포함하지 못했고 stale 문서가 우선됨",
    "severity": "high",
    "confidence": 0.82
  },

  "reproduction": {
    "reproducible": true,
    "seed": 42,
    "environment_image": "agent-sandbox:2026-06-12",
    "steps": ["load fixture", "run eval case", "compare grader"]
  },

  "improvement": {
    "proposed_fix": "retrieval에 document_date boost와 stale penalty 추가",
    "owner": "context-team",
    "patch_id": "PR-412",
    "eval_case_id": "EVAL-context-staleness-017",
    "status": "open"
  },

  "verification": {
    "before_score": 0,
    "after_score": null,
    "regression_suite": ["context_freshness", "citation_quality"],
    "release_blocker": true
  }
}
```

여기서 중요한 필드는 **prompt_hash, tool_schema_version, context snapshot, environment image, grader version**입니다. 이것들이 없으면 나중에 같은 실패를 재현할 수 없습니다. OpenAI eval 문서도 eval을 “task 정의 → test input 실행 → 결과 분석 후 prompt/system 개선”의 반복 과정으로 설명합니다. 반복이 가능하려면 입력·환경·채점 기준이 versioned artifact여야 합니다. ([OpenAI 개발자][4])

---

## 4. 원인 분류는 Counterfactual Triage로 해야 합니다

실패를 사람이 임의로 분류하면 흔들립니다. 아래 질문으로 판정하는 것이 좋습니다.

### 1단계: Trace가 충분한가?

“모델이 본 prompt, context, tool result, intermediate state, final output을 모두 볼 수 있는가?”

아니면 우선 **observability failure**입니다. Google Cloud도 agent observability에서 prompt/response, token usage, latency, tool usage, reasoning sequence, safety, quality/evaluation을 관찰 대상으로 봅니다. ([Google Cloud Documentation][5])

### 2단계: Oracle context를 주면 성공하는가?

정답 문서, 올바른 memory, 정확한 tool result를 직접 넣었을 때 성공하면 **context failure** 가능성이 큽니다.

### 3단계: 같은 context에서 더 명확한 tool schema나 control-flow를 주면 성공하는가?

성공하면 **harness failure**입니다. 예를 들어 “삭제 전 사용자 승인 필요”라는 guardrail이 없어서 삭제했다면 모델 문제가 아니라 하네스 권한 설계 문제입니다.

### 4단계: 완벽한 context와 명확한 harness에서도 실패하는가?

그때 **model failure**로 봅니다. 이 경우 prompt patch만 반복하지 말고 모델 선택, task decomposition, verifier, fine-tuning/SFT/RL 데이터화, abstention policy를 검토해야 합니다.

### 5단계: Grader가 맞는가?

실제로는 agent가 맞았는데 grader가 틀리는 경우가 자주 있습니다. Anthropic은 rigid grading, 모호한 task spec, 재현 불가능한 stochastic task 때문에 좋은 agent 성능이 낮게 측정되는 사례를 들며, transcript와 grade를 직접 읽어야 한다고 강조합니다. ([Anthropic][1])

---

## 5. 개선 루프는 이렇게 돌리는 것이 좋습니다

### Step 1. 모든 production run을 trace로 남긴다

최소 수집 항목은 다음입니다.

| 항목                                  | 이유                            |
| ----------------------------------- | ----------------------------- |
| user input                          | 실패 재현의 시작점                    |
| system/developer prompt hash        | prompt 변경 영향 추적               |
| retrieved context 전문 또는 snapshot ID | context failure 판정            |
| tool call name/args/result/error    | tool misuse, schema 문제 판정     |
| intermediate decisions              | planner/router/verifier 문제 판정 |
| final output                        | user-visible quality 판정       |
| cost/latency/token                  | 성능·비용 회귀 감지                   |
| user feedback / implicit signal     | 성공·실패 label 확보                |
| model/harness/context version       | before/after 비교               |

Langfuse도 LLM application tracing의 핵심을 prompt, model response, token usage, latency, tool/retrieval step까지 포함한 구조화 로그로 설명합니다. ([Langfuse][6])

### Step 2. trace에 feedback을 붙인다

feedback은 꼭 thumbs-up/down만이 아닙니다.

| Feedback source        | 예시                                                |
| ---------------------- | ------------------------------------------------- |
| Explicit user feedback | 좋아요/싫어요, 신고, correction                           |
| Implicit user feedback | 같은 질문 반복, ticket reopen, generated code revert    |
| Deterministic signal   | test pass/fail, schema validation, citation 존재 여부 |
| LLM-as-judge           | helpfulness, policy following, factuality         |
| Human review           | domain expert annotation, pairwise preference     |

LangChain은 trace만으로는 “무슨 일이 있었는지”만 알 수 있고, feedback이 붙어야 그것이 성공인지 실패인지 알 수 있다고 설명합니다. 또한 feedback은 trace/run/thread에 직접 연결되어야 좋은/나쁜 trajectory 비교, real failure 기반 dataset 구축, 개선 추적이 가능하다고 설명합니다. 

### Step 3. 실패를 eval case로 승격한다

모든 실패를 eval로 만들 필요는 없습니다. 아래 조건 중 하나를 만족하면 승격합니다.

| 승격 조건              | 설명                               |
| ------------------ | -------------------------------- |
| high severity      | 사용자 피해, 보안, 금전, 데이터 손실           |
| recurring          | 같은 유형이 2회 이상 반복                  |
| silent failure     | 겉으로는 성공처럼 보이나 내용이 틀림             |
| regression risk    | prompt/model/tool 변경 때 다시 깨질 가능성 |
| strategic behavior | 제품의 핵심 UX와 관련                    |

Anthropic은 user-reported failure를 test case로 바꾸면 suite가 실제 사용을 반영하고, user impact 기준으로 우선순위를 정할 수 있다고 설명합니다. ([Anthropic][1])

### Step 4. Grader를 고른다

항상 LLM-as-judge부터 쓰면 안 됩니다.

| Grader type                  | 언제 쓰나                                                        |
| ---------------------------- | ------------------------------------------------------------ |
| Exact / regex / JSON schema  | 구조화 출력, 금지어, citation, tool args                             |
| Unit test / integration test | coding agent, data transform, API workflow                   |
| Static analysis              | code quality, security rule                                  |
| Reference comparison         | 요약, 분류, 추출                                                   |
| LLM-as-judge                 | subjective quality, instruction following, reasoning quality |
| Human grader                 | 고위험, 애매한 품질, judge calibration                               |

Anthropic은 가능하면 deterministic grader를 쓰고, 필요할 때 LLM grader를 쓰며, LLM-as-judge는 human expert와 calibration해야 한다고 권장합니다. ([Anthropic][1])

### Step 5. 한 번에 한 계층만 고친다

나쁜 패턴은 “prompt도 바꾸고, retriever도 바꾸고, tool도 바꾸고, 모델도 바꾸는 것”입니다. 그러면 무엇이 효과가 있었는지 모릅니다.

권장 방식:

1. 실패를 primary type으로 분류한다.
2. 해당 계층만 patch한다.
3. 관련 eval subset만 먼저 돌린다.
4. 전체 regression suite를 돌린다.
5. before/after trace diff를 저장한다.
6. 개선이 확인되면 release gate를 통과시킨다.

2026년 arXiv의 Agentic Harness Engineering 연구도 harness 개선을 trial-and-error가 아니라, component observability, experience observability, decision observability를 통해 “각 edit을 검증 가능한 계약”으로 만드는 방향을 제안합니다. 같은 연구에서 성능 향상이 system prompt보다 tool, middleware, long-term memory 같은 harness 구조에서 주로 왔다고 보고합니다. ([arXiv][7])

---

## 6. 실패 유형별 개선 전략

### 모델 실패 개선

모델 실패는 “더 긴 prompt”로만 해결하려 하면 한계가 있습니다.

좋은 개선책:

| 개선책                            | 설명                                   |
| ------------------------------ | ------------------------------------ |
| Task decomposition             | 큰 목표를 plan → execute → verify로 나눔    |
| Verifier model                 | 최종 답변 전 fact, policy, format 검증      |
| Self-check가 아니라 external check | 모델의 자기확신보다 test/tool/ground truth 활용 |
| Few-shot hard cases            | 실제 실패 케이스를 instruction example로 추가   |
| Model routing                  | 복잡도 높은 task만 더 강한 모델로 route          |
| Abstention policy              | 불확실할 때 질문하거나 모른다고 답하게 함              |
| Fine-tuning / SFT data         | 반복적이고 명확한 model behavior failure에 사용 |

주의할 점은 model failure를 너무 쉽게 선언하면 안 된다는 것입니다. oracle context와 명확한 harness에서도 실패하는지 확인해야 합니다.

### 컨텍스트 실패 개선

컨텍스트 실패는 agent 품질을 가장 크게 흔드는 계층입니다.

좋은 개선책:

| 개선책                       | 설명                                  |
| ------------------------- | ----------------------------------- |
| Context snapshot 저장       | 실패 당시 모델이 실제로 본 정보 보존               |
| Retrieval eval 분리         | answer eval과 retrieval eval을 따로 측정  |
| Oracle-context test       | 정답 context를 주면 성공하는지 확인             |
| Staleness detector        | 오래된 문서, 폐기된 policy, 낮은 freshness 감점 |
| Source hierarchy          | 공식 문서 > 최신 내부 정책 > 과거 대화 등 우선순위     |
| Memory write gate         | 사용자 확인 없는 memory 저장 금지              |
| Memory TTL / decay        | 오래된 선호나 상태 자동 약화                    |
| Context conflict detector | 서로 다른 context가 충돌하면 단정하지 않음         |

컨텍스트 계층은 “더 많이 넣기”가 답이 아닙니다. 잘못된 context를 많이 넣으면 모델은 더 설득력 있게 틀립니다.

### 하네스 실패 개선

하네스 실패는 가장 엔지니어링적으로 고칠 수 있는 영역입니다.

좋은 개선책:

| 개선책                     | 설명                                                       |
| ----------------------- | -------------------------------------------------------- |
| Tool schema hardening   | enum, required, constraints, examples, negative examples |
| Permission boundary     | read/write/delete/payment/email 등 권한 분리                  |
| Approval gate           | irreversible action 전 human approval                     |
| Idempotent tool design  | retry가 중복 결제/중복 삭제를 만들지 않게 함                             |
| Retry with new evidence | 같은 prompt 재시도 금지, 실패 원인 반영                               |
| Loop breaker            | max steps, repeated tool-call detection                  |
| Sandbox isolation       | eval/prod 모두 clean workspace                             |
| State reset             | trial 간 file/cache/history 오염 방지                         |
| Grader versioning       | grader 변경도 product 변경처럼 관리                               |
| Trace coverage test     | trace 누락 자체를 CI failure로 처리                              |

VeRO 연구도 agent harness optimization은 deterministic code와 stochastic LLM completion이 섞이기 때문에, versioned snapshots, budget-controlled evaluation, structured execution traces가 필요하다고 설명합니다. ([arXiv][8])

---

## 7. Release Gate를 만들어야 같은 실패가 막힙니다

실패를 저장만 하면 지식 베이스입니다. 배포를 막으면 하네스입니다.

추천 gate:

| Gate                     | 기준 예시                                          |
| ------------------------ | ---------------------------------------------- |
| Critical regression gate | severity=critical eval은 100% pass              |
| Slice gate               | “결제”, “삭제”, “개인정보”, “법률/의료” slice 별 threshold  |
| Context freshness gate   | stale-source 사용률 특정 기준 이하                      |
| Tool safety gate         | destructive tool은 approval 없이 호출 0건            |
| Cost/latency gate        | p95 latency, token cost 회귀 제한                  |
| Judge drift gate         | LLM judge와 human label disagreement 증가 시 block |
| Unknown failure gate     | unknown/mixed failure 비율 급증 시 block            |

Anthropic은 자동 eval이 pre-launch와 CI/CD에서 유용하고, production monitoring은 distribution drift와 예상 못한 real-world failure를 잡으며, A/B test와 human review까지 결합해야 전체적인 agent 이해가 가능하다고 설명합니다. ([Anthropic][1])

---

## 8. 운영 지표는 pass rate보다 “재발률”이 중요합니다

Harness가 좋아지고 있는지 보려면 다음 지표를 봐야 합니다.

| 지표                         | 의미                                     |
| -------------------------- | -------------------------------------- |
| Failure recurrence rate    | 같은 root cause가 다시 발생하는 비율              |
| Escape rate                | eval에서 못 잡고 production에서 터진 실패         |
| Eval conversion rate       | production failure 중 eval case로 승격된 비율 |
| MTTR                       | failure 발견 후 patch+검증까지 시간             |
| Trace coverage             | 원인 분석에 충분한 trace 비율                    |
| Context hit rate           | 정답 context가 top-k에 있었는지                |
| Tool success rate          | tool call 성공률과 argument validation 실패율 |
| Judge-human agreement      | LLM judge 신뢰도                          |
| Regression suite stability | flaky eval 비율                          |
| Cost per successful task   | 성공 기준 비용                               |

가장 중요한 지표는 **“지난달에 고친 실패가 이번 달에 다시 나왔는가?”**입니다.

---

## 9. 실전에서는 Failure Review 문화를 만들어야 합니다

주 1회 정도 아래 형식으로 보면 좋습니다.

| 질문                                                 | 목적            |
| -------------------------------------------------- | ------------- |
| 이번 주 top recurring failure는 무엇인가?                  | 반복 실패 제거      |
| model/context/harness 비율이 어떻게 변했는가?                | 투자 방향 결정      |
| eval로 승격되지 않은 high-severity failure가 있는가?          | escape 방지     |
| grader가 틀린 사례는 있는가?                                | eval 신뢰도 개선   |
| context failure 중 stale/missing/conflicting 비율은?   | RAG/memory 개선 |
| harness failure 중 tool/permission/retry/state 문제는? | 제어 시스템 강화     |
| 새 patch가 다른 slice를 망가뜨렸는가?                         | 회귀 방지         |

여기서 중요한 문화는 **“누가 잘못했나”가 아니라 “어느 계층이 다음에 막을 수 있나”**입니다.

---

## 10. AI Agent Harness 개선은 flywheel.

```text
Production Trace
  → Feedback / Failure Detection
  → Model vs Context vs Harness 분류
  → Root Cause 기록
  → Eval Case 승격
  → Targeted Patch
  → Regression Suite
  → Release Gate
  → Production Monitoring
  → 다시 Trace
```

그리고 이 flywheel의 품질은 세 가지로 결정됩니다.

1. **Trace의 완전성**: agent가 무엇을 보고, 어떤 tool을 왜 호출했고, 무엇을 출력했는가.
2. **Failure label의 정확성**: model/context/harness 중 어디를 고쳐야 하는가.
3. **Eval 전환율**: 한 번 발생한 실패가 다음 배포를 실제로 막는가.

결국 좋은 하네스는 “agent를 더 똑똑하게 보이게 하는 장치”가 아니라, **agent가 실패했을 때 시스템 전체가 학습하도록 만드는 장치**입니다.

[1]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents "Demystifying evals for AI agents \ Anthropic"
[2]: https://openai.github.io/openai-agents-python/tracing/ "Tracing - OpenAI Agents SDK"
[3]: https://developers.openai.com/api/docs/guides/agent-evals "Evaluate agent workflows | OpenAI API"
[4]: https://developers.openai.com/api/docs/guides/evals "Working with evals | OpenAI API"
[5]: https://docs.cloud.google.com/stackdriver/docs/observability/agent-observability "Agent observability  |  Google Cloud Observability  |  Google Cloud Documentation"
[6]: https://langfuse.com/docs/observability/overview "LLM Observability & Application Tracing (Open Source) - Langfuse"
[7]: https://arxiv.org/abs/2604.25850 "[2604.25850] Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses"
[8]: https://arxiv.org/abs/2602.22480 "[2602.22480] VeRO: A Harness for Agents to Optimize Agents"
