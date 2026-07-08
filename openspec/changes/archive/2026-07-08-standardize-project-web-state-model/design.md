## Context

Project Web has grown from a read-only topic browser into an IDE-like research workbench with Dockview tabs, graph viewers, Markdown and JSON viewers, server-sent invalidations, browser history, theme/settings, and future tmux control. Current state is split across TanStack Query, URL helpers, Dockview, React component state, refs, RxJS subjects, localStorage-backed contexts, and in at least one case direct ReactFlow DOM class mutation.

The most important failure mode is split ownership: a visual state can appear selected because a DOM class was toggled, while the React state and ReactFlow props do not know it is selected. Any later render from hover preview, query updates, theme changes, layout changes, or ReactFlow internals can erase that state.

## Goals / Non-Goals

**Goals:**

- Define a state ownership rule for Project Web so new GUI work knows where state belongs.
- Keep TanStack Query as the only owner of backend-fetched data and avoid copying query data into feature stores unless the user is editing a draft.
- Keep URL/history state as the durable navigation contract for selected topic, graph scope, and opened item.
- Use typed actions and reducers for shared, durable, or complex interaction state, starting with idea lineage selection and hover behavior.
- Use RxJS for cross-component commands, async event streams, timers, server invalidations, manual refresh, and future tmux/ag-ui flows.
- Ensure ReactFlow node and edge visuals are derived from explicit interaction state and graph data, not from direct DOM mutation.
- Split Project Web into feature modules with state selectors and tests that can be verified without rendering the whole app.

**Non-Goals:**

- Do not replace TanStack Query, Dockview, ReactFlow, or the existing UI component library.
- Do not force every text input, modal tab, or transient focus flag through RxJS.
- Do not introduce Redux or another global state library for this change.
- Do not redesign the backend API or research record schema.

## Decisions

### Use a state ownership taxonomy

Project Web state will be classified before implementation:

| State category | Owner | Examples |
|---|---|---|
| Backend data | TanStack Query | project summary, topic graph, records, idea detail |
| Durable navigation | URL/history state | topic id, graph scope, open item |
| Workbench layout mechanics | Dockview adapter | tabs, active panel, panel close/focus |
| Cross-component commands and external events | RxJS streams | open record, refresh topic, SSE invalidation, future tmux commands |
| Persisted GUI preferences | settings store/context | theme, hover preview delay |
| Complex per-view interaction | feature store/reducer | selected graph node, hover pending/visible state, touch long press |
| Private disposable UI | local component state | active JSON modal tab, current search input draft |

Alternative considered: make RxJS the only way state changes. That gives a single event channel, but it makes local form state and simple modal state too costly to write and test. The chosen rule keeps RxJS for shared/effectful flows while preserving simple local React state where it is private.

### Introduce typed action stores for complex interaction state

Feature interaction state will use typed actions plus reducer-style transitions. Implement a small RxJS-backed store that exposes `dispatch(action)`, `state$`, and a React hook built on `useSyncExternalStore`; pure reducers and selectors remain testable without React.

The idea lineage graph will start with an interaction model similar to:

```ts
type IdeaLineageState = {
  selectedNodeId: string | null;
  hover:
    | { status: "idle" }
    | { status: "pending"; nodeId: string; x: number; y: number }
    | { status: "visible"; nodeId: string; x: number; y: number };
};
```

Actions include node selection, double-click open intent, hover start, hover delay elapsed, hover close, touch long press start/cancel, and graph data replacement. Effects handle timers and commands such as opening a tab. Components dispatch actions and render selected state; they do not own state transitions.

Alternative considered: use a plain `useReducer` inside `IdeaGraphPanel`. That would fix the immediate graph bug, but it would not establish a reusable pattern for future tmux, command routing, and multi-tab viewer coordination.

### Scope per-tab stores to Dockview panel identity

Per-tab feature stores will be created and disposed with a Dockview panel id. The store can keep the openable item id as metadata, but the panel id is the lifetime owner because users may keep several tabs open for the same semantic item or reopen an item into a fresh tab lifecycle later.

Alternative considered: scope stores by openable item id. That makes semantic lookup simple, but it risks leaking state between tabs that should be independent and makes panel close cleanup less direct.

### Derive visual render state from source data plus interaction state

Graph rendering will use selectors that combine `TopicGraphView` data with `IdeaLineageState` to produce render props:

```text
graph data + selectedNodeId
  -> selected node id
  -> parent node ids
  -> child node ids
  -> incoming edge ids
  -> outgoing edge ids
  -> ReactFlow nodes and declarative ReactFlow edge classes
```

The first implementation will remove direct edge DOM class toggling and use declarative ReactFlow edge classes with object identity preserved for unaffected edges. If profiling or regression tests show unacceptable edge churn, render selected edge highlights in a small overlay layer while leaving base edges stable.

Alternative considered: reapply DOM classes after every hover or render. That keeps the current optimization but preserves the split-source bug and can still flicker.

### Migrate only idea lineage state in this change

This change will prove the state model by migrating idea lineage graph interaction state first. Workbench URL/history state, Dockview panel management, explorer expansion, mobile explorer visibility, and settings state stay in their existing boundaries unless a small adapter is required for the idea lineage migration.

Alternative considered: move all Workbench state into the new model immediately. That would be cleaner on paper, but it increases blast radius and delays the bug fix that motivated the change.

### Keep effects at module boundaries

State reducers should not call Dockview, browser history, fetch APIs, or `localStorage` directly. Effects and adapters translate actions into side effects:

- Workbench effects open/focus/close Dockview panels and sync browser history.
- Query effects invalidate TanStack Query data from SSE, manual refresh, and future backend events.
- Interaction effects manage hover timers and emit open commands after double-click.
- Settings effects read/write persisted preferences.

This keeps deterministic state transitions small and makes side effects easy to test with mocked adapters.

## Risks / Trade-offs

- [Risk] Adding a store layer could make simple components harder to read. → Mitigation: only shared, durable, or complex interaction state must use typed action stores; private disposable state stays local.
- [Risk] RxJS misuse could recreate the same scattered state problem with subjects everywhere. → Mitigation: create named feature stores and avoid exporting raw writable subjects except at explicit event boundaries.
- [Risk] ReactFlow performance may suffer if all edges receive new objects on every selection. → Mitigation: selectors preserve object identity for unaffected nodes/edges, and an overlay highlight layer remains the fallback for large graphs.
- [Risk] Migration can touch many lines in `App.tsx`. → Mitigation: migrate by feature module, beginning with idea lineage graph interactions, then move workbench state and settings only after tests cover the graph.

## Migration Plan

1. Add a small state-store utility and tests for reducer/action dispatch and React subscription behavior.
2. Move idea lineage graph interaction state into a feature module with reducer, actions, effects, and selectors.
3. Replace direct ReactFlow DOM class mutation with derived declarative node and edge state or a highlight overlay.
4. Split `IdeaGraphPanel` into a container component, view component, hover preview component, and graph-render selectors.
5. Add regression tests for hover after selection, node selection identity preservation, edge highlight persistence, touch long press, and double-click open behavior.
6. Keep existing user-facing behavior and URLs stable during the migration.

## Resolved Questions

- Selected edge highlights will use declarative ReactFlow edge classes first, with an overlay reserved as a measured fallback.
- Per-tab feature stores will be scoped to Dockview panel id, with openable item id recorded as metadata.
- This change will migrate idea lineage interaction state first and leave broader Workbench state in place.
