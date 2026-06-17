# Changelog

## Unreleased

### Added

- Agent-Flow setup is now agent-agnostic, with shared workflow rules plus Codex and Claude adapter files.
- Added AF skills for small changes, worktree tasks, review gates, devlog entries, docs maintenance, backlog migration, worktree reconciliation, release promotion, and compound-mode selection.
- Added `af-migrate-backlog-devlog` to convert `Backlog.md`, `triage.md`, `backlog/`, and `.backlog/` task stores into `devlog/` entries.
- Added visual documentation coverage: architecture diagrams, user guide, demo plan, pitch copy, visual plan, and presentation outline.
- Added `docs/DOCS-STRATEGY.md` so `af-docs` can own ongoing docs maintenance without repeating the full stewardship interview for routine changes.
- Added `init-repo.sh` and `.agent-flow/config.toml` defaults for first-contact Agent-Flow enforcement choices, checked-out parent branch worktrees, optional staging, and `main` as production.
- Added task lifecycle helpers for `start-task.sh`, `finish-task.sh`, `check-push-readiness.sh`, and `install-hooks.sh`.

### Changed

- Replaced backlog-style tracking with per-commit `devlog/` entries as the project history system.
- Expanded `af-docs` from basic docs maintenance into a docs stewardship workflow for existing docs, visual assets, user guides, demos, presentations, and marketing content.
- Updated bootstrap and install behavior to create/copy Agent-Flow docs, skills, scripts, templates, and adapter files consistently.
- Changed task workflow guidance so task worktrees branch from and merge back to the checked-out parent branch. `development` remains the SDLC integration branch, optional `staging` is protected when configured, and `main` is always production.
- Changed completion guidance so agents ask before merge by default, can auto-merge only when repo config opts in, and check child task worktrees before pushing parent branches.
