#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

args=("--class" "normal")
if [ -n "$PARENT" ]; then
  args+=("--parent" "$PARENT")
fi
if [ -n "$BRANCH" ]; then
  args+=("--branch" "$BRANCH")
fi

"$SCRIPT_DIR/start-task.sh" "${args[@]}" "$1" "$2"
