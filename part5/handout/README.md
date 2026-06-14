# Part 5 Handout - Hybrid Agent Harness 구축 워크숍

Part 5는 멀티 에이전트 개념 설명이 아니라, Claude Code와 Codex를 역할별로 연결하고 파일, hook, skill, eval로 작업을 고정하는 실습형 워크숍입니다.

## 실행 원칙

모든 세션은 아래 패턴으로 실행합니다.

```bash
cd part5/lab
bash scripts/run_session.sh <session-id>
bash scripts/check.sh --session <session-id>
```

전체 검증:

```bash
cd part5/lab
bash scripts/check.sh
```

## 세션 목록

| 세션 | 파일 | 실행 ID |
| --- | --- | --- |
| 사전 환경 점검 | [00-preflight-handout.md](./00-preflight-handout.md) | `00-preflight` |
| 서브에이전트와 context isolation | [01-01-subagent-context-isolation-handout.md](./01-01-subagent-context-isolation-handout.md) | `01-01` |
| Explorer / Implementer / Verifier | [01-02-role-split-handout.md](./01-02-role-split-handout.md) | `01-02` |
| SubAgent to Main handoff | [01-03-sub-to-main.md](./01-03-sub-to-main.md) | `01-03` |
| 멀티 에이전트 패턴 선택 | [02-01-multi-agent-patterns-handout.md](./02-01-multi-agent-patterns-handout.md) | `02-01` |
| 멀티 에이전트 no-go | [02-02-multi-agent-no-go-handout.md](./02-02-multi-agent-no-go-handout.md) | `02-02` |
| Claude Code -> Codex 플러그인 | [02-03a-claude-to-codex-plugin-handout.md](./02-03a-claude-to-codex-plugin-handout.md) | `02-03a` |
| Codex -> Claude tmux bridge | [02-03b-codex-to-claude-tmux-mcp-handout.md](./02-03b-codex-to-claude-tmux-mcp-handout.md) | `02-03b` |
| 직접 tmux script bridge | [02-03c-direct-tmux-bridge-handout.md](./02-03c-direct-tmux-bridge-handout.md) | `02-03c` |
| `claude -p` guard hook | [02-03d-claude-print-guard-hook-handout.md](./02-03d-claude-print-guard-hook-handout.md) | `02-03d` |
| Channels / Remote Control | [02-03e-channels-remote-control-handout.md](./02-03e-channels-remote-control-handout.md) | `02-03e` |
| 하네스가 모델보다 중요한 이유 | [03-01-why-harness-matters-handout.md](./03-01-why-harness-matters-handout.md) | `03-01` |
| 최소 하네스 | [03-02-minimum-harness-handout.md](./03-02-minimum-harness-handout.md) | `03-02` |
| SDD spec/plan/tasks | [03-03-sdd-spec-plan-tasks-handout.md](./03-03-sdd-spec-plan-tasks-handout.md) | `03-03` |
| Skill / Hook / Eval | [03-04-skill-hook-eval-handout.md](./03-04-skill-hook-eval-handout.md) | `03-04` |
| Harness Retro | [03-05-harness-retro-handout.md](./03-05-harness-retro-handout.md) | `03-05` |
| Capstone | [04-01-capstone-handout.md](./04-01-capstone-handout.md) | `04-01` |

## Reference Source

`tmux-bridge-mcp`는 커뮤니티 MCP이므로, 강의 검토용 upstream 소스 스냅샷을 [../vendor/tmux-bridge-mcp](../vendor/tmux-bridge-mcp)에 보관합니다.
핵심 TypeScript 소스에는 강의용 한국어 주석과 JSDoc을 추가해 MCP tool, tmux pane 조작, read-before-act guard를 코드 수준에서 읽을 수 있게 했습니다.
