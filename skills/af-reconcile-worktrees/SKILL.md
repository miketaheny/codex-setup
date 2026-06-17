---
name: af-reconcile-worktrees
description: Audit and reconcile AF solo-developer git worktrees, branches, parent-branch metadata, and instruction conflicts. Use when the user asks to review worktrees, clean up completed worktrees, inspect development/staging/main branch state, find branch cleanup candidates, or compare agent instruction guidance against AF workflow rules.
---

# AF Reconcile Worktrees Skill

## Overview

Use this skill to audit first and mutate second. It identifies completed, dirty, unmerged, user-controlled, or protected work before release promotion, cleanup, or branch deletion.

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

- current branch and configured integration branch status
- worktree cleanliness and merge ancestry against each task's recorded parent branch
- local protected branch policy for `main`, optional `staging`, and reserved legacy names
- push readiness by parent branch
- local branch cleanup candidates
- heuristic agent-instruction and skill-rule conflicts

Use the script as a baseline, then apply judgment before taking action.

### 3. Classify worktrees

Use these classifications:

- Complete task worktree: clean status, has recorded `agentFlowParent`, and HEAD is already an ancestor of that parent branch.
- Ongoing: dirty status, detached/unknown state, missing parent metadata, or has commits not merged to the parent branch.
- Keep: worktree is the configured integration branch, or `staging` when `staging_enabled = true`.
- Disallowed local protected worktree: `main`, `staging` when staging is disabled or unconfigured, or reserved `master`, `production`, or `prod`.

Remove complete or disallowed clean worktrees only when the user requested cleanup in this turn or explicitly approves the specific path. Use:

```bash
git worktree remove <path>
```

Never force-remove without explicit instruction.

### 4. Classify branches

Keep the configured integration branch, `staging` only when `staging_enabled = true`, and any user-controlled branch without AF parent metadata.

Flag local `main` for deletion after confirming it has no unique work. `main` is the production PR target, not a normal local branch.

Flag local `staging` for deletion when `staging_enabled = false` or no staging choice is configured. Keep local `staging` only when `staging_enabled = true` and the repo uses the explicit release promotion flow.

Flag reserved local branches `master`, `production`, and `prod` for deletion after confirming they have no unique work.

For task branches with recorded AF parent metadata and already merged to that parent, ask before deleting:

```bash
git branch -d <branch>
```

Do not delete dirty, checked-out, unmerged, or remote-only branches. Do not use `git branch -D` unless explicitly requested.

### 5. Review instruction conflicts

Read applicable instruction sources:

- global `AGENT-FLOW.md` and adapter files
- repo-local agent instruction files
- `af-push-staging` or `push-staging` skill when present

Flag conflicts around branch ownership, missing parent metadata, worktree removal, destructive actions, release promotion, or PR-only main changes.

### 6. Check push readiness

Before pushing any user-controlled branch, run:

```bash
scripts/check-push-readiness.sh <branch>
```

The branch is not ready to push if any child task branch with `agentFlowParent = <branch>` has a dirty worktree or commits not merged into the parent.

### 7. Re-check after approved actions

After any approved merge, branch deletion, or worktree removal:

```bash
python3 <this-skill-dir>/scripts/audit_repo.py /path/to/repo
git status --short
git worktree list --porcelain
```

Confirm removed worktrees no longer appear and report any remaining dirty state.

## Output

Always return:

- current branch and integration branch cleanliness/ahead-behind state
- worktrees kept, removed, skipped, and why
- branches kept, deletion candidates awaiting approval, local protected branch policy findings, and user-controlled branches skipped
- parent branches blocked or ready for push
- agent instruction conflicts or "none found"
- actions taken and remaining user decisions
