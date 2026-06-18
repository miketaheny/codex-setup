# Project Agent-Flow Instructions

Follow the global AF Agent-Flow rules plus these project-specific instructions.

## Project Overview

- Purpose: TODO
- Main app/package: TODO
- Runtime: TODO
- Framework: TODO

## Important Directories

- `src/` - application code
- `tests/` - tests
- `docs/` - project docs
- `docs/decisions/` - architecture/implementation decisions
- `docs/solutions/` - reusable solved problems
- `docs/diagrams/` - diagram sources when separate files are useful
- `docs/presentations/` - slide outlines or deck source material

Adjust this section to match the actual repo.

## Branching

- Base implementation work from the checked-out user-controlled parent branch.
- Use one AF session worktree per file-changing chat.
- Use detached session worktrees by default; create named branches only when the user explicitly requests a branch.
- Read-only chats do not need worktrees; file-changing chats must create or adopt a session worktree before editing.
- Never work directly on `main`; `main` is the production PR target and should not be kept as a local work branch.
- Never work directly on a branch named `staging`; keep local `staging` only when `.agent-flow/config.toml` has `staging_enabled = true`.
- Do not use `master`, `production`, or `prod` as mainline branches; flag local branches with those names for cleanup.
- Merge reviewed session worktrees back to their parent branch after asking the user unless local config explicitly allows auto-merge.
- If a chat changes direction, finish, pause, or abandon the current session worktree and start a new chat/worktree.
- Use `development` as the SDLC integration branch that feeds optional `staging` and then `main`.

## Commands

Update these after inspecting the repo.

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

- Add or update one Markdown devlog file under `devlog/` for each session commit or planned squash commit.
- Update project docs and useful visual assets when behavior, setup, architecture, security, deployment, operations, onboarding, demos, or marketing needs change.
- Add reusable patterns to `docs/solutions/`.
- Add architectural decisions to `docs/decisions/`.
- Run docs maintenance before pushing or promoting `development` to optional `staging` or `main`.
- Run formal security review before creating a pull request to `staging` or `main`.
- Run `scripts/check-push-readiness.sh <branch>` before pushing a parent branch.

## Gitignore and IDE Files

- Keep a valid `.gitignore` for local runtime files, environment files, OS noise, logs, temp files, and personal IDE state.
- Do not overwrite existing repo ignore rules; append project policy blocks.
- Commit IDE files only when they encode shared project behavior such as recommended extensions, debug tasks, launch configs, formatter/linter settings, or test runner integration.
- Do not commit personal IDE preferences such as themes, window titles, UI layout, local paths, or machine-specific interpreter paths.

## Review Expectations

Before merge:

- inspect diff against the session's parent branch
- run relevant validation
- update docs
- run `af-review-gate`
- resolve P1 findings

Before protected-branch PRs:

- run `af-security-review`
- resolve SEC-P1 findings
- resolve SEC-P2 findings or record explicit user risk acceptance
