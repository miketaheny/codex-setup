# Agent-Flow Demo Plan

Use this as a script for a live demo, screen recording, or annotated walkthrough.

## Demo Goal

Show how Agent-Flow turns a new Git repo into a safer agent-ready workspace with shared instructions, agent adapters, devlog conventions, and repeatable skills.

## Audience

- solo developers adopting AI coding agents
- maintainers reviewing the workflow
- stakeholders evaluating whether Agent-Flow is worth standardizing

## Setup

Prepare:

- this Agent-Flow setup repo
- a temporary sample Git repo on `development`
- terminal with enough font size for recording
- optional second pane showing generated files

## Script

### 1. Install Agent-Flow

```bash
./scripts/install.sh
```

Show the resulting locations:

```bash
find ~/.agent-flow -maxdepth 2 -type f | sort
find ~/.codex/skills -maxdepth 2 -name SKILL.md | sort
test -f ~/.claude/CLAUDE.md && echo "Claude adapter installed"
```

### 2. Initialize a Sample Repo

```bash
mkdir /tmp/agent-flow-demo
cd /tmp/agent-flow-demo
git init -b development
~/.agent-flow/scripts/init-repo.sh --yes --no-staging
```

Show:

- `AGENT-FLOW.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.agent-flow/config.toml`
- `.git/hooks/pre-push`
- `devlog/README.md`
- `docs/decisions/000-template.md`

### 3. Explain the Daily Loop

Reference the diagram in `docs/USER-GUIDE.md`.

Narrative:

```text
Start from the checked-out parent branch, classify the prompt, create a task worktree, validate, write devlog, update docs, run review, ask before merge, and check child worktrees before pushing. Later, development promotes to main, with optional staging when configured.
```

### 4. Demonstrate Task Lifecycle

```bash
~/.agent-flow/scripts/start-task.sh --class tiny docs demo-copy
cd ../agent-flow-demo-demo-copy
```

Show that the task branch has parent metadata:

```bash
git config --get branch.docs/demo-copy.agentFlowParent
git config --get branch.docs/demo-copy.agentFlowTaskClass
```

After a small committed change, run:

```bash
~/.agent-flow/scripts/finish-task.sh
```

Show the `ASK_USER_MERGE` output.

### 5. Demonstrate Backlog Migration

Create a sample legacy task:

```bash
mkdir -p backlog/tasks
$EDITOR backlog/tasks/task-1-demo.md
```

Run:

```bash
python3 ~/.agent-flow/skills/af-migrate-backlog-devlog/scripts/migrate_backlog_to_devlog.py .
python3 ~/.agent-flow/skills/af-migrate-backlog-devlog/scripts/migrate_backlog_to_devlog.py . --write
```

Show the generated devlog entry.

### 6. Close With Review

Run:

```bash
~/.agent-flow/scripts/review-snapshot.sh
~/.agent-flow/scripts/check-push-readiness.sh development
```

Show how the snapshot supports `af-review-gate`.

## Screenshot List

- install output
- generated home directories
- init output
- generated repo instruction files
- generated `.agent-flow/config.toml`
- migration dry-run output
- generated devlog entry
- review snapshot output
- push-readiness output

## Recording Notes

- Keep the first demo under three minutes.
- Use real terminal output rather than generated imagery for the primary walkthrough.
- Add a polished title card or generated visual only for external marketing versions.
