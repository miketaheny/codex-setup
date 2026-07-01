#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage: scripts/claude-review.sh [<base> [<head>]]

Runs Claude CLI as an optional external reviewer for the current Git diff.
Defaults to the worktree's recorded Agent-Flow parent branch and HEAD.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if ! command -v claude >/dev/null 2>&1; then
  cat >&2 <<'EOF'
Error: Claude CLI was not found on PATH.

Install and authenticate Claude CLI first, then rerun:
  scripts/claude-review.sh [<base> [<head>]]
EOF
  exit 127
fi

AUTH_STATUS="$(claude auth status 2>/dev/null || true)"
if ! printf '%s\n' "$AUTH_STATUS" | grep -q '"loggedIn"[[:space:]]*:[[:space:]]*true'; then
  cat >&2 <<'EOF'
Error: Claude CLI is installed but not authenticated.

Run this once in a terminal, then rerun the review:
  claude auth login
EOF
  exit 126
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run inside a Git repository." >&2
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

BASE="${1:-$(git config --worktree --get agentFlow.parent || true)}"
HEAD_REF="${2:-HEAD}"

if [ -z "$BASE" ]; then
  BASE="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || true)"
fi

if [ -z "$BASE" ]; then
  BASE="HEAD~1"
fi

if ! git rev-parse --verify "$BASE" >/dev/null 2>&1; then
  echo "Error: base ref not found: $BASE" >&2
  exit 2
fi

if ! git rev-parse --verify "$HEAD_REF" >/dev/null 2>&1; then
  echo "Error: head ref not found: $HEAD_REF" >&2
  exit 2
fi

TMPDIR="${TMPDIR:-/tmp}"
PROMPT_FILE="$(mktemp "$TMPDIR/af-claude-review.XXXXXX.md")"
trap 'rm -f "$PROMPT_FILE"' EXIT

{
  echo "# Agent-Flow External Review"
  echo
  echo "You are reviewing an Agent-Flow session diff as an external reviewer for Codex."
  echo "Prioritize correctness bugs, regressions, security/privacy issues, broken docs, missing validation, and risky workflow changes."
  echo "Do not praise. Lead with findings ordered by severity."
  echo
  echo "Use this output format:"
  echo
  echo "Findings"
  echo "- P1/P2/P3: <file:line if possible> <issue and impact>"
  echo
  echo "Validation Gaps"
  echo "- <gap or none>"
  echo
  echo "Verdict"
  echo "- PASS, PASS WITH RISKS, or BLOCKED"
  echo
  echo "Base: $BASE"
  echo "Head: $HEAD_REF"
  echo
  echo "## Status"
  git status --short --branch
  echo
  echo "## Diff Stat"
  git diff --stat "$BASE...$HEAD_REF"
  echo
  echo "## Changed Files"
  git diff --name-only "$BASE...$HEAD_REF"
  echo
  echo "## Diff"
  git diff --no-ext-diff --find-renames "$BASE...$HEAD_REF"
} > "$PROMPT_FILE"

echo "Running Claude CLI review for $BASE...$HEAD_REF" >&2
claude -p "$(cat "$PROMPT_FILE")"
