# Agent-Flow Instructions — AF Solo Developer Workflow

These instructions apply to AI coding agent sessions unless a repository-level instruction file gives more specific guidance. `af` means Agent-Flow.

## Purpose

Make agent-assisted solo development safe and consistent across Claude, Codex, and other coding agents by enforcing:

- isolated work per task
- no direct work on protected branches
- merge-back to `development` only
- per-commit devlog files under `devlog/`
- maintained project documentation
- review before merge
- heavier multi-step workflows only when the task deserves them

## Non-Negotiable Branch Rules

- Never modify `main`, `master`, `staging`, `production`, `prod`, or release branches directly.
- Do not commit to protected branches.
- Do not push to remote protected branches unless explicitly instructed.
- Default base branch is `development`.
- If `development` does not exist, stop and explain the current branches before changing anything.
- Use a feature branch or separate git worktree for every implementation task.
- Prefer branch names like:
  - `fix/<short-description>`
  - `feat/<short-description>`
  - `docs/<short-description>`
  - `chore/<short-description>`

## Worktree Rules

When the user runs multiple agent sessions or mentions parallel work:

- Use one git worktree per task.
- Keep each task narrowly scoped.
- Avoid editing the same shared files across parallel sessions when possible.
- Add one devlog file under `devlog/` for each meaningful commit or planned squash commit.
- Do not rewrite unrelated devlog files from other branches or worktrees.
- Before merge, rebase or merge latest `development`, resolve conflicts, then run review.

## Task Intake

Before implementation, the agent should identify:

- the goal
- affected area of the repo
- expected branch/worktree
- validation command(s)
- documentation and devlog impact
- whether a heavier planning/review workflow is needed

Ask a clarifying question only when proceeding would likely cause wrong or destructive work. Otherwise make a reasonable best effort and document assumptions in the task's `devlog/` entry.

## Default Command Decision Model

Use the lightest workflow that still protects quality.

- Tiny obvious change: use `af-small-change` or simple focused work.
- Small fix with side effects: plan briefly, implement, then review.
- Normal feature: plan, implement, review, document.
- Risky/broad feature: use the agent's heavier planning/review workflow.
- Reusable lesson discovered: record it in project docs or a solution note.

## Required Documentation

For every meaningful change, add or update a Markdown file in `devlog/`.

Use one devlog file per commit. If the branch will be squashed, use one devlog file for the planned squash commit. Suggested filename:

```text
devlog/YYYY-MM-DD-<commit-subject-slug>.md
```

Each devlog file should include:

- date
- branch/worktree
- commit subject, and commit SHA when already known
- goal
- files changed
- decisions made
- validation run
- review result
- follow-ups or known risks

Update project docs when the change affects:

- UI or user-facing behavior
- public API behavior
- configuration
- deployment
- database/schema behavior
- security/privacy/compliance behavior
- operational workflows

Run project docs maintenance before pushing or promoting `development` to protected branches such as `staging`, `main`, release, or production branches.

## Review Gate

Before merging back to `development`:

- Confirm current branch is not protected.
- Inspect `git status` and `git diff`.
- Run available tests, linting, type checks, and builds where practical.
- Run or simulate code review.
- Fix P1/blocking findings.
- Record unresolved P2/P3 findings in the task's `devlog/` file.
- Summarize final status.

## Commit Style

Use small, meaningful commits.

Preferred prefixes:

- `feat:`
- `fix:`
- `docs:`
- `refactor:`
- `test:`
- `chore:`

Do not rely on commit messages as the only project history. `devlog/` is the detailed engineering record.

## Safety and Scope

- Do not delete files unless explicitly required by the task.
- Do not reformat the whole repo unless explicitly requested.
- Do not change dependencies unless needed and documented.
- Do not alter environment files, secrets, production config, DNS, auth, payments, or deployment settings without explicit approval.
- Keep changes tightly scoped to the user's request.
- Flag suspicious, risky, or destructive operations before running them.

## Done Definition

A task is done when:

- changes are implemented in a feature branch/worktree when Git is already initialized
- validation has been run or documented as unavailable
- a per-commit devlog file exists under `devlog/`
- affected project docs are updated
- review has been performed for merge-ready work
- the final response includes what changed, validation, docs updated, and merge status
