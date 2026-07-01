# Agent-Flow Demo Plan

Use this as a script for a live demo, screen recording, or annotated walkthrough.

## Goal

Show how Agent-Flow turns a Git repo into an agent-ready workspace with shared instructions, isolated session worktrees, mandatory devlog history, review, and release readiness.

## Setup

Prepare:

- this setup repo
- a temporary sample Git repo on `development`
- terminal with readable font size

## Script

### 1. Install

```bash
./scripts/install.sh
```

Show:

```bash
find ~/.agent-flow -maxdepth 2 -type f | sort
find ~/.codex/skills -maxdepth 2 -name SKILL.md | sort
ls ~/.codex/fast.config.toml ~/.codex/review.config.toml ~/.codex/deep.config.toml
test -f ~/.claude/CLAUDE.md && echo "Claude adapter installed"
```

### 2. Initialize A Sample Repo

```bash
mkdir /tmp/agent-flow-demo
cd /tmp/agent-flow-demo
git init -b development
~/.agent-flow/scripts/init-repo.sh --yes --staging
```

Show `AGENT-FLOW.md`, `AGENTS.md`, `CLAUDE.md`, `.agent-flow/config.toml`, `.git/hooks/pre-push`, `devlog/README.md`, and `docs/decisions/000-template.md`.

For a Node sample repo with `package.json`, mention that init offers pnpm onboarding. Use `--no-pnpm` to skip it or `--pnpm` to rerun the pnpm step later.

### 3. Explain The Lifecycle

```text
af-flow -> implementation -> af-devlog -> af-finish
```

Release:

```text
af-reconcile -> af-full-review -> af-release
```

Mention `af-show` for visual/manual proof and `af-security-review` for sensitive or configured security gates, including Codex Security diff scans when available.

Show `af-help` as the read-only command map. Mention `af-pnpm` for package-manager standardization, `docs/CODEX-MODEL-POLICY.md` for speed/token profile choices, `af-feature-audit` as a manual-only app-wide feature/user-story QA campaign, and `af-brand-guidelines -> af-ui-audit` as the manual brand/UI review campaign.

### 4. Demonstrate A Session

```bash
~/.agent-flow/scripts/start-session.sh docs demo-copy
cd ../agent-flow-demo-demo-copy
```

Show metadata:

```bash
git config --worktree --get agentFlow.parent
git config --worktree --get agentFlow.sessionName
git config --worktree --get agentFlow.state
```

Make a small docs change and devlog entry, then run:

```bash
~/.agent-flow/scripts/finish-session.sh
```

Show `ASK_USER_MERGE`.

### 5. Demonstrate Worktree Readiness

```bash
~/.agent-flow/scripts/worktree-manager.py
~/.agent-flow/scripts/check-push-readiness.sh development
```

Show how open child sessions block parent pushes until merged or explicitly handled.

### 6. Demonstrate Backlog Migration

Create a sample legacy Backlog file, then run:

```bash
python3 ~/.agent-flow/skills/af-migrate-backlog-devlog/scripts/migrate_backlog_to_devlog.py .
python3 ~/.agent-flow/skills/af-migrate-backlog-devlog/scripts/migrate_backlog_to_devlog.py . --write
```

Show the generated devlog entry.

## Screenshot List

- install output
- generated home directories
- initialized repo files
- generated config
- session start output
- finish output with `ASK_USER_MERGE`
- worktree manager output
- push-readiness output
- backlog migration output

## Recording Notes

Keep the first demo under three minutes. Use real terminal output as the primary visual.
