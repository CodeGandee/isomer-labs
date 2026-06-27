## ADDED Requirements

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
- **WHEN** a user runs a repository creation command for a topic repository name
- **THEN** the command registers the corresponding `topic.repos.*` label with `storage_profile = "topic_repo"` and creates the repository path through the same validated path registration flow

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
