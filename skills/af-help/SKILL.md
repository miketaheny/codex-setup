---
name: af-help
description: Show Agent-Flow commands, skill choices, lifecycle prompts, and usage-guide links. Use when the user asks for AF help, command help, how to use Agent-Flow, what skill to use, or a Markdown usage guide. Read-only unless the user explicitly asks to create or update files.
---

# AF Help

## Purpose

Use this skill to give the user a concise Agent-Flow command map and point them to the Markdown usage guide.

Default to read-only output. Do not start sessions, write files, commit, merge, push, clean up worktrees, or run release commands unless the user explicitly asks for that action.

## Usage Guide

When available, point users to:

```text
docs/AGENT-FLOW-USAGE.md
~/.agent-flow/docs/AGENT-FLOW-USAGE.md
~/.agent-flow/docs/AGENT-FLOW-USAGE.md
```

If the user asks to create a repo-local guide, use `af-flow` first and write or update `docs/AGENT-FLOW-USAGE.md`.

## Read-Only Checks

If answering inside a repo, inspect only lightweight context:

```bash
pwd
git rev-parse --show-toplevel 2>/dev/null || true
git branch --show-current 2>/dev/null || true
test -f .agent-flow/config.toml && sed -n '1,220p' .agent-flow/config.toml
test -f AGENT-FLOW.md && sed -n '1,220p' AGENT-FLOW.md
```

Skip commands that mutate state.

## Command Map

Show the relevant subset of these commands:

```bash
# install AF globally from the setup repo
./scripts/install.sh

# initialize a target repo
~/.agent-flow/scripts/init-repo.sh

# start a file-changing session
scripts/start-session.sh feat short-name

# start an explicit branch-backed session
scripts/start-session.sh --branch feat/short-name feat short-name

# finish, validate, review, and report merge readiness
scripts/finish-session.sh

# merge only after explicit approval
scripts/finish-session.sh --merge

# inspect worktrees
scripts/worktree-manager.py
scripts/worktree-manager.py --details <id>

# pick up or clean up a managed session
scripts/worktree-manager.py --pickup <id>
scripts/worktree-manager.py --cleanup <id> --yes

# check parent branch push readiness
scripts/check-push-readiness.sh development
```

## Skill Map

Use this table when the user asks what to run:

| Need | Skill |
|---|---|
| Command help and usage guide | `af-help` |
| Create or ingest brand/design guidelines | `af-brand-guidelines` |
| Start or adopt file-changing work | `af-flow` |
| Overall AF status and worktree state | `af-status` |
| Finish, validate, review, and ask before merge | `af-finish` |
| Engineering history | `af-devlog` |
| Visual/manual proof | `af-show` |
| Normal pre-merge review | `af-review` |
| Worktree cleanup or pickup | `af-reconcile` |
| Release readiness review | `af-full-review` |
| Release PRs | `af-release` |
| Security-only review | `af-security-review` |
| Docs, diagrams, demos, guides | `af-docs` |
| Whole-app feature/user-story QA campaign | `af-feature-audit` |
| Responsive UI/UX audit and fix campaign | `af-ui-audit` |
| Backlog history migration | `af-migrate-backlog-devlog` |

## Prompt Examples

```text
Use af-help and show me the Agent-Flow commands.
```

```text
Use af-flow for this file-changing request, then af-finish when done.
```

```text
Use af-feature-audit on this app and keep one canonical feature register.
```

```text
Use af-brand-guidelines to create or ingest this repo brand guideline before UI work.
```

```text
Use af-ui-audit on this app and keep one canonical UI audit register.
```

```text
Use af-status to summarize current worktrees without changing anything.
```

```text
Use af-reconcile, then af-full-review, then af-release.
```

## Output

Keep the answer short and practical:

- current repo/branch when relevant
- the command or skill the user should use next
- copyable commands
- link or path to `docs/AGENT-FLOW-USAGE.md`
- any important safety boundary such as "merge requires explicit approval"
