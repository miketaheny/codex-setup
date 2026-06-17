---
name: af-devlog
description: Maintain per-commit Markdown devlog files under devlog/ for Agent-Flow work.
---

# AF Devlog Skill

Use this skill whenever a task needs engineering-history documentation, cleanup, or review.

## Purpose

Keep detailed engineering history close to the commit that introduced it while avoiding shared-file conflicts across branches and worktrees.

## Devlog folder

`devlog/` is the detailed engineering journal.

Add one Markdown file for every meaningful commit. If a branch will be squashed before merge, create one file for the planned squash commit.

Suggested filename:

```text
devlog/YYYY-MM-DD-<commit-subject-slug>.md
```

Use a concise slug based on the commit subject or planned squash subject. A branch with multiple meaningful commits should have multiple devlog files.

## Entry Template

```md
# YYYY-MM-DD — <commit subject>

- Branch/worktree: `<branch>` / `<path if relevant>`
- Commit: `<short SHA>` or `pending`
- Goal: <what the change tried to accomplish>
- Summary:
  - <what changed>
- Files changed:
  - `<file>` — <reason>
- Decisions:
  - <decision and why>
- Validation:
  - `<command>` — <result>
- Review:
  - <review result or not run>
- Risks / follow-ups:
  - <none or items>
```

## Rules

- Create the devlog file before committing so the file travels with the branch or worktree.
- Do not rewrite unrelated devlog files from other tasks.
- If the final commit SHA is unknown at commit time, leave `Commit: pending`. A later docs maintenance pass may update it when useful.
- Do not claim tests passed unless they were run.
- Keep entries concise but useful for future agent sessions.
- Record skipped validation and known risks explicitly.
