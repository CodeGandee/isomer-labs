## Why

Participating research skills query User Skill Callbacks at both workflow boundaries, but `project skill-callbacks resolve` serializes management metadata and broad Project diagnostics that the executing agent does not need. One active Toolbox callback currently produces about 2.1 KB of JSON while an actionable locator-only projection is about 0.36 KB, so repeated begin and end resolution wastes context and makes agents parse irrelevant state.

## What Changes

- **BREAKING** Make `project skill-callbacks resolve` return a compact execution projection by default: ordered callback ids, source types, absolute instruction entrypoint paths, applicable external-source markers, and resolution-relevant diagnostics.
- Add `project skill-callbacks resolve --explain` for the existing management-oriented callback, registry, source, Toolbox status, and gating details.
- Keep `list`, `show`, and `validate` as the full metadata and provenance surfaces instead of duplicating those views in ordinary resolution.
- Bound callback resolution state loading and diagnostics to Project discovery, selected topic context, visible callback registries, requested insertion-point validation, source integrity, and applicable Toolbox gating.
- Update participating DeepSci and Kaoju skills to consume compact callbacks in returned order and read each reported instruction entrypoint according to its source type.
- Add response-size and diagnostic-relevance regression tests so the agent hot path cannot silently grow back into a management dump.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `user-skill-callbacks`: Separate compact execution resolution from explicit management explanation, define the minimal ordered instruction-locator contract, and restrict ordinary resolution diagnostics to relevant state.
- `isomer-cli-project-discovery`: Narrow the generic callback JSON requirement so each subcommand returns purpose-appropriate fields and expose the new `resolve --explain` mode.
- `research-paradigm-skills`: Require participating skills to consume compact callback locators in application order without requesting or parsing management metadata during normal workflow execution.

## Impact

The change affects the `project skill-callbacks resolve` JSON API, callback command result serialization, callback and topic-context state loading, CLI option wiring, DeepSci and Kaoju packaged skill assets, skill validators, manual documentation, and unit and CLI integration tests. Existing callers that parse full callback records from ordinary `resolve` must switch to `resolve --explain`, `list`, or `show`; callers that execute callbacks must consume the compact instruction-locator projection.
