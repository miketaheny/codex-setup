# Agent-Flow User Guide

## Install

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

Installed surfaces:

- `~/.agent-flow`
- `~/.codex`
- `~/.claude`

Custom locations:

```bash
AF_HOME=/path/to/agent-flow CODEX_HOME=/path/to/codex CLAUDE_HOME=/path/to/claude ./scripts/install.sh
```

## Initialize A Project

Inside a target Git repo:

```bash
~/.agent-flow/scripts/init-repo.sh
```

The init script creates missing AF instruction files, `devlog/`, docs folders, `.agent-flow/config.toml`, and a non-destructive `.gitignore` block. It asks about enforcement, optional staging, and the pre-push hook.

For repos with a root `package.json`, init also offers pnpm onboarding. It skips non-Node repos and repos already using pnpm. Use `--no-pnpm` to skip conversion or `--pnpm` to run only that onboarding step on an already initialized repo.

## Daily Work

Ask the agent:

```text
Use af-flow for this file-changing request, keep the work in one AF session, then use af-finish when done.
```

Direct commands:

```bash
scripts/start-session.sh fix navbar-spacing
scripts/finish-session.sh
scripts/finish-session.sh --merge
```

If the finish command reports `ASK_USER_MERGE`, approve before running `--merge`.

For command help:

```text
Use af-help and show me the Agent-Flow commands.
```

By default, new session worktrees are grouped next to the repo in a clearly named directory:

```text
../<repo>.worktrees/<session-slug>
```

Example: starting `docs isms-structure` from `core12-isms` creates `../core12-isms.worktrees/isms-structure`, not another sibling that looks like a separate repo. Use `AF_WORKTREE_ROOT=/path/to/worktrees` before `scripts/start-session.sh` to choose a different root.

## Choose A Skill

| Need | Skill |
|---|---|
| Command help and usage guide | `af-help` |
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
| Codex Security-aware security review | `af-security-review` |
| Docs, diagrams, demos, guides | `af-docs` |
| Whole-app feature/user-story QA campaign | `af-feature-audit` |
| Responsive UI/UX audit and fix campaign | `af-ui-audit` |
| Backlog history migration | `af-migrate-backlog-devlog` |

## Feature Audit

Use `af-feature-audit` only when you explicitly want an app-wide product/QA campaign:

```text
Use af-feature-audit on this app. Create one canonical feature register, test every user story, fix UX/logistical errors, and retest.
```

Default canonical register:

```text
docs/product/feature-register.csv
```

The register is spreadsheet-compatible and tracks source paths, user stories, expected behavior, acceptance criteria, test results, fix sessions, retest results, and status.

## UI Audit And Brand Guidelines

Use `af-brand-guidelines` first when a repo lacks brand/design rules:

```text
Use af-brand-guidelines to create or ingest this repo's brand guideline for UI work.
```

Default guideline path:

```text
docs/BRAND-GUIDELINES.md
```

Use `af-ui-audit` when you explicitly want a full responsive UI/UX campaign:

```text
Use af-ui-audit on this app. Audit responsive behavior, visual consistency, accessibility, brand conformance, UX issues, fixes, and retests.
```

Default canonical register:

```text
docs/product/ui-audit-register.csv
```

See [Agent-Flow Usage Guide](AGENT-FLOW-USAGE.md) for the full command map.

## Manage Worktrees

For a read-only dashboard:

```text
Use af-status to summarize current Agent-Flow status and all worktree states.
```

```bash
scripts/worktree-manager.py --interactive
scripts/worktree-manager.py --details <id>
scripts/worktree-manager.py --pickup <id>
scripts/worktree-manager.py --cleanup <id> --yes
```

Before pushing:

```bash
scripts/check-push-readiness.sh <branch>
```

## Release

Use:

```text
af-reconcile -> af-full-review -> af-release
```

Run `af-security-review` when requested, config-required, or security-sensitive. If the Codex Security plugin is available, AF prefers its diff-scan workflow for Git-backed release diffs and reports the plugin result or fallback reason.

Default release path is `development -> staging -> main`. With staging disabled, use `development -> main`.

## IDE And Ignore Policy

Commit `.vscode/extensions.json`, `.vscode/tasks.json`, `.vscode/launch.json`, or `.vscode/settings.json` only when they encode shared project tooling. Keep personal IDE preferences, local paths, env files, logs, and OS noise untracked.
