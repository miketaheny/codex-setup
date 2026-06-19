---
name: af-small-change
description: Fast, safe workflow for small file changes inside one Agent-Flow worktree session, with branch safety, scoped edits, finish-time devlog, and validation.
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
4. Use an AF session worktree from the checked-out user-controlled parent branch.
5. Keep the change narrow.
6. Avoid unrelated refactors.
7. Add or update a devlog file under `devlog/` before the session commit.
8. Run the smallest relevant validation command available.
9. Summarize what changed, validation, docs updated, and remaining risks.

## Branch handling

If already in a safe AF session worktree, continue there only when the request matches that session's direction.

If on a user-controlled parent branch such as `development` or `feat/<name>`, create a session worktree:

```bash
scripts/start-session.sh fix <short-description>
```

If `scripts/start-session.sh` is unavailable, use `scripts/new-worktree.sh fix <short-description>` and record `agentFlow.kind = session` plus `agentFlow.parent` in worktree-local config manually if needed.

If on a protected or reserved branch, ask the user to check out the intended parent branch first. Do not branch from `main` or `staging`.

Named branches are not the default. Create one only when the user explicitly asks for a branch, for example with `scripts/start-session.sh --branch fix/<short-description> fix <short-description>`.

## Finish behavior

At the end, run the finish helper when available:

```bash
scripts/finish-session.sh
```

If it reports `ASK_USER_MERGE`, ask whether to merge back to the parent branch. Automatic merge is only for repos that explicitly opt into it and all readiness checks pass.

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

Create one Markdown file under `devlog/` for the session commit or planned squash commit:

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
