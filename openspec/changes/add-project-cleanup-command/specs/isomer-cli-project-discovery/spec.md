## ADDED Requirements

### Requirement: Project Cleanup CLI Surface
The system SHALL expose a Project-scoped `isomer-cli project cleanup` command for planning and applying selected Isomer-managed Project cleanup.

#### Scenario: CLI help lists cleanup
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `project cleanup` with the other Project discovery and lifecycle commands

#### Scenario: Cleanup help lists destructive controls
- **WHEN** a user runs `isomer-cli project cleanup --help`
- **THEN** the help lists `--part`, `--dry-run`, `--yes`, topic selection controls, optional content-root selection, and purge opt-in controls

#### Scenario: Cleanup supports JSON output
- **WHEN** a user runs `isomer-cli --print-json project cleanup --part project-config --dry-run`
- **THEN** the command emits the standard versioned JSON output wrapper with a cleanup payload and deterministic diagnostics

#### Scenario: Cleanup rejects unknown part
- **WHEN** a user supplies an unsupported cleanup part
- **THEN** the command rejects the request through Click validation or an Isomer diagnostic before planning deletion

### Requirement: Project Cleanup Output Contract
The system SHALL report cleanup plans and cleanup results with deterministic text and machine-readable payloads.

#### Scenario: Dry-run payload is non-mutating
- **WHEN** cleanup runs with `--dry-run`
- **THEN** the output includes `mutated = false`, `dry_run = true`, selected parts, planned removals, skipped targets, diagnostics, and the resolved Project root

#### Scenario: Confirmed payload reports mutation
- **WHEN** cleanup runs with `--yes` and removes at least one planned target
- **THEN** the output includes `mutated = true`, `dry_run = false`, selected parts, removed targets, skipped targets, diagnostics, and the resolved Project root

#### Scenario: Cleanup diagnostics are stable
- **WHEN** cleanup refuses a target or cannot remove a planned target
- **THEN** each diagnostic includes a stable code, severity, file path when known, Isomer concept name, field or target reference when available, and a concise message

### Requirement: Project Cleanup Side-effect Boundaries
The system SHALL keep cleanup filesystem side effects explicit and SHALL avoid live runtime or service operations.

#### Scenario: Dry-run is side-effect free
- **WHEN** cleanup runs with `--dry-run`
- **THEN** it does not create, modify, or delete Project files, Workspace Runtime records, adapter manifests, live Houmao state, mailboxes, gateways, sessions, or launch dossiers

#### Scenario: Houmao overlay cleanup is local only
- **WHEN** cleanup applies `--part houmao-overlay --yes`
- **THEN** it may remove the local `.houmao/` overlay but does not stop, launch, inspect, message, or adopt live Houmao managed agents

#### Scenario: Runtime cleanup is filesystem scoped
- **WHEN** cleanup applies `--part runtime --topic <topic-id> --yes`
- **THEN** it removes only planned runtime files and directories under the selected Topic Workspace and does not invoke runtime prepare, runtime validate, or adapter live-state commands

### Requirement: Project Initialization Cleanup Separation
The system SHALL preserve Project initialization overwrite refusal and direct users to explicit cleanup when reinitialization requires removing existing managed material.

#### Scenario: Existing manifest blocks init
- **WHEN** a user runs `isomer-cli project init` in a Project with `.isomer-labs/manifest.toml`
- **THEN** init refuses to overwrite the existing Project Manifest, does not create or modify content roots, and does not run cleanup automatically

#### Scenario: Existing manifest diagnostic mentions cleanup path
- **WHEN** init refuses because the Project Manifest already exists
- **THEN** the diagnostic or human-readable guidance names `isomer-cli project cleanup --dry-run` as the supported way to preview removal before reinitialization
