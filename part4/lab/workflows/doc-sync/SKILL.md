---
name: doc-sync
description: Use when code changes may affect API contracts, architecture, workflows, or user-facing behavior. Updates only the affected documentation sections.
---

# Documentation Sync

When code changes are made:

1. Identify whether behavior, API, architecture, configuration, or workflow changed.
2. Check relevant docs:
   - `docs/api-contract.md`
   - `docs/architecture.md`
3. Update only the affected sections. Do not rewrite unrelated documentation.
4. If a doc section is now wrong but you cannot fix it confidently, leave a `> TODO: doc-sync verification needed` line and report it.
5. Run `python scripts/docs_impact_check.py --require-report` to confirm doc-code drift is resolved.
6. Summarize:
   - changed behavior
   - updated docs
   - remaining documentation risks
