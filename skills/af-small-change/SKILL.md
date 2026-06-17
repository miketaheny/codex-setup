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
3. If on `main`, `staging`, `master`, `production`, or `prod`, do not edit directly.
4. Use a task worktree from the checked-out user-controlled parent branch.
5. Keep the change narrow.
6. Avoid unrelated refactors.
7. Add a devlog file under `devlog/` for meaningful changes.
8. Run the smallest relevant validation command available.
9. Summarize what changed, validation, docs updated, and remaining risks.

## Branch handling

If already in a safe task worktree, continue there.

If on a user-controlled parent branch such as `development` or `feat/<name>`, create a task worktree:

```bash
scripts/start-task.sh --class tiny fix <short-description>
```

If `scripts/start-task.sh` is unavailable, use `scripts/new-worktree.sh fix <short-description>` and record `agentFlowTaskClass = tiny` manually.

If on a protected or reserved branch, ask the user to check out the intended parent branch first. Do not branch from `main` or `staging`.

## Finish behavior

At the end, run the finish helper when available:

```bash
scripts/finish-task.sh
```

If it reports `ASK_USER_MERGE`, ask whether to merge back to the parent branch. Automatic merge is allowed only when repo config sets `auto_merge = "tiny-only"` or stronger and all readiness checks pass.

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
