# AF Agent-Flow Workflow

## Core Idea

Use AI coding agents like a disciplined solo engineering team:

1. Classify the prompt.
2. Isolate file-changing work in a task worktree.
3. Keep scope narrow.
4. Make the change.
5. Validate it.
6. Document the reasoning.
7. Review before merge.
8. Ask before merging back to the checked-out parent branch.
9. Check child worktrees before pushing a parent branch.

## Branch Model

Agent-Flow has two branch concepts:

- Task parent branch: the user-controlled branch that is checked out when the task begins. Task worktrees branch from it and merge back to it.
- SDLC integration branch: `development`, which stays open for ongoing fixes and feeds the release path.

Typical routine work:

```text
development
  ├── fix/navbar-spacing
  ├── fix/contact-form-validation
  └── docs/devlog-cleanup
```

Longer feature work:

```text
feat/payments-redesign
  ├── feat/payment-form
  ├── fix/payment-validation
  └── docs/payment-runbook
```

After the feature branch is ready, the user merges it into `development`.

Protected or reserved branches:

- `main` - production branch
- `staging` - optional release branch when enabled; direct edits are blocked when a branch uses this name
- `master`, `production`, `prod` - reserved legacy names, not mainline branches

Release path:

- with staging: `development -> staging -> main`
- without staging: `development -> main` by pull request

## Prompt Lifecycle

| Prompt class | Default behavior |
|---|---|
| Chat/read-only | Answer directly; no worktree needed. |
| Tiny | Create a task worktree, validate, update devlog/docs if needed, ask to merge. |
| Normal | Create a task worktree, validate, run review, ask to merge. |
| Large/risky | Ask whether to create a feature parent branch first, then create task worktrees under that parent. |

Default merge policy:

- `auto_commit = "finish"` commits dirty task work after devlog checks before merge readiness.
- `merge_prompt = "always"`
- `auto_merge = "off"`
- Optional `auto_merge = "tiny-only"` can merge only validated tiny task branches.
- Agents never auto-merge into `main` or `staging`.

Dirty parent worktrees are handled before task start: review the existing changes, create or update a devlog entry, commit them, then create the new task worktree.

Lifecycle helpers:

```bash
scripts/start-task.sh --class normal feat export-csv
scripts/finish-task.sh
scripts/finish-task.sh --merge
```

For large work:

```bash
scripts/start-task.sh --class large --create-parent feat/payments feat payment-form
```

## Parallel Work Model

For multiple agent sessions:

```bash
git switch <parent-branch>
git pull

git worktree add ../repo-navbar -b fix/navbar-spacing <parent-branch>
git config branch.fix/navbar-spacing.agentFlowParent <parent-branch>

git worktree add ../repo-contact-form -b fix/contact-form-validation <parent-branch>
git config branch.fix/contact-form-validation.agentFlowParent <parent-branch>
```

Open one agent session per worktree.

## Command Choice

| Situation | Suggested workflow |
|---|---|
| Tiny typo/config/CSS fix | `af-small-change` |
| Small bug | `af-small-change` or a brief plan/work pass |
| Normal feature | plan -> work -> `af-review-gate` |
| Risky/broad feature | heavier planning/review workflow |
| Reusable lesson | project docs update or `af-devlog` |
| Legacy Backlog/task migration | `af-migrate-backlog-devlog` |
| Visual docs, guides, demos, decks, or marketing | `af-docs` |
| Worktree or branch cleanup | `af-reconcile-worktrees` |
| Before merge | `af-review-gate` |
| Before release promotion | `af-reconcile-worktrees` -> `af-docs` -> `af-push-staging` |

## Documentation Rules

Always add a devlog file under `devlog/` for meaningful commits.

Use one Markdown file per commit, or one file for the planned squash commit when the branch will be squashed before merge.

Name devlog files from the date and planned commit subject, such as `devlog/YYYY-MM-DD-fix-navbar-spacing.md`. Do not name them from the commit SHA; record the SHA inside the file when known.

Update project docs when behavior, setup, architecture, security, deployment, or operations change.

## Gitignore and IDE Policy

Repo init ensures `.gitignore` has an Agent-Flow block for local runtime files, env files, OS/editor noise, logs, temp files, and personal IDE state. Existing ignore rules are preserved.

Commit IDE files only when they encode shared project behavior. Good examples are recommended extensions, debug tasks, launch configs, formatter/linter settings, and test runner integration. Do not commit personal IDE preferences such as themes, window titles, UI layout, local paths, or machine-specific interpreter paths.

Use `af-docs` for initial documentation stewardship and ongoing docs maintenance. For repos with existing docs, the first stewardship pass should inventory current docs, interview the user about audiences and visual style, update useful docs in place, and record the maintenance contract in `docs/DOCS-STRATEGY.md`.

After `docs/DOCS-STRATEGY.md` exists, `af-docs` should fully manage `docs/` from devlog files, commits, diffs, scripts, templates, skills, screenshots, and config changes. Do not repeat the full interview for routine changes unless the user asks or the repo's audience, product direction, or documentation structure changes.

Use `af-docs` to decide which visual assets are worth creating: Mermaid or D2 diagrams, screenshots, demo videos, user guides, presentation outlines, product one-pagers, or marketing content.

Run `af-docs` before pushing or promoting `development` through optional `staging` or to `main`.

## Backlog Migration

Use `af-migrate-backlog-devlog` when a repo still has `Backlog.md`, `triage.md`, `backlog/`, or `.backlog/` files. Run its dry-run first, review the generated devlog plan, then write entries before deleting any legacy task store.

## Release Promotion

Use `af-reconcile-worktrees` before release promotion to find dirty worktrees, unmerged branches, missing task-parent metadata, and instruction conflicts.

Run `scripts/check-push-readiness.sh development` before pushing `development`. For feature parent branches, run the same check against the feature branch before pushing it.

Use `af-push-staging` to promote `development` through the configured release path. With staging enabled, it validates, merges `development` into `staging`, pushes both branches, then offers a `staging` to `main` PR. With staging disabled, it validates and pushes `development`, then offers a `development` to `main` PR.
