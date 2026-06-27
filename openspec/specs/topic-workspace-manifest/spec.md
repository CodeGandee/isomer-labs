# topic-workspace-manifest Specification

## Purpose
TBD - created by archiving change add-topic-workspace-manifest-path-resolution. Update Purpose after archive.
## Requirements
### Requirement: Topic Workspace Manifest Discovery
The system SHALL support a topic-owned Topic Workspace Manifest that declares semantic surface bindings for one Topic Workspace.

#### Scenario: Manifest lives inside the selected Topic Workspace
- **WHEN** a command resolves a Project Manifest-backed Topic Workspace
- **THEN** the system looks for the Topic Workspace Manifest at `<topic-workspace>/topic-workspace.toml`
- **AND** the system treats the manifest as topic-owned configuration, not as Project Config Directory state

#### Scenario: Project Manifest does not override topic manifest path
- **WHEN** the Project Manifest registers a Topic Workspace
- **THEN** the system derives the Topic Workspace Manifest path from that Topic Workspace path and does not read a per-topic manifest path override

#### Scenario: Missing manifest uses built-in default profile
- **WHEN** the Topic Workspace Manifest is missing and a command only needs resolvable default layout paths
- **THEN** the system synthesizes effective bindings from the built-in `isomer-default.v1` layout profile without creating files

#### Scenario: Manifest identity matches selected topic
- **WHEN** a Topic Workspace Manifest contains `research_topic_id` or `topic_workspace_id`
- **THEN** validation requires those ids to match the selected Project Manifest registration

#### Scenario: Manifest does not register a Topic Workspace
- **WHEN** a directory contains `topic-workspace.toml` but the Project Manifest does not register that directory as a Topic Workspace
- **THEN** the system does not treat the directory as an Isomer-managed Topic Workspace

### Requirement: Semantic Surface Binding Schema
The Topic Workspace Manifest SHALL bind stable semantic surface labels to concrete paths or path templates, including disposable local tmp labels.

#### Scenario: Topic tmp surface binding is declared
- **WHEN** the manifest declares topic-scoped disposable surfaces such as `topic.tmp` or `topic.repos.main.tmp`
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
- **AND** it can resolve `topic.repos.main.tmp` to `<topic-workspace>/repos/topic-main/tmp/`

#### Scenario: Default agent tmp label is available
- **WHEN** an Effective Agent Context supplies Agent Name `alice` under the default layout profile
- **THEN** the system can resolve `agent.tmp` to `<topic-workspace>/agents/alice/tmp/`

#### Scenario: Standard default materialization includes only selected tmp labels
- **WHEN** a user asks to materialize default semantic directories
- **THEN** the system creates tmp directories only when the selected label set or setup workflow owns those labels
- **AND** read-only queries still do not create tmp directories

### Requirement: Semantic Binding Path Validation
The system SHALL validate manifest-backed paths against Project, Topic Workspace, Agent Workspace, and Project Config Directory boundaries before using them.

#### Scenario: Topic surface stays project scoped
- **WHEN** a topic-scoped semantic binding resolves to a path outside the Project root
- **THEN** validation rejects the binding unless a later accepted external-root policy explicitly permits it

#### Scenario: Topic surface avoids Project Config Directory
- **WHEN** a semantic binding resolves inside `.isomer-labs/`
- **THEN** validation rejects the binding because Topic Workspace body material must not live inside the Project Config Directory

#### Scenario: Agent surface stays in selected Topic Workspace
- **WHEN** an agent-scoped semantic binding resolves outside the selected Topic Workspace
- **THEN** validation rejects the binding unless a later accepted external-root policy explicitly permits that surface

#### Scenario: Cross-topic binding is rejected
- **WHEN** a semantic binding points into another registered Research Topic's Topic Workspace
- **THEN** validation reports cross-topic leakage and rejects the binding for dependent commands

#### Scenario: Existing user directories are preserved
- **WHEN** a semantic binding points to an existing project-local directory that is otherwise safe
- **THEN** validation may accept the binding without moving, deleting, renaming, or reinitializing that directory

### Requirement: Semantic Surface Classification
Each semantic surface binding SHALL declare enough classification for commands and validation to preserve ownership, durability, sharing, and disposable semantics when paths differ from the default layout.

#### Scenario: Tmp surfaces are disposable and non-shared
- **WHEN** the manifest or default profile binds `topic.tmp`, `topic.repos.main.tmp`, or `agent.tmp`
- **THEN** the binding classification marks the surface as disposable
- **AND** it marks the surface as local/private rather than shared, peer-readable, topic-owned projection, or durable record material

#### Scenario: Tmp classification blocks durable dependency reuse
- **WHEN** a downstream workflow attempts to use a tmp-labeled path as durable state, profile material, evidence, handoff material, or Provenance Record input
- **THEN** validation can use the surface classification to report the dependency as invalid until the material is promoted

### Requirement: Manifest Validation Output
The system SHALL report deterministic diagnostics for Topic Workspace Manifest issues without silently repairing user-authored bindings.

#### Scenario: Invalid manifest is diagnostic
- **WHEN** the Topic Workspace Manifest is malformed, has an unsupported schema version, or contains invalid semantic bindings
- **THEN** validation reports diagnostics with the manifest path, semantic label when known, severity, and blocker status for dependent commands

#### Scenario: Validation does not repair paths
- **WHEN** validation finds a missing directory, unsafe path, duplicate label, or drifted binding
- **THEN** validation does not create, delete, move, or rewrite files unless the user invokes an explicit materialization or repair command

#### Scenario: Effective bindings are explainable
- **WHEN** a command resolves a semantic label from the manifest or default profile
- **THEN** the response includes the semantic label, resolved path, source, and source detail needed to explain the result

