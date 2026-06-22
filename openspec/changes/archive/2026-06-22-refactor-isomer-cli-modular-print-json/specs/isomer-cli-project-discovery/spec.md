## ADDED Requirements

### Requirement: Global Print JSON Mode
The system SHALL use root-level `--print-json` as the canonical JSON output switch for `isomer-cli`.

#### Scenario: Root print-json applies to subcommands
- **WHEN** a user runs `isomer-cli --print-json validate`, `isomer-cli --print-json doctor`, or `isomer-cli --print-json runtime inspect`
- **THEN** the selected command emits the deterministic `isomer-cli-output.v1` JSON wrapper

#### Scenario: Default output is structured text
- **WHEN** a user runs `isomer-cli validate`, `isomer-cli doctor`, or another supported command without `--print-json`
- **THEN** the command emits structured human-readable text and does not emit the JSON wrapper

#### Scenario: Help shows global output mode
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the root help lists `--print-json` as the global machine-readable output switch

## MODIFIED Requirements

### Requirement: Diagnostics and Output Formats
The system SHALL produce deterministic diagnostics, structured human-readable text, and machine-readable output for Project discovery, doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template inspection, and Topic Agent Team Profile commands.

#### Scenario: Diagnostics include stable codes
- **WHEN** validation reports an error
- **THEN** each diagnostic includes a stable code, severity, file path when known, Isomer concept name, and concise message

#### Scenario: Diagnostics avoid leaking secrets
- **WHEN** validation reports a secret-like field
- **THEN** diagnostic output identifies the offending field or path without printing the secret value

#### Scenario: JSON output is deterministic
- **WHEN** a user requests JSON output with root-level `--print-json` for `validate`, `doctor`, `topics list`, `workspaces list`, `context show`, `paths preview`, `schemas list`, `runtime init`, `runtime prepare`, `runtime inspect`, `runtime validate`, `team-instances create`, `team-instances list`, `team-instances show`, `team-templates list`, `team-templates inspect`, `team-templates validate`, `team-profiles specialize`, or `team-profiles validate`
- **THEN** the command emits deterministic JSON suitable for unit tests and future Operator Agent consumption

#### Scenario: JSON output is versioned but provisional
- **WHEN** a user requests JSON output from a command added for doctor diagnostics, Workspace Runtime management, topic environment readiness preparation, Agent Team Instance record management, template registration, or Topic Agent Team Profile specialization
- **THEN** the response includes an output schema version and is treated as a developer contract rather than a durable public research-record API

### Requirement: Click Command Registration
The system SHALL implement the `isomer-cli` command surface with modular Click command groups while preserving established Project discovery command behavior.

#### Scenario: Root command is Click backed
- **WHEN** the package exposes `isomer-cli` through `isomer_labs.cli:main`
- **THEN** the command dispatch uses a Click command group rather than an `argparse` parser tree

#### Scenario: Existing commands remain available
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help still lists `init`, `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, and `schemas list`

#### Scenario: Existing command outputs remain compatible
- **WHEN** a user runs `validate`, `topics list`, `workspaces list`, `context show`, `paths preview`, or `schemas list` with JSON output requested through root-level `--print-json`
- **THEN** the command emits the same versioned JSON contract shape used by the Milestone 1 project-discovery implementation

#### Scenario: Domain diagnostics remain Isomer diagnostics
- **WHEN** Project discovery, Project Manifest validation, Research Topic Config validation, Effective Topic Context resolution, or Workspace Path Resolution fails
- **THEN** the command reports stable Isomer diagnostics rather than replacing domain validation failures with Click parser errors

### Requirement: Fixture Project Validation Commands
The system SHALL validate milestone fixture Projects through the public CLI surfaces used by normal Projects.

#### Scenario: Fixture Project validate command is deterministic
- **WHEN** the validation suite runs `isomer-cli --print-json validate` against the Milestone 2 and 3 fixture Project
- **THEN** the output has deterministic JSON and reports no diagnostics for the positive fixture

#### Scenario: Fixture template commands are deterministic
- **WHEN** the validation suite runs `team-templates list`, `team-templates inspect`, and `team-templates validate` against fixture Projects with and without `--print-json`
- **THEN** the output has deterministic text and JSON for built-in and project-local template refs

#### Scenario: Fixture profile commands are deterministic
- **WHEN** the validation suite runs `team-profiles specialize` and `team-profiles validate` against fixture Projects with and without `--print-json`
- **THEN** the output has deterministic text and JSON for preview, write, and validation flows

### Requirement: Houmao adapter launch CLI surface
The system SHALL expose Houmao adapter launch, prepare-only, inspect-live, and stop behavior through explicit `isomer-cli team-instances` commands with deterministic text and JSON output.

#### Scenario: Help lists adapter launch commands
- **WHEN** a user runs `isomer-cli team-instances --help`
- **THEN** the command help lists `launch`, `launch-material prepare`, `inspect-live`, and `stop` without presenting Houmao-specific command names as core Isomer concepts

#### Scenario: Quick launch command reports mutation
- **WHEN** a user runs `isomer-cli --print-json team-instances launch <agent-team-instance-id> --adapter houmao`
- **THEN** the command emits deterministic JSON with Project, Research Topic, Topic Workspace, Agent Team Instance, selected Execution Adapter, launch attempt refs, manifest refs, diagnostics, and an explicit mutation summary

#### Scenario: Prepare-only command reports manual guidance
- **WHEN** a user runs `isomer-cli --print-json team-instances launch-material prepare <agent-team-instance-id> --adapter houmao`
- **THEN** the command emits deterministic JSON with generated material refs, manifest refs, validation diagnostics, and bounded manual `houmao-mgr` guidance without launching Houmao-managed agents

### Requirement: Houmao Manifest CLI Output
The system SHALL emit deterministic text and JSON output for Houmao adapter manifest and reconciliation commands.

#### Scenario: JSON output names generic refs
- **WHEN** a user requests JSON output with root-level `--print-json` from adapter link export, integrity inspection, reconcile, or adopt
- **THEN** the output names Project, Research Topic, Topic Workspace, Agent Team Instance, Agent Instance, Artifact, and Provenance refs plus opaque adapter refs and manifest paths

#### Scenario: Output reports reconciliation state
- **WHEN** a command observes linked, externally detected, adopted, drifted, conflicted, stale, or rejected state
- **THEN** the output includes the reconciliation state, mapping confidence, affected refs, and redacted diagnostics in stable field order
