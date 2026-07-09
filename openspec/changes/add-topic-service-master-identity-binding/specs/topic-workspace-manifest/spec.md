## ADDED Requirements

### Requirement: Topic Service Master Binding
The Topic Workspace Manifest SHALL store the binding between a Topic Workspace and its Houmao-backed Topic Service Master entities as topic-owned configuration.

#### Scenario: Binding table is parsed
- **WHEN** `topic-workspace.toml` contains `[topic_service_master]` and `[topic_service_master.houmao]` tables
- **THEN** the manifest parser exposes provider, status, nested Houmao specialist name, launch profile name, managed agent name, and optional refs
- **AND** the manifest JSON output includes the parsed binding

#### Scenario: Houmao binding records required names
- **WHEN** the binding provider is `houmao`
- **THEN** validation requires `topic_service_master.houmao.specialist_name`, `topic_service_master.houmao.launch_profile_name`, and `topic_service_master.houmao.managed_agent_name`
- **AND** each name must match the Topic Service Master naming contract unless an explicit repair override is in effect

#### Scenario: Binding status is bounded
- **WHEN** the binding declares a status
- **THEN** validation accepts only `prepared`, `launched`, `stopped`, `stale`, or `archived`

#### Scenario: Planned or failed preparation is not a binding
- **WHEN** Topic Service Master preparation has not successfully created or updated Houmao entities
- **THEN** the Topic Workspace Manifest does not record a `planned`, `blocked`, or `skipped` Topic Service Master binding
- **AND** command output, readiness records, or diagnostics report the blocked or skipped outcome instead

#### Scenario: Binding rejects secret and live runtime fields
- **WHEN** the binding contains credentials, tokens, passwords, raw launch profile payloads, mailbox contents, gateway queue state, process ids, or tmux session names
- **THEN** validation reports the binding as invalid
- **AND** it directs live runtime evidence to Workspace Runtime or Houmao runtime inspection surfaces

#### Scenario: Binding writes preserve other manifest content
- **WHEN** Isomer records or updates the Topic Service Master binding
- **THEN** it preserves existing path bindings, Topic Actor bindings, toolbox settings, comments where supported by the writer, and unknown non-conflicting tables
- **AND** it does not delete Topic Workspace files or Houmao Project state
