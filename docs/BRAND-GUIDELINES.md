# Agent-Flow Brand Guidelines

Agent-Flow is a workflow system for agent-assisted development. The brand should make the repo feel trustworthy, practical, and worth adopting before the reader has installed anything.

## Recommendation

Do not copy Google's or OpenAI's design language.

Use Agent-Flow's own brand system. OpenAI-style restraint is the closer influence because this is developer infrastructure: calm, precise, text-led, and credibility-driven. Google-style color and motion can feel too broad and consumer-oriented for a repo whose value is branch safety, worktree isolation, devlogs, review gates, and release discipline.

If this repo later gets a website or app UI, a small `design.md` can define UI components and layout rules. For the current public repo, this brand guide is the right source of truth because it covers positioning, voice, visuals, README structure, launch copy, and contribution rules.

## Brand Core

### Name

Use **Agent-Flow** in public-facing copy.

Use **AF** only after the full name appears once, or inside technical workflow references such as `af-docs`, `af-review`, and `AF session worktree`.

Avoid:

- `AF Agent-Flow`
- `Agent Flow`
- `agentflow`
- positioning the Codex skill layer as the whole product

### Category

Agent-Flow is an **AI agent workflow kit for solo developers**.

Secondary category phrases:

- agent-assisted development workflow
- local workflow system for coding agents
- branch-safe agent workflow kit
- devlog and review workflow for AI coding agents

### One-Line Description

Agent-Flow gives AI coding agents a shared operating model: isolated worktree sessions, durable devlogs, maintained docs, review gates, and protected release paths.

### Positioning Statement

For solo developers and maintainers using Claude, Codex, and other coding agents, Agent-Flow is a local workflow kit that turns unstructured agent chats into reviewable development sessions. Unlike prompt-only conventions, Agent-Flow installs shared instructions, agent adapters, lifecycle scripts, devlog conventions, docs maintenance rules, and release gates that keep agent-assisted work safer to merge and easier to understand later.

### Brand Promise

Every file-changing agent session should leave the repo easier to trust than it found it.

### Audience Priorities

1. Solo developers running multiple agent sessions across active repos.
2. Maintainers who need consistent agent behavior without a full task database.
3. Agent users evaluating safer branch, docs, and review habits.
4. Technical stakeholders who need to see why agent-assisted work is controlled.

## Messaging

### Primary Message

AI coding agents need operating rules, not just better prompts.

### Supporting Messages

- One related working session, one session worktree.
- Every session leaves a devlog.
- Docs move with the code.
- Review happens before merge.
- Protected release paths get a security gate.
- Agent-agnostic instructions keep Claude, Codex, and future agents aligned.

### Message Pillars

| Pillar | Meaning | Proof in repo |
|---|---|---|
| Control | Agent work is isolated and merge-aware. | `scripts/start-session.sh`, `scripts/finish-session.sh`, worktree metadata |
| Memory | Decisions and validation survive the chat. | `devlog/`, `af-devlog`, devlog templates |
| Trust | Changes are reviewed before they reach parent branches. | `af-review`, `scripts/review-snapshot.sh`, `scripts/check-push-readiness.sh` |
| Portability | The workflow works across agents and repos. | `AGENT-FLOW.md`, `AGENTS.md`, `CLAUDE.md`, `templates/` |
| Discipline | Release paths are explicit and protected. | `af-release`, `af-security-review`, protected-branch rules |

### Tagline Options

Preferred:

- Structured workflow rules for AI coding agents.

Alternates:

- Turn agent chats into reviewable development sessions.
- Branch-safe development flow for AI coding agents.
- Worktree sessions, devlogs, and review gates for agent-assisted code.

Avoid:

- "10x developer productivity"
- "Autonomous software engineering"
- "The AI operating system for coding"
- unsupported claims about speed, reliability, or compatibility

## Voice And Tone

### Voice

Agent-Flow sounds like a senior engineer writing down the workflow they actually use.

Use:

- direct verbs
- concrete commands and paths
- short explanations of why a rule exists
- precise boundaries and caveats
- confidence grounded in observable repo behavior

Avoid:

- hype
- vague productivity claims
- fear-based AI language
- corporate transformation language
- decorative metaphors
- treating one agent vendor as the product identity

### Tone By Surface

| Surface | Tone |
|---|---|
| README | crisp, practical, adoption-focused |
| `AGENT-FLOW.md` | strict, unambiguous, procedural |
| User guide | task-based, calm, complete |
| Pitch docs | benefit-led, still evidence-based |
| Social launch copy | sharp, memorable, no inflated claims |
| Devlogs | factual engineering record |

### Writing Patterns

Prefer:

```text
Agent-Flow maps each related file-changing working session to one isolated worktree session.
```

Avoid:

```text
Agent-Flow revolutionizes how AI transforms your development lifecycle.
```

Prefer:

```text
Run `scripts/check-push-readiness.sh development` before pushing a parent branch.
```

Avoid:

```text
Make sure everything is probably ready before you ship.
```

## Visual Identity

### Visual Principles

- **Structured:** layouts should look organized before they look decorative.
- **Technical:** use real commands, diagrams, and terminal output as proof.
- **Calm:** avoid loud gradients, excessive motion, and rainbow palettes.
- **Readable:** prioritize scan speed, contrast, and clear hierarchy.
- **Agent-agnostic:** do not visually imply that Agent-Flow belongs to one model vendor.

### Logo Direction

Use the committed SVG logo suite as the primary visual identity:

| Asset | Use |
|---|---|
| `docs/assets/agent-flow-logo.svg` | README header, presentations, website header, launch posts that need the full wordmark. |
| `docs/assets/agent-flow-mark.svg` | GitHub avatar, favicon source, square icon, compact slide mark. |
| `docs/assets/agent-flow-social-card.svg` | Open Graph image, social launch image, presentation title card. |

The core concept is a restrained wordmark plus a flow mark.

The mark can combine:

- a branching line for worktrees
- a check node for review
- a document node for devlog
- a guarded merge point for protected branches

The current mark uses an `AF` monogram as the skeleton, with flow nodes and a guarded merge lock to connect the symbol back to the product behavior.

Do not use:

- robot heads as the main logo
- OpenAI knot-like geometry
- Google-style multicolor product marks
- shields as the whole identity, which over-narrows the brand to security

### Color Palette

Use a neutral base with a small set of functional accents.

| Token | Hex | Use |
|---|---:|---|
| Ink | `#101418` | primary text, diagrams |
| Graphite | `#2D333A` | headings, dark UI surfaces |
| Slate | `#59636E` | secondary copy |
| Line | `#D8DEE5` | borders, dividers |
| Paper | `#F7F8FA` | page background |
| White | `#FFFFFF` | content background |
| Flow Green | `#1F9D63` | successful sessions, forward progress |
| Signal Cyan | `#168AAD` | links, active states, flow paths |
| Guard Amber | `#B7791F` | warnings, protected branch gates |
| Review Violet | `#6D5BD0` | review/security gate highlights, used sparingly |

Usage rules:

- Let neutral colors dominate.
- Use one accent per diagram or callout unless a state legend needs more.
- Use Guard Amber only for warnings, release gates, and protected branches.
- Use Review Violet sparingly so the brand does not drift into a purple-blue theme.
- Avoid full-page gradients.

### Typography

Use system-friendly developer typography.

Recommended:

- Headings and UI: Inter, Geist, or system sans-serif.
- Body: Inter, Geist, or system sans-serif.
- Code and terminal: JetBrains Mono, IBM Plex Mono, SFMono-Regular, or system monospace.

Rules:

- Do not use playful display fonts.
- Keep line lengths comfortable in docs.
- Use code formatting for commands, paths, config keys, and skill names.
- Favor tables for comparing workflow rules and scripts.

### Iconography

Use simple line icons when a visual system is needed.

Recommended concepts:

- branch or git-merge for worktrees
- file-text for devlogs
- shield-check for protected release gates
- check-circle for review complete
- terminal for scripts
- book-open for docs

Avoid mascot-led identity or AI sparkle icons as the primary visual language.

### Diagram Style

Mermaid diagrams should use:

- left-to-right flow for process diagrams
- top-to-bottom flow for hierarchy/system maps
- short node labels
- no more than two accent colors unless a legend requires more
- labels that match repo terms: session worktree, devlog, review gate, parent branch, push readiness

Preferred node names:

- `Prompt`
- `Session Worktree`
- `Scoped Change`
- `Validation`
- `Devlog`
- `Docs`
- `Review Gate`
- `Merge Prompt`
- `Push Readiness`

## Content System

### README Structure

The public README should answer, in order:

1. What is Agent-Flow?
2. Why does it matter?
3. What is included?
4. How do I install it?
5. How does the daily loop work?
6. Which docs should I read next?
7. What is the project trying to become?

### Hero Copy Pattern

Use this pattern for GitHub, a future website, or a launch post:

```text
Agent-Flow
Structured workflow rules for AI coding agents.

Turn file-changing agent chats into isolated worktree sessions with devlogs, docs checks, review gates, and protected release paths.
```

### Social Launch Copy

Short version:

```text
I built Agent-Flow to make AI coding agent work easier to trust: one related working session, one worktree, one devlog, docs when behavior changes, review before merge, and push checks before release.
```

Developer version:

```text
Agent-Flow is a local workflow kit for Claude, Codex, and other coding agents. It installs shared instructions, adapters, lifecycle scripts, devlog conventions, docs maintenance rules, and release gates so agent-assisted work stays reviewable.
```

### Repository Topics

Recommended GitHub topics:

- `ai-agents`
- `coding-agents`
- `agent-workflows`
- `developer-tools`
- `git-worktree`
- `codex`
- `claude`
- `devlog`
- `release-workflow`
- `solo-developer`

### SEO Phrases

Use naturally in docs and launch copy:

- AI coding agent workflow
- Claude Codex workflow
- coding agent worktrees
- agent-assisted development
- devlog workflow
- Git worktree automation
- AI agent review gate
- protected branch workflow

## Launch And Traction Surfaces

### GitHub Repo

Make these visible above the fold:

- one-line description
- why it exists
- quick install
- daily loop diagram
- docs map
- clear status of what is included today

Recommended pinned assets:

- README with a simple daily loop diagram
- `docs/BRAND-GUIDELINES.md`
- `docs/PITCH.md`
- `docs/DEMO.md`

### Screenshots And Media

Highest-value screenshots:

- install output
- generated `.agent-flow/config.toml`
- `start-session.sh` output
- `finish-session.sh` output with merge prompt
- `worktree-manager.py --interactive`
- `check-push-readiness.sh development`

Use real terminal output as the main proof. Use generated visuals only for social cards, title cards, or a future website hero.

### Demo

The first public demo should show:

1. Install Agent-Flow.
2. Initialize a sample repo.
3. Start a session worktree.
4. Make a tiny docs change.
5. Finish the session.
6. Show the devlog and merge prompt.
7. Run push readiness.

Keep the demo under three minutes.

### Social Card Direction

Recommended layout:

- wordmark: `Agent-Flow`
- tagline: `Structured workflow rules for AI coding agents`
- small visual: flow from chat to worktree to devlog to review to merge
- neutral background, Signal Cyan flow path, Guard Amber protected branch node

Avoid:

- model logos as the hero
- fake dashboards
- exaggerated metrics
- stock photos

## Contribution And Governance Voice

Contribution docs should make quality expectations explicit:

- keep changes scoped
- update docs when workflows change
- add or update devlog entries
- run validation
- do not bypass review or release gates

Public issue language should be direct:

```text
Describe the workflow gap, the repo state where it appears, the command or skill involved, and the expected behavior.
```

Avoid vague categories such as "AI broke my repo" when a concrete workflow failure can be named.

## Claims Policy

Allowed claims:

- Agent-Flow standardizes branch safety, worktree isolation, devlogs, docs maintenance, review gates, and protected release checks.
- Agent-Flow includes Codex-compatible skills and Claude/Codex adapter files.
- Agent-Flow is designed for solo developers and maintainers using AI coding agents.

Do not claim yet:

- measured productivity improvements
- enterprise readiness
- broad agent compatibility beyond the included adapters and Markdown-readable workflow files
- security guarantees
- automated correctness

## Design Decision

The brand should be original, technical, and grounded in the workflow:

- Use OpenAI-like restraint as an influence for tone, not as a template.
- Do not use Google's color system or consumer product feel as the visual basis.
- Keep `docs/BRAND-GUIDELINES.md` as the current source of truth.
- Add a separate `design.md` only if the project grows into a website, UI, or reusable component system.
