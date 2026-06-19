---
name: af-show
description: Capture visual or manual proof for an Agent-Flow session. Use when a change affects UI, routes, generated pages, rendered docs, CLI output, local artifacts, screenshots, or workflows that should be opened, inspected, screenshotted, or manually verified before finish or merge.
---

# AF Show

## Purpose

Use this skill to prove what changed can be seen or exercised. Prefer lightweight local verification over production deploys.

## Workflow

### 1. Decide What To Show

Identify the smallest useful proof target:

- app route or changed UI workflow
- generated documentation page or static artifact
- local file, PDF, image, CLI output, or report
- before/after state when a regression was fixed

If the change is non-visual and has no meaningful manual surface, record `not applicable`.

### 2. Start Or Open

Prefer documented local commands from README, package scripts, Makefile targets, docs, or CI. Reuse an already-running local server only when it clearly points at the current checkout.

Do not run production deploys, destructive database commands, payment/auth side effects, or external release actions as proof commands.

### 3. Inspect

Use available browser, screenshot, image, PDF, CLI, or shell tools to inspect the target. Check the changed path, relevant viewport or output, obvious console/runtime errors when practical, and the behavior the session changed.

If auth, missing credentials, unavailable tooling, or environment setup blocks proof, state the blocker and use the best local fallback without claiming visual confirmation.

### 4. Record Proof

Record in the devlog and final output:

- command used to start or open
- URL/path/command output inspected
- screenshot or artifact path when captured
- pass/fail/blocked/not-applicable status
- any residual risk

Stop a dev server only when you started it solely for this proof and the user does not need it left running.
