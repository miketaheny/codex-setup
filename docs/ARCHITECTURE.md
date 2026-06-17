# Agent-Flow Architecture

Agent-Flow is a portable setup package for solo developers using Claude, Codex, or other coding agents. It provides shared workflow rules, agent-specific adapters, reusable AF skills, repo bootstrap templates, and small safety scripts.

## System Map

```mermaid
flowchart TD
    User["Developer"] --> Install["scripts/install.sh"]
    Install --> AFHome["~/.agent-flow"]
    Install --> CodexHome["~/.codex"]
    Install --> ClaudeHome["~/.claude"]

    AFHome --> SharedRules["AGENT-FLOW.md"]
    AFHome --> SharedSkills["skills/"]
    AFHome --> SharedTemplates["templates/"]
    AFHome --> SharedScripts["scripts/"]

    CodexHome --> CodexAdapter["AGENTS.md"]
    CodexHome --> CodexSkills["Codex-compatible skills"]
    ClaudeHome --> ClaudeAdapter["CLAUDE.md"]

    SharedScripts --> Bootstrap["bootstrap-repo.sh"]
    Bootstrap --> RepoRules["repo AGENT-FLOW.md"]
    Bootstrap --> RepoAdapters["repo AGENTS.md + CLAUDE.md"]
    Bootstrap --> RepoDevlog["repo devlog/"]
    Bootstrap --> RepoDocs["repo docs/"]
```

## Repository Components

| Path | Role |
|---|---|
| `AGENT-FLOW.md` | Canonical workflow rules shared across agents. |
| `AGENTS.md` | Codex-compatible adapter that points to `AGENT-FLOW.md`. |
| `CLAUDE.md` | Claude-compatible adapter that points to `AGENT-FLOW.md`. |
| `skills/` | AF workflow skills in Codex-compatible `SKILL.md` format. |
| `scripts/` | Portable shell helpers for install, bootstrap, worktrees, branch checks, and review snapshots. |
| `templates/` | Repo-level instruction, devlog, and decision templates. |
| `docs/` | Project documentation, visual plans, prompts, guides, and communication assets. |
| `devlog/` | Per-commit engineering history and validation records. |

## Install Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Install as install.sh
    participant AF as ~/.agent-flow
    participant Codex as ~/.codex
    participant Claude as ~/.claude

    Dev->>Install: Run ./scripts/install.sh
    Install->>AF: Copy canonical rules, skills, templates, scripts, docs
    Install->>Codex: Copy AGENTS.md, AGENT-FLOW.md, skills, templates, scripts, docs
    Install->>Claude: Copy CLAUDE.md and AGENT-FLOW.md
    Install-->>Dev: Print bootstrap command
```

## Repo Bootstrap Flow

```mermaid
flowchart LR
    Repo["Target Git repo"] --> Bootstrap["~/.agent-flow/scripts/bootstrap-repo.sh"]
    Bootstrap --> Rules["AGENT-FLOW.md"]
    Bootstrap --> Adapters["AGENTS.md + CLAUDE.md"]
    Bootstrap --> Devlog["devlog/README.md"]
    Bootstrap --> Decision["docs/decisions/000-template.md"]
    Bootstrap --> Dirs["docs/solutions/ + docs/plans/"]
    Bootstrap --> VisualDirs["docs/diagrams/ + docs/assets/ + docs/presentations/"]
```

`bootstrap-repo.sh` only copies missing files. Existing repo instructions and docs are left in place.

## Skill Model

```mermaid
flowchart TD
    Request["User request"] --> Choose["Choose lightest safe AF skill"]
    Choose --> Small["af-small-change"]
    Choose --> Worktree["af-worktree-task"]
    Choose --> Docs["af-docs"]
    Choose --> Migration["af-migrate-backlog-devlog"]
    Choose --> Review["af-review-gate"]
    Choose --> Staging["af-push-staging"]
    Choose --> Reconcile["af-reconcile-worktrees"]
    Choose --> Compound["af-compound-mode"]

    Small --> Devlog["devlog entry"]
    Worktree --> Devlog
    Docs --> ProjectDocs["project docs + visuals"]
    Migration --> Devlog
    Review --> MergeDecision["merge readiness"]
    Staging --> Protected["staging promotion"]
```

Skills are written as Markdown workflows. Codex can auto-discover them through its skill format; other agents can still read them directly as reusable process instructions.

## Data and State

Agent-Flow has no database or service runtime. State is file-based:

- Global setup files under `~/.agent-flow`, `~/.codex`, and `~/.claude`.
- Repo-level instructions and docs copied into target repositories.
- Git branches, worktrees, and commits managed by the developer.
- Engineering history stored in repo `devlog/` files.

## Trust Boundaries

- Install scripts write to local home directories and should be reviewed before running.
- Bootstrap scripts write into the current Git repository and refuse to run outside a Git repo.
- Staging promotion and cleanup skills require explicit approval before destructive actions such as branch deletion or worktree removal.
- Generated docs and visuals must be grounded in source files, devlog entries, screenshots, or user-provided context.
