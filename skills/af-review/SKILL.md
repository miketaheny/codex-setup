---
name: af-review
description: Normal pre-merge review gate for Agent-Flow worktree sessions. Checks branch safety, scope, diffs, docs, devlog, validation, risk, and readiness to merge back into the recorded parent branch.
---

# AF Review

Use this before merging an AF session worktree into its recorded parent branch. For the full finish workflow, including visual/manual proof, devlog/docs checks, this review, commit readiness, and ask-before-merge, use `af-finish`.

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
