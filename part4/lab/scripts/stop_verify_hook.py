"""Stop 훅에서 공통 검증 스크립트를 실행하고 실패 시 작업 계속을 요청합니다."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path


MAX_OUTPUT_CHARS = 6000


def read_payload() -> dict[str, object]:
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def smoke_log(root: Path, status: str, payload: dict[str, object]) -> None:
    path = os.environ.get("HOOK_SMOKE_LOG")
    if not path:
        return
    target = Path(path)
    if not target.is_absolute():
        target = root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "script": "stop_verify_hook.py",
        "status": status,
        "cwd": str(root),
        "payload": payload,
        "time": time.time(),
    }
    with target.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    payload = read_payload()
    root = Path(__file__).resolve().parents[1]
    smoke_log(root, "start", payload)
    if payload.get("stop_hook_active") is True:
        smoke_log(root, "skipped:stop_hook_active", payload)
        return 0

    verify = root / "scripts" / "agent_verify.sh"
    result = subprocess.run(
        ["bash", str(verify)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        smoke_log(root, "passed", payload)
        return 0

    output = (result.stdout + "\n" + result.stderr).strip()
    if len(output) > MAX_OUTPUT_CHARS:
        output = output[-MAX_OUTPUT_CHARS:]

    print(
        "검증이 실패했습니다. 아래 출력을 보고 최소 수정 후 "
        "`bash scripts/agent_verify.sh`를 다시 실행하세요.\n\n"
        f"{output}",
        file=sys.stderr,
    )
    smoke_log(root, "failed", payload)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
