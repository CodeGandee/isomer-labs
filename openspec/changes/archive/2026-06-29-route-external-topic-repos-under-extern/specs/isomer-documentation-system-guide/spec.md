## MODIFIED Requirements

### Requirement: Semantic Workspace Path Documentation
The documentation SHALL explain that semantic surface labels are the workspace path contract and default directories are one layout profile.

#### Scenario: Topic Workspace Manifest is documented
- **WHEN** a reader opens Topic Workspace or runtime file documentation
- **THEN** the docs explain the Topic Workspace Manifest, its standard path, its topic-owned role, and its relationship to the Project Manifest

#### Scenario: Semantic labels are documented
- **WHEN** docs describe Topic Workspace and Agent Workspace paths
- **THEN** they name semantic labels such as `topic.repos.main`, non-main `topic.repos.<group...>.<repo-name>`, `topic.records.artifacts`, `agent.workspace`, `agent.private_artifacts`, `agent.public_share`, and `agent.scratch`

#### Scenario: Default layout is described as a profile
- **WHEN** docs show `repos/topic-main`, `repos/extern/...`, `records/*`, `runtime/*`, or `agents/<agent-name>`
- **THEN** they describe those paths as the `isomer-default.v1` bindings or helper defaults rather than the only valid contract

#### Scenario: Directory meanings stay readable
- **WHEN** docs describe directory meanings for the default layout
- **THEN** they use Markdown nested lists or equivalent prose instead of relying on a table as the only representation

#### Scenario: Main and external repository roles are distinguished
- **WHEN** docs describe topic-level repositories
- **THEN** they identify `repos/topic-main` as the primary Topic Main Repository and Agent Workspace worktree source
- **AND** they identify helper-created non-main `topic.repos.*` repositories under `repos/extern/...` as supporting topic-local repositories that may be inspected or modified when authorized by the gate or user

### Requirement: Storage Contract Documentation
The documentation SHALL describe Workspace Path Resolution as the storage-layer contract for Topic Workspace and Agent Workspace file surfaces.

#### Scenario: Semantic labels are named as storage API
- **WHEN** docs describe where agents, services, or adapters read or write topic files
- **THEN** they present Semantic Workspace Surface Labels and `isomer-cli project paths get/list/preview` as the canonical path lookup interface

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
- **WHEN** docs describe reserved semantic labels with default paths
- **THEN** they document how to query the default path and materialize the default filesystem target without treating the physical default path as the public contract

#### Scenario: Repository helper default is documented
- **WHEN** docs describe `project repos create`
- **THEN** they explain that bare non-main repository labels become `topic.repos.<group...>.<repo-name>` bindings with `storage_profile = "topic_repo"` and default paths under `repos/extern/...`

#### Scenario: Agents are told to query paths
- **WHEN** docs or skill references instruct an agent to use a Topic Workspace or Agent Workspace storage surface
- **THEN** they tell the agent to query the semantic label through `isomer-cli` or equivalent resolver output instead of remembering physical paths
