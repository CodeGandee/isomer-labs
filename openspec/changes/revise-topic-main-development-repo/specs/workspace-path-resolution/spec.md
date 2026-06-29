## ADDED Requirements

### Requirement: Topic Main Projection Path Resolution
Workspace Path Resolution SHALL resolve Topic Main Development Repository projection labels as built-in topic-scoped surfaces derived from the resolved `topic.repos.main` path.

#### Scenario: Projection roots resolve under custom topic-main
- **WHEN** `topic.repos.main` resolves to a safe custom existing repository path
- **THEN** `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, and `topic.repos.main.projections.manifest` resolve under that repository's `isomer-managed/` namespace
- **AND** the response reports semantic label, resolved path, source, source detail, storage profile, and storage-profile traits

#### Scenario: Projection roots are not grouped repository labels
- **WHEN** Workspace Path Resolution receives a fixed projection label under `topic.repos.main.projections.*`
- **THEN** it resolves the built-in projection surface
- **AND** it does not create or infer a dynamic grouped `topic.repos.*` repository surface for that label

#### Scenario: Unknown topic-main sublabel blocks
- **WHEN** Workspace Path Resolution receives an unsupported label under `topic.repos.main.*`
- **THEN** it reports an unknown or reserved label diagnostic
- **AND** it does not guess a filesystem path

### Requirement: Projection Evidence Output
Workspace Path Resolution and path preview outputs SHALL expose enough projection-root evidence for setup services to report external repo projection readiness.

#### Scenario: Preview includes projection labels
- **WHEN** a path preview includes standard Topic Main Development Repository surfaces
- **THEN** it includes the read-only projection root, writable projection root, and projection manifest label when the selected catalog supports them

#### Scenario: Path plans keep projection traits
- **WHEN** a runtime or service record stores a path plan for a projection root or projection manifest
- **THEN** the stored plan includes the semantic label, compatibility surface, storage profile, storage-profile traits, and source metadata

### Requirement: Breaking Path Compatibility
Workspace Path Resolution SHALL not preserve deprecated generated Topic Workspace internal paths as compatibility fallbacks for this layout revision.

#### Scenario: Old projection path does not resolve by default
- **WHEN** a caller asks for an old external projection path or an old top-level `repos/topic-main/extern/...` convention
- **THEN** the resolver does not synthesize that path as a supported default
- **AND** callers must use the revised projection labels or recreate generated topic content
