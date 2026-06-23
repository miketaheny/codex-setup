# Agent-Flow Pitch

## Positioning

Agent-Flow is a lightweight workflow kit for solo developers using AI coding agents. It standardizes branch safety, worktree isolation, devlog history, documentation maintenance, review, and release readiness across Claude, Codex, and other agents.

Public-facing brand guidance lives in `docs/BRAND-GUIDELINES.md`. The brand should feel original, technical, calm, and operational: closer to restrained developer infrastructure than consumer product design.

## Audience

- solo developers running many agent threads
- maintainers who want consistent agent behavior across repositories
- teams evaluating agent-assisted development workflows
- technical stakeholders who need predictable engineering records

## Problem

AI coding agents are useful, but unstructured sessions can drift across branches, skip documentation, overwrite parallel work, and leave weak handoff records.

## Offer

Agent-Flow provides:

- shared `AGENT-FLOW.md` rules for all agents
- `AGENTS.md` and `CLAUDE.md` adapters
- Codex-compatible AF skills for common workflows
- scripts for install, init, session lifecycle, push readiness, worktrees, and branch safety
- finish-time session `devlog/` conventions
- docs and visual asset guidance

## Proof Points From This Repo

- Agent-neutral canonical instructions exist in `AGENT-FLOW.md`.
- Codex and Claude adapters point to the same rules.
- Skills cover help, brand guidelines, session start, finish, visual proof, docs, devlogs, review, reconciliation, full release review, release PRs, security review, manual feature audits, manual UI audits, and Backlog migration.
- Bootstrap scripts create consistent repo instruction and documentation scaffolding.
- Visual docs now include architecture diagrams, a user guide, demo plan, and presentation outline.

## Short Pitch

Agent-Flow gives AI coding agents a shared operating model for solo development: safe branches, isolated worktree sessions, devlog history, documentation updates, review before merge, optional security review for sensitive releases, and push checks before release PRs.

## Longer Pitch

Agent-Flow is a portable setup for developers who use multiple AI coding agents across multiple repos. It defines one canonical workflow, installs adapters for agent-specific instruction files, adds reusable AF skills, and provides scripts that make safe branch and worktree habits repeatable. The result is a lower-friction development loop where every session leaves a readable history, every merge gets a review, and releases get a full readiness gate.

## Launch Angle

Lead with the workflow problem: AI coding agents are useful, but unstructured file-changing chats are hard to trust later. Agent-Flow turns those chats into scoped sessions with a visible lifecycle: worktree, validation, devlog, docs, review, merge prompt, and push readiness.

Use commands, diagrams, and real terminal output as proof. Do not lead with model-vendor logos, productivity metrics, or broad autonomy claims.

## Objections and Responses

| Objection | Response |
|---|---|
| "I only use one agent." | Agent-Flow still gives that agent consistent branch, docs, and review behavior across repos. |
| "This seems heavy." | The workflow explicitly prefers the lightest safe skill and reserves heavier planning for broader work. |
| "My agent does not support Codex skills." | The skill bodies are Markdown workflows and can be read or adapted by other agents. |
| "I do not want another tracking database." | Agent-Flow uses plain `devlog/` files for durable engineering history. |

## Marketing Visual Recommendations

- Use a clean workflow diagram as the primary visual.
- Use terminal screenshots for credibility.
- Use a generated hero image only if creating a website or launch announcement.
- Avoid claiming measured productivity gains until metrics exist.
- Follow `docs/BRAND-GUIDELINES.md` for color, tone, tagline, launch copy, and social-card direction.
