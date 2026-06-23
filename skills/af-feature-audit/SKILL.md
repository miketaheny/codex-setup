---
name: af-feature-audit
description: Manual whole-app feature audit for code-grounded user stories, expected behavior, a canonical feature register spreadsheet, test documentation, UX/logistical fix loops, and post-fix retesting. Use only when the user explicitly asks for af-feature-audit, a full feature audit, app-wide user-story inventory, or the feature-register QA loop.
---

# AF Feature Audit

## Purpose

Use this skill for an explicit product/QA campaign:

```text
discover every feature -> write user stories and expected behavior -> test every story -> fix UX/logistical errors -> retest
```

This is manual-only. Do not run it automatically from `af-finish`, `af-review`, `af-full-review`, or `af-release`.

## Canonical Register

Use one canonical spreadsheet-compatible register:

```text
docs/product/feature-register.csv
```

If the repo already has a canonical feature register, use that file instead of creating a duplicate. CSV is the default because it is diffable and can be opened in spreadsheet tools. If the user requires `.xlsx`, generate it as an export only when the CSV remains the source of truth or the user explicitly chooses the `.xlsx` as canonical.

Use this schema:

```csv
feature_id,area,user_role,feature_name,source_paths,route_or_entrypoint,user_story,expected_behavior,acceptance_criteria,priority,status,test_method,test_result,issue_refs,fix_session,retest_result,notes
```

Allowed statuses:

```text
discovered
story-drafted
ready-to-test
test-passed
test-failed
fix-needed
fix-in-progress
fixed-awaiting-retest
verified
blocked
out-of-scope
```

## Workflow

### 1. Start In Agent-Flow

This skill changes files when it creates or updates the register, docs, tests, fixes, or devlog entries. Start or adopt one AF session with `af-flow` before making changes.

If the repo contains several apps or packages, identify the user-facing app surface being audited. If the intended app cannot be inferred from repo structure, ask one concise question before writing the register.

### 2. Discover Features From Code

Inspect the real codebase before writing user stories:

- routes, pages, screens, commands, and entrypoints
- components, forms, tables, workflows, and navigation
- API handlers, server actions, background jobs, and integrations
- tests, fixtures, seed data, docs, and README examples
- auth, permissions, payments, notifications, imports, exports, reports, admin tools, and error flows

Do not invent features. If intent is unclear, write the observed behavior and mark gaps in `notes`.

### 3. Draft User Stories And Expected Behavior

For every user-visible behavior, create or update one row. Use stable IDs such as:

```text
FEAT-001
FEAT-002
```

Write user stories in this format:

```text
As a <role>, I want <capability>, so that <outcome>.
```

Expected behavior and acceptance criteria must be based on code, tests, docs, or directly observed runtime behavior.

### 4. Normalize The Register

Before testing, check that:

- every row has a feature ID, area, role, source path, story, expected behavior, acceptance criteria, priority, and status
- related features are grouped by `area`
- source paths are specific enough for a future agent to inspect
- no duplicate rows describe the same behavior unless they cover different roles or states
- blocked or out-of-scope rows explain why

### 5. Test Every Story

Switch from inventory to testing after the register is complete.

For each row:

- identify the lightest reliable test method: automated test, local command, browser/app flow, API request, fixture, or manual inspection
- run or perform the test when environment access allows it
- record exact results in `test_result`
- set status to `test-passed`, `test-failed`, or `blocked`
- capture screenshot, command output, error text, or artifact paths when useful

Do not claim full coverage when auth, credentials, seed data, external services, or missing tooling prevented testing.

### 6. Fix UX And Logistical Errors

Use the register as the backlog for discovered issues.

Fixes should happen through normal AF sessions:

```text
af-flow -> implementation -> af-devlog -> af-finish
```

Keep each fix session scoped to one issue or a small coherent batch. Do not turn the whole audit into one giant fix commit unless the repo is tiny and the diff is genuinely low-risk.

For each fixed issue, update:

- `issue_refs`
- `fix_session`
- `status` to `fixed-awaiting-retest`
- `notes` with any residual risk

### 7. Retest

Retest every fixed or impacted user story.

Update:

- `retest_result`
- `status` to `verified`, `test-failed`, or `blocked`
- `notes` with remaining errors or accepted risks

If a fix changes expected behavior, update the user story row and any affected docs.

### 8. Finish

The audit is done only when:

- the canonical register exists and is current
- every discovered feature has a story and expected behavior
- every testable story has a test result
- failures have issue references or fix sessions
- fixed behavior has been retested
- blocked rows explain the blocker
- devlog entries record the audit, validation, fixes, and remaining risks
- `af-finish` reports the session ready or identifies the remaining blocker

## Safety

- Do not run destructive production actions, payment captures, mass email/SMS sends, real customer imports, or irreversible admin operations as part of testing.
- Prefer local fixtures, seed data, mocks, sandbox accounts, or read-only checks for risky workflows.
- Keep secrets and customer data out of the register.
- Treat the register as product/QA documentation, not as a replacement for tests or devlog.

## Output

Report:

- canonical register path
- number of features discovered
- counts by status
- testing coverage and blockers
- fixes made or fix sessions needed
- retest results
- validation commands and artifacts
- whether the audit is ready to merge or still blocked
