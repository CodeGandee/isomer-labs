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
The Project Web idea lineage graph SHALL visually distinguish every UI-selected Research Idea and the union of their direct parent ideas, direct child ideas, incoming Idea Lineage Edges, and outgoing Idea Lineage Edges.

#### Scenario: Selecting one node highlights parents
- **WHEN** a user selects one idea node that has incoming Idea Lineage Edges
- **THEN** each direct parent node SHALL receive a parent highlight distinct from the selected node and child highlights

#### Scenario: Selecting one node highlights children
- **WHEN** a user selects one idea node that has outgoing Idea Lineage Edges
- **THEN** each direct child node SHALL receive a child highlight distinct from the selected node and parent highlights

#### Scenario: Selecting one node highlights adjacent edges
- **WHEN** a user selects one idea node with incoming or outgoing Idea Lineage Edges
- **THEN** incoming and outgoing adjacent edges SHALL receive distinct visual states

#### Scenario: Selecting multiple nodes highlights their union
- **WHEN** a user selects multiple idea nodes
- **THEN** every selected node receives selected styling
- **AND** direct-neighborhood node and edge highlights are derived from the union of all selected nodes

#### Scenario: Selected node is also another selection's neighbor
- **WHEN** a selected node is a direct parent or child of another selected node
- **THEN** selected styling takes precedence over parent or child styling for that node

### Requirement: Idea Lineage Supports Multiple UI-selected Research Ideas
The Project Web Idea Graph SHALL maintain an ordered set of UI-selected Research Idea node ids independently of backend idea status.

#### Scenario: User clicks without a selection modifier
- **WHEN** a user single-clicks an idea node without the configured multi-selection modifier
- **THEN** the UI-selected set contains that node and replaces the previous UI-selected set

#### Scenario: User modifier-clicks an unselected node
- **WHEN** a user uses Ctrl-click, Command-click, or the platform-equivalent multi-selection gesture on an unselected idea node
- **THEN** the node is added to the UI-selected set without removing existing selections

#### Scenario: User modifier-clicks a selected node
- **WHEN** a user uses the multi-selection gesture on an already selected idea node
- **THEN** that node is removed from the UI-selected set without clearing the remaining selections

#### Scenario: User completes a React Flow selection area
- **WHEN** a user selects multiple idea nodes with the React Flow selection-area interaction
- **THEN** the UI-selected set reflects the selected nodes according to the active replace or additive selection gesture

#### Scenario: User clears selection
- **WHEN** a user activates Clear Selection or the supported keyboard command
- **THEN** the UI-selected set becomes empty
- **AND** N-hop focus is disabled or reports that selected seeds are required

#### Scenario: User opens one selected idea
- **WHEN** a user double-clicks or otherwise opens one idea while multiple ideas are selected
- **THEN** Project Web opens the targeted idea detail
- **AND** does not replace the remaining UI-selected set solely because an open action occurred

### Requirement: Idea Graph Provides Multi-source N-hop Focus
The Idea Graph SHALL derive an optional visible subgraph from the union of nodes reachable within a configured hop radius from any UI-selected Research Idea.

#### Scenario: Focus is disabled
- **WHEN** N-hop focus is disabled
- **THEN** the focus projection contains the complete coherent source graph before existing visible-label search is applied

#### Scenario: Focus uses zero hops
- **WHEN** N-hop focus is enabled with one or more selected seeds and radius zero
- **THEN** the focus projection contains the selected seed nodes only

#### Scenario: Focus uses multiple seeds
- **WHEN** N-hop focus is enabled with multiple selected seeds and radius greater than zero
- **THEN** the focus projection contains the union of nodes whose shortest eligible path from any selected seed is at most the configured radius
- **AND** each selected seed has distance zero

#### Scenario: Focus traverses incoming edges
- **WHEN** focus direction is Incoming
- **THEN** traversal follows each eligible Idea Lineage Edge from target to source

#### Scenario: Focus traverses outgoing edges
- **WHEN** focus direction is Outgoing
- **THEN** traversal follows each eligible Idea Lineage Edge from source to target

#### Scenario: Focus traverses both directions
- **WHEN** focus direction is Both
- **THEN** traversal treats each eligible Idea Lineage Edge as traversable in either direction without changing its rendered direction

#### Scenario: Focus limits relation kinds
- **WHEN** the user chooses a subset of Idea Lineage Edge kinds in the Focus controls
- **THEN** the projection applies the relation-kind filter before calculating hop distance

#### Scenario: Focus derives visible edges
- **WHEN** focus produces a visible node set
- **THEN** the default visible edge set contains every eligible Idea Lineage Edge whose source and target are both visible

#### Scenario: User enables focus without seeds
- **WHEN** the UI-selected set is empty
- **THEN** Project Web does not apply an empty focus projection
- **AND** the Focus controls explain that at least one selected Research Idea is required

### Requirement: N-hop Focus Composes With Visible-label Search
The Idea Graph SHALL calculate N-hop reachability from the eligible source topology before applying the existing visible-label node search to the focused result.

#### Scenario: Search is entered while focus is active
- **WHEN** a user enters visible-label search text while an N-hop focus projection is active
- **THEN** search filters nodes from the focused result using the existing label-search contract
- **AND** search does not change the hop distances used to produce that focused result

#### Scenario: User clears search while focus is active
- **WHEN** a user clears visible-label search text while N-hop focus remains active
- **THEN** the Idea Graph restores all nodes and eligible induced edges from the current focus projection

### Requirement: Focus Controls Expose Projection State
The Idea Graph Focus controls SHALL expose selected seeds, hop radius, direction, eligible relation kinds, and visible-versus-source graph counts inside the Idea Graph panel.

#### Scenario: Focus projection is active
- **WHEN** the Idea Graph displays an active N-hop focus projection
- **THEN** the Focus controls show removable selected-seed entries and the active projection parameters
- **AND** the panel reports visible and source node and edge counts

#### Scenario: User removes a seed from Focus controls
- **WHEN** a user removes one selected seed from the Focus controls
- **THEN** Project Web recalculates the multi-source focus projection from the remaining selected seeds

#### Scenario: User exits focus
- **WHEN** a user activates Exit Focus
- **THEN** the focus projection is disabled without requiring the selected Research Ideas to be cleared
