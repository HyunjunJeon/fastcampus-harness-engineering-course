---
name: init-deep
description: Generate and maintain hierarchical AGENTS.
---

# init-deep - Advanced AGENTS.md Generator

Create or update a project-wide AGENTS.md hierarchy with smarter scoring, tighter deduping, and more reliable discovery.

md files with complexity-scored subdirectories and strict deduplication. Use when asked to create, refresh, or improve AGENTS.md documentation, project knowledge bases, or directory-level agent guides; supports update or clean-regenerate workflows for codebases.

## Quick Start

```bash
/init-deep                # Update mode: preserve + refresh + add missing
/init-deep --create-new   # Remove existing AGENTS.md and regenerate
/init-deep --max-depth=3  # Default depth cap
```

## Modes and Preservation

**Update mode (default):**
- Read existing AGENTS.md first.
- Preserve manual sections wrapped by:
  - `<!-- MANUAL START -->` ... `<!-- MANUAL END -->`
  - `<!-- KEEP -->` single-line markers.
- Only refresh generated sections; do not delete user notes.

**Create-new mode:**
- Remove existing AGENTS.md only after listing them.
- Prefer renaming to `AGENTS.md.bak.<YYYYMMDD>` before regen.

## Stability Rules

- Keep section order stable to minimize diff churn.
- Sort directory lists alphabetically.
- Avoid reflowing lines unless content changes.

## Core Workflow

1. Discover structure + existing AGENTS.md
2. Score directories + select targets
3. Generate root + subdirectory AGENTS.md
4. Deduplicate + validate quality gates

## Phase 1: Discovery

Run fast inventory commands; prefer `rg` for lists.

```bash
# Existing AGENTS/CLAUDE docs
rg --files -g 'AGENTS.md' -g 'CLAUDE.md'

# Directory depth distribution (ignore common build/venv dirs)
find . -type d -not -path '*/.*' \
  -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/venv/*' \
  -not -path '*/dist/*' -not -path '*/build/*' | awk -F/ '{print NF-1}' | sort -n | uniq -c

# Files per directory (top 40)
find . -type f -not -path '*/.*' \
  -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/venv/*' \
  -not -path '*/dist/*' -not -path '*/build/*' | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -40
```

Optional: skim for explicit warnings.

```bash
rg -n "DO NOT|NEVER|DEPRECATED|MUST NOT|BREAKING" .
```

## Phase 2: Scoring + Target Selection

Use a weighted score to decide which directories need their own AGENTS.md.

**Score =**
- 3x file count (>20)
- 2x subdir count (>5)
- 2x code ratio (>70%)
- 2x boundary signal (entry points, package roots, or exports)
- 1x change hotspot (large number of files or tests)

**Decision Rules**
- Root: ALWAYS create.
- Score >15: create.
- Score 9-15: create if distinct domain or owned subsystem.
- Score <9: skip (covered by parent).

Boundary signals to treat as strong indicators:
- `pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`
- `__init__.py` or `index.ts` in a folder with many files
- Dedicated `tests/`, `scripts/`, `docs/`, `data/` roots

Negative signals (lower priority):
- Vendored or generated dirs: `node_modules`, `dist`, `build`, `.venv`, `venv`
- Single-purpose output folders (e.g., `coverage`, `.pytest_cache`)

## Phase 3: Generate AGENTS.md

### Root AGENTS.md Template

- 50-150 lines.
- No generic advice.
- Include only project-specific conventions.
- Must reference all child AGENTS.md (Hierarchical Memory).

```markdown
# PROJECT KNOWLEDGE BASE

**Generated:** {TIMESTAMP}

## OVERVIEW
{what it is + core stack + unique constraints}

## STRUCTURE
{tree of key dirs with short purpose lines}

## WHERE TO LOOK
| Task | Location | Notes |

## CONVENTIONS
{only deviations from normal patterns}

## ANTI-PATTERNS
{explicit "do not" and risky behaviors}

## COMMANDS
{dev/test/build/lint}

## RELATED AGENTS
{links to each subdirectory AGENTS.md}
```

### Subdirectory AGENTS.md

- 30-80 lines.
- Only unique, local info (no parent repeats).
- Include entry points, local commands, and pitfalls.
- Must reference parent and direct children (if any).

Suggested footer section:
```
## RELATED AGENTS
- Parent: ../AGENTS.md
- Children: ./subdir/AGENTS.md
```

## Phase 4: Deduplicate + Validate

**Dedup rules**
- Parent keeps global info; child keeps local-only info.
- If a child repeats a line from parent, remove it.
- Prefer tables for dense lookups.

**Automated dedup**
- Run `scripts/dedup_agents.py` to detect and remove repeated lines between parent/child pairs.
- Always review the diff; keep domain-specific phrasing even if lines are similar.

```bash
# Dry run
python scripts/dedup_agents.py --root . 

# Apply changes
python scripts/dedup_agents.py --root . --apply
```

**Quality gates**
- Root exists and within length targets.
- Subdirectory docs exist only where score warrants.
- No AGENTS.md inside `node_modules`, `dist`, `build`, or virtualenvs.
- Commands and paths verified.
- Hierarchical Memory: every AGENTS.md references its parent (if any) and its immediate children (if any).

Optional duplicate scan (parent-child overlap):

```bash
python - <<'PY'
from pathlib import Path
import difflib

files = [p for p in Path('.').rglob('AGENTS.md')]
files = [p for p in files if 'node_modules' not in p.parts and 'dist' not in p.parts and 'build' not in p.parts]
for child in files:
    parent = child.parent.parent / 'AGENTS.md'
    if parent.exists():
        c = child.read_text().splitlines()
        p = parent.read_text().splitlines()
        overlap = sum(1 for line in c if line in p and line.strip())
        if overlap > 10:
            print(f'High overlap: {child} ({overlap} lines)')
PY
```

## Verification Checklist

- Root AGENTS.md exists and within 50-150 lines
- Subdirectory AGENTS.md exists only for scored targets and within 30-80 lines
- Parent/child duplication is minimal and intentional
- **Hierarchical Memory**: root references all subdirectory AGENTS.md; each child links back to its parent
- "Where to Look" table includes the most common tasks and correct paths
- Commands are verified and runnable
- No AGENTS.md created in build/venv/vendor outputs

## Anti-Patterns

- Writing AGENTS.md everywhere "just in case"
- Copy-pasting root content into subdirectories
- Leaving TODOs or placeholder sections
- Including generic coding advice

## Final Report Format

```
=== init-deep Complete ===

Mode: {update | create-new}
Files:
  ✓ ./AGENTS.md (root, {N} lines)
  ✓ ./path/AGENTS.md ({N} lines)

Dirs Analyzed: {N}
AGENTS.md Created: {N}
AGENTS.md Updated: {N}
Skipped (low score): {N}
```
