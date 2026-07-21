## ADDED Requirements

### Requirement: Explorer Topic Branches Resolve on Demand
The Project Explorer API SHALL resolve Effective Topic Context only for Research Topic branches requested as expanded or opened.

#### Scenario: Initial Explorer request
- **WHEN** the GUI requests the Project Explorer with no expanded Research Topic ids
- **THEN** the response SHALL derive collapsed topic nodes from Project Manifest registrations
- **AND** it SHALL NOT resolve every topic's Effective Topic Context

#### Scenario: One topic expands
- **WHEN** the GUI requests the Project Explorer with one expanded Research Topic id
- **THEN** the response SHALL resolve that topic and include its deeper semantic children
- **AND** it SHALL leave other collapsed topic branches unresolved

#### Scenario: Deep link bypasses tree expansion
- **WHEN** the GUI resolves a valid topic-scoped openable item directly
- **THEN** the descriptor API SHALL resolve only the requested topic
- **AND** the user SHALL NOT need to expand the matching Explorer branch first

#### Scenario: Collapsed topic configuration is damaged
- **WHEN** one collapsed topic has damaged deeper configuration
- **THEN** the initial skeleton SHALL retain its manifest-derived topic node
- **AND** expansion or opening SHALL report the detailed diagnostic for that topic
