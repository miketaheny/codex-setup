# Useful Agent-Flow Prompts

## Small change

```text
Use af-small-change. Fix [issue]. Keep scope narrow. Do not touch main or staging. Add a devlog entry under devlog/.
```

## Worktree session

```text
Use af-worktree-task. Create or adopt one AF session worktree from the checked-out parent branch. Do not create a named branch unless I explicitly ask for one. Implement the session goal, validate, add or update the devlog under devlog/, and run review before merge.
```

## Seamless session lifecycle

```text
Use Agent-Flow for this change. Create one AF session worktree, implement it, then use af-finish-session to validate, review, run browser QA if applicable, and ask me before merging if it is ready.
```

## Explicit feature branch

```text
Create a feature branch for this work only if needed, then create session worktrees under it and merge reviewed sessions back there.
```

## Review branch

```text
Use af-review-gate. Review this session worktree against AGENT-FLOW.md, agent adapter files, devlog/, project docs, tests, and merge safety. Tell me if it is ready to merge into its recorded parent branch.
```

## Finish session

```text
Use af-finish-session. Start the repo and open the Codex browser if the change is user-facing, run validation and review, update devlog/docs, then ask me before merging into the recorded parent branch.
```

## Formal security review

```text
Use af-security-review. Run the formal security gate for [head branch] against [staging or main] before creating a protected-branch pull request. Report blocking security findings and accepted risks.
```

## Project docs

```text
Use af-docs. Update project docs from devlog/ and recent commits before preparing release PRs.
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
Use af-reconcile-worktrees. Open the worktree manager, show the visual worktree map, identify incomplete or unmerged work, and clean up completed worktrees I have approved.
```

## Push readiness

```text
Run scripts/check-push-readiness.sh for the branch I am about to push. Block the push if any child session worktree is dirty or unmerged.
```

## Gitignore and IDE policy

```text
Ensure this repo has the Agent-Flow .gitignore block. Preserve existing ignore rules. Commit IDE files only if they encode shared project tooling, not personal preferences.
```

## Release PR

```text
Use af-release-pr. Ask me about open worktrees, validate development, run docs and security review, push origin development when ready, then prepare the correct release PR. Default to development -> staging, then staging -> main after staging contains the release; use development -> main only when staging is disabled or I explicitly request it.
```

## Workflow decision

```text
Use af-compound-mode. Decide whether this should use a light Agent-Flow skill or a heavier planning/review workflow, then proceed with the lightest safe option.
```

## Parallel session

```text
Use a heavier workflow for this session only. You are in an isolated worktree. Keep scope limited to [area]. Add/update the devlog under devlog/. Avoid shared files unless required. Do not merge until review passes.
```
