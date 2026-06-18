#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage: new-worktree.sh [options] <type> <session-name> [base-branch]

Options:
  --branch <branch-name>              Create a named branch. Use only when the user requested a branch.
  --class <tiny|normal|large|risky>   Compatibility metadata. Default: normal.

Examples:
  new-worktree.sh fix navbar-spacing
  new-worktree.sh feat payments-redesign development
  new-worktree.sh --branch fix/navbar-spacing fix navbar-spacing
USAGE
}

BRANCH=""
CLASS="normal"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --branch)
      shift
      [ "$#" -gt 0 ] || { echo "Error: --branch requires a branch name." >&2; exit 2; }
      BRANCH="$1"
      ;;
    --class)
      shift
      [ "$#" -gt 0 ] || { echo "Error: --class requires a value." >&2; exit 2; }
      CLASS="$1"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Error: unknown option: $1" >&2
      usage
      exit 2
      ;;
    *)
      break
      ;;
  esac
  shift
done

if [ "$#" -lt 2 ]; then
  usage
  exit 2
fi

TYPE="$1"
TASK="$2"

case "$CLASS" in
  tiny|normal|large|risky) ;;
  *)
    echo "Error: invalid class '$CLASS'. Use tiny, normal, large, or risky." >&2
    exit 2
    ;;
esac

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run this inside a git repository." >&2
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
REPO="$(basename "$ROOT")"
PARENT_DIR="$(dirname "$ROOT")"
WORKTREE="$PARENT_DIR/$REPO-$TASK"
CURRENT_BRANCH="$(git branch --show-current)"
BASE="${3:-$CURRENT_BRANCH}"

cd "$ROOT"

if [ -z "$BASE" ]; then
  echo "Error: detached HEAD. Check out the parent branch you want this task to merge back into." >&2
  exit 1
fi

case "$BASE" in
  main|staging|master|production|prod)
    echo "Error: '$BASE' is protected or reserved. Check out a user-controlled parent branch such as development." >&2
    exit 1
    ;;
esac

if ! git show-ref --verify --quiet "refs/heads/$BASE"; then
  echo "Error: base branch '$BASE' does not exist locally." >&2
  exit 1
fi

if [ -n "$BRANCH" ]; then
  case "$BRANCH" in
    main|staging|master|production|prod)
      echo "Error: '$BRANCH' is protected or reserved and cannot be a session branch." >&2
      exit 1
      ;;
  esac
  if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    echo "Error: branch '$BRANCH' already exists." >&2
    exit 1
  fi
fi

if [ -e "$WORKTREE" ]; then
  echo "Error: worktree path already exists: $WORKTREE" >&2
  exit 1
fi

# Worktree-local config lets detached session worktrees carry Agent-Flow metadata
# without creating a branch for every session.
git config extensions.worktreeConfig true

if [ -n "$BRANCH" ]; then
  git worktree add "$WORKTREE" -b "$BRANCH" "$BASE"
  git config "branch.$BRANCH.agentFlowParent" "$BASE"
  git config "branch.$BRANCH.agentFlowTaskClass" "$CLASS"
  git config "branch.$BRANCH.agentFlowState" "started"
  git config "branch.$BRANCH.agentFlowStartedAt" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  MODE="branch"
else
  git worktree add --detach "$WORKTREE" "$BASE"
  MODE="detached"
fi

git -C "$WORKTREE" config --worktree agentFlow.mode "$MODE"
git -C "$WORKTREE" config --worktree agentFlow.kind "session"
git -C "$WORKTREE" config --worktree agentFlow.sessionKind "codex-chat"
git -C "$WORKTREE" config --worktree agentFlow.sessionName "$TASK"
git -C "$WORKTREE" config --worktree agentFlow.parent "$BASE"
git -C "$WORKTREE" config --worktree agentFlow.taskType "$TYPE"
git -C "$WORKTREE" config --worktree agentFlow.taskName "$TASK"
git -C "$WORKTREE" config --worktree agentFlow.taskClass "$CLASS"
git -C "$WORKTREE" config --worktree agentFlow.state "started"
git -C "$WORKTREE" config --worktree agentFlow.owner "codex"
git -C "$WORKTREE" config --worktree agentFlow.devlogPolicy "finish"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
git -C "$WORKTREE" config --worktree agentFlow.startedAt "$STARTED_AT"
git -C "$WORKTREE" config --worktree agentFlow.lastTouchedAt "$STARTED_AT"
if [ -n "$BRANCH" ]; then
  git -C "$WORKTREE" config --worktree agentFlow.branch "$BRANCH"
fi

echo "Created worktree: $WORKTREE"
echo "Mode: $MODE"
if [ -n "$BRANCH" ]; then
  echo "Branch: $BRANCH"
else
  echo "Branch: none (detached session worktree)"
fi
echo "Parent branch: $BASE"
echo "Session metadata class: $CLASS"
echo "Next: cd '$WORKTREE' and open your preferred agent CLI."
