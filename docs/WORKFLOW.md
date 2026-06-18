# AF Agent-Flow Workflow

## Core Idea

Use AI coding agents like a disciplined solo engineering team:

1. Decide whether the chat is read-only or file-changing.
2. Isolate every file-changing chat in one AF worktree session.
3. Keep scope narrow.
4. Make the change.
5. Validate it.
6. Start the repo and review in browser/manual QA when the change needs it.
7. Document the reasoning.
8. Review before merge.
9. Ask before merging back to the checked-out parent branch.
10. Check child session worktrees before pushing a parent branch.
11. Run formal security review before protected-branch PRs.

## Branch Model

Agent-Flow has two branch concepts:

- Session parent branch: the user-controlled branch that is checked out when the session begins. Session worktrees are detached from it by default and merge back to it.
- SDLC integration branch: `development`, which stays open for ongoing fixes and feeds the release path.

Typical routine work:

```text
development
  ├── ../repo-navbar-spacing
  ├── ../repo-contact-form-validation
  └── ../repo-devlog-cleanup
```

Longer feature work:

```text
development
  ├── ../repo-payment-form
  ├── ../repo-payment-validation
  └── ../repo-payment-runbook
```

Create a feature branch only when the user explicitly asks for one. If that happens, the feature branch becomes the checked-out parent for later session worktrees.

Protected or reserved branches:

- `main` - production PR target; should not be kept as a local work branch
- `staging` - optional release branch; keep locally only when `staging_enabled = true`
- `master`, `production`, `prod` - reserved legacy names; flag local branches with these names for cleanup

Release path:

- with staging: `development -> staging -> main`
- without staging: `development -> main` by pull request

## Chat Lifecycle

| Chat kind | Default behavior |
|---|---|
| Chat/read-only | Answer directly; no worktree needed. |
| File-changing | Create or adopt exactly one AF worktree session, validate, run app/browser review when applicable, update devlog/docs if needed, ask to merge. |
| Changed direction | Finish, pause, or abandon the current worktree, then start a new chat/worktree. |

Default merge policy:

- `auto_commit = "finish"` commits dirty session work after devlog checks before merge readiness.
- `merge_prompt = "always"`
- `auto_merge = "off"`
- `auto_merge = "tiny-only"` is retained only for older metadata; the default is still to ask before merge.
- Agents never auto-merge into `main` or `staging`.

Dirty parent worktrees are reported before session start. Do not hide parent checkout changes inside a new session worktree.

Lifecycle helpers:

```bash
scripts/start-session.sh feat export-csv
scripts/finish-session.sh
scripts/finish-session.sh --merge
```

Prefer `af-finish-session` at the end of a worktree session so validation, optional browser QA, devlog/docs checks, review, and merge readiness happen together.

Create a named branch only when the user explicitly asks for one:

```bash
scripts/start-session.sh --branch feat/payment-form feat payment-form
```

## Parallel Work Model

For multiple agent sessions:

```bash
git switch <parent-branch>
git pull

git worktree add --detach ../repo-navbar <parent-branch>
git -C ../repo-navbar config --worktree agentFlow.parent <parent-branch>

git worktree add --detach ../repo-contact-form <parent-branch>
git -C ../repo-contact-form config --worktree agentFlow.parent <parent-branch>
```

Open one agent session per worktree.

## Command Choice

| Situation | Suggested workflow |
|---|---|
| Tiny typo/config/CSS fix | `af-small-change` |
| Small bug | `af-small-change` or a brief plan/work pass |
| Normal feature | plan -> work -> `af-finish-session` |
| Risky/broad feature | heavier planning/review workflow |
| Reusable lesson | project docs update or `af-devlog` |
| Legacy Backlog/task migration | `af-migrate-backlog-devlog` |
| Visual docs, guides, demos, decks, or marketing | `af-docs` |
| Worktree or branch cleanup | `af-reconcile-worktrees` |
| Pick up incomplete work | `af-reconcile-worktrees` or `scripts/worktree-manager.py --pickup <id>` |
| Complete a session before merge | `af-finish-session` with `af-review-gate` |
| Before protected-branch PR | `af-security-review` |
| Before release PR | `af-reconcile-worktrees` -> `af-docs` -> `af-release-pr` with `af-security-review` |

## Documentation Rules

Always add or update a devlog file under `devlog/` before finishing a session with meaningful changes.

Use one Markdown file per session commit, or one file for the planned squash commit when the branch will be squashed before merge.

Name devlog files from the date and planned commit subject, such as `devlog/YYYY-MM-DD-fix-navbar-spacing.md`. Do not name them from the commit SHA; record the SHA inside the file when known.

Update project docs when behavior, setup, architecture, security, deployment, or operations change.

## Worktree Manager

Use the manager to visualize, pick up, and clean up worktrees:

```bash
scripts/worktree-manager.py --interactive
scripts/worktree-manager.py --details <id>
scripts/worktree-manager.py --pickup <id>
scripts/worktree-manager.py --cleanup <id> --yes
scripts/worktree-manager.py --cleanup-all --yes
```

Pickup marks incomplete work active in AF metadata and prints a handoff. Prefer a new Codex chat when picking up a different worktree.

## Gitignore and IDE Policy

Repo init ensures `.gitignore` has an Agent-Flow block for local runtime files, env files, OS/editor noise, logs, temp files, and personal IDE state. Existing ignore rules are preserved.

Commit IDE files only when they encode shared project behavior. Good examples are recommended extensions, debug tasks, launch configs, formatter/linter settings, and test runner integration. Do not commit personal IDE preferences such as themes, window titles, UI layout, local paths, or machine-specific interpreter paths.

Use `af-docs` for initial documentation stewardship and ongoing docs maintenance. For repos with existing docs, the first stewardship pass should inventory current docs, interview the user about audiences and visual style, update useful docs in place, and record the maintenance contract in `docs/DOCS-STRATEGY.md`.

After `docs/DOCS-STRATEGY.md` exists, `af-docs` should fully manage `docs/` from devlog files, commits, diffs, scripts, templates, skills, screenshots, and config changes. Do not repeat the full interview for routine changes unless the user asks or the repo's audience, product direction, or documentation structure changes.

Use `af-docs` to decide which visual assets are worth creating: Mermaid or D2 diagrams, screenshots, demo videos, user guides, presentation outlines, product one-pagers, or marketing content.

Run `af-docs` before pushing `development` or preparing release PRs through optional `staging` or to `main`.

## Backlog Migration

Use `af-migrate-backlog-devlog` when a repo still has `Backlog.md`, `triage.md`, `backlog/`, or `.backlog/` files. Run its dry-run first, review the generated devlog plan, then write entries before deleting any legacy task store.

## Release PRs

Use `af-reconcile-worktrees` before release PRs to find dirty worktrees, unmerged branches, missing session-parent metadata, local protected branch policy violations, and instruction conflicts. Ask the user what to do with open worktrees before continuing.

Run `scripts/check-push-readiness.sh development` before pushing `development`. For an explicitly requested feature parent branch, run the same check against the feature branch before pushing it.

Use `af-release-pr` to prepare protected release PRs. By default, it validates `development`, checks readiness, pushes `origin development` after approval, runs formal security review for `development -> staging`, and offers or creates a `development -> staging` PR. After that PR is merged and staging contains the release, it runs formal security review for `staging -> main` and offers or creates a `staging -> main` PR. With staging disabled, it validates and pushes `development`, runs formal security review for `development -> main`, then offers or creates a `development -> main` PR.

Run `af-security-review` as a distinct gate before creating any pull request whose base is `staging` or `main`.
