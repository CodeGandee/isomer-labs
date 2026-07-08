## 1. State Store Foundation

- [x] 1.1 Add a small RxJS-backed Project Web state-store utility that supports typed actions, reducer transitions, subscriptions, and a React hook based on `useSyncExternalStore`.
- [x] 1.2 Add unit tests for dispatch order, reducer output, selector subscription behavior, and cleanup on unmount.
- [x] 1.3 Document the state ownership taxonomy in code near the store utility so future GUI work can classify state before adding new stores.
- [x] 1.4 Add a panel-scoped store registry keyed by Dockview panel id, with cleanup for subscriptions, timers, and interaction state when the panel closes.

## 2. Idea Lineage State Model

- [x] 2.1 Create an idea lineage feature module for actions, state types, reducer, selectors, and interaction effects.
- [x] 2.2 Implement selection actions that store the selected node id and derive direct parent nodes, direct child nodes, incoming edges, and outgoing edges from graph data.
- [x] 2.3 Implement hover actions for pending preview, visible preview, close delay, touch long press start, touch long press cancel, and open-node cleanup.
- [x] 2.4 Add pure reducer tests for single-click selection, hover delay completion, hover close, double-click open cleanup, and touch long press cancellation.
- [x] 2.5 Add selector tests that verify selected-neighborhood render state and preserve identity for unaffected nodes and edges.

## 3. ReactFlow Migration

- [x] 3.1 Split the current idea graph code out of `App.tsx` into an idea lineage container, ReactFlow view, hover preview view, and graph render selectors.
- [x] 3.2 Replace component-local selection and hover state in the idea lineage graph with the new typed interaction store.
- [x] 3.3 Remove direct ReactFlow edge DOM class mutation and represent edge highlights through declarative ReactFlow edge render state while preserving object identity for unaffected edges.
- [x] 3.4 Keep hover preview loading, Markdown rendering, scroll behavior, touch long press behavior, and double-click open behavior equivalent to the current UI.
- [x] 3.5 Keep workbench opening behavior behind typed commands instead of calling Dockview APIs from graph rendering components.
- [x] 3.6 Add a measured fallback task only if needed: implement a state-derived edge highlight overlay when declarative edge render state causes unacceptable churn in tests or profiling.

## 4. Workbench and Settings Boundaries

- [x] 4.1 Keep TanStack Query as the source for backend graph, record, idea, and topic data during the migration.
- [x] 4.2 Keep URL/history updates inside the existing workbench navigation boundary and avoid duplicating navigation state in feature stores.
- [x] 4.3 Keep persisted GUI settings behind the settings provider or a settings store API and make graph interaction effects read hover delay from that boundary.
- [x] 4.4 Ensure RxJS writable streams remain in event boundary modules or feature effects rather than being exported from rendering components.
- [x] 4.5 Leave broader Workbench state in `Workbench` for this change, except for small adapters needed to create, resolve, and dispose panel-scoped idea lineage stores.

## 5. Verification

- [x] 5.1 Add a regression test that selects an idea node, opens or loads a hover preview, and verifies selected node, parent node, child node, incoming edge, and outgoing edge highlights remain visible.
- [x] 5.2 Add a regression test that unrelated graph nodes and edges keep stable render object identity when the selected node changes.
- [x] 5.3 Add a regression test that opening an idea emits a typed workbench command and clears hover preview state.
- [x] 5.4 Run the focused frontend tests for idea graph, settings, state store, and view-model behavior.
- [x] 5.5 Run the full frontend test suite and rebuild packaged static assets.
