---
name: pr-review
description: Review code changes for correctness, security, test coverage, and documentation impact. Use when reviewing a diff, branch, or pull request.
---

# PR Review

Review in this order. Skip style nits.

1. Correctness — does the change do what the description says?
2. Security — secrets, injection, unsafe shell, broken auth?
3. Data handling — backward compatibility, migrations, race conditions?
4. Test coverage — are new code paths covered? Any tests weakened?
5. Documentation impact — does `docs/api-contract.md` or `docs/architecture.md` need updates?
6. Maintainability — naming, dead code, hidden coupling.

Output format:

## Summary

## Critical issues

## Suggested fixes

## Missing tests

## Documentation updates

## Verification commands

For each Suggested fix, include a file path and line range. Do not propose broad rewrites; propose the smallest change that resolves the issue.
