# Changelog

## Unreleased

### Added

- Agent-Flow setup is now agent-agnostic, with shared workflow rules plus Codex and Claude adapter files.
- Added AF skills for small changes, worktree tasks, review gates, devlog entries, docs maintenance, backlog migration, worktree reconciliation, staging promotion, and compound-mode selection.
- Added `af-migrate-backlog-devlog` to convert `Backlog.md`, `triage.md`, `backlog/`, and `.backlog/` task stores into `devlog/` entries.
- Added visual documentation coverage: architecture diagrams, user guide, demo plan, pitch copy, visual plan, and presentation outline.
- Added `docs/DOCS-STRATEGY.md` so `af-docs` can own ongoing docs maintenance without repeating the full stewardship interview for routine changes.

### Changed

- Replaced backlog-style tracking with per-commit `devlog/` entries as the project history system.
- Expanded `af-docs` from basic docs maintenance into a docs stewardship workflow for existing docs, visual assets, user guides, demos, presentations, and marketing content.
- Updated bootstrap and install behavior to create/copy Agent-Flow docs, skills, scripts, templates, and adapter files consistently.
