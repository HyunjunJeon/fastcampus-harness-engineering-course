**Multi Agent System을 “복잡한 지능 구조”가 아니라 “그래프 형태의 워크플로 구성”으로 보는 것**입니다.

## 1. 핵심 관점: Multi Agent는 결국 Graph Workflow다

Multi Agent 시스템은 본질적으로 **유향 그래프**입니다. 그래프 이론으로 표현하면 `G = (V, E)`이고, `V`는 에이전트, LLM 호출, 도구 호출, 라우터, 검증기, 메모리 저장소 같은 노드이며, `E`는 데이터 전달, 제어 흐름, 의존성, 이벤트를 의미합니다.

아무리 복잡해 보여도 기본 구성은 딱 4가지입니다.

| 그래프 관점            | 워크플로 형태 | 의미                                      |
| ----------------- | ------- | --------------------------------------- |
| Path              | 순차 실행   | A → B → C                               |
| Fan-out / Fan-in  | 병렬 실행   | A → {B, C, D} → Merge                   |
| Conditional Edge  | 분기      | A → 조건에 따라 B 또는 C                       |
| Cycle / Back-edge | 반복      | Generate → Evaluate → Revise → Generate |

즉, Multi Agent는 “에이전트가 많다”는 사실보다 **역할을 담당하는 노드를 어떻게 나누고, 다음에 어디로 연결할지 정하며, 최종적으로 어떤 종료 조건을 둘 것인가**의 문제입니다. Anthropic도 에이전트 설계에서 복잡한 프레임워크보다 **단순하고 조합 가능한 패턴**이 성공적이었다고 설명하며, “workflow”는 미리 정의된 코드 경로를 따르는 시스템, “agent”는 LLM이 도구 사용과 진행 방식을 동적으로 지휘하는 시스템으로 구분합니다. ([Anthropic][1])

---

## 2. 대표 Multi Agent Pattern

### 2.1 Prompt Chaining: 순차 실행 패턴

가장 단순한 형태입니다.  
하나의 작업을 여러 단계로 분해하고, 각 단계의 출력이 다음 단계의 입력이 됩니다.

```text
Input → Agent A → Agent B → Agent C → Output
```

예를 들어 “요구사항 분석 → 설계 → 코드 작성 → 리뷰”처럼 명확히 분해 가능한 작업에 적합합니다. Anthropic은 이를 **Prompt chaining**으로 설명하며, 작업이 깔끔하게 고정된 하위 단계로 나뉠 때 사용하라고 권고합니다. ([Anthropic][1])

### 2.2 Routing: 분기 패턴

라우터가 입력을 분류하고, 적절한 전문 에이전트나 워크플로로 보냅니다.

```text
Input → Router
          ├─ Backend Agent
          ├─ Frontend Agent
          └─ Security Agent
```

이는 그래프에서 **conditional edge**입니다. 고객 문의 분류, 코드 영역별 전문화, 문서 유형별 처리처럼 입력 유형이 명확히 구분될 때 적합합니다. Anthropic은 Routing을 입력을 분류해 특화된 후속 작업으로 전달하는 워크플로로 설명합니다. ([Anthropic][1])

### 2.3 Parallelization: 병렬 실행 패턴

하나의 작업을 여러 독립 하위 작업으로 나누어 동시에 처리한 뒤 결과를 합칩니다.

```text
Input → Split → Agent A
              → Agent B
              → Agent C
        → Aggregate → Output
```

그래프 이론으로는 **fan-out / fan-in**입니다. Anthropic은 병렬화의 대표 형태로 서로 다른 섹션을 나누어 처리하는 방식과, 여러 에이전트가 같은 문제를 풀고 투표 또는 집계하는 방식을 제시합니다. ([Anthropic][1])

### 2.4 Orchestrator-Workers: 중앙 조정자 + 작업자 패턴

중앙 Orchestrator가 문제를 분석하고, 필요한 하위 작업을 동적으로 생성해 Worker Agent에게 맡긴 뒤 결과를 종합합니다.

```text
Input → Orchestrator
          ├─ Worker 1
          ├─ Worker 2
          └─ Worker 3
        → Synthesis
```

Anthropic은 이 패턴을 **Orchestrator-workers**로 설명하며, 필요한 하위 작업을 미리 예측하기 어려운 경우에 적합하다고 봅니다. Claude Code의 서브에이전트 구조도 이 계열에 가깝습니다. ([Anthropic][1])

### 2.5 Evaluator-Optimizer / Generator-Verifier: 반복 개선 패턴

생성자가 결과를 만들고, 평가자가 이를 검토한 뒤 다시 개선합니다.

```text
Generate → Evaluate → Revise → Evaluate → ... → Accept
```

그래프 관점에서는 **cycle**입니다. Anthropic은 이 패턴을 **Evaluator-optimizer**로 설명하며, 명확한 평가 기준이 있고 반복 개선이 실제로 품질을 높이는 경우에 적합하다고 말합니다. Claude의 coordination patterns 글도 Generator-Verifier를 대표 패턴으로 제시하되, 루프가 멈추지 않도록 최대 반복 횟수와 fallback을 둬야 한다고 설명합니다. ([Anthropic][1])

### 2.6 Agent Teams / Message Bus / Shared State

더 복잡한 시스템에서는 여러 장기 실행 에이전트가 큐에서 작업을 가져가거나, 이벤트 버스를 통해 메시지를 주고받거나, 공유 상태 저장소를 통해 협업합니다.

```text
Agent Teams:      Coordinator → Task Queue → Workers
Message Bus:      Agent A ↔ Event Bus ↔ Agent B
Shared State:     Agent A ↔ Shared Store ↔ Agent B
```

Claude의 multi-agent coordination 글은 다섯 가지 패턴으로 **Generator-Verifier, Orchestrator-Subagent, Agent Teams, Message Bus, Shared State**를 제시합니다. 다만 시작점은 항상 가장 단순한 패턴이어야 하며, 필요할 때만 점진적으로 복잡도를 높이라고 권고합니다. ([Claude][2])

---

## 3. Multi Agent가 불필요하거나 성능상 제한이 되는 경우

중요한 점은 **복잡한 문제라고 해서 곧바로 Multi Agent가 필요한 것은 아니라는 것**입니다. LangChain도 복잡한 작업이라고 항상 multi-agent가 필요한 것은 아니며, 단일 에이전트와 동적 도구, 좋은 프롬프트만으로 충분한 경우가 많다고 설명합니다. ([LangChain Docs][3])

| 문제가 되는 경우                    | 왜 문제가 되는가                             | 해결 방향                                                      |
| ---------------------------- | ------------------------------------- | ---------------------------------------------------------- |
| 단일 LLM 호출로 충분한 작업            | 에이전트 간 조정 비용이 품질 이득보다 큼               | 단일 에이전트 + 좋은 프롬프트 + RAG + few-shot 예시                      |
| 컨텍스트를 나누기 어려운 작업             | 에이전트 간 정보 전달 과정에서 손실 발생               | 하나의 에이전트가 전체 문맥을 유지하도록 설계                                  |
| 강한 순차 의존성이 있는 작업             | 병렬화해도 대기 시간이 줄지 않고 오히려 조정 비용 증가       | Prompt chaining 또는 명시적 state machine 사용                    |
| 저가치·저위험·저복잡도 작업              | 토큰·시간·디버깅 비용이 과도함                     | 단순 workflow로 처리                                            |
| 도구가 많아서 헷갈리는 문제              | 전문화보다 tool selection 문제가 핵심일 수 있음     | Tool search, tool routing, MCP tool registry 등으로 도구 노출 최소화 |
| 평가 기준이 모호한 반복 루프             | Generator-Verifier가 무한 반복하거나 조기 성공 선언 | 명확한 acceptance criteria, negative test, 최대 반복 수 설정         |
| 공유 파일·공유 상태를 여러 에이전트가 동시에 수정 | 충돌, 중복 작업, 모순된 변경 발생                  | worktree 분리, lock, merge gate, integration test 사용         |
| 운영 관측성이 낮은 시스템               | 실패 원인 추적이 어려움                         | trace, checkpoint, durable state, end-state evaluation 도입  |

Anthropic은 에이전트 시스템을 도입할 때 **가장 단순한 해결책부터 찾으라**고 강조합니다. 에이전트 시스템은 더 좋은 성능을 줄 수 있지만, 일반적으로 latency와 cost를 희생합니다. 또한 단일 LLM 호출에 retrieval과 in-context example을 붙이는 것만으로 충분한 경우도 많다고 설명합니다. ([Anthropic][1])

특히 Anthropic의 “When to use multi-agent systems” 글은 multi-agent가 일관되게 성능을 내는 경우를 세 가지로 압축합니다. 첫째, **context pollution**을 막아야 할 때, 둘째, 작업이 **병렬화 가능**할 때, 셋째, 서로 다른 도구·프롬프트·전문성이 필요한 **specialization**이 필요할 때입니다. 반대로 이 세 가지 제약이 없다면 조정 비용이 이득을 넘어서기 쉽습니다. ([Claude][4])

비용 측면도 중요합니다. Anthropic은 multi-agent가 단일 에이전트 대비 보통 **3~10배 토큰**을 사용할 수 있다고 설명하고, 별도의 연구 시스템 글에서는 chat 대비 약 **15배 토큰**을 쓰는 multi-agent 연구 시스템 사례도 제시합니다. 따라서 high-value task가 아니면 경제성이 떨어질 수 있습니다. ([Claude][4])

---

## 4. Anthropic 에서 이야기하는 좋은 Multi Agent 설계 원칙

Anthropic 자료에서 반복적으로 나오는 원칙은 다음과 같습니다.

1. **단순한 것부터 시작한다.**
   단일 LLM, 단일 agent, prompt chaining으로 충분하면 거기서 멈춥니다. 복잡도는 성능 개선이 입증될 때만 추가합니다. ([Anthropic][1])

2. **문제 단위가 아니라 컨텍스트 단위로 쪼갠다.**
   “기획 agent / 구현 agent / 테스트 agent”처럼 역할명으로 기계적으로 나누면 오히려 정보 전달 손실이 커질 수 있습니다. Anthropic은 context-centric decomposition을 강조하며, 같은 문맥을 계속 봐야 하는 작업은 한 agent 안에 두는 것이 낫다고 설명합니다. ([Claude][4])

3. **병렬화는 속도보다 coverage를 위해 쓴다.**
   여러 agent를 병렬로 돌린다고 항상 더 빨라지는 것은 아닙니다. 오히려 토큰 사용량과 전체 시간이 늘 수 있습니다. 병렬화의 핵심 이득은 다양한 경로를 탐색하고 누락 가능성을 줄이는 것입니다. ([Claude][4])

4. **Orchestrator의 delegation 기준을 명시한다.**
   Anthropic의 multi-agent research system 글은 초기에 간단한 질의에도 과도하게 많은 subagent를 생성하는 문제가 있었다고 설명합니다. 해결책은 query complexity에 따라 subagent 수와 tool call budget을 제한하는 것입니다. ([Anthropic][5])

5. **검증 루프는 반드시 종료 조건을 가진다.**
   Generator-Verifier 패턴은 강력하지만, verifier가 부실하면 조기 성공을 선언하거나 루프가 멈추지 않을 수 있습니다. Claude 글은 구체적 기준, 충분한 검사, negative test, 명시적 실패 조건을 둬야 한다고 설명합니다. ([Claude][4])

---

## 5. Multi Agent 시스템은 Workflow Orchestration 에 불과합니다.

Multi Agent 시스템은 결국 **그래프 형태의 workflow orchestration**입니다. 순차 실행, 병렬 실행, 분기, 반복이라는 기본 제어흐름을 에이전트·도구·메모리 노드로 확장한 것입니다. 따라서 좋은 설계의 핵심은 “에이전트를 많이 쓰는 것”이 아니라, **컨텍스트를 어디서 분리할지, 어떤 작업을 병렬화할지, 어떤 전문성을 독립시킬지, 그리고 어디서 검증하고 멈출지**를 명확히 정하는 것입니다.

Anthropic 자료를 기준으로 하면, Multi Agent는 **context pollution 방지, 병렬 탐색, 전문화**가 필요한 경우에 강력합니다. 반대로 이 세 조건이 약하면 비용, latency, 디버깅 복잡도, 상태 관리 부담 때문에 단일 에이전트나 단순 workflow가 더 낫습니다. Claude Code와 Codex를 섞는 전략도 같은 원칙을 따릅니다. 하나를 primary orchestrator로 두고, 다른 하나를 독립 reviewer, adversarial verifier, rescue worker로 제한적으로 호출하는 구조가 가장 실용적입니다.

[1]: https://www.anthropic.com/engineering/building-effective-agents "Building Effective AI Agents \ Anthropic"
[2]: https://claude.com/blog/multi-agent-coordination-patterns "Multi-agent coordination patterns: Five approaches and when to use them | Claude"
[3]: https://docs.langchain.com/oss/python/langchain/multi-agent "Multi-agent - Docs by LangChain"
[4]: https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them "When to use multi-agent systems (and when not to) | Claude"
[5]: https://www.anthropic.com/engineering/multi-agent-research-system "How we built our multi-agent research system \ Anthropic"
[6]: https://github.com/openai/codex-plugin-cc "GitHub - openai/codex-plugin-cc: Use Codex from Claude Code to review code or delegate tasks. · GitHub"
[7]: https://docs.anthropic.com/en/docs/claude-code/cli-reference "CLI reference - Claude Code Docs"
[8]: https://docs.anthropic.com/en/docs/claude-code/mcp "Connect Claude Code to tools via MCP - Claude Code Docs"
[9]: https://developers.openai.com/codex/mcp "Model Context Protocol – Codex | OpenAI Developers"
[10]: https://developers.openai.com/codex/plugins "Plugins – Codex | OpenAI Developers"
