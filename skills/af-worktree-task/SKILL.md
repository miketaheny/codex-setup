---
name: af-worktree-task
description: Create and use isolated git worktrees for parallel agent tasks, based from development, with safe branch naming, scoped work, docs updates, and review readiness.
---

# AF Worktree Task Skill

Use this skill when the user wants safe parallel work, multiple agent sessions, or a clean isolated task branch.

## Goal

Prevent parallel agent sessions from colliding by isolating each task in a separate git worktree and feature branch.

## Preconditions

Before changing files:

1. Confirm this is a git repo.
2. Inspect branches.
3. Confirm `development` exists.
4. Confirm current repo status.
5. If there are uncommitted changes in the current tree, do not overwrite them.

## Worktree naming

Use this pattern:

```text
../<repo-name>-<short-task>
```

Branch pattern:

```text
fix/<short-task>
feat/<short-task>
docs/<short-task>
chore/<short-task>
```

## Create worktree

```bash
git fetch --all --prune
git switch development
git pull --ff-only
git worktree add ../<repo-name>-<short-task> -b <type>/<short-task> development
```

If `git pull --ff-only` is not appropriate because there is no upstream, document that and continue from local `development`.

## In the worktree

1. Re-read repo agent instruction files from the worktree.
2. Implement only the requested task.
3. Avoid broad shared files unless required.
4. Add per-commit devlog files under `devlog/`.
5. Update affected project docs when behavior, setup, architecture, security, deployment, or operations change.
6. Run validation.
7. Run review gate.

## Merge readiness

Do not merge automatically unless the user explicitly asked.

Before suggesting merge:

```bash
git status
git diff --stat development...HEAD
git diff development...HEAD
```

Summarize:

- worktree path
- branch name
- changed files
- validation
- docs updated
- review result
- merge command if ready

## Merge command template

```bash
cd <main-repo-or-development-worktree>
git switch development
git merge --no-ff <branch-name>
```
