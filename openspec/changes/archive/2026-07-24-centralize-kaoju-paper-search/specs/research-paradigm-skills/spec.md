## MODIFIED Requirements

### Requirement: Production Kaoju Research-Paradigm Layout
The production Kaoju family SHALL include an independent public welcome and execution entrypoint while preserving the accepted protected survey-process inventory and shared-resource ownership.

#### Scenario: Kaoju public layout is inspected
- **WHEN** production Kaoju directories are enumerated
- **THEN** the public directories are `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint`
- **AND** protected capabilities remain below the entrypoint using stable `isomer-kaoju-*` logical ids

#### Scenario: Kaoju active resources are separated
- **WHEN** Kaoju welcome and entrypoint resources are classified
- **THEN** newcomer examples and command maps belong to welcome while command implementations and protected capability resources belong to entrypoint or the selected subskill
- **AND** the package-owned process and binding registries remain the sole machine authorities

#### Scenario: Research-paradigm documentation lists both families
- **WHEN** family documentation is inspected
- **THEN** it lists `isomer-ext-deepsci-entrypoint` and `isomer-ext-kaoju-entrypoint` as optional public packs

#### Scenario: Kaoju active surface is concise and self-contained
- **WHEN** the Kaoju pack is inspected
- **THEN** its public entrypoint owns public commands and its protected members own stage-specific behavior and resources
- **AND** no old pipeline facade or top-level protected member remains

#### Scenario: Paper-search provider material remains protected
- **WHEN** the protected `paper-search` member is inspected
- **THEN** its top-level guidance owns provider-neutral paper-search actions while its bundle-local references own S2 endpoint and execution details
- **AND** public Kaoju commands, core schema, and generic provider contracts do not expose the S2 API catalog

#### Scenario: Paper-search preserves the agent and data-service boundary
- **WHEN** the protected `paper-search` member executes and records a provider-backed action
- **THEN** its selected approach directs the agent to an available external provider-native or general-purpose CLI or bounded HTTPS tool and normalizes the returned provider output
- **AND** `isomer-cli ext research literature` receives only the normalized observation for local validation, recording, indexing, and query

#### Scenario: Kaoju template roles remain explicit
- **WHEN** public manager, paper drafting, TeX composition, PDF build, or protected write guidance is inspected
- **THEN** it distinguishes named content templates from named LaTeX templates, including their independent `main` defaults and semantic ids
- **AND** role selection remains explicit command context rather than a new skill boundary

#### Scenario: Kaoju write resources remain protected
- **WHEN** the protected `write` member is inspected after relocation
- **THEN** its entrypoint, artifact bindings, paper references, and role-aware workflow remain inside the `isomer-kaoju-write` bundle
- **AND** public paper commands route to that member without duplicating its private procedure resources

#### Scenario: Kaoju skills use canonical Isomer language
- **WHEN** public and protected Kaoju guidance is inspected
- **THEN** it retains canonical Isomer domain terms and provider boundaries

### Requirement: Research-Paradigm Validation Supports Kaoju
Research-paradigm validation SHALL enforce Kaoju welcome, entrypoint, and protected-member roles without weakening existing Kaoju-specific rules.

#### Scenario: Valid Kaoju pair passes
- **WHEN** the Kaoju pack has canonical public metadata, complete welcome command coverage, a valid execution entrypoint, and sixteen valid protected members
- **THEN** research-paradigm validation accepts the public/protected layout

#### Scenario: Kaoju welcome copies execution procedure
- **WHEN** active welcome guidance embeds manager implementation, command execution steps, or protected private resource paths
- **THEN** validation reports a role-boundary violation
- **AND** it directs the content to an entrypoint command or protected owner

#### Scenario: Invalid Kaoju member reports diagnostics
- **WHEN** a protected member is missing, crosses a resource boundary, has a stale direct invocation, or violates identity mapping
- **THEN** validation reports its logical id, parent pack, file, and rule

#### Scenario: Paper-search top-level leaks provider API
- **WHEN** `isomer-kaoju-paper-search/SKILL-MAIN.md` contains an endpoint inventory, base-URL catalog, credential value, or external checkout dependency
- **THEN** validation reports the provider-boundary or resource-boundary violation
- **AND** it requires action-oriented top-level guidance and bundle-local provider references

#### Scenario: Paper-search routes provider execution through Isomer CLI
- **WHEN** active paper-search guidance tells the agent to invoke an `isomer-cli` provider search, resolution, recommendation, citation-fetch, or reference-fetch command
- **THEN** validation reports an execution-boundary violation
- **AND** it directs provider execution to a bundle-local external-tool approach and reserves `ext research literature` for local data operations

#### Scenario: Shared checks preserve family rules
- **WHEN** common pack validation succeeds
- **THEN** trial versus reproduction, evidence, binding, artifact identity, survey-process, content-template, LaTeX-template, composition, build-entrypoint, drift, and historical-record checks still run

#### Scenario: Validator tests cover Kaoju active and invalid zones
- **WHEN** unit tests exercise family-aware research-paradigm validation
- **THEN** they include valid Kaoju fixtures and failures for missing inventory, wrong namespace, manifest mismatch, broken direct references, stale domain terms, hard-coded provider or local paths, paper-search action or provider-resource drift, procedural-command drift, binding drift, directory scanning, canonical-format violations, external wiki routing, direct environment mutation, Isomer-owned repository acquisition, and pre-verification registration
