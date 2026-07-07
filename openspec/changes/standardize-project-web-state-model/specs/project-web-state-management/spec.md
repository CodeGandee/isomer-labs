## ADDED Requirements

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
The idea lineage graph SHALL own selection, hover preview, delayed hover, touch long press, and open intent through an idea lineage interaction state model.

#### Scenario: User selects idea node
- **WHEN** a user single-clicks an idea lineage node
- **THEN** the interaction store SHALL record that node as selected and derive its direct parents, direct children, incoming edges, and outgoing edges from graph data

#### Scenario: User hovers idea node
- **WHEN** a user hovers over an idea lineage node long enough to trigger the configured delay
- **THEN** the interaction store SHALL transition the hover preview from pending to visible for that node without changing the selected node

#### Scenario: User opens idea node
- **WHEN** a user double-clicks an idea lineage node or triggers an equivalent open command
- **THEN** the interaction store SHALL clear active hover preview state and emit an open intent for the selected idea

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
