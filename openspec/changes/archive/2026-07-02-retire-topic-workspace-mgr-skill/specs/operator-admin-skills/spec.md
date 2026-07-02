## MODIFIED Requirements

### Requirement: Topic Manager Operator Skill
The operator/admin skillset SHALL include `isomer-admin-topic-mgr` as the only operator skill surface for managing initialized Research Topics after Topic Creator handoff.

#### Scenario: Topic manager skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-mgr/` as an active operator skill folder
- **AND** it does not contain `skillset/operator/isomer-admin-topic-workspace-mgr/`

#### Scenario: Operator docs list only topic manager
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-admin-topic-mgr`
- **AND** it describes the skill as the initialized-topic manager for storage, Topic Actors, topic agent team topology, environment mutation, environment verification, and diagnostics
- **AND** it does not describe `isomer-admin-topic-workspace-mgr` as a compatibility wrapper or active fallback

#### Scenario: Operator validation covers topic manager and rejects old folder
- **WHEN** operator skill validation runs
- **THEN** it validates the topic manager skill with frontmatter, UI metadata, local reference, workflow, scoped subcommand, output-contract, and guardrail checks
- **AND** it fails if `skillset/operator/isomer-admin-topic-workspace-mgr/` exists
- **AND** it fails if active operator docs, manifests, or routing guidance present `isomer-admin-topic-workspace-mgr` as invokable

#### Scenario: Topic manager stays bounded
- **WHEN** the topic manager reports initialized-topic management results
- **THEN** it does not claim Research Topic initialization, research-paradigm v2 bootstrap, Agent Team Instance creation, Workspace Runtime mutation, Houmao launch, adapter launch material readiness, or runtime team readiness

## ADDED Requirements

### Requirement: Retired Workspace Manager Is Excluded From Operator Inventory
The operator/admin skillset SHALL exclude the retired `isomer-admin-topic-workspace-mgr` skill from active manifests, generated skill lists, and validation fixtures.

#### Scenario: Manifest excludes retired skill
- **WHEN** `skillset/manifest.toml` is inspected
- **THEN** it includes `operator/isomer-admin-topic-mgr`
- **AND** it does not include `operator/isomer-admin-topic-workspace-mgr`

#### Scenario: Validation fixtures do not recreate retired wrapper
- **WHEN** unit tests build valid operator skill fixtures
- **THEN** the fixtures include `isomer-admin-topic-mgr`
- **AND** they do not create a valid `isomer-admin-topic-workspace-mgr` wrapper fixture

#### Scenario: Revived old folder is rejected
- **WHEN** a test or real repository contains `skillset/operator/isomer-admin-topic-workspace-mgr/`
- **THEN** operator skill validation reports that the skill is retired and must not be a standalone skill
