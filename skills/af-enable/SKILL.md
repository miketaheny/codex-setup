---
name: af-enable
description: Enable or re-enable Agent-Flow enforcement for the current local repository. Use when the user wants a repo to use Agent-Flow, reverse an af-disable opt-out, or initialize missing AF setup.
---

# AF Enable

## Purpose

Use this skill to enable Agent-Flow in a Git repo or reverse a prior local opt-out.

## Rules

- Ask for confirmation before changing files unless the user clearly asked to enable Agent-Flow.
- If `.agent-flow/config.toml` does not exist, run the normal init flow so branch setup, staging, hooks, and pnpm onboarding are handled.
- If `.agent-flow/config.toml` exists and only needs re-enabling, update `enabled = true` and `mode = "enforced"`.
- Do not delete devlogs, docs, scripts, worktrees, or local repo history.

## Workflow

1. Confirm the Git root and current status:

```bash
git rev-parse --show-toplevel
git status --short --branch
```

2. If there is no AF config, run:

```bash
~/.agent-flow/scripts/init-repo.sh
```

Use init flags only when the user already specified choices, for example:

```bash
~/.agent-flow/scripts/init-repo.sh --enforced --integration-branch development --production-branch main
```

3. If AF config already exists, inspect it:

```bash
sed -n '1,160p' .agent-flow/config.toml
```

Then, after confirmation, run:

```bash
python3 ~/.agent-flow/scripts/set-agent-flow-mode.py --enable --yes
```

If the global helper is unavailable, use the repo-local helper:

```bash
python3 scripts/set-agent-flow-mode.py --enable --yes
```

## Result

The repo has `.agent-flow/config.toml` with:

```toml
enabled = true
mode = "enforced"
```

Future file-changing work should use the normal AF flow.
