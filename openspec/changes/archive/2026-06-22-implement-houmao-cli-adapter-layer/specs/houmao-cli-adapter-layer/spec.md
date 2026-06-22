## ADDED Requirements

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
