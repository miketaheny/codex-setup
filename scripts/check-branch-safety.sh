#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Not a git repository." >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

branch="$(git branch --show-current)"
parent="$(git config --worktree --get agentFlow.parent 2>/dev/null || true)"
worktree_mode="$(git config --worktree --get agentFlow.mode 2>/dev/null || true)"

if [ -n "$parent" ]; then
  echo "OK: Agent-Flow worktree session for parent '$parent' (mode: ${worktree_mode:-unknown})."
  exit 0
fi

if [ -f ".agent-flow/config.toml" ]; then
  mode="$(awk -F= '/^mode[[:space:]]*=/ {gsub(/[ "]/, "", $2); print $2; exit}' .agent-flow/config.toml)"
  if [ "$mode" = "disabled" ]; then
    echo "SKIPPED: Agent-Flow enforcement is disabled by .agent-flow/config.toml."
    exit 0
  fi
fi

case "$branch" in
  main|master|staging|production|prod)
    echo "BLOCKED: current branch '$branch' is protected or reserved. Start an Agent-Flow worktree session from a user-controlled parent branch such as development." >&2
    exit 1
    ;;
  "")
    echo "BLOCKED: detached HEAD without Agent-Flow worktree metadata. Start or adopt a worktree session before changing files." >&2
    exit 1
    ;;
  *)
    echo "BLOCKED: '$branch' is a parent branch or unmanaged checkout. File-changing Codex work must happen in an Agent-Flow worktree session." >&2
    echo "Start one with: scripts/start-session.sh <type> <session-name>" >&2
    echo "If this is existing unfinished work, inspect it with: scripts/worktree-manager.py --interactive" >&2
    exit 1
    ;;
esac
