## Why

Many Isomer skills describe required chat content as literal field inventories such as `interpreted_goal`, `selected_route`, or `resource_check_status`. Agents consequently render ordinary answers as pseudo-program output instead of readable technical prose, and nested skill routing can merge incompatible field vocabularies into one response.

## What Changes

- Require every active Isomer skill to present normal chat responses in natural language with descriptive Markdown sections and genuine lists.
- Treat named output items as semantic coverage requirements rather than literal chat labels or serialization keys.
- Separate output depth, Essential or Complete, from presentation format, natural Markdown or explicitly requested machine-readable output.
- Preserve exact fields and schemas for durable records, CLI and API payloads, manifests, receipts, and other explicitly structured artifacts while requiring a natural-language chat summary.
- Rewrite chat-facing output guidance that currently encourages `snake_case: value`, pseudo-JSON, pseudo-YAML, or flat record-style responses.
- Extend skill validation and tests so the natural-language presentation rule remains present and machine-shaped chat contracts do not return.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `skill-output-contracts`: Extend the shared output convention to separate content depth from presentation format and require natural-language Markdown chat responses across active Isomer skills, including research-paradigm skills, without weakening structured durable-output schemas.

## Impact

This change affects active packaged skill guidance under `src/isomer_labs/assets/system_skills/`, repository-local development and Toolbox skills under `skillset/`, the skillset validator in `scripts/validate_skillsets.py`, and focused validator and asset tests. It does not change Isomer CLI or API response schemas, durable research record formats, or installed projection layout.
