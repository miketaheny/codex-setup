---
name: af-compound-mode
description: Decide when to use light Agent-Flow skills versus a heavier planning, execution, review, or multi-agent workflow.
---

# AF Compound Mode Skill

Use this skill when deciding whether a task should use a fast Agent-Flow workflow or a heavier planning/review workflow.

## Goal

Get the benefit of deeper planning and review without making every small fix slow or token-heavy.

## Decision table

| Task | Recommended workflow |
|---|---|
| Tiny typo/config/CSS fix | `af-small-change` |
| Small known bug | `af-small-change` or a focused work pass |
| Small bug with side effects | brief plan -> work -> `af-review-gate` |
| Normal feature | plan -> work -> code review |
| Risky/broad feature | use a task worktree from the checked-out parent -> heavier planning/review workflow when needed |
| Multi-agent exploration | heavier multi-agent workflow |
| Reusable lesson | project docs or solution note |
| Legacy Backlog/task migration | `af-migrate-backlog-devlog` |
| Visual docs, guides, demos, decks, or marketing | `af-docs` |
| Worktree or branch cleanup | `af-reconcile-worktrees` |
| Before merge | `af-review-gate` |
| Before protected-branch PR | `af-security-review` |
| Before release promotion | `af-reconcile-worktrees -> af-docs -> af-push-staging` with `af-security-review` |

## When a Heavier Workflow Is Worth It

Use the agent's heavier workflow when the task needs most of these:

- broader repo context
- implementation plan
- multiple files
- tests/build/review
- docs updates
- PR-style readiness
- CI follow-up
- compounding reusable knowledge

Avoid heavier workflows when:

- the task is a typo
- the fix is obvious and tiny
- speed matters more than exhaustive review
- the user is still exploring requirements

## Parallel Sessions

Allowed only when each session has its own worktree and narrow scope.

Rules:

- One worktree per task.
- For large/risky prompts, use the checked-out parent branch unless the user explicitly requests a feature branch or different parent.
- Avoid editing shared files across sessions.
- Add per-commit devlog files under `devlog/`; do not rewrite unrelated devlog files.
- Merge each task worktree back to its recorded parent branch one at a time.
- Run `af-review-gate` after conflict resolution.
- Run `scripts/check-push-readiness.sh <branch>` before pushing a parent branch.

## Required output when invoked

State:

- chosen workflow
- why it is the lightest safe option
- worktree recommendation and branch only if explicitly requested
- documentation requirements
- validation expectations

Then proceed if enough information is available.
