#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"

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

if [ -z "$TARGET" ]; then
  TARGET="$(git branch --show-current)"
fi

if [ -z "$TARGET" ]; then
  echo "NOT_READY: detached HEAD cannot be pushed under Agent-Flow." >&2
  exit 1
fi

PRODUCTION_BRANCH="$(config_value production_branch main)"
STAGING_BRANCH="$(config_value staging_branch staging)"

if [ "$TARGET" = "$PRODUCTION_BRANCH" ]; then
  echo "NOT_READY: direct push to production branch '$PRODUCTION_BRANCH' is blocked." >&2
  exit 1
fi

if [ "$TARGET" = "$STAGING_BRANCH" ] && [ "${AF_ALLOW_RELEASE_PUSH:-0}" != "1" ]; then
  echo "NOT_READY: direct push to staging branch '$STAGING_BRANCH' is blocked outside release promotion." >&2
  echo "Set AF_ALLOW_RELEASE_PUSH=1 only inside the explicit release promotion workflow." >&2
  exit 1
fi

if ! git show-ref --verify --quiet "refs/heads/$TARGET"; then
  echo "NOT_READY: target branch '$TARGET' does not exist locally." >&2
  exit 1
fi

worktree_for_branch() {
  local branch="$1"
  git worktree list --porcelain | awk -v target="refs/heads/$branch" '
    /^worktree / { path=substr($0, 10) }
    /^branch / && substr($0, 8) == target { print path; found=1 }
    END { if (!found) exit 1 }
  '
}

failures=0
checked=0

while IFS= read -r line; do
  key="${line%% *}"
  parent="${line#* }"
  branch="${key#branch.}"
  branch="${branch%.agentflowparent}"

  if [ "$parent" != "$TARGET" ]; then
    continue
  fi

  if ! git show-ref --verify --quiet "refs/heads/$branch"; then
    continue
  fi

  checked=$((checked + 1))
  wt="$(worktree_for_branch "$branch" || true)"
  if [ -n "$wt" ] && [ -n "$(git -C "$wt" status --short)" ]; then
    echo "NOT_READY: child session '$branch' has dirty worktree: $wt" >&2
    git -C "$wt" status --short >&2
    failures=$((failures + 1))
    continue
  fi

  if ! git merge-base --is-ancestor "$branch" "$TARGET"; then
    echo "NOT_READY: child session '$branch' is not merged into '$TARGET'." >&2
    failures=$((failures + 1))
  fi
done < <(git config --get-regexp '^branch\..*\.agentflowparent$' || true)

check_worktree_child() {
  local wt="$1"
  local head="$2"
  local parent

  parent="$(git -C "$wt" config --worktree --get agentFlow.parent 2>/dev/null || true)"
  if [ "$parent" != "$TARGET" ]; then
    return
  fi

  checked=$((checked + 1))
  if [ -z "$head" ]; then
    echo "NOT_READY: child session worktree has no recorded HEAD: $wt" >&2
    failures=$((failures + 1))
    return
  fi

  if [ -n "$(git -C "$wt" status --short)" ]; then
    echo "NOT_READY: child session worktree has dirty changes: $wt" >&2
    git -C "$wt" status --short >&2
    failures=$((failures + 1))
    return
  fi

  if ! git merge-base --is-ancestor "$head" "$TARGET"; then
    echo "NOT_READY: child session worktree is not merged into '$TARGET': $wt" >&2
    echo "  HEAD: $(git -C "$wt" rev-parse --short HEAD)" >&2
    failures=$((failures + 1))
  fi
}

wt_path=""
wt_head=""
wt_branch=""
while IFS= read -r line; do
  if [ -z "$line" ]; then
    if [ -n "$wt_path" ] && [ -z "$wt_branch" ]; then
      check_worktree_child "$wt_path" "$wt_head"
    fi
    wt_path=""
    wt_head=""
    wt_branch=""
    continue
  fi

  key="${line%% *}"
  value="${line#* }"
  case "$key" in
    worktree) wt_path="$value" ;;
    HEAD) wt_head="$value" ;;
    branch) wt_branch="$value" ;;
  esac
done < <(git worktree list --porcelain)

if [ -n "$wt_path" ] && [ -z "$wt_branch" ]; then
  check_worktree_child "$wt_path" "$wt_head"
fi

if [ "$failures" -gt 0 ]; then
  echo "Push readiness failed for '$TARGET': $failures incomplete child session(s)." >&2
  exit 1
fi

echo "PUSH_READY: '$TARGET' has no incomplete child session worktrees. Checked child sessions: $checked."
