---
name: af-finish
description: Finish an Agent-Flow worktree session after implementation. Use when the user asks to finish, validate, review, commit, capture app/browser proof, check devlog/docs, report readiness, or merge a session worktree back to its recorded parent branch.
---

# AF Finish

## Purpose

Use this as the explicit end-of-session workflow for one AF worktree. It coordinates validation, `af-show` when visual or manual proof is relevant, mandatory `af-devlog`, `scripts/finish-session.sh`, and ask-before-merge. Review happens at merge time via `af-full-review` in the release pipeline, not here.

Do not invoke this automatically after every completed prompt. Invoke it when the user asks to finish, wrap up, commit, prepare for merge, review for merge, or switch away from the active session.

## Workflow

### 1. Confirm Session

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short
git config --worktree --get agentFlow.parent || git config --get branch.$(git branch --show-current).agentFlowParent
```

Stop if the current checkout is protected/reserved or has no recorded parent branch.

### 2. Inspect Diff

```bash
git diff --stat <parent-branch>...HEAD
git diff --name-only <parent-branch>...HEAD
git diff <parent-branch>...HEAD
```

Confirm the diff matches the session goal and contains no unrelated rewrites, secrets, accidental generated files, or unexpected dependency/config changes.

### 3. Validate

Use the repo's documented tests, lint, type checks, builds, or focused manual checks. If no command is obvious, inspect README, package manifests, Makefiles, scripts, CI config, and docs before deciding validation is unavailable.

Do not claim validation passed unless it ran. Record skipped validation and why.

### 4. Show When Relevant

Invoke `af-show` when the change affects browser-visible UI, generated pages, user-facing docs, app workflows, CLI output that should be inspected, or another artifact where visual/manual proof materially improves confidence.

Record the command, URL/path, and proof status in the devlog and final output. If visual proof is not applicable, say so briefly.

### 5. Verify Devlog And Docs

Ensure one session devlog entry under `devlog/` records:

- goal and changed files
- decisions
- validation and visual/manual proof status
- risks or follow-ups

Update project docs when the session changes behavior, setup, architecture, security, deployment, operations, onboarding, or user-facing workflows.

### 6. Finish Script

Run:

```bash
scripts/finish-session.sh
```

If it reports `NO_CHANGE`, there is nothing to merge. If it reports `NOT_READY`, fix the blocker and rerun. If it reports `ASK_USER_MERGE`, ask before merging. After explicit approval:

```bash
scripts/finish-session.sh --merge
```

Never merge automatically into `main` or `staging`.

This flow is intentionally fast: no full-diff review gate runs here. If the user explicitly wants a quick mid-session sanity check, run `af-review` on demand — it is optional, not a required step. The mandatory review gate runs once, at release time, via `af-full-review`.

## Output

Report session path, parent branch, changed files, validation, visual/manual proof status, docs/devlog status, finish-script result, and merge status or the exact approval needed.
