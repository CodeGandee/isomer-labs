## ADDED Requirements

### Requirement: Collect subcommand catalogs external artifacts
The `imsight-llm-wiki` skill SHALL provide a `collect` subcommand that discovers and catalogs a bounded set of external artifacts matching a user query.

#### Scenario: User requests a collection
- **WHEN** the user invokes `$imsight-llm-wiki use collect to collect "<things>"`
- **THEN** the skill SHALL search the web for matching artifacts

#### Scenario: Local wiki search is not used
- **WHEN** the user invokes `collect`
- **THEN** it SHALL NOT search the existing local wiki; local content queries remain the domain of `query`

### Requirement: Collect produces a catalog page
The collect workflow SHALL produce a single `wiki/collections/<slug>.md` page containing a deduplicated table or list of collected artifacts with provenance.

#### Scenario: Collection completes
- **WHEN** the collect workflow finishes
- **THEN** it SHALL write `wiki/collections/<slug>.md` and add the entry to `wiki/index.md`

### Requirement: Collect deduplicates entries
The collect workflow SHALL detect and merge duplicate artifacts based on name, URL, or canonical identifier.

#### Scenario: Duplicate artifacts found
- **WHEN** the collect workflow encounters two artifacts referring to the same entity
- **THEN** it SHALL record one entry and note the alternate sources

### Requirement: Collect logs its operation
The collect workflow SHALL append a log entry to the current day's `log/YYYYMMDD.md`.

#### Scenario: Collection completes
- **WHEN** collect finishes
- **THEN** it SHALL append `## [HH:MM] collect | <slug> — cataloged N artifacts`
