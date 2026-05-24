# GitHub Rulesets 적용 가이드

이 레포의 최종 안전망은 로컬 훅이 아니라 GitHub Rulesets와 CI입니다. 로컬 훅은 개발 중 피드백이고, Rulesets는 우회 방지 장치입니다.

## Branch ruleset: `main-protection`

대상 브랜치: `main`

켜야 할 규칙:

1. `Require a pull request before merging`
   - 최소 1명 승인
   - CODEOWNERS 승인 필요
2. `Require status checks to pass`
   - required check 이름: `verify`
   - 이 이름은 `.github/workflows/verify.yml`의 `jobs.verify.name`과 맞춰 둡니다.
3. `Block force pushes`
4. `Restrict deletions`
5. `Require signed commits` — 조직 보안 정책에 맞으면 활성화

## Push ruleset: `sensitive-files`

대상: 전체 push

`Restrict file paths` 예시:

- `.env`
- `.env.*`
- `secrets/**`
- `**/*.pem`
- `**/*.key`

이 규칙은 로컬 훅이나 Agent 설정을 우회한 push에도 적용됩니다.

## 운영 원칙

- 훅/정책/CI 파일 변경은 CODEOWNERS 승인을 요구합니다.
- `verify` 체크가 required status check로 설정되지 않으면 Stop 훅과 CI가 같은 기준을 공유해도 merge gate가 되지 않습니다.
- Rulesets를 쓰기 어려운 조직은 Branch protection rule에서 같은 옵션을 적용합니다.
