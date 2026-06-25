# research-topic-crud Specification

## Purpose
TBD - created by archiving change add-research-topic-crud-commands. Update Purpose after archive.
## Requirements
### Requirement: Research Topic CRUD Command Surface
The system SHALL expose authoritative Research Topic lifecycle operations under `isomer-cli project topics`.

#### Scenario: Topic command group lists CRUD operations
- **WHEN** a user runs `isomer-cli project topics --help`
- **THEN** the command help lists `list`, `show`, `create`, `update`, and `delete`

#### Scenario: Project init is not part of topic creation
- **WHEN** a user wants to create or register a Research Topic
- **THEN** the supported CLI surface is `isomer-cli project topics create`, not `isomer-cli project init`

### Requirement: Research Topic Creation
The system SHALL create Research Topic registrations, Research Topic Config files, and associated Topic Workspace registrations only through explicit topic creation commands.

#### Scenario: Create topic with default workspace
- **WHEN** a user runs `isomer-cli project topics create <topic-id> --statement "<research topic>"`
- **THEN** the system writes `.isomer-labs/research-topics/<topic-id>.toml`, registers `[[research_topics]]`, registers `[[topic_workspaces]]`, creates the Topic Workspace under the effective Topic Workspace base, and reports the created paths

#### Scenario: Create topic with custom workspace
- **WHEN** a user runs `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <dir>`
- **THEN** the system registers the Topic Workspace path as `<dir>` after validating that it resolves inside the Project root and outside Project Config, Houmao overlay, and unrelated registered Topic Workspace boundaries

#### Scenario: Create topic rejects missing statement
- **WHEN** a user runs `isomer-cli project topics create <topic-id>` without a statement
- **THEN** the system returns a deterministic diagnostic and does not create or modify Project files

#### Scenario: Create topic rejects placeholder statement
- **WHEN** a user supplies an empty, generic, or placeholder statement such as `default Research Topic`
- **THEN** the system returns a deterministic diagnostic and does not create or modify Project files

#### Scenario: Create topic rejects duplicate topic
- **WHEN** the Project Manifest already registers `<topic-id>` as a Research Topic or Topic Workspace id
- **THEN** the system refuses creation and does not overwrite the existing registration, config file, or workspace directory

#### Scenario: Create topic can set default
- **WHEN** a user runs `isomer-cli project topics create <topic-id> --statement "<research topic>" --set-default`
- **THEN** the system sets Project Manifest defaults for the Research Topic and Topic Workspace to `<topic-id>`

### Requirement: Research Topic Inspection
The system SHALL inspect registered Research Topics without requiring Effective Topic Context.

#### Scenario: List topics in empty project
- **WHEN** a user runs `isomer-cli project topics list` in a Project with no registered Research Topics
- **THEN** the command succeeds and reports an empty topic list

#### Scenario: Show registered topic
- **WHEN** a user runs `isomer-cli project topics show <topic-id>` for a registered Research Topic
- **THEN** the command reports the topic registration, Research Topic Config path, topic statement, associated Topic Workspace registration, effective workspace path, status, and diagnostics

#### Scenario: Show missing topic
- **WHEN** a user runs `isomer-cli project topics show <topic-id>` for a missing Research Topic
- **THEN** the command returns a deterministic diagnostic that the Research Topic is not registered

### Requirement: Research Topic Update
The system SHALL update bounded Research Topic metadata without renaming topic ids.

#### Scenario: Update topic statement
- **WHEN** a user runs `isomer-cli project topics update <topic-id> --statement "<research topic>"`
- **THEN** the system updates the Research Topic Config statement for `<topic-id>` and preserves the topic id, workspace id, and workspace path

#### Scenario: Update topic status
- **WHEN** a user runs `isomer-cli project topics update <topic-id> --status archived`
- **THEN** the system updates the Research Topic registration status and preserves existing files and workspace contents

#### Scenario: Update topic default
- **WHEN** a user runs `isomer-cli project topics update <topic-id> --set-default`
- **THEN** the system sets the Project Manifest default Research Topic and Topic Workspace to the selected registered topic and workspace

#### Scenario: Update refuses rename
- **WHEN** a user attempts to rename a Research Topic through `topics update`
- **THEN** the system returns a deterministic diagnostic explaining that topic rename is not supported by the first CRUD surface

### Requirement: Research Topic Deletion
The system SHALL make Research Topic deletion plan-first and preserve Topic Workspace contents unless explicitly instructed otherwise.

#### Scenario: Delete dry-run reports plan
- **WHEN** a user runs `isomer-cli project topics delete <topic-id> --dry-run`
- **THEN** the command reports the Research Topic registration, Topic Workspace registration, Research Topic Config, Project Manifest default updates, dependent registrations, blockers, and preserved workspace path without modifying files

#### Scenario: Delete requires confirmation
- **WHEN** a user runs `isomer-cli project topics delete <topic-id>` without `--dry-run` or `--yes`
- **THEN** the system returns a deterministic diagnostic and does not modify files

#### Scenario: Delete applies reviewed plan
- **WHEN** a user runs `isomer-cli project topics delete <topic-id> --yes` and no blockers remain
- **THEN** the system removes the Research Topic registration, removes the associated Topic Workspace registration, removes the Research Topic Config file, clears matching Project Manifest defaults, preserves the Topic Workspace directory, and reports the mutation

#### Scenario: Delete preserves workspace by default
- **WHEN** `topics delete <topic-id> --yes` applies without an explicit workspace removal option
- **THEN** the system preserves the Topic Workspace directory and reports it as an unmanaged preserved path

#### Scenario: Delete does not physically remove workspace
- **WHEN** `topics delete <topic-id> --yes` applies
- **THEN** the system does not delete the Topic Workspace directory and instead reports supported cleanup guidance for users who want filesystem removal

#### Scenario: Delete blocks dependent runtime or team material
- **WHEN** the selected topic has dependent Topic Agent Team Profiles, Agent Team Instance records, Workspace Runtime records, adapter material, or other registered topic-scoped material that would become dangling
- **THEN** the delete plan reports blockers and confirmed deletion refuses to apply until the user removes or preserves those dependencies through supported cleanup paths

### Requirement: Research Topic CRUD Mutation Boundaries
The system SHALL keep topic CRUD separate from runtime preparation, live agent operations, and unregistered filesystem inference.

#### Scenario: Topic CRUD does not create runtime state
- **WHEN** any `isomer-cli project topics` CRUD command completes
- **THEN** it does not create `state.sqlite`, Workspace Runtime records, Agent Workspaces, adapter launch material, Houmao managed agents, mailboxes, gateways, sessions, or launch dossiers

#### Scenario: Topic CRUD does not infer from directories
- **WHEN** directories exist under a Topic Workspace base such as `isomer-content/topic-ws/`
- **THEN** topic CRUD does not treat them as registered Research Topics unless the Project Manifest contains explicit registrations

