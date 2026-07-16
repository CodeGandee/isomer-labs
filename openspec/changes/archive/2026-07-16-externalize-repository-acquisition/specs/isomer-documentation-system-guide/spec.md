## MODIFIED Requirements

### Requirement: isomer-cli Command Reference
The system SHALL document every public `isomer-cli` command with purpose, prerequisites, side effects, common examples, and JSON/text output posture.

#### Scenario: CLI command coverage is checked
- **WHEN** documentation validation runs
- **THEN** every public command exposed by `isomer-cli --help` and documented command groups is represented in the CLI reference, or the validation reports the missing command

#### Scenario: Global JSON mode is documented
- **WHEN** a reader opens the CLI reference
- **THEN** it documents root-level `--print-json` as the canonical JSON output switch and does not present command-local `--json` or `--format json` as normal usage

#### Scenario: Side effects are explicit
- **WHEN** a documented command can mutate Project files, Workspace Runtime records, adapter manifests, generated launch material, or live Houmao-managed agents
- **THEN** the command reference states the mutation boundary before or alongside the command example

#### Scenario: Read-only commands are identified
- **WHEN** a documented command is read-only
- **THEN** the command reference states that it does not create Workspace Runtime state, Agent Workspaces, launch material, or live Houmao state

#### Scenario: Repository commands show the external boundary
- **WHEN** the command reference documents `project paths default`, `project repos create`, or `project repos register`
- **THEN** it states that default-path lookup is read-only, repository registration changes only the Topic Workspace Manifest, and repository-directory creation does not initialize or acquire a Git repository
- **AND** it explains that clone, fetch, checkout, copy, repair, and verification commands run outside Isomer APIs

#### Scenario: Removed repository acquisition command is absent
- **WHEN** the public CLI reference and examples are validated after this change
- **THEN** they contain no active `project repos acquire`, `repository_acquisition`, fixed depth-one clone, or Isomer-owned repository cleanup workflow

### Requirement: Intended Usage Workflows
The system SHALL document operator-oriented workflows for the current supported paths through Project setup, validation, runtime preparation, external repository acquisition and registration, team profile work, Agent Team Instance records, Houmao materialization, quick launch, inspection, stop, reconciliation, and adoption.

#### Scenario: Minimal project workflow is documented
- **WHEN** a new user follows the getting-started guide
- **THEN** the guide shows how to initialize a Project, inspect or validate it, resolve context, preview paths, initialize Workspace Runtime, prepare readiness, and create an Agent Team Instance without launching agents

#### Scenario: External repository workflow is documented
- **WHEN** a user or agent needs a Canonical External Repository
- **THEN** the docs show how to query or choose a non-mutating target, run user-selected or task-appropriate repository commands outside `isomer-cli`, verify source identity, register the existing path, and record applicable provenance
- **AND** failure examples do not create a successful binding or imply that Isomer cleans partial filesystem content

#### Scenario: Houmao quick launch workflow is documented
- **WHEN** a user needs Isomer to launch a Houmao-backed Agent Team Instance
- **THEN** the docs explain the quick launch command sequence, preflight expectations, generated manifests, command payload records, live inspection, stop behavior, and validation checks

#### Scenario: Manual Houmao workflow is documented
- **WHEN** a user wants to inspect or edit Houmao launch material before invoking Houmao directly
- **THEN** the docs explain prepare-only materialization, manual `houmao-mgr` operation, direct edit drift detection, reconciliation, and explicit adoption

### Requirement: Documentation Verification
The system SHALL provide a repository-local documentation verification path that can be run during implementation and review.

#### Scenario: Docs validation command exists
- **WHEN** contributors inspect development commands
- **THEN** there is a documented command or script for validating documentation coverage and links

#### Scenario: Docs validation checks command coverage
- **WHEN** docs validation runs
- **THEN** it checks that the CLI reference includes current public command names and reports missing or stale command names

#### Scenario: Docs validation checks stale JSON examples
- **WHEN** docs validation runs after this change
- **THEN** it reports stale Isomer CLI examples that use command-local `--json` or `--format json` instead of root-level `--print-json`

#### Scenario: Docs validation checks canonical language posture
- **WHEN** docs validation runs
- **THEN** it checks selected docs for known stale or forbidden project terms and reports likely violations without replacing human review

#### Scenario: Docs validation checks legacy workspace paths
- **WHEN** docs validation runs after this change
- **THEN** it reports `.isomer-agent/` and top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` guidance outside migration notes as stale workspace layout language

#### Scenario: Docs validation checks repository-acquisition ownership
- **WHEN** docs validation scans active documentation, tutorials, and system-skill explanations
- **THEN** it reports `project repos acquire`, `repository_acquisition`, the removed repository service, fixed Isomer-owned clone behavior, registration before verification, and claims that Isomer cleans partial external acquisitions
- **AND** it accepts direct repository commands only when nearby guidance identifies them as user-controlled or agent-controlled external operations followed by non-executing Isomer registration

### Requirement: Storage Contract Documentation
The documentation SHALL describe Workspace Path Resolution as the storage-layer contract for Topic Workspace and Agent Workspace file surfaces.

#### Scenario: Semantic labels are named as storage API
- **WHEN** docs describe where agents, services, or adapters read or write topic files
- **THEN** they present Semantic Workspace Surface Labels and `isomer-cli project paths get/list/preview/default` as the canonical path lookup interface

#### Scenario: Default directories are examples
- **WHEN** docs show directories such as `repos/topic-main`, `repos/extern/<repo-label-path>`, `records/artifacts`, `runtime`, or `agents/<agent-name>`
- **THEN** they identify those directories as `isomer-default.v1` bindings, helper defaults, or examples rather than the storage contract itself

#### Scenario: Custom binding example is documented
- **WHEN** docs explain the Topic Workspace Manifest
- **THEN** they include an example of rebinding a built-in label and declaring a custom `custom.*` label through `isomer-cli project paths register` with `label`, `path`, and `storage_profile`

#### Scenario: Binding lifecycle commands are documented
- **WHEN** docs describe semantic path binding management
- **THEN** they explain register, update, unregister, reset, and materialize behavior, including that unregistering or resetting a binding does not delete filesystem content or rewrite historical Path Plans

#### Scenario: Default path and materialization commands are documented
- **WHEN** docs describe reserved or valid grouped repository semantic labels with default paths
- **THEN** they document how to query the default path and, where supported, materialize a default filesystem target without treating the physical default path as the public contract

#### Scenario: Repository helpers are documented
- **WHEN** docs describe `project repos create` or `project repos register`
- **THEN** they explain that bare non-main repository labels become `topic.repos.<group...>.<repo-name>` bindings with `storage_profile = "topic_repo"` and helper defaults under `repos/extern/...`
- **AND** they distinguish directory creation from registration of an existing externally acquired repository and state that neither helper executes Git commands

#### Scenario: Agents are told to query paths
- **WHEN** docs or skill references instruct an agent to use a Topic Workspace or Agent Workspace storage surface
- **THEN** they tell the agent to query the semantic label through `isomer-cli` or equivalent resolver output instead of remembering physical paths
