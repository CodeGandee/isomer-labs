# project-web-idea-lineage-selection Specification

## Purpose
TBD - created by archiving change refine-idea-lineage-graph-selection. Update Purpose after archive.
## Requirements
### Requirement: Idea lineage hover delay
The Project Web idea lineage graph SHALL wait 2 seconds before opening an idea hover preview from hover or touch long press intent.

#### Scenario: Mouse hover waits for intent delay
- **WHEN** a user moves the mouse over an idea lineage node for less than 2 seconds
- **THEN** the system SHALL keep the hover preview closed

#### Scenario: Mouse hover opens after intent delay
- **WHEN** a user keeps the mouse over an idea lineage node for at least 2 seconds
- **THEN** the system SHALL open the hover preview for that node

#### Scenario: Touch long press uses same delay
- **WHEN** a user long-presses an idea lineage node on a touch interface for at least 2 seconds without moving outside tolerance
- **THEN** the system SHALL open the hover preview for that node

### Requirement: Idea lineage edges show direction
The Project Web idea lineage graph SHALL render visible direction on ReactFlow idea lineage edges from parent idea to child idea.

#### Scenario: Directed edge is visible
- **WHEN** the graph contains an edge from a parent idea node to a child idea node
- **THEN** the ReactFlow edge SHALL render with an arrow marker pointing at the child idea node

### Requirement: Selected idea highlights direct lineage neighborhood
The Project Web idea lineage graph SHALL visually distinguish a selected idea node, its direct parent ideas, and its direct child ideas.

#### Scenario: Selecting node highlights parents
- **WHEN** a user selects an idea node that has incoming idea lineage edges
- **THEN** each direct parent node SHALL receive a parent highlight distinct from the selected node and child highlights

#### Scenario: Selecting node highlights children
- **WHEN** a user selects an idea node that has outgoing idea lineage edges
- **THEN** each direct child node SHALL receive a child highlight distinct from the selected node and parent highlights

#### Scenario: Selecting node highlights adjacent edges
- **WHEN** a user selects an idea node with incoming or outgoing idea lineage edges
- **THEN** incoming and outgoing adjacent edges SHALL receive distinct visual states

