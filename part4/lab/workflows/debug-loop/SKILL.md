---
name: debug-loop
description: Use when a test fails, an error log is given, or a user says the implementation is wrong. Reproduces first, hypothesizes, then applies the smallest fix and verifies.
---

# Debug Loop

When debugging, do not modify code immediately. Follow this order.

1. Restate the symptom in one sentence.
2. Separate expected behavior from actual behavior.
3. Find the smallest reproduction command.
4. List at least three hypotheses about the root cause.
5. Test the most likely hypothesis first.
6. Apply the smallest safe fix.
7. Run verification:
   - `bash scripts/agent_verify.sh`
8. Summarize:
   - root cause
   - changed files
   - verification result
   - remaining risks

Do not rewrite unrelated modules. Do not weaken tests to make them pass. If the public API must change, explain the impact before changing it.
