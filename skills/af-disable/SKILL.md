---
name: af-disable
description: Disable Agent-Flow enforcement for the current local repository after explicit user confirmation. Use when the user says a repo should not use Agent-Flow, wants to opt out locally, or asks to mark AF disabled for a repo.
---

# AF Disable

## Purpose

Use this skill to explicitly opt a Git repo out of Agent-Flow enforcement.

## Rules

- Ask the user to confirm that this repo should not use Agent-Flow before changing files, unless the current user message already clearly says to disable or opt out.
- Only update the current repo. Do not change global AF installs.
- Do not delete existing AF files, devlogs, docs, scripts, branches, or worktrees.
- If work is currently inside an AF session worktree, disable the recorded parent repo only when that is clearly the user's target; otherwise stop and clarify.

## Workflow

1. Confirm the Git root:

```bash
git rev-parse --show-toplevel
git status --short --branch
```

2. Inspect current AF config if present:

```bash
test -f .agent-flow/config.toml && sed -n '1,120p' .agent-flow/config.toml || true
```

3. After confirmation, run:

```bash
python3 ~/.agent-flow/scripts/set-agent-flow-mode.py --disable --yes
```

If the global helper is unavailable, use the repo-local helper:

```bash
python3 scripts/set-agent-flow-mode.py --disable --yes
```

## Result

The repo has `.agent-flow/config.toml` with:

```toml
enabled = false
mode = "disabled"
```

Future agents should disclose that Agent-Flow is disabled and should not enforce AF in that repo.
