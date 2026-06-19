#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage: start-session.sh [options] <type> <session-name>

Options:
  --parent <branch>       Parent branch to create the session worktree from. Default: checked-out branch.
  --branch <branch>       Create a named branch only when explicitly requested.

Examples:
  start-session.sh feat checkout-flow
  start-session.sh docs workflow-refresh
  start-session.sh --branch feat/checkout-flow feat checkout-flow
USAGE
}

PARENT=""
BRANCH=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --parent)
      shift
      [ "$#" -gt 0 ] || { echo "Error: --parent requires a branch name." >&2; exit 2; }
      PARENT="$1"
      ;;
    --branch)
      shift
      [ "$#" -gt 0 ] || { echo "Error: --branch requires a branch name." >&2; exit 2; }
      BRANCH="$1"
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
SESSION_NAME="$2"

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run this inside a git repository." >&2
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

config_value() {
  local key="$1"
  local default="$2"
  if [ -f ".agent-flow/config.toml" ]; then
    awk -F= -v key="$key" '
      $1 ~ "^[[:space:]]*" key "[[:space:]]*$" {
        gsub(/^[[:space:]"]+|[[:space:]"]+$/, "", $2)
        print $2
        found=1
        exit
      }
      END { if (!found) exit 1 }
    ' .agent-flow/config.toml 2>/dev/null || printf '%s\n' "$default"
  else
    printf '%s\n' "$default"
  fi
}

is_protected_branch() {
  case "$1" in
    main|staging|master|production|prod) return 0 ;;
    *) return 1 ;;
  esac
}

MODE="$(config_value mode enforced)"
if [ "$MODE" = "disabled" ]; then
  echo "SKIPPED: Agent-Flow enforcement is disabled by .agent-flow/config.toml."
  exit 0
fi

CURRENT_BRANCH="$(git branch --show-current)"
if [ -z "$CURRENT_BRANCH" ]; then
  echo "Error: detached HEAD. Check out the parent branch you want this session to merge back into." >&2
  exit 1
fi

if is_protected_branch "$CURRENT_BRANCH"; then
  echo "Error: current branch '$CURRENT_BRANCH' is protected or reserved." >&2
  echo "Check out a user-controlled parent branch such as development or feat/<name>." >&2
  exit 1
fi

if [ -n "$(git status --short)" ]; then
  echo "DIRTY_PARENT_DEVLOG_COMMIT_REQUIRED" >&2
  echo "Parent worktree has uncommitted or untracked changes." >&2
  echo "Review those changes, create a devlog-backed commit for them, then start the new session from a clean parent." >&2
  exit 1
fi

if [ -z "$PARENT" ]; then
  PARENT="$CURRENT_BRANCH"
fi

if is_protected_branch "$PARENT"; then
  echo "Error: parent branch '$PARENT' is protected or reserved." >&2
  exit 1
fi

if ! git show-ref --verify --quiet "refs/heads/$PARENT"; then
  echo "Error: parent branch '$PARENT' does not exist locally." >&2
  exit 1
fi

if [ -n "$BRANCH" ]; then
  if is_protected_branch "$BRANCH"; then
    echo "Error: session branch '$BRANCH' is protected or reserved." >&2
    exit 1
  fi
  if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
    echo "Error: branch '$BRANCH' already exists." >&2
    exit 1
  fi
fi

SESSION_SLUG="$(printf '%s' "$SESSION_NAME" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//')"
if [ -z "$SESSION_SLUG" ]; then
  SESSION_SLUG="session"
fi

REPO="$(basename "$ROOT")"
PARENT_DIR="$(dirname "$ROOT")"
WORKTREE="$PARENT_DIR/$REPO-$SESSION_SLUG"

if [ -e "$WORKTREE" ]; then
  echo "Error: worktree path already exists: $WORKTREE" >&2
  exit 1
fi

git config extensions.worktreeConfig true

if [ -n "$BRANCH" ]; then
  git worktree add "$WORKTREE" -b "$BRANCH" "$PARENT"
  git config "branch.$BRANCH.agentFlowParent" "$PARENT"
  git config "branch.$BRANCH.agentFlowState" "started"
  git config "branch.$BRANCH.agentFlowStartedAt" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
else
  git worktree add --detach "$WORKTREE" "$PARENT"
fi

STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
git -C "$WORKTREE" config --worktree agentFlow.kind "session"
git -C "$WORKTREE" config --worktree agentFlow.parent "$PARENT"
git -C "$WORKTREE" config --worktree agentFlow.sessionName "$SESSION_NAME"
git -C "$WORKTREE" config --worktree agentFlow.state "started"
git -C "$WORKTREE" config --worktree agentFlow.owner "codex"
git -C "$WORKTREE" config --worktree agentFlow.devlogPolicy "finish"
git -C "$WORKTREE" config --worktree agentFlow.startedAt "$STARTED_AT"
git -C "$WORKTREE" config --worktree agentFlow.lastTouchedAt "$STARTED_AT"
if [ -n "$BRANCH" ]; then
  git -C "$WORKTREE" config --worktree agentFlow.branch "$BRANCH"
fi

echo "Created worktree: $WORKTREE"
if [ -n "$BRANCH" ]; then
  echo "Branch: $BRANCH"
else
  echo "Branch: none (detached session worktree)"
fi
echo "Parent branch: $PARENT"
echo "Session name: $SESSION_NAME"
echo "Next: cd '$WORKTREE' and re-read the repo instructions."
