## ADDED Requirements

### Requirement: Project Web Display Contracts Use Summary
Project Web graph, timeline, hover, detail, and record read contracts SHALL expose `summary` as the brief display field and SHALL NOT require `one_liner`.

#### Scenario: Graph node uses summary
- **WHEN** the Project Web idea graph consumes a graph response
- **THEN** each graph node exposes `title`, `summary`, material kind, status, refs, and diagnostics needed for rendering
- **AND** canonical Research Idea nodes also expose `display_key`, visibility, and parent refs
- **AND** the node contract does not expose `one_liner`

#### Scenario: Timeline row uses summary
- **WHEN** the Project Web idea timeline consumes a timeline row response
- **THEN** the row exposes creation time, display index, display key, title, summary, parent display keys or indexes, visibility, status, and diagnostics needed for table rendering
- **AND** the row contract does not expose `one_liner`

#### Scenario: Hover and detail use summary
- **WHEN** the Project Web hover preview or idea detail panel opens a Research Idea
- **THEN** the read payload exposes canonical idea `title` and `summary` and exact source-fragment `title` and `summary` when available
- **AND** source aliases remain separate from display fields

#### Scenario: Fuzzy search includes summary
- **WHEN** a GUI user performs fuzzy text search in idea graph or timeline views
- **THEN** search matching includes `summary` and the other visible/searchable row or node fields
- **AND** visibility flags still control whether supporting or hidden ideas are shown in results

### Requirement: Project Web Display Diagnostics Are Non-fatal
Project Web read contracts SHALL carry display-contract diagnostics so damaged data does not crash the GUI.

#### Scenario: Missing summary reaches GUI as diagnostic
- **WHEN** a backend graph, timeline, hover, or detail response encounters an idea without a usable `summary`
- **THEN** the response includes a diagnostic naming the affected idea and missing field
- **AND** the GUI can render the remaining interpretable data without reading `one_liner`

#### Scenario: Recent errors include display issues
- **WHEN** Project Web records display-contract warnings or errors while building read models
- **THEN** the recent-errors read contract exposes those issues for operator inspection
- **AND** the recent-errors contract remains a process-local recent diagnostic query rather than durable Workspace Runtime storage for this change
