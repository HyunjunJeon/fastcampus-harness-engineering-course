# 04-01 완료 기준 양식 + 실패 테스트 예시

[../plan.md](../plan.md) 04-01 진행 흐름의 4단계(짧은 실습)에서 사용.

## 완료 기준 양식 (3줄 형식)

수강생이 `docs/done-definition.md`에 채울 양식:

```markdown
## 작업: <한 줄 제목>

### 완료 기준
1. <행동 1> 할 수 있다. 검증 명령: `<실행 가능한 명령>`
2. <행동 2> 할 수 있다. 검증 명령: `<실행 가능한 명령>`
3. <에러 케이스>가 발생할 때 막힌다. 검증 명령: `<실행 가능한 명령>`
```

핵심: 완료 기준 *각 줄*에 *실행 가능한 검증 명령*이 붙어야 한다.

| 의견 | 기준 |
| --- | --- |
| "잘 동작한다" | `pytest tests/test_add.py::test_negatives` 통과 |
| "에러가 잡힌다" | `pytest tests/test_add.py::test_empty_string` 통과 |
| "성능이 괜찮다" | `time ./benchmark.sh` 결과 ≤ 200ms |

## 실패하는 테스트 1개 예시

### Python (pytest)

```python
# tests/test_calculator.py
from src.calculator import add


def test_add_handles_negatives():
    """완료 기준 1: 음수 두 개를 더하면 음수가 나온다."""
    assert add(-2, -3) == -5
```

실행:

```bash
pytest tests/test_calculator.py::test_add_handles_negatives -v
```

첫 실행 결과(예상): **FAIL** — `add` 함수가 아직 음수를 처리하지 않거나 함수 자체가 없을 때.

### JavaScript (vitest)

```javascript
// tests/calculator.test.js
import { describe, it, expect } from "vitest";
import { add } from "../src/calculator.js";

describe("add", () => {
  it("음수 두 개를 더하면 음수가 나온다", () => {
    expect(add(-2, -3)).toBe(-5);
  });
});
```

실행:

```bash
npx vitest run tests/calculator.test.js
```

첫 실행 결과(예상): **FAIL**.

## 레거시 코드에서 시작하는 법

테스트가 *전혀 없는* 코드베이스에서 TDD를 시작하는 흐름:

1. **이번에 바꿀 함수 1개**만 고른다. 전체 코드를 다 테스트하려 하지 말 것.
2. 그 함수의 *현재 동작* 1개를 *통과하는* 테스트(현재 동작을 고정하는 테스트)부터 쓴다 — 골든 마스터.
3. *바꾸려는 동작* 1개를 *실패하는* 테스트로 쓴다.
4. 구현을 바꾼다.
5. 두 테스트 *모두* 통과해야 다음 함수로 넘어간다.

이 과정에서 *기존 동작을 깨뜨리는지* 자동으로 알게 된다.

## 강사가 챙길 자산

- 위 양식을 본인 프로젝트 1개 기능에 적용한 시연 자료 1장
- 실패하는 테스트 → 통과하는 구현 → 리팩터링 1바퀴를 *강의 시간 안에 돌릴 수 있는 충분히 작은* 예제 미리 준비 (예: `add` 함수의 음수 처리)
- (촬영일 기준) 사용 언어의 테스트 러너 옵션(`-v`, `--watch`, `--coverage` 등) 재확인
