# Codex Model And Effort Policy

Use this policy to optimize Codex speed and token usage without losing depth on risky work.

## Defaults

Base Codex config:

```toml
model = "gpt-5.5"
model_reasoning_effort = "medium"
model_verbosity = "low"
```

This keeps the strongest recommended general Codex model while avoiding `xhigh` as the default for routine work.

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

Use the cheapest setting that matches the risk:

| AF activity | Recommended setting |
|---|---|
| `af-help`, `af-status`, read-only command lookup | `fast` or base medium |
| `af-flow` implementation | base `gpt-5.5` / `medium` |
| focused bugfix after one failed pass | `gpt-5.5` / `high` |
| `af-full-review` | `review` |
| `af-security-review` | `deep` when sensitive, otherwise `review` |
| `af-feature-audit`, `af-ui-audit` discovery | base medium; use `review` for final fix review |
| subagent exploration | `gpt-5.4-mini` / `medium` where supported |
| subagent review/security | `gpt-5.5` / `high` or `xhigh` |

## Rules

- Do not start routine sessions at `xhigh`.
- Escalate effort because the task needs it, not because it is available.
- If a low/medium pass fails twice for the same technical reason, escalate before retrying.
- Keep subagent fan-out small; subagents multiply token usage.
- Prefer better prompts, narrower scope, and targeted validation before increasing effort.
