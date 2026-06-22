---
name: af-status
description: Read-only Agent-Flow status reporting. Use when the user asks for overall AF status, current Agent-Flow state, all worktree/session states, dirty or unmerged worktree summaries, push-readiness blockers, or a concise dashboard without pickup, cleanup, merge, push, commit, or other mutations.
---

# AF Status Skill

## Goal

Produce a read-only Agent-Flow status snapshot for a repo. Summarize the AF config, current checkout, parent branch state, all current worktrees, incomplete work, cleanup candidates, push-readiness blockers, and practical next actions.

Use `af-reconcile` instead when the user wants to pick up, finish, clean up, remove, or otherwise mutate worktrees.

## Rules

- Stay read-only. Do not run `--pickup`, `--cleanup`, `--cleanup-all`, `finish-session.sh`, merge, branch deletion, commit, push, or destructive commands.
- If the user requests local-only status, do not fetch. Otherwise run `git fetch origin --prune` when an `origin` remote exists; if it fails, continue with local data and report the fetch failure.
- Prefer repo-local scripts when present. Fall back to the bundled `skills/af-reconcile/scripts/audit_repo.py` only if the wrapper is missing.
- Capture command output yourself and summarize it. Do not paste raw JSON unless the user asks for machine-readable output.
- Clearly separate current facts from recommended next actions.

## Workflow

### 1. Confirm Repo Context

Run:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short --branch
test -f .agent-flow/config.toml && sed -n '1,220p' .agent-flow/config.toml || true
```

If the current checkout is a session worktree, also run:

```bash
git config --worktree --get-regexp '^agentFlow\.' || true
```

### 2. Refresh Remote State When Allowed

When not local-only and `origin` exists:

```bash
git remote get-url origin >/dev/null 2>&1 && git fetch origin --prune
```

Continue if this fails. The status report should note that remote ahead/behind information may be stale.

### 3. Gather AF Worktree State

Prefer the manager:

```bash
scripts/worktree-manager.py --json
scripts/worktree-manager.py
```

If `scripts/worktree-manager.py` is missing but the skill scripts exist:

```bash
python3 skills/af-reconcile/scripts/audit_repo.py . --json
python3 skills/af-reconcile/scripts/audit_repo.py .
```

Use the JSON for counts and classifications, and the visual output for the compact tree.

### 4. Check Push Readiness

For each parent branch shown in the manager JSON, run the readiness helper when present:

```bash
scripts/check-push-readiness.sh <parent-branch>
```

If the helper exits nonzero, record it as a blocker and include the dirty or unmerged child worktrees it names. If the helper is unavailable, use the `parent_readiness` section from the manager JSON.

## Status Classifications

Use the manager classifications directly:

- `parent`: the integration or parent checkout.
- `dirty`: uncommitted or untracked files exist.
- `unmerged`: commits are not merged into the recorded parent.
- `complete`: clean and merged into the parent.
- `unmanaged`: missing Agent-Flow parent metadata.
- `unknown`: status could not be determined.

Treat `dirty`, `unmerged`, `unmanaged`, and `unknown` as attention-needed. Treat `complete` as a cleanup candidate only if the manager marks it cleanup-eligible, and ask before any cleanup.

## Output

Return a concise dashboard:

- repo path, AF mode, current branch or detached session, and current checkout cleanliness
- parent or integration branch, upstream behind/ahead state, and local protected branch notes
- worktree list with id, name, status, activity, parent, dirty count, head, and path
- push-readiness by parent branch
- blockers and attention-needed sessions
- cleanup candidates, if any, with no cleanup performed
- recommended next actions and the exact safe command the user can approve or run next

If there are no child worktrees, say so explicitly.
