# Project Agent-Flow Instructions

Follow the global AF rules plus these project-specific notes.

## Project Overview

- Purpose: TODO
- Main app/package: TODO
- Runtime: TODO
- Framework: TODO

## Important Directories

- `src/` - application code
- `tests/` - tests
- `docs/` - project docs
- `devlog/` - session history

Adjust this section to match the repo.

## Branching

- Use one active AF session worktree for a related working session, not one worktree per prompt.
- Keep related Codex/agent follow-up work in the same session worktree until the user asks to finish, review, reconcile, merge, or switch direction.
- Use the fast path for routine work: targeted context reads, scoped edits, focused validation, one finish-time devlog, and no full audits unless requested or risk-triggered.
- For newly adopted repos, run `~/.agent-flow/scripts/init-repo.sh` before file-changing work unless the user explicitly opts out for this repo.
- Use detached session worktrees by default.
- Create named branches only when explicitly requested.
- Merge reviewed sessions back to their recorded parent branch after asking the user.
- Never work directly on `main`.
- Treat `staging` as protected when enabled.
- Do not use `master`, `production`, or `prod` as mainline branches.
- Use `development` as the default integration branch unless this repo config says otherwise.

## Commands

Update after inspecting the repo.

```bash
# install
TODO

# dev
TODO

# test
TODO

# lint
TODO

# typecheck
TODO

# build
TODO
```

## Documentation

- Add or update one `devlog/` entry for every file-changing session.
- Update docs when behavior, setup, architecture, security, deployment, operations, onboarding, or user workflows change.
- Add reusable patterns to `docs/solutions/`.
- Add durable decisions to `docs/decisions/`.
- Use `af-feature-audit` only when explicitly requested for app-wide feature/user-story QA work; keep its canonical register at `docs/product/feature-register.csv` unless this repo config says otherwise.
- Use `af-brand-guidelines` to create or ingest brand/design rules before broad UI work when no guideline exists.
- Use `af-ui-audit` only when explicitly requested for responsive UI/UX audit work; keep its canonical register at `docs/product/ui-audit-register.csv` unless this repo config says otherwise.
- Run `scripts/check-push-readiness.sh <branch>` before pushing a parent branch.

## Review Expectations

Before merge:

- inspect the diff against the recorded parent branch
- run relevant validation
- use `af-show` when visual or manual proof matters
- update devlog and impacted docs
- run `af-review`
- resolve P1 findings

Do not run `af-finish` automatically after every prompt. Finish is a deliberate wrap-up step.

## Codex Model And Effort

For Codex, run an effort preflight before acting. Prefer `gpt-5.5` with `xhigh` reasoning for most development and computer-use work. Use fast/low settings for read-only help or status, medium for trivial one-file edits, and `deep`/`xhigh` for release review, hard debugging, or security-sensitive work. See the installed Agent-Flow guide at `~/.agent-flow/docs/CODEX-MODEL-POLICY.md`.

Before release:

- run `af-reconcile`
- run `af-full-review`
- run `af-security-review` if requested, configured, or security-sensitive; prefer the Codex Security diff-scan path when available
- run `af-release`

## Gitignore And IDE Files

- Preserve existing ignore rules; append project policy blocks.
- Commit IDE files only when they encode shared project tooling.
- Keep personal IDE preferences and local paths untracked.
