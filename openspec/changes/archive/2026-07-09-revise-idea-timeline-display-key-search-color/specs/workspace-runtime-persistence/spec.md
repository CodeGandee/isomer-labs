## ADDED Requirements

### Requirement: Research Idea Display Key Format
Workspace Runtime SHALL assign and validate Research Idea display keys using the topic-scoped `I-<positive decimal>` format.

#### Scenario: New idea gets hyphenated display key
- **WHEN** a Research Idea is created without an explicit display key
- **THEN** Workspace Runtime assigns the next available key in the `I-<index>` format
- **AND** the key is unique within the Topic Workspace

#### Scenario: Old compact key is rejected for new writes
- **WHEN** a Research Idea write provides a display key such as `I1`
- **THEN** validation reports the key as invalid for the current display-key format
- **AND** the write does not silently remap the key

#### Scenario: Allocated keys are not reused
- **WHEN** a Research Idea display key has been allocated, archived, deleted, or tombstoned
- **THEN** later automatic allocation MUST NOT reuse that display key

### Requirement: Research Idea Display Key Explicit Migration
Workspace Runtime SHALL provide an explicit operator-invoked repair or migration path for old or missing Research Idea display keys.

#### Scenario: Existing compact keys are migrated
- **WHEN** the operator runs the explicit display-key repair or migration for a Topic Workspace containing keys such as `I1`
- **THEN** the plan rewrites them to matching `I-1` style keys when the target keys are available
- **AND** the operation reports the proposed mapping before or as part of applying it

#### Scenario: Migration rejects collisions
- **WHEN** migrating an existing key would collide with another allocated display key or tombstone
- **THEN** the migration reports a deterministic diagnostic
- **AND** it does not silently choose a different display key

#### Scenario: GUI read does not migrate keys
- **WHEN** Project Web, graph, timeline, validation, query, or export code opens Workspace Runtime in read-only mode
- **THEN** it MUST NOT create, rewrite, repair, or migrate Research Idea display keys
