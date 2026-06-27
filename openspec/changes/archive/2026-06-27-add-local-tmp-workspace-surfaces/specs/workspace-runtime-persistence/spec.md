## ADDED Requirements

### Requirement: Runtime Validation Handles Local Tmp Surfaces
Workspace Runtime validation SHALL recognize resolved standard tmp-label paths as disposable local material and reject durable dependencies on them.

#### Scenario: Runtime validation reports durable tmp dependencies
- **WHEN** Workspace Runtime validation finds a runtime record, handoff, Artifact locator, Provenance Record, Evidence Item, Decision Record, profile output, or readiness record that depends on a resolved tmp path
- **THEN** it reports a non-durable temporary path diagnostic
- **AND** it does not treat the referring record as ready until the material is promoted to an approved durable surface

#### Scenario: Runtime validation reports tracked tmp contents
- **WHEN** Workspace Runtime validation finds tracked files under a resolved tmp path
- **THEN** it reports that tmp material must stay ignored and disposable unless the content is moved to an approved durable surface

#### Scenario: Runtime validation does not delete tmp
- **WHEN** Workspace Runtime validation finds files under a standard tmp path
- **THEN** it does not delete, move, archive, or promote those files automatically

## MODIFIED Requirements

### Requirement: Runtime Initialization Uses Semantic Surfaces
Workspace Runtime initialization SHALL create only the runtime-owned directories required by semantic resolution for the selected Topic Workspace.

#### Scenario: Runtime init may prepare topic tmp posture without durable dependency
- **WHEN** runtime initialization or an explicit materialization flow owns Topic Workspace local setup
- **THEN** it may create or validate resolved `topic.tmp` and the owning Topic Workspace root ignore rule
- **AND** it does not record tmp contents as durable runtime evidence

#### Scenario: Optional tmp surfaces are not required for minimal runtime init
- **WHEN** runtime initialization runs without repository setup, profile materialization, environment setup, or Agent Workspace setup
- **THEN** it does not require `topic.tmp`, `topic.main_repo.tmp`, or `agent.tmp` merely because those labels exist in the default layout profile

### Requirement: Agent Workspace Runtime Records Use Semantic Bindings
Agent Workspace runtime records SHALL use semantic `agent.workspace` resolution rather than hard-coded path assembly as the primary planning contract.

#### Scenario: Agent Workspace setup may prepare agent tmp posture
- **WHEN** Agent Team Instance creation or delegated Agent Workspace setup prepares an Agent Workspace for topic-local Agent Name `alice`
- **THEN** it may create or validate resolved `agent.tmp` and the Topic Main Repository ignore rule that keeps tmp material untracked
- **AND** it does not store files under `agent.tmp` as durable Agent Workspace evidence
