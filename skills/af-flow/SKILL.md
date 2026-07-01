---
name: af-flow
description: Start or adopt one Agent-Flow worktree session for file-changing agent work. Use when the user asks to change files, fix code, update docs, continue unfinished AF work, switch worktrees, or ensure a request happens in an isolated session before implementation.
---

# AF Flow

## Purpose

Use this as the entry workflow for any file-changing Agent-Flow session. Keep one coherent working session in one worktree until the user explicitly asks to finish, review, reconcile, merge, or switch direction.

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
5. If already inside an AF session worktree and the request matches its direction, continue there. Do not finish just because a prompt completed.
6. If the current checkout is a parent repo and an active/incomplete AF worktree already matches the user's direction, pick up that worktree instead of creating a duplicate.
7. If the request is to wrap up, review, reconcile, merge, clean up, or switch away, route to `af-finish`, `af-review`, or `af-reconcile` instead of starting another worktree.
8. If the current checkout is dirty before session start, do not hide those changes in a new worktree. Inspect them, create or require a devlog-backed commit for that existing work, then start the new session from a clean parent.

## Create Or Adopt

Work must happen in an isolated worktree. Check whether one already exists before creating anything new.

**If the agent provides native worktree isolation** (e.g. Claude Code's built-in worktree, a Codex session worktree already checked out): work within that. Record AF metadata into it and continue — do not create a second worktree.

**If already inside an AF session worktree**, continue there while the task remains part of the same working session. Update `agentFlow.state` to `active` and `agentFlow.lastTouchedAt` when picking it back up.

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
agentFlow.state = active|ready|merged
agentFlow.owner = agent
agentFlow.devlogPolicy = finish
agentFlow.startedAt = <timestamp>
agentFlow.lastTouchedAt = <timestamp>
agentFlow.branch = <explicit-branch> # only when branch-backed
agentFlow.sessionUnit = user-ended
agentFlow.endTriggers = finish,review,reconcile,merge,switch-direction
```

## Work In Session

- Re-read repo instructions from the session worktree.
- Keep edits scoped to the session goal.
- Update affected docs when behavior, setup, architecture, security, deployment, operations, onboarding, or user-facing workflows change.
- Keep working in the same session worktree across prompts until the user asks to wrap up or changes direction.
- Add or update one `devlog/` entry before the session commit.
- Run relevant validation as work accumulates.
- Use `af-finish` only when the user asks to finish, wrap up, commit, or prepare the session for merge.

## Output

Report the session worktree path, recorded parent branch, whether work was created or adopted, and that future related prompts should continue in the same worktree until finish/review/reconcile.
