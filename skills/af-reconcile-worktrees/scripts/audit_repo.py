#!/usr/bin/env python3
"""Read-only audit for local worktrees, branches, and agent instructions."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


PRIMARY_BRANCHES = {"development", "staging", "main", "master", "production", "prod"}


def run(args: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def git(args: list[str], cwd: Path) -> str:
    code, out, err = run(["git", *args], cwd)
    if code != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {err or out}")
    return out


def repo_root(path: Path) -> Path:
    return Path(git(["rev-parse", "--show-toplevel"], path)).resolve()


def parse_worktrees(raw: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in raw.splitlines():
        if not line:
            if current:
                items.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        items.append(current)
    for item in items:
        ref = item.get("branch", "")
        item["branch_name"] = ref.removeprefix("refs/heads/") if ref else "(detached)"
    return items


def status_short(path: Path) -> list[str]:
    out = git(["-C", str(path), "status", "--short"], path)
    return [line for line in out.splitlines() if line]


def branch_exists(root: Path, branch: str) -> bool:
    code, _, _ = run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"], root)
    return code == 0


def is_ancestor(root: Path, child: str, parent: str) -> bool | None:
    if not branch_exists(root, parent):
        return None
    code, _, _ = run(["git", "merge-base", "--is-ancestor", child, parent], root)
    return code == 0


def ahead_behind(root: Path, left: str, right: str) -> tuple[int, int] | None:
    code, out, _ = run(["git", "rev-list", "--left-right", "--count", f"{left}...{right}"], root)
    if code != 0 or not out:
        return None
    left_only, right_only = out.split()
    return int(left_only), int(right_only)


def local_branches(root: Path) -> list[dict[str, Any]]:
    fmt = "%(refname:short)|%(objectname)|%(upstream:short)|%(HEAD)"
    out = git(["for-each-ref", f"--format={fmt}", "refs/heads"], root)
    branches: list[dict[str, Any]] = []
    for line in out.splitlines():
        name, commit, upstream, head = (line.split("|") + ["", "", "", ""])[:4]
        merged = is_ancestor(root, name, "development") if name != "development" else True
        remote_state = ahead_behind(root, upstream, name) if upstream else None
        branches.append(
            {
                "name": name,
                "commit": commit[:12],
                "upstream": upstream or None,
                "current": head == "*",
                "merged_to_development": merged,
                "remote_behind_ahead": remote_state,
            }
        )
    return branches


def read_optional(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None


def agents_review(root: Path) -> dict[str, Any]:
    home = Path.home()
    af_home = Path(os.environ.get("AF_HOME", os.environ.get("AGENT_FLOW_HOME", home / ".agent-flow")))
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex"))
    global_flow = af_home / "AGENT-FLOW.md"
    global_agents = codex_home / "AGENTS.md"
    global_claude = Path(os.environ.get("CLAUDE_HOME", home / ".claude")) / "CLAUDE.md"
    af_push_skill = af_home / "skills" / "af-push-staging" / "SKILL.md"
    if not af_push_skill.exists():
        af_push_skill = codex_home / "skills" / "af-push-staging" / "SKILL.md"
    legacy_push_skill = codex_home / "skills" / "push-staging" / "SKILL.md"
    push_skill = af_push_skill if af_push_skill.exists() else legacy_push_skill
    instruction_names = {"AGENT-FLOW.md", "AGENTS.md", "CLAUDE.md"}
    local_agents = sorted(path for path in root.rglob("*.md") if path.name in instruction_names)
    local_agents = [
        path
        for path in local_agents
        if ".git" not in path.parts and "node_modules" not in path.parts
    ]

    global_flow_text = read_optional(global_flow)
    global_text = read_optional(global_agents)
    global_claude_text = read_optional(global_claude)
    push_text = read_optional(push_skill)
    concerns: list[str] = []

    if global_flow_text is None:
        concerns.append(f"Global AGENT-FLOW.md missing: {global_flow}")
    else:
        required = ("development", "staging", "main", "protected")
        missing = [word for word in required if word.lower() not in global_flow_text.lower()]
        if missing:
            concerns.append(f"Global AGENT-FLOW.md may be missing branch-rule terms: {', '.join(missing)}")

    if global_text is None:
        concerns.append(f"Global AGENTS.md adapter missing: {global_agents}")
    if global_claude_text is None:
        concerns.append(f"Global CLAUDE.md adapter missing: {global_claude}")

    if push_text is None:
        concerns.append(f"af-push-staging or push-staging skill missing or unreadable: {push_skill}")

    for path in local_agents:
        text = read_optional(path) or ""
        lower = text.lower()
        main_work = re.search(r"(work|commit|change|push)\s+(directly\s+)?(to|on)\s+`?main`?", lower)
        if main_work and "pull request" not in lower and " pr " not in f" {lower} ":
            concerns.append(f"{path} may allow direct work on main.")
        if "git branch -d" in lower or "worktree remove" in lower:
            if "approval" not in lower and "ask" not in lower:
                concerns.append(f"{path} mentions branch/worktree removal without an obvious approval rule.")

    return {
        "global_agent_flow": str(global_flow),
        "global_agents_adapter": str(global_agents),
        "global_claude_adapter": str(global_claude),
        "local_instruction_files": [str(path) for path in local_agents],
        "push_staging_skill": str(push_skill),
        "concerns": concerns,
    }


def classify_worktree(root: Path, item: dict[str, str]) -> dict[str, Any]:
    path = Path(item["worktree"])
    branch = item.get("branch_name", "(detached)")
    head = item.get("HEAD", "")
    status = status_short(path)
    target = branch if branch != "(detached)" else head
    merged = is_ancestor(root, target, "development") if target else None

    if branch in PRIMARY_BRANCHES:
        action = f"keep protected {branch} worktree"
    elif status:
        action = "skip dirty worktree"
    elif merged is True:
        action = "eligible for worktree removal"
    elif merged is False:
        action = "skip; commits not merged to development"
    else:
        action = "skip; cannot verify development ancestry"

    return {
        "path": str(path),
        "branch": branch,
        "head": head[:12],
        "dirty_count": len(status),
        "merged_to_development": merged,
        "action": action,
    }


def build_report(path: Path) -> dict[str, Any]:
    root = repo_root(path)
    current_branch = git(["branch", "--show-current"], root) or "(detached)"
    worktrees = [
        classify_worktree(root, item)
        for item in parse_worktrees(git(["worktree", "list", "--porcelain"], root))
    ]
    branches = local_branches(root)
    dev_branch = next((branch for branch in branches if branch["name"] == "development"), None)
    local_main = next((branch for branch in branches if branch["name"] == "main"), None)
    dev_worktree = next((worktree for worktree in worktrees if worktree["branch"] == "development"), None)

    branch_actions = []
    for branch in branches:
        name = branch["name"]
        if name in {"development", "staging"}:
            action = "keep"
        elif name == "main":
            action = "ask to remove local main"
        elif branch["current"]:
            action = "skip checked-out branch"
        elif branch["merged_to_development"] is True:
            action = "ask to delete merged branch"
        elif branch["merged_to_development"] is False:
            action = "skip; not merged to development"
        else:
            action = "skip; cannot verify"
        branch_actions.append({**branch, "action": action})

    return {
        "repo": str(root),
        "current_branch": current_branch,
        "development": dev_branch,
        "development_worktree": dev_worktree,
        "local_main_present": local_main is not None,
        "worktrees": worktrees,
        "branches": branch_actions,
        "agents": agents_review(root),
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Reconcile audit: {report['repo']}",
        "",
        f"- Current branch: `{report['current_branch']}`",
        f"- Local `main` present: {'yes' if report['local_main_present'] else 'no'}",
    ]
    dev = report.get("development")
    if dev:
        remote = dev.get("remote_behind_ahead")
        remote_text = f", upstream behind/ahead: {remote[0]}/{remote[1]}" if remote else ""
        lines.append(f"- Development: `{dev['commit']}`{remote_text}")
    else:
        lines.append("- Development: missing local branch")
    dev_wt = report.get("development_worktree")
    if dev_wt:
        lines.append(f"- Development worktree changes: {dev_wt['dirty_count']}")

    lines += ["", "## Worktrees"]
    for wt in report["worktrees"]:
        dirty = "dirty" if wt["dirty_count"] else "clean"
        lines.append(f"- `{wt['branch']}` at `{wt['path']}`: {dirty}, merged={wt['merged_to_development']}, {wt['action']}")

    lines += ["", "## Branches"]
    for branch in report["branches"]:
        lines.append(f"- `{branch['name']}`: merged={branch['merged_to_development']}, {branch['action']}")

    lines += ["", "## Agent Instruction Review"]
    concerns = report["agents"]["concerns"]
    if concerns:
        for concern in concerns:
            lines.append(f"- Concern: {concern}")
    else:
        lines.append("- No heuristic conflicts found.")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Path inside the target git repo")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    report = build_report(Path(args.repo).resolve())
    print(json.dumps(report, indent=2) if args.json else markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
