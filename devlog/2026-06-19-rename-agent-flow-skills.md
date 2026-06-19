# Rename Agent-Flow skills

- Date: 2026-06-19
- Branch/worktree: development at `/Users/taheny/vault/teamt/codex-setup`
- Commit subject: `chore: rename Agent-Flow workflow skills`
- Commit SHA: pending

## Goal

Commit the local Agent-Flow skill rename set and keep the installed repo helpers pointed at the new skill locations.

## Files Changed

- `AGENT-FLOW.md`
- `docs/AGENT-PROMPTS.md`
- `scripts/worktree-manager.py`
- `skills/af-flow-finish/`
- `skills/af-reconcile/`
- `skills/af-release/`
- `skills/af-review/`
- removed superseded `skills/af-*` workflow skill directories

## Decisions

- Kept the workflow manager wrapper but updated it to load `skills/af-reconcile/scripts/worktree_manager.py`.
- Updated current prompt and skill metadata references to use `af-flow-finish`, `af-review`, `af-reconcile`, and `af-release`.
- Preserved legacy release-skill fallbacks in the reconciliation audit so older installs can still be detected.

## Validation

- `python3 /Users/taheny/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/af-flow-finish` - passed.
- `python3 /Users/taheny/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/af-reconcile` - passed.
- `python3 /Users/taheny/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/af-release` - passed.
- `python3 /Users/taheny/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/af-review` - passed.
- `python3 -m py_compile scripts/worktree-manager.py skills/af-reconcile/scripts/audit_repo.py skills/af-reconcile/scripts/worktree_manager.py` - passed.
- `scripts/worktree-manager.py` - passed and showed no child worktrees.

## Review Result

- Self-review completed for renamed skill metadata, bundled scripts, wrapper path, docs prompt updates, and devlog coverage. No P1/P2 findings found for the staged rename set.

## Follow-ups

- Refresh broader README and guide references if the renamed skill surface is intended to replace every legacy prompt in public docs.
