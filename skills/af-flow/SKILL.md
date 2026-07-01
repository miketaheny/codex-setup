---
name: af-flow
description: Start or adopt one Agent-Flow worktree session for file-changing agent work. Use when the user asks to change files, fix code, update docs, continue unfinished AF work, switch worktrees, or ensure a request happens in an isolated session before implementation.
---

# AF Flow

## Purpose

Use this as the entry workflow for any file-changing Agent-Flow session. Keep one chat focused on one coherent session worktree.

## Start Checklist

1. Read repo instructions first: `.agent-flow/config.toml`, `AGENT-FLOW.md`, `AGENTS.md`, and `CLAUDE.md` when present, plus any more specific nested instruction file for the edited path.
2. Confirm repository state:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short
git config --worktree --get agentFlow.parent || true
```

3. If the repo config has `mode = "disabled"`, disclose that Agent-Flow is disabled and do not enforce this workflow.
4. If the current checkout is `main`, `staging`, `master`, `production`, or `prod`, stop and switch to a user-controlled parent branch before starting work.
5. If already inside an AF session worktree and the request matches its direction, continue there. If the request changes direction, finish, pause, or abandon the current session before starting another.
6. If the current checkout is dirty before session start, do not hide those changes in a new worktree. Inspect them, create or require a devlog-backed commit for that existing work, then start the new session from a clean parent.

## Create Or Adopt

Work must happen in an isolated worktree. Check whether one already exists before creating anything new.

**If the agent provides native worktree isolation** (e.g. Claude Code's built-in worktree, a Codex session worktree already checked out): work within that. Record AF metadata into it and continue — do not create a second worktree.

**If no isolated worktree exists**, use the repo helper:

```bash
scripts/start-session.sh <type> <session-name>
```

Create a named branch only when explicitly requested:

```bash
scripts/start-session.sh --branch <type>/<session-name> <type> <session-name>
```

Use the manager to pick up existing AF work:

```bash
scripts/worktree-manager.py
scripts/worktree-manager.py --details <id>
scripts/worktree-manager.py --pickup <id>
```

Session metadata should stay small and machine-focused:

```text
agentFlow.kind = session
agentFlow.parent = <parent-branch>
agentFlow.sessionName = <session-name>
agentFlow.state = started|active|ready|merged
agentFlow.owner = agent
agentFlow.devlogPolicy = finish
agentFlow.startedAt = <timestamp>
agentFlow.lastTouchedAt = <timestamp>
agentFlow.branch = <explicit-branch> # only when branch-backed
```

## Work In Session

- Re-read repo instructions from the session worktree.
- Keep edits scoped to the session goal.
- Update affected docs when behavior, setup, architecture, security, deployment, operations, onboarding, or user-facing workflows change.
- Add one `devlog/` entry before the session commit.
- Run relevant validation.
- Use `af-finish` to review, optionally show visual proof, commit if needed, and report merge readiness.

## Output

Report the session worktree path, recorded parent branch, whether work was created or adopted, and the next command or workflow step.
