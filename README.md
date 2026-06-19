# AF Agent-Flow Global Setup

Portable Agent-Flow setup for solo development with Codex, Claude, and other coding agents.

## What It Installs

- Canonical workflow rules in `AGENT-FLOW.md`.
- Agent adapters: `AGENTS.md` for Codex-compatible agents and `CLAUDE.md` for Claude-compatible agents.
- Compact AF skills:
  - `af-flow`
  - `af-status`
  - `af-devlog`
  - `af-finish`
  - `af-show`
  - `af-review`
  - `af-reconcile`
  - `af-full-review`
  - `af-release`
  - `af-security-review`
  - `af-docs`
  - `af-migrate-backlog-devlog`
- Scripts for install, repo init, session lifecycle, branch safety, push readiness, hooks, and worktree management.
- Templates for repo instructions, config, devlog entries, gitignore blocks, and decision records.

## Install

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

Default destinations:

- `~/.agent-flow` for shared AF files
- `~/.codex` for Codex adapter, skills, scripts, docs, and templates
- `~/.claude` for Claude adapter

Override locations:

```bash
AF_HOME=/path/to/agent-flow CODEX_HOME=/path/to/codex CLAUDE_HOME=/path/to/claude ./scripts/install.sh
```

Reinstalling removes retired AF skill and script names from the install targets before copying the current compact set.

## Initialize A Repo

Inside a Git repository:

```bash
~/.agent-flow/scripts/init-repo.sh
```

Init creates missing AF files and writes `.agent-flow/config.toml` with local choices:

- enforcement enabled or disabled
- session worktrees required for file-changing work
- detached session worktrees by default
- named branches only when explicitly requested
- ask-before-merge
- devlog required for file-changing sessions
- checked-out parent branch as the merge target
- `development` as integration branch
- optional `staging` between `development` and `main`
- protected/reserved branch policy
- optional pre-push hook for child session readiness

## Daily Loop

For file-changing work:

```text
af-flow -> implement -> af-devlog -> af-finish
```

For read-only repo and worktree status:

```text
af-status
```

Direct helpers:

```bash
scripts/start-session.sh feat export-csv
scripts/finish-session.sh
scripts/finish-session.sh --merge
```

`finish-session.sh` reports `ASK_USER_MERGE`; run `--merge` only after approval.

Create a named branch only on request:

```bash
scripts/start-session.sh --branch feat/export-csv feat export-csv
```

## Release Loop

```text
af-reconcile -> af-full-review -> af-release
```

Run `af-security-review` when requested, config-required, or security-sensitive.

Default release path is `development -> staging -> main`. With staging disabled or explicitly skipped, use `development -> main`.

## Documentation

- [Workflow](docs/WORKFLOW.md)
- [User Guide](docs/USER-GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Prompt Examples](docs/AGENT-PROMPTS.md)
- [Documentation Strategy](docs/DOCS-STRATEGY.md)
- [Visual Plan](docs/VISUALS.md)
- [Demo Plan](docs/DEMO.md)
- [Pitch](docs/PITCH.md)
- [Changelog](CHANGELOG.md)

## Key Rule

`devlog/` is the durable human history. Git config metadata is intentionally small and exists only so finish, reconcile, and push-readiness can route work safely.
