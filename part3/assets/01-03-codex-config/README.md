# 01-03 Codex `config.toml` 운영 모드

[../../plan.md](../../plan.md) 01-03 진행 흐름의 4단계(짧은 실습)에서 사용. 승인 정책 축과 sandbox 축 두 모드를 비교 시연.

## 두 모드 비교

| 파일 | sandbox 축 | approval 축 | 사용 시점 |
| --- | --- | --- | --- |
| [config-workspace-write.toml](config-workspace-write.toml) | `workspace-write` | `on-request` | 일반 업무 — 파일 쓰기 가능, 외부 명령은 승인 요청 |
| [config-read-only.toml](config-read-only.toml) | `read-only` | `untrusted` | 새 저장소 탐색 — 어떤 변경도 일어나지 않음 |
