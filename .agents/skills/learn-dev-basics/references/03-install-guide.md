# learn-dev-basics Installation Guide

> This skill works with both **Claude Code** and **Codex**. Follow the instructions for your tool.

---

## Method 1: Install from skills.sh (Recommended)

Works for any AI coding agent with a single command:

```bash
npx skills add [owner]/fastcampus-harness-online-learning
```

After installation, launch your AI coding agent and the skill is automatically recognized.

---

## Method 2: Clone the Course Repository

Clone the repository — the skill is included automatically:

```bash
git clone https://github.com/[repo-address].git
cd [repo-name]
```

### Using with Claude Code

```bash
claude
# Inside Claude Code:
/learn-dev-basics
```

Claude Code auto-detects skills in the `.claude/skills/` directory.

### Using with Codex

```bash
codex
# Inside Codex:
/learn-dev-basics
```

Codex auto-detects skills in the `.agents/skills/` directory. Both paths are included in the repo.

---

## Method 3: Manual Installation

Download the skill files and place them in your tool's skill directory.

### Claude Code Manual Install

**Step 1:** Create the skill directory
```bash
mkdir -p ~/.claude/skills/omc-learned/learn-dev-basics/references
```

**Step 2:** Copy these 4 files into that directory:

| File | Location |
|------|----------|
| `SKILL.md` | `~/.claude/skills/omc-learned/learn-dev-basics/SKILL.md` |
| `01-cli-basics.md` | `~/.claude/skills/omc-learned/learn-dev-basics/references/01-cli-basics.md` |
| `02-git-basics.md` | `~/.claude/skills/omc-learned/learn-dev-basics/references/02-git-basics.md` |
| `03-install-guide.md` | `~/.claude/skills/omc-learned/learn-dev-basics/references/03-install-guide.md` |

**Step 3:** Verify
```bash
claude
# Inside Claude Code:
/learn-dev-basics
```

### Codex Manual Install

**Step 1:** Create the skill directory
```bash
mkdir -p ~/.codex/skills/learn-dev-basics/references
```

**Step 2:** Copy the same 4 files into the Codex path:

| File | Location |
|------|----------|
| `SKILL.md` | `~/.codex/skills/learn-dev-basics/SKILL.md` |
| `01-cli-basics.md` | `~/.codex/skills/learn-dev-basics/references/01-cli-basics.md` |
| `02-git-basics.md` | `~/.codex/skills/learn-dev-basics/references/02-git-basics.md` |
| `03-install-guide.md` | `~/.codex/skills/learn-dev-basics/references/03-install-guide.md` |

**Step 3:** Verify
```bash
codex
# Inside Codex:
/learn-dev-basics
```

### Project-Level Installation (Both Tools)

To use the skill only within a specific project:

| Tool | Project-level path |
|------|-------------------|
| Claude Code | `project/.claude/skills/learn-dev-basics/` |
| Codex | `project/.agents/skills/learn-dev-basics/` |

---

## Verification

| Tool | How to verify |
|------|--------------|
| Claude Code | Run `claude` → type `/learn-dev-basics cli` → CLI guide appears in Korean → success |
| Codex | Run `codex` → type `/learn-dev-basics cli` → CLI guide appears in Korean → success |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not recognized | Check file paths. Ensure `SKILL.md` filename is exact and directory structure matches |
| Claude Code not installed | Run `npm install -g @anthropic-ai/claude-code` |
| Codex not installed | Run `npm install -g @openai/codex` |
| Node.js not found | Install from nodejs.org (download the LTS version) |
| Permission error on npm install | Do NOT use `sudo` as a first resort. Instead: (1) Install Node.js using the official installer from nodejs.org, or (2) Use a Node version manager like `nvm` or `fnm` which avoids permission issues entirely. Only use `sudo` as an absolute last resort, and understand it grants administrator privileges |
| `npx skills add` fails | Requires Node.js 18+. Check with `node -v` |
