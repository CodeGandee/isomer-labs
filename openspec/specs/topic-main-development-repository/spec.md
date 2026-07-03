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

### Requirement: Topic Main Anchors Topic Actor Workspace Worktrees
The system SHALL define `topic.repos.main` as the topic-owned Git anchor and integration surface for Topic Actor Workspace worktrees.

#### Scenario: Actor workspace worktree uses topic-main as source
- **WHEN** human-orchestrated preparation creates a Topic Actor Workspace worktree
- **THEN** the worktree is attached to the resolved `topic.repos.main` repository

#### Scenario: Alternate source repositories are rejected
- **WHEN** a user requests a Topic Actor Workspace worktree from a source other than `topic.repos.main`
- **THEN** the workflow reports the request as unsupported in this change
- **AND** it does not treat a custom source policy or ad hoc Git path as accepted

#### Scenario: Topic-main is not the universal actor cwd
- **WHEN** more than one Topic Actor is prepared for a Research Topic
- **THEN** operator-facing output gives each actor its resolved Topic Actor Workspace cwd rather than directing all actors to run from `topic.repos.main`
- **AND** `topic.repos.main` remains available for integration, review, and direct operator work

#### Scenario: Work surface is not durable record authority
- **WHEN** a Topic Actor creates source code, notebooks, draft files, logs, or figures in a Topic Actor Workspace or `topic.repos.main`
- **THEN** those files remain editable work-surface material until the actor records or links the accepted artifact through Topic Workspace research records
- **AND** the system does not treat a repo path alone as an accepted durable Artifact, Evidence Item, Run, Decision Record, or package record

#### Scenario: Tracked support material stays small
- **WHEN** preparation writes worker-facing support material under `topic.repos.main.isomer_managed` or a Topic Actor Workspace Isomer-managed namespace
- **THEN** the material is limited to small coordination files, pointer manifests, bootstrap notes, start packs, or boundary documents
- **AND** large outputs and accepted research artifacts are directed to Topic Workspace records

### Requirement: Tracked Topic Main Agent Rule Files
The system SHALL treat root-level `AGENTS.md` and `CLAUDE.md` in Topic Main Development Repository as tracked worker-facing guidance files.

#### Scenario: Topic main has rule files
- **WHEN** Topic Workspace environment setup prepares `topic.repos.main`
- **THEN** the repository contains root-level `AGENTS.md` and `CLAUDE.md`
- **AND** those files are normal topic-main files eligible for Git tracking
- **AND** they are not placed under `topic.repos.main.isomer_managed`, tmp paths, runtime paths, or external projection roots

#### Scenario: Existing repository content is not overwritten
- **WHEN** `topic.repos.main` already contains `AGENTS.md` or `CLAUDE.md`
- **THEN** Isomer preserves existing content outside the Isomer-managed guidance block
- **AND** Isomer does not reorder, normalize, delete, or rewrite unrelated rule-file sections

### Requirement: Isomer-Managed Topic Main Guidance Block
The system SHALL store Isomer-specific topic-main guidance in a fenced block with stable markers so the block can be updated idempotently.

#### Scenario: Guidance block uses stable boundaries
- **WHEN** Isomer writes topic-main guidance into `AGENTS.md` or `CLAUDE.md`
- **THEN** the guidance is bounded by `<!-- BEGIN isomer-labs-topic-main-guidance v1 -->` and `<!-- END isomer-labs-topic-main-guidance v1 -->`
- **AND** the guidance body is stored in a fenced block tagged `isomer-labs-topic-main-guidance`

#### Scenario: Guidance block is not duplicated
- **WHEN** Isomer updates `AGENTS.md` or `CLAUDE.md` and the file already contains a recognized Isomer-managed topic-main guidance block
- **THEN** Isomer updates the recognized block in place
- **AND** it does not append a duplicate block

#### Scenario: Guidance block avoids topic-specific values
- **WHEN** Isomer writes the topic-main guidance block
- **THEN** the block does not contain concrete Research Topic ids, topic statements, Topic Workspace paths, Topic Actor names, Agent Names, runtime file paths, credentials, external repository paths, resolved `manifest_path`, or resolved `pixi_environment`
- **AND** the block points agents to `isomer-cli` queries for those values

### Requirement: Topic Main Guidance Source of Truth
The system SHALL treat the `isomer-cli project topic-main-guidance` renderer, backed by a packaged `.j2` template asset, as the source of truth for root `AGENTS.md` and `CLAUDE.md` Isomer guidance in Topic Main Development Repository.

#### Scenario: Rule files use CLI-rendered content
- **WHEN** Topic Workspace environment setup or Topic Manager repair writes topic-main agent guidance
- **THEN** the written block is produced by `isomer-cli project topic-main-guidance` behavior
- **AND** skill documentation does not own a separate full copy of the guidance prose

#### Scenario: Template remains topic independent
- **WHEN** the packaged guidance template is rendered
- **THEN** rendered content contains placeholders or command forms for `manifest_path`, `pixi_environment`, and semantic labels
- **AND** rendered content does not contain concrete selected-topic values

#### Scenario: Topic main stores rendered files only
- **WHEN** root `AGENTS.md` or `CLAUDE.md` contains the Isomer-managed guidance block
- **THEN** the repository stores rendered Markdown files
- **AND** the canonical editable template remains in the installed Isomer package assets, not inside the Topic Main Development Repository

