## MODIFIED Requirements

### Requirement: Topic Workspace Git Layout
The topic workspace manager skill SHALL inspect, validate, summarize, and optionally repair Git-backed Topic Workspace topology, while the canonical Topic Main Development Repository setup path belongs to Topic Workspace environment setup.

#### Scenario: Workspace resolution uses Project Manifest
- **WHEN** `resolve-workspace` runs
- **THEN** it resolves Project root, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context instead of inferring a Topic Workspace by scanning directories

#### Scenario: Shared topic repo path is semantic
- **WHEN** the skill inspects or validates the shared topic repository
- **THEN** it uses the resolved `topic.repos.main` path and reports the path source
- **AND** the default path remains `<topic-workspace-dir>/repos/topic-main` under `isomer-default.v1`

#### Scenario: Isomer-managed namespace is inside topic-main
- **WHEN** the skill inspects or validates the shared topic repository
- **THEN** the expected Isomer worker-facing namespace is the resolved `topic.repos.main.isomer_managed` path

#### Scenario: Agent worktrees are placed under resolved agent labels
- **WHEN** the skill inspects, validates, or optionally creates an Agent Workspace for agent name `alice`
- **THEN** the expected worktree path is the resolved `agent.workspace` path for `alice`

#### Scenario: Canonical main repo creation is not required from this skill
- **WHEN** topic env setup has already prepared Topic Main Development Repository predecessor evidence
- **THEN** the workspace manager uses that evidence for validation or summaries
- **AND** it does not present itself as the canonical creator of `topic.repos.main`

#### Scenario: Existing unsafe repo blocks optional topology work
- **WHEN** the resolved `topic.repos.main` exists but is not a usable Git repository for worktree inspection or creation
- **THEN** the skill reports a blocker
- **AND** it does not delete, replace, pull, or reinitialize the existing path without explicit user instruction

### Requirement: Default Layout Materialization
The topic workspace manager skill SHALL materialize default Agent Workspace topology only when the operator asks for optional topology creation and Topic Main Development Repository predecessor evidence exists or is explicitly accepted.

#### Scenario: Default main repo materialization is not canonical
- **WHEN** the operator asks this skill to create default Topic Main Development Repository material
- **THEN** the skill reports that the canonical setup path is `isomer-srv-topic-env-setup`
- **AND** it may perform only an explicitly requested manual repair or compatibility operation with mutation confirmation

#### Scenario: Default agent worktrees are explicitly created
- **WHEN** the operator asks the skill to create Agent Workspace worktrees at default locations
- **THEN** the skill creates or validates `agent.workspace` default bindings for the planned Agent Names before creating the worktrees
- **AND** it requires prepared `topic.repos.main` evidence or explicit acceptance of a manual topology operation

#### Scenario: Read-only planning does not create manifest
- **WHEN** the skill runs `resolve-workspace`, `plan-agents`, `validate-worktrees`, or `summarize` without creation intent
- **THEN** it does not create or rewrite `topic-workspace.toml`, directories, branches, or worktrees

## ADDED Requirements

### Requirement: Optional Topology Support Boundary
The topic workspace manager skill SHALL be optional support for topology inspection, branch helpers, boundary summaries, and legacy compatibility diagnostics after the breaking Topic Main Development Repository revision.

#### Scenario: Topology inspection remains supported
- **WHEN** an operator asks to inspect prepared topic-main and Agent Workspace topology
- **THEN** the skill reports semantic paths, Git state, branch namespace, worktree state, Isomer-managed layout, projection roots, generated links, blockers, and next actions without materializing missing topic env surfaces

#### Scenario: Branch helper remains supported
- **WHEN** an operator asks to create a future per-agent branch under an accepted agent branch namespace
- **THEN** the skill may perform that bounded Git helper operation after validating the prepared Topic Main Development Repository and Agent Name

#### Scenario: Legacy generated content can break
- **WHEN** the skill sees old generated `isomer-content/` internals or old topic-main support paths
- **THEN** it may report them as unsupported under the revised layout
- **AND** it does not need to provide migration instructions beyond recreating generated topic content
