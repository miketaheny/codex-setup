# Visual Documentation Plan

This plan applies the `af-docs` visual interview to this Agent-Flow setup repo.

`docs/DOCS-STRATEGY.md` is the source of truth for when to update visual docs, when to interview the user, and how `af-docs` should manage the docs folder over time.

## Assumptions

| Question | Recommendation for this repo |
|---|---|
| Audience | Solo developers, AI coding agents, future maintainers, and stakeholders evaluating Agent-Flow. |
| Goal | Explain how the setup works, how to install it, how to use skills, and how to present the workflow. |
| Style | Efficient, technical, and data-driven for core docs; polished but restrained for stakeholder content. |
| Format | Markdown, Mermaid diagrams, demo scripts, and presentation outlines. |
| Fidelity | Accurate implementation diagrams now; screenshots/videos later after install flows are exercised on a real machine. |
| Source of truth | Repo files, scripts, skills, templates, and devlog entries. |

## Current Visual Inventory

| Visual | Location | Format | Purpose |
|---|---|---|---|
| System map | `docs/ARCHITECTURE.md` | Mermaid flowchart | Show how global files, adapters, skills, scripts, and templates connect. |
| Install flow | `docs/ARCHITECTURE.md` | Mermaid sequence | Show where files are copied during install. |
| Repo bootstrap flow | `docs/ARCHITECTURE.md` | Mermaid flowchart | Show what bootstrap creates in a target repo. |
| Skill model | `docs/ARCHITECTURE.md` | Mermaid flowchart | Show how requests route to AF skills. |
| Daily loop | `docs/USER-GUIDE.md` | Mermaid flowchart | Show the expected branch, validation, docs, and review cycle. |

## Recommended Formats

Use Mermaid for current docs because it is portable, diffable, and easy for agents to maintain.

Use D2 later if diagrams become too dense, especially for:

- larger topology diagrams
- dependency graphs
- multi-environment deployment views
- diagrams requiring stronger layout control

Use screenshots for:

- terminal install output
- bootstrap output inside a sample repo
- Codex skill discovery, if relevant
- Claude adapter behavior, if relevant

Use demo video for:

- install -> bootstrap -> worktree -> devlog -> review flow
- Backlog migration dry-run -> write flow
- docs/visual update workflow

Use generated images only for:

- a website hero or launch post
- a conceptual Agent-Flow workflow illustration
- stakeholder-friendly presentation visuals when screenshots do not exist

## Screenshot Checklist

Capture these after the next local install test:

- `./scripts/install.sh` success output
- `~/.agent-flow` tree view
- `~/.codex/skills` showing AF skills
- `~/.agent-flow/scripts/bootstrap-repo.sh` output in a sample repo
- generated `AGENT-FLOW.md`, `AGENTS.md`, `CLAUDE.md`, and `devlog/README.md`
- `af-migrate-backlog-devlog` dry-run output on a sample task file

## Demo Video Plan

Recommended short demo:

1. Show a clean sample repo on `development`.
2. Run `~/.agent-flow/scripts/bootstrap-repo.sh`.
3. Open the generated instruction files.
4. Create a worktree with `scripts/new-worktree.sh`.
5. Add a small devlog entry.
6. Run `scripts/review-snapshot.sh`.
7. Show where visual docs and skill docs live.

Keep the video under three minutes for adoption. Use captions for the commands and avoid relying on narration alone.

## Presentation Recommendation

Use `docs/presentations/agent-flow-overview.md` as the source outline for a future slide deck. Build a PPTX only when the audience and visual style are known.

Recommended deck style:

- quiet technical palette
- minimal screenshots
- simple workflow diagrams
- one concept per slide
- clear before/after comparison with unstructured agent usage

## Marketing Content Recommendation

Use `docs/PITCH.md` for launch or stakeholder copy. Keep claims grounded:

- Agent-Flow standardizes branch safety, devlogs, docs, and review.
- It works across Claude, Codex, and other agents through shared instructions and adapters.
- Codex skills are included, but the core workflow is agent-agnostic.

Avoid unsupported claims about speed, reliability, or compatibility until measured.
