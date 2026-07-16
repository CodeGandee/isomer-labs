## MODIFIED Requirements

### Requirement: Skill Placeholder Binding Pages
The system SHALL provide a `placeholder-bindings.md` page for each active production DeepSci research skill that defines artifact bindings, and the page SHALL use canonical uppercase `DEEPSCI:WHAT` identifiers rather than a second workflow or source representation.

#### Scenario: Binding page exists beside migration registry
- **WHEN** an active production DeepSci research skill contains `migrate/placeholders.md`
- **THEN** the skill also contains `placeholder-bindings.md`

#### Scenario: Binding page preserves canonical artifact identity
- **WHEN** `placeholder-bindings.md` lists an artifact from `migrate/placeholders.md`
- **THEN** both pages use the same exact registered uppercase `DEEPSCI:WHAT` identifier as metadata
- **AND** neither page converts it to an angle-wrapped, double-bracket, bare, lowercase, or mixed-case value or replaces it with a concrete path in workflow prose

#### Scenario: Binding page points to storage operations
- **WHEN** an agent needs to create, read, update, revise, list, show, query, or archive a durable artifact output
- **THEN** `placeholder-bindings.md` names the storage item class, default semantic label, artifact profile, and `isomer-cli ext research records` command shape to use
- **AND** every identity-bearing command passes or filters by the exact artifact identifier through `--semantic-id`

### Requirement: Research Workspace Manager Binding Aggregation
The research workspace manager skill SHALL treat skill-local artifact registries and binding pages as source material for the post-specialization binding registry while preserving canonical uppercase extension artifact identifiers.

#### Scenario: Workspace manager reads binding pages
- **WHEN** `isomer-deepsci-workspace-mgr` builds `DEEPSCI:RESEARCH-PLACEHOLDER-BINDING-REGISTRY`
- **THEN** it reads each relevant skill's `migrate/placeholders.md` and `placeholder-bindings.md`
- **AND** every aggregated row retains the exact registered uppercase `DEEPSCI:WHAT` identifier

#### Scenario: Binding registry records status
- **WHEN** an artifact target is backed by implemented CLI support
- **THEN** the registry marks that binding available
- **AND** when support is planned, custom-needed, blocked, or deferred, the registry records that status instead of inventing an untracked path or alternate identifier

### Requirement: Research Family Artifact Binding Pages
The research-paradigm binding system SHALL support configured research families through one canonical uppercase extension artifact identity grammar.

#### Scenario: Family declares binding vocabulary
- **WHEN** a research family is configured for artifact binding validation
- **THEN** its configuration names the family root, manifest extension id, semantic registry, binding filename, format-profile namespace, expected producers, and required binding fields
- **AND** every active family uses exact uppercase `EXTENSION-NAME:WHAT` identifiers rather than a family-specific or case-normalized grammar

#### Scenario: DeepSci producer has binding page
- **WHEN** a production DeepSci skill produces one or more accepted durable artifacts
- **THEN** its binding page contains one row for every produced `DEEPSCI:WHAT` identifier
- **AND** its normal create, update, revision, list, show, and query commands use `--semantic-id`

#### Scenario: Kaoju producer has binding page
- **WHEN** a production Kaoju skill produces one or more accepted durable semantic artifacts
- **THEN** the skill contains `artifact-bindings.md` with one row for every produced `KAOJU:WHAT` identifier
- **AND** a skill with no accepted durable output may omit the page only when its family configuration permits that disposition

## ADDED Requirements

### Requirement: DeepSci Binding Replacement Is Complete and Collision-Free
The binding validation harness SHALL verify complete replacement of superseded DeepSci artifact identities with canonical uppercase identifiers across source and packaged skill trees.

#### Scenario: Replacement inventory is checked
- **WHEN** implementation validation compares the original DeepSci semantic-object inventory with the replaced registries and binding pages
- **THEN** every semantic object has exactly one canonical uppercase `DEEPSCI:WHAT` identifier and exactly one applicable binding disposition
- **AND** missing, extra, duplicated, colliding, unqualified, lowercase, or mixed-case identifiers fail validation

#### Scenario: Active binding retains a superseded form
- **WHEN** an active DeepSci registry, binding page, command example, source declaration, or generated binding summary contains an angle-wrapped token, double-bracket identifier, bare artifact id, lowercase identifier, mixed-case identifier, artifact alias, or `--placeholder` command
- **THEN** validation reports the skill, file, line, offending value, and violated uppercase artifact-identity rule
- **AND** it does not derive or suggest a replacement value at runtime

#### Scenario: Old-form fixture is inspected
- **WHEN** validation or tests encounter an artifact identity that does not use exact uppercase `EXTENSION-NAME:WHAT`
- **THEN** the identity fails the same way in source, package, CLI, record, and fixture contexts
- **AND** no old-form fixture receives an identity-contract exemption
