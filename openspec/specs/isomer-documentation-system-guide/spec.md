# isomer-documentation-system-guide Specification

## Purpose
TBD - created by archiving change rewrite-docs-comprehensive-system-guide. Update Purpose after archive.
## Requirements
### Requirement: Documentation Information Architecture
The system SHALL provide a coherent `docs/` documentation set with stable entry points for getting started, core concepts, system design, CLI usage, workflows, runtime files, Houmao adapter behavior, assumptions, troubleshooting, and documentation maintenance.

#### Scenario: Required docs pages exist
- **WHEN** repository documentation is validated
- **THEN** the docs tree includes entry pages for index, getting started, concepts, system design, `isomer-cli`, workflows, runtime and files, Houmao adapter, assumptions and roadmap, troubleshooting, and contributing to docs

#### Scenario: README points to detailed docs
- **WHEN** a reader opens `README.md`
- **THEN** it gives a concise project orientation and links to the detailed docs rather than duplicating the full system guide

### Requirement: System Design Documentation
The system SHALL document the current Isomer Labs architecture using canonical domain language and explicit state ownership boundaries.

#### Scenario: Core state ownership is explained
- **WHEN** a reader opens the system design documentation
- **THEN** it explains how Project, Project Config Directory, Project Manifest, Research Topic Config, Topic Workspace, Workspace Runtime, Agent Workspace, and adapter-generated files relate to each other

#### Scenario: Execution layers are separated
- **WHEN** a reader opens the system design documentation
- **THEN** it distinguishes Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Instances, Operator Agent responsibilities, Execution Adapter behavior, and Houmao-specific implementation details

#### Scenario: Future work is not documented as current behavior
- **WHEN** docs mention roadmap features such as Operator Agent handoff normalization, GUI Backend, View Manifests, Service Requests, Gates, or full research records
- **THEN** the docs identify whether the feature is implemented, partially implemented, or planned

### Requirement: isomer-cli Command Reference
The system SHALL document every public `isomer-cli` command with purpose, prerequisites, side effects, common examples, and JSON/text output posture.

#### Scenario: CLI command coverage is checked
- **WHEN** documentation validation runs
- **THEN** every public command exposed by `isomer-cli --help` and documented command groups is represented in the CLI reference, or the validation reports the missing command

#### Scenario: Side effects are explicit
- **WHEN** a documented command can mutate Project files, Workspace Runtime records, adapter manifests, generated launch material, or live Houmao-managed agents
- **THEN** the command reference states the mutation boundary before or alongside the command example

#### Scenario: Read-only commands are identified
- **WHEN** a documented command is read-only
- **THEN** the command reference states that it does not create Workspace Runtime state, Agent Workspaces, launch material, or live Houmao state

### Requirement: Intended Usage Workflows
The system SHALL document operator-oriented workflows for the current supported paths through Project setup, validation, runtime preparation, team profile work, Agent Team Instance records, Houmao materialization, quick launch, inspection, stop, reconciliation, and adoption.

#### Scenario: Minimal project workflow is documented
- **WHEN** a new user follows the getting-started guide
- **THEN** the guide shows how to initialize a Project, inspect or validate it, resolve context, preview paths, initialize Workspace Runtime, prepare readiness, and create an Agent Team Instance without launching agents

#### Scenario: Houmao quick launch workflow is documented
- **WHEN** a user needs Isomer to launch a Houmao-backed Agent Team Instance
- **THEN** the docs explain the quick launch command sequence, preflight expectations, generated manifests, command payload records, live inspection, stop behavior, and validation checks

#### Scenario: Manual Houmao workflow is documented
- **WHEN** a user wants to inspect or edit Houmao launch material before invoking Houmao directly
- **THEN** the docs explain prepare-only materialization, manual `houmao-mgr` operation, direct edit drift detection, reconciliation, and explicit adoption

### Requirement: Assumptions and Non-goals Documentation
The system SHALL document current assumptions, side-effect boundaries, security posture, adapter boundaries, and non-goals so readers do not infer unsupported guarantees.

#### Scenario: Filesystem and workspace assumptions are documented
- **WHEN** a reader opens assumptions documentation
- **THEN** it states that Agent Workspace and Workspace Boundary semantics are advisory and do not provide filesystem-grade isolation

#### Scenario: Houmao adapter assumptions are documented
- **WHEN** a reader opens assumptions documentation or Houmao adapter documentation
- **THEN** it states that Houmao is invoked through the public CLI JSON boundary and that Houmao internals remain adapter-specific unless accepted domain language promotes a term

#### Scenario: Repair and setup assumptions are documented
- **WHEN** docs discuss missing dependencies, failed readiness, or environment repair
- **THEN** they explain that repair should be explicit through Service Request-style work rather than hidden inside read-only diagnostics or runtime preparation

### Requirement: Runtime Files and Manifest Documentation
The system SHALL document durable runtime files, generated adapter files, manifests, payload refs, and cache boundaries.

#### Scenario: Durable runtime paths are explained
- **WHEN** a reader opens runtime file documentation
- **THEN** it explains `state.sqlite`, runtime directories, path plans, Agent Workspaces, adapter manifest directories, command payloads, inspection snapshots, stop outcomes, and which files are durable records

#### Scenario: Adapter manifests are explained
- **WHEN** a reader opens Houmao adapter documentation
- **THEN** it explains `adapter-link.json`, `launch-material-manifest.json`, `adapter-runtime-manifest.json`, their purpose, and how reconciliation uses them

#### Scenario: Cache is not implied
- **WHEN** docs describe launch material, command payloads, inspection snapshots, stop outcomes, or adapter manifests
- **THEN** they state that these files are durable adapter records unless a later accepted contract explicitly classifies a file as disposable

### Requirement: Documentation Verification
The system SHALL provide a repository-local documentation verification path that can be run during implementation and review.

#### Scenario: Docs validation command exists
- **WHEN** contributors inspect development commands
- **THEN** there is a documented command or script for validating documentation coverage and links

#### Scenario: Docs validation checks command coverage
- **WHEN** docs validation runs
- **THEN** it checks that the CLI reference includes current public command names and reports missing or stale command names

#### Scenario: Docs validation checks canonical language posture
- **WHEN** docs validation runs
- **THEN** it checks selected docs for known stale or forbidden project terms and reports likely violations without replacing human review

