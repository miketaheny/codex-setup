# Agent-Flow Instructions — AF Solo Developer Workflow

These instructions apply to AI coding agent sessions unless a repository-level instruction file gives more specific guidance. `af` means Agent-Flow.

## Purpose

Make agent-assisted solo development safe and consistent across Claude, Codex, and other coding agents by enforcing:

- isolated work per task
- no direct work on protected or reserved branches
- named task branches only when the user explicitly requests a branch
- merge-back to the user-controlled parent branch that was checked out for the task
- per-commit devlog files under `devlog/`
- maintained project documentation and useful visual assets
- review before merge
- formal security review before protected-branch pull requests
- first-contact repo initialization or explicit local opt-out
- push readiness checks before remote pushes
- heavier multi-step workflows only when the task deserves them

## First-Contact Repo Rules

When an agent first opens a repository:

- Read repo-local `AGENT-FLOW.md`, `AGENTS.md`, `CLAUDE.md`, and `.agent-flow/config.toml` when present.
- If repo-local instructions or `.agent-flow/config.toml` set `mode = "disabled"`, disclose that Agent-Flow is locally disabled and do not enforce AF for that repo.
- If no repo-local Agent-Flow files or config exist, ask whether to initialize Agent-Flow or disable it locally for the repo.
- Prefer `~/.agent-flow/scripts/init-repo.sh` for initialization. It records whether enforcement is enabled, whether staging is used, and the local branch model.
- Pure read-only chat does not need a worktree. Any file edit, commit, push, dependency change, config change, or destructive action must follow the full AF workflow.
- Agent-Flow should not leave untracked, unstaged, or uncommitted files behind. Dirty worktrees must be reviewed, documented with a devlog entry, and committed before starting another task or merging.

## Prompt Lifecycle

Classify every prompt before acting:

- `chat`: read-only explanation, research, review, or planning. Do not create a worktree unless the user asks to make changes.
- `tiny`: narrow typo, text, CSS, config, or one-file fix with low risk. Create a task worktree, validate, then ask to merge unless `auto_merge = "tiny-only"` is configured.
- `normal`: ordinary fix or feature. Create a task worktree, validate, run review, then ask to merge.
- `large` or `risky`: broad feature, architecture change, migration, dependency change, security-sensitive work, or unclear blast radius. Create a task worktree from the checked-out parent branch unless the user explicitly asks for a feature branch or a different parent.

Use `scripts/start-task.sh` when available to create task worktrees and record lifecycle metadata. Use `scripts/finish-task.sh` when available to check readiness and apply the configured merge policy.

## Non-Negotiable Branch Rules

- `main` is the production PR target. Do not keep it as a local work branch; if a local `main` branch appears, flag it for deletion after confirming it has no unique work. Do not modify, commit to, or push directly to `main`.
- `staging` is optional per repo. Keep a local `staging` branch only when `staging_enabled = true`; otherwise flag it for deletion after confirming it has no unique work. When present or enabled, do not modify, commit to, or push directly to `staging` except through the release promotion workflow.
- `master`, `production`, and `prod` are reserved legacy names. Do not use them as mainline branches.
- Default SDLC integration branch is `development`; it feeds `staging` when enabled and then `main`.
- The task parent branch is the branch the user has checked out for the work. It is usually `development`, unless the user explicitly checked out or requested another non-protected parent.
- Use a separate git worktree for every implementation task.
- Do not create named task branches by default. Use detached task worktrees unless the user explicitly requests a named branch.
- Merge reviewed task worktrees back to their recorded parent branch, not always to `development`.
- When the user requests a named task branch, prefer names like:
  - `fix/<short-description>`
  - `feat/<short-description>`
  - `docs/<short-description>`
  - `chore/<short-description>`

## Worktree Rules

- Use one git worktree per implementation task.
- Create worktrees from the checked-out parent branch unless the user explicitly supplies another non-protected parent branch.
- Record detached task metadata in worktree-local Git config, for example `agentFlow.parent` and `agentFlow.taskClass`.
- For explicit named task branches, also record branch metadata, for example `branch.<task-branch>.agentFlowParent`.
- Keep each task narrowly scoped.
- Avoid editing the same shared files across parallel sessions when possible.
- Add one devlog file under `devlog/` for each meaningful commit or planned squash commit.
- Do not rewrite unrelated devlog files from other branches or worktrees.
- Before merge, update from the parent branch, resolve conflicts, then run review.

Long-running feature work still uses task worktrees by default. Create a feature branch only when the user explicitly asks for one; then use that branch as the checked-out parent for subsequent task worktrees.

## Merge Policy

- Default behavior is `merge_prompt = "always"`: after a task is validated and reviewed, ask before merging back to the parent branch.
- `auto_merge = "off"` is the default and safest behavior.
- `auto_merge = "tiny-only"` may merge only tasks recorded as `tiny`, after validation and review pass, and never into `main` or `staging`.
- `auto_merge = "always"` is allowed only for repos that explicitly opt into it; agents must still respect protected branch, devlog, docs, and validation gates.
- Do not merge dirty worktrees. Commit or clean task changes before merge.
- With `auto_commit = "finish"`, `scripts/finish-task.sh` may commit dirty task work after creating or verifying a devlog entry.
- Dirty parent branches are different: review the existing changes first, create or update a devlog entry, commit them, then start the new task worktree.

## Task Intake

Before implementation, the agent should identify:

- the goal
- affected area of the repo
- parent branch and task worktree
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

Devlog filenames are based on the date plus the planned commit subject slug, not the commit SHA. Store the short commit SHA inside the devlog entry when it is already known; otherwise use `pending`.

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

Update project docs and useful visual assets when the change affects:

- UI or user-facing behavior
- public API behavior
- configuration
- deployment
- database/schema behavior
- security/privacy/compliance behavior
- operational workflows
- onboarding, demos, presentations, screenshots, or marketing communication

Run project docs maintenance before pushing or promoting `development` to release branches such as optional `staging` and `main`.

## Push Readiness

Before pushing any user-controlled branch, verify all child task worktrees recorded against it are complete:

- no dirty child task worktrees
- no child task worktrees, detached or branch-backed, with commits missing from the parent branch
- no unresolved review or validation blockers

Use `scripts/check-push-readiness.sh <branch>` when available. Repos may install `scripts/install-hooks.sh` to enforce this with a local `pre-push` hook. Direct pushes to `main` are blocked. Direct pushes to `staging` are blocked unless the explicit release promotion workflow sets `AF_ALLOW_RELEASE_PUSH=1`.

## Formal Security Review

Before creating a pull request whose base branch is `staging` or `main`, run a distinct formal security review. Use `af-security-review` when available. This gate is separate from `af-review-gate`: task review checks merge readiness, while security review checks the accumulated release diff before protected-branch promotion.

Run the formal security review after worktree reconciliation, docs maintenance, and release validation, but before creating or offering the protected-branch pull request. If a repo updates `staging` by direct release push instead of a pull request, run the same security review before that protected release push.

The review must inspect the full protected-branch diff, check security-sensitive changes such as auth, authorization, secret handling, input validation, dependencies, infrastructure, deployment, logging, privacy, and data access, and record findings with security severity. Fix SEC-P1 findings before PR creation. Fix SEC-P2 findings or get explicit user risk acceptance before PR creation.

## Review Gate

Before merging a task worktree back to its parent branch:

- Confirm current branch is not `main`, `staging`, `master`, `production`, or `prod`.
- Confirm the merge target is the task's recorded parent branch, from worktree-local config or explicit branch metadata.
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
- Do not edit `main` or `staging` directly; use release promotion or pull requests.
- Keep `.gitignore` valid and non-destructive. Init should create or append an Agent-Flow ignore block, never replace existing repo rules.
- Treat IDE folders as personal by default. Commit `.vscode/extensions.json`, `.vscode/tasks.json`, `.vscode/launch.json`, or `.vscode/settings.json` only when they intentionally encode shared project tooling; do not commit themes, window titles, local paths, or UI preferences.
- Keep changes tightly scoped to the user's request.
- Flag suspicious, risky, or destructive operations before running them.

## Done Definition

A task is done when:

- changes are implemented in a task worktree when Git is already initialized
- validation has been run or documented as unavailable
- a per-commit devlog file exists under `devlog/`
- affected project docs and visual assets are updated
- review has been performed for merge-ready work
- formal security review has passed before protected-branch PRs or equivalent staging promotion when applicable
- merge readiness has been reported and the user has been asked whether to merge, unless local config allowed an automatic merge
- parent branch push readiness has been checked before any remote push
- the final response includes what changed, validation, docs updated, and merge status
