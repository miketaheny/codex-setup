#!/usr/bin/env bash
set -euo pipefail

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Not a git repository." >&2
  exit 2
fi

branch="$(git branch --show-current)"
case "$branch" in
  main|master|staging|production|prod)
    echo "BLOCKED: current branch '$branch' is protected. Create a feature branch/worktree from development." >&2
    exit 1
    ;;
  "")
    echo "WARNING: detached HEAD. Be careful and create a branch before editing." >&2
    exit 1
    ;;
  *)
    echo "OK: current branch '$branch' is not protected."
    ;;
esac
