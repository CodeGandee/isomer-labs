## ADDED Requirements

### Requirement: Idea Lineage Uses One Node Search
The idea lineage graph SHALL expose one search input for filtering idea nodes and SHALL NOT show separate status, relation, producer, time-range, or supporting-record filter controls in that view.

#### Scenario: User opens the idea lineage graph
- **WHEN** a user opens the idea lineage graph for a Research Topic
- **THEN** the graph toolbar SHALL show one search input for idea nodes
- **AND** the toolbar SHALL NOT show status, relation, producer, time-range, or supporting-record controls

#### Scenario: Dense graph views keep their own controls
- **WHEN** a user opens a dense non-idea graph view
- **THEN** the change SHALL NOT remove the generic graph filter controls from that dense graph view

### Requirement: Search Fuzzy-Matches Node Information
The idea lineage search SHALL use Fuse.js to fuzzy-match relevant node information and rank visible idea nodes by match quality.

#### Scenario: User searches with partial or mistyped text
- **WHEN** a user enters partial or mistyped search text in the idea lineage search input
- **THEN** the graph SHALL keep matching idea nodes visible when Fuse.js ranks them as matches
- **AND** matching SHALL consider relevant node fields such as id, record id, idea id, title, one-liner, summary, status, producer, skill, material kind, and already-loaded detail references

#### Scenario: User clears the search input
- **WHEN** a user clears the idea lineage search input
- **THEN** the graph SHALL restore the unfiltered idea lineage overview

### Requirement: Search Filters Nodes Only
The idea lineage search SHALL filter graph nodes only; edges SHALL remain visible only when both endpoint nodes remain visible after node filtering.

#### Scenario: Search hides a node
- **WHEN** a user search hides an idea node
- **THEN** edges attached to that hidden node SHALL also be hidden
- **AND** edge labels, relation kinds, and relationship metadata SHALL NOT independently cause a node to match

### Requirement: Supporting Records Are Accessed Through Details
The idea lineage graph SHALL request and display the overview idea graph without supporting records; users SHALL inspect supporting records by opening a node detail view.

#### Scenario: Idea lineage graph loads
- **WHEN** the frontend requests the idea lineage graph
- **THEN** it SHALL request the graph with supporting records disabled
- **AND** it SHALL NOT offer a toggle to include supporting records in the graph

#### Scenario: User wants supporting record context
- **WHEN** a user wants supporting record context for an idea
- **THEN** the user SHALL open the idea node detail view to inspect records, realizations, lineage, diagnostics, and JSON data available for that node
