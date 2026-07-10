# Purpose

Define the inventory capability of `imsight-llm-wiki`, which maintains a lightweight backlog of ingest candidates.

## Requirements

### Requirement: Inventory subcommand tracks candidates
The `imsight-llm-wiki` skill SHALL provide an `inventory` subcommand that maintains a backlog of ingest candidates.

#### Scenario: User adds a candidate
- **WHEN** the user invokes `$imsight-llm-wiki use inventory to add "<title>" --url <url>`
- **THEN** the skill SHALL create `wiki/inventory/<slug>.md` with title, URL, and status

### Requirement: Inventory lists open candidates
The inventory workflow SHALL list all candidates that have not been ingested or rejected.

#### Scenario: User lists inventory
- **WHEN** the user invokes `$imsight-llm-wiki use inventory to list`
- **THEN** the skill SHALL enumerate `wiki/inventory/*.md` files with `status: open`

### Requirement: Inventory promotes candidates to ingest
The inventory workflow SHALL support promoting a candidate through the existing `ingest` subcommand.

#### Scenario: User ingests a candidate
- **WHEN** the user invokes `$imsight-llm-wiki use inventory to ingest <slug>`
- **THEN** the skill SHALL run the ingest workflow on the candidate's URL or description and update the candidate's status to `ingested`

### Requirement: Inventory rejects candidates
The inventory workflow SHALL support rejecting a candidate with a reason.

#### Scenario: User rejects a candidate
- **WHEN** the user invokes `$imsight-llm-wiki use inventory to reject <slug> --reason "<reason>"`
- **THEN** the skill SHALL update the candidate's status to `rejected` and append the reason

### Requirement: Inventory logs promotions
The inventory workflow SHALL append a log entry when a candidate is ingested.

#### Scenario: Candidate ingested
- **WHEN** a candidate is promoted to ingest
- **THEN** it SHALL append `## [HH:MM] inventory | promoted <slug> to ingest`
