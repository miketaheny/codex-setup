---
name: af-finish-session
description: Complete an Agent-Flow worktree session after implementation. Use when the user asks to finish a session, review and merge a worktree, run final validation, start the repo for manual QA, open the Codex browser to inspect browser-visible changes, commit finish-time devlog work, or ask for merge approval.
---

# AF Finish Session Skill

## Overview

Use this skill as the end-to-end completion workflow for one AF session worktree. It orchestrates validation, docs and devlog checks, optional app/browser QA, `af-review-gate`, `scripts/finish-session.sh`, and the final ask-before-merge step.

This skill answers the session question: "Is this implemented work ready to merge into its recorded parent branch?" It does not promote `development` to protected branches; use `af-release-pr` for release pull requests.

## Workflow

### 1. Confirm session context

Run:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short
git config --worktree --get agentFlow.parent || git config --get branch.$(git branch --show-current).agentFlowParent
```

Stop if the current checkout is `main`, `staging`, `master`, `production`, or `prod`. Stop if there is no recorded parent branch for the session.

### 2. Inspect the finished work

Identify the recorded parent branch and inspect:

```bash
git diff --stat <parent-branch>...HEAD
git diff --name-only <parent-branch>...HEAD
git diff <parent-branch>...HEAD
```

Confirm the diff matches the session goal and does not include unrelated rewrites, accidental local files, secrets, broad formatting churn, or unexpected dependency/config changes.

### 3. Run validation

Use the repo's documented commands first: tests, lint, typecheck, build, or targeted manual checks. If there is no obvious command, inspect README, package manifests, Makefiles, scripts, CI config, and project docs before deciding that validation is unavailable.

Do not claim validation passed unless it ran. Record skipped validation and the reason in the devlog and final report.

### 4. Start the repo for manual review when applicable

Start the app or local site when the session changed browser-visible UI, routes, frontend behavior, generated pages, docs that should render locally, or any workflow where seeing the running repo materially improves review.

Use repo conventions to choose the command:

- Prefer documented commands in README, docs, package scripts, Makefile targets, or existing task files.
- Reuse an already-running local server when it clearly matches the current checkout.
- For static HTML, use a local file URL or a simple local server.
- Do not run production deploy commands, destructive database commands, or external release actions as "start" commands.

When Codex browser tools are available, open the local URL and inspect the changed workflow before merge. Check the relevant viewport or route, console-visible failures when practical, layout/text overlap, and the actual behavior the session changed. If browser tools are unavailable or not applicable, state that and use the best available fallback.

Stop the dev server only if it was started solely for this review and is not needed by the user.

### 5. Verify docs and devlog

Ensure one session devlog file under `devlog/` accurately records:

- goal and files changed
- decisions
- validation, including browser/manual review when applicable
- review result
- risks or follow-ups

Update project docs when behavior, setup, architecture, security, deployment, operations, onboarding, demos, or user-facing workflows changed.

### 6. Run the review gate

Use `af-review-gate` or perform its checklist directly:

- branch safety and merge target
- scope control
- full diff review
- docs/devlog review
- validation review
- P1/P2/P3 findings

Fix P1 findings before continuing. Fix P2 findings or record explicit user acceptance before merge.

### 7. Finish the session

Run:

```bash
scripts/finish-session.sh
```

If it reports `NO_CHANGE`, state that there is nothing to merge. If it reports `NOT_READY`, fix the blocker and rerun. If it commits dirty work, inspect the resulting commit and status.

When it reports `ASK_USER_MERGE`, ask the user whether to merge into the recorded parent branch. After explicit approval, run:

```bash
scripts/finish-session.sh --merge
```

Never merge automatically into `main` or `staging`.

## Required Output

Report:

- session worktree path and recorded parent branch
- changed files summary
- validation commands and results
- app start command, URL, and Codex browser/manual review result when applicable
- docs and devlog status
- review findings
- `scripts/finish-session.sh` result
- merge status or the exact approval needed from the user
