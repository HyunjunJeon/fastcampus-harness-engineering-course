# CLI Basics Guide

> The terminal is a "text message window" for talking to your computer. Instead of double-clicking folders with a mouse, you type commands as text. AI coding agents run inside the terminal, so you need to know a few basic commands. But don't worry — you mainly need the terminal for "installation." After that, your AI agent handles most terminal work for you.

---

## Why CLI Matters: The Control Surface for AI Agents

In Harness Engineering (Birgitta Böckeler, 2026; published at martinfowler.com), a "harness" is the control system around an AI coding agent. The harness includes **guides** (context that steers the agent before it acts, such as CLAUDE.md and architecture docs) and **sensors** (tools that check results after the agent acts, such as linters, test runners, and `git diff`). Most of these sensors live in the terminal.

This is why CLI matters for AI agent users:

- **Visibility:** The terminal shows you exactly what commands the agent ran and what output it produced. IDE-based tools often abstract this away, making the agent's actions opaque.
- **Auditability:** Shell history and terminal logs create a complete record. Anthropic's Claude Code best practices recommend the workflow "Explore → Plan → Implement → Commit" — each step happens in the terminal.
- **Efficiency:** Anthropic's best practices note: *"CLI tools are the most context-efficient way to interact with external services."* CLI uses fewer tokens than GUI interactions, leaving more of the AI's context window for your actual work.
- **Composability:** You can chain commands, pipe output, and script workflows. This is how power users orchestrate AI agents at scale.
- **Portability:** CLI workflows work on any computer. GUI tool layouts change between versions; terminal commands don't.

The OPENDEV research (arXiv:2603.05344) found that terminal-native agents operate directly where developers "manage source control, execute builds, and deploy environments." Without CLI literacy, you depend entirely on what the agent chooses to tell you. With CLI literacy, you can ask for and inspect evidence yourself.

**Bottom line:** CLI is not a relic of the past — it is the primary control surface for AI coding agents. Learning 4 commands gives you the minimum viable control.

**Sources:** Birgitta Böckeler (martinfowler.com/articles/harness-engineering.html), Anthropic Claude Code Best Practices (code.claude.com/docs/en/best-practices), arXiv:2603.05344

---

## Opening the Terminal

- **Mac:** Spotlight (Cmd+Space) → type "Terminal" → Enter
- **Windows:** Start menu → search "PowerShell" → Enter
- **Linux:** Ctrl+Alt+T

If a dark screen with a blinking cursor appears, that's normal — it's just waiting for your text message!

---

## How to Enter Commands

Type a command and press **Enter** to run it. Results appear directly below.

```
$ command
result
```

> The `$` symbol means "type your command here." Don't type the `$` itself!

---

## Concepts Before Commands

Before diving into commands, three path concepts will help everything make sense:

- **`.` (dot)** — means "the current folder I'm in right now"
- **`..` (two dots)** — means "the folder one level above." Like going up one floor in a building.
- **`~` (tilde)** — means "my home folder." Your personal base location on the computer.

**Relative vs absolute paths:**
- **Absolute path** starts from the root: `/Users/username/Desktop/my-project` — like a full street address.
- **Relative path** starts from where you are now: `./src/app.js` or `../other-folder` — like saying "the room next door."

You don't need to memorize this — just know these symbols exist so they aren't mysterious when you see them.

---

## ★ Essential Commands (needed for installation)

These 4 commands are all you need to install and launch an AI coding agent.

### `pwd` — Check Your Current Location

**Analogy:** Like checking the "You are here" marker on a building directory.

**Why you need this:** Your AI coding agent needs to run inside a project folder. If you don't know where you are, you might work in the wrong place.

**Usage:**
```bash
pwd
```

**Example:**
```bash
$ pwd
/Users/username/Desktop
```
→ This means "I'm currently in the Desktop folder."

**Common mistakes:**
- Nothing happened? → Probably forgot to press Enter.
- Path looks really long? → Normal. Computer folder structures are deeply nested.

**AI agent connection:** Before launching your AI coding agent, use `pwd` to confirm you're in the right project folder.

---

### `cd` — Move to Another Folder

**Analogy:** Like walking to a different room in a building.

**Why you need this:** You must navigate to your project folder before launching your AI agent. Running it from the wrong place means the AI can't find your project files.

**Usage:**
```bash
cd foldername
```

**Example:**
```bash
$ cd Desktop
$ cd my-project
$ pwd
/Users/username/Desktop/my-project
```

**Common patterns:**
| Command | Meaning | Description |
|---------|---------|-------------|
| `cd ..` | Go up one level | Go to the parent folder |
| `cd ~` | Go to home folder | Return to your personal base |
| `cd -` | Go to previous folder | Go back to where you just were |

**Common mistakes:**
- `cd: no such file or directory` → The folder name is wrong, or doesn't exist here. Use `ls` to check what's available.
- Folder names with **spaces** need quotes: `cd "My Project"`.

**AI agent connection:** `cd` into your project folder, then type the launch command for your AI agent (e.g., `claude` or `codex`) to start it in that project context.

---

### `ls` — List Files

**Analogy:** Like looking around a room to see what's inside.

**Why you need this:** Confirms you're in the right folder, or checks whether files were created successfully.

**Usage:**
```bash
ls
```

**Example:**
```bash
$ ls
README.md    package.json    src    node_modules
```

**Useful options:**
| Option | Meaning |
|--------|---------|
| `ls -l` | Detailed view (file size, date, etc.) |
| `ls -a` | Show hidden files (those starting with `.`) |
| `ls -la` | Both combined |

**Common mistakes:**
- Nothing showed up? → The folder is empty. That's fine, not an error.
- Too many files? → Add a folder name: `ls src`

**AI agent connection:** After installation, you can just ask your AI agent "what files are here?" and it runs `ls` for you.

---

### `mkdir` — Create a Folder

**Analogy:** Like making a new drawer to store things in.

**Why you need this:** When starting a new project, you need an empty folder to work in.

**Usage:**
```bash
mkdir foldername
```

**Example:**
```bash
$ mkdir my-first-project
$ ls
my-first-project
$ cd my-first-project
```

**Common mistakes:**
- `mkdir: cannot create directory: File exists` → A folder with that name already exists.
- Avoid spaces in folder names. Use hyphens instead: `mkdir my-project`.

**AI agent connection:** Start a new project quickly by chaining commands: first `mkdir my-app`, then `cd my-app`, then launch your AI agent.

---

## Optional Commands (good to know)

Your AI coding agent can handle these after installation, but understanding them helps you read what the AI is doing.

### `touch` — Create an Empty File

**Analogy:** Pulling out a blank page — nothing written yet, but ready.

**Why you need this:** Sometimes you create a file before asking the AI to fill it. But honestly, your AI agent can create files for you — just say "create hello.txt."

**Usage:**
```bash
touch hello.txt
```

**Common mistakes:**
- Forgot the extension: `touch hello` creates a file without one. Add `.txt`, `.md`, `.js` etc.
- Running `touch` on an existing file doesn't erase it — only updates the modification date. Safe!

---

### `rm` — Delete Files/Folders

> **WARNING:** Files deleted with `rm` do NOT go to the Recycle Bin/Trash. They vanish permanently, like putting paper through a shredder.

**Analogy:** A paper shredder — no recycle bin, no undo.

**Why you need this:** You might need to clean up files, but it's risky. Whenever possible, let your AI agent handle deletion — it asks for confirmation first.

**Usage:**
```bash
rm filename          # Delete a file
rm -i filename       # Ask "are you sure?" before deleting (safe!)
rm -r foldername     # Delete an entire folder (everything inside disappears!)
```

> **NEVER run:** `rm -rf /` — This deletes everything on your computer.

**Safer alternatives:**
- macOS: `trash filename` (requires trash-cli) — sends to Trash
- Or delete through Finder/File Explorer — much safer
- Best: tell your AI agent "delete this file" — it asks for your approval first

---

### `cp` — Copy Files

**Analogy:** Using a photocopier — the original stays, you get a duplicate.

**Usage:**
```bash
cp original copy              # Copy a file
cp -r folder copyfolder       # Copy an entire folder
```

**AI agent connection:** Once you learn Git, you rarely need `cp` for backups — Git preserves all history. Before learning Git, `cp` is a simple safety net.

---

### `mv` — Move or Rename Files

**Analogy:** Moving furniture to another room, or changing a name tag.

**Usage:**
```bash
mv oldname newname        # Rename
mv file folder/           # Move to another folder
```

**Caution:** If a file with the new name already exists, it gets **overwritten without warning.**

---

### `cat` — View File Contents

**Analogy:** Opening a notebook to read what's inside.

**Usage:**
```bash
cat filename
```

For very long files, use `head filename` to see just the first 10 lines.

**AI agent connection:** Your AI agent can read files directly. But when you want to personally verify what the AI changed, `cat` is useful.

---

### `clear` — Clear the Screen

**Analogy:** Erasing a whiteboard — content isn't deleted, just hidden. Scroll up to see it again.

**Usage:** `clear` or shortcut **Ctrl+L**.

---

## Advanced: Pipes and Redirection (optional)

Your AI agent may suggest commands using these symbols. Understanding them removes the mystery.

### `|` (Pipe) — Chain Commands Together

**Analogy:** A factory conveyor belt. The first machine produces output, which rides the belt to the second machine for further processing.

**Usage:**
```bash
command1 | command2
```

**Examples:**
```bash
$ ls | grep test           # Find files containing "test"
test.js
test-utils.js

$ cat long-file.txt | head -5    # See first 5 lines only

$ ls | wc -l               # Count files
12
```

**Common combinations:**
| Combination | Meaning |
|-------------|---------|
| `command \| grep word` | Find a specific word in output |
| `command \| head -N` | Show first N lines only |
| `command \| wc -l` | Count lines (items) |

**Note:** `|` is typed with Shift + backslash key (usually near Enter). Don't confuse it with `\`.

---

### `>` and `>>` (Redirection) — Save Output to a File

**Analogy:** If pipe is a "conveyor belt," redirection is "putting results into a box."

**Usage:**
```bash
command > filename       # Save to file (OVERWRITES existing content!)
command >> filename      # Append to end (keeps existing content — safer)
```

**Example:**
```bash
$ ls | grep test > test-files.txt    # Save filtered list to file
$ cat test-files.txt                 # Verify it was saved
test.js
test-utils.js
```

**Caution:** `>` erases existing file content. When in doubt, use `>>` (append) instead.

---

## Self-Service Learning

When you want to know what options a command has, add `--help`:

```bash
git --help          # See all Git commands
git commit --help   # See commit options specifically
ls --help           # See ls options
```

This works for almost every command and is the fastest way to learn on your own.

---

## Terminal Survival Tips

### 1. Up/Down Arrow Keys — Recall Previous Commands
Press **↑** to bring back the last command. Keep pressing for older history. No retyping needed.

### 2. Tab Key — Auto-Complete
Type part of a name and press **Tab** to auto-complete. Reduces typos and saves time.

### 3. Ctrl+C — Emergency Stop
If something went wrong or a command won't stop, press **Ctrl+C** to force-stop. It doesn't break anything.

---

## Summary

**★ Essential (4 commands for AI agent installation):**
`pwd`, `cd`, `ls`, `mkdir`

**Optional (your AI agent handles these after installation):**
`touch`, `rm`, `cp`, `mv`, `cat`, `clear`

**Advanced (for understanding AI-suggested commands):**
`|` (pipe), `>` / `>>` (redirection), `--help`
