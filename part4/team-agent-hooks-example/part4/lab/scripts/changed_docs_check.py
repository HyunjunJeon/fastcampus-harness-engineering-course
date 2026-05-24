#!/usr/bin/env python3
"""Check that governed code/policy changes update the corresponding documents."""

from __future__ import annotations

import argparse
import os
import sys

from hook_common import changed_files_from_git, load_policy, path_matches, repo_root


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("--base-ref", default=os.environ.get("AGENT_DIFF_BASE"))
    args = parser.parse_args()
    root = repo_root()
    policy = load_policy(root)
    changed = args.files or changed_files_from_git(root, args.base_ref)
    if not changed:
        print("changed_docs_check: no changed files detected")
        return 0

    failures: list[str] = []
    ci = os.environ.get("CI", "").lower() in {"1", "true", "yes"}
    strict = os.environ.get("AGENT_DOCS_STRICT", "").lower() in {"1", "true", "yes"}

    for rule in policy.get("docs_sync_rules", []):
        when_any = rule.get("when_any", [])
        require_any = rule.get("require_any", [])
        touched = [p for p in changed if path_matches(p, when_any)]
        if not touched:
            continue
        satisfied = any(path_matches(p, require_any) for p in changed)
        if satisfied:
            continue
        mode = rule.get("ci_mode" if ci else "local_mode", "warn")
        message = (
            f"docs_sync rule '{rule.get('name', 'unnamed')}' triggered by {', '.join(touched)}; "
            f"also update one of: {', '.join(require_any)}"
        )
        if mode == "enforce" or strict:
            failures.append(message)
        else:
            print("WARNING: " + message)

    if failures:
        print("changed_docs_check failed:", file=sys.stderr)
        for failure in failures:
            print("- " + failure, file=sys.stderr)
        return 1
    print("changed_docs_check: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
