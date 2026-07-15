## Why

The main `SKILL.md` files in the Imsight skillset were recently standardized to use `## Guardrails` (with strict `DO NOT ...` / `MUST ...` bullets) and `## Troubleshooting Guide` sections. However, subcommand and reference pages inside those skills still use the old `## Common Mistakes` heading, or use `## Guardrails` with loose phrasing such as "Do not ...", "Never ...", or imperative statements like "Use..." / "Preserve...". This inconsistency weakens the behavioral contract for agents that load sub-page detail into context.

## What Changes

- Convert every `## Common Mistakes` section in subcommand/reference pages to `## Guardrails` using the strict `DO NOT ...` / `MUST ...` format.
- Normalize existing `## Guardrails` sections in subcommand/reference pages so every bullet starts with `DO NOT` or `MUST`.
- Move problem-and-recovery content that does not belong in Guardrails into `## Troubleshooting Guide` where appropriate.
- Keep all guardrail and troubleshooting lists sparse, concise, and essential.
- Validate that no `## Common Mistakes` headings remain in sub-pages after the update.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `skill-guardrails-format`: The `DO NOT ...` / `MUST ...` guardrail format now applies to subcommand and reference pages, not only to `SKILL.md` entrypoints.
- `skill-troubleshooting-guide-format`: The two-level problem-and-solution troubleshooting format now applies to subcommand and reference pages where recoverable execution problems exist.

## Impact

- Affected files: subcommand and reference Markdown files under `extern/orphan/houmao-agents/skillset/imsight-skills/*/commands/` and `*/references/`.
- Main `SKILL.md` files are not modified by this change.
- No runtime code, tests, or external dependencies are affected.
