#!/usr/bin/env python3
"""Run the Agent-Flow worktree manager bundled with af-reconcile-worktrees."""

from __future__ import annotations

import runpy
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "af-reconcile-worktrees"
    / "scripts"
    / "worktree_manager.py"
)

runpy.run_path(str(SCRIPT), run_name="__main__")
