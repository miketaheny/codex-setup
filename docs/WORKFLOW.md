# AF Agent-Flow Workflow

## Core Flow

```text
Read-only chat: answer directly.
File-changing chat: af-flow -> implementation -> af-devlog -> af-finish.
Release: af-reconcile -> af-full-review -> af-release.
```

Use `af-show` during finish when seeing the app, rendered docs, CLI output, or another artifact would materially improve confidence. Use `af-security-review` only when requested, config-required, or security-sensitive.

## Branch Model

- `development` is the default integration branch.
- Session worktrees start from the checked-out parent branch and merge back to that recorded parent.
- Worktrees are detached by default.
- Named branches are created only when explicitly requested.
- `main` is the production PR target and is never a local agent work branch.
- `staging` is optional and protected when enabled.
- `master`, `production`, and `prod` are reserved legacy names.

## Session Commands

```bash
scripts/start-session.sh feat export-csv
scripts/start-session.sh --branch feat/export-csv feat export-csv
scripts/finish-session.sh
scripts/finish-session.sh --merge
```

`finish-session.sh` checks readiness and reports `ASK_USER_MERGE`; use `--merge` only after explicit approval.

## Session Metadata

Keep metadata minimal:

- `agentFlow.kind`
- `agentFlow.parent`
- `agentFlow.sessionName`
- `agentFlow.state`
- `agentFlow.owner`
- `agentFlow.devlogPolicy`
- timestamps
- `agentFlow.branch` only for explicit branch-backed sessions

Use `devlog/` for decisions, validation, review, and risks.

## Skill Choices

| Situation | Skill |
|---|---|
| Start or adopt file-changing work | `af-flow` |
| Record engineering history | `af-devlog` |
| Finish, validate, review, and ask before merge | `af-finish` |
| Capture visual/manual proof | `af-show` |
| Normal pre-merge review | `af-review` |
| Worktree audit, pickup, cleanup | `af-reconcile` |
| Exhaustive release or high-risk review | `af-full-review` |
| Prepare release PRs | `af-release` |
| Security-only deep review | `af-security-review` |
| Project docs and visual assets | `af-docs` |
| Legacy Backlog history migration | `af-migrate-backlog-devlog` |

## Devlog And Docs

Every file-changing session needs one `devlog/YYYY-MM-DD-<subject>.md` entry before commit. Record validation exactly as run and call out skipped or blocked checks.

Update project docs when behavior, setup, architecture, security, deployment, operations, onboarding, or user workflows change.

## Worktree Manager

```bash
scripts/worktree-manager.py
scripts/worktree-manager.py --interactive
scripts/worktree-manager.py --details <id>
scripts/worktree-manager.py --pickup <id>
scripts/worktree-manager.py --cleanup <id> --yes
scripts/worktree-manager.py --cleanup-all --yes
```

Pickup marks incomplete work active. Cleanup removes only clean, merged, AF-managed session worktrees.

## Push And Release

Before pushing a parent branch:

```bash
scripts/check-push-readiness.sh <branch>
```

Release sequence:

```text
af-reconcile -> af-full-review -> af-release
```

Default path is `development -> staging -> main`. Use `development -> main` only when staging is disabled or explicitly requested.
