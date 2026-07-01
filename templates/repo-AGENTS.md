# Agent-Flow Adapter for Codex

This repository uses AF (Agent-Flow) as the Codex workflow.

Read `.agent-flow/config.toml` when present, then follow `AGENT-FLOW.md`. If a more specific nested `AGENT-FLOW.md` or `AGENTS.md` applies to the file you are editing, follow the more specific file for that path.

If `.agent-flow/config.toml` sets `mode = "disabled"`, disclose that local Agent-Flow enforcement is disabled for this repo and do not enforce AF unless the user asks.

Claude is not installed as an AF adapter. Use `af-claude-review` only when Codex should run Claude CLI as an external review tool.
