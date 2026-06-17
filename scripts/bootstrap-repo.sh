#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_HOME="$(cd "$SCRIPT_DIR/.." && pwd)"
AF_HOME="${AF_HOME:-${AGENT_FLOW_HOME:-$HOME/.agent-flow}}"

if [ ! -d "$AF_HOME/templates" ]; then
  AF_HOME="$SCRIPT_HOME"
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run this inside a git repository." >&2
  exit 1
fi

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

mkdir -p docs/decisions docs/solutions docs/plans devlog

copy_if_missing() {
  local src="$1"
  local dest="$2"
  if [ -e "$dest" ]; then
    echo "Exists: $dest"
  else
    cp "$src" "$dest"
    echo "Created: $dest"
  fi
}

copy_if_missing "$AF_HOME/templates/repo-AGENT-FLOW.md" "AGENT-FLOW.md"
copy_if_missing "$AF_HOME/templates/repo-AGENTS.md" "AGENTS.md"
copy_if_missing "$AF_HOME/templates/repo-CLAUDE.md" "CLAUDE.md"
copy_if_missing "$AF_HOME/templates/devlog-README.md" "devlog/README.md"

if [ ! -f "docs/decisions/000-template.md" ]; then
  cp "$AF_HOME/templates/DECISION.md" "docs/decisions/000-template.md"
  echo "Created: docs/decisions/000-template.md"
fi

echo "Repo bootstrap complete at $ROOT"
