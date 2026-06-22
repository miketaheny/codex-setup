#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AF_HOME="${AF_HOME:-${AGENT_FLOW_HOME:-$HOME/.agent-flow}}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
STAMP="$(date +%Y%m%d-%H%M%S)"

backup_if_exists() {
  local path="$1"
  if [ -f "$path" ]; then
    cp "$path" "$path.backup-$STAMP"
    echo "Backed up existing $path to $path.backup-$STAMP"
  fi
}

remove_retired() {
  local home="$1"
  local skill script
  for skill in \
    af-small-change \
    af-worktree-task \
    af-finish-session \
    af-review-gate \
    af-reconcile-worktrees \
    af-release-pr \
    af-compound-mode \
    af-flow-finish \
    af-push-staging; do
    rm -rf "$home/skills/$skill"
  done
  for script in \
    bootstrap-repo.sh \
    commit-task.sh \
    finish-task.sh \
    new-worktree.sh \
    review-snapshot.sh \
    start-task.sh; do
    rm -f "$home/scripts/$script"
  done
}

mkdir -p "$AF_HOME" "$CODEX_HOME" "$CLAUDE_HOME"

backup_if_exists "$AF_HOME/AGENT-FLOW.md"
backup_if_exists "$CODEX_HOME/AGENTS.md"
backup_if_exists "$CLAUDE_HOME/CLAUDE.md"

cp "$SRC_DIR/AGENT-FLOW.md" "$AF_HOME/AGENT-FLOW.md"
mkdir -p "$AF_HOME/skills" "$AF_HOME/templates" "$AF_HOME/scripts" "$AF_HOME/docs"
remove_retired "$AF_HOME"
cp -R "$SRC_DIR/skills/." "$AF_HOME/skills/"
cp -R "$SRC_DIR/templates/." "$AF_HOME/templates/"
cp -R "$SRC_DIR/scripts/." "$AF_HOME/scripts/"
cp -R "$SRC_DIR/docs/." "$AF_HOME/docs/"
chmod +x "$AF_HOME/scripts/"*.sh 2>/dev/null || true

# Codex-compatible install surface.
cp "$SRC_DIR/AGENTS.md" "$CODEX_HOME/AGENTS.md"
cp "$SRC_DIR/AGENT-FLOW.md" "$CODEX_HOME/AGENT-FLOW.md"
mkdir -p "$CODEX_HOME/skills" "$CODEX_HOME/templates" "$CODEX_HOME/scripts" "$CODEX_HOME/docs"
remove_retired "$CODEX_HOME"
cp -R "$SRC_DIR/skills/." "$CODEX_HOME/skills/"
cp -R "$SRC_DIR/templates/." "$CODEX_HOME/templates/"
cp -R "$SRC_DIR/scripts/." "$CODEX_HOME/scripts/"
cp -R "$SRC_DIR/docs/." "$CODEX_HOME/docs/"
chmod +x "$CODEX_HOME/scripts/"*.sh 2>/dev/null || true

# Claude-compatible install surface.
cp "$SRC_DIR/CLAUDE.md" "$CLAUDE_HOME/CLAUDE.md"
cp "$SRC_DIR/AGENT-FLOW.md" "$CLAUDE_HOME/AGENT-FLOW.md"

echo "Installed AF Agent-Flow setup to $AF_HOME"
echo "Installed Codex adapter and skills to $CODEX_HOME"
echo "Installed Claude adapter to $CLAUDE_HOME"
echo "Next: open a repo and run: $AF_HOME/scripts/init-repo.sh"
