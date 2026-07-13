## Why

The Idea Graph currently fixes React Flow to one ELK layered layout, supports only one UI-selected Research Idea, and redirects larger graphs toward Sigma.js after a 120-node bound. Users need to explore idea lineage graphs with hundreds of nodes inside React Flow by choosing layout algorithms and parameters, saving reusable browser-local layout presets, and focusing the canvas on the N-hop neighborhood of multiple selected Research Ideas.

## What Changes

- Keep the Idea Graph on React Flow for every supported graph size and remove its automatic Sigma.js rendering branch without changing the existing Sigma.js implementation.
- Add an Idea Graph-local controls drawer for layout and focus controls instead of placing these controls in Project Settings.
- Add a curated React Flow layout registry backed initially by ELK.js algorithms, including layered, force, stress, radial, and deterministic grid layouts with typed parameters and asynchronous preview.
- Add browser-local Graph Layout Presets that users can create, update, duplicate, delete, export as versioned JSON, and import from local JSON files without backend persistence.
- Extend Idea Graph interaction state from one selected node to multiple selected Research Ideas with modifier-click and selection-area interaction.
- Add an N-hop focus projection over selected Research Ideas with configurable radius, traversal direction, and Idea Lineage Edge kinds.
- Separate graph transfer completeness from renderer limits so React Flow can receive a coherent topology for graphs with hundreds of nodes and request a read-only backend neighborhood projection when the full topology is unavailable.
- Preserve last-good graph positions and interaction state across benign refreshes, and reject stale asynchronous layout results.

## Capabilities

### New Capabilities

- `project-web-idea-graph-layout`: React Flow-only Idea Graph layout controls, algorithm previews, performance behavior, and browser-local Graph Layout Preset management, import, and export.

### Modified Capabilities

- `project-web-idea-lineage-selection`: Replace single-node selection assumptions with multi-selection and define N-hop focus projection behavior for selected Research Ideas.
- `project-web-state-management`: Extend the panel-scoped Idea Graph state model to own selected node ids, focus configuration, applied layout configuration, draft layout configuration, and layout job state through typed actions and effect adapters.
- `project-web-idea-graph-refresh`: Preserve valid multi-selection, focus, and applied layout state across benign graph refreshes and prevent stale layout jobs from replacing current positions.
- `topic-graph-read-api`: Decouple Idea Graph topology bounds from renderer choice, report topology completeness, and support coherent full-topology or read-only N-hop neighborhood responses without Sigma.js fallback requirements.

## Impact

The change affects the React Flow Idea Graph panel, graph conversion and layout utilities, panel-scoped interaction state, browser-local persistence and file import/export adapters, TypeScript graph contracts, topic graph API query handling, backend graph pagination or neighborhood projection, UI contract documentation, and unit and browser smoke tests. ELK.js remains the initial layout engine. Sigma.js and Graphology code remain unchanged, and no layout preset, selected-node state, calculated coordinate, or focus state is stored in Workspace Runtime or another backend surface.
