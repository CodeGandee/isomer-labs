## ADDED Requirements

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
The Topic Workspace Manifest SHALL bind stable semantic surface labels to concrete paths or path templates.

#### Scenario: Topic-scoped surface binding is declared
- **WHEN** the manifest declares a topic-scoped surface such as `topic.main_repo`, `topic.records.artifacts`, or `topic.runtime.db`
- **THEN** the binding includes a project- or topic-relative path, owner classification, durability classification, sharing classification, and status

#### Scenario: Agent-scoped surface binding is declared
- **WHEN** the manifest declares an agent-scoped surface such as `agent.workspace`, `agent.private_artifacts`, or `agent.scratch`
- **THEN** the binding uses a path template that can be resolved with an Effective Agent Context
- **AND** validation rejects the binding when the template cannot be resolved for a concrete Agent Name

#### Scenario: Agent workspace template syntax is bounded
- **WHEN** the manifest binds `agent.workspace` with a template intended for cwd-derived agent inference
- **THEN** the template uses one `{agent_name}` path segment placeholder and no arbitrary expression language

#### Scenario: Semantic labels are unique
- **WHEN** the manifest declares two active bindings for the same semantic label and scope
- **THEN** validation reports a duplicate binding diagnostic instead of choosing one silently

#### Scenario: Optional labels may be absent
- **WHEN** a command does not require an optional semantic label and the manifest does not bind it
- **THEN** validation does not require that surface to exist

#### Scenario: Required labels are command scoped
- **WHEN** a command requires a semantic label to run
- **THEN** validation reports a missing binding only for the required label and command scope

### Requirement: Built-in Default Layout Profile
The system SHALL provide an `isomer-default.v1` layout profile that maps standard semantic labels to the current default Topic Workspace and Agent Workspace paths.

#### Scenario: Default topic labels are available
- **WHEN** a Topic Workspace uses the default layout profile
- **THEN** the system can resolve `topic.workspace`, `topic.runtime.db`, `topic.runtime`, `topic.records`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, `topic.records.logs`, `topic.team_profile_bundle`, `topic.main_repo`, `topic.main_repo.isomer_managed`, and `topic.agents_root`

#### Scenario: Default agent labels are available
- **WHEN** an Effective Agent Context supplies Agent Name `alice` under the default layout profile
- **THEN** the system can resolve `agent.workspace` to `<topic-workspace>/agents/alice` and can resolve standard agent-owned support labels such as `agent.isomer_managed`, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, and `agent.links` under that Agent Workspace

#### Scenario: Default materialization is explicit
- **WHEN** a user asks to create the default semantic directories for a Topic Workspace
- **THEN** the system writes or updates the Topic Workspace Manifest and creates only the selected default-layout surfaces it owns

#### Scenario: Standard default materialization is topic-scoped
- **WHEN** a user runs default materialization without selecting individual labels or an Agent Name
- **THEN** the system materializes the standard topic-owned default labels needed for Topic Workspace readiness and does not create per-agent directories

#### Scenario: Agent default materialization needs agent context
- **WHEN** a user asks default materialization to create `agent.*` labels
- **THEN** the command requires an explicit Agent Name or Agent Instance selector before creating agent-scoped paths

#### Scenario: Read-only queries do not materialize
- **WHEN** a user lists, previews, or resolves semantic labels without a materialization command
- **THEN** the system does not create the Topic Workspace Manifest, directories, Workspace Runtime records, Agent Workspaces, or Git worktrees

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
Each semantic surface binding SHALL declare enough classification for commands and validation to preserve ownership, durability, and sharing semantics when paths differ from the default layout.

#### Scenario: Private agent surface is not shared
- **WHEN** the manifest binds `agent.private_artifacts`, `agent.scratch`, `agent.runtime`, or another agent-private label
- **THEN** the binding classification marks the surface as agent-owned and not a peer write surface

#### Scenario: Public share is explicitly classified
- **WHEN** the manifest binds `agent.public_share`
- **THEN** the binding classification marks the surface as agent-owned material that Peer Read Access may expose according to Workspace Boundary policy

#### Scenario: Durable records are topic-owned
- **WHEN** the manifest binds `topic.records.artifacts`, `topic.records.runs`, `topic.records.tasks`, or related record labels
- **THEN** the binding classification marks the surface as topic-owned durable material

#### Scenario: Git-backed surfaces keep repository semantics
- **WHEN** the manifest binds `topic.main_repo` or `agent.workspace` to Git-backed paths
- **THEN** the binding classification records the expected repository or worktree semantics without treating Git state as Workspace Runtime state

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
