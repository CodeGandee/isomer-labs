## ADDED Requirements

### Requirement: Revision-Aware Graph Refresh
Project Web SHALL refresh active topic graph data only when the user requests refresh or when backend topic events report a new effective index revision for that topic.

#### Scenario: Unchanged topic event arrives while graph is idle
- **WHEN** the idea lineage graph is open and a topic event arrives with the same index revision already observed for that topic
- **THEN** Project Web SHALL NOT invalidate or refetch the active idea lineage graph query

#### Scenario: Changed topic event arrives
- **WHEN** the idea lineage graph is open and a topic event arrives with a different index revision for that topic
- **THEN** Project Web SHALL invalidate graph queries that intersect the event graph scopes

#### Scenario: User requests refresh
- **WHEN** the user triggers a manual topic refresh
- **THEN** Project Web SHALL invalidate the relevant topic queries even if the latest known index revision is unchanged

### Requirement: Stable Idea Graph Rendering
The idea lineage graph SHALL avoid replacing React Flow graph render data or rerunning layout when a graph refetch returns unchanged graph content.

#### Scenario: Refetch returns only new response metadata
- **WHEN** a graph response has the same effective graph content as the current graph but a different response timestamp
- **THEN** the idea lineage graph SHALL keep existing node objects, edge objects, layout positions, selected node, and lineage highlights

#### Scenario: Graph content changes
- **WHEN** a graph response changes the effective nodes or edges used by the idea lineage graph
- **THEN** the idea lineage graph SHALL update base graph render data and recompute layout

### Requirement: Selection Survives Benign Refresh
The idea lineage graph SHALL preserve UI selection and neighborhood highlights across loading, hover preview work, and transient refresh states.

#### Scenario: Selected node remains present
- **WHEN** a selected idea node remains present after a successful graph refresh
- **THEN** the selected node, parent nodes, child nodes, incoming edges, and outgoing edges SHALL remain highlighted

#### Scenario: Transient empty or failed refresh occurs
- **WHEN** the graph has last-good content and a background refresh is loading, fails, or produces no usable graph content without a confirmed content change
- **THEN** the idea lineage graph SHALL keep the last-good nodes, edges, selection, and highlights visible

#### Scenario: Selected node is removed by confirmed content change
- **WHEN** a successful graph refresh has changed graph content and the previously selected node is absent from the new node set
- **THEN** the idea lineage graph SHALL clear the selected node and remove lineage highlights

### Requirement: Backend Status Styling Does Not Collide With UI Selection
The idea lineage graph SHALL represent backend idea status and user interaction selection with distinct render classes or properties.

#### Scenario: Backend selected idea is not clicked
- **WHEN** a graph node represents a backend idea whose status is selected but the user has not clicked that node
- **THEN** the node SHALL keep backend selected/status styling without being treated as the active UI-selected node

#### Scenario: User selects another idea
- **WHEN** the user clicks an idea node that is not the backend selected idea
- **THEN** the clicked node SHALL receive UI-selected styling without removing backend selected/status styling from other nodes
