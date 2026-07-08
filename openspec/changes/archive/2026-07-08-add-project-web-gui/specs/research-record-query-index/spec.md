## ADDED Requirements

### Requirement: Web GUI Query-index Read Model
The research record query index SHALL provide enough read-only data for the local Project web GUI to browse Topic Workspace records without parsing Markdown.

#### Scenario: GUI reads indexed summaries
- **WHEN** the web GUI lists records, exports a dashboard view, or opens lineage, file, facet, idea, experiment, or claim views
- **THEN** it reads query-index rows through the existing query APIs or equivalent Python API calls
- **AND** it does not treat generated Markdown as an authoritative data source

#### Scenario: GUI opens canonical detail
- **WHEN** the web GUI opens a record detail view
- **THEN** it uses returned record ids, payload locators, rendered Markdown locators, file locators, and structured payload metadata to reopen canonical detail sources

#### Scenario: GUI reports stale index state
- **WHEN** query-index validation reports missing, stale, orphaned, or inconsistent rows
- **THEN** the web GUI exposes those diagnostics and offers explicit maintenance actions instead of repairing the index during read operations
