# Agent-Flow Codex Fast Path Guide

This guide is the practical operating model for using Agent-Flow with Codex while keeping work fast, scoped, and token-efficient.

Use the PDF version when sharing or printing:

```text
docs/agent-flow-codex-fast-path-guide.pdf
```

## The Short Version

Agent-Flow should feel like one persistent Codex work session, not a ceremony after every prompt.

```text
start or continue one AF worktree -> keep working there -> wrap up when you ask
```

For most work, keep the visible command set to five actions:

| Moment | Action |
|---|---|
| Start or continue file-changing work | `af-flow` |
| Check current state | `af-status` |
| Ask for a quick checkpoint | `af-review` |
| Pick up, audit, or clean worktrees | `af-reconcile` |
| Commit and prepare to merge | `af-finish` |

Specialist skills are still available, but they are not part of every session.

## Daily Flow

```mermaid
flowchart TD
    A["User asks for file-changing work"] --> B{"Already in matching AF session?"}
    B -->|Yes| C["Continue same worktree"]
    B -->|No| D["Run af-flow or start-session.sh"]
    D --> C
    C --> E["Read targeted context"]
    E --> F["Make scoped change"]
    F --> G["Run focused validation"]
    G --> H{"More related prompts?"}
    H -->|Yes| C
    H -->|No, user wraps up| I["af-finish"]
    I --> J["Commit, report readiness, ask before merge"]
```

## Token-Efficient Model Policy

Start with the cheapest setting that matches the risk.

| Work | Codex setting |
|---|---|
| Read-only help, status, command lookup | `fast` profile or base medium |
| Routine implementation | base `gpt-5.5` / medium / low verbosity |
| Risky diff, hard debugging, release review | `review` profile or high effort |
| Security-sensitive or repeatedly failing work | `deep` profile or xhigh effort |

Do not start routine sessions at `xhigh`. Escalate after evidence: repeated failure, risky scope, release gate, or security-sensitive changes.

## What To Avoid In Routine Sessions

Avoid spending tokens on:

- full repo scans when targeted file reads are enough
- full reviews before the user asks for review or release
- security reviews for non-security changes
- visual capture when no UI, rendered doc, or CLI artifact needs inspection
- feature/UI audit campaigns unless explicitly requested
- subagent fan-out without narrow stop conditions

## When To Escalate

```mermaid
flowchart LR
    A["Routine session"] --> B{"Blocked twice for same reason?"}
    B -->|Yes| H["Increase effort / narrow diagnosis"]
    B -->|No| C{"Security, auth, secrets, data access?"}
    C -->|Yes| D["Use review or deep path"]
    C -->|No| E{"Preparing release?"}
    E -->|Yes| F["af-reconcile -> af-full-review -> af-release"]
    E -->|No| G["Stay on fast path"]
```

## Worktree Mental Model

```mermaid
flowchart LR
    P["Parent branch: development"] --> S["AF session worktree"]
    S --> W["Related Codex prompts keep landing here"]
    W --> S
    S --> F["af-finish when user wraps up"]
    F --> M["Ask before merge"]
    M --> P
```

The session worktree is the durable working context. Chat can be fluid; the worktree keeps the files, Git metadata, and devlog grounded.

## Practical Prompts

Start or continue work:

```text
Use af-flow for this file-changing request. Keep related work in the same AF session worktree until I ask to finish, review, reconcile, merge, or switch direction.
```

Check status:

```text
Use af-status and tell me what AF sessions are active or ready.
```

Wrap up:

```text
Use af-finish. Validate, update the devlog, commit the session, and report the merge command.
```

Release:

```text
Use af-reconcile, then af-full-review, then af-release.
```

## The Rule Of Thumb

If the work is routine, stay light. If the work is risky, blocked, or release-facing, escalate deliberately.
