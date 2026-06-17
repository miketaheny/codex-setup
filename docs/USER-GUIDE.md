# Agent-Flow User Guide

This guide covers the common workflows for installing Agent-Flow, initializing a repo, and choosing the right AF skill.

## Install Agent-Flow

From the setup repo:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

The installer writes:

- shared Agent-Flow files to `~/.agent-flow`
- Codex adapter and skills to `~/.codex`
- Claude adapter to `~/.claude`

Use environment variables when you need custom install locations:

```bash
AF_HOME=/path/to/agent-flow CODEX_HOME=/path/to/codex CLAUDE_HOME=/path/to/claude ./scripts/install.sh
```

## Initialize a Project Repo

Inside a target Git repo:

```bash
~/.agent-flow/scripts/init-repo.sh
```

Init creates missing bootstrap files, then records local choices in `.agent-flow/config.toml`:

- `AGENT-FLOW.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.agent-flow/config.toml`
- `devlog/README.md`
- `docs/decisions/000-template.md`
- `docs/solutions/`
- `docs/plans/`
- `docs/diagrams/`
- `docs/assets/`
- `docs/presentations/`

The script asks whether to disable Agent-Flow enforcement for this repo, whether the repo uses optional `staging`, and whether to install a local pre-push hook. It also creates or appends a non-destructive Agent-Flow `.gitignore` block. If staging is disabled, the local agent adapters note that agents should not assume a staging branch.

Use `bootstrap-repo.sh` only when you want to copy missing files without recording first-contact repo choices.

Gitignore and IDE defaults:

- `.gitignore` should ignore local Agent-Flow overrides, env files, OS/editor noise, logs, temp files, and personal IDE state.
- `.vscode/extensions.json`, `.vscode/tasks.json`, `.vscode/launch.json`, and `.vscode/settings.json` may be committed only when they encode shared project tooling.
- Personal IDE preferences such as themes, window titles, UI layout, local paths, or machine-specific interpreters should stay untracked.

Branch defaults:

- Task worktrees branch from the checked-out parent branch and merge back there.
- File-changing prompts use task worktrees.
- Agents ask before merge by default.
- `development` is the SDLC integration branch.
- `main` is production and agents must not edit it directly.
- `staging` is optional in the release path, and direct edits to a branch named `staging` are blocked.
- `master`, `production`, and `prod` are reserved legacy branch names.

## Daily Agent-Flow Loop

```mermaid
flowchart LR
    Prompt["User prompt"] --> Classify["Classify chat/tiny/normal/large"]
    Classify --> Branch["Create task worktree for changes"]
    Branch --> Skill["Use lightest AF skill"]
    Skill --> Change["Implement scoped change"]
    Change --> Validate["Run validation"]
    Validate --> Devlog["Add devlog entry"]
    Devlog --> Docs["Update docs and visuals if needed"]
    Docs --> Review["Run af-review-gate"]
    Review --> Ask["Ask whether to merge"]
    Ask --> Merge["Merge to parent branch after approval"]
    Merge --> PushCheck["Check child worktrees before push"]
```

## Choose a Skill

| Need | Skill |
|---|---|
| Tiny code or docs fix | `af-small-change` |
| Parallel isolated work | `af-worktree-task` |
| Engineering history | `af-devlog` |
| Project docs, diagrams, guides, demos, decks, or marketing content | `af-docs` |
| Convert legacy Backlog task files to devlog entries | `af-migrate-backlog-devlog` |
| Review before merge | `af-review-gate` |
| Audit worktrees and branch cleanup candidates | `af-reconcile-worktrees` |
| Promote `development` through release path | `af-push-staging` |
| Decide whether a heavier workflow is needed | `af-compound-mode` |

## Start And Finish A Task

Use the lifecycle helpers directly when working outside a skill:

```bash
scripts/start-task.sh --class normal feat export-csv
```

At the end of the task worktree:

```bash
scripts/finish-task.sh
```

If it reports `ASK_USER_MERGE`, ask before merging. After approval:

```bash
scripts/finish-task.sh --merge
```

For large or risky work from `development`, ask whether to create a feature parent branch first:

```bash
scripts/start-task.sh --class large --create-parent feat/payments feat payment-form
```

## Migrate Legacy Backlog Files

Dry-run first:

```bash
python3 ~/.agent-flow/skills/af-migrate-backlog-devlog/scripts/migrate_backlog_to_devlog.py /path/to/repo
```

Write devlog entries after reviewing the plan:

```bash
python3 ~/.agent-flow/skills/af-migrate-backlog-devlog/scripts/migrate_backlog_to_devlog.py /path/to/repo --write
```

Do not delete legacy Backlog files until the generated devlog entries are reviewed.

## Create Visual Docs

Use `af-docs` when the repo needs to be easier to understand or present.

Good defaults for Agent-Flow repos:

- Mermaid diagrams for architecture and workflows.
- Markdown guides for developer/operator instructions.
- Presentation outlines before building slide decks.
- Demo scripts and screenshot lists before recording videos.
- Generated images only for marketing or conceptual visuals when real product screenshots are not available.

## Promote Development

Use this sequence:

```text
af-reconcile-worktrees -> af-docs -> af-push-staging
```

The flow checks worktree state, updates docs, and validates `development`. With staging enabled, it merges to `staging`, pushes `development` and `staging`, and asks before creating a `staging` to `main` pull request. With staging disabled, it pushes `development` and asks before creating a `development` to `main` pull request.

Before pushing any parent branch, run:

```bash
scripts/check-push-readiness.sh <branch>
```

Init can install the local hook. To install or refresh it later:

```bash
scripts/install-hooks.sh
```
