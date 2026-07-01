## Why

Research v2 skills now preserve semantic placeholders such as `<MAIN_RUN_RECORD>` and `<NEXT_ROUTE_DECISION>`, but working agents still need a concrete, topic-workspace-safe way to create, query, update, and archive the corresponding storage items. Binding these placeholders through a separate page preserves skill flexibility while giving agents a stable Isomer CLI path for durable records.

## What Changes

- Add a research-record CRUD extension under `isomer-cli ext research records` for first-pass topic-scoped durable record operations over Workspace Runtime and semantic record labels.
- Add `placeholder-bindings.md` to v2 research skills so agents can map local placeholders to Isomer storage item classes, artifact profiles, semantic labels, and CRUD command shapes without replacing the placeholders in workflow prose.
- Update v2 research skill routing so agents read `placeholder-bindings.md` alongside `migrate/placeholders.md` before writing durable placeholder outputs.
- Extend validation to require binding pages for active v2 skills with placeholder registries and to ensure placeholder bindings cover registered placeholders.
- Document the transitional relationship among `ext research records`, existing `ext deepsci` compatibility calls, and the later native `project records ...` API.

## Capabilities

### New Capabilities
- `research-placeholder-bindings`: Skill-facing placeholder binding pages and validation for v2 research skills.

### Modified Capabilities
- `research-recording-contracts`: Adds a concrete extension-backed CRUD surface for topic-scoped research records while native `project records ...` commands remain future target APIs.
- `research-paradigm-skills`: Requires v2 research skills to read binding pages when producing or consuming durable placeholders.
- `isomer-cli-project-discovery`: Extends the public CLI command surface with `ext research records` commands.

## Impact

- Adds code under `src/isomer_labs/` for research-record extension commands and storage helpers.
- Updates CLI help, documentation, and unit tests for the new extension command surface.
- Adds generated or maintained binding pages under `skillset/research-paradigm/v2/*/placeholder-bindings.md`.
- Updates research-paradigm skillset validation scripts and tests.
