---
name: af-release
description: Prepare Agent-Flow release pull requests after af-reconcile and af-full-review. Use when the user asks to release, promote development, create development-to-staging or staging-to-main PRs, verify push readiness, or decide whether the release path is development to staging to main or development to main.
---

# AF Release

## Required Order

Run release work in this order:

```text
af-reconcile -> af-full-review -> af-release
```

Run `af-security-review` only when the user asks, config requires it, `af-full-review` flags security-sensitive changes, or the release touches auth, secrets, input validation, dependencies, infrastructure, privacy, or data access. When Codex Security is available, that security gate should prefer `$codex-security:security-diff-scan` for the release diff and report the plugin result or fallback reason.

## Release Path

Default path:

```text
development -> staging -> main
```

Use `development -> main` only when `.agent-flow/config.toml` sets `staging_enabled = false` or the user explicitly requests the no-staging path.

Read `.agent-flow/config.toml` when present:

- `integration_branch` defaults to `development`
- `staging_branch` defaults to `staging`
- `production_branch` defaults to `main`
- missing `staging_enabled` means staging is enabled for release planning

## Safety Rules

- Never push directly to `main`.
- Never force-push a release branch.
- Do not push `development` or create a PR while child session worktrees are dirty or unmerged unless the user explicitly excludes them and push readiness allows it.
- Ask before remote side effects such as `git push` or `gh pr create` unless the current user request clearly authorizes them.
- Do not remove worktrees, delete branches, or resolve conflicts destructively without explicit approval.

## Workflow

### 1. Confirm Context

```bash
git rev-parse --show-toplevel
git fetch origin --prune
git branch --show-current
git status --short
```

Use a clean integration worktree. If dirty, stop and finish/review that work through AF first.

### 2. Verify Reconcile And Full Review

Confirm `af-reconcile` has identified open worktrees and push readiness, then confirm `af-full-review` passed or has only explicitly accepted risks.

Use:

```bash
scripts/worktree-manager.py
scripts/check-push-readiness.sh development
```

### 3. Prepare Integration Branch

```bash
git switch development
git pull --ff-only origin development
git status --short
```

Run practical release validation: tests, lint, typecheck, build, and targeted manual review as relevant. Run docs maintenance with `af-docs` when release-relevant docs are stale.

After approval to push:

```bash
git push origin development
git fetch origin --prune
git rev-parse development
git rev-parse origin/development
```

Local and remote SHAs should match before PR creation.

### 4. Offer Or Create Release PR

For `development -> staging`:

```bash
git log --oneline origin/staging..origin/development
git diff --stat origin/staging...origin/development
git diff --name-only origin/staging...origin/development
gh pr create --base staging --head development
```

For `staging -> main`, first verify staging contains the intended development release:

```bash
git merge-base --is-ancestor origin/development origin/staging
git log --oneline origin/main..origin/staging
git diff --stat origin/main...origin/staging
git diff --name-only origin/main...origin/staging
gh pr create --base main --head staging
```

For no-staging:

```bash
git log --oneline origin/main..origin/development
git diff --stat origin/main...origin/development
git diff --name-only origin/main...origin/development
gh pr create --base main --head development
```

Create PRs only after approval. If GitHub tooling is unavailable, provide the exact branch pair and blocker.

## Output

Report release path, reconcile result, full-review result, security-review status when applicable, Codex Security plugin status when used or skipped, validation, push-readiness, push/SHA verification, PRs offered or created, and remaining blockers or accepted risks.
