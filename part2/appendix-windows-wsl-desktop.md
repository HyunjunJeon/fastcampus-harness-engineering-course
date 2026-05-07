# Appendix. Windows, WSL, Desktop App 환경 차이

## 핵심 메시지

Windows 문제는 대개 모델 성능 문제가 아니라 실행 환경 문제다. 강의에서는 항상 `native Windows`, `WSL2`, `CLI`, `Desktop App`, `project filesystem`을 분리해 설명한다.

## Windows 환경 체크리스트

```text
1. OS: Windows 11 / Windows 10 1809+ / 오래된 Windows
2. 실행 위치: PowerShell / CMD / Git Bash / WSL2 Ubuntu
3. 프로젝트 위치: C:\... / /mnt/c/... / /home/<user>/...
4. Git 설치 위치: Windows Git / WSL Git
5. Node.js 설치 위치: Windows Node / WSL Node
6. 도구 실행 위치: Claude Code CLI / Claude Desktop Code tab / Codex CLI / Codex App
7. sandbox 방식: native Windows sandbox / WSL2 Linux sandbox / sandbox 미지원
8. 회사 장비 여부: 관리자 권한, 방화벽, proxy, Windows Sandbox 정책
```

## Claude Code CLI

- native Windows는 Git for Windows가 권장된다. 없으면 PowerShell을 사용한다.
- native Windows의 Claude Code는 sandboxing이 지원되지 않는 것으로 설명한다.
- sandboxed command execution이 필요하면 WSL2를 선택한다.
- WSL에서는 WSL terminal 안에서 Linux installer를 실행하고 `claude`도 WSL에서 실행한다.
- WSL에서 `/mnt/c/...` 아래 프로젝트를 다루면 검색과 파일 접근이 느릴 수 있다.

자주 나오는 문제:

- PowerShell/CMD 설치 명령 혼동
- PATH 문제로 `claude`가 인식되지 않음
- 오래된 Claude Desktop의 `Claude.exe`가 PATH 우선순위를 가져감
- WSL에서 Windows `npm`/`node`가 섞임
- WSL2 OAuth 로그인에서 브라우저 열기 또는 붙여넣기 실패

## Claude Desktop App

- macOS와 Windows를 지원하고 Linux는 지원하지 않는다.
- Code tab은 local files에 접근하고 diff 승인 후 변경을 적용한다.
- Windows local session에서는 Git 설치가 필요하다.
- CLI와 Desktop은 `CLAUDE.md`, MCP 설정, hooks, skills, settings를 공유할 수 있지만 session history는 별도다.
- `/desktop` 명령은 CLI session을 Desktop으로 넘기는 용도로 macOS와 Windows에서 사용할 수 있다.
- Desktop은 visual diff, 파일 첨부, 병렬 session 관리가 편하고, CLI는 scripting과 automation에 적합하다.

## Codex CLI

- macOS, Windows, Linux에서 사용할 수 있다.
- Windows native는 PowerShell과 Windows sandbox를 사용한다.
- WSL2는 Linux-native toolchain이 필요할 때 선택한다.
- WSL1은 Codex `0.115` 이후 Linux sandbox 변경 때문에 지원하지 않는다고 설명한다.
- Windows 11을 권장하고, Windows 10은 최신 빌드 기준 best effort로 설명한다.

자주 나오는 문제:

- PowerShell execution policy 오류
- Windows sandbox setup 실패
- 회사 장비에서 로컬 사용자/그룹 생성, 방화벽 규칙, sandbox user logon rights가 차단됨
- `elevated` sandbox 실패 시 `unelevated` fallback 사용
- WSL에서 `/mnt/c/...` 아래 repo가 느림
- Windows native app과 WSL CLI가 `CODEX_HOME`을 자동 공유하지 않음

## Codex App

- macOS와 Windows를 지원한다.
- Windows App은 Microsoft Store 또는 `winget install Codex -s msstore`로 설치할 수 있다.
- Windows App은 native PowerShell agent를 쓰거나 설정에서 WSL2 runtime으로 바꿀 수 있다.
- integrated terminal 선택과 agent runtime 선택은 별개다.
- Windows-native agent를 쓸 계획이면 프로젝트는 Windows filesystem에 두는 편이 안정적이다.
- agent를 WSL2에서 돌린다면 프로젝트와 worktree는 WSL native filesystem에 두는 편이 낫다.
- Codex App의 Computer Use는 현재 macOS 중심 기능으로 설명하고, Windows 실습은 앱/브라우저/터미널 중심으로 잡는다.

## 강의에서의 처리 방식

- Session 1-1: 공식 문서 조사에 Windows setup과 WSL 문서를 포함한다.
- Session 1-2: Windows/WSL 공개 이슈는 검증 후보로만 다룬다.
- Session 1-3: 실습 지시문에 OS, shell, repo 위치를 포함한다.
- Session 2-2: `CLAUDE.md`에 기준 실행 환경을 적는다.
- Session 2-3: `AGENTS.md`에 OS별 명령 분기와 금지 사항을 적는다.
- Session 3-1~3-3: 핸드오프와 컨텍스트 문서에 OS/shell/runtime 정보를 남긴다.
