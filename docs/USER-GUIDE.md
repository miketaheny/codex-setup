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

## Choose A Skill

| Need | Skill |
|---|---|
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
| Backlog history migration | `af-migrate-backlog-devlog` |

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

Run `af-security-review` when requested, config-required, or security-sensitive.

Default release path is `development -> staging -> main`. With staging disabled, use `development -> main`.

## IDE And Ignore Policy

Commit `.vscode/extensions.json`, `.vscode/tasks.json`, `.vscode/launch.json`, or `.vscode/settings.json` only when they encode shared project tooling. Keep personal IDE preferences, local paths, env files, logs, and OS noise untracked.
