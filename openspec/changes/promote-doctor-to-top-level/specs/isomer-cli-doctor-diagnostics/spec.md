## ADDED Requirements

### Requirement: Host Houmao Diagnostics
The system SHALL check the optional Houmao manager command boundary as part of system-level dependency diagnostics without making Houmao availability a prerequisite for read-only doctor output.

#### Scenario: Houmao manager executable is found
- **WHEN** `houmao-mgr` is available on `PATH`
- **THEN** `doctor` reports the Houmao manager executable path as a host check
- **AND** it attempts to report the Houmao manager version without mutating Houmao state

#### Scenario: Houmao manager executable is missing
- **WHEN** `houmao-mgr` is not available on `PATH`
- **THEN** `doctor` reports a warning or skipped optional host check with an Isomer diagnostic that names Houmao as required only for Houmao-backed Project bootstrap, launch, mailbox, gateway, and agent team operations
- **AND** the missing optional Houmao manager check does not make the doctor payload `ok` field false by itself

#### Scenario: Houmao manager version cannot be read
- **WHEN** `houmao-mgr` exists but its version command fails, times out, or returns unusable output
- **THEN** `doctor` reports a deterministic host diagnostic instead of raising an uncaught exception

## MODIFIED Requirements

### Requirement: Read-only Doctor Command
The system SHALL provide a top-level `isomer-cli doctor` command that reports system dependency, Project discovery, Project readiness, and topic readiness diagnostics without mutating Project files, Topic Workspaces, Workspace Runtime state, Houmao state, or Pixi environments.

#### Scenario: Doctor appears in help
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `doctor` as a top-level command

#### Scenario: Project doctor is removed
- **WHEN** a user runs `isomer-cli project doctor`
- **THEN** the command fails as an unknown Project subcommand
- **AND** it does not run doctor diagnostics through a compatibility alias

#### Scenario: Doctor does not mutate runtime state
- **WHEN** a user runs `isomer-cli doctor` for a Project or Research Topic
- **THEN** the command does not create `state.sqlite`, Workspace Runtime directories, Topic Workspace Artifact directories, Agent Workspace directories, Run directories, Houmao state directories, or Pixi environment directories

#### Scenario: Doctor has no fix mode
- **WHEN** a user inspects `isomer-cli doctor --help`
- **THEN** the command does not offer `--fix`, `--prepare`, or another option that implies mutation in this change

#### Scenario: Doctor exposes topic filters
- **WHEN** a user inspects `isomer-cli doctor --help`
- **THEN** the command documents repeatable `--with-topic <research-topic-id>` filters for narrowing topic diagnostics
- **AND** the help explains that the filter matches Research Topic ids

### Requirement: Host Pixi Diagnostics
The system SHALL always check the required Pixi executable and Pixi version before reporting Project or topic environment readiness.

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
The system SHALL always attempt Project discovery and SHALL inspect Project-level Pixi configuration from a discovered or explicitly selected Isomer Project without requiring Workspace Runtime state.

#### Scenario: No Project is discovered
- **WHEN** a user runs `doctor` outside an Isomer Project without an explicit Project selector
- **THEN** `doctor` reports that no Project was discovered
- **AND** it still reports system-level dependency checks
- **AND** it does not run topic checks

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
The system SHALL validate Project Manifest topic Pixi environment bindings for detected or filtered Research Topics without preparing environments, SHALL resolve Topic Workspace Pixi binding targets through Pixi, and SHALL accept the registered Topic Workspace directory as the implicit default target when no explicit standalone binding is present.

#### Scenario: All detected topics are checked by default
- **WHEN** a user runs `doctor` for a Project without `--with-topic`
- **THEN** `doctor` detects manifest-registered active Research Topics from the Project
- **AND** it runs topic readiness checks for every detected Research Topic using each topic's registered or default Topic Workspace
- **AND** it identifies each topic's checks by Research Topic

#### Scenario: Unregistered filesystem workspace is not auto-detected
- **WHEN** a Project has a directory under the Topic Workspace base directory
- **AND** the Project Manifest does not register a matching active Research Topic
- **THEN** `doctor` does not treat that directory as a detected topic
- **AND** it does not run topic readiness checks for that directory by default

#### Scenario: Topic filters narrow checks
- **WHEN** a user runs `doctor --with-topic alpha`
- **THEN** `doctor` runs topic readiness checks for the Research Topic whose id is `alpha`
- **AND** it does not run topic checks for unrequested detected topics

#### Scenario: Multiple topic filters are inclusive
- **WHEN** a user runs `doctor --with-topic alpha --with-topic beta`
- **THEN** `doctor` runs topic readiness checks for the Research Topics whose ids are `alpha` and `beta`
- **AND** it does not run topic checks for unrequested detected topics

#### Scenario: Unknown topic filter is reported
- **WHEN** a user runs `doctor --with-topic missing-topic`
- **AND** the Project has no registered Research Topic with id `missing-topic`
- **THEN** `doctor` reports a deterministic diagnostic for the unmatched topic filter
- **AND** it does not crash

#### Scenario: Topic filter does not match workspace id
- **WHEN** a user runs `doctor --with-topic alpha-ws`
- **AND** the Project has no registered Research Topic with id `alpha-ws`
- **AND** the Project has a Topic Workspace with id `alpha-ws`
- **THEN** `doctor` reports a deterministic diagnostic for the unmatched Research Topic id
- **AND** it does not use Topic Workspace id as a compatibility match

#### Scenario: Explicit project Pixi environment binding is valid
- **WHEN** the Project Manifest contains an active `topic_pixi_environment_bindings` entry that binds the selected Research Topic to a Pixi environment declared in the Project-level Pixi manifest
- **THEN** `doctor` reports a passing topic environment check for that Research Topic

#### Scenario: Multiple project Pixi environment bindings are valid
- **WHEN** the Project Manifest contains multiple active `topic_pixi_environment_bindings` entries that bind the selected Research Topic to Pixi environments declared in the Project-level Pixi manifest
- **THEN** `doctor` reports each bound environment and whether each environment exists without treating the environment names as topic semantics

#### Scenario: Missing topic environment binding is reported
- **WHEN** a checked Research Topic has no active Project Manifest `topic_pixi_environment_bindings` entry
- **AND** the checked Research Topic has no active Project Manifest `topic_standalone_pixi_bindings` entry
- **AND** Pixi cannot resolve the registered Topic Workspace directory as a Topic Workspace Pixi binding target
- **THEN** `doctor` reports a failing topic check without inferring a Pixi environment from the Research Topic id or Pixi environment names

#### Scenario: Missing bound Pixi environment is reported
- **WHEN** the Project Manifest contains an active `topic_pixi_environment_bindings` entry whose `pixi_environment` is absent from the Project-level Pixi manifest
- **THEN** `doctor` reports a failing topic check without editing the Pixi manifest or the Project Manifest

#### Scenario: Standalone Pixi isolation is inspected
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry for the selected Research Topic
- **THEN** `doctor` verifies that the standalone Pixi binding target resolves inside the Project root, asks Pixi to resolve the target, and reports the target path, target kind, resolved manifest path, selected environment, environment prefix, and binding source without running installation

#### Scenario: Pixi tooling failure is reported
- **WHEN** topic Pixi binding diagnostics need Pixi-backed binding target resolution
- **AND** Pixi is unavailable, cannot execute, returns invalid JSON, or omits required binding-resolution fields
- **THEN** `doctor` reports a failing Pixi tooling check with online and offline install guidance instead of reporting a missing topic binding

#### Scenario: Unresolvable standalone Pixi binding target is reported
- **WHEN** the Project Manifest contains an active `topic_standalone_pixi_bindings` entry whose target cannot be resolved by Pixi as a workspace
- **THEN** `doctor` reports a failing topic check without creating a Pixi manifest or installing the standalone environment

#### Scenario: Escaping standalone Pixi binding target is reported
- **WHEN** Pixi resolves a standalone Pixi binding target
- **AND** the resolved manifest path or selected environment prefix is outside the registered Topic Workspace
- **THEN** `doctor` reports a failing topic check without preparing the environment

#### Scenario: Implicit default standalone Pixi binding is accepted
- **WHEN** the Project Manifest contains no active `topic_standalone_pixi_bindings` entry for the selected Research Topic
- **AND** Pixi resolves the registered Topic Workspace directory as a confined Topic Workspace Pixi binding target
- **THEN** `doctor` reports a passing topic check for the implicit default binding and identifies the binding source as implicit-default

### Requirement: Doctor Output Contract
The system SHALL emit deterministic text and versioned JSON output for `doctor` suitable for CI, unit tests, and future Operator Agent consumption.

#### Scenario: JSON output is wrapped
- **WHEN** a user runs `isomer-cli --print-json doctor`
- **THEN** the response uses the existing `isomer-cli-output.v1` wrapper and includes `ok`, `mode`, `mutated`, `checks`, `topics`, and `diagnostics`

#### Scenario: Mutated flag is false
- **WHEN** a user runs `isomer-cli --print-json doctor`
- **THEN** the JSON payload reports `mutated` as false

#### Scenario: Required failures determine ok
- **WHEN** `doctor` emits JSON output
- **THEN** the JSON payload reports `ok` as false when a required check fails or an error diagnostic is present
- **AND** it does not report `ok` as false solely because an optional Houmao check warns or is skipped

#### Scenario: Topic payload is an array
- **WHEN** `doctor` emits JSON output
- **THEN** the JSON payload includes `topics` as an array
- **AND** it does not emit the legacy singular `topic` payload field

#### Scenario: No topic checks still emits topics array
- **WHEN** `doctor` emits JSON output outside a discovered Project
- **THEN** the JSON payload includes `topics` as an empty array

#### Scenario: Per-topic payload identifies topic context
- **WHEN** `doctor` emits JSON output for one or more checked Research Topics
- **THEN** each entry in `topics` identifies the Research Topic id
- **AND** each entry identifies the Topic Workspace id when known

#### Scenario: Checks have stable shape
- **WHEN** `doctor` emits JSON checks
- **THEN** each check includes a stable id, scope, status, concept, summary, and optional source path, source detail, or details
- **AND** each topic-scoped check includes the Research Topic id in `details` when it belongs to a checked Research Topic

#### Scenario: Text output groups checks
- **WHEN** a user runs `isomer-cli doctor` without JSON output
- **THEN** the text output groups checks by host, Project, and topic scope and uses Isomer concept names in diagnostic lines

#### Scenario: Secret values are not printed
- **WHEN** Project or topic config contains secret-like fields or values
- **THEN** `doctor` reports the offending field or path without printing the secret value
