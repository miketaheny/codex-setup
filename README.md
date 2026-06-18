# AF Agent-Flow Global Setup

A clean Agent-Flow setup for solo development with Claude, Codex, and other coding agents: shared instructions, Codex-compatible skills, session worktrees, finish-time devlog files, project documentation maintenance, review gates, formal protected-branch security review, and optional heavier workflows.

## What this gives you

- A canonical `AGENT-FLOW.md` with first-contact, branch safety, worktree, and documentation rules.
- Adapter files for agent-specific entrypoints:
  - `AGENTS.md` for Codex-compatible agents.
  - `CLAUDE.md` for Claude-compatible agents.
- AF skills for repeatable workflows:
  - `af-small-change`
  - `af-worktree-task`
  - `af-review-gate`
  - `af-security-review`
  - `af-devlog`
  - `af-docs`
  - `af-migrate-backlog-devlog`
  - `af-reconcile-worktrees`
  - `af-push-staging`
  - `af-compound-mode`
- Scripts for repo initialization, common safety checks, worktrees, and repo bootstrapping.
- Lifecycle helpers for chat-to-worktree session start, finish/merge readiness, push readiness, and optional local hooks.
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

## Per-repo init

Inside a Git repository:

```bash
~/.agent-flow/scripts/init-repo.sh
```

Init runs the bootstrap step, then records local repo choices in `.agent-flow/config.toml`:

- whether Agent-Flow enforcement is enabled or locally disabled
- that session worktrees are detached from the checked-out parent branch by default and merge back there
- that named branches are created only when the user explicitly requests a branch
- that file-changing chats require AF session worktrees
- that dirty worktrees are reviewed, devlogged, and committed instead of being left loose
- that agents ask before merging by default
- that formal security review is required before pull requests to `staging` or `main`
- `development` as the SDLC integration branch
- `main` as the production PR target, not a local work branch
- whether optional `staging` is used between `development` and `main`
- `staging` as a local branch only when staging is enabled
- `main`, configured `staging`, and reserved branch names as protected from direct agent edits
- whether to install a local pre-push hook for child worktree readiness checks
- a non-destructive `.gitignore` Agent-Flow block for local config, env files, OS/editor noise, logs, temp files, and personal IDE state

When staging is disabled, init notes that in the repo-local `AGENTS.md` and `CLAUDE.md` adapters so agents do not assume a staging branch.

Agent-Flow ignores IDE folders by default but allows curated shared VS Code files. Commit `.vscode/extensions.json`, `.vscode/tasks.json`, `.vscode/launch.json`, or `.vscode/settings.json` only when they encode project tooling. Do not commit personal IDE preferences such as themes, window titles, UI layout, local paths, or machine-specific interpreter paths.

## Per-repo bootstrap

Inside a Git repository:

```bash
~/.agent-flow/scripts/bootstrap-repo.sh
```

Bootstrap only creates missing repo files:

- `AGENT-FLOW.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.gitignore` Agent-Flow block
- `devlog/README.md`
- `docs/decisions/`
- `docs/solutions/`
- `docs/plans/`
- `docs/diagrams/`
- `docs/assets/`
- `docs/presentations/`

It will not overwrite existing files or record first-contact choices. Prefer `init-repo.sh` for new repos.

## Documentation Map

- [Changelog](CHANGELOG.md) - user-facing workflow, docs, skill, and setup changes.
- [Documentation Strategy](docs/DOCS-STRATEGY.md) - how `af-docs` owns ongoing docs maintenance, interview setup, visuals, and validation.
- [Workflow](docs/WORKFLOW.md) - branch model, daily loop, migration, and release promotion.
- [Architecture](docs/ARCHITECTURE.md) - system map, install flow, init/bootstrap flow, and skill routing diagrams.
- [User Guide](docs/USER-GUIDE.md) - install, init, skill selection, migration, visual docs, and release promotion.
- [Visual Plan](docs/VISUALS.md) - diagram inventory, screenshot checklist, demo video plan, and content recommendations.
- [Demo Plan](docs/DEMO.md) - live demo and recording script.
- [Pitch](docs/PITCH.md) - positioning, value props, objections, and marketing recommendations.
- [Prompt Examples](docs/AGENT-PROMPTS.md) - reusable prompts for Agent-Flow work.

## Recommended Daily Usage

### Small fix

```text
Use af-small-change to fix this in one AF worktree session. Keep scope narrow and add/update the devlog under devlog/ before finish.
```

### Worktree session

```text
Use af-worktree-task. Create or adopt one isolated AF worktree session from the checked-out parent branch, then implement, document, validate, and review.
```

### Seamless session lifecycle

```text
Use Agent-Flow for this change. Create one session worktree, finish with readiness checks, then ask me whether to merge back to the parent branch.
```

### Review before merge

```text
Use af-review-gate and tell me whether this session worktree is ready to merge into its recorded parent branch.
```

### Formal security review

```text
Use af-security-review. Review development against staging, or staging/development against main, before creating a protected-branch pull request.
```

### Detailed documentation after a change

```text
Use af-devlog to add or update the finish-time session devlog entry under devlog/.
```

Devlog filenames use `YYYY-MM-DD-<commit-subject-slug>.md`. They are date and subject based, not SHA based; the commit SHA belongs inside the file when known.

### Project docs maintenance

```text
Use af-docs to update project docs from the latest devlog entries and commits before promoting development through the release path.
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
Use af-reconcile-worktrees to open the worktree manager, pick up incomplete work, and clean up completed worktrees before release promotion.
```

### Push readiness

```text
Run scripts/check-push-readiness.sh for this branch before pushing. Tell me which child worktrees, if any, still need to be merged or cleaned.
```

### Release promotion

```text
Use af-push-staging to reconcile worktrees, validate development, run formal security review, and promote through the configured release path. If staging is enabled, use development -> staging -> main. If staging is disabled, offer a development-to-main PR.
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
