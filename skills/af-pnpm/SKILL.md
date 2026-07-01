---
name: af-pnpm
description: Convert JavaScript or TypeScript repositories to pnpm for Agent-Flow onboarding and worktree-friendly dependency installs. Use when the user asks to check whether a repo uses pnpm, convert npm/yarn/bun repos to pnpm, standardize package-manager setup, reduce node_modules duplication across worktrees, or run the pnpm onboarding step from init-repo.
---

# AF pnpm

## Goal

Standardize Node-based repos on pnpm when appropriate, while keeping conversion evidence and follow-up risks visible. This is useful for AF worktrees because pnpm's shared store avoids reinstalling full package contents for every worktree.

## Safety Rules

- If the repo has no `package.json`, report that it is not a Node repo and make no package-manager changes.
- If the repo already has `pnpm-lock.yaml`, `pnpm-workspace.yaml`, or `packageManager` set to `pnpm@...`, report that pnpm is already configured.
- For file-changing conversions, start or adopt one AF session with `af-flow` before editing unless the conversion is running as part of `init-repo.sh` onboarding.
- Do not edit secrets, production config, deployment credentials, or app code just to make pnpm pass.
- Do not hide failures by switching pnpm to hoisted mode globally. Prefer fixing undeclared dependencies and only use compatibility settings when the repo genuinely needs them.
- Treat dependency-manager migration as dependency-sensitive work. Run tests/builds and mention that release-time `af-full-review` may route to `af-security-review` if the dependency diff is high-risk.

## Quick Commands

Check only:

```bash
python3 ~/.agent-flow/skills/af-pnpm/scripts/convert_to_pnpm.py . --check
```

Convert:

```bash
python3 ~/.agent-flow/skills/af-pnpm/scripts/convert_to_pnpm.py . --convert --yes
```

During onboarding, `init-repo.sh` calls the same helper for repos with a root `package.json`. Use `--no-pnpm` to skip that step.

## Conversion Workflow

1. Inspect current state:

```bash
git status --short
test -f package.json && sed -n '1,220p' package.json
ls package-lock.json npm-shrinkwrap.json yarn.lock bun.lock bun.lockb pnpm-lock.yaml pnpm-workspace.yaml 2>/dev/null || true
```

2. Run the helper in check mode first unless `init-repo.sh` is already driving onboarding.

3. Convert with the helper. It will:

- detect the current package manager from `packageManager`, lockfiles, and workspace files
- ensure `pnpm` is available, using Corepack when possible
- add or update `packageManager` to the active `pnpm@<version>`
- create `pnpm-workspace.yaml` from `package.json` workspaces when needed
- run `pnpm import` when a legacy lockfile is available
- run `pnpm install`
- remove legacy npm/yarn/bun lockfiles only after install succeeds
- scan common repo files for follow-up command updates such as `npm ci`, `npm install`, `npx`, `yarn`, or `bun install`

4. Update obvious scripts, docs, and CI after conversion:

```text
npm ci        -> pnpm install --frozen-lockfile
npm install   -> pnpm install
npm run build -> pnpm build
npx tool      -> pnpm dlx tool   # one-off package
npx tool      -> pnpm exec tool  # installed local bin
yarn install  -> pnpm install
bun install   -> pnpm install
```

5. Validate with the repo's normal checks:

```bash
pnpm install --frozen-lockfile
pnpm test
pnpm build
```

Run only the commands that exist for the repo. If package scripts differ, inspect `package.json` and use the closest project-native checks.

## Recommendations

- Prefer pnpm conversion repo-by-repo, not across all local repos at once.
- Keep `packageManager` pinned so agents and CI use the same pnpm major version.
- Use `pnpm-workspace.yaml` for monorepos; do not rely only on npm/yarn workspace metadata.
- Let each worktree run `pnpm install`; pnpm will reuse the shared store without symlinking the whole `node_modules`.
- For broken packages that rely on undeclared transitive dependencies, fix the dependency declaration first. Use `.npmrc` compatibility settings only as a documented fallback.
- Update CI and deploy settings in the same session when they are clearly part of the package-manager migration.
