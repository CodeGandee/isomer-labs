## Why

The Imsight skillset under `extern/orphan/houmao-agents/skillset/imsight-skills/` currently mixes `## Common Mistakes` and `## Guardrails` sections inconsistently. The skill-creation template in `imsight-agent-skill-handling/references/create.md` was recently revised to require a unified `## Guardrails` section using "DO NOT ..." and "MUST ..." rules, plus a separate `## Troubleshooting Guide` section for execution problems. Existing skills must be updated to follow this standard so agents receive consistent behavioral guardrails and practical recovery guidance across the skillset.

## What Changes

- Rename every `## Common Mistakes` section to `## Guardrails` across the 11 affected Imsight skills.
- Merge the duplicate `## Guardrails` and `## Common Mistakes` sections in `imsight-autodev-master` and `imsight-autodev-slave` into a single `## Guardrails` section.
- Rewrite all guardrail bullets as concise "DO NOT ..." or "MUST ..." statements that protect each skill's design intent and reinforce preferred actions.
- Move problem-and-recovery content that does not belong in Guardrails into a new or updated `## Troubleshooting Guide` section where appropriate.
- Keep guardrail lists sparse and essential; remove redundant or non-essential items.
- Validate that no `## Common Mistakes` headings remain in the skillset after the update.

## Capabilities

### New Capabilities

- `skill-guardrails-format`: Defines the standard format and writing rules for `## Guardrails` sections in Imsight skills, including "DO NOT ..." prohibitions and "MUST ..." requirements.
- `skill-troubleshooting-guide-format`: Defines the standard format for `## Troubleshooting Guide` sections in Imsight skills, including nested problem-and-recovery bullets.

### Modified Capabilities

- None. This change updates skill documentation and formatting; it does not alter code-level APIs or runtime behavior.

## Impact

- Affected files: `SKILL.md` files in `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-*/`.
- The `imsight-agent-skill-handling/references/create.md` template already reflects the new standard and is not modified by this change.
- No runtime code, tests, or external dependencies are affected.
