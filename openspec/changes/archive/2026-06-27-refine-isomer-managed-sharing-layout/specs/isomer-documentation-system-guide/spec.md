## MODIFIED Requirements

### Requirement: System Design Documentation
The system SHALL document the current Isomer Labs architecture using canonical domain language and explicit state ownership boundaries.

#### Scenario: Core state ownership is explained
- **WHEN** a reader opens the system design documentation
- **THEN** it explains how Project, Project Config Directory, Project Manifest, Research Topic Config, Topic Workspace, Topic Main Repository, `isomer-managed/`, Workspace Runtime, Agent Workspace, and adapter-generated files relate to each other

#### Scenario: Worker visibility boundary is explained
- **WHEN** a reader opens the system design documentation
- **THEN** it explains that worker agents normally operate from `agents/<agent-name>` and use Git branches, `isomer-managed/` shares or projections, and topic-owned Pixi tasks rather than browsing root owner-preserved directories as normal input

#### Scenario: Execution layers are separated
- **WHEN** a reader opens the system design documentation
- **THEN** it distinguishes Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Instances, Operator Agent responsibilities, Execution Adapter behavior, and Houmao-specific implementation details

#### Scenario: Future work is not documented as current behavior
- **WHEN** docs mention roadmap features such as Operator Agent handoff normalization, GUI Backend, View Manifests, Service Requests, Gates, or full research records
- **THEN** the docs identify whether the feature is implemented, partially implemented, or planned

### Requirement: Assumptions and Non-goals Documentation
The system SHALL document current assumptions, side-effect boundaries, security posture, adapter boundaries, and non-goals so readers do not infer unsupported guarantees.

#### Scenario: Filesystem and workspace assumptions are documented
- **WHEN** a reader opens assumptions documentation
- **THEN** it states that Agent Workspace, Workspace Boundary, Peer Read Access, `isomer-managed/` owner/reader split, and generated-link semantics are advisory and do not provide filesystem-grade isolation

#### Scenario: Houmao adapter assumptions are documented
- **WHEN** a reader opens assumptions documentation or Houmao adapter documentation
- **THEN** it states that Houmao is invoked through the public CLI JSON boundary and that Houmao internals remain adapter-specific unless accepted domain language promotes a term

#### Scenario: Repair and setup assumptions are documented
- **WHEN** docs discuss missing dependencies, failed readiness, or environment repair
- **THEN** they explain that repair should be explicit through Service Request-style work rather than hidden inside read-only diagnostics or runtime preparation

### Requirement: Runtime Files and Manifest Documentation
The system SHALL document durable runtime files, generated adapter files, manifests, payload refs, Isomer-managed worker-facing paths, and cache boundaries.

#### Scenario: Durable runtime paths are explained
- **WHEN** a reader opens runtime file documentation
- **THEN** it explains `state.sqlite`, root runtime directories, path plans, Agent Workspaces, `isomer-managed/` tracked and untracked worker-facing paths, adapter manifest directories, command payloads, inspection snapshots, stop outcomes, and which files are durable records

#### Scenario: Adapter manifests are explained
- **WHEN** a reader opens Houmao adapter documentation
- **THEN** it explains `adapter-link.json`, `launch-material-manifest.json`, `adapter-runtime-manifest.json`, their purpose, and how reconciliation uses them

#### Scenario: Cache is not implied
- **WHEN** docs describe launch material, command payloads, inspection snapshots, stop outcomes, adapter manifests, or untracked `isomer-managed/` shares
- **THEN** they state that these files are durable adapter records only when the relevant path plan, Artifact locator, or Provenance Record classifies them as durable rather than cache-like generated material

### Requirement: Documentation Verification
The system SHALL provide a repository-local documentation verification path that can be run during implementation and review.

#### Scenario: Docs validation command exists
- **WHEN** contributors inspect development commands
- **THEN** there is a documented command or script for validating documentation coverage and links

#### Scenario: Docs validation checks command coverage
- **WHEN** docs validation runs
- **THEN** it checks that the CLI reference includes current public command names and reports missing or stale command names

#### Scenario: Docs validation checks stale JSON examples
- **WHEN** docs validation runs after this change
- **THEN** it reports stale Isomer CLI examples that use command-local `--json` or `--format json` instead of root-level `--print-json`

#### Scenario: Docs validation checks canonical language posture
- **WHEN** docs validation runs
- **THEN** it checks selected docs for known stale or forbidden project terms and reports likely violations without replacing human review

#### Scenario: Docs validation checks legacy workspace paths
- **WHEN** docs validation runs after this change
- **THEN** it reports `.isomer-agent/` and top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` guidance outside migration notes as stale workspace layout language

## ADDED Requirements

### Requirement: Topic Workspace Definition Documentation
The system SHALL keep `docs/topic-workspace-definition.md` as the canonical documentation page for Topic Workspace and Agent Workspace filesystem structure.

#### Scenario: Standard layout shows isomer-managed namespace
- **WHEN** a reader opens `docs/topic-workspace-definition.md`
- **THEN** the standard layout shows `repos/topic-main/isomer-managed/` and the tracked, agent-owned, topic-owned, and generated-link subtrees with comments explaining their meanings

#### Scenario: Legacy support root is absent from current layout
- **WHEN** `docs/topic-workspace-definition.md` describes the current standard Agent Workspace internal layout
- **THEN** it does not present `.isomer-agent/` as the current support root

#### Scenario: Three sharing regimes are explained
- **WHEN** `docs/topic-workspace-definition.md` explains `isomer-managed/`
- **THEN** it distinguishes Git-tracked Isomer-injected material, untracked agent-owned material with owner/reader split, and untracked topic-owned material projected to agents

#### Scenario: Communication channels are updated
- **WHEN** `docs/topic-workspace-definition.md` describes Agent Communication Channels
- **THEN** it lists Git branch exchange as primary, `isomer-managed/` untracked shares and projections as secondary for large or temporary material, and topic-owned Pixi tasks as the structured tool/API channel

#### Scenario: Migration guidance is non-destructive
- **WHEN** `docs/topic-workspace-definition.md` mentions legacy `.isomer-agent/` or top-level `topic-main` Isomer directories
- **THEN** it frames them as migration diagnostics and states that Isomer must not delete or move user files without explicit operator instruction
