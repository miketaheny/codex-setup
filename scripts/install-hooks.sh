#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_HOME="$(cd "$SCRIPT_DIR/.." && pwd)"
AF_HOME="${AF_HOME:-${AGENT_FLOW_HOME:-$HOME/.agent-flow}}"

if [ ! -d "$AF_HOME/scripts" ]; then
  AF_HOME="$SCRIPT_HOME"
fi

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "Error: run this inside a git repository." >&2
  exit 1
fi

HOOK_PATH="$(git rev-parse --git-path hooks/pre-push)"
mkdir -p "$(dirname "$HOOK_PATH")"

if [ -f "$HOOK_PATH" ]; then
  STAMP="$(date +%Y%m%d-%H%M%S)"
  cp "$HOOK_PATH" "$HOOK_PATH.backup-$STAMP"
  echo "Backed up existing pre-push hook to $HOOK_PATH.backup-$STAMP"
fi

cat > "$HOOK_PATH" <<EOF
#!/usr/bin/env bash
set -euo pipefail

CHECK_SCRIPT="\${AF_HOME:-\${AGENT_FLOW_HOME:-$AF_HOME}}/scripts/check-push-readiness.sh"
if [ ! -x "\$CHECK_SCRIPT" ]; then
  echo "Agent-Flow pre-push hook cannot find executable check-push-readiness.sh: \$CHECK_SCRIPT" >&2
  exit 1
fi

while read -r local_ref local_sha remote_ref remote_sha; do
  case "\$local_sha" in
    0000000000000000000000000000000000000000)
      continue
      ;;
  esac

  case "\$remote_ref" in
    refs/heads/*)
      branch="\${remote_ref#refs/heads/}"
      "\$CHECK_SCRIPT" "\$branch"
      ;;
  esac
done
EOF

chmod +x "$HOOK_PATH"
echo "Installed Agent-Flow pre-push hook: $HOOK_PATH"
