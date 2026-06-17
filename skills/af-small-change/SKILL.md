---
name: af-small-change
description: Fast, safe workflow for tiny and small code changes that still enforces branch safety, scoped edits, devlog updates, and validation.
---

# AF Small Change Skill

Use this skill when the user wants a small fix, obvious bug repair, CSS tweak, config correction, typo fix, or narrow code change.

## Goal

Move fast without losing discipline.

## Required behavior

1. Read applicable agent instruction files such as `AGENT-FLOW.md`, `AGENTS.md`, and `CLAUDE.md`.
2. Check git state:
   - current branch
   - dirty files
   - whether branch is protected
3. If on `main`, `master`, `staging`, `production`, or `prod`, do not edit directly.
4. Prefer a feature branch from `development` for implementation.
5. Keep the change narrow.
6. Avoid unrelated refactors.
7. Add a devlog file under `devlog/` for meaningful changes.
8. Run the smallest relevant validation command available.
9. Summarize what changed, validation, docs updated, and remaining risks.

## Branch handling

If already on a safe feature branch, continue there.

If on `development`, create a branch:

```bash
git switch -c fix/<short-description>
```

If on a protected branch, switch to `development` first or ask the user if `development` does not exist.

## Validation preference

Choose the most relevant available command:

- targeted test
- lint
- typecheck
- build
- existing package script
- manual inspection when no test exists

Document skipped validation honestly.

## Devlog entry format

Create one Markdown file under `devlog/` for the commit or planned squash commit:

```md
# YYYY-MM-DD — <commit subject>

- Branch/worktree: `<branch>` / `<path if relevant>`
- Commit: `pending`
- Goal: <goal>
- Files changed:
  - `<file>` — <why>
- Decisions:
  - <decision>
- Validation:
  - <command/result or not run reason>
- Review:
  - <summary or not applicable>
- Follow-ups:
  - <none or item>
```

## Done response

End with:

- branch
- files changed
- validation result
- devlog status
- docs status
- whether ready for review or merge
