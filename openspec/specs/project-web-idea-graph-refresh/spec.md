# project-web-idea-graph-refresh Specification

## Purpose
TBD - created by archiving change stabilize-idea-lineage-refresh. Update Purpose after archive.
## Requirements
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
The Idea Graph SHALL avoid replacing React Flow graph render data or rerunning layout when a graph refetch returns unchanged effective graph content and the applied focus and layout inputs remain unchanged.

#### Scenario: Refetch returns only new response metadata
- **WHEN** a graph response has the same effective graph content and topology completeness as the current graph but a different response timestamp or equivalent response metadata
- **THEN** the Idea Graph SHALL keep existing node objects, edge objects, layout positions, selected node ids, focus projection, and lineage highlights

#### Scenario: Graph content changes outside the visible focus projection
- **WHEN** a graph response changes source graph content without changing the effective visible focus projection or applied layout input fingerprint
- **THEN** the Idea Graph SHALL update source counts and query-owned data without replacing current React Flow positions

#### Scenario: Visible graph content changes
- **WHEN** a graph response changes the effective nodes or edges in the visible graph
- **THEN** the Idea Graph SHALL update base React Flow render data
- **AND** SHALL recompute positions with the currently applied layout configuration

#### Scenario: Focus or applied layout changes
- **WHEN** the user changes focus inputs or successfully previews a different applied layout configuration
- **THEN** the Idea Graph SHALL compute positions for the new visible topology and applied layout input fingerprint

#### Scenario: Superseded layout finishes after refresh
- **WHEN** a layout result belongs to an older graph revision, visible topology, focus projection, or applied layout fingerprint
- **THEN** the Idea Graph SHALL discard that result and retain the current last-good render state

### Requirement: Selection Survives Benign Refresh
The Idea Graph SHALL preserve every still-valid UI selection, current focus configuration, and derived highlights across loading, hover preview work, and transient refresh states.

#### Scenario: All selected nodes remain present
- **WHEN** every selected Research Idea remains present after a successful graph refresh
- **THEN** the selected node-id set and its derived direct-neighborhood highlights SHALL remain active

#### Scenario: Some selected nodes are removed
- **WHEN** a successful graph refresh confirms that some but not all selected Research Ideas are absent from the new source graph
- **THEN** the Idea Graph SHALL remove only the missing node ids from the selected set
- **AND** SHALL recalculate focus and highlights from the remaining selected nodes

#### Scenario: Every selected node is removed
- **WHEN** a successful graph refresh confirms that every selected Research Idea is absent from the new source graph
- **THEN** the Idea Graph SHALL clear the selected node-id set
- **AND** SHALL disable active N-hop focus or report that focus has no valid seeds

#### Scenario: Transient empty or failed refresh occurs
- **WHEN** the graph has last-good content and a background refresh is loading, fails, or produces no usable graph content without a confirmed content change
- **THEN** the Idea Graph SHALL keep the last-good nodes, edges, positions, selected node ids, focus state, and highlights visible

### Requirement: Backend Status Styling Does Not Collide With UI Selection
The idea lineage graph SHALL represent backend idea status and user interaction selection with distinct render classes or properties.

#### Scenario: Backend selected idea is not clicked
- **WHEN** a graph node represents a backend idea whose status is selected but the user has not clicked that node
- **THEN** the node SHALL keep backend selected/status styling without being treated as the active UI-selected node

#### Scenario: User selects another idea
- **WHEN** the user clicks an idea node that is not the backend selected idea
- **THEN** the clicked node SHALL receive UI-selected styling without removing backend selected/status styling from other nodes

### Requirement: Applied Layout Choice Survives Graph Refresh
The Idea Graph SHALL retain the current applied layout configuration across graph refreshes until the user applies another configuration or restores a preset.

#### Scenario: Content changes under an applied preset
- **WHEN** graph content changes while a Graph Layout Preset configuration is applied
- **THEN** the Idea Graph recalculates affected positions with that applied algorithm and parameter configuration
- **AND** does not revert to the built-in layered default

#### Scenario: Current preset is deleted in another tab
- **WHEN** the browser-local catalog no longer contains the preset that supplied the current applied configuration
- **THEN** the Idea Graph retains the already applied validated configuration as an unsaved layout
- **AND** reports that the originating preset is unavailable

#### Scenario: Draft layout exists during refresh
- **WHEN** graph data refreshes while the user has unapplied draft layout changes
- **THEN** the Idea Graph preserves the draft controls separately
- **AND** renders refreshed content with the last successfully applied layout configuration
