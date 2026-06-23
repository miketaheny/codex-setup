# Agent-Flow Architecture

Agent-Flow is a portable local setup package. It installs shared workflow rules, agent adapters, Codex-compatible skills, templates, and scripts that keep file-changing agent work isolated and reviewable.

## System Map

```mermaid
flowchart TD
    User["Developer"] --> Install["scripts/install.sh"]
    Install --> AFHome["~/.agent-flow"]
    Install --> CodexHome["~/.codex"]
    Install --> ClaudeHome["~/.claude"]

    AFHome --> Rules["AGENT-FLOW.md"]
    AFHome --> Skills["skills/"]
    AFHome --> Scripts["scripts/"]
    AFHome --> Templates["templates/"]

    CodexHome --> CodexAdapter["AGENTS.md"]
    CodexHome --> CodexSkills["Codex skills"]
    ClaudeHome --> ClaudeAdapter["CLAUDE.md"]

    Scripts --> Init["init-repo.sh"]
    Init --> RepoConfig[".agent-flow/config.toml"]
    Init --> RepoRules["repo AGENT-FLOW.md"]
    Init --> RepoAdapters["repo AGENTS.md + CLAUDE.md"]
    Init --> RepoDevlog["repo devlog/"]
    Init --> RepoDocs["repo docs/"]
```

## Repository Components

| Path | Role |
|---|---|
| `AGENT-FLOW.md` | Canonical workflow rules. |
| `AGENTS.md` | Codex-compatible adapter. |
| `CLAUDE.md` | Claude-compatible adapter. |
| `skills/` | AF workflows in `SKILL.md` format. |
| `scripts/` | Install, init, session, readiness, hook, and worktree helpers. |
| `templates/` | Repo instruction, config, devlog, gitignore, and decision templates. |
| `docs/` | Workflow, user, architecture, visual, demo, and prompt docs. |
| `devlog/` | Session engineering history. |

## Skill Flow

```mermaid
flowchart TD
    Request["User request"] --> Kind{"File-changing?"}
    Kind -->|No| Answer["Answer directly"]
    Kind -->|Yes| Flow["af-flow"]
    Flow --> Work["Scoped implementation"]
    Work --> Devlog["af-devlog"]
    Devlog --> Finish["af-finish"]
    Finish --> Show["af-show when useful"]
    Finish --> Review["af-review"]
    Finish --> Ask["Ask before merge"]

    ReleaseStart["Release prep"] --> Reconcile["af-reconcile"]
    Reconcile --> Full["af-full-review"]
    Full --> Security{"Sensitive or required?"}
    Security -->|Yes| Sec["af-security-review with Codex Security when available"]
    Security -->|No| Release["af-release"]
    Sec --> Release
```

## Session Scripts

```mermaid
flowchart LR
    Parent["parent branch"] --> Start["start-session.sh"]
    Start --> Worktree["detached or explicit branch worktree"]
    Worktree --> Finish["finish-session.sh"]
    Finish --> Ready["ASK_USER_MERGE"]
    Ready --> Merge["finish-session.sh --merge"]
    Merge --> Parent
    Parent --> PushReady["check-push-readiness.sh"]
```

## Worktree Manager

```mermaid
flowchart LR
    Manager["worktree-manager.py"] --> Map["worktree map"]
    Manager --> Details["details"]
    Manager --> Pickup["pickup incomplete work"]
    Manager --> Cleanup["cleanup completed work"]
    Pickup --> Metadata["state / owner / lastTouchedAt"]
    Cleanup --> Remove["safe git worktree remove"]
```

## State

Agent-Flow has no service runtime. State is local:

- Global files under `~/.agent-flow`, `~/.codex`, and `~/.claude`.
- Repo choices in `.agent-flow/config.toml`.
- Session metadata in worktree-local Git config.
- Optional branch parent metadata for explicit branches.
- Human history in `devlog/`.
- Git commits, worktrees, and branches.

## Trust Boundaries

- Install scripts write to local home directories.
- Init scripts write into the current Git repo and refuse to run outside Git.
- Worktree cleanup and release side effects require explicit approval.
- Direct work on `main` is blocked by workflow.
- Push-readiness blocks parent pushes while child sessions are dirty or unmerged.
- Security review is distinct from full release review.
