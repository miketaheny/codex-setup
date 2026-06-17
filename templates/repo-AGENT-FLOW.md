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

- Base implementation work from `development`.
- Never work directly on `main`, `master`, `staging`, `production`, or `prod`.
- Use feature branches or worktrees.
- Merge reviewed work back to `development`.

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

- Add one Markdown devlog file under `devlog/` for each meaningful commit or planned squash commit.
- Update project docs and useful visual assets when behavior, setup, architecture, security, deployment, operations, onboarding, demos, or marketing needs change.
- Add reusable patterns to `docs/solutions/`.
- Add architectural decisions to `docs/decisions/`.
- Run docs maintenance before pushing or promoting `development` to protected branches.

## Review Expectations

Before merge:

- inspect diff against `development`
- run relevant validation
- update docs
- run `af-review-gate`
- resolve P1 findings
