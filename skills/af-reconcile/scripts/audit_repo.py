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


RESERVED_BRANCHES = {"master", "production", "prod"}


def parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().strip('"').lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return None


def read_af_config(root: Path) -> dict[str, Any]:
    config = {
        "path": str(root / ".agent-flow" / "config.toml"),
        "mode": "enforced",
        "integration_branch": "development",
        "production_branch": "main",
        "staging_enabled": None,
        "staging_branch": "staging",
    }
    text = read_optional(root / ".agent-flow" / "config.toml")
    if text is None:
        return config

    for line in text.splitlines():
        clean = line.split("#", 1)[0].strip()
        if "=" not in clean:
            continue
        key, value = [part.strip() for part in clean.split("=", 1)]
        if key in {"mode", "integration_branch", "production_branch", "staging_branch"}:
            config[key] = value.strip('"')
        elif key == "staging_enabled":
            parsed = parse_bool(value)
            if parsed is not None:
                config[key] = parsed
    return config


def protected_branches(config: dict[str, Any]) -> set[str]:
    branches = {config["production_branch"], *RESERVED_BRANCHES}
    branches.add(config["staging_branch"])
    return branches


def local_protected_branch_policy(config: dict[str, Any], branch: str) -> tuple[str, str]:
    if branch == config["production_branch"]:
        return "disallowed", "production branch should be a PR target, not a local work branch"
    if branch == config["staging_branch"]:
        if config.get("staging_enabled") is True:
            return "allowed", "configured staging release branch"
        if config.get("staging_enabled") is False:
            return "disallowed", "staging is disabled for this repo"
        return "review", "staging policy is not configured"
    if branch in RESERVED_BRANCHES:
        return "disallowed", "reserved legacy branch name"
    return "normal", ""


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


def branch_parent(root: Path, branch: str, config: dict[str, Any]) -> tuple[str, bool]:
    code, out, _ = run(["git", "config", "--get", f"branch.{branch}.agentFlowParent"], root)
    if code == 0 and out:
        return out, True
    return config["integration_branch"], False


def worktree_config(path: Path, key: str) -> str | None:
    code, out, _ = run(["git", "-C", str(path), "config", "--worktree", "--get", key], path)
    if code == 0 and out:
        return out
    return None


def worktree_metadata(path: Path) -> dict[str, str]:
    keys = (
        "agentFlow.kind",
        "agentFlow.sessionName",
        "agentFlow.parent",
        "agentFlow.state",
        "agentFlow.owner",
        "agentFlow.devlogPolicy",
        "agentFlow.startedAt",
        "agentFlow.lastTouchedAt",
        "agentFlow.finishedAt",
        "agentFlow.lastCommit",
    )
    metadata: dict[str, str] = {}
    for key in keys:
        value = worktree_config(path, key)
        if value:
            metadata[key] = value
    return metadata


def local_branches(root: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    fmt = "%(refname:short)|%(objectname)|%(upstream:short)|%(HEAD)"
    out = git(["for-each-ref", f"--format={fmt}", "refs/heads"], root)
    branches: list[dict[str, Any]] = []
    for line in out.splitlines():
        name, commit, upstream, head = (line.split("|") + ["", "", "", ""])[:4]
        merge_target, explicit_parent = branch_parent(root, name, config)
        merged = is_ancestor(root, name, merge_target) if name != merge_target else True
        remote_state = ahead_behind(root, upstream, name) if upstream else None
        branches.append(
            {
                "name": name,
                "commit": commit[:12],
                "upstream": upstream or None,
                "current": head == "*",
                "merge_target": merge_target,
                "explicit_parent": explicit_parent,
                "merged_to_target": merged,
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
    af_push_skill = af_home / "skills" / "af-release" / "SKILL.md"
    if not af_push_skill.exists():
        af_push_skill = codex_home / "skills" / "af-release" / "SKILL.md"
    push_skill = af_push_skill
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
        required = ("development", "staging", "main", "protected", "parent")
        missing = [word for word in required if word.lower() not in global_flow_text.lower()]
        if missing:
            concerns.append(f"Global AGENT-FLOW.md may be missing branch-rule terms: {', '.join(missing)}")

    if global_text is None:
        concerns.append(f"Global AGENTS.md adapter missing: {global_agents}")
    if global_claude_text is None:
        concerns.append(f"Global CLAUDE.md adapter missing: {global_claude}")

    if push_text is None:
        concerns.append(f"af-release skill missing or unreadable: {push_skill}")

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
        "release_skill": str(push_skill),
        "concerns": concerns,
    }


def classify_worktree(root: Path, item: dict[str, str], config: dict[str, Any]) -> dict[str, Any]:
    path = Path(item["worktree"])
    branch = item.get("branch_name", "(detached)")
    head = item.get("HEAD", "")
    status = status_short(path)
    target = branch if branch != "(detached)" else head
    metadata = worktree_metadata(path)
    wt_parent = worktree_config(path, "agentFlow.parent")
    if wt_parent:
        merge_target, explicit_parent = wt_parent, True
    elif branch != "(detached)":
        merge_target, explicit_parent = branch_parent(root, branch, config)
    else:
        merge_target, explicit_parent = config["integration_branch"], False
    merged = is_ancestor(root, target, merge_target) if target else None

    local_policy, local_policy_reason = (
        local_protected_branch_policy(config, branch)
        if branch != "(detached)"
        else ("normal", "")
    )
    if branch == config["integration_branch"]:
        action = "keep integration worktree"
    elif local_policy == "allowed":
        action = f"keep {local_policy_reason} worktree"
    elif local_policy == "disallowed":
        if status:
            action = f"skip dirty disallowed local branch worktree; {local_policy_reason}"
        elif merged is True:
            action = f"eligible for worktree removal; {local_policy_reason}"
        elif merged is False:
            action = f"review before removing disallowed local branch worktree; commits not merged to {merge_target}"
        else:
            action = f"review before removing disallowed local branch worktree; cannot verify {merge_target} ancestry"
    elif local_policy == "review":
        action = f"review local branch policy before cleanup; {local_policy_reason}"
    elif status:
        action = "skip dirty worktree"
    elif not explicit_parent:
        action = "skip; no recorded AF parent branch"
    elif merged is True:
        action = "eligible for worktree removal"
    elif merged is False:
        action = f"skip; commits not merged to {merge_target}"
    else:
        action = f"skip; cannot verify {merge_target} ancestry"

    return {
        "path": str(path),
        "branch": branch,
        "head": head[:12],
        "mode": "branch" if branch != "(detached)" else "detached",
        "metadata": metadata,
        "dirty_count": len(status),
        "merge_target": merge_target,
        "explicit_parent": explicit_parent,
        "merged_to_target": merged,
        "local_policy": local_policy,
        "local_policy_reason": local_policy_reason,
        "action": action,
    }


def build_report(path: Path) -> dict[str, Any]:
    root = repo_root(path)
    config = read_af_config(root)
    current_branch = git(["branch", "--show-current"], root) or "(detached)"
    worktrees = [
        classify_worktree(root, item, config)
        for item in parse_worktrees(git(["worktree", "list", "--porcelain"], root))
    ]
    branches = local_branches(root, config)
    integration_name = config["integration_branch"]
    production_name = config["production_branch"]
    integration_branch = next((branch for branch in branches if branch["name"] == integration_name), None)
    local_main = next((branch for branch in branches if branch["name"] == production_name), None)
    staging_name = config["staging_branch"]
    local_staging = next((branch for branch in branches if branch["name"] == staging_name), None)
    integration_worktree = next((worktree for worktree in worktrees if worktree["branch"] == integration_name), None)
    protected = protected_branches(config)

    branch_actions = []
    for branch in branches:
        name = branch["name"]
        local_policy, local_policy_reason = local_protected_branch_policy(config, name)
        if name == integration_name:
            action = "keep"
        elif local_policy == "allowed":
            action = f"keep {local_policy_reason}"
        elif local_policy == "disallowed":
            if branch["current"]:
                action = f"blocked; checked-out disallowed local branch; {local_policy_reason}"
            elif branch["merged_to_target"] is True:
                action = f"ask to delete disallowed local branch; {local_policy_reason}"
            elif branch["merged_to_target"] is False:
                action = f"review before deleting disallowed local branch; commits not merged to {branch['merge_target']}"
            else:
                action = f"review before deleting disallowed local branch; cannot verify {branch['merge_target']} ancestry"
        elif local_policy == "review":
            action = f"review local branch policy; {local_policy_reason}"
        elif name in protected:
            action = "review protected or reserved branch"
        elif branch["current"]:
            action = "skip checked-out branch"
        elif not branch["explicit_parent"]:
            action = "skip user-controlled branch without AF parent metadata"
        elif branch["merged_to_target"] is True:
            action = "ask to delete merged session branch"
        elif branch["merged_to_target"] is False:
            action = f"skip; not merged to {branch['merge_target']}"
        else:
            action = "skip; cannot verify"
        branch_actions.append({**branch, "action": action})

    worktree_by_branch = {worktree["branch"]: worktree for worktree in worktrees}
    parent_readiness: dict[str, Any] = {}
    for branch in branch_actions:
        if not branch["explicit_parent"]:
            continue
        parent = branch["merge_target"]
        worktree = worktree_by_branch.get(branch["name"], {})
        dirty_count = int(worktree.get("dirty_count", 0) or 0)
        merged = branch["merged_to_target"] is True
        incomplete = dirty_count > 0 or not merged
        parent_entry = parent_readiness.setdefault(
            parent,
            {
                "child_count": 0,
                "incomplete_count": 0,
                "children": [],
            },
        )
        parent_entry["child_count"] += 1
        if incomplete:
            parent_entry["incomplete_count"] += 1
        parent_entry["children"].append(
            {
                "name": branch["name"],
                "dirty_count": dirty_count,
                "merged": merged,
                "incomplete": incomplete,
            }
        )

    for worktree in worktrees:
        if worktree["branch"] != "(detached)" or not worktree["explicit_parent"]:
            continue
        parent = worktree["merge_target"]
        dirty_count = int(worktree.get("dirty_count", 0) or 0)
        merged = worktree["merged_to_target"] is True
        incomplete = dirty_count > 0 or not merged
        parent_entry = parent_readiness.setdefault(
            parent,
            {
                "child_count": 0,
                "incomplete_count": 0,
                "children": [],
            },
        )
        parent_entry["child_count"] += 1
        if incomplete:
            parent_entry["incomplete_count"] += 1
        parent_entry["children"].append(
            {
                "name": f"detached:{worktree['head']}",
                "path": worktree["path"],
                "dirty_count": dirty_count,
                "merged": merged,
                "incomplete": incomplete,
            }
        )

    return {
        "repo": str(root),
        "config": config,
        "current_branch": current_branch,
        "integration": integration_branch,
        "integration_worktree": integration_worktree,
        "local_main_present": local_main is not None,
        "local_staging_present": local_staging is not None,
        "local_staging_policy": local_protected_branch_policy(config, staging_name)[0],
        "worktrees": worktrees,
        "branches": branch_actions,
        "parent_readiness": parent_readiness,
        "agents": agents_review(root),
    }


def markdown(report: dict[str, Any]) -> str:
    config = report["config"]
    lines = [
        f"# Reconcile audit: {report['repo']}",
        "",
        f"- Current branch: `{report['current_branch']}`",
        f"- Agent-Flow mode: `{config['mode']}`",
        f"- Integration branch: `{config['integration_branch']}`",
        f"- Production branch: `{config['production_branch']}`",
        f"- Staging enabled: {'yes' if config.get('staging_enabled') is True else 'no' if config.get('staging_enabled') is False else 'not configured'}",
        f"- Local `{config['production_branch']}` present: {'yes' if report['local_main_present'] else 'no'}",
        f"- Local `{config['staging_branch']}` present: {'yes' if report['local_staging_present'] else 'no'}; policy: `{report['local_staging_policy']}`",
    ]
    integration = report.get("integration")
    if integration:
        remote = integration.get("remote_behind_ahead")
        remote_text = f", upstream behind/ahead: {remote[0]}/{remote[1]}" if remote else ""
        lines.append(f"- Integration: `{integration['commit']}`{remote_text}")
    else:
        lines.append("- Integration: missing local branch")
    integration_wt = report.get("integration_worktree")
    if integration_wt:
        lines.append(f"- Integration worktree changes: {integration_wt['dirty_count']}")

    lines += ["", "## Worktrees"]
    for wt in report["worktrees"]:
        dirty = "dirty" if wt["dirty_count"] else "clean"
        lines.append(f"- `{wt['branch']}` at `{wt['path']}`: {dirty}, mode=`{wt['mode']}`, target=`{wt['merge_target']}`, merged={wt['merged_to_target']}, {wt['action']}")

    lines += ["", "## Branches"]
    for branch in report["branches"]:
        lines.append(f"- `{branch['name']}`: target=`{branch['merge_target']}`, merged={branch['merged_to_target']}, {branch['action']}")

    lines += ["", "## Push Readiness By Parent"]
    if report["parent_readiness"]:
        for parent, readiness in sorted(report["parent_readiness"].items()):
            status = "ready" if readiness["incomplete_count"] == 0 else "blocked"
            lines.append(f"- `{parent}`: {status}, children={readiness['child_count']}, incomplete={readiness['incomplete_count']}")
            for child in readiness["children"]:
                if child["incomplete"]:
                    path = f", path=`{child['path']}`" if child.get("path") else ""
                    lines.append(f"  - incomplete child `{child['name']}`: dirty={child['dirty_count']}, merged={child['merged']}{path}")
    else:
        lines.append("- No child session worktrees with recorded parents found.")

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
