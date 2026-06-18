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

    SharedScripts --> Init["init-repo.sh"]
    SharedScripts --> Bootstrap["bootstrap-repo.sh"]
    Init --> RepoConfig["repo .agent-flow/config.toml"]
    Init --> Bootstrap
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
| `scripts/` | Portable shell helpers for install, init, bootstrap, session lifecycle, push readiness, hooks, worktrees, branch checks, and review snapshots. |
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
    Install-->>Dev: Print init command
```

## Repo Init And Bootstrap Flow

```mermaid
flowchart LR
    Repo["Target Git repo"] --> Init["~/.agent-flow/scripts/init-repo.sh"]
    Init --> Config[".agent-flow/config.toml"]
    Init --> Choices["enforcement + staging choices"]
    Init --> Gitignore[".gitignore Agent-Flow block"]
    Init --> Bootstrap["bootstrap-repo.sh"]
    Bootstrap --> Rules["AGENT-FLOW.md"]
    Bootstrap --> Adapters["AGENTS.md + CLAUDE.md"]
    Bootstrap --> Devlog["devlog/README.md"]
    Bootstrap --> Decision["docs/decisions/000-template.md"]
    Bootstrap --> Dirs["docs/solutions/ + docs/plans/"]
    Bootstrap --> VisualDirs["docs/diagrams/ + docs/assets/ + docs/presentations/"]
```

`init-repo.sh` records first-contact repo choices, including whether Agent-Flow enforcement is enabled, whether staging is used, and whether the local pre-push hook was installed. Enforced repos default to the `development -> staging -> main` PR path unless staging is disabled. It also ensures `.gitignore` has the Agent-Flow local/IDE/env block and notes staging-disabled repos in local agent adapters.

`bootstrap-repo.sh` only copies missing files. Existing repo instructions and docs are left in place.

## Skill Model

```mermaid
flowchart TD
    Request["User request"] --> Choose["Choose lightest safe AF skill"]
    Choose --> Small["af-small-change"]
    Choose --> Worktree["af-worktree-task"]
    Choose --> Finish["af-finish-session"]
    Choose --> Docs["af-docs"]
    Choose --> Migration["af-migrate-backlog-devlog"]
    Choose --> Review["af-review-gate"]
    Choose --> Security["af-security-review"]
    Choose --> Release["af-release-pr"]
    Choose --> Reconcile["af-reconcile-worktrees"]
    Choose --> Compound["af-compound-mode"]

    Small --> Devlog["devlog entry"]
    Worktree --> Devlog
    Finish --> BrowserQA["app/browser review when applicable"]
    Finish --> Review
    Docs --> ProjectDocs["project docs + visuals"]
    Migration --> Devlog
    Review --> MergeDecision["merge readiness"]
    Security --> ProtectedReview["protected-branch security gate"]
    Release --> Protected["protected release PRs"]
```

Skills are written as Markdown workflows. Codex can auto-discover them through its skill format; other agents can still read them directly as reusable process instructions.

## Session Lifecycle Scripts

```mermaid
flowchart LR
    Prompt["File-changing chat"] --> Start["start-session.sh"]
    Start --> Worktree["detached session worktree + AF metadata"]
    Worktree --> Finish["finish-session.sh"]
    Finish --> Ask["ASK_USER_MERGE"]
    Ask --> Merge["finish-session.sh --merge"]
    Merge --> Parent["parent branch"]
    Parent --> PushCheck["check-push-readiness.sh"]
    PushCheck --> Remote["remote push"]
```

## Worktree Manager

```mermaid
flowchart LR
    Manager["worktree-manager.py"] --> Map["visual worktree map"]
    Manager --> Details["details view"]
    Manager --> Pickup["pickup incomplete work"]
    Manager --> Cleanup["cleanup complete worktrees"]
    Pickup --> Metadata["agentFlow.state / owner / lastTouchedAt"]
    Cleanup --> Remove["git worktree remove + merged branch delete"]
```

## Data and State

Agent-Flow has no database or service runtime. State is file-based:

- Global setup files under `~/.agent-flow`, `~/.codex`, and `~/.claude`.
- Repo-level instructions and docs copied into target repositories.
- Repo-level choices stored in `.agent-flow/config.toml`.
- Repo-level ignore policy stored in `.gitignore`.
- Local protected branch policy derived from `.agent-flow/config.toml`: `main` is disallowed locally, and `staging` is local only when staging is enabled.
- Detached session metadata stored in worktree-local Git config as `agentFlow.kind`, `agentFlow.parent`, `agentFlow.sessionName`, `agentFlow.state`, `agentFlow.owner`, `agentFlow.devlogPolicy`, and timestamps.
- Explicit named branches, when requested, also store parent metadata in Git config as `branch.<branch>.agentFlowParent`.
- Git branches, worktrees, and commits managed by the developer.
- Engineering history stored in repo `devlog/` files.

## Trust Boundaries

- Install scripts write to local home directories and should be reviewed before running.
- Init and bootstrap scripts write into the current Git repository and refuse to run outside a Git repo.
- Release PR and cleanup skills require explicit approval before remote side effects or destructive actions such as PR creation, branch deletion, or worktree removal.
- Pull requests to protected branches require a distinct formal security review before PR creation.
- `main` is a production PR target and direct local agent work is blocked by workflow. `staging` is local only when enabled and protected/reserved when present.
- Optional local `pre-push` hooks call `check-push-readiness.sh` so parent branches are not pushed while child session worktrees are dirty or unmerged.
- Generated docs and visuals must be grounded in source files, devlog entries, screenshots, or user-provided context.
