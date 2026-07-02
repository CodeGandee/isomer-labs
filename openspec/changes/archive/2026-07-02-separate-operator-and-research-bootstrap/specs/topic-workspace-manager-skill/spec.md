## ADDED Requirements

### Requirement: Topic Workspace Manager Excludes Research Bootstrap
The Topic Workspace Manager SHALL remain responsible for Topic Workspace topology, Topic Actor CRUD, materialization, repair, archive, and actor-scoped path diagnostics without owning research-paradigm bootstrap or handoff records.

#### Scenario: Actor management avoids research records
- **WHEN** `isomer-admin-topic-workspace-mgr manage-actors` registers, updates, materializes, repairs, diagnoses, or archives Topic Actors
- **THEN** it reports actor topology, actor workspaces, branches, support labels, audit refs when available, blockers, and repair routes
- **AND** it does not create research records, v2 placeholder registries, v2 bootstrap outputs, or accepted research artifact instructions

#### Scenario: Topic workspace summary stays topology scoped
- **WHEN** `isomer-admin-topic-workspace-mgr summarize` reports Topic Actor readiness
- **THEN** it reports actor-scoped semantic paths, branch posture, support labels, tmp posture, boundary material, validation status, blockers, and next operator action
- **AND** it does not claim research-paradigm readiness or v2 bootstrap readiness
