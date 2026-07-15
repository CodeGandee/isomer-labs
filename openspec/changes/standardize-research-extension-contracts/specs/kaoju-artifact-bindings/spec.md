## MODIFIED Requirements

### Requirement: Kaoju Artifact Semantics Are Storage-Neutral
The Kaoju extension SHALL define one shared artifact semantic registry whose entries describe durable survey meanings independently of storage implementation and are queryable through the package-owned Kaoju extension surface.

#### Scenario: Semantic entry avoids physical binding
- **WHEN** an agent reads a Kaoju artifact semantic entry returned by the extension or summarized by bundle-local shared guidance
- **THEN** the entry provides a stable canonical identifier such as `KAOJU:SURVEY-CONTRACT`, meaning, required semantic content, producer, consumer, and update intent
- **AND** it does not prescribe a filesystem path, record-store subpath, provider payload, or implementation command body

#### Scenario: Active skills use registered semantic ids
- **WHEN** active Kaoju guidance names an accepted durable output
- **THEN** it uses an exact registered `KAOJU:WHAT` identifier available from the shared Kaoju extension query
- **AND** it does not wrap the identifier in angle brackets, use a bare object name, or use lowercase or mixed case
- **AND** unregistered or ambiguous durable output semantics are reported by validation

### Requirement: Kaoju Artifact Bindings Are Separate and Complete
The package-owned Kaoju extension implementation SHALL provide one versioned machine-readable Kaoju binding registry that is separate from the storage-neutral semantic registry and complete for every active Kaoju semantic id.

#### Scenario: Binding entry is complete
- **WHEN** the binding registry maps a Kaoju semantic id
- **THEN** the entry names its artifact type, compatible record kind, default semantic label, family-neutral format profile, content mode, producer, consumers, required relationship roles, revision mode, scope-key policy, latest-selection policy, and validation and acceptance expectations
- **AND** it does not embed executable commands, provider payloads, credentials, or implementation-specific command bodies

#### Scenario: Binding coverage is bidirectional
- **WHEN** the Kaoju binding validator compares the shared semantic registry, active skill references, binding registry, schema and renderer assets, and built-in profile catalog
- **THEN** it rejects missing, extra, duplicated, cross-family, unresolved, aliased, non-uppercase, or incompatible semantic ids, profiles, producers, consumers, scope policies, and content modes
- **AND** each diagnostic names the family, semantic id, affected file, line when available, and violated binding rule

#### Scenario: Skills discover and apply physical bindings
- **WHEN** a Kaoju skill needs to inspect a binding before creating, revising, or querying an accepted durable output
- **THEN** it discovers the contract through an exact command such as `isomer-cli --print-json ext kaoju bindings describe KAOJU:SURVEY-CONTRACT` and uses `isomer-cli project artifacts` for the topic-scoped operation
- **AND** the extension query and project artifact service resolve the same package-owned canonical registry

#### Scenario: Per-skill binding guidance remains a local projection
- **WHEN** a skill contains `artifact-bindings.md` or equivalent local guidance
- **THEN** that bundle-local page may summarize only the semantic ids and usage needed by its owning skill and directs the agent to the extension query for current binding data
- **AND** it does not name a registry filesystem path, become an independent physical binding authority, or repeat full executable command shapes

#### Scenario: Binding selects a storage surface without defining an internal path
- **WHEN** a Kaoju binding selects a managed content mode and default Semantic Workspace Surface Label
- **THEN** the artifact service allocates a generic internal path from record kind and opaque record or revision identity
- **AND** the binding and producer do not declare, construct, or rely on a Kaoju-specific subdirectory convention
