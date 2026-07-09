## ADDED Requirements

### Requirement: Structured Record Display Contract Enforcement
Research recording create, update, validate, show, list, and repair paths SHALL enforce and expose the canonical `title` and `summary` display contract for structured records.

#### Scenario: Create rejects unsupported v1 schema
- **WHEN** a caller creates or updates a structured Research Record with a `structured-record.v1` schema ref or v1-backed Artifact Format Profile
- **THEN** the recording path rejects the write with an unsupported-schema diagnostic
- **AND** it directs callers to the supported v2 display contract

#### Scenario: Create rejects missing display fields
- **WHEN** a caller creates or updates a structured Research Record with a supported v2 Artifact Format Profile
- **THEN** the recording path rejects payloads that lack non-empty top-level `title` or `summary`
- **AND** the returned diagnostic identifies the missing display field and payload source

#### Scenario: Validation reports existing display drift
- **WHEN** a caller validates existing structured Research Records
- **THEN** validation reports records with missing `title`, missing `summary`, empty display fields, duplicated `title` and `summary`, or legacy-only display aliases
- **AND** validation does not mutate records unless an explicit repair apply action is requested

#### Scenario: Show and list expose canonical fields
- **WHEN** a caller lists or shows structured Research Records through CLI or Python APIs
- **THEN** each record summary uses the canonical `title` and `summary` fields
- **AND** the response does not expose `one_liner` as a first-class display field

#### Scenario: Repair previews display migration
- **WHEN** repair code can derive a missing `summary` from legacy `one_liner` or other existing data
- **THEN** the repair preview names the source field, target field, affected record, and whether the proposal is exact
- **AND** the repair apply path writes `summary` as durable data rather than relying on future read-time conversion

### Requirement: Research Idea Display Contract Enforcement
Research recording paths that create or maintain canonical Research Ideas SHALL write `summary` instead of `one_liner`.

#### Scenario: Idea write stores summary
- **WHEN** an operator, agent, import path, repair path, or record-write convenience creates or updates a canonical Research Idea
- **THEN** the stored idea has non-empty `title` and `summary`
- **AND** no normal write API requires or returns `one_liner`

#### Scenario: Idea display migration is bounded
- **WHEN** legacy idea data contains `one_liner`
- **THEN** only migration, validation, or repair code reads that legacy value
- **AND** normal GUI, CLI, and API read paths read the stored `summary` value directly

### Requirement: Clean Summary Persistence
Workspace Runtime persistence SHALL store canonical idea display text in `summary` columns rather than retaining `one_liner` as an ignored live column.

#### Scenario: Runtime idea table uses summary
- **WHEN** Workspace Runtime schema migration completes for `research_ideas`
- **THEN** the canonical table has a `summary` column used by normal runtime reads and writes
- **AND** normal runtime code does not read or write a live `one_liner` column

#### Scenario: Idea facet table uses summary
- **WHEN** Workspace Runtime schema migration completes for query-index idea facets
- **THEN** the canonical facet table has a `summary` column used by normal query-index reads and writes
- **AND** normal query-index code does not read or write a live `one_liner` column
