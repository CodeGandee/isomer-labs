## Context

The Project Web Idea Graph currently obtains the `idea-lineage` read model through TanStack Query, converts the response into React Flow nodes and edges, runs one fixed ELK layered layout, and stores the resulting React Flow objects in component state. The graph uses one UI-selected node id and derives direct parent, child, incoming-edge, and outgoing-edge highlights from that selection. A frontend renderer selector and a matching backend sparse-graph limit redirect graphs above 120 nodes toward Sigma.js, while the Sigma.js component assigns random positions.

This change keeps the Idea Graph entirely on React Flow. The existing Sigma.js and Graphology implementation remains untouched and is not an implementation target. The graph must instead remain usable with hundreds of source nodes through complete topology delivery, optional N-hop focus, React Flow visibility controls, stable render objects, and asynchronous layout calculation.

The current graph API pages nodes and keeps only edges whose endpoints occur in the same returned node slice. Fetching those pages independently cannot reconstruct cross-page Idea Lineage Edges, so the browser cannot calculate correct N-hop reachability unless the response declares and supplies a coherent topology. The API therefore needs explicit completeness metadata and a bounded server-side neighborhood projection for graphs that exceed a renderer-independent transfer limit.

Graph layout preferences are frontend presentation data. The canonical Isomer language already uses Default Layout Profile for workspace path mappings, so this feature uses Graph Layout Preset for saved graph algorithm recipes. Presets, draft controls, selected Research Ideas, focus state, coordinates, and viewport state must not become Workspace Runtime or query-index data.

## Goals / Non-Goals

**Goals:**

- Render every supported Idea Graph response with React Flow, independent of node count and legacy renderer hints.
- Let users select and preview curated layout algorithms with safe, typed parameters from an Idea Graph-local controls drawer.
- Keep React Flow responsive while calculating layouts for hundreds of nodes.
- Let users save algorithm recipes as browser-local Graph Layout Presets and exchange them through validated JSON files.
- Support React Flow multi-selection and a deterministic union-based N-hop focus projection over selected Research Ideas.
- Preserve valid selection, focus, applied layout configuration, and last-good positions across benign graph refreshes.
- Give the frontend complete topology when safely bounded and a coherent read-only backend neighborhood projection otherwise.
- Keep graph layout, profile, selection, and focus persistence out of the backend.

**Non-Goals:**

- Changing, optimizing, removing, or adding layout behavior to Sigma.js or Graphology.
- Choosing a renderer dynamically for the Idea Graph.
- Persisting Graph Layout Presets, selected nodes, focus state, manual node positions, or viewport state in Workspace Runtime, the Project Manifest, Research Topic Config, or another backend store.
- Saving an exact graph arrangement or synchronizing presets between browsers or users.
- Exposing arbitrary ELK.js option keys or every algorithm included in the ELK.js bundle.
- Introducing graph editing or mutating Research Ideas and Idea Lineage Edges from React Flow.
- Replacing the existing visible-label search contract.

## Decisions

### 1. Use One React Flow Pipeline for the Idea Graph

The Idea Graph panel will remove its `SigmaGraph` import and renderer-selection branch. It will request `idea-lineage` data for React Flow and render every usable full or projected response inside `ReactFlowProvider`. Compatibility `renderer_hint` values remain parseable but do not select the Idea Graph renderer.

The pipeline becomes:

```text
TanStack Query source graph
        |
        v
eligible source topology
        |
        v
multi-source N-hop focus projection
        |
        v
existing visible-label search
        |
        v
visible graph and dimension signature
        |
        v
layout worker and position map
        |
        v
memoized React Flow nodes and edges
```

React Flow receives `onlyRenderVisibleElements`, memoized custom idea nodes, stable base edge objects, controlled selection state, and zoom-dependent detail reduction. Node or viewport interaction does not choose another renderer.

Alternative considered: retain the automatic Sigma.js fallback for large graphs. This conflicts with the requested React Flow-only scope and makes layout presets and selection behavior renderer-dependent.

### 2. Separate Query-owned Graph Data From Panel Interaction State

TanStack Query remains the owner of graph response nodes, edges, groups, facets, completeness metadata, and diagnostics. The panel-scoped Idea Graph store owns only interaction and derived-result state:

```ts
type IdeaGraphInteractionState = {
  selectedNodeIds: string[];
  focus: {
    enabled: boolean;
    hopRadius: number;
    direction: "incoming" | "outgoing" | "both";
    relationKinds: string[];
  };
  layoutDraft: GraphLayoutConfiguration;
  appliedLayout: GraphLayoutConfiguration;
  appliedPresetId: string | null;
  positionsByNodeId: Record<string, { x: number; y: number }>;
  layoutJob: LayoutJobState;
  hover: IdeaLineageHoverState;
  touchLongPress: TouchLongPressState;
  openIntent: IdeaLineageOpenIntent | null;
};
```

Selected node ids use an ordered unique array because reducer state, tests, and possible panel serialization benefit from JSON-compatible values. Selectors build `Set` values internally when membership lookup matters.

Pure selectors derive the eligible topology, N-hop projection, visible-label search result, direct-neighborhood highlights, React Flow render data, and layout input fingerprint. Effects own graph fetching, worker messages, localStorage, file import and export, timers, and workbench open commands.

Alternative considered: copy the full source graph into the interaction store. This would duplicate TanStack Query state and make refresh identity and last-good behavior harder to reason about.

### 3. Define Multi-selection Independently of React Flow Internals

The application store is authoritative for selected Research Idea ids. React Flow receives `selected` flags derived from that store and reports user intent through typed handlers. An unmodified single click replaces the set, Ctrl-click or Command-click toggles membership, and selection-area completion replaces or adds according to the active gesture. Clear Selection empties the set. Double-click opens the targeted idea without implicitly discarding other selections.

Direct-neighborhood styling is calculated from the union of selected nodes. Selected styling has precedence when a node is also another selected node's direct parent or child. Backend idea status remains represented by separate classes and never populates UI selection.

React Flow's `selectionOnDrag`, `multiSelectionKeyCode`, selection change callbacks, and controlled node data provide the interaction primitives. Pointer and double-click guards remain necessary so selection-area interaction, node opening, hover preview, and touch long press do not produce duplicate commands.

Alternative considered: trust React Flow's internal selected flags as the source of truth. This would conflict with panel-scoped reducers, focus derivation, refresh repair, and existing declarative highlight requirements.

### 4. Use Deterministic Multi-source BFS for N-hop Focus

For complete client topology, a pure projection function constructs adjacency lists from Idea Lineage Edges after relation-kind filtering and runs breadth-first search with all selected node ids at distance zero. Nodes with shortest distance less than or equal to the requested radius form the visible focus node set.

Direction has mechanical traversal semantics:

- `incoming`: traverse an edge from target to source.
- `outgoing`: traverse an edge from source to target.
- `both`: add both adjacency directions while preserving the edge's rendered direction.

The default projected edge set is induced: every eligible Idea Lineage Edge whose endpoints are both visible. Stable node and edge ids are sorted before traversal so diagnostics, tests, and layout input fingerprints remain deterministic. Radius zero returns the valid selected seeds only. Multiple seeds always mean union in this change; intersection and connecting-path modes remain future capabilities.

The existing visible-label search runs after focus projection. Search can hide focused nodes and their attached edges, but it does not alter traversal distances. Clearing search restores the current focused result.

Alternative considered: run N-hop traversal after visible-label search. That can break valid paths because intermediate nodes hidden by text search disappear from the traversal topology.

### 5. Use a Curated Versioned Layout Registry

A frontend registry defines stable public algorithm ids, configuration versions, labels, descriptions, parameter schemas, safe bounds, defaults, compatibility checks, and worker mappings. Initial algorithms are:

| Public ID | Engine Mapping | Intended Use | Initial Parameters |
| --- | --- | --- | --- |
| `layered` | `org.eclipse.elk.layered` | Directed Idea Lineage DAG | direction, node spacing, layer spacing, edge routing |
| `force` | `org.eclipse.elk.force` | Dense relationship exploration | model, iterations, repulsion, temperature, random seed |
| `stress` | `org.eclipse.elk.stress` | Balanced general relationship view | desired edge length, iteration limit, epsilon, random seed |
| `radial` | `org.eclipse.elk.radial` | Exploration around selected ideas or graph roots | radius, compaction, center behavior, random seed |
| `grid` | built-in deterministic adapter | Fast fallback and auditing | columns, horizontal spacing, vertical spacing, sort key |

The public parameter model does not expose raw ELK.js keys. Each registry entry maps its validated configuration to engine options. This keeps exported presets stable across engine upgrades and prevents imports from enabling unknown or expensive options.

Radial layout uses one selected seed as its center when exactly one exists. With multiple selected seeds or multiple source roots, the worker may add a virtual layout-only root connected to candidate centers. The virtual root never appears in React Flow and never changes the Idea Lineage Edge model.

All nondeterministic adapters sort input ids and receive a stored random seed. Grid is implemented as a small local adapter instead of using ELK Box because the application needs explicit column count and stable semantic sorting.

Alternative considered: add Dagre, D3 Force, Cytoscape, or ForceAtlas2 immediately. ELK.js is already a direct dependency and supplies the required initial algorithm families. Additional engines can be registered later if measured quality justifies their dependency and adapter cost.

### 6. Run Layout Through a Typed Worker Boundary

The frontend will create a dedicated layout worker module. The main thread sends a structured-clone-safe request containing job id, input fingerprint, algorithm id and version, validated parameters, normalized node dimensions, and stable node and edge identities. The worker returns positions, bounds, duration, and safe diagnostics.

```ts
type LayoutRequest = {
  jobId: number;
  inputFingerprint: string;
  algorithm: GraphLayoutConfiguration;
  nodes: Array<{ id: string; width: number; height: number }>;
  edges: Array<{ id: string; source: string; target: string }>;
};

type LayoutResult = {
  jobId: number;
  inputFingerprint: string;
  positions: Record<string, { x: number; y: number }>;
  bounds: { width: number; height: number };
  elapsedMs: number;
  diagnostics: LayoutDiagnostic[];
};
```

The panel accepts a result only when both job id and input fingerprint match the current job. Starting a new job cancels or supersedes the old job. Closing the panel terminates its worker or releases its shared-worker subscription. Errors retain the last-good position map.

The initial built-in layered configuration runs automatically when the panel first obtains a visible topology. User edits remain in `layoutDraft` until Preview Layout succeeds. A successful preview becomes `appliedLayout`; saving a preset serializes the applied configuration, not an unpreviewed draft.

Layout input fingerprinting uses visible node ids, edge ids and endpoints, normalized dimensions, and the applied algorithm configuration. It excludes timestamps, hover, selection styling when focus is disabled, viewport, and progress state. An in-memory result cache keyed by this fingerprint can avoid repeat calculations, but coordinates are not written to browser-local persistent storage.

Idea cards will use normalized layout dimensions shared by CSS, React Flow conversion, and the worker. Visible label content is clamped within the card contract so the worker's dimensions match rendered bounds. This removes the current mismatch between the ELK `250 x 90` assumption and the React Flow node's styled width.

Alternative considered: call ELK directly from React effects. Promise-based calls still compete with UI work and offer weak cancellation for large jobs.

### 7. Keep Graph Controls Inside the Idea Graph Panel

`IdeaGraphPanel` owns a Graph Controls trigger and a collapsible local drawer with Focus and Layout sections. On wide panels, the drawer shares horizontal space with the canvas. On narrow panels, it becomes a bounded overlay or stacked region without moving controls into Project Settings.

The Focus section shows selected-seed chips, Clear Selection, enabled state, hop radius, direction, relation kinds, Exit Focus, and source-versus-visible counts. The Layout section shows preset selection, algorithm selection, typed parameters, Preview Layout, Revert Draft, Save as Preset, preset management, import, export, job status, duration, and diagnostics.

The controls display an unsaved marker when the applied configuration no longer matches its originating preset or when the preset was removed in another browser tab. Deleting that preset does not invalidate an already applied configuration.

Alternative considered: add controls to Project Settings. Layout and focus are contextual graph operations, and moving them global would obscure which open panel receives a change.

### 8. Store Algorithm Recipes as Graph Layout Presets

The persistence adapter owns a single versioned catalog under a namespaced localStorage key such as `isomer-web-idea-graph-layout-presets-v1`. Built-in presets live in source code and are immutable. User-defined presets use generated stable ids and the following external shape:

```json
{
  "kind": "isomer.idea-graph-layout-preset",
  "schema_version": 1,
  "preset_id": "generated-id",
  "name": "Wide horizontal lineage",
  "graph_kind": "idea-lineage",
  "algorithm": {
    "id": "layered",
    "config_version": 1,
    "parameters": {
      "direction": "right",
      "node_spacing": 60,
      "layer_spacing": 120,
      "edge_routing": "orthogonal"
    }
  },
  "viewport": {
    "fit_after_layout": true,
    "padding": 0.2
  }
}
```

Zod schemas validate storage reads, imports, and registry-specific parameters. Corrupt storage falls back to an empty user catalog and produces a safe GUI diagnostic. Storage events refresh other open tabs after validation. Quota failures leave the prior catalog intact and report an error.

Export uses Blob and browser download behavior for broad compatibility. Import uses a user-selected JSON file. A catalog wrapper can export multiple presets. Files have discriminator and schema-version checks, bounded byte size, bounded preset count, and bounded strings. Conflicting ids import as new copies by default. Unknown future versions are rejected rather than partially interpreted. The File System Access API is optional progressive enhancement, not a dependency.

Presets store algorithm recipes and optional fit behavior only. They do not store positions, source graph data, topic identity, selected seeds, focus settings, credentials, or renderer choice.

Alternative considered: persist exact positions. Position snapshots are graph-revision-specific, potentially large, and semantically different from reusable algorithm recipes.

### 9. Make Topology Completeness Explicit in the Graph API

The backend will split the existing `SPARSE_GRAPH_LIMIT` responsibilities. React Flow suitability will no longer bound `idea-lineage` responses. A renderer-independent transfer policy will govern complete graph delivery and read-only neighborhood projection.

Ordinary `idea-lineage` responses add fields equivalent to:

```json
{
  "topology_complete": true,
  "total_node_count": 438,
  "total_edge_count": 612
}
```

When `topology_complete` is true, all eligible edges for the declared source scope have returned endpoints. When a transfer limit, cursor, or other bound omits nodes or cross-boundary edges, the response reports `topology_complete: false`, total counts, and diagnostics. The frontend must not merge the current node pages and assume topology completeness.

For hundreds of nodes, the normal path requests and receives a complete renderer-neutral topology. Exact transfer limits remain configuration constants and will be calibrated with fixture and browser performance checks rather than being named as React Flow limits.

When a graph is incomplete and the user enables focus, the frontend requests a bounded backend neighborhood projection with selected node ids, hop radius, direction, relation kinds, and edge mode. The transport can use repeated GET query parameters while seed-count and URL-size bounds remain small. If those bounds prove insufficient, the same read-only semantics can move to a body-bearing query endpoint without changing the projection model.

The projection response records resolved and unresolved seeds, projection parameters, source and visible counts, source index revision, and completeness for the projected scope. Backend BFS uses the same traversal semantics as the client and returns induced edges by default. Shared conformance fixtures ensure the client and backend projection functions agree.

Alternative considered: always compute N-hop focus in the browser. That is correct only when the browser has complete topology, which current pagination does not guarantee.

### 10. Preserve Refresh and Layout Stability by Fingerprint

The existing graph content signature expands to include topology completeness and any projection identity that changes traversal meaning while continuing to ignore response timestamps and order. Source refresh follows these rules:

- If effective source content, focus projection, and applied layout fingerprint are unchanged, preserve React Flow objects and positions.
- If source content changes outside the visible focus projection, update query data and counts without relayout.
- If visible topology changes, rebuild only affected render data and run the applied layout configuration.
- Remove missing selected ids individually; retain remaining selections and recalculate focus.
- Keep last-good graph and positions during loading, transient empty data, failed refresh, or failed layout.
- Preserve an unapplied draft independently from the applied layout during refresh.
- Discard any worker result whose job id or fingerprint is stale.

Alternative considered: relayout on every successful refetch. That causes visual instability and repeats expensive work when only transport metadata changes.

## Risks / Trade-offs

- [Risk] React Flow uses DOM nodes and SVG edges, so a complete graph with hundreds of rich cards can still become slow. → Mitigation: project N-hop focus before conversion, enable visible-element rendering, memoize node components, preserve object identity, reduce low-zoom labels, benchmark fixture sizes, and warn at explicit safety bounds without renderer switching.
- [Risk] One high-degree seed can make a one-hop projection nearly as large as the source graph. → Mitigation: show projected counts before or during application, enforce explicit renderer-independent node and edge safety bounds, and return incomplete diagnostics instead of silent trimming.
- [Risk] ELK force, stress, or radial algorithms may produce surprising layouts for a directed DAG. → Mitigation: keep layered as the built-in default, describe algorithm intent, use deterministic seeds, provide Preview and Revert, and retain the last-good positions on error.
- [Risk] Browser worker bundling or teardown can leak work after a Dockview panel closes. → Mitigation: use typed job ownership, terminate or unsubscribe on panel disposal, and add lifecycle tests that confirm late results cannot dispatch into a disposed store.
- [Risk] Client and backend N-hop semantics can diverge. → Mitigation: define direction and induced-edge rules in one contract and run shared graph fixtures through both implementations.
- [Risk] Browser-local preset data can be corrupt, oversized, or cleared by the user. → Mitigation: validate every read, cap import size and count, retain immutable built-in presets, provide export, and treat browser-local persistence as a convenience rather than research truth.
- [Risk] A future ELK.js upgrade can change engine option behavior. → Mitigation: keep stable public algorithm ids, version each algorithm configuration, map friendly parameters through adapters, and add migration functions before accepting older preset versions.
- [Risk] Complete topology responses can increase API payload size. → Mitigation: use a renderer-independent transfer bound, compressed API responses, total counts and completeness metadata, and backend neighborhood projection beyond the bound.
- [Risk] Selection-area gestures can conflict with panning, node dragging, double-click opening, and touch long press. → Mitigation: define gesture precedence, use React Flow's selection and multi-selection properties, preserve the existing pointer guards, and cover mouse, keyboard modifier, and touch behavior in browser tests.

## Migration Plan

1. Add backward-compatible graph response fields for topology completeness and total counts, split renderer and transfer constants, and add backend projection tests before the frontend depends on the new fields.
2. Add frontend schemas that accept the new fields while safely treating older responses as incomplete unless existing paging metadata proves completeness.
3. Extend the panel store and pure selectors for ordered multi-selection, focus configuration, client BFS, and refresh repair while retaining the current single-click behavior as the default replace gesture.
4. Add the layout registry, worker protocol, built-in layered configuration, and position fingerprinting. Keep the existing layout path available behind an internal migration boundary until worker parity tests pass.
5. Add the local Graph Controls drawer, React Flow controlled multi-selection, N-hop focus, visible-element rendering, layout preview, and responsive behavior.
6. Add the Graph Layout Preset persistence and file exchange adapter under a new storage key. No existing browser setting requires migration.
7. Remove the Idea Graph's `SigmaGraph` import and renderer-selection branch after the React Flow path passes unit, integration, responsive, and browser smoke tests. Do not edit the Sigma.js component.
8. Update `docs/ui/contracts/topic-graph.md`, rebuild packaged static assets, and run `pixi run lint`, `pixi run typecheck`, `pixi run test`, frontend tests, and targeted browser smoke checks.

Rollback can restore the previous Idea Graph panel bundle because the existing Sigma.js component remains present. The added API fields are backward-compatible for older frontends, while the renderer-independent limit must continue returning contract-compatible bounded data. No database, Workspace Runtime, Project Manifest, or Research Topic Config migration is required.

## Open Questions

- What complete-topology node, edge, payload-byte, hop-radius, and seed-count safety defaults provide acceptable behavior on supported development machines? Implementation should establish these values through fixtures and browser profiling, then document them as configurable policy rather than renderer identity.
- Should low-zoom detail reduction initially hide only edge labels, or also replace full idea cards with compact custom nodes below a zoom threshold? The first implementation can start with edge-label reduction and add compact nodes only if profiling shows a clear benefit.
- Should a future capability persist panel focus state in browser history for bookmarkable neighborhood views? This change keeps focus and selected seeds panel-scoped and excludes them from Graph Layout Presets.
