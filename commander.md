# AF Agent-Flow Commander Notes

This file is optional scratch guidance for the repo owner.

Recommended flow:

1. Start from `development`.
2. Create or adopt one detached AF session worktree for each file-changing chat; create a branch only when you explicitly want one.
3. Use the lightest safe skill.
4. Add or update the finish-time session devlog entry under `devlog/`.
5. Update project docs and useful visual assets when behavior, setup, architecture, security, deployment, operations, onboarding, demos, or marketing needs change.
6. Run docs maintenance before promoting `development` to protected branches.
7. Use `af-migrate-backlog-devlog` before removing legacy Backlog task files.
8. Run `af-review-gate`.
9. Merge into `development`.
10. Run `af-reconcile-worktrees` or `scripts/worktree-manager.py --interactive` before cleanup or staging promotion.
11. Run `af-security-review` before protected-branch PRs or direct staging promotion.
12. Run `af-push-staging` when ready to promote `development` to `staging`.
