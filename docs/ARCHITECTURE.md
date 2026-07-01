# Agent-Flow Architecture

Agent-Flow is a Codex-focused local setup package. It installs workflow rules, Codex skills, templates, and scripts that keep file-changing Codex work isolated and reviewable.

## System Map

```mermaid
flowchart TD
    User["Developer"] --> Install["scripts/install.sh"]
    Install --> AFHome["~/.agent-flow"]
    Install --> CodexHome["~/.codex"]

    AFHome --> Rules["AGENT-FLOW.md"]
    AFHome --> Skills["skills/"]
    AFHome --> Scripts["scripts/"]
    AFHome --> Templates["templates/"]

    CodexHome --> CodexAdapter["AGENTS.md"]
    CodexHome --> CodexSkills["Codex skills"]
    CodexHome --> CodexProfiles["fast/review/deep config profiles"]
    CodexSkills --> ClaudeReview["optional af-claude-review"]
    ClaudeReview --> ClaudeCLI["Claude CLI when installed"]

    Scripts --> Init["init-repo.sh"]
    Init --> RepoConfig[".agent-flow/config.toml"]
    Init --> RepoRules["repo AGENT-FLOW.md"]
    Init --> RepoAdapters["repo AGENTS.md"]
    Init --> RepoDevlog["repo devlog/"]
    Init --> RepoDocs["repo docs/"]
    Init --> Pnpm["pnpm onboarding for Node repos"]
```

## Repository Components

| Path | Role |
|---|---|
| `AGENT-FLOW.md` | Canonical workflow rules. |
| `AGENTS.md` | Codex adapter. |
| `skills/` | AF workflows in `SKILL.md` format. |
| `scripts/` | Install, init, session, readiness, hook, and worktree helpers. |
| `templates/` | Repo instruction, config, devlog, gitignore, and decision templates. |
| `docs/` | Workflow, user, architecture, visual, demo, and prompt docs. |
| `devlog/` | Session engineering history. |

## Skill Flow

```mermaid
flowchart TD
    Request --> Help{"Command help?"}
    Help -->|Yes| AFHelp["af-help"]
    Help -->|No| Kind
    Kind -->|No| Answer["Answer directly"]
    Kind -->|Yes| Flow["af-flow"]
    Flow --> Work["Persistent scoped implementation"]
    Work --> Devlog["af-devlog"]
    Devlog --> Finish["af-finish"]
    Finish --> Show["af-show when useful"]
    Finish --> Review["af-review"]
    Finish --> Ask["Ask before merge"]

    ReleaseStart["Release prep"] --> Reconcile["af-reconcile"]
    Reconcile --> Full["af-full-review"]
    Full --> ClaudeReview{"External model check requested?"}
    ClaudeReview -->|Yes| ClaudeSkill["af-claude-review via Claude CLI"]
    ClaudeReview -->|No| Security
    ClaudeSkill --> Security
    Security{"Sensitive or required?"}
    Security -->|Yes| Sec["af-security-review with Codex Security when available"]
    Security -->|No| Release["af-release"]
    Sec --> Release

    PnpmStart["Package-manager migration"] --> PnpmSkill["af-pnpm"]
    PnpmSkill --> PnpmLock["pnpm-lock.yaml + packageManager"]

    AuditStart["Explicit feature audit"] --> Audit["af-feature-audit"]
    Audit --> Register["docs/product/feature-register.csv"]
    Audit --> AuditFix["Scoped AF fix sessions"]

    UIStart["Explicit UI audit"] --> Brand["af-brand-guidelines when needed"]
    Brand --> UIAudit["af-ui-audit"]
    UIAudit --> UIRegister["docs/product/ui-audit-register.csv"]
    UIAudit --> UIFix["Scoped AF fix sessions"]
```

## Fast Path Routing

```mermaid
flowchart LR
    Prompt["Codex prompt"] --> ReadOnly{"Read only?"}
    ReadOnly -->|Yes| Fast["fast profile or base medium"]
    Fast --> Answer["Answer directly"]
    ReadOnly -->|No| Active{"Matching active AF session?"}
    Active -->|Yes| Continue["Continue same worktree"]
    Active -->|No| Start["af-flow / start-session.sh"]
    Start --> Continue
    Continue --> Scoped["Targeted reads + scoped edits"]
    Scoped --> Validate["Focused validation"]
    Validate --> More{"More related work?"}
    More -->|Yes| Continue
    More -->|No, user wraps up| Finish["af-finish"]
    Finish --> Ready["Ready / ask before merge"]
```

## Session Scripts

```mermaid
flowchart LR
    Parent["parent branch"] --> Start["start-session.sh"]
    Start --> Worktree["active detached or explicit branch worktree"]
    Worktree --> Continue["related prompts continue here"]
    Continue --> Worktree
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

- Global files under `~/.agent-flow` and `~/.codex`.
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
