---
name: learn-dev-basics
description: A beginner-friendly guide to CLI basics and Git fundamentals for non-developers, grounded in the Harness Engineering framework. Uses everyday analogies, real examples, and evidence-based reasoning (including the ~45% Silent Failure Rate in AI-generated code) to explain why CLI and Git are essential control surfaces for AI coding agents. Supports both Claude Code and Codex. Use this skill whenever users mention terminal, CLI, commands, command line, Git, version control, development basics, coding beginner, dev-basics, learn-cli-git, harness engineering, AI safety, vibe coding, or say they don't know terminal/Git commands, or want to learn development tool basics, or ask why CLI/Git matter for AI agents.
compatibility: Claude Code, Codex (OpenAI)
metadata:
  argument-hint: "[cli|git|install|all]"
  aliases: dev-basics, learn-cli-git
---

# Development Tools Basics for Non-Developers

This skill helps people with little to no coding experience learn the minimum CLI and Git knowledge needed to use AI coding agents (Claude Code, Codex, etc.). The goal is not to "master" the terminal or Git, but to build just enough confidence to install and safely use an AI coding agent — like getting a driver's license, not becoming a mechanic.

## Why CLI and Git? The Harness Engineering Perspective

This skill is grounded in the **Harness Engineering** framework (Birgitta Böckeler, 2026; published at martinfowler.com). A "harness" is the control system surrounding an AI coding agent — everything except the model itself — designed to guide the agent's output and catch errors before they reach production.

The harness has two parts:
- **Guides (feedforward):** steer the agent before it acts — CLAUDE.md rules, AGENTS.md, architecture docs, coding conventions. Anthropic's best practices describe CLAUDE.md as *"a special file that Claude reads at the start of every conversation"* that provides *"persistent context it can't infer from code alone"* — a direct example of a feedforward guide.
- **Sensors (feedback):** observe and correct after the agent acts — linters, type checkers, tests, `git diff`, code review, logs. These are the tools that catch errors the guide didn't prevent.

**CLI is how you access both guides and sensors.** The terminal is where deterministic tools (linters, test runners, build commands) live. Anthropic's Claude Code best practices note: *"CLI tools are the most context-efficient way to interact with external services."* Without CLI literacy, you cannot inspect what the agent is actually doing.

**Git is the primary feedback sensor.** Every commit is a checkpoint; every diff is evidence. In a study of 450 vibe-coded safety-calculation scripts, researchers found an approximately **45% Silent Failure Rate** — code that runs but produces wrong results (arXiv:2604.12311). Git's diff/revert/branch system is what makes these silent failures discoverable and reversible.

Anthropic's Claude Code best practices emphasize verification as the highest-leverage practice: *"Claude performs dramatically better when it can verify its own work — run tests, compare screenshots, and validate outputs."* The recommended workflow (Explore → Plan → Implement → Commit) places Git at the final step. Anthropic also distinguishes between session-level checkpoints (reversible within a conversation) and Git (long-term history that persists across sessions) — making Git the durable safety net.

**Sources:** Birgitta Böckeler (martinfowler.com/articles/harness-engineering.html), arXiv:2604.12311, Anthropic Claude Code Best Practices (code.claude.com/docs/en/best-practices), Anthropic Checkpointing (code.claude.com/docs/en/checkpointing)

## Usage

- `/learn-dev-basics` or `/learn-dev-basics all` — Full CLI + Git guide
- `/learn-dev-basics cli` — CLI commands only
- `/learn-dev-basics git` — Git commands only
- `/learn-dev-basics install` — Installation guide for this skill
- Specific command: `/learn-dev-basics git commit` — That command's section only

## Routing

1. If the argument is `cli`, Read `references/01-cli-basics.md` from this skill's directory.
2. If the argument is `git`, Read `references/02-git-basics.md` from this skill's directory.
3. If the argument is `install`, Read `references/03-install-guide.md` from this skill's directory.
4. If no argument or `all`, Read both `01-cli-basics.md` and `02-git-basics.md`.
5. If a specific command name is included (e.g., `git commit`, `cd`), extract and present only that section.
6. For follow-up questions, refer back to the relevant reference file.

## Response Principles

When presenting content from this skill, follow these rules precisely:

### Language Rules
- **Always respond in Korean using 해요체 (polite informal register).** Keep it warm but not overly casual.
- **Keep commands, flags, paths, file names, and terminal output in English as-is.** Never translate them.
- **Introduce technical terms as:** 한글 설명 (English term). Example: "버전 관리 (version control)"
- **Translate table headers and warning labels into Korean.** Column data can stay in English.

### Pedagogy Rules
- **Lead with the analogy**, then explain "why you need this," then show usage/examples, then common mistakes, then the AI agent connection.
- **Explain "why" before "how".** Before showing how to use a command, explain why they need it.
- **Warn about dangerous commands.** For irreversible commands like `rm`, give a warning first and suggest safer alternatives.
- **Encourage naturally but not repetitively.** Use reassurance like "걱정 마세요" or "처음엔 누구나 헷갈려요" but don't repeat the same phrase. Vary encouragement across responses.

### Tool Neutrality
- **Use "AI 코딩 에이전트" or "AI 도구" as the default reference** to any AI coding agent. Only mention Claude Code or Codex by name when giving tool-specific instructions (e.g., installation commands, tool-specific features).

### Response Template (recommended flow per command)
```
비유 한 줄 → 왜 필요한지 → 명령어 사용법 → 실제 예시 → 자주 하는 실수 → AI 도구와의 연결
```

## CLI Commands Summary

| Command | What it does | Analogy |
|---------|-------------|---------|
| `pwd` | Show current location | "You are here" on a building directory |
| `cd` | Move to a folder | Walking to another room |
| `ls` | List files | Looking around a room |
| `mkdir` | Create a folder | Making a new drawer |
| `touch` | Create an empty file | Pulling out a blank page |
| `rm` | Delete (caution!) | Paper shredder (no recycle bin!) |
| `cp` | Copy | Photocopying a document |
| `mv` | Move/rename | Moving furniture / changing a name tag |
| `cat` | View file contents | Opening a notebook to read |
| `clear` | Clear the screen | Erasing a whiteboard |
| `\|` (pipe) | Chain commands | Factory conveyor belt |
| `>` / `>>` | Save output to file | Putting results in a box |
| `--help` | See command options | Reading the instruction manual |

Essential commands (★): `pwd`, `cd`, `ls`, `mkdir`. The rest are optional — your AI agent can handle them after installation.

## Git Commands Summary

| Command | What it does | Analogy |
|---------|-------------|---------|
| `git init` | Create new repository | Starting a new diary |
| `git clone` | Copy a project to your computer | Photocopying an entire binder |
| `git status` | Check what changed | Viewing a checklist |
| `git add` | Select files to save | Putting papers into a folder before filing |
| `git commit` | Save a checkpoint | Sealing and labeling that folder |
| `git log` | View history | Flipping through a filing cabinet |
| `git diff` | Compare changes | Spot-the-difference game |
| `git branch` | Manage branches | Game save slots |
| `git switch` | Switch branches | Loading a different save slot |
| `git merge` | Combine branches | Merging two separately edited documents |
| `git push` | Upload to remote | Backing up to the cloud |
| `git pull` | Download from remote | Syncing the latest version from cloud |
| Conflict | Same line edited differently | Two people edited the same sentence |

Essential commands (★): `git clone`, `git add`, `git commit`, `git push`. The rest become useful as you gain confidence.

## Installation

Use `/learn-dev-basics install` or read `references/03-install-guide.md`.
