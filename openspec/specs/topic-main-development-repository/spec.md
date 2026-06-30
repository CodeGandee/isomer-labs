# topic-main-development-repository Specification

## Purpose
TBD - created while bulk-archiving completed changes. Update Purpose after archive.

## Requirements

### Requirement: Topic Main Development Repository Ownership
The system SHALL define the Topic Main Development Repository as the topic-owned normal Git repository resolved by `topic.repos.main`, created, configured, and verified by Topic Workspace environment setup before Agent Workspace worktrees are materialized.

#### Scenario: Topic env setup owns main repository readiness
- **WHEN** Topic Workspace environment setup runs for a registered Research Topic
- **THEN** it creates or validates the resolved `topic.repos.main` as a normal non-bare Git repository
- **AND** it reports the repository path, source, Git state, owner branch posture, Isomer-managed namespace posture, commands run, blockers, and readiness evidence

#### Scenario: Agent env setup consumes predecessor evidence
- **WHEN** Agent Workspace environment setup needs to create or validate per-agent worktrees
- **THEN** it requires Topic Main Development Repository predecessor evidence from Topic Workspace environment setup
- **AND** it does not create, initialize, configure, or repair `topic.repos.main` as part of the normal agent env flow

#### Scenario: Existing user repository stays root-clean
- **WHEN** `topic.repos.main` resolves to an existing user-provided normal Git repository
- **THEN** Isomer-injected worker-facing material is placed under the resolved `topic.repos.main.isomer_managed` namespace
- **AND** setup does not create top-level Isomer directories or external repo directories at the repository root

### Requirement: Canonical External Repositories
The system SHALL keep third-party or supporting repositories as canonical topic repositories under semantic `topic.repos.<group...>.<repo-name>` labels, defaulting to `repos/extern/<repo-label-path>`.

#### Scenario: External repository source is semantic
- **WHEN** topic env setup needs a third-party repository
- **THEN** it resolves or registers a non-main `topic.repos.*` label for the canonical external repository
- **AND** the default target path is under `<topic-workspace>/repos/extern/...`

#### Scenario: External repository is not the main repository
- **WHEN** a non-main topic repository exists under `repos/extern/...`
- **THEN** the system treats it as canonical supporting source material
- **AND** it does not use that repository as the Git anchor for Agent Workspace worktrees

### Requirement: Topic-Main External Repository Projections
The system SHALL expose external repositories inside Topic Main Development Repository only through Isomer-managed topic-owned projection roots.

#### Scenario: Read-only projection root is used
- **WHEN** an external repository is intended to be readable by humans or agents from topic-main
- **THEN** its developer-facing projection is under `isomer-managed/topic-owned/readonly/extern/<repo-label-path>/`
- **AND** the projection is read-only by policy even when the filesystem cannot enforce read-only access

#### Scenario: Writable projection root is used
- **WHEN** an external repository is intended to be writable by humans or agents from topic-main
- **THEN** its developer-facing projection is under `isomer-managed/topic-owned/writable/extern/<repo-label-path>/`
- **AND** the projection must be a copy, dedicated clone, dedicated worktree, or another isolated writable materialization unless the user explicitly authorizes writes to the canonical external repository

#### Scenario: No top-level extern directory is created
- **WHEN** Topic Workspace environment setup projects an external repository into topic-main
- **THEN** it does not create `repos/topic-main/extern/...`
- **AND** it keeps the projection under `isomer-managed/topic-owned/{readonly,writable}/extern/...`

### Requirement: External Projection Metadata
The system SHALL record external repository projection metadata in a tracked Isomer manifest inside Topic Main Development Repository.

#### Scenario: Projection manifest is tracked
- **WHEN** topic env setup creates, updates, validates, or blocks an external repo projection
- **THEN** it records projection metadata under `isomer-managed/tracked/manifests/extern-projections.toml`
- **AND** that manifest is eligible for normal Git tracking in topic-main

#### Scenario: Projection entry is explicit
- **WHEN** a projection manifest records one external repository projection
- **THEN** the entry names the canonical source semantic label, canonical source path, projection path, intended access, projection mode, mutation policy, status, blockers, and source evidence

#### Scenario: Projection metadata is not source truth
- **WHEN** a projection manifest entry names an external repository
- **THEN** the canonical source remains the resolved `topic.repos.*` repository path
- **AND** the projection manifest records how that source is exposed inside topic-main

### Requirement: Breaking Topic Workspace Recreate Policy
The system SHALL treat this Topic Workspace layout revision as breaking and SHALL NOT preserve old generated `isomer-content/` internals.

#### Scenario: Old generated content may break
- **WHEN** existing generated Topic Workspace content uses old internal paths or old setup ownership assumptions
- **THEN** the system may report blockers or validation failures without breaking-layout diagnostics
- **AND** the accepted operator action is to recreate generated topic content under the revised layout

#### Scenario: Compatibility paths are not required
- **WHEN** implementation removes old default internal paths, old source gate paths, old projection locations, or old topic-main ownership assumptions
- **THEN** tests and docs do not require compatibility shims for those old paths
