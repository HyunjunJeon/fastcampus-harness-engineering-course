# Part 2 세션별 진행안

이 폴더는 `docs/part2-session-plan.md`의 큰 내용을 촬영/강의 준비용으로 쪼갠 문서다. 각 세션 파일은 강사가 그대로 보고 진행할 수 있도록 `목표`, `준비물`, `진행 순서`, `데모/실습`, `Windows/WSL 주의`, `산출물`, `완료 기준` 순서로 구성한다.

## 전체 흐름

Part 2는 도구 사용법을 더 많이 외우는 파트가 아니라, AI 코딩 에이전트가 오래 안정적으로 일하도록 문서와 컨텍스트를 설계하는 파트다.

1. 공식 문서를 읽고 현재 기능을 확인한다.
2. 문서 밖 정보는 후보로만 탐색하고 검증한다.
3. 읽은 문서를 실습 지시문으로 바꾼다.
4. 반복 지시는 `CLAUDE.md`와 `AGENTS.md`로 고정한다.
5. 긴 세션은 압축, 재개, 새 세션, 문서 분리 기준으로 관리한다.
6. Windows/WSL/macOS 차이는 매 세션에서 환경 정보로 확인한다.

## 세션 목록

### Chapter 1. Claude Code, Codex 공식 문서 활용법

- [Session 1-1. 공식 문서를 통해 기능과 활용법 이해하기](./01-01-official-docs.md)
- [Session 1-2. 공식 문서 밖 정보를 안전하게 탐색하기](./01-02-doc-gaps-research.md)
- [Session 1-3. 문서를 읽고 실습으로 바꾸는 질문법](./01-03-docs-to-practice.md)

### Chapter 2. CLAUDE.md와 AGENTS.md로 AI를 팀원처럼 일하게 만들기

- [Session 2-1. 좋은 지시형 프롬프트: WHAT, WHY, HOW](./02-01-what-why-how.md)
- [Session 2-2. CLAUDE.md: 전역, 프로젝트, 하위 폴더 규칙](./02-02-claude-md.md)
- [Session 2-3. AGENTS.md: 여러 도구에 통하는 공통 지시문](./02-03-agents-md.md)
- [Session 2-4. 나쁜 지시문을 고치는 실전 리팩터링](./02-04-instruction-refactor.md)

### Chapter 3. 긴 대화를 무너지지 않게 관리하기

- [Session 3-1. 긴 대화가 망가지는 이유와 새 세션 타이밍](./03-01-context-rot-new-session.md)
- [Session 3-2. /compact, resume, memory를 언제 어떻게 쓸까](./03-02-compact-resume-memory.md)
- [Session 3-3. 컨텍스트-문서 분리 전략](./03-03-context-doc-separation.md)

### Appendix

- [Windows, WSL, Desktop App 환경 차이](./appendix-windows-wsl-desktop.md)

## 촬영 공통 규칙

- 제품 기능명과 명령은 촬영 당일 공식 문서와 로컬 도움말로 다시 확인한다.
- Claude Code와 Codex를 억지로 1:1 대응시키지 않는다.
- `AGENTS.md`는 공통 지시문 포맷으로 설명하되, 모든 도구가 완전히 동일하게 처리한다고 말하지 않는다.
- Windows는 `native Windows`, `WSL2`, `Desktop App`, `CLI`를 분리해 설명한다.
- GitHub issue나 커뮤니티 글은 검증 후보로만 다룬다.
