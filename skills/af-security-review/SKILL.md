---
name: af-security-review
description: Formal security review gate before creating pull requests to protected branches such as staging or main, and before explicitly approved direct protected-branch release exceptions.
---

# AF Security Review Skill

Use this skill after normal validation and docs checks, but before creating any pull request whose base is `staging` or `main`. If a repo uses an explicitly approved direct release push to `staging` instead of a pull request, run the same review before that protected-branch push.

This is distinct from `af-review-gate`. The normal review gate checks session quality before merging into a parent branch. This security review checks the accumulated release diff before protected-branch PRs or approved direct release exceptions.

## Inputs

Identify:

- target base branch, usually `staging` or `main`
- candidate head branch, usually `development` or `staging`
- whether staging is enabled in `.agent-flow/config.toml`
- validation already run for the candidate
- any docs, devlog entries, or known risks that changed since the last protected-branch review

## Required Workflow

### 1. Confirm protected target

Run:

```bash
git rev-parse --show-toplevel
git fetch origin --prune
git status --short
git branch --show-current
```

Stop if the worktree is dirty unless the dirty files are explicitly part of the review evidence and will not be included in the protected-branch PR.

### 2. Inspect the release diff

Run:

```bash
git log --oneline <base-branch>..<head-branch>
git diff --name-only <base-branch>...<head-branch>
git diff --stat <base-branch>...<head-branch>
git diff <base-branch>...<head-branch>
```

Review the full diff, not only file names or summaries.

### 3. Check security-sensitive areas

Look specifically for:

- authentication, authorization, session, token, or permission changes
- secret handling, environment variables, credentials, API keys, and config defaults
- input validation, parsing, deserialization, file path, upload, or template rendering behavior
- subprocess, shell, eval, dynamic import, plugin, extension, or code-generation behavior
- network clients, webhook handlers, CORS, redirects, SSRF surfaces, and external service trust boundaries
- database queries, migrations, row-level security, tenant isolation, and data-retention behavior
- cryptography, signing, hashing, random values, and key rotation behavior
- dependency, build, CI, deployment, DNS, infrastructure, logging, telemetry, payment, or privacy changes
- accidental secrets, test credentials, local paths, or sensitive data in committed files

### 4. Run practical security checks

Prefer existing project tooling. Examples include:

- test, lint, typecheck, and build commands already used for release validation
- dependency audit commands when lockfiles and package managers are present
- configured secret scanners such as `gitleaks` or `trufflehog`
- configured static analysis such as CodeQL, Semgrep, Bandit, or framework-specific analyzers
- targeted manual tests for changed auth, permission, input-validation, or release-config behavior

Do not install new security tooling only to satisfy this gate unless the user explicitly approves it. If a relevant tool is unavailable, state that clearly and lower confidence.

### 5. Findings and disposition

Use these severities:

- SEC-P1: blocks protected-branch PR or protected release push until fixed.
- SEC-P2: blocks unless fixed or explicitly accepted by the user and recorded in the PR notes or devlog.
- SEC-P3: non-blocking hardening recommendation that must be recorded.

Do not create a pull request to `main` or `staging` while SEC-P1 findings remain open. Do not create it with SEC-P2 findings unless the user explicitly accepts the risk.

## Required Output

End with one of:

```text
SECURITY REVIEW PASSED FOR <head-branch> -> <base-branch>
```

or

```text
SECURITY REVIEW PASSED WITH ACCEPTED RISKS FOR <head-branch> -> <base-branch>
```

or

```text
SECURITY REVIEW BLOCKED FOR <head-branch> -> <base-branch>
```

Include:

- base branch and head branch
- changed files and security-sensitive areas reviewed
- validation and security checks run
- findings by severity
- risks accepted or deferred
- whether a protected-branch PR or protected release push may proceed
- recommended next command
