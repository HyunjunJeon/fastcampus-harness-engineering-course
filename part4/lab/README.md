# Part 4 실습 레포 (`lab/`)

Part 4의 모든 세션은 이 한 저장소를 점점 채워나가는 방식으로 진행합니다. handout이 "무엇을 하는가"라면, 이 레포는 "어디에 두는가"입니다.

## 두 가지 트랙

| 트랙 | 만지는 폴더 | 검증 방법 |
|---|---|---|
| 비개발 트랙 | `workflows/`, `docs/`, `.claude/`, `.codex/`, `.agents/`, `scripts/` 일부 | `bash scripts/agent_verify.sh --docs-only` |
| 개발자 트랙 | 위 + `app/`, `tests/` | `bash scripts/agent_verify.sh` |

비개발 트랙은 마크다운, 스킬 정의, 정책 파일, 문서 동기화만 다룹니다. 개발자 트랙은 같은 레포에서 FastAPI 메모 API에 기능을 더하면서 동일한 검증 루프를 통과시킵니다.

## 폴더 지도

```
lab/
  CLAUDE.md                 # Claude Code용 프로젝트 규칙
  AGENTS.md                 # Codex용 동일 규칙 미러
  workflows/                # 도구 중립적인 스킬 원본
  common_skills/            # Claude/Codex에 함께 배포할 공통 스킬 원본
  .claude/skills/           # Claude Code 배포 (common_skills 링크)
  .agents/skills/           # Codex 배포 (common_skills 링크)
  .codex/                   # Codex 훅·설정
  scripts/                  # 공통 검증·정책 스크립트와 Post/Stop 훅 래퍼
  .github/workflows/        # CI 게이트
  docs/                     # 실습용 문서 (동기화 대상)
  app/                      # 개발자 트랙 샘플
  tests/                    # 개발자 트랙 테스트
```

## 첫 실행

Claude Code는 `part4/lab`에서 실행하면 이 폴더의 `.claude/settings.json`을 읽습니다. Codex CLI는 프로젝트 Git 루트의 `.codex/` 계층을 기준으로 훅을 읽으므로, Codex 훅 실습은 `part4/lab`을 단독 실습 레포로 열거나 복사한 뒤 실행하세요.

비개발 트랙:

```bash
bash scripts/agent_verify.sh --docs-only
```

개발자 트랙(Python 3.12+ 권장):

```bash
pip install -e ".[dev]"   # 별도 pyproject.toml은 강의 진행 중 추가합니다
bash scripts/agent_verify.sh
```

## 주의

- `.claude/skills/`와 `.agents/skills/`는 `scripts/sync_common_skills.sh`로 `common_skills/`의 직계 스킬 폴더 링크를 동기화합니다. 링크 상태는 `scripts/agent_verify.sh`에서 매번 검사합니다.
- Codex CLI에서 새 프로젝트 훅은 `/hooks` 화면에서 신뢰해야 실행됩니다. `PreToolUse`, `PostToolUse`, `Stop` 프로젝트 훅이 `Trusted`인지 확인한 뒤 실습하세요.
- 실습 중 만지는 명령은 `scripts/risky_command_policy.py`의 차단 목록을 먼저 통과해야 합니다. 차단되면 멈춰서 사람이 확인하는 것이 기본 동작입니다.
- 이 레포는 강의 자료입니다. 실제 운영 코드로 사용하지 마세요.
