## ADDED Requirements

### Requirement: Manifest-sourced Runtime Path Plans
Workspace Runtime SHALL persist selected semantic path resolutions before durable runtime records depend on manifest-backed paths.

#### Scenario: Runtime init records semantic path sources
- **WHEN** Workspace Runtime initialization creates path plans for the selected Topic Workspace
- **THEN** each new semantic path plan records `semantic_label`, `scope_ref`, canonical path, source, source detail, and any compatibility surface id used by Workspace Path Resolution

#### Scenario: Manifest source is preserved
- **WHEN** a path plan is selected from the Topic Workspace Manifest
- **THEN** the stored path plan identifies the source as Topic Workspace Manifest-backed, records the semantic label in `semantic_label`, records the selected topic or agent scope in `scope_ref`, and records the manifest path in source detail

#### Scenario: Default profile source is preserved
- **WHEN** a path plan is selected from the built-in `isomer-default.v1` layout profile
- **THEN** the stored path plan identifies the source as default-profile-backed rather than pretending it came from an authored manifest

#### Scenario: Semantic identity is not encoded only in source detail
- **WHEN** a new path plan is created from a semantic label
- **THEN** validation and inspection can read the semantic label and scope from first-class fields without parsing source detail

#### Scenario: Existing path plan precedence is preserved
- **WHEN** a runtime record already references a stored path plan
- **THEN** later path resolution for that record uses the stored path plan before current manifest or default-profile bindings

### Requirement: Runtime Initialization Uses Semantic Surfaces
Workspace Runtime initialization SHALL create only the runtime-owned directories required by semantic resolution for the selected Topic Workspace.

#### Scenario: Runtime directories come from semantic labels
- **WHEN** runtime initialization needs Workspace Runtime database, records, runtime support, repository root, or Agent Workspace root paths
- **THEN** it resolves those paths through semantic labels before creating owned directories or path plans

#### Scenario: Minimal runtime initialization label set is command scoped
- **WHEN** runtime initialization runs without repository setup, profile materialization, or Agent Team Instance creation
- **THEN** it requires only `topic.runtime.db`, `topic.runtime`, `topic.records`, and the specific `topic.records.*` labels for record classes it initializes
- **AND** it does not require `topic.main_repo`, `topic.team_profile_bundle`, `topic.agents_root`, or `agent.workspace` unless the selected command path creates or depends on those surfaces

#### Scenario: Optional unused surfaces are not created
- **WHEN** the Topic Workspace Manifest omits optional semantic labels that runtime initialization does not need
- **THEN** runtime initialization does not create those optional directories merely because they exist in the default layout profile

#### Scenario: Unsafe manifest binding blocks mutation
- **WHEN** a required semantic label resolves to an unsafe path
- **THEN** runtime initialization reports a blocker and does not create Workspace Runtime records or directories that depend on that path

#### Scenario: Missing manifest may still initialize default runtime
- **WHEN** the Topic Workspace Manifest is missing and default-layout semantic labels can satisfy runtime initialization
- **THEN** runtime initialization may use the built-in default profile and record default-profile path-plan sources

### Requirement: Agent Workspace Runtime Records Use Semantic Bindings
Agent Workspace runtime records SHALL use semantic `agent.workspace` resolution rather than hard-coded path assembly as the primary planning contract.

#### Scenario: Agent workspace path plan uses semantic label
- **WHEN** Agent Team Instance creation creates an Agent Workspace record for Agent Name `alice`
- **THEN** it resolves `agent.workspace` for `alice` before creating the Agent Workspace path plan and Agent Workspace record

#### Scenario: Agent support paths use semantic labels
- **WHEN** Agent Team Instance creation records support paths for the Agent Workspace
- **THEN** it resolves labels such as `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.public_share`, and `agent.links` when those surfaces are required

#### Scenario: Agent Instance id remains independent
- **WHEN** `agent.workspace` resolves from Agent Name `alice`
- **THEN** the created Agent Instance id remains globally unique and does not need to equal `alice`

#### Scenario: Missing required agent label blocks creation
- **WHEN** Agent Team Instance creation requires an agent-scoped label that cannot be resolved for the selected Agent Name
- **THEN** creation fails with a validation diagnostic before writing dependent runtime records

### Requirement: Manifest Drift Validation
Workspace Runtime validation SHALL report drift between stored path plans and current semantic resolution without rewriting historical runtime records.

#### Scenario: Manifest change differs from stored path plan
- **WHEN** a stored path plan for a semantic label points to a different path than the current Topic Workspace Manifest binding resolves
- **THEN** validation reports a path-plan drift diagnostic and preserves the stored path plan

#### Scenario: Missing current binding is diagnostic
- **WHEN** a stored path plan references a semantic label that no longer resolves from the current manifest or default profile
- **THEN** validation reports that the historical path plan remains but the current binding is missing

#### Scenario: Drift does not delete files
- **WHEN** validation detects semantic path drift
- **THEN** it does not move, delete, archive, or rewrite files or runtime rows automatically

#### Scenario: Rebinding needs explicit action
- **WHEN** an operator wants a durable record to depend on a new semantic binding
- **THEN** the system requires an explicit migration, repair, or new runtime action rather than silently rebinding existing records

### Requirement: Runtime Inspection Reports Semantic Paths
Runtime inspection SHALL expose semantic path metadata for stored path plans when available.

#### Scenario: Inspect includes semantic labels
- **WHEN** a user inspects Workspace Runtime path plans
- **THEN** the output includes semantic labels, compatibility surface ids when present, canonical paths, sources, source detail, and drift diagnostics when validation has computed them

#### Scenario: Compatibility-only plans remain readable
- **WHEN** an older path plan has only a compatibility surface id and no semantic label metadata
- **THEN** runtime inspection still reports the path plan and maps it to a semantic label when a known alias exists
