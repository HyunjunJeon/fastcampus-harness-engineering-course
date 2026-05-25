"""코드 변경 뒤 문서 영향도 판단표를 생성하고 완료 전 검증합니다.

규칙:
- `app/` 또는 `tests/` 안의 파일이 변경되면 문서 영향도 판단표가 필요합니다.
- `--soft`는 작업 중 알림용입니다. 판단표 템플릿을 만들고 항상 종료 코드 0으로 끝냅니다.
- `--require-report`는 완료 검증용입니다. 판단표가 없거나 필수 검토 항목이 비어 있으면 실패합니다.
- 판단표에서 문서 수정이 필요하다고 적었는데 `docs/` 변경이 없으면 실패합니다.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


CODE_PREFIXES = ("app/", "tests/", "scripts/")
DOC_PREFIXES = ("docs/", "README.md")
REPORT_PATH = Path(".agent/reports/docs-impact.md")
REQUIRED_TABLE_ITEMS = (
    "README.md",
    "docs/",
    "예시 명령",
    "설정 파일",
    "API 계약",
    "스크린샷",
)
TODO_MARKERS = ("TODO", "TBD", "미정", "작성 필요")
NO_DOC_UPDATE_WORDS = ("아니오", "없음", "불필요")
DOC_UPDATE_WORDS = ("예", "필요", "수정")


def run_git(root: Path, args: list[str]) -> str:
    if shutil.which("git") is None:
        return ""
    try:
        return subprocess.check_output(
            ["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return ""


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "scripts" / "docs_impact_check.py").exists() and (cwd / "docs").is_dir():
        return cwd
    out = run_git(Path.cwd(), ["rev-parse", "--show-toplevel"]).strip()
    if out:
        return Path(out)
    return Path(__file__).resolve().parents[1]


def changed_files(root: Path, staged: bool) -> list[str]:
    args = ["diff", "--name-only", "--relative"]
    args.append("--cached" if staged else "HEAD")
    files = [line.strip() for line in run_git(root, args).splitlines() if line.strip()]
    if not staged:
        files.extend(
            line.strip()
            for line in run_git(
                root, ["ls-files", "--others", "--exclude-standard"]
            ).splitlines()
            if line.strip()
        )
    return sorted(dict.fromkeys(files))


def is_code_file(path: str) -> bool:
    return path.startswith(CODE_PREFIXES)


def is_doc_file(path: str) -> bool:
    return path == "README.md" or path.startswith("docs/")


def report_template(files: list[str]) -> str:
    code_files = [path for path in files if is_code_file(path)]
    doc_files = [path for path in files if is_doc_file(path)]
    code_text = ", ".join(code_files) if code_files else "없음"
    doc_text = ", ".join(doc_files) if doc_files else "없음"
    return "\n".join(
        [
            "# 문서 영향도 판단표",
            "",
            "> 이 파일은 훅이 생성한 검토용 리포트입니다. 실제 문서는 사람이 확인한 뒤 별도로 수정합니다.",
            "",
            f"- 변경된 코드: {code_text}",
            f"- 변경된 문서: {doc_text}",
            "",
            "문서 수정 필요 여부: TODO",
            "수정 불필요 사유: TODO",
            "수정 전후 요약: TODO",
            "사람 확인 방법: TODO",
            "",
            "| 항목 | 영향 | 이유 | 확인 방법 |",
            "|---|---|---|---|",
            "| README.md | TODO | 사용법, 설치, 실행 명령 변화 여부 | README를 읽고 실행 명령 확인 |",
            "| docs/ | TODO | 아키텍처, 팀 정책, API 계약 변화 여부 | docs/ 관련 문서 확인 |",
            "| 예시 명령 | TODO | CLI, 테스트, 훅 실행 명령 변화 여부 | README와 문서의 명령 실행 |",
            "| 설정 파일 | TODO | .claude, .codex, GitHub 설정 변화 여부 | 설정 파일 diff 확인 |",
            "| API 계약 | TODO | 입출력, 상태 코드, 데이터 구조 변화 여부 | docs/api-contract.md 확인 |",
            "| 스크린샷 | TODO | 화면이나 UI 설명 변화 여부 | 사람이 화면 확인 |",
            "",
        ]
    )


def write_report(root: Path, files: list[str]) -> Path:
    path = root / REPORT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_template(files), encoding="utf-8")
    return path


def value_for(label: str, text: str) -> str:
    prefix = f"{label}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return ""


def has_todo(value: str) -> bool:
    return not value or any(marker in value for marker in TODO_MARKERS)


def docs_marked_needed(text: str) -> bool:
    value = value_for("문서 수정 필요 여부", text)
    if any(word in value for word in NO_DOC_UPDATE_WORDS):
        return False
    return any(word in value for word in DOC_UPDATE_WORDS)


def validate_report(root: Path, files: list[str]) -> list[str]:
    path = root / REPORT_PATH
    if not path.exists():
        return [f"{REPORT_PATH} 문서 영향도 판단표가 없습니다."]

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if "문서 영향도 판단표" not in text:
        errors.append("문서 영향도 판단표 제목이 없습니다.")
    for item in REQUIRED_TABLE_ITEMS:
        if f"| {item} |" not in text:
            errors.append(f"판단표에 '{item}' 항목이 없습니다.")

    needed = value_for("문서 수정 필요 여부", text)
    no_reason = value_for("수정 불필요 사유", text)
    summary = value_for("수정 전후 요약", text)
    human_check = value_for("사람 확인 방법", text)

    if has_todo(needed):
        errors.append("문서 수정 필요 여부가 비어 있습니다.")
    if not docs_marked_needed(text) and has_todo(no_reason):
        errors.append("문서 수정 불필요 사유가 비어 있습니다.")
    if has_todo(summary):
        errors.append("수정 전후 요약이 비어 있습니다.")
    if has_todo(human_check):
        errors.append("사람 확인 방법이 비어 있습니다.")

    docs_changed = any(path.startswith(DOC_PREFIXES) for path in files)
    if docs_marked_needed(text) and not docs_changed:
        errors.append("문서 수정 필요로 표시됐지만 docs/ 변경이 없습니다.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument(
        "--soft", action="store_true", help="작업 중 경고만 출력하고 실패하지 않습니다."
    )
    parser.add_argument(
        "--require-report",
        action="store_true",
        help="문서 영향도 판단표를 완료 기준으로 검증합니다.",
    )
    args = parser.parse_args()

    root = project_root()
    files = changed_files(root, args.staged)
    code_changed = [path for path in files if is_code_file(path)]
    doc_changed = [path for path in files if is_doc_file(path)]

    if not code_changed:
        print("[docs-impact] 코드 변경 없음 - 통과")
        return 0

    if args.soft:
        path = write_report(root, files)
        print(f"[docs-impact] 코드 변경 감지: {', '.join(code_changed)}")
        print(f"[docs-impact] 문서 영향도 판단표 생성: {path.relative_to(root)}")
        return 0

    if args.require_report:
        errors = validate_report(root, files)
        if errors:
            for error in errors:
                print(f"[docs-impact] {error}")
            return 1
        print("[docs-impact] 문서 영향도 판단표 확인 완료")
        return 0

    if not doc_changed:
        print(
            "[docs-impact] 코드 변경은 있는데 문서 변경이 없습니다. "
            f"변경된 코드: {', '.join(code_changed)}"
        )
        return 1

    print("[docs-impact] 코드 변경과 문서 변경이 함께 있습니다 - 통과")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
