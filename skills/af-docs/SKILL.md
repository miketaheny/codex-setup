---
name: af-docs
description: Maintain project documentation for the AF solo developer workflow, including first-time backfill, ongoing updates from devlog/ and commits, and pre-promotion docs checks.
---

# AF Docs Skill

Use this skill to keep project documentation accurate as the repository changes.

## Purpose

Project docs should explain the current system, not just the latest code diff. This skill handles both first-time documentation setup and ongoing maintenance from recent work.

## When to Run

Run this skill when:

- a repo has missing, empty, or placeholder project docs
- meaningful work changed behavior, setup, architecture, security, deployment, or operations
- recent devlog files or commits describe work that is not reflected in docs
- `development` is about to be pushed or promoted to protected branches such as `staging`, `main`, release, or production branches

Do documentation work on `development` or a feature branch/worktree. Do not edit directly on protected branches.

## Documentation Model

Use the docs the repo already has. When docs are missing or only placeholders, establish a practical baseline under `docs/`.

Recommended baseline:

- `README.md` - project purpose, setup, common commands, and navigation
- `docs/REQUIREMENTS.md` - user-visible behavior and non-functional requirements
- `docs/ARCHITECTURE.md` - major components, boundaries, data flow, storage, and integrations
- `docs/RUNBOOK.md` - local setup, environment variables, deploy, rollback, logs, and operations
- `docs/SECURITY.md` - authentication, authorization, secret handling, trust boundaries, and reporting
- `docs/decisions/` - durable architecture or workflow decisions
- `docs/solutions/` - reusable fixes, patterns, and lessons worth finding later

Only create files that are useful for the repo. Avoid boilerplate that cannot be grounded in code, configuration, or devlog history.

## Source Material

Read enough evidence to make factual updates:

- `devlog/*.md` files changed on the branch or created since the target branch diverged
- recent commits, using `git log`, `git diff`, and `git show` when Git is available
- README and existing `docs/`
- package manifests, dependency files, and command definitions
- app entry points, routes, APIs, CLIs, and tests
- environment examples, scripts, CI workflows, and deployment config
- auth, authorization, secret handling, external service clients, and validation code
- task files or planning notes when they explain intent that code alone does not show

If Git is unavailable, use the available filesystem state and devlog files, then document the limitation.

## Workflow

1. Inspect branch safety and the current working tree.
2. Identify the docs that already exist and whether they are established or placeholder-only.
3. Identify the change range:
   - for branch work, compare against `development` or the intended merge base
   - for pre-promotion work, compare `development` against the protected target branch when available
   - when no range is available, read recent devlog files and representative project files
4. Decide whether this is a backfill or maintenance pass.
5. Update only the docs needed to make the repository accurate.
6. Preserve human-written sections unless they are stale or contradicted by current evidence.
7. Mark uncertain claims with HTML TODO comments instead of guessing.
8. Run the lightest validation that fits the change, usually docs rendering, link checks, markdown linting, or targeted inspection.
9. Summarize docs changed, evidence used, validation, and remaining TODOs.

## Backfill Mode

Use backfill mode when docs are missing, empty, or mostly placeholders.

Read the repo shape first:

- stack indicators such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, or framework config
- top-level source directories such as `app/`, `pages/`, `src/`, `lib/`, `api/`, `routes/`, or `services/`
- app or CLI entry points
- database, storage, queue, auth, and integration code
- `.env.example`, deploy config, CI workflows, scripts, and test commands

Write concise first-pass docs that are grounded in visible files. Use TODO comments for product intent, ownership, URLs, contacts, or operational details that the repo does not reveal.

## Maintenance Mode

Use maintenance mode when docs already contain useful project-specific content.

Start with the newest relevant devlog files and commits. For each change, decide whether docs need updates:

- Behavior changed: update requirements, README usage, API docs, or user workflow docs.
- Components changed: update architecture diagrams, component tables, data flow, or integration notes.
- Setup changed: update install, commands, environment variables, or local run steps.
- Deployment or operations changed: update runbook deploy, rollback, monitoring, logs, or incident notes.
- Security changed: update auth, authorization, secret handling, trust boundaries, or vulnerability reporting.
- Reusable lesson discovered: add or update a focused solution note.
- Durable tradeoff made: add or update a decision record.

Do not rewrite established docs wholesale when a narrow patch is enough.

## Pre-Promotion Check

Before pushing or promoting `development` to protected branches:

1. Confirm the work is on `development` or a non-protected branch.
2. Review devlog files and commits since the last promotion or since the target branch diverged.
3. Check whether all user-facing, operational, architectural, setup, and security changes are reflected in docs.
4. Resolve stale TODOs that block promotion, or record why they are acceptable to carry forward.
5. Report whether docs are ready for promotion.

This skill does not perform the push or promotion by itself.

## Content Standards

- Prefer concrete paths, commands, and config names over generic prose.
- Keep docs short enough to scan, but complete enough for the next agent session or maintainer to act.
- Distinguish observed facts from inferred intent.
- Do not invent integrations, URLs, contacts, owners, service levels, or policies.
- Do not move or rename docs unless the existing layout is clearly broken.
- Do not claim validation passed unless it actually ran.

## Expected Output

End with:

- branch or worktree status
- docs created or changed
- evidence used, including devlog files or commit range when available
- validation performed or why it was skipped
- unresolved TODOs or risks
- whether docs are ready for merge or protected-branch promotion
