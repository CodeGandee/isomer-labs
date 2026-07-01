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

### Requirement: Reserved and Custom Semantic Binding Schema
The Topic Workspace Manifest SHALL allow topic owners to bind accepted reserved semantic surface labels and declare custom semantic surface labels under `custom.*` using compact bindings with `label`, `path`, and `storage_profile`.

#### Scenario: Topic storage profile custom binding is accepted
- **WHEN** the manifest declares a label under `custom.*` with a path and an accepted topic-scoped `storage_profile`
- **THEN** manifest validation accepts the binding when its path resolves safely for the selected Topic Workspace

#### Scenario: Agent storage profile custom binding is accepted
- **WHEN** the manifest declares a label under `custom.*` with a path template and an accepted agent-scoped `storage_profile`
- **THEN** manifest validation accepts the binding when its resolved path stays within the selected Topic Workspace and passes agent-scoped safety checks

#### Scenario: Grouped topic repository binding is accepted
- **WHEN** the manifest declares a valid `topic.repos.*` label such as `topic.repos.main` or `topic.repos.inner_group.some_repo_name` with a path and repository `storage_profile`
- **THEN** manifest validation accepts the binding when its path resolves safely for the selected Topic Workspace and the label passes grouped repository syntax rules

#### Scenario: storage_profile is required
- **WHEN** a semantic binding omits `storage_profile` or names an unknown storage profile
- **THEN** manifest validation reports the binding as invalid before Workspace Path Resolution exposes it as usable

#### Scenario: Storage profile traits are not duplicated on bindings
- **WHEN** a semantic binding includes storage-profile-owned fields such as required context, owner, durability, sharing, path kind, lifecycle, visibility, safety policy, or Git semantics
- **THEN** manifest validation reports those fields as unsupported binding fields and requires the author to select the appropriate `storage_profile` instead

#### Scenario: Reserved label namespace is protected
- **WHEN** the manifest declares an unknown label outside `custom.*`, or declares an undeclared label under an Isomer-owned reserved root without a matching grouped-label rule
- **THEN** manifest validation reports an unknown or reserved semantic label diagnostic

### Requirement: Manifest Binding Path Templates
The Topic Workspace Manifest SHALL validate custom and built-in binding paths before they can become effective path bindings.

#### Scenario: Agent template uses whole-segment agent placeholder
- **WHEN** an agent-scoped binding template includes `{agent_name}`
- **THEN** validation requires `{agent_name}` to occupy exactly one whole path segment

#### Scenario: Custom binding avoids Project Config Directory
- **WHEN** a custom binding resolves inside `.isomer-labs/`
- **THEN** validation rejects the binding because Topic Workspace body material must not live inside the Project Config Directory

#### Scenario: Custom binding avoids another Topic Workspace
- **WHEN** a custom binding resolves inside another registered Topic Workspace
- **THEN** validation reports cross-topic leakage and rejects the binding for dependent commands

### Requirement: Manifest Materialization Preserves User Bindings
Default materialization SHALL add selected default bindings without deleting, rewriting, or reclassifying existing user-authored custom bindings.

#### Scenario: Materialize default leaves custom labels intact
- **WHEN** `project paths materialize-default` updates a Topic Workspace Manifest that already contains valid `custom.*` bindings
- **THEN** the command preserves those custom bindings and only adds or updates selected default-layout bindings it owns

#### Scenario: Invalid custom binding blocks dependent materialization
- **WHEN** the Topic Workspace Manifest contains an invalid custom binding and materialization would depend on the effective catalog
- **THEN** the command reports diagnostics and avoids partially rewriting the manifest as a silent repair

### Requirement: CLI-backed Binding Registration
The Topic Workspace Manifest SHALL be writable through validated `isomer-cli` path registration commands so users do not need to edit the manifest directly for normal binding creation.

#### Scenario: CLI registers a path binding
- **WHEN** a user runs a path registration command with label, path, and storage_profile
- **THEN** the command validates the same namespace, storage profile, duplicate binding, and path safety rules as manifest loading before writing a binding to the Topic Workspace Manifest

#### Scenario: CLI creates path while registering
- **WHEN** a user runs a path registration command with `--create`
- **THEN** the command creates the target path according to the selected storage profile and writes the manifest binding only if validation and creation succeed

#### Scenario: CLI rejects duplicate binding without replacement intent
- **WHEN** a path registration command targets a label that already has an active binding
- **THEN** the command reports the existing binding and refuses to replace it unless the user passes an explicit replacement option

#### Scenario: Repository create command registers grouped repository label
- **WHEN** a user runs a repository creation command for a non-main topic repository name
- **THEN** the command registers the corresponding `topic.repos.*` label with `storage_profile = "topic_repo"` and creates the repository path through the same validated path registration flow
- **AND** when no explicit path is supplied, the command uses `repos/extern/<repo-label-path>` as the default target path

#### Scenario: Repository create command protects Topic Main Repository
- **WHEN** a user runs a repository creation command for `main` or `topic.repos.main` without an explicit path
- **THEN** the command reports that `topic.repos.main` is a built-in label and does not create a conflicting `repos/main` repository target
- **AND** it directs the user to materialize or override `topic.repos.main` through semantic path commands

### Requirement: CLI-backed Binding Lifecycle
The Topic Workspace Manifest SHALL support validated binding lifecycle operations while preserving Isomer-owned semantic label definitions and user filesystem content.

#### Scenario: CLI updates an existing binding
- **WHEN** a user updates an existing manifest binding with a new path or accepted replacement `storage_profile`
- **THEN** the command validates the new binding with the same namespace, storage profile, duplicate binding, and path safety rules before rewriting that binding record

#### Scenario: Binding update does not move files
- **WHEN** a user updates a binding path
- **THEN** the command does not move files from the previous target and reports that historical Path Plans still refer to their recorded paths

#### Scenario: Custom label unregister removes label from effective catalog
- **WHEN** a user unregisters a `custom.*` label
- **THEN** the command removes the manifest binding and the label is no longer present in the effective catalog unless the user registers it again

#### Scenario: Grouped repository unregister removes dynamic label slot
- **WHEN** a user unregisters a manifest-defined grouped repository label such as `topic.repos.inner_group.some_repo_name`
- **THEN** the command removes that concrete label slot from the effective catalog without deleting the repository path

#### Scenario: Built-in label reset removes override only
- **WHEN** a user resets a built-in reserved label that has a manifest override
- **THEN** the command removes the manifest override while preserving the built-in label definition and allowing remaining precedence sources such as environment overrides or default-layout bindings to apply

#### Scenario: Built-in label definition cannot be deleted
- **WHEN** a user attempts to unregister or delete a built-in reserved label definition
- **THEN** the command rejects the request and directs the user to reset a user-authored override when one exists

#### Scenario: Binding deletion leaves filesystem targets untouched
- **WHEN** a user unregisters or resets a binding
- **THEN** the command does not delete directories, repositories, files, runtime databases, or other storage targets that the binding previously resolved to

### Requirement: Intent Storage Profiles and Default Bindings
The Topic Workspace Manifest and built-in default layout profile SHALL support reserved topic intent and env target-spec semantic labels through accepted storage profiles.

#### Scenario: Default profile declares intent storage profiles
- **WHEN** the built-in `isomer-default.v1` layout profile is used for a Topic Workspace
- **THEN** `topic.intent.overview`, `topic.intent.topic_env_requirements`, and `topic.intent.agent_env_requirements` use the `topic_intent_source_file` storage profile
- **AND** `topic.env.topic_setup_target_spec` and `topic.env.agent_setup_target_spec` use the `topic_env_target_spec_file` storage profile

#### Scenario: Source intent storage profile is user-editable
- **WHEN** a binding uses the `topic_intent_source_file` storage profile
- **THEN** validation treats the surface as topic-scoped, durable, user-editable, Markdown-compatible, file-kind material
- **AND** validation does not classify the surface as runtime-internal, cache-like, disposable, or service-only output

#### Scenario: Target spec storage profile is service-owned but reviewable
- **WHEN** a binding uses the `topic_env_target_spec_file` storage profile
- **THEN** validation treats the surface as topic-scoped, durable, reviewable, Markdown-compatible, file-kind material used as a setup service target spec
- **AND** validation does not classify the surface as user source intent, runtime-internal state, cache-like material, or a disposable execution log

### Requirement: Intent Semantic Binding Overrides
The Topic Workspace Manifest SHALL allow safe overrides of accepted reserved intent and target-spec labels without allowing skills to bypass semantic path resolution.

#### Scenario: Manifest override for intent label is accepted
- **WHEN** a Topic Workspace Manifest declares `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.agent_env_requirements`, `topic.env.topic_setup_target_spec`, or `topic.env.agent_setup_target_spec` with a path and the expected storage profile
- **THEN** manifest validation accepts the binding when the resolved path is safe for the selected Topic Workspace and matches the label scope and path kind

#### Scenario: Wrong storage profile is rejected
- **WHEN** a manifest binding for a reserved intent or target-spec label uses an unknown storage profile or a storage profile that does not match the label
- **THEN** manifest validation reports the binding as invalid before Workspace Path Resolution exposes it as usable

#### Scenario: Unsafe intent override is rejected
- **WHEN** a manifest binding for an intent or target-spec label resolves outside the Project root, inside `.isomer-labs/`, into another registered Topic Workspace, or into an Agent Workspace-private surface
- **THEN** manifest validation rejects the binding for dependent commands

#### Scenario: CLI registration can bind intent labels
- **WHEN** a user runs a supported path registration command for one of the reserved intent or target-spec labels with a path and expected storage profile
- **THEN** the command validates the same namespace, storage profile, duplicate binding, and path safety rules as manifest loading before writing the binding

### Requirement: Topic Main Projection Semantic Labels
The Topic Workspace Manifest and built-in default layout profile SHALL support fixed semantic labels for Topic Main Development Repository projection roots and projection metadata.

#### Scenario: Default projection labels exist
- **WHEN** a Topic Workspace uses the built-in `isomer-default.v1` layout profile
- **THEN** `topic.repos.main.projections.readonly` resolves to `<resolved topic.repos.main>/isomer-managed/topic-owned/readonly/extern/`
- **AND** `topic.repos.main.projections.writable` resolves to `<resolved topic.repos.main>/isomer-managed/topic-owned/writable/extern/`
- **AND** `topic.repos.main.projections.manifest` resolves to `<resolved topic.repos.main>/isomer-managed/tracked/manifests/extern-projections.toml`

#### Scenario: Projection label storage profiles are explicit
- **WHEN** the built-in catalog declares Topic Main projection labels
- **THEN** read-only and writable projection roots use accepted topic-repo-local projection directory storage profiles
- **AND** the projection manifest uses an accepted topic-repo-local tracked file storage profile

#### Scenario: Projection labels follow custom main repo binding
- **WHEN** a Topic Workspace Manifest safely overrides `topic.repos.main`
- **THEN** the default projection label paths are derived under the resolved custom `topic.repos.main` path
- **AND** the system does not fall back to `<topic-workspace>/repos/topic-main` for those projection labels

### Requirement: Projection Namespace Is Reserved
The Topic Workspace Manifest SHALL reserve Topic Main Development Repository projection labels as built-in labels instead of treating them as dynamic grouped topic repository labels.

#### Scenario: Projection labels are not external repo sources
- **WHEN** a command resolves `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, or `topic.repos.main.projections.manifest`
- **THEN** it treats the label as a built-in Topic Main support surface
- **AND** it does not treat the label as a canonical `topic.repos.*` external repository

#### Scenario: Unknown main sublabels are rejected
- **WHEN** a manifest declares an unknown label under `topic.repos.main.*`
- **THEN** validation reports an unknown or reserved semantic label diagnostic
- **AND** it does not accept the label through the grouped `topic.repos.*` dynamic repository rule

### Requirement: Breaking Manifest Compatibility
The Topic Workspace Manifest implementation SHALL not preserve old generated layout internals after this breaking layout revision.

#### Scenario: Old generated bindings are invalid
- **WHEN** old generated Topic Workspace bindings point to deprecated source gate paths, deprecated topic-main support paths, or deprecated projection paths
- **THEN** validation may reject those bindings without offering an automatic migration path

#### Scenario: Recreated content uses new defaults
- **WHEN** a Project recreates generated `isomer-content/` material after this change
- **THEN** the default profile uses the revised Topic Main Development Repository and projection labels

### Requirement: Topic Actor Binding Schema
The Topic Workspace Manifest SHALL support Topic Actor bindings for human-orchestrated topic-local workers.

#### Scenario: Topic Actor binding is parsed
- **WHEN** `topic-workspace.toml` contains a Topic Actor binding
- **THEN** manifest loading exposes the actor's topic-local name, actor kind, runtime kind, role kind, controller, default cwd label, optional workspace label, optional workspace path, optional branch, optional adapter ref, status, and source detail

#### Scenario: Topic Actor name is path safe
- **WHEN** validation checks a Topic Actor binding
- **THEN** it requires `topic_actor_name` to be path-safe and unique among active Topic Actor bindings in the selected Topic Workspace

#### Scenario: Topic Actor enum fields are bounded and extensible
- **WHEN** validation checks `actor_kind`, `runtime_kind`, `role_kind`, `controller_kind`, or `status`
- **THEN** it accepts defined core values and values under `custom.*`
- **AND** it rejects unknown non-extension values with a deterministic diagnostic

#### Scenario: Topic Actor binding does not imply Agent Instance
- **WHEN** a Topic Actor binding omits Agent Instance or Agent Team Instance refs
- **THEN** manifest validation accepts the binding when its actor fields and workspace fields are otherwise valid

#### Scenario: Manifest remains actor topology authority
- **WHEN** Workspace Runtime contains mutation or provenance audit records for Topic Actor registration or materialization
- **THEN** path resolution still uses the Topic Workspace Manifest Topic Actor binding as the authoritative actor topology source

### Requirement: Actor-Scoped Semantic Labels
The Topic Workspace Manifest and default layout profile SHALL support actor-scoped semantic labels for Topic Actor Workspaces.

#### Scenario: Default Topic Actor Workspace label resolves under actors root
- **WHEN** a Topic Actor named `claude-scout` uses the default layout profile
- **THEN** `topic.actors.workspace` resolves to `<topic-workspace>/actors/claude-scout`
- **AND** the Topic Actor Workspace is separate from `topic.repos.main` and from formal `agent.workspace` paths

#### Scenario: Actor support labels resolve under Topic Actor Workspace
- **WHEN** actor-scoped support labels are resolved for a Topic Actor
- **THEN** labels such as `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` resolve under that Topic Actor Workspace according to the selected layout profile

#### Scenario: Actor label requires actor context
- **WHEN** a command resolves `topic.actors.workspace` or another actor-scoped label without a Topic Actor selector, environment actor context, cwd-derived actor context, or lifecycle actor ref
- **THEN** path resolution reports that a Topic Actor context is required

### Requirement: Topic Actor Workspace Metadata
The Topic Workspace Manifest SHALL record enough Topic Actor Workspace metadata for reproducible worktree setup.

#### Scenario: Actor branch namespace is recorded
- **WHEN** a Topic Actor binding requests a worktree-backed Topic Actor Workspace
- **THEN** the binding or derived plan records a branch under `per-topic-actor/<topic-actor-name>/`

#### Scenario: Actor workspace source is topic-main
- **WHEN** a Topic Actor Workspace worktree is prepared
- **THEN** the source repository is the resolved `topic.repos.main` repository and the actor binding does not redefine `topic.repos.main`

