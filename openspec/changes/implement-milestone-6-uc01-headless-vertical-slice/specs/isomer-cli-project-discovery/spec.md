## ADDED Requirements

### Requirement: UC-01 Headless Manual Harness
The system SHALL expose a manual harness for running or validating the UC-01 headless workflow from an Isomer Project while keeping named UC-01 orchestration out of the product CLI.

#### Scenario: UC-01 harness is discoverable
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface does not include `uc01`, `uc01 run`, or `uc01 inspect`
- **AND** workflow docs point to `tests/manual/uc01_headless_vertical_slice`

#### Scenario: UC-01 harness uses generic context APIs
- **WHEN** a user runs the UC-01 manual harness
- **THEN** the harness resolves the Project, Research Topic, Topic Workspace, Topic Agent Team Profile, adapter mode, actor ref, and follow-up inquiry selection through generic CLI commands or reusable Python APIs

### Requirement: UC-01 Deterministic JSON Output
The system SHALL emit deterministic JSON for the UC-01 headless workflow through the manual harness.

#### Scenario: JSON output reports created records
- **WHEN** a user runs `pixi run python tests/manual/uc01_headless_vertical_slice`
- **THEN** the output includes `ok`, selected Project and topic refs, Agent Team Instance ref, Research Inquiry refs, Research Task refs, Run refs, handoff refs, Artifact refs, Evidence Item refs, Gate ref, Decision Record ref, route classification, View Manifest refs, Provenance refs, diagnostics, and live or simulated mode

#### Scenario: Generic commands keep structured output behavior
- **WHEN** a user runs generic Isomer CLI commands with or without `--print-json`
- **THEN** those commands keep their generic JSON or human-readable output behavior without adding command-local `--json`, `--format json`, or `--format=json` options

### Requirement: UC-01 Harness Side-effect Boundary
The system SHALL make UC-01 workflow mutation explicit and keep fixture validation side-effect free.

#### Scenario: Harness mutates only temporary fixture copies
- **WHEN** the user invokes the UC-01 harness in simulated or live mode
- **THEN** the harness copies the fixture Project to a temporary directory before creating Workspace Runtime records, adapter payloads, Artifacts, Gates, Decision Records, View Manifests, and Provenance Records

#### Scenario: Harness does not start UC-07 work
- **WHEN** the UC-01 harness records a follow-up inquiry classified as UC-07-style measured optimization
- **THEN** the harness exits after recording the Gate, Decision Record, selected Research Inquiry, and route classification without running measurement, baseline, or candidate optimization commands

#### Scenario: Fixture validation is read-only
- **WHEN** the user invokes generic `validate` against the pinned UC-01 fixture Project
- **THEN** the command reports Project diagnostics without creating runtime records, launching agents, dispatching handoffs, or resolving Gates

### Requirement: UC-01 Live Gate Reporting
The system SHALL report live-gated Houmao validation status before UC-01 live mutation.

#### Scenario: Missing live gate skips live mode
- **WHEN** live Houmao mode is requested without the required live-validation environment gate
- **THEN** the harness exits the live check with a deterministic skipped status and does not mutate Project files, Workspace Runtime, adapter files, or live Houmao state for that live copy

#### Scenario: Capability report precedes live mutation
- **WHEN** live Houmao mode is allowed
- **THEN** the harness reports the Houmao command resolution, checkout path candidates, read-only capability checks, and cleanup plan before running launch, handoff, or stop mutations
