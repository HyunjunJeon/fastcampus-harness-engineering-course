"""Tests for the documentation impact report gate."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "docs_impact_check.py"


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(ROOT / "scripts", repo / "scripts")
    (repo / "app").mkdir()
    (repo / "tests").mkdir()
    (repo / "docs").mkdir()
    (repo / "app" / "services.py").write_text("VALUE = 1\n", encoding="utf-8")
    (repo / "tests" / "test_services.py").write_text(
        "def test_value():\n    assert True\n", encoding="utf-8"
    )
    (repo / "docs" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
    (repo / "README.md").write_text("# Lab\n", encoding="utf-8")
    run(["git", "init"], repo)
    run(["git", "config", "user.email", "test@example.com"], repo)
    run(["git", "config", "user.name", "Test User"], repo)
    run(["git", "add", "."], repo)
    run(["git", "commit", "-m", "baseline"], repo)
    return repo


def test_soft_mode_generates_impact_report_without_blocking(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    (repo / "app" / "services.py").write_text("VALUE = 2\n", encoding="utf-8")

    result = run(["python", str(SCRIPT), "--soft"], repo)

    report = repo / ".agent" / "reports" / "docs-impact.md"
    assert result.returncode == 0
    assert report.exists()
    text = report.read_text(encoding="utf-8")
    assert "문서 영향도 판단표" in text
    assert "| README.md |" in text
    assert "| docs/ |" in text
    assert "app/services.py" in text


def test_require_report_fails_when_code_changed_without_report(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    (repo / "app" / "services.py").write_text("VALUE = 2\n", encoding="utf-8")

    result = run(["python", str(SCRIPT), "--require-report"], repo)

    assert result.returncode == 1
    assert "문서 영향도 판단표가 없습니다" in result.stdout


def test_require_report_passes_with_no_doc_change_reason(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    (repo / "app" / "services.py").write_text("VALUE = 2\n", encoding="utf-8")
    report = repo / ".agent" / "reports" / "docs-impact.md"
    report.parent.mkdir(parents=True)
    report.write_text(
        "\n".join(
            [
                "# 문서 영향도 판단표",
                "",
                "문서 수정 필요 여부: 아니오",
                "수정 불필요 사유: 내부 상수만 바뀌어 사용자 문서 영향이 없습니다.",
                "수정 전후 요약: 공개 동작 변화 없음.",
                "사람 확인 방법: python -m pytest",
                "",
                "| 항목 | 영향 | 이유 | 확인 방법 |",
                "|---|---|---|---|",
                "| README.md | 없음 | 공개 사용법 변화 없음 | README 확인 |",
                "| docs/ | 없음 | 아키텍처 변화 없음 | docs 확인 |",
                "| 예시 명령 | 없음 | 명령 변화 없음 | README 확인 |",
                "| 설정 파일 | 없음 | 설정 키 변화 없음 | 설정 확인 |",
                "| API 계약 | 없음 | API 응답 변화 없음 | 테스트 확인 |",
                "| 스크린샷 | 없음 | UI 변화 없음 | 화면 확인 |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = run(["python", str(SCRIPT), "--require-report"], repo)

    assert result.returncode == 0
    assert "문서 영향도 판단표 확인 완료" in result.stdout


def test_require_report_fails_when_docs_needed_without_doc_update(
    tmp_path: Path,
) -> None:
    repo = make_repo(tmp_path)
    (repo / "app" / "services.py").write_text("VALUE = 2\n", encoding="utf-8")
    report = repo / ".agent" / "reports" / "docs-impact.md"
    report.parent.mkdir(parents=True)
    report.write_text(
        "\n".join(
            [
                "# 문서 영향도 판단표",
                "",
                "문서 수정 필요 여부: 예",
                "수정 불필요 사유: 해당 없음",
                "수정 전후 요약: 서비스 동작 설명을 갱신해야 합니다.",
                "사람 확인 방법: docs/architecture.md 확인",
                "",
                "| 항목 | 영향 | 이유 | 확인 방법 |",
                "|---|---|---|---|",
                "| README.md | 필요 | 사용법 변경 | README 확인 |",
                "| docs/ | 필요 | 아키텍처 설명 변경 | docs 확인 |",
                "| 예시 명령 | 없음 | 명령 변화 없음 | README 확인 |",
                "| 설정 파일 | 없음 | 설정 키 변화 없음 | 설정 확인 |",
                "| API 계약 | 없음 | API 응답 변화 없음 | 테스트 확인 |",
                "| 스크린샷 | 없음 | UI 변화 없음 | 화면 확인 |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = run(["python", str(SCRIPT), "--require-report"], repo)

    assert result.returncode == 1
    assert "문서 수정 필요로 표시됐지만 docs/ 변경이 없습니다" in result.stdout
