
## Claude Code × Codex 하이브리드 AI 코딩 에이전트 전략

여기서는 Claude Code와 Codex를 서로의 대체재가 아니라 **역할이 다른 전문 에이전트**로 봅니다.  
한쪽이 primary orchestrator를 맡고, 다른 쪽은 review, adversarial critique, rescue, parallel exploration을 맡게 하면 구조가 더 안정적입니다.

### 1 Claude Code 안에서 Codex 호출

`openai/codex-plugin-cc`는 Claude Code 안에서 Codex를 호출하는 플러그인입니다.  
이 자료는 로컬에 설치된 `codex@openai-codex` 1.0.4에서 확인한 slash command를 기준으로 합니다. 주요 명령은 `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, `/codex:status`, `/codex:result`, `/codex:cancel`입니다.

예를 들어 Claude Code가 구현을 맡고, Codex는 read-only review를 수행합니다.
`/codex:review`는 변경사항을 검토하는 read-only review 명령입니다. multi-file 변경처럼 범위가 넓을 때는 background 실행을 권장합니다. 여기서 `--background`는 Claude CLI 옵션이 아니라 `/codex:*` 플러그인 명령의 실행 플래그입니다.

```text
Claude Code:
  1. 요구사항 분석
  2. 구현
  3. 테스트 실행
  4. /codex:review --background
   /codex:adversarial-review --background
  6. Codex 결과 반영
```

`/codex:adversarial-review`는 구현의 가정, 설계 선택, trade-off, 숨은 리스크를 압박 검토하는 명령입니다. 단순 코드 리뷰보다 **반대편 변호사 역할**에 가깝습니다.

`/codex:rescue`는 Claude Code가 특정 버그나 막힌 작업을 Codex에 넘길 때 사용합니다. 설치된 플러그인 기준으로 `--background|--wait`, `--resume|--fresh`, `--model`, `--effort` 같은 실행 제어 플래그를 받을 수 있습니다.

### 2 Codex 안에서 Claude Code 호출

반대 방향도 필요합니다. 이때는 **Codex가 primary orchestrator를 맡고 Claude Code를 보조 검토 표면으로 활용**합니다.

다만 `claude -p` 방식은 제외합니다. Anthropic CLI 문서상 `claude -p`는 SDK query 후 종료하는 print mode 성격의 호출입니다. interactive session 보존과 Agent SDK credit / **usage credits** 방향성으로 설명드리는 것이 목표이므로, 설계 대상에서 제외합니다.

대신 다음 세 가지 방향을 사용할 수 있습니다.

#### A. Claude Code agents view와 별도 session 확인

Claude Code에는 background agent 관리를 위한 `claude agents` 하위 명령이 있고, `claude agents --json`으로 활성 session을 JSON으로 조회할 수 있습니다. 중요한 점은 `claude agents --json`이 실행 중인 session을 **조회**하는 명령이라는 것입니다. 새 작업을 script로 만들거나 log를 가져오는 명령은 아닙니다. ([Claude API Docs][7])

따라서 Claude Code의 agents view에서 사람이 별도 session을 만들고 Codex가 상태만 조회하거나, tmux bridge MCP 등으로 이미 열린 Claude Code interactive session에 요청을 보내는 편이 좋습니다.

#### B. Claude Code MCP server를 Codex에 연결

Claude Code는 `claude mcp serve`로 MCP server를 실행할 수 있고, 문서상 View, Edit, LS 같은 Claude Code 도구를 MCP 클라이언트에 노출할 수 있습니다. ([Claude API Docs][8])

Codex도 MCP 서버 연결을 지원합니다.  
Codex 문서는 `codex mcp` 명령과 설정 파일로 MCP 서버를 추가할 수 있다고 설명합니다. ([OpenAI Developers][9])

개념적으로는 다음과 같은 구조입니다.

```bash
codex mcp add claude-code -- claude mcp serve
```

주의할 점이 있습니다.  
이 방식이 곧 “Claude를 또 하나의 완전한 autonomous agent로 호출한다”는 뜻은 아닙니다.  
더 정확히는 **Claude Code의 tool surface를 Codex 쪽 MCP tool로 노출**하는 구조입니다. 
Claude 자체의 장기 추론·작업자 역할까지 원하면 Claude Code의 agents view나 tmux로 띄운 별도 interactive session도 함께 사용해야 합니다.

#### C. Codex plugin / custom agent로 Claude bridge 만들기

Codex는 plugin과 custom agent 구성을 지원합니다. Codex 문서에 따르면 plugin은 skills, apps, MCP servers를 번들링할 수 있고, custom agent에는 모델, sandbox, MCP, skill 등을 설정할 수 있습니다. ([OpenAI Developers][10])

따라서 프로젝트 내부에 “Claude Reviewer” 또는 “Claude Rescue Worker” 같은 Codex custom agent를 정의하고, 다음 원칙을 부여할 수 있습니다.

```text
- Claude 호출은 실제 CLI에 존재하는 agents view, MCP bridge, tmux bridge 표면만 사용한다.
- claude -p는 사용하지 않는다.
- Claude 결과는 agents JSON, MCP 응답, response/done marker, 또는 tmux pane transcript처럼 관찰 가능한 표면에서 회수한다.
- Claude가 수정 작업을 한다면 별도 worktree 또는 제한된 파일 범위에서만 수행한다.
- 최종 merge 판단은 Codex primary agent가 한다.
```

이렇게 구성하면 Codex 안에서도 Claude Code를 보조 검토 표면으로 연결할 수 있습니다.

---

## 6. 실무적으로 추천하는 Hybrid Workflow

### 기본형: Claude 구현 + Codex 검증

```text
Claude Code
  → 설계
  → 구현
  → 테스트
  → Codex review
  → Codex adversarial review
  → Claude 수정
  → 최종 테스트
```

이 구조가 가장 안정적입니다.  
Claude Code는 긴 문맥의 구현과 리팩터링을 맡고, Codex는 독립 검토자로 작동합니다.  
`codex-plugin-cc`가 이 방향을 직접 지원합니다. ([GitHub][6])

### 반대형: Codex 구현 + Claude Code 검증

```text
Codex
  → 구현 또는 수정
  → Claude Code agents view, MCP bridge, 또는 tmux bridge로 review session 분리
  → claude agents --json, MCP 응답, response/done marker, 또는 pane transcript로 결과 회수
  → Codex가 수정 여부 판단
```

이 구조에서는 Claude Code를 Codex의 보조 검토 표면으로 씁니다. 단, `claude -p`와 존재하지 않는 `claude --bg` 호출은 제외합니다. agents view, MCP bridge, tmux bridge처럼 실제로 검증 가능한 표면만 사용합니다. ([Claude API Docs][7])

### 고위험 변경: 양방향 독립 검증

보안, 결제, 인증, 마이그레이션, 대규모 리팩터링처럼 위험도가 높은 작업에는 다음 구조가 적합합니다.

```text
Primary Agent: 구현 책임
Secondary Agent: read-only adversarial review
Verifier: 테스트 / lint / typecheck / security scan
Human Gate: 최종 승인
```

여기서 핵심 원칙은 **두 에이전트가 동시에 같은 파일을 마음대로 수정하지 않게 하는 것**입니다. 한쪽은 primary implementer, 다른 한쪽은 read-only reviewer로 두는 것이 가장 안전합니다. 둘 다 수정해야 한다면 반드시 worktree, branch, file ownership, merge gate를 둬야 합니다.
