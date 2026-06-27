## MODIFIED Requirements

### Requirement: System Design Documentation
The system SHALL document the current Isomer Labs architecture using canonical domain language and explicit state ownership boundaries.

#### Scenario: Core state ownership is explained
- **WHEN** a reader opens the system design documentation
- **THEN** it explains how Project, Project Config Directory, Project Manifest, Research Topic Config, Topic Workspace, Workspace Runtime, Topic Main Repository, Agent Workspace, owner-preserved records, and adapter-generated files relate to each other

#### Scenario: Worker visibility boundary is explained
- **WHEN** a reader opens the system design documentation
- **THEN** it distinguishes worker-visible Git surfaces under `repos/topic-main` and `agents/<agent-name>` from root `records/*`, `runtime/`, `state.sqlite`, and Project config surfaces

#### Scenario: Execution layers are separated
- **WHEN** a reader opens the system design documentation
- **THEN** it distinguishes Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Instances, Operator Agent responsibilities, Execution Adapter behavior, and Houmao-specific implementation details

#### Scenario: Future work is not documented as current behavior
- **WHEN** docs mention roadmap features such as Operator Agent handoff normalization, GUI Backend, View Manifests, Service Requests, Gates, or full research records
- **THEN** the docs identify whether the feature is implemented, partially implemented, or planned

### Requirement: Runtime Files and Manifest Documentation
The system SHALL document durable runtime files, generated adapter files, manifests, payload refs, topic-owner records, worker-visible Git surfaces, and cache boundaries.

#### Scenario: Durable runtime paths are explained
- **WHEN** a reader opens runtime file documentation
- **THEN** it explains `state.sqlite`, `records/*`, `runtime/`, path plans, Agent Workspaces, adapter manifest directories, command payloads, inspection snapshots, stop outcomes, and which files are durable records

#### Scenario: Topic-main paths are explained
- **WHEN** a reader opens runtime file or Topic Workspace documentation
- **THEN** it explains that worker-visible `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, `logs/`, and `tools/` surfaces belong under `repos/topic-main` or per-agent worktrees when the topic needs them

#### Scenario: Adapter manifests are explained
- **WHEN** a reader opens Houmao adapter documentation
- **THEN** it explains `adapter-link.json`, `launch-material-manifest.json`, `adapter-runtime-manifest.json`, their purpose, and how reconciliation uses them

#### Scenario: Cache is not implied
- **WHEN** docs describe launch material, command payloads, inspection snapshots, stop outcomes, adapter manifests, or owner-preserved records
- **THEN** they state that these files are durable adapter or topic-owner records unless a later accepted contract explicitly classifies a file as disposable
