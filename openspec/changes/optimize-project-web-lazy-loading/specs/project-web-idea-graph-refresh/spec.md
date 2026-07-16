## ADDED Requirements

### Requirement: Topic Events Use Lightweight Revision Reads
Project Web SHALL derive topic change events from query-index revision metadata without exporting graph or record content.

#### Scenario: Event poll reads current revision
- **WHEN** the event stream polls a Research Topic for changes
- **THEN** the backend SHALL read bounded query-index table revision metadata
- **AND** it SHALL NOT select graph nodes, canonical idea payloads, source JSON, or full index diagnostics

#### Scenario: Revision is unchanged
- **WHEN** two consecutive polls produce the same effective index revision
- **THEN** the event stream SHALL suppress a duplicate change event
- **AND** the frontend SHALL NOT refetch the graph

#### Scenario: Revision changes
- **WHEN** a later poll produces a different index revision
- **THEN** the event SHALL carry the new revision and affected graph scopes
- **AND** mounted intersecting graph queries SHALL become eligible for invalidation

### Requirement: Event Polling Does Not Block the Web Service
Project Web SHALL isolate synchronous revision reads from the asynchronous response loop.

#### Scenario: Revision read is slow
- **WHEN** a filesystem or SQLite revision read takes longer than expected
- **THEN** the event stream SHALL run that work outside the ASGI event-loop thread
- **AND** health, asset, and unrelated API requests SHALL remain serviceable

#### Scenario: Event subscriber disconnects
- **WHEN** the browser closes the event stream or its owning topic subscription
- **THEN** Project Web SHALL stop scheduling further revision polls for that stream
