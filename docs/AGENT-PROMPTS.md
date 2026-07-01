# Useful Agent-Flow Prompts

## Help

```text
Use af-help. Show me the Agent-Flow command map, skill choices, and usage-guide path.
```

## Brand Guidelines

```text
Use af-brand-guidelines. Create or ingest this repo's brand/design guideline for UI work, mark whether it is canonical or provisional, and record open questions.
```

## Start Or Continue Work

```text
Use af-flow for this file-changing request. Create or adopt one AF session worktree, keep related follow-up work in that same worktree, and do not finish until I ask to wrap up, review, reconcile, merge, or switch direction.
```

## Finish Existing Session

```text
Use af-finish. Run validation, use af-show if visual or manual proof matters, verify devlog/docs, run af-review, and ask me before merging into the recorded parent branch.
```

## Review Only

```text
Use af-review. Review this session worktree against its recorded parent branch and tell me whether it is ready to merge.
```

## Status Snapshot

```text
Use af-status. Summarize current Agent-Flow status, push-readiness blockers, and all worktree states without mutating anything.
```

## Visual Proof

```text
Use af-show. Start or open the relevant app, page, artifact, or command output, inspect the changed behavior, and record proof status in the devlog.
```

## Release Prep

```text
Use af-reconcile, then af-full-review, then af-release. Run af-security-review only if requested, config-required, or security-sensitive. If Codex Security is available, prefer its diff-scan path for the release diff.
```

## Security Review

```text
Use af-security-review for [head] against [base]. Prefer Codex Security diff scan when available, then report security-sensitive behavior, checks, findings, accepted risks, and any fallback reason.
```

## Project Docs

```text
Use af-docs. Update project docs from devlog entries, commits, changed scripts, skills, templates, screenshots, and config.
```

## pnpm Conversion

```text
Use af-pnpm. Check whether this repo already uses pnpm, convert it if needed, update obvious CI/docs commands, and validate install/build/test.
```

## Feature Audit

```text
Use af-feature-audit on this app. Go over every feature, create a user story with expected behavior from the code, keep one canonical feature register, test every story, fix UX/logistical errors in scoped AF sessions, and retest after fixes.
```

## UI Audit

```text
Use af-ui-audit on this app. Audit responsive design, visual consistency, accessibility, brand conformance, UX issues, and layout defects across routes and viewports; keep one canonical UI audit register, fix scoped batches, and retest.
```

## Existing Docs Stewardship

```text
Use af-docs. Inventory existing docs, ask targeted questions about audience and maintenance rules, update useful docs in place, and create or update docs/DOCS-STRATEGY.md.
```

## Backlog Migration

```text
Use af-migrate-backlog-devlog. Dry-run a migration from Backlog.md, triage.md, backlog/, or .backlog files to devlog entries, show the plan, then write entries after approval.
```

## Push Readiness

```text
Run scripts/check-push-readiness.sh for the branch I am about to push. Block the push if any child AF session worktree is dirty or unmerged.
```
