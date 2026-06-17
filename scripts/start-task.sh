#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat >&2 <<'USAGE'
Usage: start-task.sh [options] <branch-type> <short-task-name>

Options:
  --class <tiny|normal|large|risky>   Task size/risk classification. Default: normal.
  --parent <branch>                   Parent branch to branch from. Default: checked-out branch.
  --create-parent <branch>            Create and switch to a user-controlled parent branch first.
  --use-current-parent                Allow a large/risky task to branch directly from the current parent.

Examples:
  start-task.sh --class tiny fix navbar-spacing
  start-task.sh --class normal feat export-csv
  start-task.sh --class large --create-parent feat/payments feat payment-form
USAGE
}

CLASS="normal"
PARENT=""
CREATE_PARENT=""
USE_CURRENT_PARENT=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --class)
      shift
      [ "$#" -gt 0 ] || { echo "Error: --class requires a value." >&2; exit 2; }
      CLASS="$1"
      ;;
    --parent)
      shift
      [ "$#" -gt 0 ] || { echo "Error: --parent requires a branch name." >&2; exit 2; }
      PARENT="$1"
      ;;
    --create-parent)
      shift
      [ "$#" -gt 0 ] || { echo "Error: --create-parent requires a branch name." >&2; exit 2; }
      CREATE_PARENT="$1"
      ;;
    --use-current-parent)
      USE_CURRENT_PARENT=1
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
BRANCH="$TYPE/$TASK"

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

MODE="$(config_value mode enforced)"
if [ "$MODE" = "disabled" ]; then
  echo "SKIPPED: Agent-Flow enforcement is disabled by .agent-flow/config.toml."
  exit 0
fi

CURRENT_BRANCH="$(git branch --show-current)"
if [ -z "$CURRENT_BRANCH" ]; then
  echo "Error: detached HEAD. Check out a user-controlled parent branch first." >&2
  exit 1
fi

case "$CURRENT_BRANCH" in
  main|staging|master|production|prod)
    echo "Error: current branch '$CURRENT_BRANCH' is protected or reserved." >&2
    echo "Check out a user-controlled parent branch such as development or feat/<name>." >&2
    exit 1
    ;;
esac

if [ -n "$(git status --short)" ]; then
  echo "DIRTY_PARENT_REVIEW_AND_COMMIT_REQUIRED" >&2
  echo "Parent worktree has uncommitted or untracked changes." >&2
  echo "Review the diff, then run: $SCRIPT_DIR/commit-task.sh --message '<type>: <subject>'" >&2
  echo "Restart start-task after the parent worktree is clean." >&2
  exit 1
fi

if [ -n "$CREATE_PARENT" ]; then
  case "$CREATE_PARENT" in
    main|staging|master|production|prod)
      echo "Error: '$CREATE_PARENT' is protected or reserved and cannot be a task parent." >&2
      exit 1
      ;;
  esac
  if git show-ref --verify --quiet "refs/heads/$CREATE_PARENT"; then
    echo "Error: parent branch already exists: $CREATE_PARENT" >&2
    exit 1
  fi
  git switch -c "$CREATE_PARENT"
  PARENT="$CREATE_PARENT"
elif [ -z "$PARENT" ]; then
  PARENT="$CURRENT_BRANCH"
fi

INTEGRATION_BRANCH="$(config_value integration_branch development)"
if [ "$USE_CURRENT_PARENT" -ne 1 ] && [ "$PARENT" = "$INTEGRATION_BRANCH" ]; then
  case "$CLASS" in
    large|risky)
      echo "ASK_USER_LARGE_TASK_PARENT" >&2
      echo "Large/risky task requested from '$INTEGRATION_BRANCH'." >&2
      echo "Ask whether to create a feature parent branch first, then rerun with --create-parent feat/<name>." >&2
      echo "Use --use-current-parent only if the user wants this task to branch directly from '$INTEGRATION_BRANCH'." >&2
      exit 3
      ;;
  esac
fi

"$SCRIPT_DIR/new-worktree.sh" "$TYPE" "$TASK" "$PARENT"
git config "branch.$BRANCH.agentFlowTaskClass" "$CLASS"
git config "branch.$BRANCH.agentFlowState" "started"
git config "branch.$BRANCH.agentFlowStartedAt" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "Task class: $CLASS"
echo "Lifecycle: finish with $SCRIPT_DIR/finish-task.sh from the task worktree."
