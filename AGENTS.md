# Agent-Flow Adapter for Codex

This project uses AF (Agent-Flow) as the Codex workflow.

Read `.agent-flow/config.toml` when present, then follow `AGENT-FLOW.md`. If a repository contains a more specific nested `AGENT-FLOW.md` or `AGENTS.md`, follow the more specific file for that path.

Codex-specific note: this file exists so Codex auto-loads Agent-Flow. Claude is not installed as an AF adapter; use `af-claude-review` only when Codex should call Claude CLI as an external reviewer.
