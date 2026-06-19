#!/usr/bin/env python3
"""Interactive Agent-Flow worktree manager."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_repo  # noqa: E402


def run(args: list[str], cwd: Path) -> tuple[int, str, str]:
    return audit_repo.run(args, cwd)


def git(args: list[str], cwd: Path) -> str:
    return audit_repo.git(args, cwd)


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_report(repo: Path) -> dict[str, Any]:
    return audit_repo.build_report(repo)


def indexed_worktrees(report: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    for idx, wt in enumerate(report["worktrees"], start=1):
        item = dict(wt)
        item["id"] = idx
        item["status"] = session_status(report, wt)
        item["activity"] = activity_status(wt)
        item["cleanup_eligible"] = cleanup_eligible(report, wt)
        items.append(item)
    return items


def session_status(report: dict[str, Any], wt: dict[str, Any]) -> str:
    integration = report["config"]["integration_branch"]
    if wt["branch"] == integration:
        return "parent"
    if wt["dirty_count"]:
        return "dirty"
    if not wt["explicit_parent"]:
        return "unmanaged"
    if wt["merged_to_target"] is True:
        return "complete"
    if wt["merged_to_target"] is False:
        return "unmerged"
    return "unknown"


def activity_status(wt: dict[str, Any]) -> str:
    metadata = wt.get("metadata", {})
    state = metadata.get("agentFlow.state", "")
    touched = metadata.get("agentFlow.lastTouchedAt") or metadata.get("agentFlow.startedAt")
    if state in {"active", "started"}:
        return f"{state}; last touch {touched or 'unknown'}"
    if state:
        return state
    return "none"


def cleanup_eligible(report: dict[str, Any], wt: dict[str, Any]) -> bool:
    config = report["config"]
    if wt["path"] == report["repo"]:
        return False
    if wt["branch"] == config["integration_branch"]:
        return False
    if wt["dirty_count"] != 0:
        return False
    if wt["merged_to_target"] is not True:
        return False
    return "eligible for worktree removal" in wt["action"]


def find_worktree(report: dict[str, Any], selector: str) -> dict[str, Any]:
    items = indexed_worktrees(report)
    if selector.isdigit():
        wanted = int(selector)
        for item in items:
            if item["id"] == wanted:
                return item
    for item in items:
        if selector in {item["path"], item["branch"], item["head"]}:
            return item
    raise SystemExit(f"No worktree matches selector: {selector}")


def visual(report: dict[str, Any]) -> str:
    config = report["config"]
    lines = [
        f"Agent-Flow worktrees for {report['repo']}",
        f"parent: {config['integration_branch']} | current: {report['current_branch']}",
        "",
    ]
    integration = report.get("integration")
    if integration:
        remote = integration.get("remote_behind_ahead")
        remote_text = f" upstream {remote[0]}/{remote[1]}" if remote else ""
        lines.append(f"{config['integration_branch']} [{integration['commit']}]{remote_text}")
    else:
        lines.append(f"{config['integration_branch']} [missing]")

    for wt in indexed_worktrees(report):
        if wt["status"] == "parent":
            continue
        marker = "*" if wt["dirty_count"] else "-"
        metadata = wt.get("metadata", {})
        name = metadata.get("agentFlow.sessionName") or wt["branch"]
        branch = wt["branch"] if wt["branch"] != "(detached)" else f"detached:{wt['head']}"
        cleanup = " cleanup" if wt["cleanup_eligible"] else ""
        lines.append(
            f"|-- [{wt['id']}] {marker} {name} ({branch}) "
            f"status={wt['status']} mode={wt['mode']} parent={wt['merge_target']}{cleanup}"
        )
        lines.append(f"|      path={wt['path']}")
        lines.append(f"|      activity={wt['activity']}")

    if len(lines) <= 5:
        lines.append("|-- no child worktrees")
    lines += [
        "",
        "Commands:",
        "  details <id>       show status, metadata, diff stats, and next commands",
        "  pickup <id>        mark an incomplete worktree active and print handoff commands",
        "  cleanup <id>       remove one complete clean worktree and delete its merged session branch",
        "  cleanup-all        remove all complete clean worktrees and merged session branches",
        "  refresh            re-run the audit",
        "  quit               exit",
    ]
    return "\n".join(lines)


def details(report: dict[str, Any], wt: dict[str, Any]) -> str:
    path = Path(wt["path"])
    parent = wt["merge_target"]
    lines = [
        f"Worktree [{wt['id']}]",
        f"- Path: {wt['path']}",
        f"- Branch: {wt['branch']}",
        f"- Head: {wt['head']}",
        f"- Parent: {parent}",
        f"- Mode: {wt['mode']}",
        f"- Status: {wt['status']}",
        f"- Dirty files: {wt['dirty_count']}",
        f"- Merged to parent: {wt['merged_to_target']}",
        f"- Cleanup eligible: {'yes' if wt['cleanup_eligible'] else 'no'}",
        f"- Activity: {wt['activity']}",
    ]
    metadata = wt.get("metadata", {})
    if metadata:
        lines.append("- Metadata:")
        for key in sorted(metadata):
            lines.append(f"  - {key} = {metadata[key]}")
    code, status, err = run(["git", "-C", str(path), "status", "--short"], path)
    if code == 0 and status:
        lines.append("- Dirty status:")
        lines.extend(f"  {line}" for line in status.splitlines())
    elif code != 0:
        lines.append(f"- Dirty status unavailable: {err or status}")

    if parent and wt["status"] not in {"parent", "unmanaged"}:
        code, stat, _ = run(["git", "-C", str(path), "diff", "--stat", f"{parent}...HEAD"], path)
        if code == 0 and stat:
            lines.append("- Diff stat against parent:")
            lines.extend(f"  {line}" for line in stat.splitlines())

    if wt["status"] in {"dirty", "unmerged", "unknown"}:
        lines += [
            "- Pickup:",
            f"  cd {wt['path']}",
            "  scripts/worktree-manager.py --pickup " + str(wt["id"]),
            "  scripts/finish-session.sh",
        ]
    elif wt["cleanup_eligible"]:
        lines += [
            "- Cleanup:",
            f"  scripts/worktree-manager.py --cleanup {wt['id']} --yes",
        ]
    return "\n".join(lines)


def branch_for_worktree(wt: dict[str, Any]) -> str | None:
    branch = wt["branch"]
    if branch == "(detached)":
        return None
    return branch


def branch_cleanup_eligible(report: dict[str, Any], branch: str | None) -> bool:
    if not branch:
        return False
    config = report["config"]
    protected = {config["integration_branch"], config["production_branch"], config["staging_branch"], "master", "production", "prod"}
    if branch in protected:
        return False
    for item in report["branches"]:
        if item["name"] == branch:
            return bool(item["explicit_parent"] and item["merged_to_target"] is True and not item["current"])
    return False


def cleanup_one(report: dict[str, Any], wt: dict[str, Any], assume_yes: bool) -> list[str]:
    if not wt["cleanup_eligible"]:
        raise SystemExit(f"Worktree {wt['id']} is not safe to clean up: {wt['action']}")
    if not assume_yes and not confirm(f"Remove worktree {wt['path']}?"):
        return [f"Skipped {wt['path']}"]

    root = Path(report["repo"])
    path = Path(wt["path"])
    messages = []
    code, out, err = run(["git", "worktree", "remove", str(path)], root)
    if code != 0:
        raise SystemExit(err or out or f"Failed to remove {path}")
    messages.append(f"Removed worktree: {path}")

    branch = branch_for_worktree(wt)
    if branch_cleanup_eligible(report, branch):
        code, out, err = run(["git", "branch", "-d", branch], root)
        if code != 0:
            messages.append(f"Skipped branch delete for {branch}: {err or out}")
        else:
            messages.append(out or f"Deleted branch: {branch}")
    return messages


def cleanup_all(report: dict[str, Any], assume_yes: bool) -> list[str]:
    items = [wt for wt in indexed_worktrees(report) if wt["cleanup_eligible"]]
    if not items:
        return ["No cleanup-eligible worktrees found."]
    if not assume_yes and not confirm(f"Remove {len(items)} cleanup-eligible worktree(s)?"):
        return ["Cleanup skipped."]
    messages: list[str] = []
    current = report
    for item in items:
        fresh = find_worktree(current, item["path"])
        messages.extend(cleanup_one(current, fresh, assume_yes=True))
        current = build_report(Path(current["repo"]))
    return messages


def pickup(report: dict[str, Any], wt: dict[str, Any]) -> str:
    if wt["status"] in {"parent", "complete"}:
        raise SystemExit(f"Worktree {wt['id']} is {wt['status']}; nothing to pick up.")
    root = Path(report["repo"])
    path = Path(wt["path"])
    run(["git", "config", "extensions.worktreeConfig", "true"], root)
    metadata = {
        "agentFlow.state": "active",
        "agentFlow.owner": "codex",
        "agentFlow.lastTouchedAt": now_iso(),
    }
    for key, value in metadata.items():
        code, out, err = run(["git", "-C", str(path), "config", "--worktree", key, value], path)
        if code != 0:
            raise SystemExit(err or out or f"Failed to write {key}")
    return "\n".join(
        [
            f"Picked up worktree [{wt['id']}]: {wt['path']}",
            "",
            "Recommended new Codex chat start:",
            f"  cd {wt['path']}",
            "  Use Agent-Flow. Continue this AF worktree session, inspect the status, then finish or merge when ready.",
            "",
            "Useful commands:",
            "  scripts/worktree-manager.py --details " + str(wt["id"]),
            "  scripts/finish-session.sh",
        ]
    )


def confirm(prompt: str) -> bool:
    answer = input(f"{prompt} [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def interactive(repo: Path) -> int:
    report = build_report(repo)
    while True:
        print(visual(report))
        try:
            command = input("af-worktrees> ").strip()
        except EOFError:
            print()
            return 0
        if not command:
            continue
        parts = command.split()
        verb = parts[0].lower()
        try:
            if verb in {"q", "quit", "exit"}:
                return 0
            if verb in {"r", "refresh"}:
                report = build_report(repo)
                continue
            if verb in {"d", "details"} and len(parts) == 2:
                print(details(report, find_worktree(report, parts[1])))
            elif verb in {"p", "pickup"} and len(parts) == 2:
                print(pickup(report, find_worktree(report, parts[1])))
                report = build_report(repo)
            elif verb in {"c", "cleanup"} and len(parts) == 2:
                for line in cleanup_one(report, find_worktree(report, parts[1]), assume_yes=False):
                    print(line)
                report = build_report(repo)
            elif verb in {"ca", "cleanup-all"}:
                for line in cleanup_all(report, assume_yes=False):
                    print(line)
                report = build_report(repo)
            else:
                print("Unknown command. Use details <id>, pickup <id>, cleanup <id>, cleanup-all, refresh, or quit.")
        except SystemExit as exc:
            print(exc, file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Path inside the target git repo")
    parser.add_argument("--json", action="store_true", help="Emit the manager report as JSON")
    parser.add_argument("--interactive", "-i", action="store_true", help="Open the terminal picker")
    parser.add_argument("--details", help="Show details for a worktree id, path, branch, or short head")
    parser.add_argument("--pickup", help="Mark an incomplete worktree active and print handoff commands")
    parser.add_argument("--cleanup", help="Clean up one complete worktree by id, path, branch, or short head")
    parser.add_argument("--cleanup-all", action="store_true", help="Clean up every complete clean worktree")
    parser.add_argument("--yes", action="store_true", help="Do not prompt for cleanup confirmation")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    report = build_report(repo)
    if args.json:
        manager_report = dict(report)
        manager_report["worktrees"] = indexed_worktrees(report)
        print(json.dumps(manager_report, indent=2))
        return 0
    if args.details:
        print(details(report, find_worktree(report, args.details)))
        return 0
    if args.pickup:
        print(pickup(report, find_worktree(report, args.pickup)))
        return 0
    if args.cleanup:
        for line in cleanup_one(report, find_worktree(report, args.cleanup), assume_yes=args.yes):
            print(line)
        return 0
    if args.cleanup_all:
        for line in cleanup_all(report, assume_yes=args.yes):
            print(line)
        return 0
    if args.interactive:
        return interactive(repo)
    print(visual(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
