## ADDED Requirements

### Requirement: Houmao Adapter CLI Surface
The system SHALL expose deterministic CLI commands for Houmao-backed Agent Team Instance launch, inspection, stop, and manual handoff operations while preserving existing read-only command guarantees.

#### Scenario: Launch command is explicit mutation
- **WHEN** a user runs `isomer-cli team-instances launch`
- **THEN** the command may materialize adapter launch files, create adapter records, start Houmao-managed agents, and update Workspace Runtime launch state for the selected Agent Team Instance

#### Scenario: Live inspect reads adapter state
- **WHEN** a user runs `isomer-cli team-instances inspect-live`
- **THEN** the command reads Houmao adapter state for the selected Agent Team Instance and emits deterministic JSON without creating a new Agent Team Instance or launching additional agents

#### Scenario: Stop command is explicit mutation
- **WHEN** a user runs `isomer-cli team-instances stop`
- **THEN** the command may request Houmao stop behavior and record stopped, failed, or stale adapter outcome state in Workspace Runtime

#### Scenario: Handoff dispatch command is explicit mutation
- **WHEN** a user runs `isomer-cli handoffs dispatch` for a launched Agent Team Instance
- **THEN** the command may create Run, handoff, adapter dispatch, Signal Observation, Artifact, and Provenance records for the selected Topic Workspace

#### Scenario: Handoff observation and normalization are explicit mutations
- **WHEN** a user runs `isomer-cli handoffs observe` or `isomer-cli handoffs normalize`
- **THEN** the command may record Signal Observations or accepted or rejected normalization results while keeping adapter observations separate from authoritative handoff completion

#### Scenario: Runtime record inspection remains read-only
- **WHEN** a user runs `runtime inspect`, `runtime validate`, `team-instances list`, or `team-instances show`
- **THEN** those commands do not launch Houmao agents, send handoffs, stop agents, or mutate adapter records

### Requirement: Houmao Adapter CLI Output
The system SHALL emit deterministic text and JSON for Houmao-backed launch, live inspection, stop, and handoff commands.

#### Scenario: Launch output names generic and adapter refs
- **WHEN** a user requests JSON from `team-instances launch`
- **THEN** the output includes generic Project, Research Topic, Topic Workspace, Agent Team Instance, Agent Instance, Run, and readiness refs plus opaque adapter refs and diagnostics

#### Scenario: Inspect output separates runtime and adapter state
- **WHEN** a user requests JSON from `team-instances inspect-live`
- **THEN** the output separates generic Workspace Runtime state from Houmao adapter inspection snapshots and opaque adapter payload refs

#### Scenario: Stop output preserves failed cleanup details
- **WHEN** a stop request cannot fully stop all Houmao-managed actors
- **THEN** the output reports remaining adapter refs and cleanup diagnostics without deleting launch records

#### Scenario: Handoff output names runtime and adapter refs
- **WHEN** a user requests JSON from `handoffs dispatch`, `handoffs observe`, or `handoffs normalize`
- **THEN** the output includes generic handoff, Run, Agent Team Instance, Signal Observation, Artifact, and Provenance refs plus opaque adapter refs and diagnostics
