## ADDED Requirements

### Requirement: Research Template Commands Use Indexed Record Reads
The system SHALL use the topic-scoped research record query index to list and locate `kaoju:writing-template` records without materializing unrelated lifecycle records or mutating the query index.

#### Scenario: Template list uses exact indexed identity
- **WHEN** a caller runs `isomer-cli ext research templates list` for a selected Topic Workspace
- **THEN** the command queries indexed records with exact semantic id `kaoju:writing-template`
- **AND** it does not call the full lifecycle-record listing path

#### Scenario: Template list preserves its public summary
- **WHEN** indexed template rows are returned
- **THEN** the command returns the existing template identity, record id, status, venue, paper type, preview-build status, updated timestamp, and transition metadata fields when available
- **AND** it marks the template named `main` as the default

#### Scenario: Template list filters indexed metadata
- **WHEN** a caller supplies `--venue` or `--paper-type`
- **THEN** the command filters the indexed template rows by the corresponding transition metadata
- **AND** unrelated indexed records do not affect the result

#### Scenario: Named template operations use indexed lookup
- **WHEN** `show`, `refresh`, `compile`, or `remove` locates a default or named template
- **THEN** the command uses the shared indexed template lookup and active-status policy
- **AND** any canonical record detail or mutation is performed only after the indexed record identity is selected

#### Scenario: Template reads do not repair the index
- **WHEN** indexed template data is missing, stale, or inconsistent
- **THEN** a template read does not rebuild, backfill, repair, or otherwise mutate query-index rows
- **AND** available query diagnostics or rebuild guidance remain visible to the caller
