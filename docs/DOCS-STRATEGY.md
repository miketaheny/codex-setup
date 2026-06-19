# Documentation Strategy

This file is the source of truth for how `af-docs` manages this repo's `docs/` folder.

## Stewardship Model

`af-docs` owns ongoing documentation maintenance for this repo. After this strategy exists, routine code, skill, script, template, and workflow changes should update docs directly from evidence instead of repeating the full documentation interview.

Use the in-depth interview process only when:

- adopting or overhauling an existing repo's docs for the first time
- this repo's audience, product direction, or documentation structure materially changes
- the user explicitly asks to revisit the documentation strategy

For ordinary changes, update docs from:

- changed files and diffs
- `devlog/` entries
- recent commits
- scripts, templates, skills, and adapter files
- validation output
- screenshots, demos, or other user-provided evidence when available

Do not treat archiving as the default cleanup action. Update useful docs in place, merge overlapping docs, split overloaded docs, or mark content as superseded. Archive or remove docs only when they are obsolete or misleading and the user approves.

## Audiences

Priority audiences:

1. Solo developers using Agent-Flow across Claude, Codex, and other agents.
2. AI coding agents that need unambiguous workflow rules and repo-specific context.
3. Future maintainers evolving the setup, scripts, skills, and adapters.
4. Stakeholders evaluating whether Agent-Flow is useful for safer agent-assisted development.

## Documentation Jobs

Docs should help readers:

- install the global Agent-Flow setup
- initialize new repositories
- choose the correct AF skill for a session
- understand chat/session classification, branch, worktree, devlog, review, optional security review, merge, push-readiness, and release PR rules
- migrate legacy Backlog-style stores into `devlog/`
- understand how the setup stays agent-agnostic
- visualize architecture, skill routing, and daily workflows
- create demos, presentations, user guides, and stakeholder-facing material
- keep public-facing brand, README, launch copy, and visual recommendations consistent

## Docs Map

Current canonical docs:

| Path | Status | Maintenance rule |
|---|---|---|
| `CHANGELOG.md` | Current | Keep user-facing workflow, docs, skill, and setup changes summarized. |
| `README.md` | Current | Keep as the quick entrypoint, install guide, and docs map. |
| `docs/WORKFLOW.md` | Current | Keep branch, devlog, review, migration, and release workflow accurate. |
| `docs/BRAND-GUIDELINES.md` | Current | Keep positioning, messaging, voice, visual identity, launch surfaces, and public repo presentation guidance aligned with the product direction. |
| `docs/AGENT-PROMPTS.md` | Current | Keep prompt examples aligned with current AF skills and workflow rules. |
| `docs/ARCHITECTURE.md` | Current | Keep system, install, init, and skill-routing diagrams aligned with scripts and files. |
| `docs/USER-GUIDE.md` | Current | Keep session-based install, init, skill, migration, and release guidance accurate. |
| `docs/VISUALS.md` | Current | Keep visual format recommendations, screenshots, demos, decks, and content plans current. |
| `docs/DEMO.md` | Current | Keep demo and recording flow aligned with the repo's actual commands. |
| `docs/PITCH.md` | Current | Keep stakeholder and marketing copy grounded in verified repo behavior. |
| `docs/presentations/agent-flow-overview.md` | Current | Keep as the editable slide-outline source until a PPTX is explicitly requested. |
| `docs/decisions/` | Optional support | Use for durable workflow or architecture decisions. |
| `docs/solutions/` | Optional support | Use for reusable implementation lessons. |
| `docs/plans/` | Optional support | Use for meaningful future work plans. |
| `docs/diagrams/` | Optional support | Use for diagram source files when diagrams outgrow inline Mermaid. |
| `docs/assets/` | Optional support | Use for screenshots, generated visuals, or demo media. |
| `docs/presentations/` | Optional support | Use for slide outlines and future deck artifacts. |

## Visual Strategy

Use visual assets when they reduce explanation cost.

- Mermaid is the default for source-accurate workflow, sequence, and architecture diagrams.
- D2 is recommended when larger topology or dependency diagrams need stronger layout control.
- Screenshots are recommended for install, init, session lifecycle, skill discovery, and real UI or terminal flows.
- Demo videos are recommended for install-to-init, start-session-to-finish-session, worktree-manager pickup/cleanup, push-readiness, release PR, backlog migration, and docs maintenance walkthroughs.
- Generated images should be limited to conceptual, marketing, or presentation assets when real product screenshots are not available.

For this repo, prefer efficient, technical, and data-driven visuals in core docs. Use polished but restrained visuals for presentations and stakeholder-facing content.

Use `docs/BRAND-GUIDELINES.md` as the source of truth for public-facing voice, visual identity, launch copy, social cards, README hierarchy, and whether a future `design.md` is needed.

## Maintenance Triggers

Run `af-docs` when changes affect:

- installation, init, gitignore, or IDE policy behavior
- scripts under `scripts/`
- skills under `skills/`
- agent adapters such as `AGENTS.md`, `CLAUDE.md`, or `AGENT-FLOW.md`
- templates copied into target repos
- prompt lifecycle, branch, worktree, devlog, review, optional security review, merge, push-readiness, or release workflows
- backlog migration behavior
- visual documentation, demo, presentation, or marketing guidance
- public brand, README positioning, launch copy, or repo traction content
- README navigation or setup commands
- user-facing workflow, setup, skill, or docs behavior that belongs in `CHANGELOG.md`

For each trigger, update only the docs that need to change.

## Validation

Use the lightest useful validation for docs-only work:

- inspect Markdown for broken relative links and stale file references
- run skill validation when skill docs changed
- run shell syntax checks when script references changed
- run `git diff --check`
- render diagrams or inspect previews when visual syntax changed and tooling is available

Do not claim screenshots, videos, or rendered diagrams were verified unless they were actually produced or rendered.

## Current Assumptions

- `devlog/` is the project history system; legacy `Backlog.md`, `triage.md`, `backlog/`, and `.backlog/` stores should be migrated before removal.
- The repo should remain agent-agnostic, with Codex skills as one supported adapter layer rather than the core product identity.
- The docs folder should stay practical and maintainable; avoid placeholder files that are not grounded in current behavior.
