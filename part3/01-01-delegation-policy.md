# Session 1-1. AI에게 어디까지 맡길 것인가: 승인 정책의 기본

## 목표

AI 코딩 에이전트를 "똑똑한 채팅창"이 아니라 파일을 읽고, 수정하고, 명령을 실행할 수 있는 작업자로 이해한다. 
수강생은 작업을 맡기기 전에 위험도와 승인 경계를 먼저 정할 수 있어야 한다.

## 준비물

- Claude Code 공식 settings/permissions 문서
- Codex 공식 config/sandbox/approval 문서

## 진행

1. 작업 위험도를 5단계로 나눈다.
   - 읽기: 파일 탐색, 구조 설명, 공식 문서 요약
   - 로컬 수정: README 수정, 작은 버그 수정, 테스트 추가
   - 명령 실행: 테스트, 린트, 빌드, 패키지 설치
   - 외부 연결: GitHub, DB, 브라우저, SaaS, MCP 서버
   - 파괴적 작업: 삭제, 마이그레이션, 배포, 비용 발생, 권한 변경

2. Human-in-the-Loop을 설명한다.
   - 모든 작업을 매번 승인하는 것이 안전 설계는 아니다.
   - 낮은 위험 작업은 빠르게, 높은 위험 작업은 멈춰서 검토하도록 경계를 세운다.
   - 승인 기준은 도구별 기능명보다 조직과 프로젝트의 실패 비용에 맞춰 정한다.

3. Claude Code와 Codex를 비교한다.
   - Claude Code는 settings/permissions 중심으로 설명한다.
   - Codex는 approval policy, sandbox mode, workspace 접근 범위 중심으로 설명한다.
   - "같은 기능"이라고 외우지 말고, 둘 다 작업자의 권한 경계를 정하는 장치라고 이해시킨다.

## 데모/실습

다음 작업을 `자동 허용 / 승인 필요 / 금지`로 분류한다.

- 코드 구조 설명
- README 오타 수정
- `.env` 파일 읽기
- 테스트 실행
- 새 패키지 설치
- `git push`
- DB 마이그레이션
- 운영 배포

AI에게 먼저 분류를 요청한다.

```text
아래 작업을 실행하지 말고 위험도만 분류해줘.
각 작업에 필요한 권한, 사람 승인 필요 여부, 실패했을 때의 영향, 검증 방법을 표로 정리해줘.
추측한 항목은 "확인 필요"로 표시해줘.
```


## 완료 기준

수강생이 AI에게 작업을 맡기기 전에 해당 작업이 어떤 권한을 요구하고, 언제 사람 승인이 필요한지 설명할 수 있어야 한다.

https://code.claude.com/docs/ko/permissions
https://developers.openai.com/codex/agent-approvals-security