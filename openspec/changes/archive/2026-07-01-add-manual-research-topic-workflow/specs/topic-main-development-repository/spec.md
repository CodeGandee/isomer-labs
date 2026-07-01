## ADDED Requirements

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
