---
name: af-release
description: Prepare and create Agent-Flow release pull requests. Use when the user asks to push staging, promote development, create a development-to-staging PR, create a staging-to-main PR, promote staging to main, reconcile worktrees before release, verify development push readiness, or decide whether the default release path should be development to staging to main or development to main.
---

# AF Release PR Skill

## Overview

Use this skill to move completed work through protected branches by pull request. The default release path is:

```text
development -> staging -> main
```

Use `development -> main` only when `.agent-flow/config.toml` explicitly sets `staging_enabled = false` or the user explicitly requests the no-staging path.

This skill is intentionally PR-first. Do not merge `development` into `staging` locally or push `staging` directly as the normal workflow.

## Safety Rules

- Never push directly to `main`.
- Never force-push any release branch.
- Never create a pull request to `staging` or `main` until the formal `af-security-review` gate has passed for that exact base/head pair.
- Never bypass dirty, incomplete, or unmerged worktrees silently. Ask the user about open worktrees before release PR creation.
- Never remove worktrees, delete branches, or resolve merge conflicts destructively without explicit approval for the specific path or branch.
- Ask before remote side effects such as `git push` or `gh pr create` unless the user's current request already clearly authorizes that action.
- If a direct protected staging push is required by a repo-specific exception, stop and ask for explicit approval; this skill defaults to protected-branch PRs.

## Release Path Decision

Read `.agent-flow/config.toml` when present:

- `integration_branch` defaults to `development`.
- `staging_branch` defaults to `staging`.
- `production_branch` defaults to `main`.
- Missing or unspecified `staging_enabled` means staging is enabled for this skill.
- `staging_enabled = false` means use `development -> main`.

If the user asks generally to "release", "push staging", or "promote development", start with the `development -> staging` PR. Create or offer the `staging -> main` PR only after `staging` contains the intended release, usually after the `development -> staging` PR is merged.

If the user asks specifically for `staging -> main`, verify that `origin/staging` already contains the intended `origin/development` release before opening the PR.

## Workflow

### 1. Confirm repository context

Run:

```bash
git rev-parse --show-toplevel
git fetch origin --prune
git branch --show-current
git status --short
```

Use a clean worktree for the integration branch. If the current worktree is dirty, stop and ask how to handle the local changes before switching branches or pushing.

### 2. Ask about open worktrees

Use `af-reconcile` when available. Otherwise audit manually:

```bash
git worktree list --porcelain
git branch --list
scripts/check-push-readiness.sh development
```

Summarize open AF session worktrees, dirty worktrees, unmerged session commits, branch-backed sessions, and protected-branch policy concerns.

Before continuing, ask the user what to do with open worktrees that could affect the release:

- finish and merge them before release
- exclude them from this release
- pause the release
- clean up completed worktrees

Do not continue past incomplete child worktrees of `development` unless the user explicitly says to exclude them or the readiness check proves they are already merged and clean.

### 3. Prepare `development`

Switch to the integration branch only from a clean worktree:

```bash
git switch development
git pull --ff-only origin development
git status --short
```

Inspect any local changes before committing. If `development` has intended local changes, run the normal session finish/review workflow first instead of committing them as part of release PR prep.

Run docs maintenance when changed work affects user-facing behavior, setup, architecture, security, deployment, operations, onboarding, demos, or release communication:

```text
af-docs
```

Run practical release validation:

- tests
- lint
- typecheck
- build
- targeted manual review

Then verify push readiness:

```bash
scripts/check-push-readiness.sh development
```

If readiness passes and the user authorized the push, push and verify the remote ref:

```bash
git push origin development
git fetch origin --prune
git rev-parse development
git rev-parse origin/development
```

The local and remote `development` SHAs should match before opening a release PR from `development`.

### 4. Create or offer the `development -> staging` PR

Use this path by default when staging is enabled or unspecified.

Confirm `staging` exists locally or remotely:

```bash
git show-ref --verify --quiet refs/remotes/origin/staging || git show-ref --verify --quiet refs/heads/staging
```

Review the release diff:

```bash
git log --oneline origin/staging..origin/development
git diff --name-only origin/staging...origin/development
git diff --stat origin/staging...origin/development
git diff origin/staging...origin/development
```

Run `af-security-review` for:

```text
base = staging
head = development
```

Do not create the PR while SEC-P1 findings remain open. Do not create it with SEC-P2 findings unless the user explicitly accepts the risk.

Create the PR only after approval:

```bash
gh pr create --base staging --head development
```

If GitHub tooling is unavailable, provide the exact branch pair and blocker instead of pretending the PR was created.

### 5. Create or offer the `staging -> main` PR

Use this path after the `development -> staging` PR is merged, or when the user explicitly asks for staging to main and `staging` already contains the intended release.

Verify remote branch state:

```bash
git fetch origin --prune
git merge-base --is-ancestor origin/development origin/staging
git log --oneline origin/main..origin/staging
git diff --name-only origin/main...origin/staging
git diff --stat origin/main...origin/staging
git diff origin/main...origin/staging
```

If `origin/development` is not an ancestor of `origin/staging`, stop and report that staging does not yet contain the current development release.

Run `af-security-review` for:

```text
base = main
head = staging
```

Do not create the PR while SEC-P1 findings remain open. Do not create it with SEC-P2 findings unless the user explicitly accepts the risk.

Create the PR only after approval:

```bash
gh pr create --base main --head staging
```

### 6. No-staging path

Use this only when `.agent-flow/config.toml` explicitly sets `staging_enabled = false` or the user explicitly requests it.

After `development` is clean, validated, push-ready, pushed, and remote-verified, review:

```bash
git log --oneline origin/main..origin/development
git diff --name-only origin/main...origin/development
git diff --stat origin/main...origin/development
git diff origin/main...origin/development
```

Run `af-security-review` for:

```text
base = main
head = development
```

Then create the PR only after approval:

```bash
gh pr create --base main --head development
```

## Final Response

Report:

- chosen release path and why
- open worktrees found and the user's decision for each relevant item
- docs maintenance and validation results
- push-readiness result
- `git push origin development` result and remote SHA verification
- formal security review base/head and result
- PRs offered or created, with URLs when available
- remaining blockers, accepted risks, or next release step
