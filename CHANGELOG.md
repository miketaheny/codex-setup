# Changelog

## Unreleased

### Added

- Added a Codex fast-path guide in Markdown and PDF form, including workflow, escalation, and worktree diagrams.
- Added a reproducible PDF generator for the Codex fast-path guide.
- Added `af-flow` as the entry workflow for file-changing sessions.
- Added `af-help` for read-only Agent-Flow command help and usage-guide routing.
- Added `af-brand-guidelines` for creating, ingesting, interviewing for, or updating repo brand/design guidelines.
- Added `af-status` for read-only Agent-Flow repo and worktree status snapshots.
- Added `af-finish` as the end-of-session workflow replacing the previous finish naming.
- Added `af-show` for visual or manual proof during finish.
- Added `af-full-review` for release readiness and high-risk exhaustive review.
- Added `af-feature-audit` as a manual-only app-wide feature register, user-story, test, fix, and retest campaign.
- Added `af-ui-audit` as a manual-only responsive UI/UX audit, issue-register, fix, and retest campaign.
- Added installer cleanup for retired AF skill and script names.
- Added `docs/AGENT-FLOW-USAGE.md` and a `templates/feature-register.csv` starting schema.
- Added `templates/ui-audit-register.csv` and `templates/brand-guidelines.md` starting schemas.
- Added Agent-Flow brand guidelines covering positioning, messaging, voice, visual identity, launch surfaces, README hierarchy, and public repo presentation.
- Added an Agent-Flow SVG logo suite with a README wordmark, standalone mark, and social-card asset.

### Changed

- Clarified the daily Agent-Flow fast path: one persistent worktree, targeted context, scoped edits, focused validation, one finish-time devlog, and deliberate escalation.
- Updated Codex model guidance to emphasize starting with the cheapest setting that fits the risk and escalating only when blocked, risky, security-sensitive, or release-facing.
- Simplified Agent-Flow around one lifecycle: `af-flow -> af-devlog -> af-finish`.
- Simplified release readiness to `af-reconcile -> af-full-review -> af-release`.
- Updated `af-security-review` to prefer Codex Security diff scans for Git-backed release diffs when available, with the manual AF checklist as fallback.
- Reworked session scripts so `start-session.sh` and `finish-session.sh` own the lifecycle directly.
- Reduced AF metadata to parent branch, session name, state, owner, devlog policy, timestamps, and optional explicit branch pointer.
- Updated docs, templates, prompts, and skill metadata to use folder names as the source of truth.
- Refreshed the README as a sharper public entrypoint with purpose, goals, included components, compact daily loop, docs navigation, logo, and brand direction.
- Removed task-size and tiny auto-merge compatibility language from the active workflow.

### Removed

- Removed retired public workflow names from current docs and install cleanup.
- Removed task-named lifecycle scripts from the active setup.
