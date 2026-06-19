# Changelog

## Unreleased

### Added

- Added `af-flow` as the entry workflow for file-changing sessions.
- Added `af-finish` as the end-of-session workflow replacing the previous finish naming.
- Added `af-show` for visual or manual proof during finish.
- Added `af-full-review` for release readiness and high-risk exhaustive review.
- Added installer cleanup for retired AF skill and script names.

### Changed

- Simplified Agent-Flow around one lifecycle: `af-flow -> af-devlog -> af-finish`.
- Simplified release readiness to `af-reconcile -> af-full-review -> af-release`.
- Kept `af-security-review` as an optional deep security-only gate when requested, configured, or security-sensitive.
- Reworked session scripts so `start-session.sh` and `finish-session.sh` own the lifecycle directly.
- Reduced AF metadata to parent branch, session name, state, owner, devlog policy, timestamps, and optional explicit branch pointer.
- Updated docs, templates, prompts, and skill metadata to use folder names as the source of truth.
- Removed task-size and tiny auto-merge compatibility language from the active workflow.

### Removed

- Removed retired public workflow names from current docs and install cleanup.
- Removed task-named lifecycle scripts from the active setup.
