# Session 2-4 - 팀 개발 규칙을 자동화하는 훅 기반 워크플로우

> 팀 규칙은 문서, 스킬, 훅, 정책, 사람 승인으로 나누어 배치해야 오래 갑니다.

- 팀 규칙을 작업 시작 전, 파일 변경 후, 커밋 전, PR 전으로 나눕니다.
- 안내는 문서, 반복 절차는 스킬, 실행 전후 검사는 훅으로 배치합니다.
- 처음부터 완전 자동화하지 않고 제안, 알림, 일부 자동 실행 순서로 도입합니다.
- Agent OS 관점에서 AI Agent가 코드를 작성하게 두고, 사람은 정책·승인·검증 증거와 Agent 산출물 리뷰 기준을 설계합니다.

## 진행 흐름

1. 팀 규칙이 1개의 파일에 몰릴 때 생기는 유지보수 문제를 설명합니다.
2. 문서, 스킬, 훅, 정책, 사람 승인의 역할을 구분합니다.
3. 작업 시작 전, 파일 변경 후, 커밋 전, PR 전 단계 등 구체적인 워크플로우를 나눕니다.
4. Agent OS에서 사람과 AI Agent의 역할을 나눕니다 
 > Agent는 코드 작성·수정·검증 실행, 사람은 목표·금지선·승인 기준·증거 확인·산출물 리뷰.

## Claude Code를 쓴다면

Claude Code에서는 `CLAUDE.md`, Skills, Hooks, Settings가 서로 다른 역할을 맡습니다. 
`CLAUDE.md`에는 팀의 기본 작업 방식, Skills에는 반복 업무 절차, Hooks에는 자동 확인 절차, 
Settings에는 권한과 도구 설정을 둡니다.

한 파일에 모든 규칙을 넣으면 처음에는 편하지만 나중에 유지보수가 어려워지고 Context Rot 이 발생해 
결과물의 퀄리티가 떨어집니다.

## Codex를 쓴다면

Codex에서는 `AGENTS.md`, Skills, Hooks, Rules를 함께 설계합니다. 
`AGENTS.md`는 저장소 공통 지침, Skills는 반복 작업, Hooks는 이벤트 기반 확인, 
Rules는 sandbox 밖 명령의 허용·승인·차단 기준으로 나누는 방식이 자연스럽습니다.

## Agent OS 관점에서 사람의 역할

이 강의에서 코드는 사람이 처음부터 직접 작성하는 대상이 아닙니다.
AI Agent가 코드를 만들고 고치며 검증 명령까지 실행합니다. 
사람의 일은 더 앞과 뒤로 이동합니다.

| 사람의 역할 | Agent의 역할 | 남겨야 할 증거 |
|---|---|---|
| 목표와 제외 범위를 정한다 | 구현 후보를 제안한다 | 작업 계획, 제외 범위 |
| 위험 명령의 승인 기준을 정한다 | Python 훅으로 정책을 구현한다 | 허용/승인/차단 표, hook 결과 |
| 완료 기준을 정한다 | 포맷·린트·테스트를 실행한다 | `agent_verify.sh` 결과 |
| PR에서 볼 증거를 정한다 | 변경 diff와 검증 결과를 요약한다 | diff 요약, CI check |

Python 훅 코드를 직접 외워 쓰는 것이 목표는 아니지만, 이 코드는 AI Agent가 만든 실제 운영 산출물이므로 리뷰 대상입니다. 
핵심은 **팀이 어떤 행동을 자동 허용하고 어떤 행동은 멈춰야 하는지**를 정하고, 구현이 그 결정과 맞는지 확인하는 것입니다.

## Python 훅 구현을 리뷰하는 방법

Python 훅 구현은 개발자만 보는 내부 코드가 아닙니다. 
Agent OS 방식에서는 Agent가 작성한 코드가 팀 운영 규칙을 실제로 집행하므로, 사람은 아래 관점으로 구현을 읽습니다.

| 파일 | Agent가 구현한 것 | 사람이 확인할 질문 |
|---|---|---|
| `scripts/risky_command_policy.py` | hook payload를 읽고 위험 패턴이면 deny 결정 반환 | 차단 목록이 팀 정책과 맞는가? 허용해도 되는 명령을 과하게 막지 않는가? |
| `scripts/post_file_change_hook.py` | 파일 변경 뒤 문서 동기화, 포맷, 린트, 빠른 테스트 실행 | 저장할 때마다 돌려도 부담 없는 검사만 들어 있는가? 실패 로그가 사람이 읽을 수 있는가? |
| `scripts/stop_verify_hook.py` | Agent가 멈추기 전에 `agent_verify.sh`를 실행하고 실패 시 계속 작업하게 함 | 무한 루프를 막는 장치가 있는가? 최종 검증 실패가 조용히 묻히지 않는가? |
| `scripts/agent_verify.sh` | 사람·hook·CI가 함께 쓰는 단일 검증 진입점 | 사람이 직접 실행할 수 있는가? CI와 로컬 기준이 같은가? |

비개발 트랙에서는 전체 코드를 한 줄씩 설명하지 않아도 됩니다. 대신 입력, 결정, 실패 시 행동을 확인합니다. 개발자 트랙에서는 정규식, exit code, JSON 출력, subprocess 호출까지 함께 봅니다.

## 자주 하는 실수

| 이렇게 하지 않기 | 이렇게 바꾸기 |
|---|---|
| 팀 규칙을 전부 프롬프트에만 쓰기 | 문서, 스킬, 훅, 정책으로 분리 |
| 첫날부터 전부 자동 실행 | 제안과 알림부터 시작 |
| 실패 시 책임자를 정하지 않기 | AI 행동과 사람 확인을 분리 |
| 도구별 설정만 만들고 운영표를 안 만들기 | 단계별 워크플로우 표를 함께 유지 |

## Reference

- 공식 (Claude Code): [Hooks](https://code.claude.com/docs/en/hooks)
- 공식 (Claude Code): [Settings](https://code.claude.com/docs/en/settings)
- 공식 (Claude Code): [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- Claude Blog [How Claude Code works in large codebases: Best practices and where to start](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start)
- 공식 (Codex): [Hooks](https://developers.openai.com/codex/hooks)
- 공식 (Codex): [Rules](https://developers.openai.com/codex/rules)

## 실습 내용 설명

## 설계 방향성

핵심은 **팀 정책은 한 번만 정의하고**, Claude Code와 Codex는 그 정책을 서로 다른 훅 설정으로 호출하게 만드는 구조입니다. Claude Code는 프로젝트 공유 설정인 `.claude/settings.json`과 개인용 `.claude/settings.local.json`의 경계를 공식적으로 제공하고, 훅 matcher는 `Bash`, `Edit|Write`, `SessionStart` 같은 이벤트/도구 기준으로 동작합니다. ([Claude Code][1]) Codex도 `hooks.json` 또는 `config.toml` 기반 훅을 지원하지만, 프로젝트 `.codex/` 레이어는 신뢰된 경우에만 로드되고, non-managed command hook은 변경 시 review/trust가 필요합니다. ([OpenAI Developers][2])

패키지 구조는 다음과 같습니다.

```text
part4/lab/
  CLAUDE.md
  AGENTS.md

  docs/
    team-agent-policy.md
    architecture.md
    api-contract.md
    hook-review-checklist.md

  policy/
    agent-policy.json

  scripts/
    hook_common.py
    risky_command_policy.py
    post_file_change_hook.py
    pre_commit_guard.py
    pre_pr_guard.py
    stop_verify_hook.py
    session_context_hook.py
    user_prompt_guard.py
    changed_docs_check.py
    project_fast_check.sh
    agent_verify.sh
    smoke_test_hooks.sh

  .claude/
    settings.json
    settings.local.example.json
    skills/team-agent-workflow/SKILL.md

  .codex/
    hooks.json
    config.toml
    rules/default.rules

  .agents/
    skills/team-agent-workflow/SKILL.md

  .github/
    workflows/verify.yml
    CODEOWNERS
    RULESETS.md
```

## 팀 / 프로젝트 / 개인 관리 경계

| 영역       | 팀/조직 관리                              | 프로젝트 관리                                                  | 개인 관리                                                |
| -------- | ------------------------------------ | -------------------------------------------------------- | ---------------------------------------------------- |
| 기본 작업 방식 | 조직 Agent 정책, 보안 원칙                   | `CLAUDE.md`, `AGENTS.md`, `docs/*.md`                    | 개인 메모, 개인 prompt                                     |
| 반복 절차    | 공통 Skill 템플릿                         | `.claude/skills/**`, `.agents/skills/**`                 | `~/.claude/skills`, 개인 skill                         |
| 훅 실행     | managed settings, requirements, 보안 훅 | `.claude/settings.json`, `.codex/hooks.json`             | `.claude/settings.local.json`, `~/.codex/hooks.json` |
| 명령 승인    | 조직 차단 정책                             | `policy/agent-policy.json`, `.codex/rules/default.rules` | 개인 allow rule, 단 팀 정책 약화 금지                          |
| 최종 게이트   | GitHub Rulesets, required CI         | `.github/workflows/verify.yml`, CODEOWNERS               | 없음                                                   |

Skills는 반복 절차에만 두었습니다. Claude Code는 `SKILL.md` 기반 skill을 필요할 때 로드하는 방식이어서 긴 반복 절차를 `CLAUDE.md`에 계속 누적하지 않는 편이 낫고, Codex도 `SKILL.md`를 가진 skill directory를 재사용 워크플로우 단위로 인식합니다. ([Claude Code][3])

## 실제 훅 매핑

| 단계          | Claude Code                                     | Codex                                           | 공통 실행 파일                   |
| ----------- | ----------------------------------------------- | ----------------------------------------------- | -------------------------- |
| 작업 시작 전     | `SessionStart`                                  | `SessionStart`                                  | `session_context_hook.py`  |
| 사용자 요청 제출 전 | `UserPromptSubmit`                              | `UserPromptSubmit`                              | `user_prompt_guard.py`     |
| 명령/파일 변경 전  | `PreToolUse`                                    | `PreToolUse`                                    | `risky_command_policy.py`  |
| 승인 요청 시점    | `PermissionRequest`                             | `PermissionRequest`                             | `risky_command_policy.py`  |
| 파일 변경 직후    | `PostToolUse`                                   | `PostToolUse`                                   | `post_file_change_hook.py` |
| 커밋 전        | `PreToolUse`에서 `git commit` self-filter         | `PreToolUse`에서 `git commit` self-filter         | `pre_commit_guard.py`      |
| PR 전        | `PreToolUse`에서 `gh pr create/merge` self-filter | `PreToolUse`에서 `gh pr create/merge` self-filter | `pre_pr_guard.py`          |
| Agent 종료 전  | `Stop`                                          | `Stop`                                          | `stop_verify_hook.py`      |
| 최종 병합 게이트   | GitHub Actions + Rulesets                       | GitHub Actions + Rulesets                       | `agent_verify.sh`          |

Claude Code 쪽은 `PreToolUse`에서 `deny`, `ask`, `allow`류 결정을 더 직접적으로 표현할 수 있습니다. 반면 Codex의 `PreToolUse`는 현재 `deny`는 가능하지만 `permissionDecision: "ask"`는 아직 지원되지 않으므로, 패키지에서는 Codex의 승인성 작업을 `.codex/rules/default.rules`와 `PermissionRequest` 흐름으로 분리했습니다. ([Claude Code][1])

## 들어 있는 정책

`policy/agent-policy.json`에 공통 정책을 넣었습니다.

```json
{
  "protected_paths": [
    ".env",
    ".env.*",
    "secrets/**",
    "**/*.pem",
    "**/*.key"
  ],
  "governed_paths": [
    ".github/workflows/**",
    ".claude/settings.json",
    ".codex/hooks.json",
    ".codex/rules/**",
    "policy/**",
    "scripts/*hook*.py",
    "scripts/agent_verify.sh"
  ],
  "deny_command_patterns": [
    "rm -rf / 계열",
    "curl|wget pipe-to-shell",
    "chmod -R 777",
    "git push --force",
    "secret read",
    "disk format"
  ],
  "approval_command_patterns": [
    "git push",
    "publish/release",
    "terraform/kubectl/pulumi",
    "production DB",
    "history rewrite",
    "PR merge"
  ]
}
```

Codex 쪽은 `.codex/rules/default.rules`에도 sandbox 밖 명령 기준을 별도로 넣었습니다. Codex Rules는 `.rules` 파일의 `prefix_rule()`로 `allow`, `prompt`, `forbidden`을 정의하며, 공식 문서상 아직 experimental로 안내되어 있어 훅 정책 엔진과 CI를 함께 둔 3중 안전망으로 설계([OpenAI Developers][4])

## GitHub 안전망

`.github/workflows/verify.yml`의 job 이름은 `verify`입니다. GitHub Rulesets에서 required status check로 `verify`를 지정하면, AI Agent가 만든 PR이든 사람이 만든 PR이든 같은 `scripts/agent_verify.sh`를 통과해야 merge됩니다. GitHub Rulesets/branch protection은 required status checks, force push 차단, deletion 제한 같은 병합 게이트를 제공하고, push rulesets는 특정 파일 경로 push 차단에 사용할 수 있습니다. ([GitHub Docs][5])

## 적용

```bash
chmod +x scripts/*.py scripts/*.sh
bash scripts/agent_verify.sh --fast
bash scripts/agent_verify.sh
bash scripts/smoke_test_hooks.sh
```

Claude Code에서는 프로젝트에서 `/hooks`로 hook 로딩 상태를 확인하고, Codex에서는 프로젝트 `.codex/` 레이어를 trust한 뒤 `/hooks`에서 hook review/trust 상태를 확인하는 흐름으로 운영하면 됩니다. 패키지 내부 스크립트, JSON/TOML, shell syntax, smoke test는 검증해 두었습니다. 실제 조직 적용 시에는 GitHub Rulesets 화면에서 `verify` required check와 민감 파일 path restriction만 추가로 켜면 됩니다.

[1]: https://code.claude.com/docs/en/hooks "Hooks reference - Claude Code Docs"
[2]: https://developers.openai.com/codex/hooks "Hooks – Codex | OpenAI Developers"
[3]: https://code.claude.com/docs/ko/skills "Claude를 skills로 확장하기 - Claude Code Docs"
[4]: https://developers.openai.com/codex/rules "Rules – Codex | OpenAI Developers"
[5]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets?utm_source=chatgpt.com "Available rules for rulesets"
