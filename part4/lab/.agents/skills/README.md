# Codex 스킬 배포 위치

이 폴더는 Codex가 읽는 스킬 위치입니다. Claude Code 쪽 `.claude/skills/`와 같은 패턴을 따릅니다.

이 폴더의 링크는 **버전 관리 대상이 아닙니다**(`.gitignore`). 소스는 `common_skills/`뿐이고, 링크는 OS별로 자동 재생성됩니다. `README.md`만 커밋됩니다.

## 권장: 공통 스킬 동기화

```bash
bash scripts/sync_common_skills.sh
```

`common_skills/` 바로 아래의 각 스킬 폴더가 이 폴더에 링크로 연결됩니다. 링크 방식은 OS에 따라 자동으로 갈립니다.

- macOS·Linux: 상대 심볼릭 링크 (`ln -s`)
- Windows: 디렉터리 정션 (`mklink /J`) — 관리자 권한·개발자 모드 불필요

매 세션 시작 시 `SessionStart` 훅(`.codex/hooks.json`)이 이 스크립트를 자동 실행해 링크를 최신으로 맞춥니다. `scripts/agent_verify.sh`는 작업 종료 시 `--check` 모드로 링크 상태를 다시 검사합니다.

## Codex 전용 메타데이터가 필요할 때

도구별 추가 메타데이터(예: `agents/openai.yaml`)는 공통 `common_skills/`에 두지 말고, 이 폴더 또는 별도 어댑터 폴더에만 둡니다. 공통 자산을 도구 전용 정보로 오염시키지 않기 위해서입니다.
