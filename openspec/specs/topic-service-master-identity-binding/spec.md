# topic-service-master-identity-binding Specification

## Purpose
TBD - created by archiving change add-topic-service-master-identity-binding. Update Purpose after archive.
## Requirements
### Requirement: Canonical Topic Service Master Houmao Names
The system SHALL derive deterministic Houmao entity names for the Topic Service Master associated with a Topic Workspace.

#### Scenario: Names are derived from Topic Workspace id
- **WHEN** Isomer derives Topic Service Master names for Topic Workspace id `alpha`
- **THEN** it reports stem `isomer-tsm-alpha`
- **AND** it reports specialist name `isomer-tsm-alpha-specialist`
- **AND** it reports launch profile name `isomer-tsm-alpha-profile`
- **AND** it reports managed agent name `isomer-tsm-alpha-agent`

#### Scenario: Topic Workspace id is slugged
- **WHEN** the Topic Workspace id contains uppercase letters, underscores, spaces, or punctuation
- **THEN** Isomer lowercases the id, replaces non-alphanumeric runs with dashes, collapses repeated dashes, and trims leading or trailing dashes before building names

#### Scenario: Empty slug is rejected
- **WHEN** the Topic Workspace id cannot produce a non-empty slug
- **THEN** Isomer reports a deterministic diagnostic
- **AND** it does not guess specialist, launch profile, or managed agent names

#### Scenario: Long names are stable
- **WHEN** the derived names would exceed the accepted maximum name length
- **THEN** Isomer shortens the slug and appends a deterministic hash suffix
- **AND** repeated calls for the same Topic Workspace id return the same names

### Requirement: Topic Service Master Names CLI
The system SHALL expose a read-only CLI command that returns suggested Topic Service Master Houmao names for a Topic Workspace id.

#### Scenario: Suggested names are queryable by Topic Workspace id
- **WHEN** a user or agent runs `isomer-cli --print-json project integrations houmao topic-service-master names --topic-workspace <topic-workspace-id>`
- **THEN** the JSON output includes `topic_workspace_id`, `topic_workspace_slug`, `stem`, `specialist_name`, `launch_profile_name`, and `managed_agent_name`
- **AND** the command does not require Houmao integration to be enabled

#### Scenario: Suggested names resolve Project Manifest workspace
- **WHEN** the requested Topic Workspace id is registered in the Project Manifest
- **THEN** the JSON output includes the Topic Workspace path and associated Research Topic id

#### Scenario: Unknown workspace is diagnostic
- **WHEN** the requested Topic Workspace id is not registered in the Project Manifest
- **THEN** the command reports a deterministic diagnostic naming the missing Topic Workspace id
- **AND** it does not write Project or Topic Workspace state

### Requirement: Houmao Skill Context Includes Topic Service Master Identity
The system SHALL include Topic Service Master name and binding context in Houmao skill-context output when a Topic Workspace is selected.

#### Scenario: Skill context includes suggested names
- **WHEN** `isomer-cli --print-json project integrations houmao skill-context prepare-topic-service-master --topic <research-topic-id>` resolves a Topic Workspace
- **THEN** the JSON output includes `topic_service_master.suggested_names.specialist_name`
- **AND** it includes `topic_service_master.suggested_names.launch_profile_name`
- **AND** it includes `topic_service_master.suggested_names.managed_agent_name`

#### Scenario: Skill context includes existing binding
- **WHEN** the selected Topic Workspace Manifest records a Topic Service Master binding
- **THEN** skill-context output includes `topic_service_master.binding`
- **AND** the binding includes provider, status, and nested Houmao specialist name, launch profile name, managed agent name, and refs when present

#### Scenario: Skill context reports binding drift
- **WHEN** the selected Topic Workspace Manifest binding names differ from current suggested names
- **THEN** skill-context output includes a diagnostic or drift marker
- **AND** it does not silently replace the binding

### Requirement: Topic Service Master Binding CLI
The system SHALL expose CLI commands for inspecting and recording the Topic Workspace Manifest binding for Topic Service Master Houmao entities.

#### Scenario: Binding can be inspected
- **WHEN** a user or agent runs `isomer-cli --print-json project integrations houmao topic-service-master binding show --topic <research-topic-id>`
- **THEN** the JSON output includes the current binding when present
- **AND** it includes suggested names for the selected Topic Workspace

#### Scenario: Binding can be recorded after preparation
- **WHEN** a service workflow records a binding with provider `houmao`, status `prepared`, specialist name, launch profile name, and managed agent name
- **THEN** Isomer validates those names against the suggested name set unless an explicit repair override is used
- **AND** it writes Isomer-level binding metadata under `[topic_service_master]`
- **AND** it writes Houmao-specific names and refs under `[topic_service_master.houmao]`

#### Scenario: Failed preparation does not write planned binding
- **WHEN** Houmao preparation is blocked, skipped, or fails before reporting created or updated entities
- **THEN** the binding record command reports the outcome without writing a Topic Workspace Manifest binding
- **AND** later prepare or repair workflows can recompute suggested names from the Topic Workspace id

#### Scenario: Disabled integration does not write binding
- **WHEN** Project Houmao integration is disabled
- **THEN** binding record commands report a skipped status
- **AND** they do not create or update the Topic Workspace Manifest binding

