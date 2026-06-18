---
name: af-worktree-task
description: Create and use isolated git worktrees for agent tasks, based from the checked-out parent branch, with named branches only when explicitly requested.
---

# AF Worktree Task Skill

Use this skill for any prompt that changes files, and when the user wants safe parallel work, multiple agent sessions, or a clean isolated task worktree.

## Goal

Prevent agent sessions from colliding by isolating each implementation task in a separate git worktree. Use detached task worktrees by default; create a named branch only when the user explicitly asks for one.

## Preconditions

Before changing files:

1. Confirm this is a git repo.
2. Inspect branches.
3. Identify the checked-out parent branch.
4. Confirm current repo status.
5. If there are uncommitted changes in the current tree, do not overwrite them.
6. If the current branch is `main`, `staging`, `master`, `production`, or `prod`, stop and ask the user to check out a user-controlled parent branch such as `development` or `feat/<name>`.
7. Classify the task as `tiny`, `normal`, `large`, or `risky`.
8. For `large` or `risky` tasks, use the checked-out parent branch unless the user explicitly asks for a feature branch or different parent.

## Worktree naming

Use this pattern:

```text
../<repo-name>-<short-task>
```

Branch pattern when explicitly requested:

```text
fix/<short-task>
feat/<short-task>
docs/<short-task>
chore/<short-task>
```

## Create worktree

Prefer the lifecycle helper when available:

```bash
scripts/start-task.sh --class <tiny|normal|large|risky> <type> <short-task>
```

Create a named task branch only when the user explicitly asks for one:

```bash
scripts/start-task.sh --branch <type>/<short-task> --class <tiny|normal|large|risky> <type> <short-task>
```

Manual equivalent:

```bash
git fetch --all --prune
git branch --show-current
git pull --ff-only
git worktree add --detach ../<repo-name>-<short-task> <checked-out-parent-branch>
git -C ../<repo-name>-<short-task> config --worktree agentFlow.parent <checked-out-parent-branch>
git -C ../<repo-name>-<short-task> config --worktree agentFlow.taskClass <tiny|normal|large|risky>
```

If `git pull --ff-only` is not appropriate because there is no upstream, document that and continue from the local parent branch.

The parent branch is user-controlled. It is usually `development` for fixes and routine work. For larger features, still use detached task worktrees from the checked-out parent unless the user intentionally asks for a feature branch.

## In the worktree

1. Re-read repo agent instruction files from the worktree.
2. Implement only the requested task.
3. Avoid broad shared files unless required.
4. Add per-commit devlog files under `devlog/`.
5. Update affected project docs when behavior, setup, architecture, security, deployment, or operations change.
6. Run validation.
7. Run review gate.
8. Finish with the lifecycle helper when available:

```bash
scripts/finish-task.sh
```

If it reports `ASK_USER_MERGE`, ask whether to merge. After explicit approval, run:

```bash
scripts/finish-task.sh --merge
```

## Merge readiness

Do not merge automatically unless the repo config opts into it and the task meets the configured threshold.

Defaults:

- `merge_prompt = "always"` means ask before merge.
- `auto_merge = "off"` means no automatic merge.
- `auto_merge = "tiny-only"` may auto-merge only `tiny` task worktrees after readiness checks pass.
- Never auto-merge to `main` or `staging`.

Before suggesting merge:

```bash
git status
git diff --stat <parent-branch>...HEAD
git diff <parent-branch>...HEAD
```

Summarize:

- worktree path
- branch name, or detached commit when no branch was requested
- parent branch
- changed files
- validation
- docs updated
- review result
- merge command if ready

## Merge command template

```bash
cd <parent-branch-worktree>
git switch <parent-branch>
git merge --no-ff <branch-name>
```
