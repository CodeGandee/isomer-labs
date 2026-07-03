## ADDED Requirements

### Requirement: Topic Main Guidance Inspection
The Topic Manager skill SHALL report Topic Main Development Repository agent guidance posture during storage inspection.

#### Scenario: Storage inspection reports rule-file posture
- **WHEN** `isomer-admin-topic-mgr storage-inspect-main` inspects a usable normal non-bare `topic.repos.main`
- **THEN** it reports whether root-level `AGENTS.md` and `CLAUDE.md` exist
- **AND** it reports whether each file contains the current Isomer-managed topic-main guidance block
- **AND** it reports missing, stale, duplicated, malformed, or unknown-version guidance blocks as blockers or next actions

#### Scenario: Storage inspection remains non-destructive
- **WHEN** `storage-inspect-main` detects missing or stale topic-main guidance without an explicit repair request
- **THEN** it reports the condition and the recommended repair route
- **AND** it does not create, append, update, delete, reset, or rewrite rule files

### Requirement: Topic Main Guidance Repair Route
The Topic Manager skill SHALL provide an explicit storage-scoped route for refreshing topic-main agent guidance after topic initialization.

#### Scenario: Explicit repair refreshes guidance
- **WHEN** the operator explicitly requests topic-main agent guidance repair or refresh for an initialized topic
- **THEN** the Topic Manager resolves `topic.repos.main` through `storage-resolve`
- **AND** it creates missing root-level `AGENTS.md` or `CLAUDE.md`
- **AND** it appends or updates the Isomer-managed topic-main guidance block without changing unrelated rule-file content
- **AND** it reports changed files, guidance block version, blockers, and next action

#### Scenario: Repair blocks on unsafe repository state
- **WHEN** the resolved `topic.repos.main` is missing, not a normal Git repository, bare, corrupt, ambiguous, or otherwise unsafe for bounded rule-file mutation
- **THEN** the Topic Manager reports a blocker
- **AND** it routes canonical repository repair to `isomer-srv-topic-env-setup` when repository preparation is needed
