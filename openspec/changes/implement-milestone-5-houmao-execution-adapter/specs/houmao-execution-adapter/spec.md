## ADDED Requirements

### Requirement: Houmao Adapter Boundary
The system SHALL implement Houmao as an Execution Adapter that maps Isomer runtime refs onto Houmao launch, communication, inspection, and stop surfaces without changing generic Isomer domain records.

#### Scenario: Adapter consumes Isomer runtime refs
- **WHEN** the Houmao adapter prepares an Agent Team Instance launch
- **THEN** it consumes validated Domain Agent Team Template, Topic Agent Team Profile, Agent Team Instance, Agent Instance, Agent Workspace, Run, and Artifact refs from Workspace Runtime rather than reading untracked launch facts from Project config

#### Scenario: Houmao details remain adapter scoped
- **WHEN** the adapter records Houmao project-profile launch refs, mailbox refs, gateway refs, notifier refs, managed-agent refs, or live process refs
- **THEN** those details are stored as opaque adapter refs or adapter-specific records linked to generic Workspace Runtime records

#### Scenario: Generic schema excludes Houmao fields
- **WHEN** an Agent Team Instance, Agent Instance, Run, handoff, or Artifact record is inspected through generic Isomer APIs
- **THEN** the record does not expose Houmao-specific field names as core schema fields

### Requirement: Local Houmao Checkout Preflight
The system SHALL validate the local Houmao checkout before live Houmao launch behavior depends on it.

#### Scenario: Houmao checkout is resolved
- **WHEN** a launch command selects the Houmao adapter
- **THEN** preflight resolves the ignored local checkout at `extern/orphan/houmao` or a documented override and reports the resolved source path

#### Scenario: Missing checkout blocks launch only
- **WHEN** the local Houmao checkout is missing or invalid
- **THEN** the system blocks Houmao launch and live adapter inspection while preserving unrelated Workspace Runtime inspection, validation, and record review

#### Scenario: Houmao validation is separate
- **WHEN** the adapter discovers a Houmao defect or missing capability
- **THEN** the required fix is made and validated in the Houmao checkout before Isomer records the adapter capability as available

#### Scenario: Capability gate is read-only
- **WHEN** Isomer checks whether the local Houmao checkout is available for adapter behavior
- **THEN** it resolves the checkout path, verifies `tmux -V`, runs `pixi run houmao-mgr --version`, `pixi run houmao-mgr --print-json system-skills list`, `pixi run houmao-mgr --print-json project --project-dir <project> status`, and `pixi run houmao-mgr --print-json agents global list` without launching agents, stopping agents, sending handoffs, or mutating Houmao state

### Requirement: Houmao Launch Material Generation
The system SHALL materialize Houmao launch material from the selected `deepsci-org` template and topic runtime records under recorded Workspace Runtime paths.

#### Scenario: Launch material uses deepsci-org template inputs
- **WHEN** the adapter materializes launch material for a `deepsci-org` Agent Team Instance
- **THEN** it uses `teams/deepsci-org/execplan/agents/`, generated skills, notifier prompts, topology, communication templates, Topic Agent Team Profile role bindings, and Agent Workspace path plans

#### Scenario: Launch material is path-planned
- **WHEN** launch material files are generated
- **THEN** the adapter records path plans and Provenance refs before Houmao launch depends on those files

#### Scenario: Launch material is retained durably
- **WHEN** the adapter generates project-profile launch files, notifier prompts, communication templates, mailbox metadata, gateway metadata, command JSON, checksums, or launch logs for a launch attempt
- **THEN** it records the generated material as durable file-backed Artifacts or adapter payload refs with Provenance Records and does not classify it as cache-like

#### Scenario: Generated material is topic scoped
- **WHEN** launch material is generated for one Topic Workspace
- **THEN** validation rejects launch material refs that point into another Topic Workspace or an untracked workspace-local team directory

### Requirement: Houmao Team Launch Inspect and Stop
The system SHALL launch, inspect, and stop one manual-mode Houmao-backed `deepsci-org` Agent Team Instance from Workspace Runtime.

#### Scenario: Manual team launch starts agents
- **WHEN** launch preflight passes for a manual-mode `deepsci-org` Agent Team Instance
- **THEN** the adapter starts the corresponding Houmao-managed agents and records adapter refs, launch status, Agent Instance mappings, and Provenance refs

#### Scenario: Launch uses public Houmao project profile surface
- **WHEN** the adapter starts Houmao-managed agents for Milestone 5
- **THEN** it invokes the documented public Houmao project-backed launch path `houmao-mgr --print-json project --project-dir <dir> agents launch --profile <generated-profile>` and stores command output, profile refs, managed-agent refs, gateway refs, mailbox refs, and runtime refs as opaque adapter payload refs

#### Scenario: Adapter inspection records snapshot
- **WHEN** the user inspects a launched Houmao-backed Agent Team Instance
- **THEN** the adapter reads Houmao runtime state and records or returns an inspection snapshot linked to the Agent Team Instance without mutating unrelated lifecycle state

#### Scenario: Stop records outcome
- **WHEN** the user stops a Houmao-backed Agent Team Instance
- **THEN** the adapter requests Houmao stop behavior, records stopped, failed, or stale outcome state, and preserves launch records for audit

#### Scenario: Partial launch remains recoverable
- **WHEN** Houmao launch partially succeeds and then fails
- **THEN** the system records the partial launch attempt, maps any known Agent Instance refs, and exposes stop or cleanup diagnostics without deleting existing runtime records

### Requirement: Houmao Manual Handoff Round
The system SHALL support one manual handoff round through Houmao mail or gateway observation and Operator Agent normalization.

#### Scenario: Manual handoff dispatches through adapter
- **WHEN** the Operator Agent delegates a Research Task or Run step from `deepsci-org-master` to a specialist Agent Instance
- **THEN** the adapter dispatches the handoff through Houmao mail or gateway surfaces and records the handoff, Run linkage, adapter refs, expected output refs, and Provenance refs

#### Scenario: Observation is not completion
- **WHEN** Houmao mail, gateway events, files, or inspection output indicate candidate completion
- **THEN** the adapter records Signal Observations without marking the handoff accepted

#### Scenario: Normalization accepts result
- **WHEN** the Operator Agent normalizes an observed handoff result
- **THEN** Workspace Runtime records accepted handoff state, produced Artifact refs when present, Run status updates, and Provenance Records
