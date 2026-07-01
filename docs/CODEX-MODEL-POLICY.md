# Codex Model And Effort Policy

Use this policy to optimize Codex speed and token usage without losing depth on real development work.

## Defaults

Base Codex config:

```toml
model = "gpt-5.5"
model_reasoning_effort = "xhigh"
model_verbosity = "low"
```

This favors quality for the work that usually costs the most to redo: development, debugging, refactoring, browser/computer-use, release, and high-context tasks.

## Operating Principle

Run an effort preflight before acting. Keep the workflow lightweight, then choose the cheapest effort tier that is still likely to do the task correctly on the first pass.

Default to `xhigh` for most development and computer-use work. Downgrade only when the task is clearly low-risk, narrow, and easy to verify.

## Effort Preflight

Classify the task before starting or continuing work:

| Task class | Recommended effort | Examples |
|---|---|---|
| Read-only lookup | `fast` or medium | command help, status, simple explanation |
| Trivial edit | medium | typo, one-file docs copy, formatting, tiny config |
| Normal development | `xhigh` | features, bugfixes, refactors, migrations, tests |
| Computer/browser use | `xhigh` | live UI QA, CMS/admin work, remote desktop, multi-step browser tasks |
| Review/release/security | `xhigh` or `deep` | full review, release diff, auth, secrets, data access |

If uncertain, choose `xhigh` for development and computer-use work.

## Profiles

Agent-Flow installs these Codex profile templates when the target files do not already exist:

| Profile | Model | Effort | Use |
|---|---|---|---|
| `fast` | `gpt-5.4-mini` | `low` | read-only help/status, quick edits, lightweight exploration |
| `review` | `gpt-5.5` | `high` | `af-full-review`, risky diffs, final release checks |
| `deep` | `gpt-5.5` | `xhigh` | hard debugging, security-sensitive analysis, repeated failed attempts |

CLI examples:

```bash
codex --profile fast
codex --profile review
codex --profile deep
codex exec --profile review "review this session diff"
```

For Codex app or IDE work, use the model/effort selector when available. Codex can switch models manually during an active CLI thread with `/model`, but Agent-Flow should not assume automatic model escalation.

## Agent-Flow Routing

Use the effort preflight:

| AF activity | Recommended setting |
|---|---|
| `af-help`, `af-status`, read-only command lookup | `fast` or base medium |
| trivial docs/config edit | base `gpt-5.5` / `medium` |
| `af-flow` implementation | base `gpt-5.5` / `xhigh` |
| computer/browser-use workflow | base `gpt-5.5` / `xhigh` |
| focused bugfix after one failed pass | `gpt-5.5` / `xhigh` |
| `af-full-review` | `deep` or `xhigh` |
| `af-security-review` | `deep` |
| `af-feature-audit`, `af-ui-audit` discovery | `xhigh` for real apps; medium only for tiny/static repos |
| subagent exploration | `gpt-5.4-mini` / `medium` where supported |
| subagent review/security | `gpt-5.5` / `high` or `xhigh` |

## Token Budget Rules

- Keep the AF workflow light, but do not under-reason real development work.
- Use `xhigh` for most `af-flow` implementation, debugging, browser/computer-use, and release-facing work.
- Use `fast` for read-only status, command lookup, and one-file or docs-only edits that do not need deep reasoning.
- Downgrade only when the task is narrow, low-risk, and cheap to verify.
- Avoid default subagent fan-out. Each subagent should have a narrow question and a clear stop condition.
- Prefer devlogs and local Git metadata as compact memory instead of rereading whole chat history or whole repositories.
- Prefer `git diff --stat`, `rg`, and targeted file reads before opening large docs or source trees.

## Rules

- Choose effort before acting, then state or record the choice when it matters.
- Use `xhigh` as the default for most development and computer-use work.
- Use lower effort because the task is clearly cheap, not because token minimization is the only goal.
- Keep subagent fan-out small; subagents multiply token usage.
- Prefer better prompts, narrower scope, and targeted validation before adding agents or broad scans.
