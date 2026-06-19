# Agent-Flow Overview Presentation

## Slide 1: Agent-Flow

Shared workflow rules for Claude, Codex, and other coding agents.

Visual: simple flow from developer to agents to protected Git workflow.

## Slide 2: The Problem

Unstructured agent sessions can drift across branches, skip docs, overwrite parallel work, and leave weak handoff records.

Visual: before/after comparison.

## Slide 3: The Core Loop

For file-changing chats, create one AF session worktree, validate, run app/browser review when applicable, write devlog, update docs, review, ask before merge, then check child worktrees before push.

Visual: Mermaid loop from `docs/USER-GUIDE.md`.

## Slide 4: Agent-Agnostic Instructions

`AGENT-FLOW.md` is canonical. `AGENTS.md` and `CLAUDE.md` are adapters.

Visual: hub-and-spoke diagram.

## Slide 5: Skills and Scripts

AF skills cover small changes, worktrees, finishing sessions, docs, devlogs, review, security review, reconciliation, release PRs, and Backlog migration.

Visual: skill routing diagram from `docs/ARCHITECTURE.md`.

## Slide 6: Session Lifecycle Helpers

`start-session.sh`, `finish-session.sh`, `worktree-manager.py`, and `check-push-readiness.sh` make the default flow repeatable while keeping merges explicit.

Visual: session lifecycle diagram from `docs/ARCHITECTURE.md`.

## Slide 7: Documentation and Visuals

Agent-Flow requires devlog entries and recommends docs, diagrams, screenshots, demos, and presentation materials when they improve understanding.

Visual: docs artifact matrix.

## Slide 8: Demo Flow

Install, initialize a repo, inspect generated config and instruction files, start a session, run finish checks, inspect push readiness.

Visual: terminal screenshot sequence.

## Slide 9: Why It Matters

Agent-Flow makes agent-assisted solo development more consistent, reviewable, and easier to hand off.

Visual: concise outcome list.

## Production Notes

- Start with this Markdown outline.
- Convert to PPTX only after the audience and visual style are confirmed.
- Use real terminal screenshots for credibility.
- Add generated imagery only for a marketing version, not for the technical overview.
- Follow `docs/BRAND-GUIDELINES.md` for tagline, voice, color, and public-facing visual direction.
