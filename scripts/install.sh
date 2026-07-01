#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AF_HOME="${AF_HOME:-${AGENT_FLOW_HOME:-$HOME/.agent-flow}}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
STAMP="$(date +%Y%m%d-%H%M%S)"

backup_if_exists() {
  local path="$1"
  if [ -f "$path" ]; then
    cp "$path" "$path.backup-$STAMP"
    echo "Backed up existing $path to $path.backup-$STAMP"
  fi
}

copy_if_missing() {
  local src="$1"
  local dest="$2"
  if [ -f "$dest" ]; then
    echo "Exists: $dest"
  else
    cp "$src" "$dest"
    echo "Created: $dest"
  fi
}

install_codex_profiles() {
  copy_if_missing "$SRC_DIR/templates/codex-fast.config.toml" "$CODEX_HOME/fast.config.toml"
  copy_if_missing "$SRC_DIR/templates/codex-review.config.toml" "$CODEX_HOME/review.config.toml"
  copy_if_missing "$SRC_DIR/templates/codex-deep.config.toml" "$CODEX_HOME/deep.config.toml"
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
  rm -f "$home/CLAUDE.md" "$home/templates/repo-CLAUDE.md"
}

remove_legacy_claude_install() {
  local claude_home="${CLAUDE_HOME:-$HOME/.claude}"

  if [ ! -d "$claude_home" ]; then
    return
  fi

  rm -f "$claude_home/AGENT-FLOW.md"
  rm -f "$claude_home/CLAUDE.md"
  rm -f "$claude_home"/CLAUDE.md.backup-*
  rm -rf "$claude_home/docs"
  rm -rf "$claude_home/templates"
  rm -rf "$claude_home/skills"/af-*

  for script in \
    check-branch-safety.sh \
    check-push-readiness.sh \
    claude-review.sh \
    finish-session.sh \
    generate-agent-flow-walkthrough-pdf.py \
    generate-codex-fast-path-pdf.py \
    init-repo.sh \
    install-hooks.sh \
    install.sh \
    set-agent-flow-mode.py \
    start-session.sh \
    worktree-manager.py; do
    rm -f "$claude_home/scripts/$script"
  done

  rmdir "$claude_home/scripts" "$claude_home/skills" 2>/dev/null || true
}

mkdir -p "$AF_HOME" "$CODEX_HOME"

backup_if_exists "$AF_HOME/AGENT-FLOW.md"
backup_if_exists "$CODEX_HOME/AGENTS.md"

cp "$SRC_DIR/AGENT-FLOW.md" "$AF_HOME/AGENT-FLOW.md"
mkdir -p "$AF_HOME/skills" "$AF_HOME/templates" "$AF_HOME/scripts" "$AF_HOME/docs"
remove_retired "$AF_HOME"
cp -R "$SRC_DIR/skills/." "$AF_HOME/skills/"
cp -R "$SRC_DIR/templates/." "$AF_HOME/templates/"
cp -R "$SRC_DIR/scripts/." "$AF_HOME/scripts/"
cp -R "$SRC_DIR/docs/." "$AF_HOME/docs/"
chmod +x "$AF_HOME/scripts/"*.sh 2>/dev/null || true

# Codex install surface.
cp "$SRC_DIR/AGENTS.md" "$CODEX_HOME/AGENTS.md"
cp "$SRC_DIR/AGENT-FLOW.md" "$CODEX_HOME/AGENT-FLOW.md"
mkdir -p "$CODEX_HOME/skills" "$CODEX_HOME/templates" "$CODEX_HOME/scripts" "$CODEX_HOME/docs"
remove_retired "$CODEX_HOME"
cp -R "$SRC_DIR/skills/." "$CODEX_HOME/skills/"
cp -R "$SRC_DIR/templates/." "$CODEX_HOME/templates/"
cp -R "$SRC_DIR/scripts/." "$CODEX_HOME/scripts/"
cp -R "$SRC_DIR/docs/." "$CODEX_HOME/docs/"
chmod +x "$CODEX_HOME/scripts/"*.sh 2>/dev/null || true
install_codex_profiles
remove_legacy_claude_install

echo "Installed AF Agent-Flow setup to $AF_HOME"
echo "Installed Codex-focused adapter and skills to $CODEX_HOME"
echo "Claude CLI is supported only as an optional external review tool via af-claude-review."
echo "Next: open a repo and run: $AF_HOME/scripts/init-repo.sh"
