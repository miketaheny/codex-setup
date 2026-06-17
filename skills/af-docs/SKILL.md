---
name: af-docs
description: Maintain project documentation and visual communication assets for Agent-Flow, including first-time backfill, ongoing updates from devlog/ and commits, diagrams, user guides, presentations, screenshots, demos, and marketing content. Use when docs need to explain, visualize, teach, sell, or operationalize a repo.
---

# AF Docs Skill

Use this skill to keep project documentation accurate, visual, and useful as the repository changes.

## Purpose

Project docs should explain the current system, not just the latest code diff. This skill handles first-time documentation setup, ongoing maintenance, and visual assets that help users, maintainers, operators, and buyers understand the project.

## When to Run

Run this skill when:

- a repo has missing, empty, or placeholder project docs
- meaningful work changed behavior, setup, architecture, security, deployment, or operations
- recent devlog files or commits describe work that is not reflected in docs
- the user asks to visualize a system, workflow, architecture, value proposition, or user journey
- the repo needs user guides, screenshots, demo videos, diagrams, presentations, or marketing content
- `development` is about to be pushed or promoted to protected branches such as `staging`, `main`, release, or production branches

Do documentation work on `development` or a feature branch/worktree. Do not edit directly on protected branches.

## Documentation Model

Use the docs the repo already has. When docs are missing or only placeholders, establish a practical baseline under `docs/`.

Recommended baseline:

- `README.md` - project purpose, setup, common commands, and navigation
- `docs/REQUIREMENTS.md` - user-visible behavior and non-functional requirements
- `docs/ARCHITECTURE.md` - major components, boundaries, data flow, storage, and integrations
- `docs/RUNBOOK.md` - local setup, environment variables, deploy, rollback, logs, and operations
- `docs/SECURITY.md` - authentication, authorization, secret handling, trust boundaries, and reporting
- `docs/USER-GUIDE.md` - task-based user instructions and walkthroughs
- `docs/VISUALS.md` - visual asset plan, diagram inventory, screenshots, demos, and presentation recommendations
- `docs/decisions/` - durable architecture or workflow decisions
- `docs/solutions/` - reusable fixes, patterns, and lessons worth finding later

Only create files that are useful for the repo. Avoid boilerplate that cannot be grounded in code, configuration, or devlog history.

## Visual Interview

When the user wants visualization or the audience is unclear, briefly interview them before producing major visual assets. Ask only the questions that materially change the result:

- Audience: internal operators, engineers, executives, customers, prospects, support, or new users?
- Goal: explain how it works, teach usage, sell value, debug operations, onboard contributors, or support a launch?
- Style: efficient and data-driven, polished internal app, product-marketing, technical architecture, executive summary, or training material?
- Format: Markdown docs, Mermaid, D2, static images, generated images, screenshots, demo video, slide deck, one-pager, or website content?
- Fidelity: quick schematic, accurate implementation diagram, polished visual, or production-ready marketing collateral?
- Source of truth: code, devlog, screenshots, live app, analytics/data, existing brand guidance, or user-provided examples?

If the user is not available and work should continue, choose the smallest accurate visual set, mark assumptions, and recommend follow-ups.

## Visual Artifact Recommendations

Choose visual formats by purpose:

| Purpose | Recommended artifact | Default format |
|---|---|---|
| Explain repo structure | system map, component diagram | Mermaid flowchart |
| Explain request/data flow | sequence diagram or data-flow diagram | Mermaid sequence/flowchart |
| Explain state machines or lifecycle | state diagram | Mermaid state diagram |
| Explain dependencies or platform topology | architecture graph | D2 or Mermaid |
| Explain user journey | journey map or task walkthrough | Markdown plus Mermaid |
| Teach product usage | user guide with screenshots | Markdown plus screenshots |
| Demonstrate UI behavior | short demo video or GIF | live capture when app runs |
| Explain before/after changes | comparison table plus annotated screenshots | Markdown plus images |
| Internal operations | runbook diagrams, checklists, dashboards | efficient and data-driven visuals |
| Customer/prospect education | presentation, one-pager, marketing narrative | polished visuals and screenshots |
| Launch or landing-page support | copy blocks, product shots, generated imagery if no real visuals exist | marketing content pack |

Default to source-accurate Mermaid diagrams for technical docs. Use D2 when layout clarity matters for infrastructure or larger graph diagrams. Use screenshots or live demo captures when users need to inspect the real interface. Use generated images only for marketing, conceptual, or brand visuals when real product images are unavailable or insufficient.

## Visual Quality Rules

- Visuals must be grounded in real code, config, workflows, screenshots, or user-provided context.
- Diagrams should have a clear title, purpose, and surrounding explanation.
- Prefer maintainable text-based diagrams in docs when accuracy matters over polish.
- Prefer screenshots or demo videos for user guides when a UI exists.
- Prefer concise decks for executive or marketing audiences; avoid turning docs into slide scripts.
- For internal/admin tools, use dense, efficient, data-driven visuals rather than decorative imagery.
- For customer-facing or marketing content, use higher-fidelity visuals, product screenshots, generated hero images, and benefit-led copy when appropriate.
- Do not invent product capabilities, metrics, customers, integrations, or brand claims.
- Keep visual source files close to docs, such as `docs/diagrams/`, `docs/assets/`, or `docs/presentations/`.

## Source Material

Read enough evidence to make factual updates:

- `devlog/*.md` files changed on the branch or created since the target branch diverged
- recent commits, using `git log`, `git diff`, and `git show` when Git is available
- README and existing `docs/`
- package manifests, dependency files, and command definitions
- app entry points, routes, APIs, CLIs, and tests
- environment examples, scripts, CI workflows, and deployment config
- auth, authorization, secret handling, external service clients, and validation code
- task files or planning notes when they explain intent that code alone does not show

If Git is unavailable, use the available filesystem state and devlog files, then document the limitation.

## Workflow

1. Inspect branch safety and the current working tree.
2. Identify the docs that already exist and whether they are established or placeholder-only.
3. Identify the change range:
   - for branch work, compare against `development` or the intended merge base
   - for pre-promotion work, compare `development` against the protected target branch when available
   - when no range is available, read recent devlog files and representative project files
4. Decide whether this is a backfill or maintenance pass.
5. Update only the docs needed to make the repository accurate.
6. Decide whether visual assets are needed using the Visual Artifact Recommendations table.
7. Create or update diagrams, screenshots plans, user guides, presentations, or marketing content only when they improve understanding.
8. Preserve human-written sections unless they are stale or contradicted by current evidence.
9. Mark uncertain claims with HTML TODO comments instead of guessing.
10. Run the lightest validation that fits the change, usually docs rendering, link checks, diagram rendering, screenshot verification, markdown linting, or targeted inspection.
11. Summarize docs changed, visuals created or recommended, evidence used, validation, and remaining TODOs.

## Backfill Mode

Use backfill mode when docs are missing, empty, or mostly placeholders.

Read the repo shape first:

- stack indicators such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, or framework config
- top-level source directories such as `app/`, `pages/`, `src/`, `lib/`, `api/`, `routes/`, or `services/`
- app or CLI entry points
- database, storage, queue, auth, and integration code
- `.env.example`, deploy config, CI workflows, scripts, and test commands

Write concise first-pass docs that are grounded in visible files. Use TODO comments for product intent, ownership, URLs, contacts, or operational details that the repo does not reveal.

For visual backfills, usually create:

- one architecture or system map
- one common workflow diagram
- one user guide or operator guide
- one visual asset plan that recommends screenshots, videos, decks, or marketing material

## Maintenance Mode

Use maintenance mode when docs already contain useful project-specific content.

Start with the newest relevant devlog files and commits. For each change, decide whether docs need updates:

- Behavior changed: update requirements, README usage, API docs, or user workflow docs.
- Components changed: update architecture diagrams, component tables, data flow, or integration notes.
- Setup changed: update install, commands, environment variables, or local run steps.
- Deployment or operations changed: update runbook deploy, rollback, monitoring, logs, or incident notes.
- Security changed: update auth, authorization, secret handling, trust boundaries, or vulnerability reporting.
- Reusable lesson discovered: add or update a focused solution note.
- Durable tradeoff made: add or update a decision record.
- User workflow changed: update user guide screenshots, walkthroughs, demo scripts, and journey diagrams.
- Product positioning changed: update marketing copy, pitch outline, screenshots, and presentation recommendations.

Do not rewrite established docs wholesale when a narrow patch is enough.

## Presentation and Marketing Mode

Use this mode when the audience includes users, buyers, executives, stakeholders, or launch/support teams.

Recommended outputs:

- `docs/PITCH.md` - positioning, audience, value props, proof points, and objections
- `docs/USER-GUIDE.md` - task-based guide with screenshots or screenshot placeholders
- `docs/DEMO.md` - live demo script, screenshot list, and video capture plan
- `docs/presentations/<topic>.md` - slide outline that can be converted to a deck
- `docs/assets/` - screenshots, generated imagery, and supporting media when available

Ask whether the artifact should feel:

- efficient and data-driven for internal apps
- technical and precise for engineering docs
- polished and visual for stakeholder presentations
- benefit-led and image-rich for marketing

When creating presentations, prefer a crisp outline first unless the user explicitly requests a PPTX. When creating marketing content, separate verified facts from recommended messaging.

## Pre-Promotion Check

Before pushing or promoting `development` to protected branches:

1. Confirm the work is on `development` or a non-protected branch.
2. Review devlog files and commits since the last promotion or since the target branch diverged.
3. Check whether all user-facing, operational, architectural, setup, and security changes are reflected in docs.
4. Resolve stale TODOs that block promotion, or record why they are acceptable to carry forward.
5. Report whether docs are ready for promotion.

This skill does not perform the push or promotion by itself.

## Content Standards

- Prefer concrete paths, commands, and config names over generic prose.
- Keep docs short enough to scan, but complete enough for the next agent session or maintainer to act.
- Distinguish observed facts from inferred intent.
- Do not invent integrations, URLs, contacts, owners, service levels, or policies.
- Do not move or rename docs unless the existing layout is clearly broken.
- Do not claim validation passed unless it actually ran.
- Include diagrams when they materially reduce explanation cost.
- Include screenshots or demo capture recommendations when users need to see real UI behavior.
- Include presentation and marketing recommendations when the project needs stakeholder communication, adoption, launch, or sales support.

## Expected Output

End with:

- branch or worktree status
- docs created or changed
- diagrams, screenshots, videos, presentations, guides, or marketing content created or recommended
- evidence used, including devlog files or commit range when available
- validation performed or why it was skipped
- unresolved TODOs or risks
- whether docs are ready for merge or protected-branch promotion
