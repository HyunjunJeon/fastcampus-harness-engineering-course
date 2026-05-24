# 팀 개발 규칙 자동화를 위한 Claude Code / Codex Hook 워크플로우

이 예제는 같은 정책 파일과 같은 Python/Bash 스크립트를 Claude Code와 Codex 양쪽에서 사용하도록 만든 실전형 구성입니다. 도구별로 다른 것은 훅 설정 파일과 이벤트 matcher뿐입니다.

## 핵심 설계

- 문서: 사람이 읽고 수정하는 계약 (`docs/team-agent-policy.md`, `docs/architecture.md`)
- 스킬: 반복 절차 (`.claude/skills/team-agent-workflow`, `.agents/skills/team-agent-workflow`)
- 훅: 이벤트 기반 자동 확인 (`scripts/*hook*.py`, `.claude/settings.json`, `.codex/hooks.json`)
- 정책: 기계가 읽는 결정표 (`policy/agent-policy.json`, `.codex/rules/default.rules`)
- 승인: 사람과 GitHub Rulesets/CODEOWNERS/required CI

## 설치

```bash
cp -R part4/lab/. /path/to/your/repo/
cd /path/to/your/repo
chmod +x scripts/*.py scripts/*.sh
bash scripts/agent_verify.sh --fast
```

## Claude Code 적용

- 프로젝트 공유 설정: `.claude/settings.json`
- 개인 override: `.claude/settings.local.json`를 만들고 커밋하지 않습니다.
- Claude Code 안에서 `/hooks`로 로드된 훅을 확인합니다.

주요 매핑:

| 단계 | 이벤트 | 실행 |
|---|---|---|
| 작업 시작 전 | `SessionStart`, `UserPromptSubmit` | 팀 정책 context 주입, bypass 요청 차단 |
| 실행 전 | `PreToolUse`, `PermissionRequest` | 위험 명령/경로 차단, governed file 승인 요청 |
| 파일 변경 후 | `PostToolUse` | JSON/TOML/Python/Shell 빠른 검사 |
| 커밋 전 | `PreToolUse` + `Bash(git commit*)` | `agent_verify.sh --fast` |
| PR 전 | `PreToolUse` + `Bash(gh pr create*)` | full verify + docs sync |
| 종료 전 | `Stop` | `agent_verify.sh` 실패 시 Agent continuation |

## Codex 적용

- 프로젝트 훅: `.codex/hooks.json`
- 프로젝트 설정: `.codex/config.toml`
- sandbox 밖 명령 규칙: `.codex/rules/default.rules`
- 프로젝트 `.codex/` layer를 신뢰해야 project-local hooks/rules가 로드됩니다.
- non-managed command hook은 변경될 때 trust review가 다시 필요합니다.

Codex는 `PreToolUse`에서 승인 요청을 직접 표현하기보다 `deny`와 Rules/PermissionRequest 조합을 사용합니다. 따라서 `risky_command_policy.py --runtime codex`는 차단해야 하는 것은 deny하고, 승인 요청 성격은 context를 추가한 뒤 Codex Rules가 prompt하게 둡니다.

Rules 테스트 예시:

```bash
codex execpolicy check --pretty \
  --rules .codex/rules/default.rules \
  -- gh pr create --fill
```

## GitHub CI / Rulesets

`.github/workflows/verify.yml`의 job 이름은 `verify`입니다. GitHub Rulesets에서 required status check로 `verify`를 지정합니다.

함께 켤 방어:

- Require PR before merging
- Require status checks to pass: `verify`
- Block force pushes
- Restrict deletions
- Restrict file paths: `.env`, `.env.*`, `secrets/**`, `**/*.pem`, `**/*.key`
- Require signed commits: 조직 정책에 맞으면 활성화

자세한 절차는 `.github/RULESETS.md`를 봅니다.

## 관리 책임 분리

| 파일/설정 | 관리 레벨 | 이유 |
|---|---|---|
| `docs/team-agent-policy.md` | 팀 | 사람이 읽는 운영 계약 |
| `policy/agent-policy.json` | 팀/플랫폼 | 훅이 읽는 결정표 |
| `scripts/*.py`, `scripts/agent_verify.sh` | 팀/플랫폼 | 실제 집행 코드 |
| `.claude/settings.json` | 프로젝트 | 레포별 Claude Code 훅/권한 |
| `.codex/hooks.json`, `.codex/rules/default.rules` | 프로젝트 | 레포별 Codex 훅/승인 규칙 |
| `.claude/settings.local.json`, `~/.codex/*` | 개인 | 개인 편의와 실험. 팀 정책을 약화하면 안 됨 |
| `.github/workflows/verify.yml`, Rulesets | 팀/조직 | 최종 merge gate |

## 검증

```bash
bash scripts/agent_verify.sh --fast
bash scripts/agent_verify.sh
python3 scripts/changed_docs_check.py
```

## 튜닝 지점

- `policy/agent-policy.json`: protected/governed path, deny/approval command regex, docs sync rule
- `.codex/rules/default.rules`: sandbox 밖 명령에 대한 allow/prompt/forbidden prefix
- `.claude/settings.json`: Claude permissions와 hook matcher
- `scripts/project_fast_check.sh`: 저장 직후 실행할 빠른 검사
