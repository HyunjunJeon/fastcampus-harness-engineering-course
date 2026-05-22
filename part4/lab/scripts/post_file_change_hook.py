"""PostToolUse 훅에서 파일 변경 뒤 포맷과 빠른 테스트를 실행합니다."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


MAX_OUTPUT_CHARS = 6000


def run(cmd: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        cmd,
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def show_failure(label: str, result: subprocess.CompletedProcess[str]) -> None:
    output = (result.stdout + "\n" + result.stderr).strip()
    if len(output) > MAX_OUTPUT_CHARS:
        output = output[-MAX_OUTPUT_CHARS:]
    print(f"[post-change] {label} failed", file=sys.stderr)
    if output:
        print(output, file=sys.stderr)


def log(verbose: bool, message: str) -> None:
    if verbose:
        print(f"[post-change] {message}", file=sys.stderr)


def smoke_log(root: Path, status: str, payload: str = "") -> None:
    path = os.environ.get("HOOK_SMOKE_LOG")
    if not path:
        return
    target = Path(path)
    if not target.is_absolute():
        target = root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "script": "post_file_change_hook.py",
        "status": status,
        "cwd": str(root),
        "payload": payload[:1000],
        "time": time.time(),
    }
    with target.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    payload = sys.stdin.read()
    smoke_log(root, "start", payload)
    targets = ["scripts", "tests"]
    if (root / "app").is_dir():
        targets.append("app")

    docs_check = run(["python", "scripts/changed_docs_check.py", "--soft"], root)
    if docs_check.returncode != 0:
        show_failure("docs check", docs_check)
        smoke_log(root, "failed:docs")
        return 2
    log(args.verbose, "docs check passed")

    if shutil.which("ruff") is None:
        log(args.verbose, "ruff not installed; skipping format and lint")
    else:
        fmt = run(["ruff", "format", *targets], root)
        if fmt.returncode != 0:
            show_failure("ruff format", fmt)
            smoke_log(root, "failed:format")
            return 2
        log(args.verbose, "ruff format passed")

        lint = run(["ruff", "check", *targets], root)
        if lint.returncode != 0:
            show_failure("ruff check", lint)
            smoke_log(root, "failed:lint")
            return 2
        log(args.verbose, "ruff check passed")

    if (root / "app").is_dir() and shutil.which("pytest") is not None:
        tests = run(["python", "-m", "pytest", "-q", "-p", "no:cacheprovider"], root)
        if tests.returncode != 0:
            show_failure("pytest", tests)
            smoke_log(root, "failed:pytest")
            return 2
        log(args.verbose, "pytest passed")
    else:
        log(args.verbose, "pytest unavailable or app/ missing; skipping tests")

    smoke_log(root, "passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
