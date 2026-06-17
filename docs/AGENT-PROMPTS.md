# Useful Agent-Flow Prompts

## Small change

```text
Use af-small-change. Fix [issue]. Keep scope narrow. Do not touch main or staging. Add a devlog entry under devlog/.
```

## Worktree task

```text
Use af-worktree-task. Create a worktree from the checked-out parent branch named ../[repo]-[task] with branch [type]/[task]. Implement the task, validate, add a devlog entry under devlog/, and run review before merge.
```

## Seamless task lifecycle

```text
Use Agent-Flow for this change. Classify the task, create a task worktree, implement it, run finish-task, and ask me before merging if it is ready.
```

## Large feature branch

```text
This may be large. Ask whether to create a feature parent branch first. If approved, create the feature parent branch, then create task worktrees under it and merge reviewed subtasks back there.
```

## Review branch

```text
Use af-review-gate. Review this branch against AGENT-FLOW.md, agent adapter files, devlog/, project docs, tests, and merge safety. Tell me if it is ready to merge into its recorded parent branch.
```

## Formal security review

```text
Use af-security-review. Run the formal security gate for [head branch] against [staging or main] before creating a protected-branch pull request. Report blocking security findings and accepted risks.
```

## Project docs

```text
Use af-docs. Update project docs from devlog/ and recent commits before promoting development through the release path.
```

## Existing docs stewardship

```text
Use af-docs. Inventory the existing docs, interview me in depth about audience, jobs, visual style, authoritative docs, and maintenance rules, then update useful docs in place and create docs/DOCS-STRATEGY.md so future docs updates can be managed from devlog/, commits, diffs, and repo evidence.
```

## Ongoing docs maintenance

```text
Use af-docs. Follow docs/DOCS-STRATEGY.md, then update docs/ from the latest devlog entries, commits, changed scripts, skills, templates, screenshots, and config. Do not repeat the full stewardship interview unless the strategy needs to change.
```

## Visual docs

```text
Use af-docs. Interview me about the audience, style, and format, then recommend and create useful diagrams, guides, screenshots, demo plans, presentations, and marketing content.
```

## Backlog migration

```text
Use af-migrate-backlog-devlog. Dry-run a migration from Backlog.md, backlog/, or .backlog task files to devlog entries, show me the plan, then write entries after approval.
```

## Reconcile worktrees

```text
Use af-reconcile-worktrees. Audit worktrees, local branches, and agent instruction conflicts. Do not remove worktrees or delete branches without explicit approval.
```

## Push readiness

```text
Run scripts/check-push-readiness.sh for the branch I am about to push. Block the push if any child task worktree is dirty or unmerged.
```

## Gitignore and IDE policy

```text
Ensure this repo has the Agent-Flow .gitignore block. Preserve existing ignore rules. Commit IDE files only if they encode shared project tooling, not personal preferences.
```

## Promote development

```text
Use af-push-staging. Reconcile worktrees, validate development, run formal security review, and promote through the configured release path. If staging is enabled, review development to staging, merge development into staging, then review staging to main before asking to create a staging-to-main PR. If staging is disabled, review development to main before asking to create a development-to-main PR.
```

## Workflow decision

```text
Use af-compound-mode. Decide whether this should use a light Agent-Flow skill or a heavier planning/review workflow, then proceed with the lightest safe option.
```

## Parallel session

```text
Use a heavier workflow for this task only. You are in an isolated worktree. Keep scope limited to [area]. Add devlog entries under devlog/. Avoid shared files unless required. Do not merge until review passes.
```
