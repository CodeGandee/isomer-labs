# project-web-recent-errors-query Specification

## Purpose
TBD - created by archiving change revise-project-web-graph-idea-views. Update Purpose after archive.
## Requirements
### Requirement: Recent Errors Query
Project Web SHALL provide a read-only backend query for recent read-model and GUI interpretation errors observed by the running Project Web service process.

#### Scenario: Query recent topic errors
- **WHEN** the GUI requests recent errors for a Research Topic
- **THEN** the backend returns a bounded newest-first list of recent errors or warnings for that topic
- **AND** each item includes timestamp, severity, code, message, source view or operation when known, and optional idea or record refs when known
- **AND** the list is sourced from a service-local bounded in-memory ring buffer

#### Scenario: Query is read-only
- **WHEN** a caller requests recent errors
- **THEN** the backend does not rebuild, repair, cleanup, migrate, backfill, or write Workspace Runtime records or query-index rows

#### Scenario: Service restart clears recent errors
- **WHEN** the Project Web service process restarts
- **THEN** previously collected recent errors are not required to survive
- **AND** the query remains a live troubleshooting surface rather than durable audit history

#### Scenario: No recent errors
- **WHEN** no recent errors are available for the selected scope
- **THEN** the backend returns an empty list with `mutated: false`

#### Scenario: Error query is bounded
- **WHEN** many errors have occurred
- **THEN** the backend limits the response to a documented maximum or caller-provided bounded limit
- **AND** it does not return unbounded logs, raw payload bodies, file contents, terminal output, credentials, or secrets

### Requirement: Recent Errors Surface Supports Timeline Warnings
Project Web SHALL let graph and timeline views point users to recent backend errors when read-model data becomes non-interpretable.

#### Scenario: Timeline cannot interpret data
- **WHEN** the Idea Timeline view cannot safely interpret current idea data
- **THEN** the GUI shows a warning and can query recent errors for context

#### Scenario: Graph or timeline refresh records warning
- **WHEN** a graph or timeline refresh detects malformed relationships, missing endpoints, or invalid timestamps
- **THEN** the backend recent-errors query can expose a recent diagnostic for that failed interpretation attempt

