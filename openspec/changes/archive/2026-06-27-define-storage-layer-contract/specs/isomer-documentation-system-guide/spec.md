## ADDED Requirements

### Requirement: Storage Contract Documentation
The documentation SHALL describe Workspace Path Resolution as the storage-layer contract for Topic Workspace and Agent Workspace file surfaces.

#### Scenario: Semantic labels are named as storage API
- **WHEN** docs describe where agents, services, or adapters read or write topic files
- **THEN** they present Semantic Workspace Surface Labels and `isomer-cli project paths get/list/preview` as the canonical path lookup interface

#### Scenario: Default directories are examples
- **WHEN** docs show directories such as `repos/topic-main`, `records/artifacts`, `runtime`, or `agents/<agent-name>`
- **THEN** they identify those directories as `isomer-default.v1` bindings rather than the storage contract itself

#### Scenario: Custom binding example is documented
- **WHEN** docs explain the Topic Workspace Manifest
- **THEN** they include an example of rebinding a built-in label and declaring a custom `custom.*` label through `isomer-cli project paths register` with `label`, `path`, and `storage_profile`

#### Scenario: Binding lifecycle commands are documented
- **WHEN** docs describe semantic path binding management
- **THEN** they explain register, update, unregister, reset, and materialize behavior, including that unregistering or resetting a binding does not delete filesystem content or rewrite historical Path Plans

#### Scenario: Default path and materialization commands are documented
- **WHEN** docs describe reserved semantic labels with default paths
- **THEN** they document how to query the default path and materialize the default filesystem target without treating the physical default path as the public contract

#### Scenario: Agents are told to query paths
- **WHEN** docs or skill references instruct an agent to use a Topic Workspace or Agent Workspace storage surface
- **THEN** they tell the agent to query the semantic label through `isomer-cli` or equivalent resolver output instead of remembering physical paths

### Requirement: Documentation Validation Detects Default-path-only Guidance
Documentation validation SHALL report guidance that treats concrete default directories as authoritative without nearby semantic labels or default-profile framing.

#### Scenario: Default path without semantic label is reported
- **WHEN** docs mention a default storage path such as `repos/topic-main` or `agents/<agent-name>` as a command target without naming the related semantic label
- **THEN** documentation validation reports the path guidance as stale or incomplete

#### Scenario: Custom label docs are checked
- **WHEN** docs describe user-defined semantic paths
- **THEN** documentation validation requires accepted custom namespace examples and storage profile terms rather than repeated storage-profile-derived fields
