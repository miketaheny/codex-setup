# Useful Agent-Flow Prompts

## Small change

```text
Use af-small-change. Fix [issue]. Keep scope narrow. Do not touch main/staging. Add a devlog entry under devlog/.
```

## Worktree task

```text
Use af-worktree-task. Create a worktree from development named ../[repo]-[task] with branch [type]/[task]. Implement the task, validate, add a devlog entry under devlog/, and run review before merge.
```

## Review branch

```text
Use af-review-gate. Review this branch against AGENT-FLOW.md, agent adapter files, devlog/, project docs, tests, and merge safety. Tell me if it is ready to merge into development.
```

## Project docs

```text
Use af-docs. Update project docs from devlog/ and recent commits before promoting development.
```

## Reconcile worktrees

```text
Use af-reconcile-worktrees. Audit worktrees, local branches, and agent instruction conflicts. Do not remove worktrees or delete branches without explicit approval.
```

## Promote staging

```text
Use af-push-staging. Reconcile worktrees, validate development, merge development into staging, push development and staging, then ask before creating a staging-to-main PR.
```

## Workflow decision

```text
Use af-compound-mode. Decide whether this should use a light Agent-Flow skill or a heavier planning/review workflow, then proceed with the lightest safe option.
```

## Parallel session

```text
Use a heavier workflow for this task only. You are in an isolated worktree. Keep scope limited to [area]. Add devlog entries under devlog/. Avoid shared files unless required. Do not merge until review passes.
```
