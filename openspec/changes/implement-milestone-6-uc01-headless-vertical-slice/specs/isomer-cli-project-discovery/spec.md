## ADDED Requirements

### Requirement: UC-01 Headless Workflow Command
The system SHALL expose a modular CLI surface for running or validating the UC-01 headless workflow from an Isomer Project.

#### Scenario: UC-01 command is discoverable
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command surface includes a UC-01 headless workflow command or command group implemented outside the root CLI monolith

#### Scenario: UC-01 command accepts topic selectors
- **WHEN** a user runs the UC-01 headless workflow command
- **THEN** the command accepts Project selectors, topic selectors, optional Agent Team Instance selector, adapter mode selector, actor ref, and follow-up inquiry selection inputs using the same Effective Topic Context rules as other topic-scoped commands

### Requirement: UC-01 Deterministic JSON Output
The system SHALL emit deterministic JSON for the UC-01 headless workflow through root-level `--print-json`.

#### Scenario: JSON output reports created records
- **WHEN** a user runs `isomer-cli --print-json ...` for the UC-01 headless workflow
- **THEN** the output uses `isomer-cli-output.v1` and includes `ok`, `mutated`, selected Project and topic refs, Agent Team Instance ref, Research Inquiry refs, Research Task refs, Run refs, handoff refs, Artifact refs, Evidence Item refs, Gate ref, Decision Record ref, View Manifest refs, Provenance refs, diagnostics, and live or simulated mode

#### Scenario: Text output is structured
- **WHEN** a user runs the UC-01 headless workflow without `--print-json`
- **THEN** the output prints structured human-readable status lines for major stages and does not emit raw JSON by default

### Requirement: UC-01 Command Side-effect Boundary
The system SHALL make UC-01 workflow mutation explicit and keep inspection and dry validation side-effect free.

#### Scenario: Run command mutates explicitly
- **WHEN** the user invokes the UC-01 run command in simulated or live mode
- **THEN** the command may create Workspace Runtime records, adapter payloads, Artifacts, Gates, Decision Records, View Manifests, and Provenance Records and reports `mutated: true` in JSON output

#### Scenario: Validate command is read-only
- **WHEN** the user invokes UC-01 validation or dry inspection for an existing run
- **THEN** the command reports the current UC-01 record graph and diagnostics without creating missing records, launching agents, dispatching handoffs, or resolving Gates

### Requirement: UC-01 Live Gate Reporting
The system SHALL report live-gated Houmao validation status before UC-01 live mutation.

#### Scenario: Missing live gate skips live mode
- **WHEN** live Houmao mode is requested without the required live-validation environment gate
- **THEN** the command exits with a deterministic skipped status and does not mutate Project files, Workspace Runtime, adapter files, or live Houmao state

#### Scenario: Capability report precedes live mutation
- **WHEN** live Houmao mode is allowed
- **THEN** the command reports the Houmao command resolution, checkout path candidates, read-only capability checks, and cleanup plan before running launch, handoff, or stop mutations
