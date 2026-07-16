## Why

Kaoju skills currently reach outside their own bundles for shared survey contracts, while Kaoju and DeepSci use different conventions for the same class of durable artifact identity. Kaoju uses lowercase extension-qualified semantic ids such as `kaoju:survey-contract`; DeepSci uses angle-wrapped placeholders such as `<MAIN_RUN_RECORD>`, bare pipeline ids, and family-specific conversion code. These inconsistencies couple skills to repository layout, make artifact references difficult to distinguish from ordinary prose, require family-specific parsing, and make active skill prose disagree with source code and CLI contracts.

## What Changes

- Define a package-wide skill/shared-resource contract that distinguishes skill-local resources, shared machine-readable resources, and shared procedural guidance.
- Define one canonical extension artifact identifier syntax, `EXTENSION-NAME:WHAT`, with both segments expressed in uppercase kebab case. The namespace segment is the uppercase projection of the packaged extension's manifest `extension_id`.
- **BREAKING:** Refactor active DeepSci skills, registries, binding pages, examples, generated summaries, validators, tests, source constants, schemas, and record operations to use exact identifiers such as `DEEPSCI:MAIN-RUN-RECORD` instead of angle-wrapped, double-bracket, bare, or lowercase forms.
- **BREAKING:** Refactor Kaoju registries, skills, Python services, CLI operations, tests, and source constants from lowercase values such as `kaoju:survey-contract` to exact uppercase values such as `KAOJU:SURVEY-CONTRACT`.
- Make `semantic_id` the sole artifact-identity field for extension-owned research records and remove artifact-identity parsing, indexing, querying, aliasing, or write behavior for every superseded form. This is a clean break with no conversion or compatibility layer.
- Move the Kaoju survey-process contract, artifact-semantic registry, binding registry, and their validation schemas out of the system-skill asset tree and into the package-owned Kaoju CLI implementation.
- Add read-only `isomer-cli ext kaoju` query commands for the survey-process contract and artifact-binding inventory, including machine-readable list and describe operations.
- Replace parent-relative Kaoju skill references with CLI queries or concise skill-local projections. Keep procedure pages used by one skill inside that skill, and keep cross-skill process guidance in `isomer-kaoju-shared`.
- Preserve `project artifacts describe` as the topic-scoped artifact-operation surface while making `ext kaoju` the agent-facing discovery surface for shared Kaoju contract data.
- Strengthen package and research-skill validation so noncanonical artifact identifiers, parent-relative runtime references, uninstalled sibling resources, duplicated shared process instructions, and filesystem-path coupling fail with deterministic diagnostics.
- Test Kaoju and DeepSci from flat installed-skill projections so repository symlinks cannot hide packaging or identity-contract violations.

## Capabilities

### New Capabilities

- `skill-shared-resource-contract`: Defines ownership, access, naming, installation, and validation rules for skill-local resources, package-shared machine resources, and `<prefix>-shared` procedural guidance.
- `extension-artifact-identity-contract`: Defines the canonical uppercase `EXTENSION-NAME:WHAT` syntax, manifest ownership projection, exact cross-layer representation, clean-break rejection rules, and validation requirements for extension artifact identities.

### Modified Capabilities

- `kaoju-research-extension`: Requires every Kaoju skill to avoid parent-relative runtime dependencies, use exact `KAOJU:WHAT` artifact identifiers, and route shared survey-process data through `ext kaoju` while retaining skill-local command pages and shared procedural guidance in `isomer-kaoju-shared`.
- `kaoju-artifact-bindings`: Makes the package-owned Kaoju CLI the query authority for the versioned binding registry, standardizes registered artifact identifiers, and removes filesystem registry paths from per-skill binding guidance.
- `kaoju-cli-services`: Adds deterministic, read-only Kaoju process and binding discovery commands under `isomer-cli ext kaoju` and requires those commands to consume and return exact canonical artifact identifiers.
- `research-placeholder-bindings`: Replaces DeepSci binding registries and commands with canonical `DEEPSCI:WHAT` identifiers while preserving binding coverage and semantic-versus-storage separation.
- `research-recording-contracts`: Makes uppercase `semantic_id` values the sole extension artifact identity and removes the former placeholder identity surface and all old-form derivation behavior.
- `research-paradigm-skills`: Refactors active DeepSci and Kaoju skills to one uppercase identifier convention and extends validation and fixtures to enforce artifact identity and resource ownership in installed research skill families.
- `packaged-system-skills`: Requires installed-skill validation from a flat projection, canonical manifest-owned artifact identifiers, and exclusion of family-root support files that are not declared skill bundles.

## Impact

The change affects the packaged and source DeepSci skill trees, all DeepSci artifact registries and binding pages, DeepSci pipeline control artifacts, research-record semantic-id parsing and indexing, Kaoju contract loading, semantic and binding registries, the `ext kaoju` CLI command tree, all Kaoju binding summaries, pipeline and shared guidance, research-paradigm validation, installer validation, and unit or integration tests for package-data access and installed projections. Angle-wrapped, double-bracket, bare, mixed-case, and lowercase artifact identities become unsupported everywhere; the system does not derive uppercase identifiers from them or preserve a legacy artifact-identity query path.
