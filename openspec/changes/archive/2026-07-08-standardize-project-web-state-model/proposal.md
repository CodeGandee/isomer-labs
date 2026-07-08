## Why

The Project Web GUI now mixes backend cache state, URL state, Dockview state, RxJS events, component-local interaction state, and imperative DOM mutations inside large React components. This makes bugs such as hover-triggered graph highlight loss likely because the same visual state is split across React state and out-of-band DOM state.

## What Changes

- Add a principled Project Web state model that defines which state belongs to TanStack Query, URL history, Dockview adapters, persisted settings, RxJS actions, per-view interaction stores, and local component state.
- Introduce typed action/reducer boundaries for shared, durable, or complex GUI interactions, starting with idea lineage graph selection, hover preview, touch long press, and highlight state.
- Require visual state such as selected nodes, parent/child highlights, and adjacent edge highlights to be derived from explicit state instead of direct DOM mutation.
- Keep RxJS as the event/effect spine for cross-component commands, server events, manual refresh, future tmux control, and delayed interactions, without forcing trivial private input state through streams.
- Use declarative ReactFlow edge render state first for idea lineage highlights, scope tab interaction stores by Dockview panel id, and keep the initial migration focused on idea lineage state.
- Split oversized Project Web components into feature modules with selectors and tests that prove state transitions, derived render data, and event effects separately.

## Capabilities

### New Capabilities

- `project-web-state-management`: Defines Project Web GUI state ownership, action flow, interaction stores, derived render state, and tests for state correctness.

### Modified Capabilities

- None.

## Impact

- Affects `web/ui/src/App.tsx`, Project Web feature module boundaries, graph utilities, tests, and static frontend assets.
- Adds a small observable store or reducer bridge for typed state/actions, likely using existing RxJS and React `useSyncExternalStore` patterns rather than introducing Redux.
- Preserves TanStack Query as the owner of backend data and keeps Dockview as the owner of tab layout mechanics behind a workbench adapter.
