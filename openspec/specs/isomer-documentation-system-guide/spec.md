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

### Requirement: isomer-cli Command Reference
The system SHALL document every public `isomer-cli` command with purpose, prerequisites, side effects, common examples, and JSON/text output posture.

#### Scenario: CLI command coverage is checked
- **WHEN** documentation validation runs
- **THEN** every public command exposed by `isomer-cli --help` and documented command groups is represented in the CLI reference, or the validation reports the missing command

#### Scenario: Global JSON mode is documented
- **WHEN** a reader opens the CLI reference
- **THEN** it documents root-level `--print-json` as the canonical JSON output switch and does not present command-local `--json` or `--format json` as normal usage

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

### Requirement: Semantic Workspace Path Documentation
The documentation SHALL explain that semantic surface labels are the workspace path contract and default directories are one layout profile.

#### Scenario: Topic Workspace Manifest is documented
- **WHEN** a reader opens Topic Workspace or runtime file documentation
- **THEN** the docs explain the Topic Workspace Manifest, its standard path, its topic-owned role, and its relationship to the Project Manifest

#### Scenario: Semantic labels are documented
- **WHEN** docs describe Topic Workspace and Agent Workspace paths
- **THEN** they name semantic labels such as `topic.repos.main`, `topic.records.artifacts`, `agent.workspace`, `agent.private_artifacts`, `agent.public_share`, and `agent.scratch`

#### Scenario: Default layout is described as a profile
- **WHEN** docs show `repos/topic-main`, `records/*`, `runtime/*`, or `agents/<agent-name>`
- **THEN** they describe those paths as the `isomer-default.v1` bindings rather than the only valid contract

#### Scenario: Directory meanings stay readable
- **WHEN** docs describe directory meanings for the default layout
- **THEN** they use Markdown nested lists or equivalent prose instead of relying on a table as the only representation

### Requirement: Semantic Path CLI Documentation
The documentation SHALL describe the CLI commands that query and materialize semantic paths.

#### Scenario: Path get is documented
- **WHEN** a reader opens the `isomer-cli` reference
- **THEN** it explains how to query one semantic label with `project paths get <semantic-label>`

#### Scenario: Path list is documented
- **WHEN** a reader opens the `isomer-cli` reference
- **THEN** it explains how to list known semantic labels and their resolution status with `project paths list`

#### Scenario: Materialization is documented as mutating
- **WHEN** docs describe default semantic directory creation
- **THEN** they document the explicit materialization command as mutating and keep read-only path queries separate

#### Scenario: Side effects remain explicit
- **WHEN** docs show path query commands
- **THEN** they state which commands are read-only and which commands can create manifests, directories, repositories, or worktrees

### Requirement: Cwd-derived Agent Context Documentation
The documentation SHALL explain when agent-scoped semantic path queries can omit Agent Name.

#### Scenario: Agent workspace cwd query is documented
- **WHEN** docs describe Agent Workspace operation
- **THEN** they show that an agent running inside its own Agent Workspace can query agent-scoped labels such as `agent.private_artifacts` without passing Agent Name

#### Scenario: Inference precedence is documented
- **WHEN** docs describe agent-scoped path queries
- **THEN** they explain the precedence of explicit selector, environment context, cwd-derived Agent Workspace match, and missing-context diagnostic

#### Scenario: Topic Main Repository does not infer agent
- **WHEN** docs describe cwd-derived agent inference
- **THEN** they state that cwd inside the Topic Main Repository owner checkout does not identify an Agent Workspace

#### Scenario: Inference is not access control
- **WHEN** docs describe cwd-derived agent context
- **THEN** they state that it is a convenience for path resolution and not filesystem-grade identity, isolation, or access control

### Requirement: Documentation Verification for Semantic Paths
The documentation verification path SHALL detect stale wording that treats default paths as the only workspace contract or treats tmp material as shared, durable, or evidence-ready.

#### Scenario: Docs validation rejects durable tmp wording
- **WHEN** docs validation scans documentation that mentions `tmp/`
- **THEN** it allows the wording only when the same document names semantic labels such as `topic.tmp`, `topic.repos.main.tmp`, or `agent.tmp`
- **AND** the document states that tmp material is local, ignored, disposable, not shared, and not durable evidence

#### Scenario: Docs validation rejects fixed tmp path authority
- **WHEN** docs validation scans documentation that describes `tmp/` as the only supported path contract
- **THEN** it reports that tmp path wording must be semantic-label-first and must identify default directories as `isomer-default.v1` bindings

### Requirement: tmp Surfaces Are Documented as Downstream Labels
The documentation SHALL frame local `tmp/` surfaces as semantic labels that inherit the manifest-backed path model.

#### Scenario: Topic Workspace definition lists implemented tmp labels
- **WHEN** a reader opens the Topic Workspace definition after this change is implemented
- **THEN** it lists `topic.tmp`, `topic.repos.main.tmp`, and `agent.tmp` as Local Tmp Surface labels with local disposable meanings
- **AND** default directories are described only as `isomer-default.v1` bindings

#### Scenario: Documentation no longer calls implemented labels planned
- **WHEN** documentation describes `topic.tmp`, `topic.repos.main.tmp`, or `agent.tmp` after the semantic surface catalog supports them
- **THEN** it describes them as implemented standard labels rather than planned or future labels

#### Scenario: Documentation distinguishes tmp from sharing
- **WHEN** documentation explains worker visibility and collaboration paths
- **THEN** it states that tmp is not Peer Read Access, not a generated-link target, not owner-preserved records, and not Git-tracked collaboration material

#### Scenario: Documentation distinguishes tmp from scratch
- **WHEN** documentation explains `agent.scratch` or `isomer-managed/agent-owned/scratch/`
- **THEN** it distinguishes agent-owned draft support from root tmp disposable material

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

