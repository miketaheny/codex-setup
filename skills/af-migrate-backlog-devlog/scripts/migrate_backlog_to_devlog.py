#!/usr/bin/env python3
"""Convert Backlog-style Markdown task files into Agent-Flow devlog entries."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


DEFAULT_SOURCE_PATTERNS = (
    "Backlog.md",
    "triage.md",
    "backlog/tasks/*.md",
    "backlog/drafts/*.md",
    ".backlog/tasks/*.md",
    ".backlog/drafts/*.md",
)


@dataclass
class TaskDoc:
    path: Path
    metadata: dict[str, str]
    title: str
    body: str


def run_git_branch(repo: Path) -> str:
    proc = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.stdout.strip() or "unknown"


def slugify(value: str, fallback: str = "task") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:80].strip("-") or fallback


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")
    return metadata, text[match.end() :]


def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        match = re.match(r"^#\s+(.+)$", line.strip())
        if match:
            return match.group(1).strip()
    return None


def first_nonempty(body: str, max_len: int = 240) -> str:
    for line in body.splitlines():
        stripped = line.strip().strip("#").strip()
        if stripped and not stripped.startswith("<!--"):
            return stripped[:max_len]
    return "No description recorded."


def section(body: str, names: tuple[str, ...]) -> str:
    pattern = re.compile(r"^##+\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(body))
    lowered = {name.lower() for name in names}
    for index, match in enumerate(matches):
        heading = match.group(1).strip().lower()
        if heading not in lowered:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        return content or "Not recorded."
    return "Not recorded."


def discover_sources(repo: Path, explicit: list[str]) -> list[Path]:
    paths: list[Path] = []
    if explicit:
        for item in explicit:
            path = (repo / item).resolve() if not Path(item).is_absolute() else Path(item)
            if path.is_dir():
                paths.extend(sorted(path.rglob("*.md")))
            elif path.is_file():
                paths.append(path)
        return sorted(dict.fromkeys(paths))

    for pattern in DEFAULT_SOURCE_PATTERNS:
        paths.extend(repo.glob(pattern))
    return sorted(dict.fromkeys(path.resolve() for path in paths if path.is_file()))


def load_task(path: Path, repo: Path) -> TaskDoc:
    text = path.read_text(encoding="utf-8", errors="replace")
    metadata, body = parse_frontmatter(text)
    title = metadata.get("title") or first_heading(body) or path.stem
    rel_path = path.relative_to(repo) if path.is_relative_to(repo) else path
    return TaskDoc(path=rel_path, metadata=metadata, title=title, body=body.strip())


def devlog_name(task: TaskDoc, date: str) -> str:
    task_id = task.metadata.get("id") or task.path.stem
    return f"{date}-backlog-{slugify(task_id)}-{slugify(task.title)}.md"


def format_block(value: str, empty: str = "Not recorded.") -> str:
    value = value.strip()
    return value if value else empty


def render_devlog(task: TaskDoc, repo: Path, date: str, branch: str) -> str:
    metadata = task.metadata
    status = metadata.get("status", "unknown")
    priority = metadata.get("priority", "unknown")
    created = metadata.get("created_date", metadata.get("created", "unknown"))
    updated = metadata.get("updated_date", metadata.get("updated", "unknown"))
    task_id = metadata.get("id", task.path.stem)
    description = section(task.body, ("Description",))
    if description == "Not recorded.":
        description = first_nonempty(task.body)
    acceptance = section(task.body, ("Acceptance Criteria", "Acceptance"))
    plan = section(task.body, ("Implementation Plan", "Plan"))
    notes = section(task.body, ("Implementation Notes", "Notes"))
    done = section(task.body, ("Definition of Done", "Done"))

    return f"""# {date} - Backlog migration: {task.title}

- Branch/worktree: `{branch}` / `{repo}`
- Commit: `pending`
- Source Backlog file: `{task.path}`
- Task id: `{task_id}`
- Task status: `{status}`
- Priority: `{priority}`
- Created: `{created}`
- Updated: `{updated}`

## Goal

{format_block(description)}

## Acceptance Criteria

{format_block(acceptance)}

## Implementation Plan

{format_block(plan)}

## Implementation Notes

{format_block(notes)}

## Definition of Done

{format_block(done)}

## Migration Decisions

- Migrated from a Backlog-style task record into Agent-Flow devlog format.
- Preserved the source path and status so incomplete work remains visible.
- Legacy source files were not deleted by this conversion.

## Validation

- Migration generated this devlog entry from `{task.path}`.
- Review source content before deleting any legacy task files.

## Risks / Follow-ups

- If task status is not complete, treat this entry as historical context, not proof that the work is done.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Repository root")
    parser.add_argument("--source", action="append", default=[], help="Specific file or directory to migrate; repeatable")
    parser.add_argument("--output", default="devlog", help="Output directory relative to repo")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Date prefix for generated entries")
    parser.add_argument("--write", action="store_true", help="Write files. Defaults to dry-run.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    output = repo / args.output
    sources = discover_sources(repo, args.source)
    branch = run_git_branch(repo)

    print(f"Repo: {repo}")
    print(f"Output: {output}")
    print(f"Mode: {'write' if args.write else 'dry-run'}")
    print(f"Sources found: {len(sources)}")

    if not sources:
        return 0

    if args.write:
        output.mkdir(parents=True, exist_ok=True)

    for source in sources:
        task = load_task(source, repo)
        target = output / devlog_name(task, args.date)
        rel_target = target.relative_to(repo) if target.is_relative_to(repo) else target
        if target.exists():
            print(f"SKIP existing: {rel_target}")
            continue
        print(f"{'WRITE' if args.write else 'WOULD WRITE'}: {rel_target} <- {task.path}")
        if args.write:
            target.write_text(render_devlog(task, repo, args.date, branch), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
