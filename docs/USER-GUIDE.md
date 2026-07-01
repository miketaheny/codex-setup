# Agent-Flow User Guide

## Install

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

Installed surfaces:

- `~/.agent-flow`
- `~/.codex`

Custom locations:

```bash
AF_HOME=/path/to/agent-flow CODEX_HOME=/path/to/codex ./scripts/install.sh
```

Agent-Flow also installs Codex profile templates when missing:

```bash
codex --profile fast
codex --profile review
codex --profile deep
```

Use base `gpt-5.5` / `xhigh` for most development and computer-use work. Use `fast` or medium for cheap read-only/status tasks and trivial edits. Use `deep` for release review, security-sensitive work, or hard debugging.

The default habit is to run an effort preflight first: keep the AF workflow lightweight, but do not under-reason real development work.

## Initialize A Project

Inside a target Git repo:

```bash
~/.agent-flow/scripts/init-repo.sh
```

The init script creates missing AF instruction files, `devlog/`, docs folders, `.agent-flow/config.toml`, and a non-destructive `.gitignore` block. It asks about enforcement, optional staging, and the pre-push hook.

If a repo has no AF setup, agents should stop before file edits and ask to initialize AF or explicitly opt out for that repo. Init asks:

- whether AF enforcement should be enabled at all
- which branch receives completed session merges, default `development`
- which branch is the production/final PR target, default `main`
- whether the repo uses protected `staging`
- whether to install the pre-push worktree readiness hook
- whether to run pnpm onboarding for root Node repos

For repos with a root `package.json`, init also offers pnpm onboarding. It skips non-Node repos and repos already using pnpm. Use `--no-pnpm` to skip conversion or `--pnpm` to run only that onboarding step on an already initialized repo.

## Daily Work

Ask the agent:

```text
Use af-flow for this file-changing request. Keep related work in this AF session worktree until I ask to finish, review, reconcile, merge, or switch direction.
```

Direct commands:

```bash
scripts/start-session.sh fix navbar-spacing
scripts/finish-session.sh
scripts/finish-session.sh --merge
```

If the finish command reports `ASK_USER_MERGE`, approve before running `--merge`.

Do not finish after every prompt. A normal Codex flow/vibe session should remain in the same worktree while the work is related. Use `af-finish` only when you want to wrap up the session; use `af-review` or `af-reconcile` when you want a checkpoint without starting a new worktree.

For most days, keep the mental model to five actions:

| Moment | Action |
|---|---|
| Start or continue changing files | `af-flow` |
| Check where things stand | `af-status` |
| Get a quick sanity check | `af-review` |
| Clean up or pick up worktrees | `af-reconcile` |
| Commit and prepare to merge | `af-finish` |

Use specialist skills only when the task needs them: `af-pnpm` for pnpm conversion, `af-docs` for docs and visuals, `af-feature-audit` for an explicit feature QA campaign, and `af-ui-audit` for an explicit responsive UI/UX campaign.

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
| Disable AF enforcement for this repo | `af-disable` |
| Enable or re-enable AF for this repo | `af-enable` |
| Start or adopt work | `af-flow` |
| Overall AF status and worktree state | `af-status` |
| Finish a session | `af-finish` |
| Visual/manual proof | `af-show` |
| Engineering history | `af-devlog` |
| Normal review | `af-review` |
| Optional Claude CLI external review | `af-claude-review` |
| Worktree cleanup or pickup | `af-reconcile` |
| Release readiness review | `af-full-review` |
| Release PRs | `af-release` |
| Codex Security-aware security review | `af-security-review` |
| Docs, diagrams, demos, guides | `af-docs` |
| Whole-app feature/user-story QA campaign | `af-feature-audit` |
| Responsive UI/UX audit and fix campaign | `af-ui-audit` |
| Backlog history migration | `af-migrate-backlog-devlog` |

Use `af-claude-review` only when you want Codex to run Claude CLI as an external second-model review. It requires the `claude` command to already be installed and authenticated.

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

For a printable Codex-focused guide with flow charts, see [Agent-Flow Codex Fast Path Guide](AGENT-FLOW-CODEX-GUIDE.md) or `docs/agent-flow-codex-fast-path-guide.pdf`.

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
