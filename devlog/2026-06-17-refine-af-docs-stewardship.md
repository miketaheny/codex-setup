# 2026-06-17 - Refine AF docs stewardship

## Branch / Worktree

- Branch: `feat/visual-docs-backlog-migration`
- Worktree: `/Users/taheny/vault/teamt/codex-setup`

## Goal

Update `af-docs` so it can run an in-depth interview for existing documentation stewardship, then manage `docs/` continuously from repo evidence instead of treating docs cleanup as an archive-first or repeated-interview workflow.

## Files Changed

- `skills/af-docs/SKILL.md`
- `CHANGELOG.md`
- `docs/DOCS-STRATEGY.md`
- `README.md`
- `docs/WORKFLOW.md`
- `docs/AGENT-PROMPTS.md`
- `docs/VISUALS.md`
- `devlog/2026-06-17-refine-af-docs-stewardship.md`

## Decisions

- Added a one-time stewardship setup mode to `af-docs` for repos with existing docs.
- Made `docs/DOCS-STRATEGY.md` the ongoing source of truth for docs ownership, audiences, visual decisions, and maintenance triggers.
- Clarified that useful docs should be updated, merged, split, or superseded before considering archive/removal.
- Clarified that future routine docs updates should use devlog entries, commits, diffs, scripts, skills, templates, screenshots, and config rather than repeating the full interview.
- Documented this repo's current docs inventory and visual strategy so `af-docs` can manage `docs/` consistently on future changes.
- Added a project changelog because this branch changes user-facing Agent-Flow workflow behavior.

## Validation

- `quick_validate.py` passed for all AF skills.
- `bash -n` passed for `scripts/install.sh`, `scripts/bootstrap-repo.sh`, `scripts/new-worktree.sh`, `scripts/review-snapshot.sh`, and `scripts/check-branch-safety.sh`.
- `python3 -m py_compile` passed for the Python helper scripts.
- `git diff --check` passed.
- Focused content scan confirmed the new stewardship and `DOCS-STRATEGY.md` guidance is present across the skill and docs.
- After adding `CHANGELOG.md`, reran skill validation, shell syntax checks, and `git diff --check`; all passed.

## Review Result

- Self-review completed. No blocking issues found.

## Follow-ups / Risks

- Future runs should render Mermaid diagrams if diagram syntax changes.
- Future screenshot or demo assets should be verified from a real install/bootstrap run before claiming they are complete.
