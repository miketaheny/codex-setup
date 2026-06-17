---
name: af-push-staging
description: Promote `development` to `staging` safely in the AF solo-developer workflow. Use when the user asks to push staging, promote development to staging or UAT, reconcile worktrees before a staging push, push development and staging, or prepare a staging-to-main pull request after staging is updated.
---

# AF Push Staging Skill

## Overview

Use this skill to move completed work from `development` to `staging` while preserving local work, respecting protected branch rules, and keeping the user in control of destructive or release-adjacent actions.

## Safety Rules

- Never push directly to `main`, `master`, `production`, `prod`, or release branches.
- Never force-push.
- Never delete branches or remove worktrees without explicit approval for each path or branch.
- Never resolve merge conflicts destructively without the user's approval.
- Do not switch away from a dirty worktree unless the changes are understood and preserved.
- Offer a `staging` to `main` pull request only after `development` and `staging` push successfully.

## Workflow

### 1. Confirm repository context

Run:

```bash
git rev-parse --show-toplevel
git fetch origin --prune
git branch --show-current
git status --short
```

If the current branch is not `development`, switch to `development` only when the current worktree is clean. If it is dirty, stop and ask how to handle the local changes.

### 2. Prepare `development`

Inspect the actual diff before committing:

```bash
git status --short
git diff --stat
git diff
```

If there are intended changes on `development`, stage and commit them with a concise message based on the diff. If the user supplied a commit message, use it. If there are no changes, state that `development` has nothing new to commit.

When the repo has an `af-docs` workflow and project docs should be updated before protected-branch promotion, run it before pushing staging.

### 3. Reconcile worktrees before staging

Use `af-reconcile-worktrees` when available. Otherwise, audit manually:

```bash
git worktree list --porcelain
git branch --list
```

For each worktree, inspect status and ancestry:

```bash
git -C <worktree-path> status --short
git merge-base --is-ancestor <branch-or-head> development
```

Ask before merging an unmerged branch, removing a worktree, or deleting a branch. Dirty worktrees are not eligible for removal or automatic merge.

### 4. Validate before staging

Run practical project validation before touching `staging`:

- targeted tests
- lint
- typecheck
- build
- manual review when no automated command exists

Document any skipped validation honestly.

### 5. Merge `development` into `staging`

Run:

```bash
git switch staging
git pull --ff-only origin staging
git merge development
```

If `staging` does not exist, stop and report the branch state. If conflicts occur, stop, list conflicted files, and ask before resolving.

### 6. Push release branches

After the merge succeeds and `git status --short` is clean:

```bash
git push origin development
git push origin staging
```

If either push is rejected, stop and report the exact rejection. Do not force-push.

### 7. Offer the main PR

After both pushes succeed, ask whether to create a pull request from `staging` to `main`. Do not create it until the user explicitly agrees.

Use the available GitHub tooling or:

```bash
gh pr create --base main --head staging
```

## Final Response

Report:

- commits created on `development`
- worktrees or branches merged, removed, skipped, or awaiting approval
- validation run and results
- whether `development` and `staging` pushed successfully
- whether a `staging` to `main` PR was offered or created
- remaining user decisions
