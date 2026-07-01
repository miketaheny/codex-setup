# Agent-Flow Instructions

Agent-Flow (`AF`) is the Codex workflow for this repo.

## Core Lifecycle

Use one lifecycle:

```text
af-flow -> persistent implementation session -> af-devlog -> af-finish
```

Release work adds:

```text
af-reconcile -> af-full-review -> af-release
```

Run `af-show` during finish when visual or manual proof is useful. Run `af-security-review` only when requested, when repo config requires it, when `af-full-review` flags security-sensitive changes, or when the release touches auth, secrets, input validation, dependencies, infrastructure, privacy, or data access. Prefer the Codex Security diff-scan path when available, falling back to the manual AF checklist only when no security-review tool is available.

`af-finish` is intentionally fast and does not run a full review — it validates, checks devlog/docs, and reports readiness to merge into the session's parent branch. The one mandatory review gate is `af-full-review`, run once as part of the release flow before code reaches `main`. Use `af-review` only as an optional, on-demand quick check mid-session; it is never required.

Use `af-help` for read-only command help and usage-guide routing. Use `af-claude-review` only when the user asks for Claude CLI as an external review pass or when a release/high-risk review explicitly wants a second-model check. Use `af-feature-audit` only when explicitly requested for a whole-app feature register, user-story, test, fix, and retest campaign. Use `af-brand-guidelines` to create or ingest brand/design rules, and `af-ui-audit` only when explicitly requested for a responsive UI/UX audit, fix, and retest campaign.

## Fast Path

Default to the smallest workflow that preserves safety:

```text
continue or create one session worktree -> make the scoped change -> run targeted validation -> write one finish-time devlog -> finish when asked
```

Do not run full audits, broad repo scans, release reviews, security reviews, or visual captures unless the user asks, the change is high-risk, or the evidence says they are needed. Keep the user-facing command set small: `af-flow`, `af-status`, `af-review`, `af-reconcile`, and `af-finish`. Treat specialist skills such as `af-pnpm`, `af-docs`, `af-feature-audit`, and `af-ui-audit` as on-demand tools, not mandatory steps in ordinary sessions.

Use cached local context before rereading large docs. Inside an active session, re-check only the files and instructions relevant to the changed paths unless the user changes direction or the repo state looks inconsistent.

## Codex Model And Effort

For Codex, run a quick effort preflight before meaningful work. Fast workflow does not mean low reasoning: keep the AF process lightweight, but use enough model effort for the task.

Default to `gpt-5.5` with `model_reasoning_effort = "xhigh"` and low verbosity for most development, debugging, refactoring, multi-file docs, browser/computer-use, release, and high-context work.

Downgrade deliberately:

- Use a fast profile or `gpt-5.4-mini` for read-only help, status, command lookup, and lightweight exploration.
- Use base `gpt-5.5` / `medium` for trivial one-file edits, narrow docs copy, formatting, or low-risk config changes.
- Use `gpt-5.5` / `high` for moderate implementation when `xhigh` is unnecessary but low/medium would be brittle.
- Use `gpt-5.5` / `xhigh` for normal development and computer-use work unless the effort preflight clearly chooses a cheaper tier.

See `docs/CODEX-MODEL-POLICY.md` for the profile names and routing table.

## First Contact

When opening a repo:

- Read repo-local `.agent-flow/config.toml`, `AGENT-FLOW.md`, and `AGENTS.md` when present.
- Follow the most specific nested `AGENT-FLOW.md` or adapter file for the path being edited.
- If config says `mode = "disabled"`, disclose that AF is disabled and do not enforce AF in that repo.
- If no AF instructions or config exist, do not do file-changing work until the repo is initialized with `~/.agent-flow/scripts/init-repo.sh` or the user explicitly opts out for that repo. Read-only questions can still be answered directly.
- Read-only chats can answer directly. Any file edit, dependency change, commit, push, config change, or destructive operation must happen in one AF session worktree.
- In Codex, treat a working thread as a persistent AF session. Keep using the same session worktree until the user asks to wrap up, finish, review, reconcile, switch direction, or merge.
- Do not install or maintain Claude adapter files. Claude CLI is supported only as an optional external review command through `af-claude-review`.

## Branch Rules

- `main` is the production PR target. Do not work, commit, or push directly on it.
- `staging` is optional and protected when enabled. Use it through release PRs unless an explicit repo exception is approved.
- `master`, `production`, and `prod` are reserved legacy names.
- `development` is the default integration branch.
- A session's parent branch is the user-controlled branch checked out when the session starts, unless the user explicitly chooses another non-protected parent.
- Create named branches only when the user explicitly asks. Otherwise use detached session worktrees.
- Merge reviewed sessions back to their recorded parent branch, not blindly to `development`.

## Session Worktrees

Work must happen in an isolated worktree. AF does not prescribe how that isolation is created — only that it exists.

An AF session is not one prompt and not necessarily one chat turn. It is a worktree-backed working context that stays active until the user explicitly ends it or asks for a session action.

- If the agent provides native worktree isolation, work within it and record AF metadata there.
- If no isolated worktree exists, use `af-flow` or `scripts/start-session.sh` to create one.
- If the current checkout is already an AF session worktree and the user is continuing the same direction, keep working there. Do not run `af-finish` just because one request completed.
- If the user asks to review, reconcile, finish, wrap up, or merge, route to the matching AF skill/script instead of starting a new worktree.
- If the user changes to a clearly unrelated direction, finish, pause, or explicitly reconcile the current session before starting another.

AF metadata should stay small:

```text
agentFlow.kind = session
agentFlow.parent = <parent-branch>
agentFlow.sessionName = <session-name>
agentFlow.state = active|ready|merged
agentFlow.owner = <agent> (set via AF_AGENT_ID env var, defaults to "agent")
agentFlow.devlogPolicy = finish
agentFlow.startedAt = <timestamp>
agentFlow.lastTouchedAt = <timestamp>
agentFlow.branch = <explicit-branch> # only when branch-backed
agentFlow.sessionUnit = user-ended
agentFlow.endTriggers = finish,review,reconcile,merge,switch-direction
```

If the current checkout is dirty before starting, inspect it and create or require a devlog-backed commit for that existing work before opening a new session. Do not hide dirty parent work in a new worktree.

## Finish Policy

Every file-changing session needs a `devlog/` entry before the session commit.

Do not finish automatically after every prompt. Finish only when the user asks to wrap up, finish, commit, review for merge, reconcile the session, switch away from the current work, or otherwise end the active working session.

Finish with `af-finish` or:

```bash
scripts/finish-session.sh
```

The finish flow validates, checks docs/devlog, uses `af-show` when useful, commits dirty session work when configured, and reports readiness. It does not run a review — that happens once, at release time, via `af-full-review`. Ready sessions ask before merge:

```bash
scripts/finish-session.sh --merge
```

Run that only after explicit approval.

## Docs And Devlog

- `devlog/` is the durable human history for every file-changing session.
- Metadata is only machine routing.
- Update project docs when behavior, setup, architecture, security, deployment, operations, onboarding, or user workflows change.
- Use `af-docs` for docs maintenance, diagrams, guides, demo plans, presentations, and visual communication assets.
- Use `af-feature-audit` only for explicit app-wide feature/user-story QA campaigns; it is not part of the default finish or release gates.
- Use `af-brand-guidelines` before broad UI work when a repo lacks a usable brand/design source of truth.
- Use `af-ui-audit` only for explicit responsive UI/UX review, issue-register, fix, and retest campaigns; it is not part of the default finish or release gates.
- Use `af-migrate-backlog-devlog` only for preserving old Backlog-style history.

## Push Readiness

Before pushing a parent branch:

```bash
scripts/check-push-readiness.sh <branch>
```

The check blocks dirty or unmerged child session worktrees. Reconcile with:

```bash
scripts/worktree-manager.py
scripts/worktree-manager.py --interactive
scripts/worktree-manager.py --pickup <id>
scripts/worktree-manager.py --cleanup <id> --yes
```

## Release Flow

Default path:

```text
development -> staging -> main
```

Use `development -> main` only when staging is disabled in config or explicitly requested.

Before release:

1. Run `af-reconcile`.
2. Run `af-full-review`.
3. Run `af-security-review` if requested, config-required, or security-sensitive. Prefer Codex Security when available.
4. Run `af-claude-review` only when the user requests Claude CLI review or the release/high-risk review explicitly needs an external model check.
5. Run `af-release`.

Ask before remote side effects such as `git push` or `gh pr create` unless the user clearly authorized them in the current request.

## Safety

- Keep changes scoped to the user request.
- Do not delete files, worktrees, branches, or config unless the request requires it and the action is safe.
- Do not change secrets, production config, DNS, auth, payments, or deployment settings without explicit approval.
- Preserve existing `.gitignore` rules; append AF policy blocks rather than replacing them.
- Commit IDE files only when they encode shared project tooling, not personal preferences.

## Done

A session is done when changes are implemented in one AF session worktree, validation is run or explicitly skipped with reason, visual/manual proof is recorded when relevant, devlog and impacted docs are updated, merge readiness is reported, and the user has been asked before merge. Full review is a release-time gate (`af-full-review`), not a per-session requirement.
