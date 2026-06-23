---
name: af-brand-guidelines
description: Create, ingest, interview for, or update a repo brand/design guideline for UI work. Use when the user asks for af-brand-guidelines, brand guidelines, design-system guidance, visual standards, UI style rules, or when af-ui-audit needs a brand baseline and the repo lacks a usable guideline.
---

# AF Brand Guidelines

## Purpose

Use this skill to establish the repo's UI brand/design source of truth before broad UI work.

Default canonical file:

```text
docs/BRAND-GUIDELINES.md
```

If a repo already uses a more specific brand path, such as `docs/brand/` or `docs/marketing/BRAND-GUIDELINES.md`, update that file instead of creating a duplicate.

## Modes

### Ingest

Use when the user provides brand docs, screenshots, links, design files, CSS tokens, logos, colors, copy guidance, or existing style rules.

Preserve provenance. Distinguish user-provided rules from inferred rules.

### Interview

Use when brand direction is unclear and the user is available. Ask only the questions that materially affect UI decisions:

- audience and product category
- desired feel: operational, premium, playful, editorial, technical, restrained, energetic, etc.
- references to keep or avoid
- logo/wordmark and color constraints
- typography preferences or existing fonts
- component density, radius, icon style, imagery, motion, and accessibility expectations
- mobile/responsive priorities
- content voice and product terminology

If the user does not answer and progress is expected, create a provisional guideline from repo evidence and mark open questions.

### Create From Repo Evidence

Inspect:

- existing docs, README, pitch, marketing, screenshots, and demo files
- CSS variables, theme config, Tailwind config, design tokens, component libraries, and layout primitives
- existing pages/components for repeated colors, typography, spacing, radius, iconography, density, and interaction patterns
- product domain, user roles, operational context, and accessibility needs

Do not invent logos, metrics, customer claims, fonts, or brand assets. Mark uncertain choices as provisional.

## Guideline Structure

Use or update this structure:

```md
# Brand Guidelines

## Source And Status
## Product Positioning
## Audience
## Brand Attributes
## Voice And Terminology
## Color
## Typography
## Spacing, Radius, Shadow, And Density
## Components And Interaction Patterns
## Iconography And Imagery
## Responsive Behavior
## Accessibility
## Do / Do Not
## Open Questions
```

Keep it practical for implementation. Prefer token names, CSS variables, component examples, and concrete do/do-not rules over vague adjectives.

## Workflow

### 1. Start In Agent-Flow

Creating or updating brand guidelines changes files, so start or adopt one AF session with `af-flow`.

### 2. Find Existing Sources

Search for existing brand/design sources before writing:

```text
docs/BRAND-GUIDELINES.md
docs/brand/
docs/marketing/BRAND-GUIDELINES.md
design.md
style-guide.md
theme config
CSS variables
component library config
```

### 3. Decide Status

Mark the guideline as one of:

```text
canonical
imported
provisional
needs-user-review
```

Use `canonical` only when the user supplied or approved it, or the repo already treats it as authoritative.

### 4. Write Or Update The Guideline

Create the canonical file only if no suitable one exists. If a brand doc already exists, update it in place.

Include:

- source/provenance
- implementation tokens and paths
- design rules for UI audits and future frontend work
- responsive and accessibility expectations
- open questions and decisions needed

### 5. Validate

Check links and references. If code tokens are cited, verify the paths exist. If the guideline is provisional, do not present it as approved brand direction.

## Output

Report:

- guideline path
- status: canonical, imported, provisional, or needs-user-review
- sources used
- key decisions made
- open questions
- how `af-ui-audit` should use the guideline
