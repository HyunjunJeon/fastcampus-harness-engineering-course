# Session 3-4 - Skill / Hook(Eval)로 묶어두기

반복되는 요청은 prompt가 아니라 `skill, hook(eval)`, 로 승격해야 
`재사용` 가능하게 만들 수 있습니다.

- spec review를 skill로 만듭니다.
- 필요한 체크 작업을 Stop hook에 연결합니다.

## Claude Code

`.claude/settings.json`에서 Stop hook이 검증 명령을 호출하도록 둡니다.

## Codex

`.codex/config.toml`에서 Stop hook을 연결합니다. hook은 guardrail이며 CI나 권한 설정과 함께 써야 합니다.
완료 선언에는 테스트 결과뿐 아니라 report, current-state, scorecard 위치를 함께 적습니다.

## 추가 자료

- Codex Skills: https://developers.openai.com/codex/skills
- Codex Hooks: https://developers.openai.com/codex/hooks
- Claude Skills: https://docs.anthropic.com/en/docs/claude-code/skills
- Claude Hooks: https://docs.anthropic.com/en/docs/claude-code/hooks
