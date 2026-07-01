---
name: af-review
description: Optional, on-demand review checklist for an Agent-Flow worktree session. Checks branch safety, scope, diffs, docs, devlog, validation, risk. Use only when the user explicitly asks for a quick review mid-session — it is not run automatically by af-finish and is not required before merging into the parent branch.
---

# AF Review

Use this only when the user explicitly asks for a review before `af-full-review` would otherwise run. It is not part of the mandatory lifecycle: `af-finish` does not invoke it, so session finishes stay fast. The mandatory review gate before code merges toward `main` is `af-full-review`, run once as part of the release flow.

Reach for this when the user wants a faster gut-check on a session worktree without waiting for the full release review.

## Checklist

### 1. Branch Safety

- Current checkout is not `main`, `staging`, `master`, `production`, or `prod`.
- Merge target is the recorded parent from worktree-local `agentFlow.parent` or explicit branch metadata.
- Work is isolated to one AF session worktree.

### 2. Scope Control

- Changes match the user request.
- No unrelated rewrites or broad formatting churn.
- No unexpected dependency, config, auth, payment, deployment, or generated-file changes.

### 3. Diff Review

Inspect:

```bash
git status
git config --worktree --get agentFlow.parent || git config --get branch.$(git branch --show-current).agentFlowParent
git diff --stat <parent-branch>...HEAD
git diff <parent-branch>...HEAD
```

Look for logic bugs, missing edge cases, security/privacy issues, broken imports/types, missing error handling, accidental secrets, and untracked files that should or should not be committed.

### 4. Docs And Devlog

- `devlog/` contains one entry for the session commit or planned squash commit.
- Project docs are updated when behavior, setup, architecture, security, deployment, operations, onboarding, or user workflows changed.
- Docs and devlog do not exaggerate validation.
- Follow-ups and known risks are recorded.

### 5. Validation

Prefer existing project commands: tests, lint, typecheck, build, targeted manual tests, and app/browser review for user-facing changes. If validation cannot run, explain why and lower confidence.

### 6. Findings

Use:

- P1: must fix before merge
- P2: should fix or explicitly accept before merge
- P3: minor improvement

## Output

End with `READY TO MERGE INTO <parent-branch>`, `READY BUT ASK USER BEFORE MERGE`, or `NOT READY TO MERGE`.

Include the session branch or detached commit, changed files, validation results, docs/devlog status, findings, and recommended next command.
