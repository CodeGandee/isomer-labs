# external-repository-registration Specification

## Purpose
TBD - created by syncing completed OpenSpec changes.

## Requirements

### Requirement: Repository Acquisition Remains Outside Isomer APIs
The system SHALL leave source-repository command selection and execution to the acting user or agent outside `isomer-cli`, Isomer package services, and Execution Adapter Command Requests.

#### Scenario: User supplies an acquisition command
- **WHEN** the user supplies an exact `git`, provider-CLI, local-copy, wrapper, or multi-command acquisition procedure
- **THEN** the acting agent runs or asks the user to run that procedure through the available external command surface, subject to the user request, applicable Gates, resource limits, and owner boundaries
- **AND** Isomer does not translate the procedure into a fixed clone, fetch, checkout, or cleanup API

#### Scenario: Agent selects an acquisition procedure
- **WHEN** a repository is required and the user has not supplied exact commands
- **THEN** the acting agent selects commands suited to the requested source, revision, authentication posture, repository features, and available tools
- **AND** no Isomer API imposes a shallow clone, remote name, branch, history depth, provider, credential wrapper, staging layout, retry sequence, or cleanup policy

#### Scenario: Existing repository needs a later source operation
- **WHEN** an already registered repository requires fetch, pull, checkout, submodule, LFS, worktree, repair, or other source-control work
- **THEN** the acting user or agent performs that work outside Isomer APIs under the applicable authorization
- **AND** Isomer receives only the resulting registration, Artifact revision, Provenance Record, Run checkpoint, or blocker data

### Requirement: Unregistered Repository Targets Can Be Planned Without Mutation
Workspace Path Resolution SHALL return the `isomer-default.v1` candidate path for a valid unregistered non-main `topic.repos.<group...>.<repo-name>` label without creating a binding or filesystem content.

#### Scenario: Caller previews a default repository target
- **WHEN** a caller queries `project paths default topic.repos.<group...>.<repo-name>` before acquisition
- **THEN** the command returns `<topic-workspace>/repos/extern/<group...>/<repo-name>`, `storage_profile = "topic_repo"`, and `mutated: false`
- **AND** it does not create the target directory, update the Topic Workspace Manifest, or execute a repository command

#### Scenario: Caller chooses an explicit target
- **WHEN** the user or applicable workspace plan requires another safe Project-local path
- **THEN** the acting user or agent may acquire the repository at that explicit path and later register that same path
- **AND** the default-path query does not override the explicit post-acquisition registration

### Requirement: Existing External Repository Registration Is Non-Executing
The CLI SHALL provide `project repos register <repo-label> --path <existing-path>` to register an existing Canonical External Repository under a non-main `topic.repos.*` Semantic Workspace Surface Label without creating or changing repository content.

#### Scenario: Verified existing repository is registered
- **WHEN** the caller supplies a valid non-main repository label and a safe existing directory after external acquisition and verification succeed
- **THEN** the command normalizes a bare repository label to `topic.repos.<group...>.<repo-name>`, registers the canonical path with `storage_profile = "topic_repo"`, and returns the manifest ref, semantic label, canonical path, and `mutated: true`
- **AND** the command does not create directories or run `git`, a provider CLI, a copy tool, a credential wrapper, or another subprocess

#### Scenario: Target does not exist or is not a directory
- **WHEN** `project repos register` receives a missing path, a non-directory path, or a path rejected by Workspace Path Resolution safety rules
- **THEN** it returns a deterministic non-mutating diagnostic
- **AND** it does not add or replace a Topic Workspace Manifest binding

#### Scenario: Label already has another binding
- **WHEN** the requested semantic label is already bound to a different canonical path
- **THEN** registration fails with the existing and requested paths and the explicit binding-management route
- **AND** it does not overwrite the binding, merge repositories, move content, or delete either path

#### Scenario: Registration fails after acquisition
- **WHEN** external acquisition and verification succeeded but semantic registration fails
- **THEN** the acquired filesystem content remains untouched for diagnosis or an explicit retry
- **AND** the procedure reports registration as incomplete rather than claiming a registered Canonical External Repository

### Requirement: Registration Follows Source Verification
An acquisition workflow SHALL register a new Canonical External Repository only after the acting user or agent verifies the intended source relationship and observes the resulting repository identity with external commands or equivalent source-specific checks.

#### Scenario: Acquisition and verification succeed
- **WHEN** the selected external commands complete and the caller verifies the intended source locator, local target, and immutable revision or digest
- **THEN** the caller registers the existing target through `project repos register`
- **AND** any research workflow records the verified identity through its typed Artifact and provenance surfaces before reporting the ingestion complete

#### Scenario: Acquisition or verification fails
- **WHEN** an external command fails, the target is partial, the source relationship remains ambiguous, or the observed identity differs from the accepted request
- **THEN** the workflow records a blocker or resumable checkpoint with the attempted method, impact, and safe resume condition
- **AND** it does not create a successful semantic binding or accepted repository Artifact for that attempt

### Requirement: Repository Topology and Research Provenance Stay Separate
The system SHALL use the Topic Workspace Manifest as authority for a Canonical External Repository path and SHALL use typed Artifacts and Provenance Records as authority for research source identity, acquisition evidence, and revision history.

#### Scenario: Repository topology is registered
- **WHEN** `project repos register` succeeds
- **THEN** the Topic Workspace Manifest records the semantic label, canonical path, and topic-repository storage profile
- **AND** it does not embed remote URLs, command transcripts, credentials, source claims, or research relationships in the path binding

#### Scenario: Repository is accepted as research material
- **WHEN** Kaoju or another research workflow accepts a registered repository as source material
- **THEN** the applicable Artifact revision records or links the requested and resolved source locators, immutable commit or digest, acquisition method, sanitized command evidence, observed time, access and license posture, limitations, source relationships, and provenance refs
- **AND** it refers to the registered semantic label rather than treating its physical default path as durable identity

#### Scenario: Command evidence may contain secrets
- **WHEN** acquisition uses credentials, signed URLs, environment values, headers, credential helpers, or sensitive command output
- **THEN** durable evidence stores a redacted command description and non-secret observations sufficient for provenance
- **AND** it does not persist credentials or sensitive raw output in the Topic Workspace Manifest, Artifact payload, log, or diagnostic

#### Scenario: Registered repository revision changes
- **WHEN** later externally executed commands change the observed immutable revision at the registered path
- **THEN** the path binding remains stable and the research workflow creates or revises the applicable Artifact and provenance records
- **AND** historical revision identity is not silently rewritten in an existing accepted record
