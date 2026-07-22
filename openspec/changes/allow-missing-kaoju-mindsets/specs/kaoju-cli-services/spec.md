## MODIFIED Requirements

### Requirement: Project Run Commands Persist Resumable Stages
The CLI SHALL provide `project runs begin`, `resolve-mindset`, `checkpoint`, `status`, and `complete` for bounded Research Task attempts.

#### Scenario: Run begins
- **WHEN** a pipeline procedure starts for a Research Task
- **THEN** `begin` records procedure id, control mode, actors, normalized input refs, expected output semantics, scheduler and Gate policy refs, and initial stage

#### Scenario: Recorded mindset resolution is persisted
- **WHEN** a caller invokes `resolve-mindset` with one applicable key and a Run-scoped `KAOJU:MINDSET-RECORD` ref
- **THEN** the service verifies the Record semantic id, Run scope, and snapshotted key, stores disposition `recorded`, and appends the Record ref to Run inputs
- **AND** fresh `status` output reports Source status `present`, Record status `available`, and the Record ref

#### Scenario: Missing mindset resolution is persisted
- **WHEN** a caller invokes `resolve-mindset` with one applicable key and `--source-missing`
- **THEN** the service resolves the deterministic Source path, verifies that no file exists, and stores disposition `skipped_source_missing`, Source status `missing`, Record status `absent`, and reason `source_missing`
- **AND** it creates no Source, placeholder ref, or Mindset Record

#### Scenario: Missing posture is claimed for an existing file
- **WHEN** `resolve-mindset --source-missing` finds any file at the deterministic selected Source path
- **THEN** the operation fails without changing Run state and directs the caller to validate or repair the existing file
- **AND** unreadable or invalid is not normalized to missing

#### Scenario: Mindset resolution is retried or changed
- **WHEN** a Run already has a mindset resolution
- **THEN** an exact repeat succeeds idempotently
- **AND** a different key, disposition, or Record ref fails without replacing the original resolution

#### Scenario: Run checkpoints
- **WHEN** a durable stage completes or pauses
- **THEN** `checkpoint` records stage id, output refs, pending Gate, blocker or Service Request refs, stage status, observations, and resume hint while preserving the mindset resolution
- **AND** the update is visible through fresh Workspace Runtime state

#### Scenario: Run completes
- **WHEN** the bounded procedure reaches a terminal state
- **THEN** `complete` records `complete`, `paused`, or `blocked`, exact output refs, unresolved items, resource observations, resume posture, and the preserved mindset resolution
- **AND** it does not start another macro procedure
