# GitHub Rulesets 적용 가이드

이 문서는 `part4/lab/`을 GitHub에 올렸을 때 적용하는 정책 게이트의 권장 구성을 정리합니다. AI 액션을 required로 걸지 않고, **GitHub Rulesets로 결정적 게이트만 강제**하는 것이 강의의 권장 방향입니다.

> 촬영일(2026-05-16) 기준 공식 문서에서 룰 이름과 동작 범위를 다시 확인하세요. GitHub은 Rulesets와 branch protection rule을 함께 운영합니다.

## 권장 룰 6가지

보호 브랜치(예: `main`)에 적용할 Ruleset에 다음을 함께 켭니다.

| 룰 | 설정 | 효과 |
|---|---|---|
| Require a pull request before merging | Required reviews ≥ 1 | main 직접 push 차단 |
| Require status checks to pass before merging | Status check: `verify` | 우리 워크플로우(`.github/workflows/verify.yml`)의 `jobs.verify`가 통과해야 머지 가능 |
| Block force pushes | 기본 활성 유지 | 기록 덮어쓰기 차단 |
| Restrict deletions | 기본 활성 유지 | 보호 브랜치 삭제 차단 |
| Restrict file paths | 패턴 등록 (아래 참고) | 비밀 파일 변경 자체를 차단 |
| Require signed commits (옵션) | 활성 | 신원 확인된 커밋만 허용 |

## Restrict file paths 권장 패턴

비밀 파일·인증 파일·운영 설정이 PR로 들어오지 못하게 합니다. 최대 200개 항목까지 등록 가능합니다.

```
.env
.env.*
**/secrets/**
**/*.pem
**/*.key
**/credentials.json
**/service-account*.json
```

운영 환경 설정 파일도 같은 방식으로 추가하면 됩니다.

## 적용 절차

1. GitHub 저장소 → Settings → Rules → Rulesets → New ruleset.
2. Ruleset name: `lab-protection`, Enforcement status: `Active`.
3. Target → 보호하고 싶은 브랜치 선택(`main` 또는 패턴).
4. Rules → 위 표의 6가지를 켜고, status check 이름에 `verify` 입력.
5. Restrict file paths → 위 권장 패턴 등록.
6. Save changes → PR을 일부러 위반시켜 보고 차단되는지 확인.

## AI 액션과의 관계

`anthropics/claude-code-action@v1` 같은 AI 액션은 우리 구조에서 **"보조 리뷰 장치"**입니다. PR에 코멘트만 다는 보조 잡으로 두고, **머지를 막는 권한은 위 6가지 Rulesets에만** 둡니다.

이유:

- AI 액션은 토큰·모델 가용성에 종속됩니다. required로 걸면 잠시 장애로 머지가 막힙니다.
- AI 액션의 release/입력 스키마가 바뀌면 그 자리에서 머지가 일제히 막힙니다(`@beta` → `@v1` breaking change 사례).
- 거버넌스 메시지가 단순해집니다 — "사람이든 AI든, Claude든 Codex든, 같은 6가지 게이트를 통과한다."

## 강의 시연 동선

1. **막히는 PR**: 일부러 `verify`를 실패시키고, Rulesets의 required status check 때문에 머지 버튼이 비활성화된 화면을 보여준다.
2. **보조 리뷰 PR**: 같은 PR에 `@claude` 멘션을 달아 코멘트가 달리는 모습 — 단 그 리뷰는 머지 결정 권한이 없음을 강조.
3. **차단되는 push**: `.env`를 일부러 변경한 PR을 만들어 Restrict file paths 룰로 push 자체가 막히는 화면.

이 3단계 시연이 "AI 시대에도 통하는 정책 설계"라는 메시지를 손에 잡히게 만듭니다.

## 관련 자료

- 본 레포의 `.github/workflows/verify.yml` — required로 등록할 잡 (`jobs.verify`).
- 본 레포의 `scripts/agent_verify.sh` — verify 잡이 실행하는 단일 진입점.
- `part4/handout/03-02-ai-git-rules-handout.md` — 강의 본문과 시연 동선.
