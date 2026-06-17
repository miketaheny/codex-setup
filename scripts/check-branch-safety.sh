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
    echo "BLOCKED: current branch '$branch' is protected or reserved. Create a task worktree from a user-controlled parent branch such as development or feat/<name>." >&2
    exit 1
    ;;
  "")
    echo "BLOCKED: detached HEAD. Check out a user-controlled parent branch before editing." >&2
    exit 1
    ;;
  *)
    echo "OK: current branch '$branch' is user-controlled."
    ;;
esac
