#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat >&2 <<'USAGE'
Usage: finish-task.sh [options]

Options:
  --merge              Merge into the recorded parent branch after readiness checks.
  --no-merge           Report readiness only, even when auto-merge config would allow it.
  --parent <branch>    Override the recorded parent branch.

Default behavior follows .agent-flow/config.toml:
  auto_commit = "finish"    -> commit dirty task work before readiness checks
  auto_merge = "off"       -> report READY and ask before merge
  auto_merge = "tiny-only" -> auto-merge only task class tiny
  auto_merge = "always"    -> auto-merge any ready task worktree
USAGE
}

REQUEST_MERGE=0
NO_MERGE=0
PARENT_OVERRIDE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --merge)
      REQUEST_MERGE=1
      ;;
    --no-merge)
      NO_MERGE=1
      ;;
    --parent)
      shift
      [ "$#" -gt 0 ] || { echo "Error: --parent requires a branch name." >&2; exit 2; }
      PARENT_OVERRIDE="$1"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown option: $1" >&2
      usage
      exit 2
      ;;
  esac
  shift
done

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

BRANCH="$(git branch --show-current)"
WORKTREE_MODE="$(git config --worktree --get agentFlow.mode 2>/dev/null || true)"

if [ -n "$BRANCH" ]; then
  case "$BRANCH" in
    main|staging|master|production|prod)
      echo "NOT_READY: current branch '$BRANCH' is protected or reserved." >&2
      exit 1
      ;;
  esac
elif [ "$WORKTREE_MODE" != "detached" ]; then
  echo "NOT_READY: detached HEAD has no Agent-Flow task metadata." >&2
  echo "Create task worktrees with scripts/start-task.sh or scripts/new-worktree.sh." >&2
  exit 1
fi

PARENT="${PARENT_OVERRIDE:-$(git config --worktree --get agentFlow.parent 2>/dev/null || true)}"
if [ -z "$PARENT" ] && [ -n "$BRANCH" ]; then
  PARENT="$(git config --get "branch.$BRANCH.agentFlowParent" || true)"
fi
if [ -z "$PARENT" ]; then
  echo "NOT_READY: task worktree has no recorded Agent-Flow parent." >&2
  if [ -n "$BRANCH" ]; then
    echo "Set it with: git config branch.$BRANCH.agentFlowParent <parent-branch>" >&2
  else
    echo "Set it with: git config --worktree agentFlow.parent <parent-branch>" >&2
  fi
  exit 1
fi

if ! git show-ref --verify --quiet "refs/heads/$PARENT"; then
  echo "NOT_READY: parent branch '$PARENT' does not exist locally." >&2
  exit 1
fi

if [ -n "$(git status --short)" ]; then
  AUTO_COMMIT="$(config_value auto_commit finish)"
  if [ "$AUTO_COMMIT" = "finish" ]; then
    "$SCRIPT_DIR/commit-task.sh"
  else
    echo "NOT_READY: task worktree has uncommitted or untracked changes." >&2
    echo "Commit or clean the task worktree before merging." >&2
    git status --short
    exit 1
  fi
fi

if ! git diff --check "$PARENT"...HEAD >/dev/null; then
  echo "NOT_READY: git diff --check failed." >&2
  git diff --check "$PARENT"...HEAD || true
  exit 1
fi

AHEAD_COUNT="$(git rev-list --count "$PARENT"..HEAD)"
if [ "$AHEAD_COUNT" = "0" ]; then
  echo "NO_CHANGE: task worktree has no commits ahead of '$PARENT'."
  exit 0
fi

DEVLOG_COUNT="$(git diff --name-only "$PARENT"...HEAD -- 'devlog/*.md' | wc -l | tr -d ' ')"
if [ "$DEVLOG_COUNT" = "0" ]; then
  echo "NOT_READY: no devlog entry changed in this task worktree." >&2
  exit 1
fi

parent_worktree() {
  local target="$1"
  git worktree list --porcelain | awk -v target="refs/heads/$target" '
    /^worktree / { path=substr($0, 10) }
    /^branch / && substr($0, 8) == target { print path; found=1 }
    END { if (!found) exit 1 }
  '
}

PARENT_WORKTREE="$(parent_worktree "$PARENT" || true)"
if [ -z "$PARENT_WORKTREE" ]; then
  echo "NOT_READY: no checked-out worktree found for parent branch '$PARENT'." >&2
  exit 1
fi

if [ -n "$(git -C "$PARENT_WORKTREE" status --short)" ]; then
  echo "NOT_READY: parent worktree '$PARENT_WORKTREE' has uncommitted changes." >&2
  git -C "$PARENT_WORKTREE" status --short
  exit 1
fi

echo "READY_TO_MERGE"
if [ -n "$BRANCH" ]; then
  echo "Branch: $BRANCH"
  MERGE_REF="$BRANCH"
else
  MERGE_REF="$(git rev-parse HEAD)"
  echo "Branch: none (detached task worktree)"
  echo "Commit: $(git rev-parse --short HEAD)"
fi
echo "Parent: $PARENT"
echo "Parent worktree: $PARENT_WORKTREE"
echo "Commits ahead: $AHEAD_COUNT"
echo "Devlog files changed: $DEVLOG_COUNT"
echo
git diff --stat "$PARENT"...HEAD

AUTO_MERGE="$(config_value auto_merge off)"
TASK_CLASS="$(git config --worktree --get agentFlow.taskClass 2>/dev/null || true)"
if [ -z "$TASK_CLASS" ] && [ -n "$BRANCH" ]; then
  TASK_CLASS="$(git config --get "branch.$BRANCH.agentFlowTaskClass" || true)"
fi
TASK_CLASS="${TASK_CLASS:-normal}"

SHOULD_MERGE=0
if [ "$REQUEST_MERGE" -eq 1 ]; then
  SHOULD_MERGE=1
elif [ "$NO_MERGE" -eq 0 ]; then
  case "$AUTO_MERGE" in
    always)
      SHOULD_MERGE=1
      ;;
    tiny-only)
      if [ "$TASK_CLASS" = "tiny" ]; then
        SHOULD_MERGE=1
      fi
      ;;
  esac
fi

if [ "$SHOULD_MERGE" -ne 1 ]; then
  echo
  echo "ASK_USER_MERGE: run this after approval:"
  echo "  $SCRIPT_DIR/finish-task.sh --merge"
  exit 0
fi

git -C "$PARENT_WORKTREE" merge --no-ff "$MERGE_REF"
if [ -n "$BRANCH" ]; then
  git config "branch.$BRANCH.agentFlowState" "merged"
  git config "branch.$BRANCH.agentFlowMergedAt" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
else
  git config --worktree agentFlow.state "merged"
  git config --worktree agentFlow.mergedAt "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
fi

echo "MERGED: ${BRANCH:-$(git rev-parse --short HEAD)} -> $PARENT"
