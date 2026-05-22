"""코드가 바뀌면 관련 문서도 바뀌었는지 확인하는 검증 스크립트.

규칙:
- `app/` 또는 `tests/` 안의 파일이 변경되면, `docs/` 안의 최소 한 파일이 함께 변경되어야 한다.
- 변경 비교 기준은 다음 순서로 시도한다.
  1. `--staged`로 호출되면 `git diff --cached --name-only`
  2. 기본은 `git diff --name-only HEAD`
- `--soft`로 호출되면 위반이 있어도 종료 코드 0으로 끝내고 경고만 출력한다.
  훅에서 작업 중간에 멈추지 않기 위해 사용한다.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess

CODE_PREFIXES = ("app/", "tests/")
DOC_PREFIXES = ("docs/",)


def changed_files(staged: bool) -> list[str]:
    if shutil.which("git") is None:
        return []
    cmd = ["git", "diff", "--name-only"]
    cmd.append("--cached" if staged else "HEAD")
    try:
        out = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument(
        "--soft",
        action="store_true",
        help="위반이 있어도 종료 코드 0. 훅용.",
    )
    args = parser.parse_args()

    files = changed_files(args.staged)
    code_changed = [f for f in files if f.startswith(CODE_PREFIXES)]
    doc_changed = [f for f in files if f.startswith(DOC_PREFIXES)]

    if not code_changed:
        print("[docs-check] 코드 변경 없음 — 통과")
        return 0
    if not doc_changed:
        msg = (
            "[docs-check] 코드 변경은 있는데 docs/ 변경이 없습니다. "
            f"변경된 코드: {', '.join(code_changed)}"
        )
        print(msg)
        return 0 if args.soft else 1

    print("[docs-check] 코드 변경과 문서 변경이 함께 있습니다 — 통과")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
