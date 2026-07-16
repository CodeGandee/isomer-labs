## ADDED Requirements

### Requirement: Extension Artifacts Use One Canonical Identifier Syntax
Every durable artifact identity owned by a packaged extension SHALL use the exact uppercase form `EXTENSION-NAME:WHAT` and match `^[A-Z0-9]+(?:-[A-Z0-9]+)*:[A-Z0-9]+(?:-[A-Z0-9]+)*$`.

#### Scenario: Extension artifact is named
- **WHEN** an active skill, registry, binding, source constant, schema, CLI request, CLI response, record, test, or generated summary names an extension-owned artifact
- **THEN** it uses the same exact `EXTENSION-NAME:WHAT` identifier
- **AND** it does not wrap the identifier in angle brackets, use a double-bracket form, lowercase or mix its case, or omit the extension namespace

#### Scenario: Identifier describes meaning
- **WHEN** a new extension artifact identifier is registered
- **THEN** its `WHAT` segment names the durable research meaning rather than a path, record kind, profile, storage label, command, producer skill, or provider implementation

#### Scenario: Markdown and shell guidance use the exact value
- **WHEN** active skill guidance displays an artifact identifier in Markdown or passes it to a shell command
- **THEN** Markdown may wrap the exact value in inline-code backticks for presentation and the command passes the unwrapped `EXTENSION-NAME:WHAT` value
- **AND** presentation markup does not become part of the identifier

### Requirement: Extension Ownership Determines the Uppercase Namespace
The system SHALL validate an artifact identifier's uppercase extension namespace against the packaged system-skill manifest or equivalent installed extension catalog.

#### Scenario: Registered extension owns an identifier
- **WHEN** the manifest extension `deepsci` registers `DEEPSCI:MAIN-RUN-RECORD` or the manifest extension `kaoju` registers `KAOJU:SURVEY-CONTRACT`
- **THEN** the identifier namespace exactly equals the uppercase projection of the owning manifest `extension_id`
- **AND** a skill from another extension cannot claim the same complete identifier

#### Scenario: Manifest and artifact conventions remain distinct
- **WHEN** ownership validation compares an artifact namespace with an extension catalog entry
- **THEN** it derives the expected uppercase namespace from the lowercase catalog id only for the ownership check
- **AND** it does not change the catalog id, CLI extension name, skill name, path, profile URI, or artifact identifier

#### Scenario: Namespace is missing or unknown
- **WHEN** active guidance, source data, or a record operation uses a bare object name or an identifier whose uppercase namespace does not identify the owning installed extension
- **THEN** validation rejects it with the offending value and expected uppercase namespace when the owning skill is known
- **AND** it does not infer or persist an identifier

### Requirement: Canonical Artifact Identity Is Preserved Across Layers
Artifact registries, binding services, record operations, and query indexes SHALL store, compare, filter, and return the exact uppercase canonical identifier without presentation conversion or case normalization.

#### Scenario: Skill resolves and writes an artifact
- **WHEN** a skill reads `DEEPSCI:EXPERIMENT-CONTRACT` or `KAOJU:SURVEY-CONTRACT` from binding guidance and invokes the applicable Artifact operation
- **THEN** the registry lookup, CLI argument, record metadata, binding response, and query result use that exact identifier
- **AND** the operation does not require a second placeholder token

#### Scenario: Canonical identity round-trips
- **WHEN** validation loads an identifier from any active registry, projection, source declaration, record, or CLI fixture
- **THEN** parsing and serializing it returns the same exact uppercase value
- **AND** duplicate, ambiguous, case-changing, or lossy mappings fail validation

### Requirement: Artifact Identity Uses a Clean Break
The system SHALL provide no alias, normalization, derivation, indexing, query, or write behavior for any artifact identity that is not exact uppercase `EXTENSION-NAME:WHAT`.

#### Scenario: Superseded form is supplied
- **WHEN** a caller or active source supplies an angle-wrapped, double-bracket, bare, lowercase, or mixed-case artifact identity
- **THEN** the applicable parser, validator, registry, binding service, or record operation rejects the value as noncanonical
- **AND** it does not unwrap, case-fold, qualify, map, promote, or suggest a derived replacement

#### Scenario: Stored record lacks a canonical uppercase identity
- **WHEN** record indexing encounters placeholder metadata or a lowercase semantic id without an authored uppercase `semantic_id`
- **THEN** it does not derive a canonical artifact identity from that metadata
- **AND** the record does not participate in canonical artifact-identity filters through an inferred value

#### Scenario: Artifact alias is declared
- **WHEN** a semantic or binding registry declares an alternate artifact identity for a canonical entry
- **THEN** validation rejects the alias declaration
- **AND** active CLI and service lookup accepts only the canonical registered identifier
