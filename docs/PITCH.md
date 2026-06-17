# Agent-Flow Pitch

## Positioning

Agent-Flow is a lightweight workflow kit for solo developers using AI coding agents. It standardizes branch safety, worktree isolation, devlog history, documentation maintenance, review gates, and formal protected-branch security review across Claude, Codex, and other agents.

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
- scripts for install, init/bootstrap, task lifecycle, push readiness, worktrees, branch safety, and review snapshots
- per-commit `devlog/` conventions
- docs and visual asset guidance

## Proof Points From This Repo

- Agent-neutral canonical instructions exist in `AGENT-FLOW.md`.
- Codex and Claude adapters point to the same rules.
- Skills cover small changes, worktrees, docs, devlogs, review, security review, reconciliation, release promotion, and Backlog migration.
- Bootstrap scripts create consistent repo instruction and documentation scaffolding.
- Visual docs now include architecture diagrams, a user guide, demo plan, and presentation outline.

## Short Pitch

Agent-Flow gives every AI coding agent the same operating system for solo development: safe branches, isolated work, devlog history, documentation updates, review before merge, formal security review before protected-branch PRs, and push checks before branch promotion.

## Longer Pitch

Agent-Flow is a portable setup for developers who use multiple AI coding agents across multiple repos. It defines one canonical workflow, installs adapters for agent-specific instruction files, adds reusable AF skills, and provides scripts that make safe branch and worktree habits repeatable. The result is a lower-friction development loop where every task leaves a readable history, every merge gets a review gate, and protected-branch PRs get a distinct security gate.

## Objections and Responses

| Objection | Response |
|---|---|
| "I only use one agent." | Agent-Flow still gives that agent consistent branch, docs, and review behavior across repos. |
| "This seems heavy." | The workflow explicitly prefers the lightest safe skill and reserves heavier planning for broader tasks. |
| "My agent does not support Codex skills." | The skill bodies are Markdown workflows and can be read or adapted by other agents. |
| "I do not want a task database." | Current Agent-Flow uses `devlog/` files for durable engineering history. |

## Marketing Visual Recommendations

- Use a clean workflow diagram as the primary visual.
- Use terminal screenshots for credibility.
- Use a generated hero image only if creating a website or launch announcement.
- Avoid claiming measured productivity gains until metrics exist.
