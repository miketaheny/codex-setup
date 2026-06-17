---
name: af-migrate-backlog-devlog
description: Migrate legacy Backlog.md, triage.md, backlog/, or .backlog task files into Agent-Flow devlog/ Markdown entries. Use when a repo is leaving Backlog-style task tracking, when task history needs to be preserved as devlog records, or when backlog/task files should be converted before removing Backlog tooling.
---

# AF Migrate Backlog Devlog Skill

## Overview

Use this skill to preserve planning and task history while moving a repository from Backlog-style task stores to Agent-Flow `devlog/` entries.

## Safety Rules

- Dry-run first.
- Do not delete `Backlog.md`, `triage.md`, `backlog/`, or `.backlog/` files unless the user explicitly approves deletion after reviewing the migrated output.
- Preserve source paths in every generated devlog entry.
- Do not claim a task was completed unless the source says it was completed.
- If source metadata is incomplete, write `unknown` instead of guessing.

## Workflow

### 1. Inventory sources

Look for:

- `Backlog.md`
- `triage.md`
- `backlog/tasks/*.md`
- `backlog/drafts/*.md`
- `.backlog/tasks/*.md`
- `.backlog/drafts/*.md`
- any user-provided task file or directory

Summarize the count of files by source type before writing anything.

### 2. Run a dry-run conversion

Use the bundled helper:

```bash
python3 <this-skill-dir>/scripts/migrate_backlog_to_devlog.py /path/to/repo
```

The helper defaults to dry-run mode and prints the devlog files it would create.

To target explicit files or directories:

```bash
python3 <this-skill-dir>/scripts/migrate_backlog_to_devlog.py /path/to/repo --source Backlog.md --source .backlog/tasks
```

### 3. Review the plan

Check for:

- duplicate or unclear task titles
- tasks marked `In Progress` or `To Do` that should remain open
- source files that are sensitive or should not be copied into devlog
- generated filenames that collide with existing devlog entries

Ask the user before proceeding if migration would duplicate a large amount of history or expose sensitive planning notes.

### 4. Write devlog entries

After review:

```bash
python3 <this-skill-dir>/scripts/migrate_backlog_to_devlog.py /path/to/repo --write
```

Generated entries go to `devlog/` by default. The helper refuses to overwrite existing files.

### 5. Validate

Run:

```bash
git status --short
find devlog -maxdepth 1 -type f | sort
rg -n "Source Backlog|Task status|Migrated from" devlog
```

Manually spot-check at least one completed task and one incomplete task when both exist.

### 6. Cleanup only after approval

If the user approves removing the legacy task store:

1. Confirm migrated entries exist.
2. Confirm no active workflow still references the legacy files.
3. Delete only the approved files.
4. Add a devlog entry describing the removal.

## Migration Format

Each generated devlog entry should include:

- source path
- task id, title, status, priority, created and updated dates when present
- branch/worktree if known
- goal or source description
- summarized acceptance criteria and definition of done
- implementation plan and notes when present
- validation or review information when present
- follow-ups for incomplete tasks

## Expected Output

End with:

- sources scanned
- entries created or planned
- entries skipped and why
- validation performed
- whether legacy files were left in place or removed with approval
