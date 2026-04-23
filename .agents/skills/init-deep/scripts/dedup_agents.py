#!/usr/bin/env python3
"""Deduplicate child AGENTS.md lines that repeat parent AGENTS.md content."""
from __future__ import annotations

import argparse
from pathlib import Path


MANUAL_START = "<!-- MANUAL START -->"
MANUAL_END = "<!-- MANUAL END -->"
KEEP_MARKER = "<!-- KEEP -->"


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def write_lines(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parent_set(lines: list[str]) -> set[str]:
    parent_set: set[str] = set()
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            continue
        if "|" in line:
            continue
        if stripped.startswith("#"):
            continue
        parent_set.add(stripped)
    return parent_set


def dedup_child(child_lines: list[str], parent_set: set[str]) -> tuple[list[str], int]:
    out: list[str] = []
    removed = 0
    in_fence = False
    in_manual = False

    for line in child_lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue

        if stripped == MANUAL_START:
            in_manual = True
            out.append(line)
            continue
        if stripped == MANUAL_END:
            in_manual = False
            out.append(line)
            continue

        if in_fence or in_manual:
            out.append(line)
            continue

        if KEEP_MARKER in line:
            out.append(line)
            continue

        if not stripped:
            out.append(line)
            continue

        if "|" in line:
            out.append(line)
            continue

        if stripped.startswith("#"):
            out.append(line)
            continue

        if stripped in parent_set:
            removed += 1
            continue

        out.append(line)

    return out, removed


def find_agents(root: Path) -> list[Path]:
    paths = []
    for p in root.rglob("AGENTS.md"):
        if any(part in {"node_modules", "dist", "build", ".venv", "venv"} for part in p.parts):
            continue
        paths.append(p)
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description="Dedup AGENTS.md vs parent")
    parser.add_argument("--root", default=".", help="project root")
    parser.add_argument("--apply", action="store_true", help="write changes")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = find_agents(root)
    total_removed = 0
    changed = 0

    for child in files:
        parent = child.parent.parent / "AGENTS.md"
        if not parent.exists():
            continue

        parent_set = build_parent_set(read_lines(parent))
        child_lines = read_lines(child)
        new_lines, removed = dedup_child(child_lines, parent_set)
        if removed:
            changed += 1
            total_removed += removed
            print(f"{child}: removed {removed} duplicate lines")
            if args.apply:
                write_lines(child, new_lines)

    if not changed:
        print("No duplicates found.")
    else:
        print(f"Total files changed: {changed}")
        print(f"Total lines removed: {total_removed}")
        if not args.apply:
            print("Dry run only. Re-run with --apply to write changes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
