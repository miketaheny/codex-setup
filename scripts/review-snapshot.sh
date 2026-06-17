#!/usr/bin/env bash
set -euo pipefail

BASE="${1:-development}"

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run this inside a git repository." >&2
  exit 1
fi

branch="$(git branch --show-current)"
echo "Branch: $branch"
echo "Base: $BASE"
echo

echo "== Git status =="
git status --short

echo
echo "== Diff stat against $BASE =="
git diff --stat "$BASE"...HEAD || true

echo
echo "== Staged diff stat =="
git diff --cached --stat || true

echo
echo "== Working tree diff stat =="
git diff --stat || true

echo
echo "== Recent commits =="
git log --oneline --decorate --max-count=10 "$BASE"..HEAD || true

echo
echo "Review with your agent: Use af-review-gate and inspect this snapshot."
