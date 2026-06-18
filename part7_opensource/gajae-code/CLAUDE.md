# Gajae-Code Claude Code Contract

Claude Code should follow the same repository contract as Codex. Read `AGENTS.md` first and treat it as authoritative for workflow routing, repository focus, coding rules, and verification.

## GitNexus-first orientation

Before answering architecture, call-flow, package-boundary, or "how does this work?" questions about this repository, consult the local GitNexus wiki first, then verify important claims against source.

Primary GitNexus artifacts:
- `.gitnexus/wiki/index.html` — generated viewer for human navigation
- `.gitnexus/wiki/overview.md` — first read for repo-wide orientation
- `.gitnexus/wiki/document-index.md` — generated list of source Markdown docs and GitNexus wiki artifacts
- `.gitnexus/wiki/module_tree.json` — module list and file ownership map
- `.gitnexus/wiki/coding-agent-cli-and-commands.md` — CLI entry and command routing
- `.gitnexus/wiki/coding-agent-session-runtime.md` — session/runtime assembly
- `.gitnexus/wiki/coding-agent-workflow-skills-and-state-runtime.md` — workflow skill and state runtime
- `.gitnexus/wiki/coding-agent-tool-registry-and-built-in-tool-backends.md` and `.gitnexus/wiki/execution-and-tools.md` — tool registry and execution backends
- `.gitnexus/wiki/dependency-and-support-boundary.md` — package dependency/support boundary
- `.gitnexus/wiki/support-boundary-*.md` — detailed support-package boundaries for agent-core, AI providers, TUI, native/Rust, stats, bridge/utilities, Python RPC, and workspace tooling

Use this order:
1. Start with `.gitnexus/wiki/overview.md` and the relevant module page before broad source search.
2. Use `.gitnexus/wiki/module_tree.json` to identify the source files owned by a module.
3. Cross-check any user-facing conclusion with direct source reads before presenting it as current fact.
4. If GitNexus MCP/tools are available, prefer them for graph lookups, impact analysis, and symbol relationships; otherwise read the generated wiki and source files directly.
5. Treat `packages/coding-agent/` as the primary analysis surface. For other packages, start from the matching support-boundary page and summarize them as dependency/support boundaries unless the user explicitly widens scope.

Refresh shared GitNexus outputs with `bun run gitnexus:analyze`; it runs the analyzer for this subproject root and regenerates `.gitnexus/wiki/document-index.md`.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **gajae-code-part7** (52574 symbols, 134660 relationships, 300 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/gajae-code-part7/context` | Codebase overview, check index freshness |
| `gitnexus://repo/gajae-code-part7/clusters` | All functional areas |
| `gitnexus://repo/gajae-code-part7/processes` | All execution flows |
| `gitnexus://repo/gajae-code-part7/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
