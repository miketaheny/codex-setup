---
name: af-claude-review
description: Run Claude CLI from a terminal as an optional external review pass for a Codex Agent-Flow session or release diff. Use when the user asks for Claude review, an outside model check, or the workflow requires an external reviewer.
---

# AF Claude Review

## Purpose

Use this from Codex to run Claude CLI as an external reviewer. Agent-Flow remains Codex-first; Claude is only a terminal review tool, not an installed AF adapter.

## Rules

- Do not run this automatically during routine `af-finish`.
- Use it when the user asks for Claude review, when `af-full-review` wants an external model check, or when a high-risk diff needs an independent review pass.
- Stop cleanly if `claude` is not installed or authenticated.
- Treat Claude output as review input, not final authority. Codex must still inspect findings and decide which are valid.
- Do not paste secrets, `.env` values, credentials, private keys, production tokens, or unrelated large files into Claude.

## Workflow

1. Confirm the Git root, status, and review range:

```bash
git rev-parse --show-toplevel
git status --short --branch
git config --worktree --get agentFlow.parent || true
```

2. Check Claude CLI availability:

```bash
command -v claude
claude --help
```

3. Run the terminal review from the session worktree:

```bash
scripts/claude-review.sh
```

Or pass an explicit range:

```bash
scripts/claude-review.sh <base> <head>
```

4. Triage the output:

- Verify every P1/P2 claim against the local diff.
- Reject hallucinated file paths, stale assumptions, and findings with no code path.
- Add valid findings to the current `af-review` or `af-full-review` result.
- Record whether Claude CLI was unavailable, failed, passed, or found valid blockers.

## Output

Report:

- review range
- Claude CLI status
- findings accepted, rejected, or requiring follow-up
- validation gaps
- final AF verdict: `PASS`, `PASS WITH RISKS`, or `BLOCKED`
