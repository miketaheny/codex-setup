---
name: af-push-staging
description: Promote `development` safely through the configured release path. Use when the user asks to push staging, promote development to staging or main, reconcile worktrees before release promotion, or prepare a staging-to-main or development-to-main pull request.
---

# AF Push Staging Skill

## Overview

Use this skill to move completed work from `development` through the repo's configured release path while preserving local work, respecting protected branch rules, and keeping the user in control of destructive or release-adjacent actions.

## Safety Rules

- Never push directly to `main`; `main` is production.
- Never push directly to `staging` except as part of the explicit promotion workflow when staging is enabled.
- Never use `master`, `production`, or `prod` as mainline branches.
- Never force-push.
- Never delete branches or remove worktrees without explicit approval for each path or branch.
- Never resolve merge conflicts destructively without the user's approval.
- Do not switch away from a dirty worktree unless the changes are understood and preserved.
- Offer a `staging` to `main` pull request only after `development` and `staging` push successfully.
- When staging is disabled, offer a `development` to `main` pull request after `development` pushes successfully.

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

Read `.agent-flow/config.toml` if present. Treat `staging_enabled = false` as a `development -> main` release path. Treat `staging_enabled = true` as `development -> staging -> main`.

### 2. Prepare `development`

Inspect the actual diff before committing:

```bash
git status --short
git diff --stat
git diff
```

If there are intended changes on `development`, stage and commit them with a concise message based on the diff. If the user supplied a commit message, use it. If there are no changes, state that `development` has nothing new to commit.

When the repo has an `af-docs` workflow and project docs should be updated before protected-branch promotion, run it before pushing staging.

### 3. Reconcile worktrees before release promotion

Use `af-reconcile-worktrees` when available. Otherwise, audit manually:

```bash
git worktree list --porcelain
git branch --list
```

For each worktree, inspect status and ancestry:

```bash
git -C <worktree-path> status --short
git config --get branch.<branch-name>.agentFlowParent
git merge-base --is-ancestor <branch-or-head> <recorded-parent-or-development>
```

Ask before merging an unmerged branch, removing a worktree, or deleting a branch. Dirty worktrees are not eligible for removal or automatic merge.

### 4. Validate before release promotion

Run practical project validation before touching `staging` or preparing a `main` pull request:

- targeted tests
- lint
- typecheck
- build
- manual review when no automated command exists

Document any skipped validation honestly.

Before pushing `development`, run the push-readiness check when available:

```bash
scripts/check-push-readiness.sh development
```

Do not push while any child task worktree from `development` is dirty or unmerged.

### 5. Merge `development` into `staging` when enabled

Run:

```bash
git switch staging
git pull --ff-only origin staging
git merge development
```

If `staging_enabled = false`, skip this step and do not create or use `staging`.

If `staging_enabled = true` and `staging` does not exist, stop and report the branch state. If conflicts occur, stop, list conflicted files, and ask before resolving.

### 6. Push release branches

After the merge succeeds and `git status --short` is clean:

```bash
git push origin development
AF_ALLOW_RELEASE_PUSH=1 git push origin staging
```

When staging is disabled, push only `development`. If any push is rejected, stop and report the exact rejection. Do not force-push.

### 7. Offer the main PR

After required pushes succeed, ask whether to create the pull request to `main`. Do not create it until the user explicitly agrees.

Use the available GitHub tooling or:

```bash
gh pr create --base main --head staging
gh pr create --base main --head development
```

Use `staging` as the head only when staging is enabled. Use `development` as the head when staging is disabled.

## Final Response

Report:

- commits created on `development`
- worktrees or branches merged, removed, skipped, or awaiting approval
- validation run and results
- whether `development` and optional `staging` pushed successfully
- whether a `staging` to `main` or `development` to `main` PR was offered or created
- remaining user decisions
