#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_HOME="$(cd "$SCRIPT_DIR/.." && pwd)"
AF_HOME="${AF_HOME:-${AGENT_FLOW_HOME:-$HOME/.agent-flow}}"

if [ ! -d "$AF_HOME/templates" ]; then
  AF_HOME="$SCRIPT_HOME"
fi

FORCE=0
YES=0
MODE=""
STAGING_CHOICE=""
HOOKS_CHOICE=""
INTEGRATION_BRANCH="development"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --force)
      FORCE=1
      ;;
    --yes)
      YES=1
      ;;
    --disabled)
      MODE="disabled"
      ;;
    --enforced)
      MODE="enforced"
      ;;
    --staging)
      STAGING_CHOICE="true"
      ;;
    --no-staging)
      STAGING_CHOICE="false"
      ;;
    --install-hooks)
      HOOKS_CHOICE="true"
      ;;
    --no-hooks)
      HOOKS_CHOICE="false"
      ;;
    --integration-branch)
      shift
      if [ "$#" -eq 0 ]; then
        echo "Error: --integration-branch requires a branch name." >&2
        exit 2
      fi
      INTEGRATION_BRANCH="$1"
      ;;
    -h|--help)
      echo "Usage: $0 [--force] [--yes] [--enforced|--disabled] [--staging|--no-staging] [--install-hooks|--no-hooks] [--integration-branch <branch>]" >&2
      exit 0
      ;;
    *)
      echo "Error: unknown argument: $1" >&2
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

CONFIG_DIR=".agent-flow"
CONFIG_FILE="$CONFIG_DIR/config.toml"
REPO_HELPER_SCRIPTS=(
  "check-branch-safety.sh"
  "check-push-readiness.sh"
  "finish-session.sh"
  "install-hooks.sh"
  "start-session.sh"
  "worktree-manager.py"
)

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

ensure_repo_helpers() {
  local helper src dest verb

  mkdir -p scripts

  for helper in "${REPO_HELPER_SCRIPTS[@]}"; do
    src="$AF_HOME/scripts/$helper"
    if [ ! -f "$src" ]; then
      src="$SCRIPT_HOME/scripts/$helper"
    fi
    if [ ! -f "$src" ]; then
      echo "Warning: Agent-Flow helper missing; skipped scripts/$helper" >&2
      continue
    fi

    dest="scripts/$helper"
    if [ -e "$dest" ] && [ "$FORCE" -ne 1 ]; then
      echo "Exists: $dest"
      continue
    fi

    if [ -e "$dest" ]; then
      verb="Updated"
    else
      verb="Created"
    fi
    cp "$src" "$dest"
    chmod +x "$dest" 2>/dev/null || true
    echo "$verb: $dest"
  done
}

prompt_yes_no() {
  local question="$1"
  local default="$2"
  local answer

  if [ "$YES" -eq 1 ]; then
    printf '%s\n' "$default"
    return
  fi

  if [ "$default" = "yes" ]; then
    read -r -p "$question [Y/n] " answer
    case "${answer:-Y}" in
      y|Y|yes|YES) printf '%s\n' "yes" ;;
      *) printf '%s\n' "no" ;;
    esac
  else
    read -r -p "$question [y/N] " answer
    case "${answer:-N}" in
      y|Y|yes|YES) printf '%s\n' "yes" ;;
      *) printf '%s\n' "no" ;;
    esac
  fi
}

if [ -f "$CONFIG_FILE" ] && [ "$FORCE" -ne 1 ]; then
  ensure_repo_helpers
  echo "Agent-Flow already initialized: $CONFIG_FILE"
  echo "Repo helper scripts checked."
  echo "Use --force to rewrite repo choices and refresh Agent-Flow-owned helpers."
  exit 0
fi

mkdir -p "$CONFIG_DIR"

mkdir -p docs/decisions docs/solutions docs/plans docs/diagrams docs/assets docs/presentations devlog

copy_if_missing "$AF_HOME/templates/repo-AGENT-FLOW.md" "AGENT-FLOW.md"
copy_if_missing "$AF_HOME/templates/repo-AGENTS.md" "AGENTS.md"
copy_if_missing "$AF_HOME/templates/repo-CLAUDE.md" "CLAUDE.md"
copy_if_missing "$AF_HOME/templates/devlog-README.md" "devlog/README.md"
ensure_repo_helpers

if [ ! -f "docs/decisions/000-template.md" ]; then
  cp "$AF_HOME/templates/DECISION.md" "docs/decisions/000-template.md"
  echo "Created: docs/decisions/000-template.md"
fi

ensure_gitignore() {
  local gitignore=".gitignore"
  local block="$AF_HOME/templates/repo-gitignore-block"

  if [ ! -f "$block" ]; then
    block="$SCRIPT_HOME/templates/repo-gitignore-block"
  fi

  if [ ! -f "$block" ]; then
    echo "Warning: Agent-Flow gitignore template missing; skipped .gitignore update." >&2
    return
  fi

  if [ ! -f "$gitignore" ]; then
    {
      echo "# agent-flow-gitignore-start"
      cat "$block"
      echo "# agent-flow-gitignore-end"
    } > "$gitignore"
    echo "Created: .gitignore"
    return
  fi

  if grep -q "agent-flow-gitignore-start" "$gitignore"; then
    echo "Exists: .gitignore Agent-Flow block"
    return
  fi

  {
    echo
    echo "# agent-flow-gitignore-start"
    cat "$block"
    echo "# agent-flow-gitignore-end"
  } >> "$gitignore"
  echo "Updated: .gitignore"
}

ensure_gitignore

if [ -z "$MODE" ]; then
  disable="$(prompt_yes_no "Disable Agent-Flow enforcement for this repo?" "no")"
  if [ "$disable" = "yes" ]; then
    MODE="disabled"
  else
    MODE="enforced"
  fi
fi

if [ -z "$STAGING_CHOICE" ]; then
  if [ "$MODE" = "disabled" ]; then
    STAGING_CHOICE="false"
  else
    staging_answer="$(prompt_yes_no "Does this repo use a staging branch between development and main?" "yes")"
    if [ "$staging_answer" = "yes" ]; then
      STAGING_CHOICE="true"
    else
      STAGING_CHOICE="false"
    fi
  fi
fi

if [ "$MODE" = "disabled" ]; then
  ENABLED="false"
else
  ENABLED="true"
fi

if [ -z "$HOOKS_CHOICE" ]; then
  if [ "$MODE" = "disabled" ]; then
    HOOKS_CHOICE="false"
  else
    hooks_answer="$(prompt_yes_no "Install a local pre-push hook to check child session worktrees before push?" "yes")"
    if [ "$hooks_answer" = "yes" ]; then
      HOOKS_CHOICE="true"
    else
      HOOKS_CHOICE="false"
    fi
  fi
fi

PROTECTED='["main", "staging"]'
FLOW="development -> main"
STAGING_NOTE="Staging: disabled. Do not assume a staging branch unless .agent-flow/config.toml changes."
if [ "$STAGING_CHOICE" = "true" ]; then
  FLOW="development -> staging -> main"
  STAGING_NOTE="Staging: enabled. Treat staging as protected and use it only through the release PR flow unless an explicit direct-push exception is approved."
fi

cat > "$CONFIG_FILE" <<EOF
version = 1
enabled = $ENABLED
mode = "$MODE"

worktrees = "required-for-changes"
session_base = "checked-out"
session_merge_target = "parent"
session_branch = "explicit-only"
session_unit = "chat"
devlog_policy = "finish"

merge_prompt = "always"
auto_commit = "finish"
dirty_parent_policy = "review-and-commit"
devlog_filename = "date-subject"
pre_push_worktree_check = true
pre_push_hook_installed = $HOOKS_CHOICE

integration_branch = "$INTEGRATION_BRANCH"
production_branch = "main"
staging_enabled = $STAGING_CHOICE
staging_branch = "staging"
reserved_branch_names = ["master", "production", "prod"]
protected_branches = $PROTECTED

devlog = "required-for-changes"
docs = "required-when-impacted"

security_review = "optional"
formal_security_review = "when-configured-or-sensitive"
security_review_pr_bases = ["staging", "main"]
EOF

append_local_choices() {
  local file="$1"

  if [ ! -f "$file" ]; then
    return
  fi

  if grep -q "agent-flow-local-start" "$file"; then
    return
  fi

  cat >> "$file" <<EOF

<!-- agent-flow-local-start -->
## Agent-Flow Local Repo Choices

- Enforcement: $MODE via \`.agent-flow/config.toml\`.
- Session worktrees are detached by default from the checked-out parent branch and merge back there after review.
- Create named branches only when the user explicitly requests a branch.
- Merge behavior: ask before merge by default.
- Push behavior: check child session worktrees before pushing a parent branch.
- Pre-push hook installed: $HOOKS_CHOICE.
- SDLC flow: $FLOW. \`main\` is the production PR target and should not be kept as a local work branch.
- $STAGING_NOTE
- Legacy branch names \`master\`, \`production\`, and \`prod\` are reserved and should not be used as mainline branches.
<!-- agent-flow-local-end -->
EOF
}

append_local_choices "AGENTS.md"
append_local_choices "CLAUDE.md"

if [ "$HOOKS_CHOICE" = "true" ]; then
  AF_HOME="$AF_HOME" "$SCRIPT_DIR/install-hooks.sh"
fi

echo "Agent-Flow initialized at $ROOT"
echo "Config: $CONFIG_FILE"
echo "Mode: $MODE"
echo "Flow: $FLOW"
echo "Pre-push hook: $HOOKS_CHOICE"
