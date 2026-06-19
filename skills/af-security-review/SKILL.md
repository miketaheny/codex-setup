---
name: af-security-review
description: Deep security-only review for Agent-Flow releases or high-risk diffs. Use when requested, when config requires it, when af-full-review flags security-sensitive areas, or before a protected-branch PR/direct release exception that changes auth, secrets, input validation, dependencies, infrastructure, privacy, or data access.
---

# AF Security Review

Use this as a distinct security gate. It is not the general release review; run `af-full-review` for broad correctness and release readiness.

## Inputs

Identify:

- base branch and head branch or commit range
- whether the review was requested, config-required, or triggered by security-sensitive changes
- validation already run
- docs, devlog entries, known risks, and accepted risk context

## Workflow

### 1. Confirm Context

```bash
git rev-parse --show-toplevel
git fetch origin --prune
git status --short
git branch --show-current
```

Stop if the worktree is dirty unless the dirty files are explicit review evidence and will not be included in the release.

### 2. Inspect Full Diff

```bash
git log --oneline <base>..<head>
git diff --name-only <base>...<head>
git diff --stat <base>...<head>
git diff <base>...<head>
```

Review the full diff, not only summaries.

### 3. Security Focus Areas

Look for:

- authentication, authorization, sessions, tokens, and permissions
- secrets, environment variables, credentials, API keys, and config defaults
- input validation, parsing, deserialization, file paths, uploads, and template rendering
- subprocess, shell, eval, dynamic import, plugin, extension, and generated-code behavior
- network clients, webhooks, CORS, redirects, SSRF surfaces, and trust boundaries
- database queries, migrations, row-level security, tenant isolation, and retention behavior
- cryptography, signing, hashing, random values, and key rotation
- dependencies, build, CI, deployment, DNS, infrastructure, logging, telemetry, payment, privacy, and accidental sensitive data

### 4. Practical Checks

Prefer existing project tooling: tests, lint, typecheck, build, dependency audit, secret scanning, static analysis, and targeted manual tests for changed security behavior.

Do not install new security tooling only to satisfy this gate unless the user approves it. If a relevant tool is unavailable, state that and lower confidence.

### 5. Findings

Use:

- SEC-P1: blocks release or protected-branch PR until fixed.
- SEC-P2: blocks unless fixed or explicitly accepted by the user.
- SEC-P3: non-blocking hardening recommendation.

## Output

End with `SECURITY REVIEW PASSED FOR <head> -> <base>`, `SECURITY REVIEW PASSED WITH ACCEPTED RISKS FOR <head> -> <base>`, or `SECURITY REVIEW BLOCKED FOR <head> -> <base>`.

Include changed files, sensitive areas reviewed, checks run, findings, accepted risks, and whether the release may proceed from a security standpoint.
