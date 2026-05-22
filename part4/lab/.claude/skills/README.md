# Claude Code 스킬 배포 위치

이 폴더는 Claude Code가 실제로 읽는 스킬 위치입니다. 공통 스킬 원본은 `common_skills/`에 한 번만 두고, 이 폴더에서는 그쪽으로 연결만 합니다.

## 권장: 공통 스킬 동기화

```bash
bash scripts/sync_common_skills.sh
```

`common_skills/` 바로 아래의 각 스킬 폴더가 이 폴더에 심볼릭 링크로 연결됩니다. `scripts/agent_verify.sh`는 `--check` 모드로 링크 상태를 매번 검사합니다.

## 심볼릭 링크가 막힌 환경

이번 실습 구성은 복사 fallback을 자동화하지 않습니다. 운영체제나 보안 정책 때문에 심볼릭 링크가 막혀 있으면, 강의 환경 관리자에게 확인한 뒤 별도 복사 절차를 사용합니다.
