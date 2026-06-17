# AF Agent-Flow Workflow

## Core Idea

Use AI coding agents like a disciplined solo engineering team:

1. Isolate work.
2. Keep scope narrow.
3. Make the change.
4. Validate it.
5. Document the reasoning.
6. Review before merge.
7. Merge back to `development`, not protected branches.

## Branch Model

```text
development
  ├── fix/navbar-spacing
  ├── fix/contact-form-validation
  ├── feat/service-card
  └── docs/devlog-cleanup
```

Protected branches:

- `main`
- `master`
- `staging`
- `production`
- `prod`

Default merge target:

- `development`

## Parallel Work Model

For multiple agent sessions:

```bash
git switch development
git pull

git worktree add ../repo-navbar -b fix/navbar-spacing development
git worktree add ../repo-contact-form -b fix/contact-form-validation development
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
| Worktree or branch cleanup | `af-reconcile-worktrees` |
| Before merge | `af-review-gate` |
| Before staging promotion | `af-reconcile-worktrees` -> `af-docs` -> `af-push-staging` |

## Documentation Rules

Always add a devlog file under `devlog/` for meaningful commits.

Use one Markdown file per commit, or one file for the planned squash commit when the branch will be squashed before merge.

Update project docs when behavior, setup, architecture, security, deployment, or operations change.

Run `af-docs` before pushing or promoting `development` to protected branches such as `staging`, `main`, release, or production branches.

## Staging Promotion

Use `af-reconcile-worktrees` before staging promotion to find dirty worktrees, unmerged branches, and instruction conflicts.

Use `af-push-staging` to promote `development` to `staging`. It commits intended `development` changes, validates, merges into `staging`, pushes `development` and `staging`, then offers a `staging` to `main` PR only after the push succeeds.
