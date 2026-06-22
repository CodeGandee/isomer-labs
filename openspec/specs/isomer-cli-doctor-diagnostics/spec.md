# isomer-cli-doctor-diagnostics Specification

## Purpose
Define the read-only `isomer-cli doctor` diagnostics contract for host dependency, Project, and Research Topic readiness checks.

## Requirements
### Requirement: Read-only Doctor Command
The system SHALL provide a top-level `isomer-cli doctor` command that reports dependency, Project, and topic readiness diagnostics without mutating Project files, Topic Workspaces, Workspace Runtime state, or Pixi environments.

#### Scenario: Doctor appears in help
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `doctor` as a top-level command

#### Scenario: Doctor does not mutate runtime state
- **WHEN** a user runs `isomer-cli doctor` for a Project or Research Topic
- **THEN** the command does not create `state.sqlite`, Workspace Runtime directories, Topic Workspace Artifact directories, Agent Workspace directories, Run directories, or Pixi environment directories

#### Scenario: Doctor has no fix mode
- **WHEN** a user inspects `isomer-cli doctor --help`
- **THEN** the command does not offer `--fix`, `--prepare`, or another option that implies mutation in this change

### Requirement: Host Pixi Diagnostics
The system SHALL check the required Pixi executable and Pixi version before reporting Project or topic environment readiness.

#### Scenario: Pixi executable is found
- **WHEN** `pixi` is available on `PATH`
- **THEN** `doctor` reports the Pixi executable path and version as a passing host check

#### Scenario: Pixi executable is missing
- **WHEN** `pixi` is not available on `PATH`
- **THEN** `doctor` reports a failing host check with an Isomer diagnostic that names Pixi as a required Project dependency

#### Scenario: Pixi requirement is verified when declared
- **WHEN** the Project-level Pixi manifest declares `requires-pixi`
- **THEN** `doctor` verifies the running Pixi version against that requirement or reports that the check was skipped because Pixi is unavailable

### Requirement: Project Pixi Manifest Diagnostics
The system SHALL inspect Project-level Pixi configuration from a discovered or explicitly selected Isomer Project without requiring Workspace Runtime state.

#### Scenario: Project-level Pixi manifest is detected
- **WHEN** a Project has Pixi configuration in `pyproject.toml` or `pixi.toml`
- **THEN** `doctor` reports the manifest path, available Pixi environments when known, and whether `pixi.lock` is present

#### Scenario: Project-level Pixi manifest is missing
- **WHEN** a Project has no Project-level Pixi manifest or recognized Pixi configuration
- **THEN** `doctor` reports a failing Project check because Pixi is a required dependency for this Isomer version

#### Scenario: Lockfile warning is reported
- **WHEN** a Project-level Pixi manifest exists but `pixi.lock` is missing
- **THEN** `doctor` reports a warning check rather than creating or updating the lockfile

### Requirement: Topic Environment Binding Diagnostics
The system SHALL validate explicit Project Manifest topic Pixi environment bindings for selected or default Research Topics without preparing environments.

#### Scenario: Explicit project Pixi environment binding is valid
- **WHEN** the Project Manifest contains an active `topic_pixi_environment_bindings` entry that binds the selected Research Topic to a Pixi environment declared in the Project-level Pixi manifest
- **THEN** `doctor` reports a passing topic environment check for that Research Topic

#### Scenario: Multiple project Pixi environment bindings are valid
- **WHEN** the Project Manifest contains multiple active `topic_pixi_environment_bindings` entries that bind the selected Research Topic to Pixi environments declared in the Project-level Pixi manifest
- **THEN** `doctor` reports each bound environment and whether each environment exists without treating the environment names as topic semantics

#### Scenario: Missing topic environment binding is reported
- **WHEN** the selected Research Topic has no active Project Manifest `topic_pixi_environment_bindings` entry
- **THEN** `doctor` reports a failing topic check without inferring a Pixi environment from the Research Topic id or Pixi environment names

#### Scenario: Missing bound Pixi environment is reported
- **WHEN** the Project Manifest contains an active `topic_pixi_environment_bindings` entry whose `pixi_environment` is absent from the Project-level Pixi manifest
- **THEN** `doctor` reports a failing topic check without editing the Pixi manifest or the Project Manifest

#### Scenario: Standalone Pixi isolation is inspected
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry for the selected Research Topic
- **THEN** `doctor` verifies that the standalone Pixi manifest path resolves inside the Project root and reports whether the manifest exists without running installation

#### Scenario: Missing standalone Pixi manifest is reported
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry whose `manifest_path` does not exist
- **THEN** `doctor` reports a failing topic check without creating the standalone manifest or installing the standalone environment

### Requirement: Doctor Output Contract
The system SHALL emit deterministic text and versioned JSON output for `doctor` suitable for CI, unit tests, and future Operator Agent consumption.

#### Scenario: JSON output is wrapped
- **WHEN** a user runs `isomer-cli doctor --json`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, `mode`, `mutated`, `checks`, and `diagnostics`

#### Scenario: Mutated flag is false
- **WHEN** a user runs `isomer-cli doctor --json`
- **THEN** the JSON payload reports `mutated` as false

#### Scenario: Checks have stable shape
- **WHEN** `doctor` emits JSON checks
- **THEN** each check includes a stable id, scope, status, concept, summary, and optional source path or source detail

#### Scenario: Text output groups checks
- **WHEN** a user runs `isomer-cli doctor` without JSON output
- **THEN** the text output groups checks by host, Project, and topic scope and uses Isomer concept names in diagnostic lines

#### Scenario: Secret values are not printed
- **WHEN** Project or topic config contains secret-like fields or values
- **THEN** `doctor` reports the offending field or path without printing the secret value
