## ADDED Requirements

### Requirement: Workspace Manager Owns Topic Actor Management
The Topic Workspace Manager skill SHALL manage Topic Actor CRUD and Topic Actor Workspace materialization as Topic Workspace topology operations.

#### Scenario: Actor CRUD uses workspace manager
- **WHEN** a user or operator asks to list, show, register, update, archive, materialize, repair, or diagnose Topic Actors
- **THEN** the Topic Workspace Manager performs or guides the operation through the `project topic-actors ...` CLI surface
- **AND** it updates Topic Workspace Manifest actor bindings as the actor topology authority

#### Scenario: Topic Actor binding records worker identity
- **WHEN** the Topic Workspace Manager registers a manually controlled worker for a Research Topic
- **THEN** the binding records a path-safe `topic_actor_name`, actor kind, runtime kind, role kind, controller ref or controller kind, default cwd label, optional workspace label, optional workspace path, optional branch, optional adapter ref, status, and provenance metadata

#### Scenario: Topic Actor field values are bounded but extensible
- **WHEN** the Topic Workspace Manager validates actor kind, runtime kind, role kind, controller kind, or status
- **THEN** it accepts the core values defined by the Topic Actor binding contract and accepts extension values under `custom.*`
- **AND** it rejects unknown non-extension values with a deterministic diagnostic

#### Scenario: Topic Actor registration is audited when runtime is available
- **WHEN** Topic Actor registration or materialization mutates the Topic Workspace and Workspace Runtime is initialized
- **THEN** the Topic Workspace Manager records a Workspace Runtime mutation or provenance audit record for the operation
- **AND** the Topic Workspace Manifest remains the topology and path-resolution authority for the actor binding

#### Scenario: Mixed runtimes are accepted
- **WHEN** the Topic Workspace Manager registers Topic Actors backed by Claude Code, Codex, Houmao, shell sessions, or another supported runtime kind
- **THEN** the workflow allows them to coexist in the same Topic Workspace when each actor has a distinct topic-local name and workspace binding

### Requirement: Workspace Manager Materializes Topic Actor Workspaces
The Topic Workspace Manager skill SHALL prepare separate Topic Actor Workspaces for Topic Actors that need independent development surfaces.

#### Scenario: Actor workspace worktree is created from topic-main
- **WHEN** the operator asks to create or repair a Topic Actor Workspace
- **THEN** the Topic Workspace Manager uses the resolved `topic.repos.main` repository as the Git anchor, resolves `topic.actors.workspace` for the selected Topic Actor, and prepares a worktree at the Topic Actor Workspace path
- **AND** the default branch uses the `per-topic-actor/<topic-actor-name>/main` namespace

#### Scenario: Alternate worktree sources are out of scope
- **WHEN** the user requests a Topic Actor Workspace worktree anchored from a repository other than `topic.repos.main`
- **THEN** the Topic Workspace Manager reports that alternate source repositories are unsupported in this change
- **AND** it does not create an ad hoc worktree from the alternate source

### Requirement: Workspace Manager Supports Actor Diagnostics
The Topic Workspace Manager skill SHALL support diagnostics and topology inspection for Topic Actor Workspaces without becoming the canonical creator of topic-main, topic env readiness, or research records.

#### Scenario: Actor diagnostics report resolved surfaces
- **WHEN** the Topic Workspace Manager skill is invoked for a human-orchestrated research topic
- **THEN** it reports the selected Topic Workspace, `topic.repos.main`, Topic Actor roster, Topic Actor Workspace paths, formal Agent Workspace paths when present, Isomer-managed namespace posture, research record labels, optional projection roots, blockers, and next actions
- **AND** it identifies which surfaces are authoritative records, Git anchors, actor work surfaces, formal agent work surfaces, or local temporary surfaces

#### Scenario: Manager does not replace setup services
- **WHEN** actor diagnostics find missing topic-main readiness, topic env readiness, research record labels, or Topic Actor Workspace readiness
- **THEN** the manager reports the missing evidence and routes repair to the common topic preparation workflow, Topic Workspace environment setup, Topic Actor management workflow, or research workspace bootstrap
- **AND** it does not claim canonical readiness by creating substitute files outside those workflows
