#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <branch-type> <short-task-name> [base-branch]" >&2
  echo "Example: $0 fix navbar-spacing" >&2
  echo "Example with explicit parent: $0 feat payments-redesign feat/payments" >&2
  exit 2
fi

TYPE="$1"
TASK="$2"

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run this inside a git repository." >&2
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
REPO="$(basename "$ROOT")"
PARENT="$(dirname "$ROOT")"
BRANCH="$TYPE/$TASK"
WORKTREE="$PARENT/$REPO-$TASK"
CURRENT_BRANCH="$(git branch --show-current)"
BASE="${3:-$CURRENT_BRANCH}"

cd "$ROOT"

if [ -z "$BASE" ]; then
  echo "Error: detached HEAD. Check out the parent branch you want this task to merge back into." >&2
  exit 1
fi

case "$BASE" in
  main|staging|master|production|prod)
    echo "Error: '$BASE' is protected or reserved. Check out a user-controlled parent branch such as development or feat/<name>." >&2
    exit 1
    ;;
esac

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
git config "branch.$BRANCH.agentFlowParent" "$BASE"

echo "Created worktree: $WORKTREE"
echo "Branch: $BRANCH"
echo "Parent branch: $BASE"
echo "Next: cd '$WORKTREE' and open your preferred agent CLI."
