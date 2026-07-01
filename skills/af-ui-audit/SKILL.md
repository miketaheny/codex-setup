---
name: af-ui-audit
description: Manual full UI/UX audit for responsive design, accessibility, visual consistency, brand-guideline conformance, interaction quality, layout defects, and fix/retest loops. Use only when the user explicitly asks for af-ui-audit, a full UI audit, responsive design audit, UX review, visual inconsistency report, or UI/UX fix campaign.
---

# AF UI Audit

## Purpose

Use this skill for an explicit UI/UX campaign:

```text
establish brand/design baseline -> inspect UI across routes and viewports -> record issues -> fix scoped batches -> retest
```

This is manual-only. Do not run it automatically from `af-finish`, `af-review`, `af-full-review`, or `af-release`.

## Brand Baseline

Before judging visual consistency, look for an existing brand/design source of truth:

```text
docs/BRAND-GUIDELINES.md
docs/brand/
docs/marketing/BRAND-GUIDELINES.md
design.md
style-guide.md
README design sections
theme tokens, CSS variables, Tailwind config, component library config
```

If no usable guideline exists, run `af-brand-guidelines` first unless the user explicitly wants a quick provisional audit. A provisional audit may infer visible design rules from code and screenshots, but must mark brand judgments as provisional.

## Canonical Register

Use one canonical spreadsheet-compatible UI audit register:

```text
docs/product/ui-audit-register.csv
```

If the repo already has a UI audit register, continue that file instead of creating a duplicate. CSV is the default because it is diffable and opens in spreadsheet tools.

Use this schema:

```csv
issue_id,area,page_or_route,viewport,breakpoint,component,source_paths,guideline_ref,issue_type,severity,current_behavior,expected_behavior,evidence,recommendation,status,fix_session,retest_result,notes
```

Allowed statuses:

```text
identified
needs-brand-decision
ready-to-fix
fix-in-progress
fixed-awaiting-retest
verified
accepted
blocked
out-of-scope
```

## Workflow

### 1. Start In Agent-Flow

This skill creates or updates files and may fix UI code, so start or adopt one AF session with `af-flow` before making changes.

If the repo has multiple apps, identify the UI surface being audited. If it cannot be inferred from routes, scripts, package names, or docs, ask one concise question.

### 2. Establish Audit Matrix

Define the routes, screens, and states to inspect from code and docs:

- public pages, app pages, dashboards, auth flows, forms, tables, modals, empty/loading/error states
- navigation, sidebars, headers, footers, settings, search, filters, imports, exports, and reports
- responsive breakpoints including at least mobile, tablet, desktop, and one narrow mobile viewport when practical
- light/dark themes or branded themes when present
- important browser/device constraints documented by the repo

### 3. Inspect UI And UX

Check for:

- responsive overflow, clipping, wrapping, horizontal scroll, unstable layout, and broken breakpoints
- inconsistent spacing, typography, radius, shadows, color use, icon style, component variants, and density
- unclear hierarchy, weak scanability, awkward empty/error states, confusing labels, and slow repeated workflows
- accessibility issues such as contrast, focus states, keyboard traps, target size, labels, alt text, and reduced-motion gaps
- brand-guideline mismatches, missing brand primitives, or one-off styles that should become tokens/components
- console/runtime errors, hydration errors, broken assets, and obvious performance/layout jank when practical

Capture evidence with screenshots, command output, console errors, or artifact paths when useful.

### 4. Record Findings

Every issue should get a register row with:

- exact route/screen/state and viewport
- source path or likely owner
- issue type and severity
- current behavior and expected behavior
- guideline reference or `provisional`
- evidence path or notes
- recommended fix

Severity:

```text
P1 blocks core use or causes severe mobile/accessibility breakage
P2 harms normal use, trust, consistency, or conversion
P3 polish, cleanup, or future design-system consolidation
```

### 5. Fix Scoped Batches

Fixes should use normal AF session discipline:

```text
af-flow -> persistent implementation -> af-devlog -> af-finish
```

Within the same audit session, keep batches coherent by route, component family, or breakpoint class. Avoid broad visual rewrites unless the brand guideline supports them and the diff remains reviewable.

Update `fix_session` and set status to `fixed-awaiting-retest`.

### 6. Retest

Retest affected routes and viewports after fixes.

Update:

- `retest_result`
- `status` to `verified`, `blocked`, or `accepted`
- screenshot/artifact paths when captured
- residual risks in `notes`

### 7. Finish

The audit is done only when:

- the brand/design baseline is recorded or explicitly marked provisional
- the canonical UI audit register exists and is current
- inspected routes and viewport matrix are documented
- P1/P2 findings are fixed, accepted, or blocked with reasons
- fixed issues are retested
- screenshots/manual proof are recorded when useful
- devlog records validation, proof, fixes, and remaining risks
- `af-finish` reports readiness or identifies the remaining blocker

## Safety

- Do not mutate production content, customer data, payments, mass messaging, or destructive admin settings for UI proof.
- Prefer local/dev/staging data, fixtures, screenshots, mocks, and read-only flows.
- Do not invent brand rules when the repo lacks a guideline; mark inferred rules as provisional or use `af-brand-guidelines`.
- Do not make a UI one-note by forcing all components into one hue or decorative style without brand support.

## Output

Report:

- brand guideline path or provisional baseline
- UI audit register path
- route and viewport coverage
- findings by severity and status
- fixes made or sessions needed
- retest results and proof artifacts
- unresolved brand decisions, blockers, and accepted risks
