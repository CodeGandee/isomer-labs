## ADDED Requirements

### Requirement: Topic Creator Uses Stable Topic Service Master Names
The Topic Creator skill SHALL route Houmao-backed Topic Service Master preparation with Isomer-provided specialist, launch profile, and managed-agent names.

#### Scenario: Setup actors obtains suggested names
- **WHEN** `setup-actors` reaches enabled Houmao-backed Topic Service Master preparation
- **THEN** it routes through `isomer-srv-topic-service-agent-support prepare-topic-service-master`
- **AND** the service route obtains suggested Topic Service Master names from `isomer-cli`

#### Scenario: Preparation records binding
- **WHEN** Houmao-owned procedure creates or updates the Topic Service Master specialist and launch profile
- **THEN** Topic Creator readiness consumes evidence that the Topic Workspace Manifest binding was recorded
- **AND** it does not treat preparation as ready from a chat-only name choice

#### Scenario: Final output includes binding state
- **WHEN** Topic Creator finalization reports Topic Workspace readiness
- **THEN** Essential Output includes Topic Service Master binding status, specialist name, launch profile name, managed agent name, or skip reason
- **AND** Complete Output includes the Topic Workspace Manifest binding evidence when available

#### Scenario: Disabled integration skips binding
- **WHEN** Project Houmao integration is disabled during setup-actors
- **THEN** Topic Creator reports Topic Service Master preparation and binding as skipped
- **AND** it does not create suggested-name bindings in the Topic Workspace Manifest
