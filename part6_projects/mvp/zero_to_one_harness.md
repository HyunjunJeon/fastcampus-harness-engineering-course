실제 Agent Harness를 아래 네 층으로 나눕니다.

1. System Prompt        = 모든 에이전트가 따라야 하는 헌법
2. Multi Agent System   = 역할 분담, 상태머신, 작업 DAG
3. Hook                 = 파일 수정·명령 실행·완료 선언을 막거나 검증하는 강제 게이트
4. Skills               = PRD 작성, SPEC 분해, 테스트 생성처럼 반복되는 작업 절차

핵심은 **System Prompt와 Skills를 섞지 않는 것**입니다. System Prompt에는 변하지 않는 원칙만 넣고, 길고 반복적인 절차는 Skills로 빼야 합니다. Claude Code 문서도 `CLAUDE.md`는 행동을 유도하는 컨텍스트이지 강제 설정은 아니며, 행동을 차단하려면 `PreToolUse` hook 같은 강제 장치를 쓰라고 설명합니다. 또한 반복해서 붙여 넣는 절차나 체크리스트는 Skill로 빼는 것이 적합하다고 안내합니다. ([Claude][1])

---

# 1. 전체 디렉터리 구조

실제 하네스 구조는 이렇게 잡겠습니다.

```text
my-mvp-project/
├── AGENTS.md
├── CLAUDE.md
├── docs/
│   ├── prd.md
│   ├── mvp-scope.md
│   ├── roadmap.md
│   └── architecture.md
├── specs/
│   ├── SPEC-001-auth.md
│   └── SPEC-002-dashboard.md
├── tasks/
│   ├── TASK-001-auth-ui.yaml
│   ├── TASK-002-auth-api.yaml
│   └── TASK-003-dashboard-shell.yaml
├── harness/
│   ├── config.yaml
│   ├── system/
│   │   ├── core-system-prompt.md
│   │   ├── evidence-contract.md
│   │   ├── safety-contract.md
│   │   └── merge-contract.md
│   ├── agents/
│   │   ├── product-orchestrator.md
│   │   ├── spec-architect.md
│   │   ├── task-decomposer.md
│   │   ├── ui-scaffold-agent.md
│   │   ├── implementation-agent.md
│   │   ├── test-agent.md
│   │   ├── review-agent.md
│   │   └── integration-agent.md
│   ├── hooks/
│   │   ├── pre-tool-guard.mjs
│   │   ├── post-edit-validate.mjs
│   │   ├── diff-scope-check.mjs
│   │   ├── evidence-gate.mjs
│   │   └── dependency-guard.mjs
│   ├── skills/
│   │   ├── prd-to-mvp-scope/
│   │   │   ├── SKILL.md
│   │   │   ├── templates/
│   │   │   └── examples/
│   │   ├── spec-compiler/
│   │   │   ├── SKILL.md
│   │   │   ├── templates/
│   │   │   └── schemas/
│   │   ├── task-splitter/
│   │   │   ├── SKILL.md
│   │   │   ├── templates/
│   │   │   └── scripts/
│   │   ├── atomic-implementation/
│   │   │   ├── SKILL.md
│   │   │   └── checklists/
│   │   ├── failure-repair/
│   │   │   ├── SKILL.md
│   │   │   └── examples/
│   │   └── review-diff/
│   │       ├── SKILL.md
│   │       └── rubrics/
│   ├── schemas/
│   │   ├── task.schema.json
│   │   ├── evidence.schema.json
│   │   ├── spec.schema.json
│   │   └── agent-run.schema.json
│   └── runs/
│       └── <run-id>/
│           ├── prompt.md
│           ├── stdout.log
│           ├── stderr.log
│           ├── diff.patch
│           ├── evidence.json
│           └── summary.md
├── .claude/
│   ├── agents/
│   │   ├── spec-architect.md
│   │   ├── ui-scaffold-agent.md
│   │   ├── test-agent.md
│   │   └── review-agent.md
│   ├── skills/
│   │   ├── prd-to-mvp-scope/
│   │   ├── spec-compiler/
│   │   ├── task-splitter/
│   │   └── review-diff/
│   └── settings.json
├── .codex/
│   ├── agents/
│   │   ├── task-implementer.toml
│   │   ├── test-writer.toml
│   │   └── reviewer.toml
│   └── config.toml
├── .agents/
│   └── skills/
│       ├── atomic-implementation/
│       ├── failure-repair/
│       └── review-diff/
└── .github/
    └── workflows/
        ├── ci.yml
        ├── harness-validate.yml
        └── codex-review.yml
```

여기서 `AGENTS.md`는 Codex 쪽 canonical instruction으로 두고, `CLAUDE.md`는 `@AGENTS.md`를 import하게 둡니다. Codex는 작업 전 `AGENTS.md`를 읽고, global → project → nested directory 순서로 지침을 합칩니다. ([OpenAI 개발자][2]) Claude Code는 `CLAUDE.md`를 읽기 때문에, 이미 `AGENTS.md`를 쓰는 저장소라면 `CLAUDE.md`에서 `@AGENTS.md`로 import하라고 공식 문서가 안내합니다. ([Claude][1])

---

# 2. System Prompt

System Prompt는 에이전트에게 **무엇을 절대 어기면 안 되는가**를 알려주는 층입니다.

```text
1. 권한 체계
2. 작업 상태머신
3. 산출물 계약
4. 실패 시 행동 규칙
```

예시는 이렇게 잡겠습니다.

```markdown
# Core

You are an agent operating inside an Agent Harness for MVP development.

Your job is not to maximize code output.
Your job is to produce small, reviewable, verifiable changes that satisfy the assigned task.

## Authority Order

Follow instructions in this order:

1. Safety and security constraints
2. Harness system prompt
3. AGENTS.md / CLAUDE.md project rules
4. Current SPEC
5. Current TASK file
6. User request
7. Local style inference from existing code

When two instructions conflict, follow the higher-priority instruction and report the conflict.

## Operating Model

Every change must trace back to:

- PRD
- MVP Scope
- SPEC
- TASK
- Acceptance Criteria
- Validation Evidence

Never implement work that is not required by the current TASK.

## Task Boundary

You may only modify files listed in `allowed_paths`.
You must not modify files listed in `forbidden_paths`.
You must not add production dependencies unless the TASK explicitly allows it.
You must not change database schema, auth behavior, billing behavior, or deployment config unless explicitly allowed.

## Completion Standard

A task is not complete because code was written.
A task is complete only when:

1. the requested diff exists,
2. validation commands were run,
3. results are recorded,
4. acceptance criteria are mapped to pass/fail,
5. evidence.json is produced.

## Failure Behavior

If validation fails:

1. identify the smallest likely cause,
2. attempt one minimal repair if it stays within scope,
3. rerun the failing command,
4. record the final state honestly.

Never claim success if a validation command failed.
Never hide, delete, or weaken tests to pass validation.
```

이 System Prompt는 **짧고 강해야 합니다**. 
PRD 작성법, SPEC 작성법, 테스트 작성법 같은 상세 작업 절차는 여기에 넣지 않습니다. 
그런 내용은 Skills로 빼야 합니다.

---

# 3. Multi Agent System

Multi Agent System은 “에이전트가 많다”가 아니라, **각 에이전트가 서로 다른 책임과 권한을 갖는 구조**입니다. Claude Code의 subagent는 별도 context window, custom system prompt, 특정 tool access, 독립 permission을 가질 수 있어 역할별 분리에 적합합니다. ([Claude Platform Docs][3]) Codex도 subagent workflow를 통해 여러 전문 agent를 병렬로 실행하고 결과를 모아 하나의 응답으로 통합할 수 있으며, 복잡하고 병렬성이 높은 코드 탐색·기능 구현에 적합하다고 설명합니다. ([OpenAI 개발자][4])

나는 다음과 같이 나눕니다.

```text
Human Owner
  └── Product Orchestrator
        ├── PRD Writer
        ├── MVP Scope Cutter
        ├── Spec Architect
        ├── Task Decomposer
        ├── UI Scaffold Agent
        ├── Implementation Agent Pool
        ├── Test Agent
        ├── Review Agent
        ├── Integration Agent
        └── Release Agent
```

각 agent의 책임은 이렇게 분리합니다.

| Agent                     | 책임                                          | 주 도구                     | 수정 권한              |
| ------------------------- | ------------------------------------------- | ------------------------ | ------------------ |
| Product Orchestrator      | 전체 상태머신, 승인 지점, 작업 DAG 관리                   | Harness CLI              | 제한적                |
| PRD Writer                | 문제, 사용자, 목표, non-goal 작성                    | Claude / ChatGPT         | docs only          |
| MVP Scope Cutter          | Core / Support / Later / Kill 분류            | Claude / ChatGPT         | docs only          |
| Spec Architect            | PRD를 SPEC으로 변환                              | Claude Code subagent     | specs only         |
| Task Decomposer           | SPEC을 TASK YAML로 분해                         | Claude / Codex           | tasks only         |
| UI Scaffold Agent         | route, layout, component boundary 생성        | Claude Code              | UI paths           |
| Implementation Agent Pool | atomic task 병렬 구현                           | Codex                    | allowed_paths only |
| Test Agent                | unit/integration/e2e test 작성                | Codex / Claude           | tests only         |
| Review Agent              | diff와 acceptance criteria 검토                | Codex / Claude           | read-only          |
| Integration Agent         | branch/worktree 병합, 충돌 처리                   | Harness + human approval | controlled         |
| Release Agent             | release note, known issues, next roadmap 작성 | Codex / Claude           | docs only          |

중요한 점은 **Claude와 Codex를 경쟁시키지 않고 보완하도록 만드는 것**입니다.

```text
Claude Code:
- 큰 맥락 읽기
- 구조 설계
- 화면 골격
- 컴포넌트 경계
- 복잡한 다중 파일 refactor 계획

Codex:
- 작게 쪼갠 task 구현
- 병렬 worker
- CI / non-interactive validation
- PR review
- failure repair
```

Codex는 `codex exec`로 스크립트나 CI에서 비대화형으로 실행할 수 있고, read-only sandbox가 기본이며 필요한 경우 `workspace-write`처럼 권한을 명시적으로 올릴 수 있습니다. ([OpenAI 개발자][5]) Codex GitHub Action도 CI/CD job, patch 적용, PR review에 사용할 수 있으며 `codex exec`를 지정한 permission 하에서 실행합니다. ([OpenAI 개발자][6])

---

## Claude Code subagent 예시

`.claude/agents/spec-architect.md`

```markdown
---
name: spec-architect
description: Use when PRD and MVP scope must be converted into implementation-ready SPEC files.
tools: Read, Write, Edit, Glob, Grep
model: sonnet
---

You are the Spec Architect for this Agent Harness project.

Your job:
- Read docs/prd.md and docs/mvp-scope.md.
- Produce one SPEC per coherent feature slice.
- Make every SPEC implementation-ready.
- Include data contracts, routes, acceptance criteria, test requirements, and out-of-scope items.

Rules:
- Do not write implementation code.
- Do not invent hidden product requirements.
- Flag ambiguity explicitly.
- Keep each SPEC small enough to split into atomic TASK files.

Output:
- specs/SPEC-xxx-<name>.md
- summary of assumptions
- unresolved product questions
```

Claude Code의 custom subagent는 Markdown file + YAML frontmatter로 정의할 수 있고, 프로젝트 단위 subagent는 `.claude/agents/`에 저장해 팀과 공유하기 좋습니다. ([Claude Platform Docs][3])

---

## Codex custom agent 예시

`.codex/agents/task-implementer.toml`

```toml
name = "task-implementer"
description = "Implements one atomic TASK YAML with strict path boundaries and validation evidence."

developer_instructions = """
You are an implementation worker inside an Agent Harness.

Read:
- AGENTS.md
- the assigned TASK yaml
- the parent SPEC
- relevant source files only

Rules:
- Implement exactly one TASK.
- Stay within allowed_paths.
- Do not modify forbidden_paths.
- Do not add dependencies unless explicitly allowed.
- Prefer minimal, reviewable diffs.
- Run validation commands from the TASK.
- Produce a clear final summary with changed files, commands run, results, and risks.

If the task cannot be completed under these constraints, stop and report why.
"""

sandbox_mode = "workspace-write"
model_reasoning_effort = "medium"
```

Codex custom agent는 project-scoped `.codex/agents/` 또는 user-level `~/.codex/agents/` 아래 TOML 파일로 정의할 수 있고, 각 파일에는 `name`, `description`, `developer_instructions`가 필요합니다. ([OpenAI 개발자][4])

---

# 4. Hook

Hook은 에이전트가 “좋은 의도”로 규칙을 따르길 기대하는 층이 아닙니다. **어기면 막는 층**입니다.

Claude Code hooks는 session, prompt, tool call, file change, worktree lifecycle 등 특정 시점에 shell command, HTTP endpoint, LLM prompt를 실행할 수 있게 해줍니다. 특히 `PreToolUse`는 tool call 실행 전에 동작하고 차단할 수 있습니다. ([Claude Platform Docs][7]) Codex hooks도 `PreToolUse`, `PostToolUse`, `PermissionRequest`, `Stop` 같은 event와 matcher, hook handler 구조를 갖습니다. ([OpenAI 개발자][8])

내가 둘 hook은 최소 다섯 개입니다.

```text
1. prompt-intake hook
   - TASK 없는 구현 요청 차단
   - PRD/SPEC/TASK traceability 확인

2. pre-tool-guard hook
   - rm -rf, secret access, package manager install, migration 실행 차단
   - allowed_paths / forbidden_paths 검사

3. post-edit-validate hook
   - Edit/Write 이후 lint 대상 기록
   - package.json 변경 감지
   - schema 변경 감지

4. evidence-gate hook
   - Stop 시점에 evidence.json 없으면 완료 선언 차단
   - validation command 결과 없으면 needs_review 처리

5. diff-scope-check hook
   - git diff가 TASK allowed_paths 밖을 건드리면 실패
   - changed files와 TASK 계약 비교
```

다만 Codex 문서는 `PreToolUse`가 guardrail이지 완전한 enforcement boundary는 아니며, 일부 shell call이나 non-shell tool call은 가로채지 못할 수 있다고 명시합니다. 그래서 hook만 믿으면 안 되고, **run 종료 후 git diff 기반의 별도 검증**을 반드시 둬야 합니다. ([OpenAI 개발자][8])

---

## Claude hook 설정 예시

`.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "node harness/hooks/session-context.mjs"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "node harness/hooks/pre-tool-guard.mjs"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "node harness/hooks/post-edit-validate.mjs"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node harness/hooks/evidence-gate.mjs"
          }
        ]
      }
    ]
  }
}
```

---

## Codex hook 설정 예시

`.codex/config.toml`

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = 'node "$(git rev-parse --show-toplevel)/harness/hooks/pre-tool-guard.mjs"'
timeout = 30
statusMessage = "Checking command against harness policy"

[[hooks.PreToolUse]]
matcher = "^apply_patch$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = 'node "$(git rev-parse --show-toplevel)/harness/hooks/patch-scope-guard.mjs"'
timeout = 30
statusMessage = "Checking patch scope"

[[hooks.PostToolUse]]
matcher = "^Bash$"

[[hooks.PostToolUse.hooks]]
type = "command"
command = 'node "$(git rev-parse --show-toplevel)/harness/hooks/post-command-review.mjs"'
timeout = 30
statusMessage = "Reviewing command output"
```

Codex hook command는 `stdin`으로 JSON object를 받고, `PreToolUse`에서는 `permissionDecision: "deny"` 형태로 tool call을 차단할 수 있습니다. ([OpenAI 개발자][8])

---

## pre-tool-guard.mjs 예시

```js
#!/usr/bin/env node

import fs from "node:fs";

const input = JSON.parse(fs.readFileSync(0, "utf8"));
const taskPath = process.env.HARNESS_TASK_FILE;

function deny(reason) {
  console.log(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: input.hook_event_name || "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: reason
    }
  }));
  process.exit(0);
}

if (!taskPath || !fs.existsSync(taskPath)) {
  deny("No HARNESS_TASK_FILE is set. Implementation work requires an explicit TASK file.");
}

const taskText = fs.readFileSync(taskPath, "utf8");

const command =
  input?.tool_input?.command ||
  input?.tool_input?.cmd ||
  "";

const destructivePatterns = [
  /rm\s+-rf\s+\//,
  /git\s+push\s+--force/,
  /npm\s+install\s+/,
  /pnpm\s+add\s+/,
  /yarn\s+add\s+/,
  /prisma\s+migrate/,
  /db\s+push/
];

for (const pattern of destructivePatterns) {
  if (pattern.test(command)) {
    deny(`Blocked command by harness policy: ${command}`);
  }
}

if (command.includes("package.json") && !taskText.includes("allow_dependencies: true")) {
  deny("Dependency or package.json change is not allowed by this TASK.");
}

process.exit(0);
```

이 hook은 완전한 보안 시스템은 아니지만, 에이전트가 자주 하는 위험 행동을 초기에 막는 데 충분히 효과적입니다. 최종 enforcement는 반드시 `git diff --name-only`와 TASK YAML을 비교하는 `diff-scope-check`에서 다시 해야 합니다.

---

# 5. Skills

Skills는 “반복 가능한 작업법”입니다. PRD 작성, SPEC 컴파일, TASK 분해, 실패 복구, 리뷰 같은 작업은 매번 같은 절차를 반복하므로 Skill로 만들어야 합니다.

Claude Code의 Skill은 `SKILL.md`를 중심으로 instruction, supporting files, scripts, reference docs를 담는 구조이며, 필요할 때만 본문을 load해 context 비용을 줄입니다. ([Claude Platform Docs][9]) Codex의 Agent Skills도 task-specific capability를 확장하기 위한 형식이고, `SKILL.md`와 optional scripts, references, assets를 포함할 수 있습니다. ([OpenAI 개발자][10])

내가 둘 핵심 Skills는 다음입니다.

```text
prd-to-mvp-scope
spec-compiler
task-splitter
ui-scaffold
atomic-implementation
test-generator
failure-repair
review-diff
release-summarizer
```

각 Skill은 아래 구성으로 둡니다.

```text
harness/skills/task-splitter/
├── SKILL.md
├── templates/
│   └── task-template.yaml
├── schemas/
│   └── task.schema.json
├── examples/
│   ├── good-task.yaml
│   └── bad-task.yaml
└── scripts/
    └── validate-task.mjs
```

---

## task-splitter Skill 예시

`harness/skills/task-splitter/SKILL.md`

```markdown
---
name: task-splitter
description: Convert one implementation-ready SPEC into atomic TASK YAML files for parallel AI coding agents.
---

# Task Splitter Skill

Use this skill when a SPEC must be decomposed into small, verifiable implementation tasks.

## Inputs

Required:
- One SPEC file under `specs/`
- `docs/architecture.md`
- `docs/mvp-scope.md`
- Existing task files under `tasks/`

## Output

Create one or more TASK files under `tasks/`.

Each TASK must include:

- id
- title
- parent spec
- goal
- allowed_paths
- forbidden_paths
- depends_on
- parallel_group
- risk_level
- acceptance criteria
- validation commands
- expected outputs

## Splitting Rules

A good TASK:
- has one clear outcome,
- can be reviewed as a small diff,
- avoids touching the same files as another parallel task,
- has validation commands,
- has explicit file boundaries.

A bad TASK:
- says "implement dashboard",
- touches frontend, backend, database, and tests at once,
- adds dependencies without approval,
- lacks test requirements,
- depends on hidden assumptions.

## Parallelization Rules

Mark tasks as parallel only when:
- their allowed_paths do not overlap,
- they do not require the same data contract to be changed,
- one does not depend on the output of the other.

## Required Final Response

Return:
- list of created task files
- dependency graph summary
- tasks safe to run in parallel
- tasks requiring human review
- unresolved ambiguity
```

---

## atomic-implementation Skill 예시

`.agents/skills/atomic-implementation/SKILL.md`

````markdown
---
name: atomic-implementation
description: Implement exactly one Agent Harness TASK YAML with strict scope control and validation evidence.
---

# Atomic Implementation Skill

Use this skill when implementing one TASK file.

## Required Reading

Read these files before editing:
- AGENTS.md
- assigned TASK YAML
- parent SPEC
- relevant existing code

## Implementation Rules

- Modify only files in `allowed_paths`.
- Never modify files in `forbidden_paths`.
- Do not add dependencies unless `allow_dependencies: true`.
- Do not change public contracts unless the TASK says so.
- Do not broaden the feature.
- Prefer minimal diffs.

## Validation

Run every command listed under `validation.commands`.

For each command, record:
- command
- status
- duration
- relevant output
- failure summary, if failed

## Evidence

Produce or update:

```text
harness/runs/<run-id>/evidence.json
harness/runs/<run-id>/summary.md
````

## Completion

You may say the task is complete only if:

* all required acceptance criteria are satisfied,
* validation results are recorded,
* no forbidden files were changed,
* remaining risks are explicitly listed.

````

Codex Skills는 repo, user, admin, system 위치에서 읽을 수 있고, repo에서는 `.agents/skills`를 스캔합니다. Skill은 명시적으로 호출하거나, 설명이 task와 맞을 때 암묵적으로 선택될 수 있습니다. :contentReference[oaicite:15]{index=15}

---

# 6. 네 층을 어떻게 연결할 것인가

실제 실행 흐름은 이렇게 잡습니다.

```text
User idea
  ↓
prd-to-mvp-scope skill
  ↓
Product Orchestrator
  ↓
spec-compiler skill
  ↓
Spec Architect agent
  ↓
task-splitter skill
  ↓
Task Decomposer agent
  ↓
Harness DAG builder
  ↓
UI Scaffold Agent, Claude Code
  ↓
Implementation Agent Pool, Codex
  ↓
Hooks: path guard, dependency guard, evidence gate
  ↓
Test Agent
  ↓
Review Agent
  ↓
Integration Agent
  ↓
Release Agent
````

이를 CLI로 표현하면 다음과 같습니다.

```bash
harness init

harness prd create \
  --idea docs/idea.md \
  --skill prd-to-mvp-scope

harness spec compile \
  --from docs/mvp-scope.md \
  --agent spec-architect

harness tasks split \
  --spec specs/SPEC-002-dashboard.md \
  --skill task-splitter

harness scaffold \
  --task TASK-003-dashboard-shell \
  --agent claude:ui-scaffold-agent

harness run \
  --parallel wave-1 \
  --agent codex:task-implementer \
  --skill atomic-implementation

harness validate

harness review \
  --agent codex:reviewer \
  --skill review-diff

harness integrate

harness release
```

여기서 `harness run --parallel wave-1`은 task graph를 보고 서로 충돌하지 않는 task만 동시에 실행합니다.

```yaml
wave: wave-1
max_parallel: 4

tasks:
  - TASK-003-dashboard-shell
  - TASK-004-run-status-card
  - TASK-005-failed-task-list
  - TASK-006-task-evidence-panel

locks:
  TASK-003-dashboard-shell:
    - src/app/dashboard/**
    - src/components/dashboard/layout/**
  TASK-004-run-status-card:
    - src/components/dashboard/RunStatusCard.tsx
    - tests/components/RunStatusCard.test.tsx
  TASK-005-failed-task-list:
    - src/components/dashboard/FailedTaskList.tsx
    - tests/components/FailedTaskList.test.tsx
```

---

# 7. 실제로 필요한 계약 파일

Agent Harness에서 가장 중요한 파일은 `TASK.yaml`과 `evidence.json`입니다.

## TASK 예시

```yaml
id: TASK-004
title: "Create RunStatusCard component"
spec: SPEC-002-dashboard
status: ready
risk_level: low
agent_preference: codex
skill: atomic-implementation

depends_on:
  - TASK-003

parallel_group: wave-1-dashboard-components

allowed_paths:
  - "src/components/dashboard/RunStatusCard.tsx"
  - "src/components/dashboard/RunStatusCard.stories.tsx"
  - "tests/components/RunStatusCard.test.tsx"

forbidden_paths:
  - "package.json"
  - "src/db/**"
  - "src/auth/**"
  - "src/app/api/**"

goal: >
  Implement a presentational RunStatusCard component that displays a harness run status,
  started time, finished time, agent name, and validation summary.

acceptance:
  - "Component accepts a HarnessRun prop"
  - "Component renders queued, running, passed, failed, and needs_review states"
  - "Component has accessible labels for status"
  - "Component has unit tests for every status"
  - "No production dependency is added"

validation:
  commands:
    - "npm run lint"
    - "npm run test -- RunStatusCard"

outputs:
  - "src/components/dashboard/RunStatusCard.tsx"
  - "tests/components/RunStatusCard.test.tsx"
  - "harness/runs/${RUN_ID}/evidence.json"
```

## evidence.json 예시

```json
{
  "run_id": "2026-06-29T12-00-00Z-TASK-004",
  "task_id": "TASK-004",
  "agent": "codex:task-implementer",
  "skill": "atomic-implementation",
  "base_sha": "abc123",
  "head_sha": "def456",
  "changed_files": [
    "src/components/dashboard/RunStatusCard.tsx",
    "tests/components/RunStatusCard.test.tsx"
  ],
  "scope_check": {
    "status": "passed",
    "forbidden_paths_touched": []
  },
  "validation": [
    {
      "command": "npm run lint",
      "status": "passed",
      "duration_ms": 4210
    },
    {
      "command": "npm run test -- RunStatusCard",
      "status": "passed",
      "duration_ms": 6880
    }
  ],
  "acceptance": [
    {
      "criterion": "Component accepts a HarnessRun prop",
      "status": "passed"
    },
    {
      "criterion": "Component renders queued, running, passed, failed, and needs_review states",
      "status": "passed"
    },
    {
      "criterion": "No production dependency is added",
      "status": "passed"
    }
  ],
  "merge_recommendation": "mergeable",
  "risks": []
}
```

---

# 8. System Prompt / Multi Agent / Hook / Skills의 책임 경계

이 네 층은 다음처럼 구분합니다.

| 항목                 | 넣을 것                                   | 넣지 말 것                      |
| ------------------ | -------------------------------------- | --------------------------- |
| System Prompt      | 불변 원칙, 권한 순서, 실패 규칙, evidence 기준       | PRD 작성법, 상세 테스트 절차, 긴 체크리스트 |
| Multi Agent System | 역할, agent manifest, 상태머신, DAG, 병렬화 규칙  | 개별 구현 코드                    |
| Hook               | 차단, 검증, 로그, evidence 강제, diff scope 검사 | 창의적 판단, 제품 의사결정             |
| Skills             | 반복 작업 절차, 템플릿, 예시, scripts, rubrics    | 절대 규칙, 보안 강제 장치             |

짧게 말하면:

```text
System Prompt는 “항상 지킬 법”
Multi Agent System은 “누가 무엇을 할지”
Hook은 “어기면 막는 장치”
Skills는 “일 잘하는 방법”
```

---

# 9. MVP 개발용 최소 세트

처음부터 모든 걸 만들 필요는 없습니다. MVP용 하네스는 아래 정도면 충분합니다.

```text
필수 System Prompt
- core-system-prompt.md
- evidence-contract.md
- safety-contract.md

필수 Agents
- product-orchestrator
- spec-architect
- task-decomposer
- implementation-agent
- review-agent

필수 Hooks
- pre-tool-guard
- diff-scope-check
- evidence-gate
- dependency-guard

필수 Skills
- prd-to-mvp-scope
- spec-compiler
- task-splitter
- atomic-implementation
- failure-repair
- review-diff
```

이 정도만 있어도 다음이 가능합니다.

```text
아이디어 입력
→ PRD 생성
→ MVP 범위 컷
→ SPEC 생성
→ TASK 분해
→ Claude Code로 화면 골격 생성
→ Codex worker로 TASK 병렬 구현
→ Hook으로 범위 위반 차단
→ evidence.json 기반 검증
→ Review Agent가 merge 가능 여부 판단
```

---

# 10. 결론적으로 내가 설계할 하네스

내가 이 하네스를 실제로 만든다면 핵심 철학은 이렇습니다.

> Agent Harness는 AI에게 “더 자유롭게 코딩해줘”라고 말하는 도구가 아니다.
> 오히려 AI가 제품 개발 안에서 안전하게 일할 수 있도록 자유도를 줄이고, 작업 단위와 검증 기준을 강제하는 시스템이다.

따라서 네 층은 이렇게 설계합니다.

```text
System Prompt
- 모든 agent run에 공통 주입
- 범위, 권한, evidence, 실패 행동을 정의

Multi Agent System
- PRD, SPEC, TASK, 구현, 테스트, 리뷰, 병합을 역할별로 분리
- Claude는 구조화와 scaffold
- Codex는 atomic task 병렬 구현과 CI 검증

Hook
- 에이전트의 행동을 사후 신뢰하지 않고 실행 중 차단
- allowed_paths, forbidden_paths, dependency, secret, evidence 강제

Skills
- 반복 가능한 개발 절차를 패키징
- PRD 작성법, SPEC 작성법, TASK 분해법, failure repair, review rubric 제공
```

가장 중요한 설계 판단은 이것입니다.

```text
System Prompt는 짧게.
Agent는 역할별로.
Hook은 엄격하게.
Skill은 풍부하게.
```

이렇게 해야 Claude Code와 Codex가 단순한 코드 생성기가 아니라, **MVP 개발 파이프라인 안에서 서로 다른 책임을 가진 작업자들**처럼 움직입니다.

[1]: https://code.claude.com/docs/en/memory "How Claude remembers your project - Claude Code Docs"
[2]: https://developers.openai.com/codex/guides/agents-md "Custom instructions with AGENTS.md – Codex | OpenAI Developers"
[3]: https://docs.anthropic.com/en/docs/claude-code/sub-agents "Create custom subagents - Claude Code Docs"
[4]: https://developers.openai.com/codex/subagents "Subagents – Codex | OpenAI Developers"
[5]: https://developers.openai.com/codex/noninteractive "Non-interactive mode – Codex | OpenAI Developers"
[6]: https://developers.openai.com/codex/github-action "GitHub Action – Codex | OpenAI Developers"
[7]: https://docs.anthropic.com/en/docs/claude-code/hooks "Hooks reference - Claude Code Docs"
[8]: https://developers.openai.com/codex/hooks "Hooks – Codex | OpenAI Developers"
[9]: https://docs.anthropic.com/en/docs/claude-code/skills "Extend Claude with skills - Claude Code Docs"
[10]: https://developers.openai.com/codex/skills "Agent Skills – Codex | OpenAI Developers"
