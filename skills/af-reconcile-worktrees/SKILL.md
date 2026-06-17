---
name: af-reconcile-worktrees
description: Audit and reconcile AF solo-developer git worktrees, branches, and instruction conflicts. Use when the user asks to review worktrees, clean up completed worktrees, inspect development/staging/main branch state, find branch cleanup candidates, or compare agent instruction guidance against AF workflow rules.
---

# AF Reconcile Worktrees Skill

## Overview

Use this skill to audit first and mutate second. It identifies completed, dirty, unmerged, or protected work before staging promotion, cleanup, or branch deletion.

## Workflow

### 1. Confirm repository context

Run:

```bash
git rev-parse --show-toplevel
git fetch origin --prune
git branch --show-current
git status --short
```

Skip `git fetch` only when the user explicitly requested an offline/local-only review.

### 2. Run the bundled audit

Prefer the bundled read-only audit script:

```bash
python3 <this-skill-dir>/scripts/audit_repo.py /path/to/repo
```

The script reports:

- current branch and `development` status
- worktree cleanliness and merge ancestry
- local branch cleanup candidates
- heuristic agent-instruction and skill-rule conflicts

Use the script as a baseline, then apply judgment before taking action.

### 3. Classify worktrees

Use these classifications:

- Complete: clean status and HEAD is already an ancestor of local `development`.
- Ongoing: dirty status, detached/unknown state, or has commits not merged to `development`.
- Protected: worktree is `development`, `staging`, or `main`.

Remove complete worktrees only when the user requested cleanup in this turn or explicitly approves the specific path. Use:

```bash
git worktree remove <path>
```

Never force-remove without explicit instruction.

### 4. Classify branches

Keep `development` and `staging`.

If local `main` exists, ask whether to remove it after switching active work to `development` or `staging`; changes to `main` should happen through pull requests only.

For any other local branch already merged to `development`, ask before deleting:

```bash
git branch -d <branch>
```

Do not delete dirty, checked-out, unmerged, or remote-only branches. Do not use `git branch -D` unless explicitly requested.

### 5. Review instruction conflicts

Read applicable instruction sources:

- global `AGENT-FLOW.md` and adapter files
- repo-local agent instruction files
- `af-push-staging` or `push-staging` skill when present

Flag conflicts around branch ownership, local `main`, worktree removal, destructive actions, staging promotion, or PR-only main changes.

### 6. Re-check after approved actions

After any approved merge, branch deletion, or worktree removal:

```bash
python3 <this-skill-dir>/scripts/audit_repo.py /path/to/repo
git status --short
git worktree list --porcelain
```

Confirm removed worktrees no longer appear and report any remaining dirty state.

## Output

Always return:

- current branch and `development` cleanliness/ahead-behind state
- worktrees kept, removed, skipped, and why
- branches kept, deletion candidates awaiting approval, and local `main` prompt
- agent instruction conflicts or "none found"
- actions taken and remaining user decisions
