## ADDED Requirements

### Requirement: Topic Workspace Summary Semantic Path Label
Workspace Path Resolution SHALL expose `topic.workspace.summary` as the built-in topic-scoped semantic label for the durable Topic Workspace readiness summary.

#### Scenario: Summary label appears in catalog
- **WHEN** a command queries the effective semantic surface catalog for a Topic Workspace
- **THEN** the catalog includes `topic.workspace.summary`
- **AND** the entry reports `storage_profile = "topic_workspace_summary_file"`, path kind `file`, topic scope, owner, durability, source, source detail, and diagnostics when available

#### Scenario: Default layout resolves summary label
- **WHEN** a Topic Workspace uses the built-in `isomer-default.v1` layout profile and no higher-precedence binding overrides the summary label
- **THEN** Workspace Path Resolution resolves `topic.workspace.summary` to `<topic-workspace>/isomer-topic-workspace-summary.md`

#### Scenario: Summary materialization prepares parent only
- **WHEN** a workflow materializes `topic.workspace.summary`
- **THEN** materialization creates or validates the parent directory for the resolved file path according to `topic_workspace_summary_file`
- **AND** it leaves summary file content to the workflow that owns the content write

#### Scenario: Skills query summary label before file access
- **WHEN** Topic Creator needs to read, write, validate, report, or refresh the Topic Workspace readiness summary
- **THEN** it resolves `topic.workspace.summary` through Workspace Path Resolution before touching a filesystem path
- **AND** it reports the semantic label and resolved path in outputs that mention the summary

#### Scenario: Summary label diagnostics block guessed paths
- **WHEN** Workspace Path Resolution cannot resolve `topic.workspace.summary` for the selected Topic Workspace
- **THEN** dependent skills report the resolver diagnostic instead of guessing a root-level summary file path

## MODIFIED Requirements

### Requirement: Effective Semantic Surface Catalog
Workspace Path Resolution SHALL resolve paths from an effective semantic surface catalog composed of built-in reserved labels, accepted grouped reserved labels, and valid manifest-declared `custom.*` labels.

#### Scenario: Built-in labels remain available
- **WHEN** a caller lists semantic paths for a selected Topic Workspace
- **THEN** the output includes built-in labels such as `topic.repos.main`, `topic.records.artifacts`, `topic.runtime.db`, `topic.workspace.summary`, `agent.workspace`, `agent.private_artifacts`, and `agent.tmp` with `storage_profile` id and storage-profile-derived traits

#### Scenario: Grouped topic repository labels are available
- **WHEN** the effective catalog contains accepted repository labels such as `topic.repos.main` or `topic.repos.inner_group.some_repo_name`
- **THEN** Workspace Path Resolution can resolve each label with source, `storage_profile` id, storage-profile-derived traits, and diagnostics

#### Scenario: Manifest custom labels are available
- **WHEN** the Topic Workspace Manifest declares a valid custom label under `custom.*`
- **THEN** Workspace Path Resolution includes that label in the effective catalog and can resolve it with source, `storage_profile` id, storage-profile-derived traits, and diagnostics

#### Scenario: Undeclared custom label is rejected
- **WHEN** a caller requests a label that is neither built into Isomer nor declared as a valid custom label in the Topic Workspace Manifest
- **THEN** Workspace Path Resolution reports an unknown semantic label diagnostic
