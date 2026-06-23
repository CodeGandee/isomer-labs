# houmao-cli-adapter-layer Specification

## Purpose
TBD - created by archiving change implement-houmao-cli-adapter-layer. Update Purpose after archive.
## Requirements
### Requirement: CLI-backed Houmao adapter boundary
The system SHALL implement Houmao live lifecycle behavior through a bounded adapter layer that invokes `houmao-mgr --print-json` subprocess commands and does not require importing Houmao as a Python module in Isomer runtime code.

#### Scenario: Adapter does not require Houmao import
- **WHEN** Isomer imports its Houmao adapter modules in an environment where the `houmao` Python package is absent
- **THEN** the import succeeds, adapter availability reports the missing backend as a diagnostic when live operations are requested, and no generic Isomer import path executes `import houmao`

#### Scenario: CLI output is parsed and recorded
- **WHEN** the adapter runs a Houmao CLI command
- **THEN** it captures argv, cwd, bounded environment hints, exit status, parsed JSON output when present, sanitized diagnostics, timestamps, and payload refs in adapter-scoped records

#### Scenario: Nonzero exit returns Isomer diagnostics
- **WHEN** a Houmao CLI command exits with a nonzero status or emits invalid JSON for a `--print-json` request
- **THEN** the adapter returns deterministic Isomer diagnostics and does not replace them with raw Click tracebacks or unredacted Houmao output

### Requirement: Houmao adapter preflight
The system SHALL run read-only Houmao adapter preflight before writing launch material or mutating live Houmao-managed agents.

#### Scenario: Preflight checks local backend availability
- **WHEN** a quick launch or prepare-only command selects the Houmao adapter
- **THEN** preflight resolves the configured Houmao command or local checkout, verifies required command availability, validates selected Workspace Runtime schema and topic readiness, and reports blockers before any launch material or live Houmao state is changed

#### Scenario: Read-only capability probes do not mutate live state
- **WHEN** preflight probes Houmao capabilities
- **THEN** it may run read-only commands such as version, system-skills list, project status, and managed-agent listing, but it does not launch, stop, message, or edit Houmao-managed agents

### Requirement: Shared Houmao launch materialization
The system SHALL use one shared materialization flow for quick launch and prepare-only/manual Houmao workflows.

#### Scenario: Materialization writes durable adapter files
- **WHEN** the adapter materializes launch material for an Agent Team Instance
- **THEN** it writes deterministic Houmao project material, per-Agent Instance launch inputs, `adapter-link.json`, and `launch-material-manifest.json` under recorded Topic Workspace path plans before any Houmao launch command runs

#### Scenario: Materialization records editable material
- **WHEN** prepare-only material is generated for direct Houmao use
- **THEN** the launch-material manifest records generated file refs, raw byte digests, source, editable policy, and Agent Instance mapping hints so later reconciliation can detect user edits

#### Scenario: Materialization avoids cache semantics
- **WHEN** the adapter writes launch material, command payloads, launch logs, or generated Houmao profile files
- **THEN** it records them as durable adapter payload refs, Artifacts, or path-plan-backed files and does not classify them as cache or disposable temporary state

### Requirement: Isomer quick launch orchestration
The system SHALL quick-launch a Houmao-backed Agent Team Instance by launching one Houmao managed agent per Isomer Agent Instance and recording the resulting adapter refs.

#### Scenario: Quick launch starts mapped agents
- **WHEN** a user runs the Isomer quick launch command for a valid Houmao-backed Agent Team Instance and preflight passes
- **THEN** the adapter materializes launch files, launches the mapped Houmao managed agents through `houmao-mgr --print-json`, records per-Agent Instance launch attempts, writes `adapter-runtime-manifest.json`, and links the result to Workspace Runtime

#### Scenario: Partial launch remains recoverable
- **WHEN** one or more Houmao managed agents start successfully and a later launch step fails
- **THEN** Workspace Runtime preserves the launch attempt, known Agent Instance mappings, command payload refs, diagnostics, and stop or inspect-live recovery guidance

#### Scenario: Launch does not rewrite generic identity
- **WHEN** Houmao returns managed-agent ids, session refs, mailbox refs, gateway refs, or profile names
- **THEN** the adapter stores those values as opaque adapter refs or adapter payload refs and does not write them into generic Agent Team Instance or Agent Instance identity fields

### Requirement: Direct prepare and reconciliation lane
The system SHALL support a prepare-only Houmao adapter lane that lets users invoke `houmao-mgr` directly and later reconcile or adopt observed state through Isomer.

#### Scenario: Prepare-only does not launch
- **WHEN** a user runs the prepare-only launch material command for a Houmao-backed Agent Team Instance
- **THEN** Isomer writes launch material, `adapter-link.json`, and `launch-material-manifest.json`, reports the equivalent Houmao CLI guidance, and does not launch, stop, message, or inspect Houmao-managed agents

#### Scenario: Direct Houmao launch can be reconciled
- **WHEN** a user launches or edits Houmao material outside Isomer after prepare-only materialization
- **THEN** Isomer can use manifest reconciliation plus read-only Houmao inspection to report linked, externally detected, drifted, conflicted, adopted, stale, rejected, or launched-by-Isomer state without overwriting user-authored material

### Requirement: Houmao live inspect and stop operations
The system SHALL provide live inspect and stop operations through the CLI-backed Houmao adapter with explicit read-only and mutation boundaries.

#### Scenario: Inspect-live reads without starting agents
- **WHEN** a user inspects a Houmao-backed Agent Team Instance through Isomer
- **THEN** the adapter runs read-only Houmao CLI inspection, returns a deterministic generic runtime summary with bounded adapter details, and does not launch or stop managed agents

#### Scenario: Stop records durable outcome
- **WHEN** a user stops a Houmao-backed Agent Team Instance through Isomer
- **THEN** the adapter invokes the configured Houmao stop path for known mapped agents, records stopped, failed, partial, or stale outcomes with diagnostics and Provenance refs, and preserves launch records for audit

### Requirement: UC-01 Adapter Boundary
The system SHALL run UC-01 through the Houmao Execution Adapter boundary or an adapter-simulated equivalent without exposing Houmao native fields in generic research records.

#### Scenario: UC-01 uses adapter refs
- **WHEN** the UC-01 runner launches, simulates, dispatches, observes, normalizes, inspects, or stops adapter-backed work
- **THEN** Houmao command outputs, message ids, gateway events, managed-agent ids, sessions, and project overlay refs are stored only in adapter payload refs, manifests, or adapter-scoped records

#### Scenario: Generic UC-01 records stay provider-neutral
- **WHEN** UC-01 Artifacts, Evidence Items, Findings, Gates, Decision Records, View Manifests, Research Inquiries, Research Tasks, Runs, or Provenance Records are inspected
- **THEN** they expose Isomer lifecycle and recording refs rather than fields named after Houmao mailboxes, gateways, specialists, managed agents, or launch dossiers

### Requirement: UC-01 Simulated Adapter Mode
The system SHALL provide an adapter-simulated mode for UC-01 that exercises the same Isomer-side recording flow as live Houmao.

#### Scenario: Simulated mode produces handoff observations
- **WHEN** UC-01 runs in simulated adapter mode
- **THEN** the adapter layer produces deterministic dispatch, observation, and normalization inputs for Flash Attention 4 on GB10 scouting and synthesis-review handoffs without invoking real Houmao live mutations

#### Scenario: Simulated mode preserves payload refs
- **WHEN** simulated adapter mode produces command-like outputs
- **THEN** the system records bounded adapter payload refs so runtime summaries and validation use the same ref patterns as live mode

#### Scenario: Simulated mode stops before measured optimization
- **WHEN** simulated UC-01 output selects a UC-07-style measured optimization follow-up inquiry
- **THEN** the adapter layer records the decision path and does not simulate benchmark, baseline, candidate optimization, or correctness-check execution

### Requirement: UC-01 Live Houmao Cleanup
The system SHALL preserve cleanup and recovery state for UC-01 live Houmao runs.

#### Scenario: Live run records cleanup outcome
- **WHEN** UC-01 live mode launches or adopts Houmao-backed agents
- **THEN** the runner stops or reports cleanup state for the Agent Team Instance and records stopped, partial, failed, or skipped cleanup outcome with diagnostics

#### Scenario: Partial live run remains recoverable
- **WHEN** UC-01 live mode fails after some launch, handoff, observation, or recording work
- **THEN** Workspace Runtime preserves adapter command refs, payload refs, handoff refs, lifecycle refs, diagnostics, and recovery guidance without deleting started-agent or research records

