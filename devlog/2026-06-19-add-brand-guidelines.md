# Add brand guidelines

- Date: 2026-06-19
- Branch/worktree: detached AF session at `/Users/taheny/vault/teamt/codex-setup-brand-guidelines`, parent `development`
- Commit subject: `docs: add Agent-Flow brand guidelines`
- Commit SHA: pending

## Goal

Create a complete public-facing brand guideline for Agent-Flow and refresh the README so the repo communicates purpose, goals, workflow value, and adoption path more clearly.

## Files Changed

- `README.md`
- `docs/BRAND-GUIDELINES.md`
- `docs/assets/agent-flow-logo.svg`
- `docs/assets/agent-flow-mark.svg`
- `docs/assets/agent-flow-social-card.svg`
- `docs/DOCS-STRATEGY.md`
- `docs/PITCH.md`
- `docs/VISUALS.md`
- `docs/presentations/agent-flow-overview.md`
- `CHANGELOG.md`
- `devlog/2026-06-19-add-brand-guidelines.md`

## Decisions

- Made `docs/BRAND-GUIDELINES.md` the source of truth for positioning, messaging, visual identity, voice, launch surfaces, and public repo presentation.
- Recommended an original Agent-Flow brand system instead of copying Google or OpenAI design language.
- Used OpenAI-style restraint only as an influence for developer-infrastructure tone, while keeping the actual brand identity original and agent-agnostic.
- Added a hand-authored SVG logo suite: full README wordmark, standalone square mark, and social-card/title-card asset.
- Based the mark on an `AF` monogram with flow nodes and a guarded merge lock so the identity points back to Agent-Flow's actual workflow behavior.
- Rewrote the README around public repo adoption: what Agent-Flow is, why it matters, what is included, install/init commands, daily loop, docs map, goals, and brand direction.
- Aligned the README skill list with the skill directories currently present in this repo.

## Validation

- `git diff --cached --check` - passed.
- README documentation links were checked against the local filesystem - passed.
- `find skills -maxdepth 2 -name SKILL.md | sort` - used to verify the README skill list matches the current repo skill directories.
- `xmllint --noout docs/assets/agent-flow-logo.svg docs/assets/agent-flow-mark.svg docs/assets/agent-flow-social-card.svg` - passed.
- `qlmanage -t -s 1200 -o /tmp/agent-flow-logo-preview docs/assets/agent-flow-logo.svg docs/assets/agent-flow-mark.svg docs/assets/agent-flow-social-card.svg` - passed and thumbnails were visually inspected.

## Review Result

- Self-review completed for README positioning, brand guidance, docs map updates, pitch/visual alignment, changelog coverage, and AF devlog coverage. No P1/P2 findings found.

## Follow-ups

- Capture real terminal screenshots after the next install/init demo and add them under `docs/assets/` if the repo is prepared for a public launch.
