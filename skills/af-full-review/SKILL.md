---
name: af-full-review
description: Run an exhaustive Agent-Flow review for release readiness, high-risk work, or broad changes. Use before af-release, after af-reconcile, or when correctness, tests, docs, devlog, worktree state, security-sensitive areas, regressions, and unresolved risks need a deeper gate than normal af-review.
---

# AF Full Review

## Purpose

Use this for broad release readiness and high-risk changes. It is the single mandatory review gate before code merges toward `main` — `af-finish` is intentionally fast and does not review, so this is where review work happens. It is deeper than the optional, on-demand `af-review` checklist and broader than `af-security-review`.

## Workflow

### 1. Establish Scope

Confirm the base/head or parent/session being reviewed:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short
git diff --name-only <base>...<head>
git diff --stat <base>...<head>
```

Use `af-reconcile` first for release readiness so dirty, unmerged, or unmanaged worktrees are known before review.

### 2. Review Correctness

Inspect the full diff for logic errors, broken contracts, missing edge cases, data-loss risks, dependency/config mistakes, accidental generated files, and broad formatting churn.

### 3. Review Validation

Check that relevant tests, lint, type checks, builds, migrations, smoke tests, and manual/visual proof ran. When validation is missing, decide whether that is acceptable for the risk level and record the gap.

### 4. Review Docs And Devlog

Confirm session devlogs exist for included work and do not exaggerate validation. Confirm user-facing, setup, architecture, deployment, operations, and security docs changed when impacted.

### 5. Review Worktree And Release State

Confirm:

- parent/integration worktree is clean
- no child session worktrees are dirty or unmerged unless explicitly excluded
- push-readiness checks pass for the release parent
- branch targets match the configured release path

### 6. Review Security-Relevant Areas

Flag security-sensitive changes such as auth, authorization, secrets, input validation, dependency upgrades, infrastructure, logging, privacy, and data access. If the release touches these areas or config requires it, run `af-security-review` as a distinct security-only gate. That skill will use the agent's built-in security review tool for the scan.

### 7. Findings

Use:

- P1: must fix before release or merge
- P2: should fix or explicitly accept
- P3: minor improvement

End with `FULL REVIEW PASS`, `FULL REVIEW PASS WITH ACCEPTED RISKS`, or `FULL REVIEW BLOCKED`.
