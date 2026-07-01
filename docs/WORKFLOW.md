# AF Agent-Flow Workflow

## Core Flow

```text
Read-only chat: answer directly.
File-changing session: af-flow -> persistent implementation -> af-devlog -> af-finish.
Release: af-reconcile -> af-full-review -> af-release.
Manual feature audit: af-feature-audit.
Manual UI audit: af-brand-guidelines -> af-ui-audit.
```

Use `af-show` during finish when seeing the app, rendered docs, CLI output, or another artifact would materially improve confidence. Use `af-security-review` only when requested, config-required, or security-sensitive. When the Codex Security plugin is available, AF prefers `$codex-security:security-diff-scan` for Git-backed release diffs and records the plugin result or fallback reason.

Use `af-help` for command help and usage-guide routing. `af-feature-audit` and `af-ui-audit` are manual-only and should not run as part of ordinary finish or release gates.

## Fast Path

Most Codex sessions should use the light path:

```text
one persistent worktree -> targeted context -> scoped change -> focused validation -> one devlog -> finish on request
```

The daily command surface is intentionally small:

```text
af-flow, af-status, af-review, af-reconcile, af-finish
```

Escalate to specialist skills, full review, security review, release checks, visual capture, or broad audits only when requested, risk-triggered, or needed after repeated failure.

## Codex Model And Effort

Default Codex posture is `gpt-5.5` with medium effort and low verbosity. Use `fast` for read-only help/status, `review` for `af-full-review`, and `deep` only for security-sensitive or repeatedly failing work. See `docs/CODEX-MODEL-POLICY.md`.

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

Do not run `finish-session.sh` after every prompt. A session is open-ended by default and remains active while related work continues. End it only when the user asks to finish, review, reconcile, merge, or switch direction.

New session worktrees are created under a sibling worktree root so they are visually distinct from normal repositories:

```text
../<repo>.worktrees/<session-slug>
```

For example, `scripts/start-session.sh docs isms-structure` in `core12-isms` creates `../core12-isms.worktrees/isms-structure`. Set `AF_WORKTREE_ROOT=/path/to/worktrees` when a repo needs a custom location.

## Session Metadata

Keep metadata minimal:

- `agentFlow.kind`
- `agentFlow.parent`
- `agentFlow.sessionName`
- `agentFlow.state`
- `agentFlow.owner`
- `agentFlow.devlogPolicy`
- `agentFlow.sessionUnit = user-ended`
- `agentFlow.endTriggers`
- timestamps
- `agentFlow.branch` only for explicit branch-backed sessions

Use `devlog/` for decisions, validation, review, and risks.

## Skill Choices

| Situation | Skill |
|---|---|
| Command help and usage guide | `af-help` |
| Create or ingest brand/design guidelines | `af-brand-guidelines` |
| Convert Node repos to pnpm | `af-pnpm` |
| Start or adopt file-changing work | `af-flow` |
| Overall AF status and worktree state | `af-status` |
| Record engineering history | `af-devlog` |
| Finish, validate, review, and ask before merge | `af-finish` |
| Capture visual/manual proof | `af-show` |
| Normal pre-merge review | `af-review` |
| Worktree audit, pickup, cleanup | `af-reconcile` |
| Exhaustive release or high-risk review | `af-full-review` |
| Prepare release PRs | `af-release` |
| Codex Security-aware security review | `af-security-review` |
| Project docs and visual assets | `af-docs` |
| Whole-app feature/user-story QA campaign | `af-feature-audit` |
| Responsive UI/UX audit and fix campaign | `af-ui-audit` |
| Legacy Backlog history migration | `af-migrate-backlog-devlog` |

## Feature Audit Campaigns

Run `af-feature-audit` only when explicitly requested. It creates or updates one canonical spreadsheet-compatible register, normally:

```text
docs/product/feature-register.csv
```

The campaign flow is:

```text
discover features -> draft user stories and expected behavior -> test every story -> fix UX/logistical errors in scoped AF sessions -> retest
```

Feature-audit fixes still use normal file-changing session rules, including devlog, validation, review, and ask-before-merge.

## UI Audit Campaigns

Run `af-brand-guidelines` when the repo lacks a usable brand/design source of truth. It creates or updates:

```text
docs/BRAND-GUIDELINES.md
```

Run `af-ui-audit` only when explicitly requested. It creates or updates one canonical spreadsheet-compatible register, normally:

```text
docs/product/ui-audit-register.csv
```

The campaign flow is:

```text
establish brand/design baseline -> inspect routes and viewports -> record UI/UX issues -> fix scoped batches -> retest
```

UI-audit fixes still use normal file-changing session rules, including devlog, validation, visual/manual proof, review, and ask-before-merge.

## Devlog And Docs

Every file-changing session needs one `devlog/YYYY-MM-DD-<subject>.md` entry before commit. Record validation exactly as run and call out skipped or blocked checks.

Update project docs when behavior, setup, architecture, security, deployment, operations, onboarding, or user workflows change.

## Worktree Manager

Use `af-status` for a read-only summary of AF config, current checkout, all worktrees, and push-readiness blockers.

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
