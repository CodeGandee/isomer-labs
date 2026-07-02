## ADDED Requirements

### Requirement: V2 Research Workspace Manager Owns V2 Bootstrap
The v2 research-paradigm skillset SHALL make `isomer-rsch-workspace-mgr-v2` the owner of v2-specific research workspace bootstrap.

#### Scenario: V2 bootstrap consumes operator readiness
- **WHEN** `isomer-rsch-workspace-mgr-v2` prepares v2 research workspace readiness for a Topic Workspace
- **THEN** it consumes Topic Workspace and Topic Actor readiness evidence produced by operator skills as input
- **AND** it does not require operator skills to validate selected v2 skills, v2 placeholder binding files, v2 placeholder binding registries, or accepted research artifact command shapes

#### Scenario: V2 bootstrap reports research recording guidance
- **WHEN** `isomer-rsch-workspace-mgr-v2` completes v2 bootstrap
- **THEN** it reports selected v2 skill readiness, placeholder binding entrypoints, research storage or record guidance, actor access plans, and accepted research artifact recording instructions when those are in scope
- **AND** it treats those outputs as research-paradigm material rather than operator Topic Actor topology material

#### Scenario: V2 actor access plan preserves actor metadata
- **WHEN** v2 bootstrap includes human-orchestrated Topic Actors
- **THEN** it preserves Topic Actor names, actor kind, runtime kind, role kind, controller kind, and cwd labels from operator readiness evidence
- **AND** it adds v2-specific recording metadata only inside v2 research workspace outputs
