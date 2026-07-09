## ADDED Requirements

### Requirement: Query Index Uses Canonical Summary
The research record query index SHALL derive record summaries, idea facet summaries, and graph node summaries from canonical `summary` fields rather than from `one_liner` or generated Markdown.

#### Scenario: Record summary is indexed
- **WHEN** query-index rebuild processes a structured Research Record payload
- **THEN** the indexed record row stores `title` from the payload root `title`
- **AND** it stores `summary` from the payload root `summary`

#### Scenario: Idea facet summary is indexed
- **WHEN** query-index extraction processes an idea-bearing payload section
- **THEN** each extracted idea facet stores the idea entry's `title` and `summary`
- **AND** it does not create or expose a first-class `one_liner` facet field

#### Scenario: Rebuild reports missing summary
- **WHEN** query-index rebuild encounters a record or idea entry without a required `summary`
- **THEN** it records a deterministic diagnostic and skips or marks only the affected derived field or row
- **AND** it does not synthesize a summary from arbitrary text during ordinary rebuild

#### Scenario: Export omits one-liner display field
- **WHEN** query list, export, lineage, facets, graph, or timeline responses include record or idea summaries
- **THEN** they expose `summary` as the brief display field
- **AND** they do not require GUI consumers to read `one_liner`

#### Scenario: Graph node summaries use summary across material kinds
- **WHEN** query-index or Project Web graph export builds nodes for ideas, records, routes, claims, files, or other material kinds
- **THEN** each node uses `summary` for its brief display text when such text is available
- **AND** it does not expose `one_liner` as the generic node subtitle field

### Requirement: Query Index Display Diagnostics
The query-index export API SHALL include display-contract diagnostics in GUI-safe diagnostic summaries.

#### Scenario: Export includes display diagnostics
- **WHEN** a GUI or operator exports a query-index view for a Topic Workspace with missing, duplicated, stale, or legacy display fields
- **THEN** the response includes full diagnostics and a grouped summary by severity and diagnostic code
- **AND** the response preserves safely interpretable nodes, rows, and detail locators
