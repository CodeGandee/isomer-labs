## ADDED Requirements

### Requirement: Viewer Data Is Demand Driven
Project Web viewers SHALL request only the primary data and supporting resources needed by their mounted surface and active user action.

#### Scenario: Idea Graph is the only open viewer
- **WHEN** a user opens an Idea Graph and no supporting viewer is open
- **THEN** the graph panel SHALL request its graph payload and required change-event stream
- **AND** it SHALL NOT request topic overview JSON, runtime inspection, actors, record details, or unopened idea details

#### Scenario: Supporting JSON remains closed
- **WHEN** a detail or overview panel offers a `View JSON` action that remains closed
- **THEN** the panel SHALL NOT request optional full source JSON or supporting JSON payloads

#### Scenario: Supporting JSON opens
- **WHEN** the user opens `View JSON`
- **THEN** the panel SHALL fetch the required JSON on demand and show a bounded loading state

#### Scenario: Viewer module remains unopened
- **WHEN** no mounted panel needs a graph, Markdown, PDF, Mermaid, KaTeX, or layout worker module
- **THEN** the initial browser bundle SHALL leave that module in its lazy chunk
