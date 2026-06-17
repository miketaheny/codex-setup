# AF Agent-Flow Commander Notes

This file is optional scratch guidance for the repo owner.

Recommended flow:

1. Start from `development`.
2. Create a branch or worktree.
3. Use the lightest safe skill.
4. Add a per-commit devlog entry under `devlog/`.
5. Update project docs when behavior, setup, architecture, security, deployment, or operations change.
6. Run docs maintenance before promoting `development` to protected branches.
7. Run `af-review-gate`.
8. Merge into `development`.
9. Run `af-reconcile-worktrees` before cleanup or staging promotion.
10. Run `af-push-staging` when ready to promote `development` to `staging`.
