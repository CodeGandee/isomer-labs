## ADDED Requirements

### Requirement: Project-Level Houmao Bootstrap
The system SHALL support Project-level Houmao bootstrap through the same CLI-backed Houmao boundary used by adapter operations, while keeping bootstrap distinct from per-Agent Team Instance launch material and live managed-agent mutation.

#### Scenario: Project bootstrap uses Houmao CLI
- **WHEN** Isomer initializes a new Project that requires Houmao support
- **THEN** it invokes `houmao-mgr --print-json project --project-dir <project-root> init` or the equivalent catalog-backed command runner without importing Houmao Python internals

#### Scenario: Project bootstrap records bounded diagnostics
- **WHEN** the Houmao Project bootstrap command returns invalid JSON, exits nonzero, times out, or cannot be resolved
- **THEN** Isomer reports deterministic diagnostics through its CLI output contract and does not expose raw tracebacks or unredacted Houmao output

#### Scenario: Project bootstrap is not adapter launch materialization
- **WHEN** Project-level Houmao bootstrap creates or validates `<project-root>/.houmao/`
- **THEN** the system does not treat that directory as an Agent Team Instance adapter root, launch-material manifest, adapter-runtime manifest, command payload directory, or live launch record

#### Scenario: Adapter overlay remains per team
- **WHEN** a later Houmao-backed Agent Team Instance is prepared or launched
- **THEN** the adapter continues to use Topic Workspace adapter paths for per-team launch material, reconciliation manifests, and runtime payload refs rather than storing those per-team records directly in Project bootstrap state
