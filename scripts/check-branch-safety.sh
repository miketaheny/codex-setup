#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Not a git repository." >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

branch="$(git branch --show-current)"

if [ -f ".agent-flow/config.toml" ]; then
  mode="$(awk -F= '/^mode[[:space:]]*=/ {gsub(/[ "]/, "", $2); print $2; exit}' .agent-flow/config.toml)"
  if [ "$mode" = "disabled" ]; then
    echo "SKIPPED: Agent-Flow enforcement is disabled by .agent-flow/config.toml."
    exit 0
  fi
fi

case "$branch" in
  main|master|staging|production|prod)
    echo "BLOCKED: current branch '$branch' is protected or reserved. Create a task worktree from a user-controlled parent branch such as development." >&2
    exit 1
    ;;
  "")
    parent="$(git config --worktree --get agentFlow.parent 2>/dev/null || true)"
    mode="$(git config --worktree --get agentFlow.mode 2>/dev/null || true)"
    if [ "$mode" = "detached" ] && [ -n "$parent" ]; then
      echo "OK: detached Agent-Flow task worktree for parent '$parent'."
      exit 0
    fi
    echo "BLOCKED: detached HEAD without Agent-Flow task metadata. Check out a user-controlled parent branch or create a task worktree with start-task.sh." >&2
    exit 1
    ;;
  *)
    echo "OK: current branch '$branch' is user-controlled."
    ;;
esac
