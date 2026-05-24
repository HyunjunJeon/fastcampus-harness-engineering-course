---
name: team-agent-workflow
description: Use for commits, pull requests, policy changes, release preparation, and any task requiring team Agent workflow evidence.
disable-model-invocation: false
---

# Team Agent Workflow Skill

Use this workflow when preparing a commit, PR, policy change, release, or high-risk code change.

1. Restate goal and exclusions.
2. Inspect the diff with `git diff --stat` and `git diff`.
3. Run `bash scripts/agent_verify.sh` unless the user explicitly limits scope.
4. Summarize evidence:
   - changed files
   - verification commands and outcomes
   - human approvals needed
   - residual risks
5. Do not read or modify protected secrets paths.

For hook/policy/CI changes, also check `docs/team-agent-policy.md`, `docs/architecture.md`, and `.github/RULESETS.md`.
