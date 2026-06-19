---
name: af-devlog
description: Maintain mandatory session Markdown devlog files under devlog/ for every file-changing Agent-Flow session. Use when starting, finishing, reviewing, reconciling, or documenting AF work so the human history travels with the session commit.
---

# AF Devlog

## Purpose

Use `devlog/` as the durable human history for Agent-Flow. Metadata is only lightweight routing; devlog entries explain what happened, why, and how it was validated.

## Requirement

Every file-changing AF session must add or update one Markdown file under `devlog/` before the session commit. Do not merge a session without a devlog entry unless the work produced no repository changes.

Suggested filename:

```text
devlog/YYYY-MM-DD-<commit-subject-slug>.md
```

Use the planned commit subject or squash subject for the slug. A branch with multiple meaningful commits may have multiple devlog files.

## Entry Template

```md
# YYYY-MM-DD - <commit subject>

- Branch/worktree: `<branch or detached short SHA>` / `<path if relevant>`
- Commit: `<short SHA>` or `pending`
- Goal: <what the change tried to accomplish>
- Summary:
  - <what changed>
- Files changed:
  - `<file>` - <reason>
- Decisions:
  - <decision and why>
- Validation:
  - `<command>` - <result>
- Visual/manual proof:
  - <not applicable, passed, blocked, or skipped with reason>
- Review:
  - <review result or not run>
- Risks / follow-ups:
  - <none or items>
```

## Rules

- Create the devlog file before committing so it travels with the session changes.
- Do not rewrite unrelated devlog files from other sessions.
- Leave `Commit: pending` when the final SHA is unknown at commit time.
- Do not claim tests, builds, browser checks, or security checks passed unless they ran.
- Record skipped validation, blocked proof, and known risks explicitly.
- Keep entries concise but useful for future agents and maintainers.
