---
name: af-push-staging
description: Legacy Agent-Flow release PR alias. Use only when the user explicitly asks for af-push-staging, push staging, or old staging promotion wording; follow af-release-pr to push development and create protected release pull requests.
---

# AF Push Staging Compatibility Skill

This legacy skill name is retained so older prompts and installed setups do not run stale direct-staging-push instructions.

Use `af-release-pr` as the canonical workflow. If `af-release-pr` is unavailable, follow the PR-first release rules:

- Ask about open worktrees before release PR creation.
- Validate `development` and run docs maintenance when needed.
- Run `scripts/check-push-readiness.sh development`.
- Push and verify `origin/development` after approval.
- Run `af-security-review` before any PR whose base is `staging` or `main`.
- Default to a `development -> staging` PR, then a `staging -> main` PR after staging contains the release.
- Use `development -> main` only when staging is disabled or explicitly requested.
- Do not push `staging` directly except as an explicitly approved repo-specific exception.
