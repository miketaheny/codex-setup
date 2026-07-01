# Agent-Flow Overview Presentation

The current branded landscape PDF presentation lives at `docs/presentations/agent-flow-walkthrough.pdf`.
Regenerate it with `scripts/generate-agent-flow-walkthrough-pdf.py`.

## Slide 1: Agent-Flow

Structured workflow rules for Codex.

Visual: simple flow from developer to agents to protected Git workflow.

## Slide 2: The Problem

Unstructured agent sessions can drift across branches, skip docs, overwrite parallel work, and leave weak handoff records.

Visual: before/after comparison.

## Slide 3: The Core Loop

For file-changing work, use `af-flow`, keep related prompts in one AF session worktree, write devlog, use `af-finish` when wrapping up, ask before merge, then check child worktrees before push. Use `af-help` for command help.

Visual: Mermaid loop from `docs/USER-GUIDE.md`.

## Slide 4: Codex Instructions

`AGENT-FLOW.md` is canonical. `AGENTS.md` is the Codex adapter. Claude CLI is optional review tooling only.

Visual: hub-and-spoke diagram.

## Slide 5: Skills and Scripts

AF skills cover help, brand guidelines, pnpm conversion, Codex speed/depth profiles, session start, finish, visual proof, docs, devlogs, review, reconciliation, full release review, release PRs, Codex Security-aware security review, manual feature audits, manual UI audits, and Backlog migration.

Visual: skill routing diagram from `docs/ARCHITECTURE.md`.

## Slide 6: Session Lifecycle Helpers

`start-session.sh`, `finish-session.sh`, `worktree-manager.py`, and `check-push-readiness.sh` make the default flow repeatable while keeping merges explicit.

Visual: session lifecycle diagram from `docs/ARCHITECTURE.md`.

## Slide 7: Documentation and Visuals

Agent-Flow requires devlog entries and recommends docs, diagrams, screenshots, demos, and presentation materials when they improve understanding.

Visual: docs artifact matrix.

## Slide 8: Demo Flow

Install, initialize a repo, inspect generated config and instruction files, show pnpm onboarding for Node repos, start a session, run finish checks, inspect push readiness.

Visual: terminal screenshot sequence.

## Slide 9: Why It Matters

Agent-Flow makes agent-assisted solo development more consistent, reviewable, and easier to hand off.

Visual: concise outcome list.

## Production Notes

- Start with this Markdown outline.
- Create PDF presentations, not PPTX files, after the audience and visual style are confirmed.
- Use real terminal screenshots for credibility.
- Add generated imagery only for a marketing version, not for the technical overview.
- Follow `docs/BRAND-GUIDELINES.md` for tagline, voice, color, and public-facing visual direction.
