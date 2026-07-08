## Context

The idea lineage graph currently renders `GraphFiltersBar`, which exposes `search`, `status`, `relation`, and `Supporting Records`. That component is shared with dense graph panels, but the idea lineage graph is a user-facing idea map where users expect a simple search over ideas rather than low-level graph-query controls.

The backend already supports node-only substring search through `_filter_nodes()` and `_node_haystack()`, but that search is exact substring matching and every change refetches graph data. Idea lineage nodes are already loaded into the frontend before ReactFlow layout, so fuzzy filtering can run locally for a smoother interaction.

## Goals / Non-Goals

**Goals:**
- Replace the idea lineage controls with one search input.
- Use Fuse.js to fuzzy-match already-loaded idea node data.
- Filter nodes only and derive visible edges from visible node ids.
- Keep supporting records out of the idea lineage overview graph.
- Preserve dense graph filter controls outside the idea lineage view.

**Non-Goals:**
- Do not remove backend graph filtering parameters.
- Do not remove `GraphFiltersBar` from dense graph views.
- Do not add supporting-record expansion controls to the graph.
- Do not change idea detail payload shape unless a test exposes a missing already-loaded field.
- Do not implement global project search.

## Decisions

Use Fuse.js in the frontend for idea lineage node filtering. Fuse.js fits this view because the graph already has the node list in memory, the expected node count is sparse compared with experiment/paper graphs, and the user gets instant fuzzy search without backend round trips. MiniSearch is better for a larger document index, and RapidFuzz would move an interactive UI concern into the Python backend.

Add a dedicated idea-lineage search component instead of changing `GraphFiltersBar`. Dense graph panels still use `GraphFiltersBar`, while `IdeaLineagePanel` renders a single search input with an accessible label such as `Search ideas`. This avoids weakening dense graph exploration while simplifying the idea map.

Keep the backend graph request for idea lineage stable and overview-only. The request should pass `includeSecondary: false` and omit `status`, `relationKind`, and `producer` filters. The backend can keep its current graph search capability for API compatibility, but the simplified UI should not rely on it for idea lineage search.

Filter after graph payload fetch and before ReactFlow layout. Build a Fuse index from the loaded graph nodes and fields that describe the node: `id`, `record_id`, `idea_id`, `title`, `one_liner`, `summary`, `status`, `producer`, `skill`, `material_kind`, and already-loaded refs or realization hints when present. After matching nodes, keep only edges whose `source` and `target` are both still visible, then reuse the existing layout conversion.

Use conservative Fuse options. Start with weighted keys that prefer `title`, `one_liner`, and `summary`; use a threshold that tolerates small typos without turning short queries into noisy matches. Keep exact substring behavior naturally strong by including the same text fields in the Fuse document.

## Risks / Trade-offs

- Short fuzzy queries can match too much -> require trimming empty input and tune threshold/min match behavior in tests.
- Client-side filtering means the graph summary should describe visible nodes, not all fetched nodes -> compute summary from the filtered graph data or keep the existing summary clear enough for the visible graph.
- Fuse.js adds a frontend dependency -> add it through `npm install fuse.js` and commit `package-lock.json`.
- Filtering after layout can produce stale hidden edges if not done carefully -> filter graph payload before `layoutFlowGraph()` and add tests for edge pruning.

## Migration Plan

1. Add `fuse.js` to `web/ui`.
2. Add a dedicated idea-lineage search component or inline search control in `IdeaLineagePanel`.
3. Replace the idea lineage `GraphFiltersBar` usage with the single search control.
4. Keep the idea lineage query parameters overview-only with `includeSecondary: false`.
5. Add Fuse.js node filtering and edge pruning before layout.
6. Update tests for the simplified controls, fuzzy matching, and edge pruning.

## Open Questions

- None. The intended UX is a single fuzzy node search, no supporting-record toggle, and detail views for supporting records.
