## MODIFIED Requirements

### Requirement: Workspace Runtime CLI and API Surface
The system SHALL expose deterministic CLI and Python APIs for Workspace Runtime initialization, inspection, validation, and Agent Team Instance record management.

#### Scenario: Runtime commands are available
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface includes `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, and `team-instances show`

#### Scenario: Runtime init emits deterministic JSON
- **WHEN** a user runs `isomer-cli --print-json runtime init`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, Project ref, Research Topic ref, Topic Workspace ref, runtime schema version, runtime path, created-or-opened status, and diagnostics

#### Scenario: Runtime prepare emits deterministic JSON
- **WHEN** a user runs `isomer-cli --print-json runtime prepare`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, Project ref, Research Topic ref, Topic Workspace ref, runtime schema version, readiness records, readiness status, preparation status, and diagnostics

#### Scenario: Team instance list is topic scoped
- **WHEN** a user runs `isomer-cli team-instances list`
- **THEN** the command lists only Agent Team Instance records from the selected Topic Workspace unless a later accepted contract adds a Project-wide listing mode

#### Scenario: Team instance show reports related records
- **WHEN** a user runs `isomer-cli team-instances show <agent-team-instance-id>`
- **THEN** the command reports the Agent Team Instance record, Agent Instance refs, Agent Workspace refs, active Run refs when known, Workflow Stage Cursor refs, status, blocker refs, and diagnostics
