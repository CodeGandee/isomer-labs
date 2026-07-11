## ADDED Requirements

### Requirement: Durable Records Support Family-Neutral Semantic Ids
The research recording API and CLI SHALL support an optional `semantic_id` that identifies a durable semantic object independently of its producing skill and format profile.

#### Scenario: Create records semantic id
- **WHEN** a caller creates a durable record with `--semantic-id <family>:<semantic-id>`
- **THEN** Workspace Runtime stores that exact semantic id in record metadata and returns it through create, show, list, revision, and query responses
- **AND** structured validation checks it against the selected profile when the profile declares a semantic id

#### Scenario: Semantic id is filterable
- **WHEN** a caller lists or queries research records by exact semantic id
- **THEN** only topic-scoped records with that semantic id are returned in deterministic order
- **AND** the response preserves record kind, status, family, profile, title, summary, revision state, and content locator when known

#### Scenario: Revision preserves semantic identity
- **WHEN** a caller revises a record carrying a semantic id
- **THEN** the descendant carries the same semantic id unless the selected binding explicitly creates a different semantic object
- **AND** the prior record remains queryable through revision lineage

### Requirement: Placeholder Compatibility Remains Available
Family-neutral semantic ids SHALL be additive to the existing DeepSci placeholder contract.

#### Scenario: Existing placeholder command is unchanged
- **WHEN** a caller creates, lists, updates, revises, or shows a record using `--placeholder`
- **THEN** the command retains its existing behavior and response metadata
- **AND** no existing placeholder value or stored record is rewritten

#### Scenario: Placeholder can participate in generalized indexing
- **WHEN** the query index normalizes an existing DeepSci placeholder-backed record
- **THEN** it may expose a generalized semantic identity derived from the placeholder for cross-family query infrastructure
- **AND** it still exposes the original placeholder and does not claim that the record was authored with `--semantic-id`

