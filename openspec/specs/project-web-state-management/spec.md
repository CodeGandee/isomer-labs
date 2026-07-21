# project-web-state-management Specification

## Purpose
TBD - created by archiving change standardize-project-web-state-model. Update Purpose after archive.
## Requirements
### Requirement: Project Web State Ownership
Project Web SHALL classify GUI state by ownership before storing or mutating it.

#### Scenario: Backend data remains query-owned
- **WHEN** a Project Web feature needs Project, Topic, graph, record, or idea detail data from the backend
- **THEN** the feature SHALL read that data through TanStack Query or a selector over TanStack Query data instead of copying it into independent component state

#### Scenario: Durable navigation remains URL-owned
- **WHEN** a Project Web feature changes selected Topic, graph scope, or opened semantic item
- **THEN** the feature SHALL route that change through the workbench navigation model that writes URL and history state

#### Scenario: Private disposable UI may stay local
- **WHEN** a UI state value affects only one component instance and has no URL, backend, tab, graph, or cross-component meaning
- **THEN** the component MAY keep that value in local React state

### Requirement: Shared State Changes Use Typed Actions
Project Web SHALL change shared, durable, or complex interaction state through typed actions handled by reducers or feature stores.

#### Scenario: Component requests shared state change
- **WHEN** a component needs to select a graph node, open a workbench item, refresh a Topic, change persisted settings, or trigger a delayed interaction
- **THEN** the component SHALL dispatch a typed action or call a typed command API instead of mutating shared state directly

#### Scenario: Reducer transitions are testable
- **WHEN** a feature store handles a typed action
- **THEN** the resulting state transition SHALL be testable without rendering the full Project Web app

#### Scenario: Raw writable streams are contained
- **WHEN** RxJS is used for Project Web commands or events
- **THEN** writable Subjects SHALL remain behind named feature APIs or event boundary modules rather than being scattered through rendering components

### Requirement: Feature Stores Use Panel Lifetime
Project Web feature stores for tab-scoped interaction state SHALL be scoped to Dockview panel identity.

#### Scenario: Store is created for panel
- **WHEN** a Dockview panel opens a feature that needs complex interaction state
- **THEN** the feature store SHALL be keyed by the Dockview panel id and MAY store the openable item id as metadata

#### Scenario: Store is disposed with panel
- **WHEN** the owning Dockview panel closes
- **THEN** the feature store SHALL release subscriptions, timers, and cached interaction state for that panel

#### Scenario: Same item opens independently
- **WHEN** the same semantic openable item is opened in separate panel lifecycles
- **THEN** each panel SHALL receive independent interaction state unless a later requirement explicitly defines shared state for that feature

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

### Requirement: Graph Visuals Are Derived From State
Project Web graph visuals SHALL be derived from graph data and explicit interaction state rather than direct DOM mutation.

#### Scenario: Selected neighborhood renders from state
- **WHEN** an idea node is selected
- **THEN** the selected node, direct parent nodes, direct child nodes, incoming edges, and outgoing edges SHALL receive their visual states from React render data derived from the interaction state

#### Scenario: Hover render does not erase selection
- **WHEN** a hover preview opens, loads Markdown, closes, or rerenders
- **THEN** the selected idea lineage node and its adjacent node and edge highlights SHALL remain visible until the selected node changes or the graph data changes

#### Scenario: Edge highlighting is not DOM-owned
- **WHEN** an adjacent idea lineage edge is highlighted
- **THEN** the highlight SHALL be represented first through declarative ReactFlow edge render state and SHALL NOT depend on one-time `classList` mutation of ReactFlow DOM elements

#### Scenario: Overlay is a measured fallback
- **WHEN** declarative ReactFlow edge render state causes unacceptable edge churn in tests or profiling
- **THEN** the implementation MAY use a state-derived highlight overlay while keeping base edge props stable

### Requirement: Effect Boundaries Are Explicit
Project Web SHALL isolate side effects from state reducers and selectors.

#### Scenario: Store handles pure transition
- **WHEN** a typed action is reduced into new state
- **THEN** the reducer SHALL avoid direct calls to browser history, Dockview APIs, fetch APIs, localStorage, timers, or DOM mutation

#### Scenario: Adapter handles side effect
- **WHEN** a state transition requires opening a tab, syncing URL history, invalidating queries, writing settings, scheduling hover delay, or sending a future tmux command
- **THEN** a named effect or adapter SHALL perform that side effect from a typed action or derived event

### Requirement: State Model Regression Tests
Project Web SHALL include tests that cover state transitions, derived graph render state, and effect boundaries for the migrated interaction flows.

#### Scenario: Selection survives hover rerender
- **WHEN** a test selects an idea node and then triggers hover preview state changes
- **THEN** the test SHALL verify that selected node, parent node, child node, incoming edge, and outgoing edge visual states remain derived and visible

#### Scenario: Unaffected graph objects stay stable
- **WHEN** a test selects an idea node in a graph with unrelated nodes and edges
- **THEN** the test SHALL verify that selectors preserve object identity for unaffected render objects or keep base edge props stable when an overlay is used

#### Scenario: Commands remain typed
- **WHEN** a test opens an idea or record from a graph interaction
- **THEN** the test SHALL verify that the interaction emits a typed workbench command rather than directly mutating Dockview from the graph rendering component

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

