#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <branch-type> <short-task-name> [base-branch]" >&2
  echo "Example: $0 fix navbar-spacing development" >&2
  exit 2
fi

TYPE="$1"
TASK="$2"
BASE="${3:-development}"

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run this inside a git repository." >&2
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
REPO="$(basename "$ROOT")"
PARENT="$(dirname "$ROOT")"
BRANCH="$TYPE/$TASK"
WORKTREE="$PARENT/$REPO-$TASK"

cd "$ROOT"

if ! git show-ref --verify --quiet "refs/heads/$BASE"; then
  echo "Error: base branch '$BASE' does not exist locally." >&2
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "Error: branch '$BRANCH' already exists." >&2
  exit 1
fi

if [ -e "$WORKTREE" ]; then
  echo "Error: worktree path already exists: $WORKTREE" >&2
  exit 1
fi

git worktree add "$WORKTREE" -b "$BRANCH" "$BASE"

echo "Created worktree: $WORKTREE"
echo "Branch: $BRANCH"
echo "Next: cd '$WORKTREE' and open your preferred agent CLI."
