---
name: af-review-gate
description: Pre-merge review gate for solo-dev Agent-Flow task branches. Checks branch safety, scope, diffs, docs, tests, risk, and readiness to merge back into the recorded parent branch.
---

# AF Review Gate Skill

Use this skill before merging any agent-created task branch back into its recorded parent branch.

## Goal

Act like a disciplined reviewer for a solo developer.

## Review checklist

### 1. Branch safety

- Current branch is not `main`, `staging`, `master`, `production`, or `prod`.
- Merge target is the task branch's recorded parent branch, usually from `branch.<branch>.agentFlowParent`.
- Work is isolated to a feature branch or worktree.

### 2. Scope control

- Changes match the user request.
- No unrelated rewrites.
- No broad formatting-only churn unless requested.
- No unexpected dependency, config, auth, payment, or deployment changes.

### 3. Diff review

Inspect:

```bash
git status
git config --get branch.$(git branch --show-current).agentFlowParent
git diff --stat <parent-branch>...HEAD
git diff <parent-branch>...HEAD
```

Look for:

- logic bugs
- missing edge cases
- security/privacy issues
- broken imports/types
- missing error handling
- accidental secrets
- untracked files that should/should not be committed

### 4. Docs review

- `devlog/` contains one entry file for each meaningful commit or planned squash commit.
- Project docs are updated when behavior, setup, architecture, security, deployment, or operations changed.
- Docs do not exaggerate validation.
- Follow-ups/known risks recorded.

### 5. Validation review

Prefer existing project commands:

- tests
- lint
- typecheck
- build
- targeted manual test

If validation cannot run, explain why and lower confidence.

### 6. Findings format

Use severity:

- P1: must fix before merge
- P2: should fix or explicitly accept before merge
- P3: minor improvement

### 7. Merge policy

Read `.agent-flow/config.toml` when present.

- If `merge_prompt = "always"`, report ready state and ask the user before merge.
- If `auto_merge = "tiny-only"`, auto-merge is eligible only for branches with `agentFlowTaskClass = tiny` and no findings.
- Never approve automatic merge into `main` or `staging`.
- Run `scripts/check-push-readiness.sh <parent-branch>` before pushing a parent branch.

## Required output

End with one of:

```text
READY TO MERGE INTO <parent-branch>
```

or

```text
READY BUT ASK USER BEFORE MERGE
```

or

```text
NOT READY TO MERGE
```

Include:

- branch
- changed files summary
- validation results
- docs status
- findings
- recommended next command
