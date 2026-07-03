## ADDED Requirements

### Requirement: Worker Output Root Path Resolution
Workspace Path Resolution SHALL resolve Topic Actor and Agent worker output roots using deterministic precedence and selector-aware context.

#### Scenario: Topic Actor output root resolves with actor context
- **WHEN** a caller resolves a Topic Actor worker output root
- **THEN** the resolver requires an explicit Topic Actor selector or cwd-derived Effective Topic Actor Context
- **AND** the resolved path is under the selected Topic Actor Workspace

#### Scenario: Agent output root resolves with agent context
- **WHEN** a caller resolves an Agent worker output root
- **THEN** the resolver requires an explicit Agent selector, Agent Instance selector, or cwd-derived Effective Agent Context
- **AND** the resolved path is under the selected Agent Workspace

#### Scenario: Configured output root overrides default
- **WHEN** a worker has a valid configured output root
- **THEN** Workspace Path Resolution returns the configured root before falling back to the built-in default path

#### Scenario: Default output root is conflict-safe
- **WHEN** no configured output root exists for a selected worker
- **THEN** Workspace Path Resolution returns the built-in default root under `isomer-managed/worker-output/`
- **AND** the default root includes the worker kind and worker name

#### Scenario: Read-only path queries do not create output roots
- **WHEN** a caller queries a worker output root through a read-only path or output-policy command
- **THEN** the command returns the effective path and source metadata without creating directories

### Requirement: Worker Output Policy Query
The CLI SHALL expose an agent-readable query that returns the resolved worker output root together with the effective `commit_after_operation` preference.

#### Scenario: Query returns path and policy
- **WHEN** a caller asks for a selected worker's output policy
- **THEN** the response includes the absolute output root path, worker-relative output root path, selected worker identity, source metadata, suggested operation-set pattern, and effective `commit_after_operation`

#### Scenario: Query reports Git ignore authority
- **WHEN** the output-policy query returns file tracking guidance
- **THEN** it states that `.gitignore` and Git status control whether output files are tracked or committable
- **AND** it does not return a separate Isomer tracking policy as the authority for file tracking

#### Scenario: Query fails on ambiguous worker context
- **WHEN** a caller asks for output policy without enough Topic Actor or Agent context to select one worker
- **THEN** the command reports a diagnostic and does not guess from sibling workspace directories

### Requirement: Worker Output Path Plans
Workspace Runtime SHALL record worker output root path plans when worker setup or dependent runtime records rely on those paths.

#### Scenario: Topic Actor output path plan is recorded
- **WHEN** Topic Actor materialization prepares a worker output root
- **THEN** Workspace Runtime records the selected semantic label, scope, worker identity, canonical path, and source metadata before dependent actor support records use that path

#### Scenario: Agent output path plan is recorded
- **WHEN** Agent Workspace setup prepares a worker output root
- **THEN** Workspace Runtime records the selected semantic label, scope, worker identity, canonical path, and source metadata before dependent Agent Workspace records use that path

#### Scenario: Historical output path plans are preserved
- **WHEN** a later manifest change would resolve a different output root for an existing worker
- **THEN** validation reports drift against historical path plans without silently rewriting prior dependent records
