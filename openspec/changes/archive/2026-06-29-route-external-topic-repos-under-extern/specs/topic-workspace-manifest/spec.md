## MODIFIED Requirements

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
