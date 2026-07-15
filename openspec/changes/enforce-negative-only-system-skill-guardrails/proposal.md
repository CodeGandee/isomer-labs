## Why

The upstream Imsight skill-creation template now reserves `## Guardrails` exclusively for concise negative-action prevention, while Isomer's active specification, validator, tests, and packaged system skills still allow positive `MUST ...` rules there. Aligning the packaged skills now prevents operational procedures, routing rules, and output requirements from becoming a second workflow hidden inside Guardrails.

## What Changes

- Require every active packaged system-skill Guardrails bullet to begin with `DO NOT ...` and state one prohibited action.
- Move positive requirements, ordering, recipes, routing, evidence requirements, and output requirements into Workflow, Procedure, Core Pattern, Contract, or another substantive section without weakening behavior.
- Remove duplicated positive Guardrails when the same behavior is already authoritative in a workflow, subcommand page, command boundary, or output contract.
- Update active entrypoints and executable or behavioral subpages while excluding provenance, migration, passive-template, and archived OpenSpec history.
- Update the packaged-skill validator and unit tests to reject `MUST ...` and other non-`DO NOT ...` Guardrails bullets.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `skill-guardrails-format`: Guardrails become negative-only and positive operational guidance must live in substantive sections.
- `packaged-system-skill-template-format`: Active packaged entrypoints and behavioral subpages must conform to the negative-only Guardrails template while preserving their behavioral contracts.

## Impact

This change affects active Markdown under `src/isomer_labs/assets/system_skills/`, `scripts/validate_skillsets.py`, validator unit tests, and the two modified OpenSpec capabilities. It does not change public skill names, subcommands, domain terminology, CLI interfaces, or archived change records.
