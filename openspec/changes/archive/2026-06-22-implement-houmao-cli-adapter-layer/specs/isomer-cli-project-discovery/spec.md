## ADDED Requirements

### Requirement: Houmao adapter launch CLI surface
The system SHALL expose Houmao adapter launch, prepare-only, inspect-live, and stop behavior through explicit `isomer-cli team-instances` commands with deterministic text and JSON output.

#### Scenario: Help lists adapter launch commands
- **WHEN** a user runs `isomer-cli team-instances --help`
- **THEN** the command help lists `launch`, `launch-material prepare`, `inspect-live`, and `stop` without presenting Houmao-specific command names as core Isomer concepts

#### Scenario: Quick launch command reports mutation
- **WHEN** a user runs `isomer-cli team-instances launch <agent-team-instance-id> --adapter houmao --json`
- **THEN** the command emits deterministic JSON with Project, Research Topic, Topic Workspace, Agent Team Instance, selected Execution Adapter, launch attempt refs, manifest refs, diagnostics, and an explicit mutation summary

#### Scenario: Prepare-only command reports manual guidance
- **WHEN** a user runs `isomer-cli team-instances launch-material prepare <agent-team-instance-id> --adapter houmao --json`
- **THEN** the command emits deterministic JSON with generated material refs, manifest refs, validation diagnostics, and bounded manual `houmao-mgr` guidance without launching Houmao-managed agents

### Requirement: Houmao adapter CLI side-effect boundaries
The system SHALL make side effects explicit for all Houmao adapter CLI commands.

#### Scenario: Inspect-live is read-only by default
- **WHEN** a user runs `isomer-cli team-instances inspect-live <agent-team-instance-id> --adapter houmao`
- **THEN** the command may read Workspace Runtime, manifests, and live Houmao state, but it does not create Agent Team Instances, launch agents, stop agents, or write adoption state unless a separate explicit recording or reconciliation command is used

#### Scenario: Stop is explicit mutation
- **WHEN** a user runs `isomer-cli team-instances stop <agent-team-instance-id> --adapter houmao`
- **THEN** the command reports that it may mutate live Houmao state and records the stop outcome in Workspace Runtime when the selected runtime schema supports adapter stop records

#### Scenario: Failed preflight has no live mutation
- **WHEN** quick launch or stop preflight fails
- **THEN** the command returns deterministic diagnostics and does not start, stop, message, or edit Houmao-managed agents
