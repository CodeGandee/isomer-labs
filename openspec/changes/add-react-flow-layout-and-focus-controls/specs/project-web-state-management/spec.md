## MODIFIED Requirements

### Requirement: Idea Lineage Interaction Store
The Idea Graph SHALL own multi-selection, N-hop focus configuration, draft and applied layout configuration, layout job identity and status, hover preview, delayed hover, touch long press, and open intent through a panel-scoped Idea Graph interaction state model.

#### Scenario: User selects one idea node
- **WHEN** a user single-clicks an idea lineage node without a multi-selection modifier
- **THEN** the interaction store SHALL replace its selected node-id set with that node id and derive direct-neighborhood highlights from graph data

#### Scenario: User changes multiple selected nodes
- **WHEN** a user adds, removes, replaces, area-selects, or clears UI-selected idea nodes
- **THEN** the interaction store SHALL update selected node ids through typed actions
- **AND** selectors SHALL derive selected-node and direct-neighborhood visual state without mutating React Flow DOM elements

#### Scenario: User changes focus configuration
- **WHEN** a user enables or disables focus or changes hop radius, direction, or eligible relation kinds
- **THEN** the interaction store SHALL record the focus configuration through typed actions
- **AND** a pure selector SHALL derive the requested focus projection from current graph data and selected node ids when complete topology is available

#### Scenario: User edits layout configuration
- **WHEN** a user changes a layout algorithm or parameter
- **THEN** the interaction store SHALL update draft layout configuration without replacing the applied layout configuration or current positions

#### Scenario: Layout job begins and completes
- **WHEN** an effect adapter starts or completes a layout job
- **THEN** the interaction store SHALL record a typed job identity, input fingerprint, status, and safe result metadata
- **AND** the reducer SHALL accept positions only from the current job identity and fingerprint

#### Scenario: User hovers idea node
- **WHEN** a user hovers over an idea lineage node long enough to trigger the configured delay
- **THEN** the interaction store SHALL transition the hover preview from pending to visible for that node without changing the selected node-id set

#### Scenario: User opens idea node
- **WHEN** a user double-clicks an idea lineage node or triggers an equivalent open command
- **THEN** the interaction store SHALL clear active hover preview state and emit an open intent for the targeted idea without discarding unrelated selected node ids

#### Scenario: Touch interaction mirrors hover
- **WHEN** a user long-presses an idea lineage node on a touch interface without exceeding movement tolerance before the delay elapses
- **THEN** the interaction store SHALL show the same hover preview state used by mouse hover

## ADDED Requirements

### Requirement: Idea Graph Projections and Layout Inputs Are Derived
Project Web SHALL derive focus projections, visible React Flow data, layout input fingerprints, and selection highlights from query-owned graph data and explicit panel interaction state.

#### Scenario: Complete graph data and focus state are available
- **WHEN** the graph query provides complete topology and the panel has an active focus configuration
- **THEN** a pure selector derives the visible N-hop projection without copying backend graph data into an independent mutable graph store

#### Scenario: Visible topology changes
- **WHEN** selected seeds, focus parameters, search, structural graph content, or eligible relation kinds change the visible topology
- **THEN** Project Web derives a new layout input fingerprint from stable node and edge identity plus the applied algorithm configuration

#### Scenario: Visual-only state changes
- **WHEN** hover, selection styling, viewport, progress text, or another visual-only state changes without changing the visible topology
- **THEN** the layout input fingerprint remains unchanged

### Requirement: Graph Layout Preset Effects Use a Dedicated Adapter
Project Web SHALL perform Graph Layout Preset storage, browser storage-event synchronization, local file import, and local file export through named adapters outside state reducers and React Flow rendering components.

#### Scenario: Reducer handles a preset command
- **WHEN** a typed command requests preset save, update, delete, import, or export
- **THEN** the pure reducer records only the interaction intent or resulting validated catalog state
- **AND** a dedicated adapter performs localStorage or file API side effects

#### Scenario: Browser storage event arrives
- **WHEN** another browser tab changes the Graph Layout Preset catalog
- **THEN** the persistence adapter validates the new catalog before dispatching a typed replacement action
