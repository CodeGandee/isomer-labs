## ADDED Requirements

### Requirement: Queries Activate by Surface Demand
Project Web SHALL activate backend queries only when navigation, a mounted panel, or an explicit user action needs their data.

#### Scenario: Deep-linked graph starts
- **WHEN** URL state identifies an Idea Graph for a known Research Topic
- **THEN** Project Web SHALL request its lightweight descriptor and graph data
- **AND** it SHALL NOT wait for separate Project or Topics bootstrap queries

#### Scenario: Unopened supporting surfaces stay idle
- **WHEN** the Idea Graph is open while overview JSON, runtime, actors, records, and idea detail surfaces are closed
- **THEN** Project Web SHALL NOT request data for those closed surfaces

#### Scenario: User opens a supporting surface
- **WHEN** a user opens a panel or action that needs supporting data
- **THEN** the owning panel or action SHALL activate its query and show a non-blocking loading state

#### Scenario: Panel closes
- **WHEN** the last mounted consumer of a panel-scoped query closes
- **THEN** Project Web SHALL stop panel-owned polling, event reactions, and expensive rendering work
