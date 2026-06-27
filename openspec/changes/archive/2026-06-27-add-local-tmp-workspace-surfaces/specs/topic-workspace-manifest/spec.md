## MODIFIED Requirements

### Requirement: Semantic Surface Binding Schema
The Topic Workspace Manifest SHALL bind stable semantic surface labels to concrete paths or path templates, including disposable local tmp labels.

#### Scenario: Topic tmp surface binding is declared
- **WHEN** the manifest declares topic-scoped disposable surfaces such as `topic.tmp` or `topic.main_repo.tmp`
- **THEN** each binding includes a project- or topic-relative path, owner classification, disposable durability classification, private or local sharing classification, and status

#### Scenario: Agent tmp surface binding is declared
- **WHEN** the manifest declares the agent-scoped disposable surface `agent.tmp`
- **THEN** the binding uses a path template that can be resolved with an Effective Agent Context
- **AND** validation rejects the binding when the template cannot be resolved for a concrete Agent Name

### Requirement: Built-in Default Layout Profile
The system SHALL provide an `isomer-default.v1` layout profile that maps standard semantic labels, including local tmp labels, to the current default Topic Workspace and Agent Workspace paths.

#### Scenario: Default topic tmp labels are available
- **WHEN** a Topic Workspace uses the default layout profile
- **THEN** the system can resolve `topic.tmp` to `<topic-workspace>/tmp/`
- **AND** it can resolve `topic.main_repo.tmp` to `<topic-workspace>/repos/topic-main/tmp/`

#### Scenario: Default agent tmp label is available
- **WHEN** an Effective Agent Context supplies Agent Name `alice` under the default layout profile
- **THEN** the system can resolve `agent.tmp` to `<topic-workspace>/agents/alice/tmp/`

#### Scenario: Standard default materialization includes only selected tmp labels
- **WHEN** a user asks to materialize default semantic directories
- **THEN** the system creates tmp directories only when the selected label set or setup workflow owns those labels
- **AND** read-only queries still do not create tmp directories

### Requirement: Semantic Surface Classification
Each semantic surface binding SHALL declare enough classification for commands and validation to preserve ownership, durability, sharing, and disposable semantics when paths differ from the default layout.

#### Scenario: Tmp surfaces are disposable and non-shared
- **WHEN** the manifest or default profile binds `topic.tmp`, `topic.main_repo.tmp`, or `agent.tmp`
- **THEN** the binding classification marks the surface as disposable
- **AND** it marks the surface as local/private rather than shared, peer-readable, topic-owned projection, or durable record material

#### Scenario: Tmp classification blocks durable dependency reuse
- **WHEN** a downstream workflow attempts to use a tmp-labeled path as durable state, profile material, evidence, handoff material, or Provenance Record input
- **THEN** validation can use the surface classification to report the dependency as invalid until the material is promoted
