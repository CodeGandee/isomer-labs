# project-web-idea-graph-layout Specification

## Purpose
TBD - created by archiving change add-react-flow-layout-and-focus-controls. Update Purpose after archive.

## Requirements

### Requirement: Idea Graph Uses React Flow Exclusively
The Project Web Idea Graph SHALL use React Flow as its graph renderer for every supported `idea-lineage` response and SHALL NOT select another renderer from node count or backend renderer hints.

#### Scenario: Idea Graph opens with a small topology
- **WHEN** a user opens an Idea Graph whose current response contains a small number of nodes
- **THEN** Project Web renders the relationship graph with React Flow

#### Scenario: Idea Graph opens with hundreds of nodes
- **WHEN** a user opens an Idea Graph whose coherent response or focus projection contains hundreds of nodes
- **THEN** Project Web keeps the graph on React Flow
- **AND** it does not instantiate the existing Sigma.js graph component

#### Scenario: Backend returns a legacy Sigma hint
- **WHEN** an `idea-lineage` response includes a legacy `sigma-overview` renderer hint
- **THEN** the Idea Graph treats the hint as non-authoritative compatibility metadata
- **AND** renders the supported response with React Flow

### Requirement: Idea Graph Owns Layout Controls
The Idea Graph SHALL provide a collapsible Graph Controls surface inside the owning Idea Graph panel for changing and previewing layout behavior.

#### Scenario: User opens Graph Controls
- **WHEN** a user activates Graph Controls from the Idea Graph
- **THEN** the Idea Graph exposes its Layout and Focus controls inside that panel
- **AND** the React Flow canvas remains visible beside or beneath the controls according to available panel width

#### Scenario: User opens Project Settings
- **WHEN** a user opens the global Project Settings panel
- **THEN** Project Settings does not present Idea Graph layout algorithms, layout parameters, focus controls, or Graph Layout Preset management

### Requirement: Idea Graph Provides Curated Layout Algorithms
The Idea Graph SHALL expose a versioned layout algorithm registry that maps typed user-facing parameters to supported position calculations for React Flow nodes.

#### Scenario: User selects a layout algorithm
- **WHEN** a user opens the layout algorithm selector
- **THEN** the selector offers layered, force, stress, radial, and deterministic grid layouts
- **AND** each choice exposes only its supported parameters with defaults, bounds, and validation

#### Scenario: User configures layered layout
- **WHEN** the user selects layered layout
- **THEN** the controls allow the user to configure direction, node spacing, layer spacing, and edge routing

#### Scenario: User configures a nondeterministic algorithm
- **WHEN** the user selects a force, stress, or another algorithm that uses randomized initialization
- **THEN** the applied configuration includes a user-visible or preset-stored random seed so the same topology and configuration can produce repeatable positions

#### Scenario: Imported parameters contain raw engine options
- **WHEN** a Graph Layout Preset contains unregistered raw ELK.js option names or unsupported parameters
- **THEN** Project Web rejects those values instead of forwarding arbitrary options to the layout engine

### Requirement: Layout Preview Is Explicit and Safe
The Idea Graph SHALL separate draft layout controls from the last successfully applied layout and SHALL apply a draft only after an explicit preview request.

#### Scenario: User edits a layout parameter
- **WHEN** a user changes a draft algorithm or parameter without requesting preview
- **THEN** the current React Flow node positions remain unchanged
- **AND** the controls indicate that unapplied layout changes exist

#### Scenario: Layout preview succeeds
- **WHEN** the user requests Preview Layout and the layout job succeeds for the current visible topology
- **THEN** the Idea Graph applies the returned positions to React Flow
- **AND** reports the applied algorithm and layout duration

#### Scenario: Layout preview fails
- **WHEN** a layout job fails validation, exceeds a configured safety bound, or reports an engine error
- **THEN** the Idea Graph keeps the last successfully applied positions visible
- **AND** reports an actionable layout diagnostic

#### Scenario: Older layout job finishes late
- **WHEN** a layout job finishes after its topology, focus projection, or draft configuration has been superseded
- **THEN** the Idea Graph discards that stale result
- **AND** does not replace the current React Flow positions

### Requirement: Expensive Layout Work Does Not Block React Flow Interaction
The Idea Graph SHALL isolate expensive layout calculation from the browser UI thread and preserve stable React Flow render data when layout inputs have not changed.

#### Scenario: User previews a layout for hundreds of nodes
- **WHEN** the visible graph contains hundreds of nodes and the user requests layout preview
- **THEN** the layout calculation runs through an asynchronous worker boundary
- **AND** the panel can continue reporting progress and accepting safe navigation or cancellation input

#### Scenario: User changes selection without changing focus
- **WHEN** the user changes selected Research Ideas while N-hop focus is disabled and the visible topology is unchanged
- **THEN** the Idea Graph updates selection styling without rerunning layout

#### Scenario: User pans or zooms the canvas
- **WHEN** the React Flow viewport changes without a topology or applied layout change
- **THEN** the Idea Graph does not rerun the layout algorithm

### Requirement: Graph Layout Presets Are Browser-local
Project Web SHALL let users manage reusable, versioned Graph Layout Presets in browser-local storage without persisting them through the backend.

#### Scenario: User saves a successful layout configuration
- **WHEN** a user saves the currently applied algorithm and parameters as a named Graph Layout Preset
- **THEN** Project Web stores a versioned preset in browser-local storage
- **AND** the preset is available to other Idea Graph panels in that browser origin

#### Scenario: User manages a preset
- **WHEN** a user chooses to create, duplicate, rename, update, or delete a user-defined Graph Layout Preset
- **THEN** Project Web updates the browser-local preset catalog and synchronizes the catalog with other open tabs through browser storage events

#### Scenario: User modifies a built-in preset
- **WHEN** a user changes parameters derived from an immutable built-in preset
- **THEN** Project Web requires saving the changes as a user-defined preset instead of overwriting the built-in preset

#### Scenario: Preset is stored
- **WHEN** Project Web serializes a Graph Layout Preset
- **THEN** the preset contains its schema version, stable preset id, name, compatible graph kind, algorithm id, algorithm configuration version, validated parameters, and optional viewport fitting preferences
- **AND** it does not contain graph nodes, graph edges, topic ids, selected node ids, focus state, calculated node coordinates, credentials, or backend renderer state

#### Scenario: Backend graph request is made
- **WHEN** the Idea Graph loads, previews a layout, or applies a Graph Layout Preset
- **THEN** Project Web does not send the preset catalog, selected preset, layout parameters, or calculated positions to Workspace Runtime or another backend persistence surface

### Requirement: Graph Layout Presets Support Local File Exchange
Project Web SHALL export and import Graph Layout Presets as validated versioned JSON files selected by the user.

#### Scenario: User exports one preset
- **WHEN** a user exports a selected Graph Layout Preset
- **THEN** the browser offers a local JSON file containing that preset and its format discriminator and schema version

#### Scenario: User exports the preset catalog
- **WHEN** a user exports all user-defined Graph Layout Presets
- **THEN** the browser offers one versioned JSON document containing the browser-local catalog without graph or backend data

#### Scenario: User imports compatible presets
- **WHEN** a user selects a supported preset JSON file whose values pass schema and parameter validation
- **THEN** Project Web adds the imported presets to the browser-local catalog
- **AND** reports the number imported, copied because of conflicts, or skipped

#### Scenario: Imported preset id conflicts
- **WHEN** an imported preset id already belongs to a different browser-local preset
- **THEN** Project Web imports the incoming preset as a copy by default instead of silently overwriting existing data

#### Scenario: Import is invalid or unsupported
- **WHEN** an imported file exceeds configured size or count bounds, has an unknown discriminator, uses a newer unsupported schema version, or contains invalid algorithm parameters
- **THEN** Project Web rejects the affected import without changing the existing preset catalog
- **AND** reports a diagnostic that does not include local file contents beyond safe validation context

### Requirement: React Flow Remains Bounded During Large Graph Interaction
The Idea Graph SHALL apply focus projection before layout and React Flow conversion, and SHALL use React Flow visibility and render-stability controls when the visible graph remains large.

#### Scenario: N-hop focus reduces a large graph
- **WHEN** a user enables N-hop focus for selected Research Ideas
- **THEN** the Idea Graph lays out and sends only the resulting visible subgraph to React Flow

#### Scenario: Full graph remains visible
- **WHEN** focus is disabled and the coherent source graph contains hundreds of nodes
- **THEN** the Idea Graph keeps React Flow active
- **AND** uses visible-element rendering, memoized node components, stable node and edge objects, and reduced low-zoom detail according to its performance policy

#### Scenario: Visible graph exceeds a layout safety bound
- **WHEN** a selected layout would exceed its configured node, edge, iteration, or execution safety bound
- **THEN** the Idea Graph warns the user and retains the current layout
- **AND** it does not silently switch to another renderer or silently remove graph content
