# Agent-Flow Codex Fast Path Guide

This guide is the practical operating model for using Agent-Flow with Codex while keeping the workflow fast and the reasoning effort right-sized.

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

## Effort Preflight

Pick effort before acting. The default for real development and computer-use work is extra-high reasoning; downgrade only when the task is obviously cheap and easy to verify.

| Work | Codex setting |
|---|---|
| Read-only help, status, command lookup | `fast` profile or base medium |
| Trivial one-file edit or narrow docs copy | base `gpt-5.5` / medium |
| Normal development, debugging, refactoring | base `gpt-5.5` / xhigh / low verbosity |
| Browser or computer-use workflow | base `gpt-5.5` / xhigh |
| Review, release, security-sensitive work | `deep` profile or xhigh effort |

If uncertain, choose `xhigh` for development and computer-use work. Save tokens by keeping context targeted, not by under-reasoning important work.

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
    A["New task"] --> B{"Read-only or trivial?"}
    B -->|Yes| C["fast or medium"]
    B -->|No| D{"Development or computer use?"}
    D -->|Yes| E["xhigh"]
    D -->|No| F{"Release/security/review?"}
    F -->|Yes| G["deep / xhigh"]
    F -->|No| H["medium or high"]
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

Keep the workflow light. Use extra-high reasoning for real development and computer-use work unless the preflight clearly says the task is cheap.
