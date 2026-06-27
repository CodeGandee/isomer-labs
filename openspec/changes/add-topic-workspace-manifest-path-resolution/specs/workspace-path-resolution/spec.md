## ADDED Requirements

### Requirement: Semantic Path Resolution
Workspace Path Resolution SHALL resolve public semantic surface labels to concrete paths for the selected Effective Topic Context.

#### Scenario: Semantic label resolves to path
- **WHEN** a caller requests a semantic label such as `topic.main_repo`, `topic.records.artifacts`, `agent.workspace`, or `agent.private_artifacts`
- **THEN** the resolver returns the resolved path, semantic label, source, source detail, and diagnostics

#### Scenario: Unknown label is rejected
- **WHEN** a caller requests a semantic label that is not in the built-in catalog and not accepted by the Topic Workspace Manifest
- **THEN** the resolver reports an unknown semantic label diagnostic

#### Scenario: Agent label requires agent context
- **WHEN** a caller requests an agent-scoped semantic label without explicit, environment-derived, cwd-derived, or recorded Effective Agent Context
- **THEN** path resolution fails with a diagnostic that says the label requires an Agent Name or Agent Instance selector

#### Scenario: Topic label does not require agent context
- **WHEN** a caller requests a topic-scoped semantic label
- **THEN** the resolver does not require Agent Name or Agent Instance context

### Requirement: Semantic Resolution Precedence
Workspace Path Resolution SHALL apply deterministic precedence when resolving semantic labels.

#### Scenario: Recorded path plan wins
- **WHEN** a durable runtime record already has a PathPlanRecord for the requested semantic label and scope
- **THEN** the resolver uses the stored path plan before checking environment overrides, the Topic Workspace Manifest, Project Manifest defaults, or built-in defaults

#### Scenario: Environment context overrides manifest binding
- **WHEN** no applicable recorded path plan exists and a supported `ISOMER_*` environment override applies to the requested semantic label
- **THEN** the resolver uses the environment override before checking the Topic Workspace Manifest

#### Scenario: Topic Workspace Manifest overrides default profile
- **WHEN** no recorded path plan or supported environment override applies and the Topic Workspace Manifest binds the requested semantic label
- **THEN** the resolver uses the manifest binding before checking built-in default layout profile bindings

#### Scenario: Default profile is fallback
- **WHEN** no recorded path plan, supported environment override, or Topic Workspace Manifest binding applies
- **THEN** the resolver uses the built-in `isomer-default.v1` binding when the requested label is part of that profile

#### Scenario: Source is reported consistently
- **WHEN** a semantic label resolves
- **THEN** the result reports whether the selected path came from `path_plan`, `env`, `topic_workspace_manifest`, `project_manifest`, or `default_profile`

### Requirement: Semantic Path Query CLI
The CLI SHALL expose direct read-only semantic path query behavior in addition to broad path previews.

#### Scenario: Single semantic label is queried
- **WHEN** a user runs `isomer-cli project paths get <semantic-label>` for a selected Topic Workspace
- **THEN** the command returns one resolved semantic path result or diagnostics without creating files

#### Scenario: Resolve is not a second public command
- **WHEN** a user needs one semantic path answer
- **THEN** the documented public command is `isomer-cli project paths get <semantic-label>` rather than a parallel `project paths resolve` command

#### Scenario: Semantic labels are listed
- **WHEN** a user runs `isomer-cli project paths list` for a selected Topic Workspace
- **THEN** the command lists known semantic labels, scope, required context, resolved status, and source when available

#### Scenario: Preview remains read-only
- **WHEN** a user runs `isomer-cli project paths preview`
- **THEN** the command may include semantic labels and compatibility surface ids but still does not create files, directories, manifests, or Workspace Runtime records

#### Scenario: Explicit materialization command is separate
- **WHEN** a user wants to create default semantic directories
- **THEN** the user must run an explicit materialization command rather than relying on `paths get`, `paths list`, or `paths preview`

### Requirement: Compatibility Surface Mapping
Workspace Path Resolution SHALL preserve compatibility for existing internal path surface ids while presenting semantic labels as the public contract.

#### Scenario: Existing surface id remains accepted
- **WHEN** existing code requests a compatibility surface such as `topic_main_repo`, `records_artifacts`, or `agent_workspace:<agent-name>`
- **THEN** the resolver maps that surface to the corresponding semantic label when possible and preserves existing behavior

#### Scenario: Semantic label appears in new output
- **WHEN** new CLI or API output reports a resolved path
- **THEN** the output includes the semantic label even when an internal compatibility surface id was used to locate an existing path plan

#### Scenario: Compatibility aliases do not create new semantics
- **WHEN** a compatibility surface and a semantic label map to the same path class
- **THEN** validation treats them as aliases for one semantic surface rather than two independent durability contracts

### Requirement: Manifest-backed Path Safety
Workspace Path Resolution SHALL apply the same canonicalization and safety checks to manifest-backed semantic paths as it applies to default and environment-derived paths.

#### Scenario: Manifest path is canonicalized
- **WHEN** a path is selected from the Topic Workspace Manifest
- **THEN** the resolver canonicalizes the path before returning it

#### Scenario: Unsafe manifest path is rejected
- **WHEN** a manifest-backed semantic path points outside the Project root, inside `.isomer-labs/`, or into another Topic Workspace without an accepted policy
- **THEN** the resolver reports a validation diagnostic and does not return the path as usable for dependent work

#### Scenario: External roots are deferred
- **WHEN** a manifest-backed semantic path points outside the Project root
- **THEN** the resolver rejects it until a later accepted external-root policy explicitly permits that surface

#### Scenario: Missing path can still be previewed
- **WHEN** a safe manifest-backed path does not yet exist on disk
- **THEN** read-only path query output may report the planned path and missing status without creating it
