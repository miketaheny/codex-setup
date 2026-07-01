# 2026-07-01 - Remove repo Claude settings

- Branch/worktree: `f4ec6b6` / `/Users/taheny/vault/teamt/agent-flow.worktrees/remove-claude-settings`
- Commit: pending
- Goal: Remove the remaining repo-level Claude settings file before releasing the Codex-first Agent-Flow workflow.
- Summary:
  - Removed `.claude/settings.json` because Agent-Flow is now Codex-first and no longer keeps Claude adapter/config surfaces in the repo.
- Validation:
  - `find . -path './.git' -prune -o -path './.claude/*' -print` - passed, no repo `.claude` files remain after deletion.
  - `find . -name 'CLAUDE.md' -o -name '*CLAUDE*' -print` - passed, no repo Claude adapter files remain.
  - `git diff --check` - passed.
- Risks / follow-ups:
  - None.
