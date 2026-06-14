# Session 3-4 - Skill / Hook / Eval로 묶기

## 핵심 한 줄

반복되는 요청은 prompt가 아니라 skill, hook, eval로 승격해야 재사용할 수 있습니다.

## 오늘 가져갈 것

- spec review를 skill로 만듭니다.
- `scripts/check.sh`를 Stop hook에 연결합니다.
- harness 품질을 scorecard로 평가합니다.
- `.harness/reports`, `docs/current-state.md`, `HARNESS_RETRO.md`, `evals/harness-scorecard.md`를 evidence ledger로 묶습니다.

## 실습

```bash
cd part5/lab
bash scripts/run_session.sh 03-04
```

## 검증

```bash
cd part5/lab
bash scripts/check.sh --session 03-04
```

## Claude Code를 쓴다면

`.claude/settings.json`에서 Stop hook이 검증 명령을 호출하도록 둡니다.

## Codex를 쓴다면

`.codex/config.toml`에서 Stop hook을 연결합니다. hook은 guardrail이며 CI나 권한 설정과 함께 써야 합니다.
완료 선언에는 테스트 결과뿐 아니라 report, current-state, scorecard 위치를 함께 적습니다.

## 실습 결과물

- `.agents/skills/spec-review/SKILL.md`
- `.claude/settings.json`
- `.codex/config.toml`
- `evals/harness-scorecard.md`
- evidence ledger: `.harness/reports/`, `docs/current-state.md`, `HARNESS_RETRO.md`

## 더 알아보기

- Codex Skills: https://developers.openai.com/codex/skills
- Codex Hooks: https://developers.openai.com/codex/hooks
