## ADDED Requirements

### Requirement: Handoff CLI Surface
The system SHALL expose top-level deterministic CLI commands for manual handoff dispatch, observation, and normalization while preserving existing read-only command guarantees.

#### Scenario: Handoff group is discoverable
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists a top-level `handoffs` command group without presenting Houmao-specific command names as core Isomer concepts

#### Scenario: Handoff dispatch command is explicit mutation
- **WHEN** a user runs `isomer-cli handoffs dispatch` for a launched or adopted Agent Team Instance
- **THEN** the command may create or update Run, handoff, adapter dispatch, adapter payload, Signal Observation, Artifact, and Provenance records for the selected Topic Workspace

#### Scenario: Handoff observe command is explicit mutation
- **WHEN** a user runs `isomer-cli handoffs observe`
- **THEN** the command may ingest Houmao mail, gateway, file, or bounded inspection signals as Signal Observations while keeping adapter observations separate from accepted handoff completion

#### Scenario: Handoff normalize command is explicit mutation
- **WHEN** a user runs `isomer-cli handoffs normalize`
- **THEN** the command may record accepted, rejected, blocked, superseded, repair-routed, or follow-up handoff normalization results with Run, Artifact, and Provenance refs

#### Scenario: Runtime record inspection remains read-only
- **WHEN** a user runs `runtime inspect`, `runtime validate`, `team-instances list`, `team-instances show`, or future read-only handoff inspection commands
- **THEN** those commands do not launch Houmao agents, send handoffs, stop agents, normalize results, or mutate adapter records

### Requirement: Handoff CLI Output
The system SHALL emit structured human-readable text by default and deterministic root-level `--print-json` output for manual handoff commands.

#### Scenario: Handoff dispatch JSON names runtime and adapter refs
- **WHEN** a user runs `isomer-cli --print-json handoffs dispatch`
- **THEN** the output includes generic Project, Research Topic, Topic Workspace, Agent Team Instance, source Agent Instance, target Agent Instance, handoff, Run, expected output, adapter dispatch, adapter payload, and Provenance refs plus diagnostics

#### Scenario: Handoff observe JSON keeps signals non-authoritative
- **WHEN** a user runs `isomer-cli --print-json handoffs observe`
- **THEN** the output includes Signal Observation refs, adapter payload refs, candidate status, diagnostics, and a field or diagnostic that indicates the observation did not mark the handoff accepted

#### Scenario: Handoff normalize JSON reports accepted or rejected result
- **WHEN** a user runs `isomer-cli --print-json handoffs normalize`
- **THEN** the output includes the handoff ref, normalization status, Run updates, Artifact refs, rejected or repair refs when present, Provenance refs, and diagnostics

#### Scenario: Handoff text output is structured
- **WHEN** a user runs `isomer-cli handoffs dispatch`, `isomer-cli handoffs observe`, or `isomer-cli handoffs normalize` without `--print-json`
- **THEN** the command emits structured human-readable text that names the selected Project, Research Topic, Topic Workspace, handoff status, relevant runtime refs, and diagnostics without dumping raw Houmao payloads

#### Scenario: Handoff commands do not add local JSON flags
- **WHEN** a user inspects help for `handoffs dispatch`, `handoffs observe`, or `handoffs normalize`
- **THEN** the commands do not advertise command-local `--json`, `--format json`, or `--format=json` flags and rely on root-level `--print-json` for machine-readable output
