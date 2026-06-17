---
id: TASK-3
title: Make Agent-Flow agent agnostic
status: Done
assignee: []
created_date: '2026-06-17 12:05'
updated_date: '2026-06-17 12:40'
labels: []
dependencies: []
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Rename and reframe the setup as AF Agent-Flow instead of a Codex-only setup. Keep Codex compatibility, add Claude compatibility, make canonical instructions agent-neutral, update scripts/templates/docs/skills accordingly, and initialize a Git repository on `development` when complete.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Canonical workflow instructions use Agent-Flow/AF naming and are not Codex-specific.
- [x] #2 Codex and Claude entrypoint files both exist and point agents to the shared Agent-Flow guidance.
- [x] #3 README, workflow docs, prompts, templates, and scripts describe agent-neutral install/bootstrap behavior while preserving Codex skill installation.
- [x] #4 AF skill wording avoids Codex-only framing except where a Codex-specific skill format or install path is intentional.
- [x] #5 Validation confirms stale Codex-only branding was removed or intentionally retained for tool-specific compatibility.
- [x] #6 A Git repository is initialized on `development` after the edits are complete.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Search for Codex/Claude/agent-specific naming across docs, templates, scripts, and skills.
2. Add a canonical `AGENT-FLOW.md` and adapter files for Codex and Claude.
3. Update README, workflow docs, prompts, templates, and scripts to use Agent-Flow naming.
4. Update skill metadata/body text where it incorrectly says Codex instead of agent/Agent-Flow.
5. Validate skills and scripts, search for remaining branded wording, and document intentional exceptions.
6. Initialize Git with `development` as the initial branch and record final status.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-06-17: Created before implementation. `$triage-md` is not available in this session, so this is tracked directly in filesystem Backlog mode. The project is not a Git repository at task start; Git initialization will happen after implementation per user request.

2026-06-17: Implemented agent-neutral Agent-Flow framing. Added canonical `AGENT-FLOW.md`, root `CLAUDE.md`, and adapter-style `AGENTS.md`; added repo templates for all three; renamed prompt docs to `docs/AGENT-PROMPTS.md`; updated README, workflow docs, commander notes, install/bootstrap scripts, AF skills, reconciliation audit helper, VS Code title, Backlog project name, and `.gitignore`. Codex/OpenAI references remain only where they describe intentional compatibility surfaces such as `.codex`, Codex skill format, `agents/openai.yaml`, and optional Codex plugin setup.

Validation passed: `bash -n` over shell scripts; `quick_validate.py` over all skills; `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile skills/af-reconcile-worktrees/scripts/audit_repo.py`; temporary Git repo bootstrap smoke test; `rg` searches over active files for stale Codex-only branding. Git repository initialization on `development` is the final step after this tracking update.

2026-06-17: `backlog/` disappeared unexpectedly during implementation. Recreated only `backlog/config.yml` and this current task record to preserve tracking for the active request without reconstructing older task history.
<!-- SECTION:NOTES:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Agent-neutral docs and adapter files are in place.
- [x] #2 Install/bootstrap scripts create both Codex and Claude-compatible instruction entrypoints where appropriate.
- [x] #3 Skills validate after wording updates.
- [x] #4 Devlog entry records changes and validation.
- [x] #5 Git repository exists on `development`.
<!-- DOD:END -->
