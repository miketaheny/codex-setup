# AF Agent-Flow Global Setup

A clean Agent-Flow setup for solo development with Claude, Codex, and other coding agents: shared instructions, Codex-compatible skills, git worktrees, per-commit devlog files, project documentation maintenance, review gates, and optional heavier workflows.

## What this gives you

- A canonical `AGENT-FLOW.md` with branch safety and documentation rules.
- Adapter files for agent-specific entrypoints:
  - `AGENTS.md` for Codex-compatible agents.
  - `CLAUDE.md` for Claude-compatible agents.
- AF skills for repeatable workflows:
  - `af-small-change`
  - `af-worktree-task`
  - `af-review-gate`
  - `af-devlog`
  - `af-docs`
  - `af-migrate-backlog-devlog`
  - `af-reconcile-worktrees`
  - `af-push-staging`
  - `af-compound-mode`
- Scripts for common safety checks and repo bootstrapping.
- Templates for repo-level `AGENT-FLOW.md`, agent adapters, `devlog/`, and decision records.

## Install

From this folder:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

The installer writes the shared setup to `~/.agent-flow` by default. It also installs Codex-compatible adapters and skills to `~/.codex`, and a Claude adapter to `~/.claude`.

Override locations with:

```bash
AF_HOME=/path/to/agent-flow CODEX_HOME=/path/to/codex CLAUDE_HOME=/path/to/claude ./scripts/install.sh
```

## Manual install

```bash
mkdir -p ~/.agent-flow ~/.codex ~/.claude
mkdir -p ~/.agent-flow/skills ~/.agent-flow/templates ~/.agent-flow/scripts ~/.agent-flow/docs ~/.codex/skills
cp AGENT-FLOW.md ~/.agent-flow/AGENT-FLOW.md
cp AGENTS.md ~/.codex/AGENTS.md
cp AGENT-FLOW.md ~/.codex/AGENT-FLOW.md
cp CLAUDE.md ~/.claude/CLAUDE.md
cp AGENT-FLOW.md ~/.claude/AGENT-FLOW.md
cp -R skills/. ~/.agent-flow/skills/
cp -R templates/. ~/.agent-flow/templates/
cp -R scripts/. ~/.agent-flow/scripts/
cp -R docs/. ~/.agent-flow/docs/
cp -R skills/. ~/.codex/skills/
```

## Per-repo bootstrap

Inside a Git repository:

```bash
~/.agent-flow/scripts/bootstrap-repo.sh
```

This creates missing repo files:

- `AGENT-FLOW.md`
- `AGENTS.md`
- `CLAUDE.md`
- `devlog/README.md`
- `docs/decisions/`
- `docs/solutions/`
- `docs/plans/`
- `docs/diagrams/`
- `docs/assets/`
- `docs/presentations/`

It will not overwrite existing files.

## Documentation Map

- [Changelog](CHANGELOG.md) - user-facing workflow, docs, skill, and setup changes.
- [Documentation Strategy](docs/DOCS-STRATEGY.md) - how `af-docs` owns ongoing docs maintenance, interview setup, visuals, and validation.
- [Workflow](docs/WORKFLOW.md) - branch model, daily loop, migration, and staging promotion.
- [Architecture](docs/ARCHITECTURE.md) - system map, install flow, bootstrap flow, and skill routing diagrams.
- [User Guide](docs/USER-GUIDE.md) - install, bootstrap, skill selection, migration, visual docs, and staging usage.
- [Visual Plan](docs/VISUALS.md) - diagram inventory, screenshot checklist, demo video plan, and content recommendations.
- [Demo Plan](docs/DEMO.md) - live demo and recording script.
- [Pitch](docs/PITCH.md) - positioning, value props, objections, and marketing recommendations.
- [Prompt Examples](docs/AGENT-PROMPTS.md) - reusable prompts for Agent-Flow work.

## Recommended Daily Usage

### Tiny fix

```text
Use af-small-change to fix this. Keep scope narrow and add a devlog entry under devlog/.
```

### Worktree task

```text
Use af-worktree-task. Create an isolated worktree from development for this task, then implement, document, and review.
```

### Review before merge

```text
Use af-review-gate and tell me whether this branch is ready to merge into development.
```

### Detailed documentation after a change

```text
Use af-devlog to add a per-commit devlog entry under devlog/.
```

### Project docs maintenance

```text
Use af-docs to update project docs from the latest devlog entries and commits before promoting development.
```

### Existing docs stewardship

```text
Use af-docs to run a one-time in-depth interview for this repo's existing docs, update useful docs in place, and write docs/DOCS-STRATEGY.md so future changes can be maintained from evidence without repeating the full interview.
```

### Visual docs and content

```text
Use af-docs to recommend and create diagrams, user guides, demo plans, presentations, screenshots, and marketing content for this project.
```

### Backlog migration

```text
Use af-migrate-backlog-devlog to convert Backlog.md, backlog/, or .backlog task files into devlog entries before removing old task stores.
```

### Worktree reconciliation

```text
Use af-reconcile-worktrees to audit worktrees, branches, and agent instruction conflicts before cleanup or staging promotion.
```

### Staging promotion

```text
Use af-push-staging to reconcile worktrees, validate development, merge development into staging, and offer a staging-to-main PR.
```

### Bigger/riskier work

```text
Use af-compound-mode to decide whether this should use a light Agent-Flow skill or a heavier planning/review workflow, then proceed with the lightest safe option.
```

## Codex-Specific Notes

The `skills/` directory uses the Codex skill format, and `agents/openai.yaml` files are Codex/OpenAI UI metadata. Other agents can still read the `SKILL.md` files as workflow instructions or adapt them into their own command format.

Compound Engineering is optional and Codex-specific in this package. Install it separately if desired:

```bash
codex plugin marketplace add EveryInc/compound-engineering-plugin
bunx @every-env/compound-plugin install compound-engineering --to codex
codex
```

Inside Codex, run:

```text
/plugins
```

Then install/activate Compound Engineering and restart Codex.

## Intended Behavior

Agent-Flow treats heavier planning/review workflows as optional power mode. The non-negotiable workflow rules live in `AGENT-FLOW.md`; `AGENTS.md` and `CLAUDE.md` are adapters so different agents enter the same workflow.

Use the custom AF skills for speed and consistency on daily solo-dev work. Use heavier workflows only when the task needs broader context, deeper review, or multi-agent coordination.
