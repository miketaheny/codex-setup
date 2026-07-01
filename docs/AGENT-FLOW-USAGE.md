# Agent-Flow Usage Guide

This guide is the quick reference for using Agent-Flow from a repo that has been initialized with AF.

## Core Rules

- Read-only questions can be answered directly.
- File-changing work uses one AF session worktree.
- Every file-changing session gets a `devlog/` entry before commit.
- `af-finish` validates, reviews, commits when configured, and asks before merge.
- Parent branches should pass push-readiness checks before pushing.
- Release work uses `af-reconcile -> af-full-review -> af-release`.

## Install

From the Agent-Flow setup repo:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

Default install targets:

```text
~/.agent-flow
~/.codex
~/.claude
```

## Initialize A Repo

Inside a target Git repo:

```bash
~/.agent-flow/scripts/init-repo.sh
```

The init script creates repo instruction files, `.agent-flow/config.toml`, `devlog/`, docs scaffolding, helper scripts, and optional pre-push hooks.

For repos with a root `package.json`, init also offers pnpm onboarding. It skips non-Node repos and repos already using pnpm. Use `--no-pnpm` to skip conversion or `--pnpm` to run the pnpm step on an already initialized repo.

## Daily File-Changing Work

Ask the agent:

```text
Use af-flow for this file-changing request, keep it in one AF session, add the devlog entry, then use af-finish when done.
```

Direct script flow:

```bash
scripts/start-session.sh feat short-name
scripts/finish-session.sh
```

If finish reports `ASK_USER_MERGE`, merge only after explicit approval:

```bash
scripts/finish-session.sh --merge
```

Create a named branch only when explicitly wanted:

```bash
scripts/start-session.sh --branch feat/short-name feat short-name
```

## Command Cheat Sheet

| Job | Command |
|---|---|
| Initialize repo | `~/.agent-flow/scripts/init-repo.sh` |
| Initialize without pnpm conversion | `~/.agent-flow/scripts/init-repo.sh --no-pnpm` |
| Start session | `scripts/start-session.sh feat short-name` |
| Start branch-backed session | `scripts/start-session.sh --branch feat/short-name feat short-name` |
| Finish session | `scripts/finish-session.sh` |
| Merge finished session after approval | `scripts/finish-session.sh --merge` |
| List worktrees | `scripts/worktree-manager.py` |
| Inspect worktree | `scripts/worktree-manager.py --details <id>` |
| Pick up worktree | `scripts/worktree-manager.py --pickup <id>` |
| Clean up merged worktree | `scripts/worktree-manager.py --cleanup <id> --yes` |
| Check push readiness | `scripts/check-push-readiness.sh development` |

## Skill Cheat Sheet

| Need | Skill |
|---|---|
| Command help and this usage guide | `af-help` |
| Create or ingest brand/design guidelines | `af-brand-guidelines` |
| Convert Node repos to pnpm | `af-pnpm` |
| Start or adopt work | `af-flow` |
| Overall AF status and worktree state | `af-status` |
| Finish a session | `af-finish` |
| Visual/manual proof | `af-show` |
| Engineering history | `af-devlog` |
| Normal review | `af-review` |
| Worktree cleanup or pickup | `af-reconcile` |
| Release readiness review | `af-full-review` |
| Release PRs | `af-release` |
| Security-only review | `af-security-review` |
| Docs, diagrams, demos, guides | `af-docs` |
| Whole-app feature/user-story QA campaign | `af-feature-audit` |
| Responsive UI/UX audit and fix campaign | `af-ui-audit` |
| Backlog history migration | `af-migrate-backlog-devlog` |

## Feature Audit

Use `af-feature-audit` only when explicitly starting an app-wide feature and QA campaign.

Default canonical register:

```text
docs/product/feature-register.csv
```

The audit loop is:

```text
discover features -> write user stories -> record expected behavior -> test every story -> fix UX/logistical errors -> retest
```

Fixes discovered during an audit still use normal AF sessions:

```text
af-flow -> implementation -> af-devlog -> af-finish
```

## UI Audit And Brand Guidelines

Use `af-brand-guidelines` to create, ingest, or update the repo brand/design source of truth.

Default guideline:

```text
docs/BRAND-GUIDELINES.md
```

Use `af-ui-audit` only when explicitly starting a responsive UI/UX review and fix campaign.

Default UI audit register:

```text
docs/product/ui-audit-register.csv
```

The audit loop is:

```text
establish brand/design baseline -> inspect routes and viewports -> record issues -> fix responsive/UI/UX problems -> retest
```

## Release

Use:

```text
af-reconcile -> af-full-review -> af-release
```

Run `af-security-review` when requested, config-required, or when the release touches auth, secrets, validation, dependencies, infrastructure, privacy, or data access.

## Safe Defaults

- Do not work directly on `main`.
- Treat `staging` as protected when enabled.
- Use detached session worktrees unless a named branch is explicitly requested.
- Keep metadata small and record human decisions in `devlog/`.
- Do not run destructive production actions as proof or QA.
- Do not leave untracked or uncommitted session work behind at finish.
