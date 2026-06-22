#!/usr/bin/env python3
"""Run the Agent-Flow worktree manager bundled with af-reconcile."""

from __future__ import annotations

import os
import runpy
from pathlib import Path


def candidate_roots() -> list[Path]:
    script_home = Path(__file__).resolve().parents[1]
    roots = [script_home]

    for env_name in ("AF_HOME", "AGENT_FLOW_HOME", "CODEX_HOME"):
        value = os.environ.get(env_name)
        if value:
            roots.append(Path(value).expanduser())

    roots.extend([Path.home() / ".agent-flow", Path.home() / ".codex"])

    unique_roots: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        resolved = root.resolve()
        if resolved not in seen:
            unique_roots.append(resolved)
            seen.add(resolved)
    return unique_roots


for root in candidate_roots():
    script = root / "skills" / "af-reconcile" / "scripts" / "worktree_manager.py"
    if script.is_file():
        runpy.run_path(str(script), run_name="__main__")
        raise SystemExit(0)

searched = "\n  ".join(str(root) for root in candidate_roots())
raise SystemExit(
    "Error: cannot find af-reconcile worktree_manager.py. "
    "Install Agent-Flow or set AF_HOME/AGENT_FLOW_HOME/CODEX_HOME.\n"
    f"Searched:\n  {searched}"
)
