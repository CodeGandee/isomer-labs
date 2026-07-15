## Context

The main `SKILL.md` files in the Imsight skillset now follow a unified `## Guardrails` / `## Troubleshooting Guide` format. Subcommand and reference pages (under `commands/` and `references/`) still mix `## Common Mistakes` with loosely phrased `## Guardrails`. Agents load these sub-pages into context when executing detailed workflows, so inconsistent behavioral guidance here directly affects execution quality.

## Goals / Non-Goals

**Goals:**

- Every subcommand/reference page in the Imsight skillset uses `## Guardrails` instead of `## Common Mistakes`.
- All guardrail bullets in subcommand/reference pages start with `DO NOT` or `MUST`.
- Problem-and-recovery content moves to `## Troubleshooting Guide` where appropriate.
- No `## Common Mistakes` headings remain in sub-pages after the update.

**Non-Goals:**

- Changing main `SKILL.md` files (already done in a prior change).
- Adding new functionality, scripts, or references.
- Updating top-level skillset documentation unless it references old section names.
- Running pressure tests or full skill validation suites.

## Decisions

- **Apply the same standard to sub-pages.** The `DO NOT ...` / `MUST ...` guardrail format and the two-level troubleshooting format apply to any Markdown page that an agent may execute as part of a skill workflow, not just the entrypoint.
- **Convert Common Mistakes to Guardrails.** Most sub-page `Common Mistakes` bullets describe prohibited or required behaviors; rewrite them as guardrails.
- **Normalize loose Guardrails.** Existing guardrails using "Do not ...", "Never ...", or imperative guidance are rewritten as strict `DO NOT ...` or `MUST ...` statements.
- **Preserve page-specific detail.** Each sub-page has domain-specific rules; do not generalize or merge rules across pages.
- **No mechanical rewrite.** Review each bullet to ensure the converted rule still matches the page's actual workflow and intent.

## Risks / Trade-offs

- **Volume of files** — ~38 sub-pages need edits. Mitigation: batch by skill and use focused edits per file.
- **Over-normalization** — Some imperative guidance (e.g., "Use byte-range downloads...") may become awkward as `MUST`. Mitigation: keep the rephrased rule concrete and readable.
- **Scope creep** — It is tempting to also refactor workflow wording while editing. Mitigation: restrict edits to Guardrails/Troubleshooting/Common Mistakes sections.
- **Inconsistent classification** — Some bullets could be either guardrails or troubleshooting. Mitigation: ask "Is this a prohibited/required behavior, or a recoverable execution problem?" for each bullet.
