# Session 3-5 - Harness Retro와 regression

## 핵심 한 줄

좋은 하네스는 실패를 먹고 자랍니다.  
실패를 기록하고 같은 실패를 막는 regression을 남깁니다.

## 오늘 가져갈 것

- 실패를 모델 실패, 컨텍스트 실패, 하네스 실패로 나눕니다.
- 하나의 실패를 skill/hook/eval 개선으로 연결합니다.

## 실습

```bash
cd part5/lab
bash scripts/run_session.sh 03-05
```

## 검증

```bash
cd part5/lab
bash scripts/check.sh --session 03-05
```

## Claude Code를 쓴다면

실패한 세션을 요약하고, 다음 세션에서 같은 실패가 반복되지 않게 `HARNESS_RETRO.md`를 갱신합니다.

## Codex를 쓴다면

Codex는 retro를 바탕으로 regression fixture나 hook 메시지를 수정합니다.

## 실습 결과물

- `HARNESS_RETRO.md`
- `evals/regression.yaml`
- `.agents/skills/harness-retro/SKILL.md`

## 더 알아보기

- OpenAI Harness engineering: https://openai.com/index/harness-engineering/

