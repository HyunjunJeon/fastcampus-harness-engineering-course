# Git Basics Guide

## What is Git?

> In Google Docs, you can open "Version History" to see who changed what and when, and revert to any previous version. **Git is "version history" for code files.**

Why Git matters when using AI coding agents:
- **Safety net:** When the AI changes code incorrectly, Git lets you go back to a working state
- **Tracking:** The AI agent reads Git's change records (diff) to verify its own work
- **Collaboration:** Multiple people (or multiple AIs) can safely work on the same project

---

## Why Git is Critical: The Harness Engineering Evidence

In Harness Engineering (Birgitta Böckeler, 2026; published at martinfowler.com), Git functions as the primary **feedback sensor** — the mechanism that observes what the AI agent did and enables correction. Here is the evidence for why this matters:

### The Silent Failure Problem

A 2026 study (arXiv:2604.12311) tested 450 vibe-coded Python scripts for construction-safety calculations across three frontier models (Claude, GPT-4o-Mini, Gemini). The findings:

| Metric | Value |
|--------|-------|
| Scripts that ran successfully | ~85% |
| **Silent Failure Rate among working scripts** | **~45%** |
| GPT-4o-Mini mathematical inaccuracies | ~56% |

**What this means:** In this domain, nearly half of AI-generated code that *compiled and ran* still produced wrong results. The code looked fine. It didn't crash. But the logic was wrong. This is a domain-specific study, but the pattern applies broadly: AI code can fail silently, and without Git's diff and revert capabilities, these failures are invisible.

### How Git Acts as a Harness

In Böckeler's framework, the harness operates as a steering loop:

1. **Guide** the agent before generation (CLAUDE.md, AGENTS.md, architecture rules)
2. **Sense** the result after generation (linters, type checkers, tests, `git diff`, code review)
3. **Feed back** sensor output to the agent for self-correction
4. **Integrate** only when verified (commit, push, merge)

Git is the infrastructure for steps 2-4. Specifically:
- `git diff` = the sensor that reveals what actually changed
- `git commit` = the checkpoint that makes changes reversible
- `git branch` = the isolation that makes experiments safe
- `git revert` = the rollback that undoes mistakes in seconds

### What Anthropic Says

Anthropic's Claude Code best practices (code.claude.com/docs/en/best-practices) identify verification as the single highest-leverage practice:

> *"Claude performs dramatically better when it can verify its own work — run tests, compare screenshots, and validate outputs."*

The docs also warn about the "trust-then-verify gap": without clear success criteria and verification, plausible-looking AI output may not actually work. The recommended mitigation is to always provide verification criteria — tests, scripts, or commands that check output.

The official workflow places Git at the final step: **Explore → Plan → Implement → Commit**. Anthropic also explicitly distinguishes between session-level checkpoints (which are reversible within a Claude Code conversation) and Git (which provides durable, long-term history that persists across sessions and machines). This makes Git the permanent safety net, not just a convenience.

### What Professional Developers Do

The Stack Overflow 2025 Developer Survey found:
- **46%** of developers distrust AI output accuracy
- Only **3.1%** highly trust it
- **58.7%** do not plan to use AI for committing/reviewing code

Meanwhile, research (arXiv:2512.14012) titled "Professional Software Developers Don't Vibe, They Control" found that experienced developers use AI agents as productivity tools **while retaining control over quality-critical decisions**. This is consistent with Git-based review workflows where every AI change is inspectable via diff and reversible via revert.

### What This Means for Non-Developers

These statistics might sound alarming, but that's exactly why Git exists as a safety harness. You don't need to catch every error yourself — you need the tools to make errors visible and reversible. That's what Git does.

You are not learning Git to become a software engineer. You are learning Git to **safely supervise an AI agent** that generates code on your behalf. The three essential Git skills are:

1. **See what changed** (`git diff`) — inspect the AI's work
2. **Save checkpoints** (`git commit`) — create restore points
3. **Undo mistakes** (`git revert` / `git switch main`) — roll back when needed

GitHub's own non-developer tutorial recommends committing frequently — after each successful iteration — so you can always return to a previous working version. (docs.github.com/en/copilot/tutorials/vibe-coding)

**Sources:** Birgitta Böckeler (martinfowler.com/articles/harness-engineering.html), arXiv:2604.12311, Anthropic Claude Code Best Practices (code.claude.com/docs/en/best-practices), Anthropic Checkpointing (code.claude.com/docs/en/checkpointing), Stack Overflow 2025 Survey (survey.stackoverflow.co/2025/ai), arXiv:2512.14012, GitHub Docs (docs.github.com/en/copilot/tutorials/vibe-coding)

---

## Concepts Before Commands

Before learning Git commands, these three concepts make everything click:

### The Staging Area

Git doesn't save all changes automatically. Instead, you pick which changes to include in each save:

```
Edit files → Select files (git add) → Save checkpoint (git commit)
```

Think of it like filing papers: you spread papers on your desk (editing), put the ones you want to keep into a folder (staging with `add`), then seal and label the folder (committing). This two-step process exists so you can organize saves logically rather than dumping everything at once.

### Remote and Origin

- **Remote** = a copy of your project stored on the internet (usually GitHub). Like having a backup of your files in the cloud.
- **Origin** = the default name Git gives to the remote you downloaded from. When you see `origin` in commands, it just means "the GitHub version."

### The Core Workflow

```
[Your Computer]                              [GitHub]
Edit files → git add → git commit    →    git push →    Remote copy
                                      ←    git pull ←
```

**Daily routine:** Edit → `add` → `commit` → `push`. That's it.

---

## ★ Essential Commands

### `git clone` — Copy a Project to Your Computer

**Analogy:** Like photocopying an entire binder. You get your own complete copy of the project, including all its history.

**Why you need this:** To download projects from GitHub for your AI agent to analyze, or to join a team project.

**Usage:**
```bash
git clone URL
```

**Example:**
```bash
$ git clone https://github.com/user/cool-project.git
Cloning into 'cool-project'...
done.

$ cd cool-project
$ ls
README.md    src    package.json
```

**Common mistakes:**
- `fatal: repository not found` → URL is wrong or it's a private repository.
- Clone creates a folder automatically. You need to `cd` into it.

**AI agent connection:** Clone a project, then launch your AI agent — it can read and explain the entire project to you.

---

### `git status` — Check What Changed

**Analogy:** Like viewing a checklist of "what changed today."

**Why you need this:** The first thing to run after the AI modifies files. Shows exactly what was touched.

**Usage:**
```bash
git status
```

**Example:**
```bash
$ git status
On branch main
Changes not staged for commit:
  modified:   README.md

Untracked files:
  new-file.txt
```

**Reading the output:**
| Status | Meaning | Color |
|--------|---------|-------|
| `modified` | Existing file was changed | Red |
| `Untracked files` | New file Git hasn't seen before | Red |
| `Changes to be committed` | Staged, waiting for commit | Green |

**AI agent connection:** After the AI works, run `git status` to see which files it changed.

---

### `git add` — Select Files to Save

**Analogy:** Like putting selected papers into a folder before filing. You're choosing which changes go into the next checkpoint.

**Why you need this:** You can selectively include specific changes, or include everything at once with `git add .`.

**Usage:**
```bash
git add filename       # Select a specific file
git add .              # Select all changed files
```

**Example:**
```bash
$ git add README.md
$ git status
Changes to be committed:
  modified:   README.md       # Turns green — selected for saving!
```

**Common mistakes:**
- `git add` alone doesn't save! You must follow with `git commit`.
- Wrong file staged? Undo with: `git restore --staged filename`

**AI agent connection:** When the AI modified multiple files but you only want to save some, use `git add filename` to pick selectively.

---

### `git commit` — Save a Checkpoint

**Analogy:** Like sealing and labeling a folder of papers. The folder (from `git add`) is now permanently filed with a description on the label.

**Why you need this:** Commits are Git's core feature. Each commit is a checkpoint you can return to. If the AI breaks something, revert to the last commit.

**Usage:**
```bash
git commit -m "description of what changed"
```

**Example:**
```bash
$ git add .
$ git commit -m "Add installation instructions to README"
[main abc1234] Add installation instructions to README
 1 file changed, 5 insertions(+)
```

**Good commit messages:**
| Bad | Good |
|-----|------|
| "update" | "Add email change feature to user profile" |
| "fix" | "Fix cart quantity calculation error" |
| "changes" | "Refactor login page to use JWT tokens" |

**Common mistakes:**
- Forgot `-m` and a text editor opened? Type `:q!` then Enter to escape.
- `nothing to commit` → Run `git add` first.

**AI agent connection:** Before asking the AI to make big changes, run `git commit` to save the current state. If things go wrong, you can go back.

---

### `git push` — Upload to Remote

**Analogy:** Like backing up your filed folders to the cloud. Even if your computer breaks, your work survives on GitHub.

**Why you need this:** Push makes your work permanent and accessible from anywhere.

**Usage:**
```bash
git push origin main           # Upload main branch to GitHub
```

**Example:**
```bash
$ git push origin main
To https://github.com/user/my-project.git
   abc1234..def5678  main -> main
```

**Common mistakes:**
- `rejected` error → GitHub has changes you don't have. Run `git pull` first, then push again.
- If asked for credentials, enter your GitHub username and **Personal Access Token** (not your password).

**AI agent connection:** After working with the AI, push to permanently save your results.

> **Important:** Never push files containing secrets (API keys, passwords, `.env` files). Add sensitive files to `.gitignore` before pushing. If unsure, ask your AI agent: "Are there any secrets in this project that shouldn't be pushed?"

---

## Useful Commands (learn as needed)

### `git init` — Create a New Repository

**Analogy:** Starting a new diary. You declare "from today, I'll track every change in this folder."

**Usage:**
```bash
mkdir my-project
cd my-project
git init
```

Note: If you plan to push to GitHub later, you'll need to connect a remote first: `git remote add origin URL`.

---

### `git log` — View History

**Analogy:** Flipping through a filing cabinet to see all past checkpoints.

**Usage:**
```bash
git log --oneline    # Compact view (recommended)
```

**Example:**
```bash
$ git log --oneline
abc1234 Add installation instructions
def5678 Initial project setup
```

Press **q** to exit if the log is long.

---

### `git diff` — Compare Changes

**Analogy:** A spot-the-difference game between the old and new versions.

**Usage:**
```bash
git diff              # View unstaged changes
git diff --staged     # View staged changes
```

Red lines (`-`) = deleted. Green lines (`+`) = added. Press **q** to exit.

**AI agent connection:** After the AI edits code, `git diff` shows exactly what changed. "Trust but verify."

---

### `git pull` — Download Latest from Remote

**Analogy:** Syncing the latest version from the cloud — like refreshing a shared Google Doc.

**Usage:**
```bash
git pull origin main
```

**Tip:** Pull before starting each work session to minimize conflicts.

---

### `git branch` — Manage Branches

**Analogy:** Game save slots. The main save (main) stays untouched while you experiment in a new slot.

**Why you need this:** Create a branch before risky AI experiments. If things go wrong, your main code is safe.

**Usage:**
```bash
git branch                    # List branches (* = current)
git branch experiment         # Create a new branch
git branch -d experiment      # Delete a branch
```

---

### `git switch` — Switch Branches

**Analogy:** Loading a different save slot.

**Usage:**
```bash
git switch branch-name        # Switch to existing branch
git switch -c new-branch      # Create AND switch (most common!)
```

**Example:**
```bash
$ git switch -c ai-experiment
Switched to a new branch 'ai-experiment'

# Work with AI here...

$ git switch main              # Return to main
Switched to branch 'main'
```

> **Note:** You may see `git checkout` in older tutorials — it does the same thing but is less clear. `git switch` is the modern, beginner-friendly version.

**AI agent connection:** For risky AI tasks: `git switch -c ai-test` → AI works → like the result? merge. Don't like it? `git switch main`.

---

### `git merge` — Combine Branches

**Analogy:** Merging two separately edited copies of the same document into one final version.

**Usage:**
```bash
git switch main                # First, go to main
git merge experiment           # Bring in changes from experiment
```

If the same lines were edited differently in both branches, a **conflict** occurs. See the next section.

---

## Handling Conflicts

> A conflict means "two edits landed on the same sentence." Git can't decide which version is correct, so it asks you to choose. It looks scary the first time, but the structure is simple.

### When do conflicts happen?

- When merging branches with `git merge`
- When pulling remote changes with `git pull`
- When the same lines of a file were edited differently in two places

### Reading Conflict Markers

The file shows both versions with markers:

```
<<<<<<< HEAD
My version of this line
=======
Their version of this line
>>>>>>> experiment
```

| Marker | Meaning |
|--------|---------|
| `<<<<<<< HEAD` | Start of **my** version |
| `=======` | Boundary between the two versions |
| `>>>>>>> branch-name` | End of **their** version |

### Resolving Conflicts

#### Method 1: Ask the AI (Recommended)

Simply tell your AI agent:

```
Merge conflict happened. Please resolve it.
```

The AI reads both sides, understands the intent, and merges appropriately. You review and approve.

#### Method 2: Resolve Manually

1. Open the file
2. Delete all three marker lines (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Keep only the content you want
4. Save, then run:

```bash
git add .
git commit -m "Resolve merge conflict"
```

### If Things Get Messy

Run `git merge --abort` to cancel the merge and return to the pre-merge state — like pressing undo. You can always start over.

---

## Summary: Basic Git Routine for Working with AI

```
1. git pull              ← Start with latest state
2. git switch -c experiment  ← Work in a safe branch
3. (Work with AI)
4. git add .             ← Select changed files
5. git commit -m "description"  ← Save checkpoint
6. git push              ← Back up to cloud
```

Happy with the AI's work → `git switch main` then `git merge experiment`
Not happy → `git switch main` (experiment branch stays separate, delete later)

---

## Further Reading: Official Git Documentation

| Resource | URL | Description |
|----------|-----|-------------|
| **Git Official Site** | https://git-scm.com | Downloads, docs, community |
| **Git Book (Korean)** | https://git-scm.com/book/ko/v2 | Free online textbook, Korean translation available |
| **Git Command Reference** | https://git-scm.com/docs | Detailed options for every command |
| **GitHub Docs (Korean)** | https://docs.github.com/ko | Official GitHub guide, Korean supported |

> **Tip:** The fastest way to learn about a specific command is to ask your AI agent. Use official docs to verify or to dig deeper.
