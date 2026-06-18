---
name: af-worktree-task
description: Create, adopt, and finish one Agent-Flow worktree session for a file-changing Codex chat. Use when the user asks Codex to change files, continue unfinished work, switch worktrees, or ensure work happens in an isolated AF worktree.
---

# AF Worktree Session Skill

This skill keeps the legacy `af-worktree-task` name for compatibility, but the workflow unit is a worktree session.

## Goal

Make one file-changing chat equal one AF-owned worktree. Do not edit parent branches directly. If the chat changes direction, finish, pause, or abandon the current worktree, then start a new chat/worktree.

## Preconditions

Before changing files:

1. Confirm this is a Git repo.
2. Run `git branch --show-current` and `git status --short`.
3. If the current checkout is dirty before session start, report it and do not hide it in a new worktree.
4. If already inside an AF worktree with `agentFlow.parent`, continue only if the request matches that worktree's direction.
5. If the request changes direction, stop and ask to finish, pause, or abandon the current worktree before opening a new chat/worktree.
6. If on a parent branch such as `development`, create or adopt a session worktree before editing.

## Create Or Adopt

Prefer the lifecycle helper:

```bash
scripts/start-session.sh <type> <session-name>
```

Create a named branch only when the user explicitly asks:

```bash
scripts/start-session.sh --branch <type>/<session-name> <type> <session-name>
```

Use the manager to inspect or pick up existing work:

```bash
scripts/worktree-manager.py --interactive
scripts/worktree-manager.py --pickup <id>
```

The created worktree must have worktree-local metadata such as:

```text
agentFlow.kind = session
agentFlow.parent = development
agentFlow.sessionName = <session-name>
agentFlow.state = started
agentFlow.owner = codex
agentFlow.devlogPolicy = finish
```

## In The Session

1. Re-read repo agent instruction files from the worktree.
2. Implement only the session's coherent direction.
3. Update `agentFlow.lastTouchedAt` when adopting or finishing.
4. Add or update one devlog file under `devlog/` before the session commit.
5. Update affected project docs when behavior, setup, architecture, security, deployment, or operations change.
6. Run validation.
7. Run review gate.
8. Finish with:

```bash
scripts/finish-session.sh
```

If it reports `ASK_USER_MERGE`, ask whether to merge. After explicit approval:

```bash
scripts/finish-session.sh --merge
```

## Switching Worktrees

Prefer a new Codex chat when switching worktrees. Codex cannot truly clear all previous chat assumptions inside the same conversation. If same-chat switching is unavoidable, first run:

```bash
scripts/worktree-manager.py --details <id>
```

Then state the new worktree path, parent branch, status, and goal before making changes.

## Summary

Report:

- worktree path
- parent branch
- session status
- changed files
- devlog file
- validation
- docs updated
- review result
- merge command or cleanup action if ready
