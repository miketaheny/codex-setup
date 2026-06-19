---
name: af-review
description: Pre-merge review gate for Agent-Flow worktree sessions. Checks branch safety, scope, diffs, docs, tests, risk, and readiness to merge back into the recorded parent branch.
---

# AF Review Gate Skill

Use this skill before merging any agent-created session worktree back into its recorded parent branch.

For the full end-of-session workflow, including app start, Codex browser/manual review when applicable, devlog/docs checks, this review gate, and `scripts/finish-session.sh`, use `af-flow-finish`.

## Goal

Act like a disciplined reviewer for a solo developer.

## Review checklist

### 1. Branch safety

- Current branch is not `main`, `staging`, `master`, `production`, or `prod`.
- Merge target is the session worktree's recorded parent branch, usually from worktree-local `agentFlow.parent`; explicit named branches may also use `branch.<branch>.agentFlowParent`.
- Work is isolated to one AF worktree session. A named branch is optional and should exist only when explicitly requested.

### 2. Scope control

- Changes match the user request.
- No unrelated rewrites.
- No broad formatting-only churn unless requested.
- No unexpected dependency, config, auth, payment, or deployment changes.

### 3. Diff review

Inspect:

```bash
git status
git config --worktree --get agentFlow.parent || git config --get branch.$(git branch --show-current).agentFlowParent
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

- `devlog/` contains one entry file for the session commit or planned squash commit.
- Project docs are updated when behavior, setup, architecture, security, deployment, or operations changed.
- Docs do not exaggerate validation.
- Follow-ups/known risks recorded.

### 5. Validation review

Prefer existing project commands:

- tests
- lint
- typecheck
- build
- app/browser review for browser-visible or user-facing changes
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
- `auto_merge = "tiny-only"` is compatibility-only for older metadata; default behavior is to ask before merge.
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

- branch or detached session commit
- changed files summary
- validation results
- docs status
- findings
- recommended next command
