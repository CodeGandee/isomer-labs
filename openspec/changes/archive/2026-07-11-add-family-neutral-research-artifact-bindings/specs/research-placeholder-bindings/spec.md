## ADDED Requirements

### Requirement: Research Family Artifact Binding Pages
The research-paradigm binding system SHALL support configured research families whose durable semantic objects are not DeepSci migration placeholders.

#### Scenario: Family declares binding vocabulary
- **WHEN** a research family is configured for artifact binding validation
- **THEN** its configuration names the family root, semantic registry, semantic-id pattern, binding filename, format-profile namespace, expected producers, and required binding fields
- **AND** DeepSci continues using its existing placeholder registry and `placeholder-bindings.md` rules

#### Scenario: Kaoju producer has binding page
- **WHEN** a production Kaoju skill produces one or more accepted durable semantic artifacts
- **THEN** the skill contains `artifact-bindings.md` with one row for every produced semantic id
- **AND** a skill with no accepted durable output may omit the page only when its family configuration permits that disposition

### Requirement: Family Binding Validation Preserves Semantic Separation
Binding validation SHALL compare semantic definitions and actual bindings without moving storage choices into method prose.

#### Scenario: Registry and binding coverage match
- **WHEN** validation inspects a configured research family
- **THEN** every active semantic id has one owner or explicitly shared binding, every binding id exists in the semantic registry, and every structured profile resolves from the declared namespace
- **AND** missing, duplicate, extra, cross-family, or unresolved entries fail validation

#### Scenario: Semantic registry contains physical binding
- **WHEN** a storage-neutral semantic registry entry includes a concrete path, semantic label, record kind, profile, or create command
- **THEN** validation reports premature physical binding and points to the producer binding page that should own it

#### Scenario: Active skill invents command shape
- **WHEN** active stage guidance gives a conflicting record kind, label, profile, or normal create command instead of routing to its binding page
- **THEN** validation reports binding drift with the skill, semantic id, and authoritative binding location

### Requirement: Family Bindings Use Payload-First Record Operations
Configured family binding pages SHALL define accepted structured outputs through validated payload-file records and family-neutral semantic identity.

#### Scenario: Kaoju create command is complete
- **WHEN** a Kaoju structured binding gives its normal create command
- **THEN** it uses global `isomer-cli ext research records create` with `--semantic-id`, `--record-kind`, `--format-profile`, `--skill`, producer and consumer metadata hooks, and `--payload-file`
- **AND** it does not use direct Markdown `--body` or `--body-file` authoring as canonical state

#### Scenario: Binding defines lifecycle operations
- **WHEN** an agent needs to inspect or change a bound semantic object
- **THEN** its binding authority defines exact list, show, revision or follow-up, metadata update, on-demand render or export, and archive patterns
- **AND** it distinguishes content revision from status-only mutation and separate descendant evidence

#### Scenario: Binding defines lineage and query metadata
- **WHEN** a bound record derives from prior records or carries authored relationships, files, claims, metrics, catalog items, or status facets
- **THEN** the binding distinguishes canonical parent lineage from relationship, file, and index hints
- **AND** it names the payload paths or metadata inputs that drive profile-based extraction

### Requirement: Research Workspace Managers Aggregate Family Bindings
Each configured research family workspace manager SHALL aggregate selected skill bindings into a topic-level readiness index.

#### Scenario: Kaoju workspace manager builds binding index
- **WHEN** `isomer-kaoju-workspace-mgr` prepares storage readiness
- **THEN** it reads the shared semantic registry and selected skills' binding pages, validates profile and label availability, and records binding status by semantic id
- **AND** unavailable support becomes an explicit blocker or deferred disposition rather than an invented path or command

