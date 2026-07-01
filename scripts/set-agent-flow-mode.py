#!/usr/bin/env python3
"""Enable or disable Agent-Flow enforcement in the current Git repo."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


MINIMAL_DISABLED = """version = 1
enabled = false
mode = "disabled"

# This repo explicitly opts out of Agent-Flow enforcement.
# Run `~/.agent-flow/scripts/init-repo.sh --force --enforced` or use `af-enable` to re-enable.
"""


def git_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit("Error: run this inside a git repository.")
    return Path(result.stdout.strip())


def replace_or_insert(lines: list[str], key: str, value: str) -> list[str]:
    prefix = f"{key} ="
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = f"{key} = {value}\n"
            return lines
    insert_at = 1 if lines and lines[0].startswith("version =") else 0
    lines.insert(insert_at, f"{key} = {value}\n")
    return lines


def set_mode(config: Path, mode: str) -> None:
    if mode == "disabled" and not config.exists():
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(MINIMAL_DISABLED, encoding="utf-8")
        return

    if not config.exists():
        raise SystemExit(
            "Error: no .agent-flow/config.toml exists. Run init-repo.sh to enable Agent-Flow."
        )

    lines = config.read_text(encoding="utf-8").splitlines(keepends=True)
    enabled = "false" if mode == "disabled" else "true"
    lines = replace_or_insert(lines, "enabled", enabled)
    lines = replace_or_insert(lines, "mode", f'"{mode}"')
    config.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--disable", action="store_true")
    group.add_argument("--enable", action="store_true")
    parser.add_argument("--yes", action="store_true", help="confirm the requested mutation")
    args = parser.parse_args()

    if not args.yes:
        raise SystemExit("Error: pass --yes after user confirmation.")

    root = git_root()
    config = root / ".agent-flow" / "config.toml"
    if args.disable:
        set_mode(config, "disabled")
        print(f"Agent-Flow disabled in {root}")
        print(f"Config: {config}")
    else:
        set_mode(config, "enforced")
        print(f"Agent-Flow enabled in {root}")
        print(f"Config: {config}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
