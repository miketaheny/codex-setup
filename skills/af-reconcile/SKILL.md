---
name: af-reconcile
description: Audit, visualize, pick up, finish, and clean up Agent-Flow worktree sessions. Use when the user asks to review worktrees, find dirty or unmerged work, continue incomplete agent work, clean up merged worktrees or branches, inspect development/staging/main state, or check push readiness.
---

# AF Reconcile

## Overview

Audit first and mutate second. Worktrees may contain active agent sessions, dirty changes, unmerged commits, or completed cleanup candidates. Never remove dirty or unmerged work.

## Workflow

### 1. Confirm Context

Run:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short
```

Run `git fetch origin --prune` unless the user explicitly requested local-only review.

### 2. Open The Manager

Prefer the functional manager when present:

```bash
scripts/worktree-manager.py --interactive
```

If the repo wrapper is unavailable, use the bundled script:

```bash
python3 <this-skill-dir>/scripts/worktree_manager.py /path/to/repo --interactive
```

The manager provides:

- an ASCII worktree map
- numbered picker entries
- details view with metadata, status, dirty files, and diff stats
- pickup/adopt action for incomplete work
- individual cleanup for complete clean worktrees
- cleanup-all for all complete clean worktrees

For read-only output:

```bash
scripts/worktree-manager.py
scripts/worktree-manager.py --details <id>
python3 <this-skill-dir>/scripts/audit_repo.py /path/to/repo
```

### 3. Classify Work

Use these classifications:

- Parent: the integration branch checkout, usually `development`.
- Dirty: has uncommitted or untracked files.
- Unmerged: has commits not merged to the recorded parent branch.
- Complete: clean, has recorded AF parent metadata, and HEAD is already merged to parent.
- Unmanaged: missing AF parent metadata.
- Protected/disallowed: local `main`, disabled/unconfigured `staging`, or reserved `master`, `production`, or `prod`.

### 4. Pick Up Incomplete Work

Use pickup for dirty, unmerged, unknown, or stale work:

```bash
scripts/worktree-manager.py --pickup <id>
```

Pickup updates AF metadata such as `agentFlow.state`, `agentFlow.owner`, and `agentFlow.lastTouchedAt`, then prints the worktree path and recommended new-chat handoff.

Prefer starting a new agent session in the picked-up worktree. If staying in the same session, restate the worktree path, parent branch, status, and goal before editing.

### 5. Clean Up Completed Work

Clean only worktrees that the manager marks cleanup-eligible:

```bash
scripts/worktree-manager.py --cleanup <id> --yes
scripts/worktree-manager.py --cleanup-all --yes
```

Cleanup may remove the worktree and delete a merged explicit session branch. It must not remove dirty, unmerged, unmanaged, protected, or parent worktrees.

### 6. Recheck

After merge, pickup, cleanup, or branch deletion:

```bash
scripts/worktree-manager.py
scripts/check-push-readiness.sh <parent-branch>
git status --short
```

## Output

Return:

- current branch and integration branch cleanliness/ahead-behind state
- visual worktree summary
- worktrees picked up, removed, skipped, and why
- branches deleted or kept
- parent branches blocked or ready for push
- remaining user decisions
