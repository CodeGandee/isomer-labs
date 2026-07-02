## REMOVED Requirements

### Requirement: Topic Workspace Manager Operator Skill
**Reason**: The active operator surface is renamed and broadened to `isomer-admin-topic-mgr`.
**Migration**: Replace active inventory and documentation references with `isomer-admin-topic-mgr`. Keep `isomer-admin-topic-workspace-mgr` only as a deprecated compatibility wrapper when retained.

## ADDED Requirements

### Requirement: Topic Manager Operator Skill
The operator/admin skillset SHALL include `isomer-admin-topic-mgr` as the operator surface for managing initialized Research Topics after Topic Creator handoff.

#### Scenario: Topic manager skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-mgr/` as an active operator skill folder

#### Scenario: Operator docs list topic manager
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-admin-topic-mgr`
- **AND** it describes the skill as the initialized-topic manager for storage, Topic Actors, topic agent team topology, environment mutation, environment verification, and diagnostics

#### Scenario: Operator validation covers topic manager
- **WHEN** operator skill validation runs
- **THEN** it validates the topic manager skill with frontmatter, UI metadata, local reference, workflow, scoped subcommand, output-contract, and guardrail checks

#### Scenario: Workspace manager wrapper is deprecated
- **WHEN** the operator skillset keeps `skillset/operator/isomer-admin-topic-workspace-mgr/`
- **THEN** operator validation accepts it only as a deprecated compatibility wrapper that names `isomer-admin-topic-mgr` as the replacement
- **AND** operator documentation does not present it as the active initialized-topic management surface

#### Scenario: Topic manager stays bounded
- **WHEN** the topic manager reports initialized-topic management results
- **THEN** it does not claim Research Topic initialization, research-paradigm v2 bootstrap, Agent Team Instance creation, Workspace Runtime mutation, Houmao launch, adapter launch material readiness, or runtime team readiness
