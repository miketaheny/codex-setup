#!/usr/bin/env python3
"""Detect and convert a JavaScript repository to pnpm."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


try:
    sys.stdout.reconfigure(line_buffering=True)
except AttributeError:
    pass

LEGACY_LOCKFILES = (
    "package-lock.json",
    "npm-shrinkwrap.json",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
)
COMMAND_PATTERNS = (
    "npm ci",
    "npm install",
    "npm run ",
    "npx ",
    "yarn ",
    "bun install",
)
SCAN_DIR_SKIP = {
    ".git",
    ".agent-flow",
    ".next",
    ".turbo",
    ".vercel",
    "coverage",
    "dist",
    "node_modules",
    "vendor",
}
SCAN_FILE_SUFFIXES = {
    ".Dockerfile",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".sh",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
}


class ConversionError(RuntimeError):
    """Raised for conversion failures with user-facing messages."""


def run(cmd: list[str], cwd: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=cwd, text=True, check=False)
    if check and result.returncode != 0:
        raise ConversionError(f"Command failed with exit {result.returncode}: {' '.join(cmd)}")
    return result


def load_package_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ConversionError(f"Invalid package.json: {exc}") from exc
    if not isinstance(data, dict):
        raise ConversionError("package.json must contain a JSON object.")
    return data


def write_package_json(path: Path, data: dict[str, Any]) -> None:
    rendered = json.dumps(data, indent=2, ensure_ascii=False)
    path.write_text(rendered + "\n", encoding="utf-8")


def existing_lockfiles(root: Path) -> list[str]:
    names = [name for name in ("pnpm-lock.yaml", *LEGACY_LOCKFILES) if (root / name).exists()]
    if (root / "pnpm-workspace.yaml").exists():
        names.append("pnpm-workspace.yaml")
    return names


def detect_manager(root: Path, package_data: dict[str, Any]) -> str:
    package_manager = str(package_data.get("packageManager", "")).strip()
    if package_manager.startswith("pnpm@"):
        return "pnpm"
    if package_manager.startswith("npm@"):
        return "npm"
    if package_manager.startswith("yarn@"):
        return "yarn"
    if package_manager.startswith("bun@"):
        return "bun"

    if (root / "pnpm-lock.yaml").exists() or (root / "pnpm-workspace.yaml").exists():
        return "pnpm"
    if (root / "bun.lock").exists() or (root / "bun.lockb").exists():
        return "bun"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "package-lock.json").exists() or (root / "npm-shrinkwrap.json").exists():
        return "npm"
    return "unknown"


def workspace_packages(package_data: dict[str, Any]) -> list[str]:
    workspaces = package_data.get("workspaces")
    if isinstance(workspaces, list):
        return [str(item) for item in workspaces if str(item).strip()]
    if isinstance(workspaces, dict):
        packages = workspaces.get("packages")
        if isinstance(packages, list):
            return [str(item) for item in packages if str(item).strip()]
    return []


def ensure_workspace_file(root: Path, package_data: dict[str, Any]) -> bool:
    workspace_file = root / "pnpm-workspace.yaml"
    if workspace_file.exists():
        return False

    packages = workspace_packages(package_data)
    if not packages:
        return False

    lines = ["packages:"]
    for package in packages:
        escaped = package.replace('"', '\\"')
        lines.append(f'  - "{escaped}"')
    workspace_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Created: {workspace_file.relative_to(root)}")
    return True


def ensure_pnpm(root: Path, target: str | None) -> tuple[str, str]:
    pnpm = shutil.which("pnpm")
    if pnpm is None:
        corepack = shutil.which("corepack")
        if corepack is None:
            raise ConversionError("pnpm is not installed and corepack is not available. Install pnpm or Node/Corepack first.")
        run([corepack, "enable"], root)
        requested = target or "latest"
        run([corepack, "prepare", f"pnpm@{requested}", "--activate"], root)
        pnpm = shutil.which("pnpm")
        if pnpm is None:
            raise ConversionError("Corepack ran, but pnpm is still not on PATH.")

    version_result = subprocess.run([pnpm, "--version"], cwd=root, text=True, capture_output=True, check=False)
    if version_result.returncode != 0:
        raise ConversionError("pnpm is on PATH, but `pnpm --version` failed.")
    return pnpm, version_result.stdout.strip()


def import_legacy_lockfile(root: Path, pnpm: str) -> None:
    if (root / "pnpm-lock.yaml").exists():
        return

    if not any((root / name).exists() for name in LEGACY_LOCKFILES):
        return

    result = run([pnpm, "import"], root, check=False)
    if result.returncode != 0:
        print("Warning: `pnpm import` failed; continuing with `pnpm install` to generate a fresh lockfile.", file=sys.stderr)


def remove_legacy_lockfiles(root: Path) -> list[str]:
    removed: list[str] = []
    for name in LEGACY_LOCKFILES:
        path = root / name
        if path.exists():
            path.unlink()
            removed.append(name)
            print(f"Removed: {name}")
    return removed


def scan_followups(root: Path) -> list[str]:
    matches: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in SCAN_DIR_SKIP for part in rel.parts):
            continue
        if path.name in {"Dockerfile", "Containerfile"}:
            pass
        elif path.suffix not in SCAN_FILE_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern in text for pattern in COMMAND_PATTERNS):
            matches.append(str(rel))
    return sorted(set(matches))


def print_summary(root: Path, package_data: dict[str, Any]) -> str:
    manager = detect_manager(root, package_data)
    locks = existing_lockfiles(root)
    print(f"Repo: {root}")
    print(f"Detected package manager: {manager}")
    print(f"Lock/workspace files: {', '.join(locks) if locks else 'none'}")
    package_manager = package_data.get("packageManager")
    if package_manager:
        print(f"packageManager: {package_manager}")
    return manager


def convert(root: Path, args: argparse.Namespace) -> None:
    package_json = root / "package.json"
    if not package_json.exists():
        print("NO_PACKAGE_JSON: not a Node repo; pnpm conversion skipped.")
        return

    package_data = load_package_json(package_json)
    manager = print_summary(root, package_data)
    if manager == "pnpm":
        print("PNPM_ALREADY_CONFIGURED: no conversion needed.")
        return

    if not args.yes and not args.onboarding:
        answer = input("Convert this repo to pnpm? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("PNPM_CONVERSION_SKIPPED")
            return

    pnpm, pnpm_version = ensure_pnpm(root, args.target_version)
    package_data["packageManager"] = f"pnpm@{pnpm_version}"
    write_package_json(package_json, package_data)
    print(f"Updated: package.json packageManager=pnpm@{pnpm_version}")

    ensure_workspace_file(root, package_data)
    import_legacy_lockfile(root, pnpm)
    run([pnpm, "install"], root)

    if not args.keep_legacy_lockfiles:
        remove_legacy_lockfiles(root)

    followups = scan_followups(root)
    if followups:
        print("FOLLOW_UP_COMMAND_REFERENCES:")
        for item in followups:
            print(f"- {item}")
        print("Review these files for npm/yarn/bun commands that should become pnpm commands.")

    print("PNPM_CONVERSION_COMPLETE")


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect and convert a JavaScript repository to pnpm.")
    parser.add_argument("repo", nargs="?", default=".", help="Repository root or subdirectory inside the repo.")
    parser.add_argument("--check", action="store_true", help="Only report current package-manager state.")
    parser.add_argument("--convert", action="store_true", help="Convert the repo to pnpm when needed.")
    parser.add_argument("--yes", action="store_true", help="Do not prompt before conversion.")
    parser.add_argument("--onboarding", action="store_true", help="Run from Agent-Flow init-repo onboarding.")
    parser.add_argument("--target-version", help="pnpm version for Corepack when pnpm is missing; default is latest.")
    parser.add_argument("--keep-legacy-lockfiles", action="store_true", help="Leave npm/yarn/bun lockfiles after successful install.")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    if not root.exists():
        raise ConversionError(f"Repo path does not exist: {root}")
    try:
        git_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if git_root.returncode == 0:
            root = Path(git_root.stdout.strip()).resolve()
    except FileNotFoundError:
        pass

    package_json = root / "package.json"
    if not package_json.exists():
        print("NO_PACKAGE_JSON: not a Node repo; pnpm conversion skipped.")
        return 0

    package_data = load_package_json(package_json)
    if args.check or not args.convert:
        manager = print_summary(root, package_data)
        if manager == "pnpm":
            print("PNPM_ALREADY_CONFIGURED")
        else:
            print("PNPM_CONVERSION_AVAILABLE")
        return 0

    convert(root, args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ConversionError as exc:
        print(f"PNPM_CONVERSION_FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
