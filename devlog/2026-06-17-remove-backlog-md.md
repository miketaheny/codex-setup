# Remove Backlog.md

- Date: 2026-06-17
- Branch/worktree: unavailable; `/Users/taheny/vault/teamt/codex-setup` is not a Git repository.
- Commit subject: `chore: remove Backlog.md tooling`
- Commit SHA: not available

## Goal

Remove the local Backlog.md install and stop AF/Codex skills from depending on Backlog task state.

## Files Changed

- `README.md` - removed Backlog task wording from reconciliation usage.
- `docs/WORKFLOW.md` - removed Backlog task wording from staging promotion guidance.
- `docs/AGENT-PROMPTS.md` - removed Backlog task wording from prompt examples.
- `skills/af-reconcile-worktrees/SKILL.md` - removed Backlog task workflow instructions.
- `skills/af-reconcile-worktrees/scripts/audit_repo.py` - removed Backlog and `.backlog` parsing.
- `/Users/taheny/.codex/skills/reconcile-worktrees/SKILL.md` - removed Backlog task workflow instructions from the installed skill.
- `/Users/taheny/.codex/skills/reconcile-worktrees/agents/openai.yaml` - removed Backlog wording from the installed skill prompt.
- `/Users/taheny/.codex/skills/reconcile-worktrees/scripts/audit_repo.py` - removed Backlog parsing from the installed helper.
- `backlog/` - removed the local Backlog task-store directory from this setup repo.

## Machine Changes

- Uninstalled Homebrew formula `backlog-md`.
- Removed `/opt/homebrew/bin/backlog` through the Homebrew uninstall.
- Removed leftover Homebrew lock file `/opt/homebrew/var/homebrew/locks/backlog-md.formula.lock`.
- Uninstalled `com.local.backlog-command-center` LaunchAgent.
- Removed `~/Library/Application Support/Backlog Command Center`.
- Removed `~/Library/Logs/Backlog Command Center`.

## Decisions

- Kept the `reconcile-worktrees` skill, but removed its Backlog dependency because it still provides useful worktree, branch, and instruction-conflict auditing.
- Left unrelated project repositories and their task data outside this setup repo untouched. A machine-wide deletion of every `backlog/`, `.backlog/`, or `Backlog.md` file would remove project data across multiple repos.

## Validation

- `brew list --formula | rg '^backlog-md$'` - no match.
- `which -a backlog backlog.md backlog-md` - no commands found.
- `find /opt/homebrew -maxdepth 4 \( -iname '*backlog*' -o -iname '*backlog.md*' \)` - no results.
- `test ! -e ~/Library/LaunchAgents/com.local.backlog-command-center.plist` - passed.
- `launchctl print gui/502/com.local.backlog-command-center` - service not found.
- `test ! -e ~/Library/Application\ Support/Backlog\ Command\ Center` - passed.
- `test ! -e ~/Library/Logs/Backlog\ Command\ Center` - passed.
- `rg -n -i "backlog(\.md|-md)?|\.backlog" ~/.codex/skills ./skills ./README.md ./docs ./commander.md` - no active skill/doc matches.
- `python3 -m py_compile skills/af-reconcile-worktrees/scripts/audit_repo.py /Users/taheny/.codex/skills/reconcile-worktrees/scripts/audit_repo.py` - passed.

## Review Result

No blocking issues found. Historical devlog entries still mention the removed tool for audit history.

## Follow-ups

- If a complete project-data purge is desired, separately review and delete each remaining project-level `backlog/`, `.backlog/`, or `Backlog.md` path.
