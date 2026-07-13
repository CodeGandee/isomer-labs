## 1. Graph Contract and Topology Completeness

- [x] 1.1 Extend the Python graph response models with topology completeness, total node and edge counts, and optional neighborhood projection metadata while preserving renderer-neutral payloads.
- [x] 1.2 Extend the TypeScript and Zod graph schemas with the same completeness and projection fields, including safe compatibility handling for older responses.
- [x] 1.3 Split the backend sparse renderer constant into renderer-independent complete-transfer and neighborhood safety policies, and stop rejecting `idea-lineage` requests solely because React Flow was requested above 120 nodes.
- [x] 1.4 Make ordinary bounded `idea-lineage` responses report correct complete or incomplete topology and ensure complete responses include every eligible edge between returned nodes.
- [x] 1.5 Add backend unit tests for complete topology, incomplete or paged topology, total counts, legacy renderer parameters, removed graph scopes, and read-only behavior.

## 2. Read-only Backend Neighborhood Projection

- [x] 2.1 Define and validate bounded graph query inputs for repeated selected seed ids, nonnegative hop radius, incoming, outgoing, or both direction, relation kinds, and induced or traversal edge mode.
- [x] 2.2 Implement deterministic backend multi-source BFS with relation filtering before traversal, union semantics, unresolved-seed diagnostics, and induced edges by default.
- [x] 2.3 Return projection identity, resolved and unresolved seeds, direction, radius, relation kinds, source counts, visible counts, source index revision, and projected-scope completeness without writing Workspace Runtime or query-index state.
- [x] 2.4 Add backend projection tests for zero hops, multiple seeds, every direction, relation filtering, induced edges, unknown seeds, cycles or malformed edges, and configured safety-bound failures.
- [x] 2.5 Add shared graph fixtures that can verify equivalent client and backend N-hop projection results.

## 3. Panel State, Multi-selection, and Client Focus

- [x] 3.1 Extend the panel-scoped Idea Graph interaction state and typed actions from one selected node id to ordered unique selected node ids, focus configuration, layout draft, applied layout, applied preset identity, positions, and layout job state.
- [x] 3.2 Update selection and direct-neighborhood selectors to derive union highlights with selected styling precedence while preserving backend status styling and stable unaffected render objects.
- [x] 3.3 Implement a pure deterministic client multi-source BFS selector with zero-hop, incoming, outgoing, both, relation filtering, induced-edge, source-count, and visible-count behavior.
- [x] 3.4 Compose focus projection before the existing visible-label search and add tests proving search does not change hop reachability and clearing search restores the focused result.
- [x] 3.5 Add reducer and selector tests for replace, modifier-toggle, area selection, clear, seed removal, exit focus, targeted open intent, missing-node repair, and hover or touch state independence.

## 4. Layout Registry and Worker

- [x] 4.1 Define versioned public layout configuration schemas, safe parameter bounds, built-in defaults, normalized node dimensions, diagnostics, and registry metadata for layered, force, stress, radial, and grid algorithms.
- [x] 4.2 Implement validated mappings from public layered, force, stress, and radial parameters to existing ELK.js algorithms without accepting arbitrary engine option keys.
- [x] 4.3 Implement deterministic grid layout and radial virtual-root preparation without adding virtual nodes or edges to React Flow graph data.
- [x] 4.4 Add the structured-clone-safe layout worker request and result protocol with job identity, input fingerprint, bounds, duration, and safe diagnostics.
- [x] 4.5 Run ELK.js and grid layout through the worker boundary, support cancellation or supersession, and terminate worker ownership when the Dockview panel closes.
- [x] 4.6 Implement visible-topology and applied-configuration fingerprinting, last-good position retention, stale-result rejection, and optional in-memory layout result caching.
- [x] 4.7 Align Idea Graph card CSS and React Flow conversion dimensions with worker layout dimensions so calculated bounds match rendered nodes.
- [x] 4.8 Add layout registry, mapping, deterministic seed, grid, virtual-root, worker lifecycle, failure, cancellation, fingerprint, and stale-result unit tests.

## 5. Browser-local Graph Layout Presets

- [x] 5.1 Define Zod schemas and TypeScript types for versioned Graph Layout Presets and preset catalogs, excluding graph data, topic identity, selection, focus, coordinates, credentials, and renderer choice.
- [x] 5.2 Implement immutable built-in presets and a dedicated browser-local persistence adapter with validated reads, atomic catalog writes, quota diagnostics, and storage-event synchronization.
- [x] 5.3 Implement create, duplicate, rename, update, and delete operations for user-defined presets while requiring built-in changes to save as user-defined copies.
- [x] 5.4 Implement bounded JSON export for one preset and the user catalog through browser download behavior.
- [x] 5.5 Implement bounded local JSON import with discriminator and version validation, algorithm-specific parameter validation, conflict-as-copy behavior, and safe result diagnostics.
- [x] 5.6 Add persistence, corrupt storage, quota failure, cross-tab refresh, CRUD, immutable built-in, export, valid import, conflicting id, unsupported version, and oversized import tests.

## 6. React Flow Idea Graph Controls and Interaction

- [x] 6.1 Remove the Idea Graph's Sigma.js import and node-count or renderer-hint branch so every usable `idea-lineage` response renders through React Flow without editing the Sigma.js component.
- [x] 6.2 Add controlled React Flow multi-selection with replace click, Ctrl or Command toggle, selection-area behavior, Clear Selection, selected-node chips, and targeted double-click opening.
- [x] 6.3 Add the collapsible Idea Graph-local Graph Controls surface with responsive Focus and Layout sections while keeping all controls out of Project Settings.
- [x] 6.4 Add Focus controls for selected seeds, enabled state, hop radius, direction, relation kinds, Exit Focus, and visible-versus-source counts, including the no-valid-seed state.
- [x] 6.5 Add Layout controls for preset choice, algorithm choice, parameter forms, unapplied draft indication, Preview Layout, Revert Draft, save and management actions, import, export, progress, duration, and diagnostics.
- [x] 6.6 Apply the built-in layered configuration on initial topology, require explicit preview for user draft changes, and make a successful preview the applied configuration used by later refreshes.
- [x] 6.7 Enable React Flow visible-element rendering, memoized custom idea nodes, stable edge objects, and low-zoom edge-label reduction without rerunning layout on selection, hover, pan, or zoom.
- [x] 6.8 Add responsive styling and accessibility labels, focus order, keyboard interaction, live job status, and error announcements for Graph Controls and multi-selection.

## 7. Data Fetching and Refresh Stability

- [x] 7.1 Update the frontend graph API client and query keys to request coherent React Flow Idea Graph topology and bounded backend neighborhood projections when source topology is incomplete.
- [x] 7.2 Keep complete-topology N-hop projection client-side and switch to the read-only backend projection only when completeness metadata requires it, preserving identical projection semantics.
- [x] 7.3 Extend graph content and layout signatures with topology and projection identity while continuing to ignore response timestamps, payload ordering, hover, viewport, and other visual-only metadata.
- [x] 7.4 Preserve still-valid selected node ids, focus configuration, applied layout configuration, unapplied draft, and last-good positions across loading, benign refresh, transient empty data, and request failure.
- [x] 7.5 Recompute positions only when the effective visible topology, normalized dimensions, or applied layout configuration changes, and discard results from older graph revisions or fingerprints.
- [x] 7.6 Add query, refresh, partial-selection repair, incomplete-topology fallback, unchanged-focused-subgraph, deleted-preset, draft-preservation, and stale-worker-result integration tests.

## 8. Documentation, Performance, and End-to-end Validation

- [x] 8.1 Update `docs/ui/contracts/topic-graph.md` with completeness, total-count, projection request and response, read-only, and no-backend-layout-persistence semantics.
- [x] 8.2 Add frontend unit and component coverage for React Flow-only rendering, legacy Sigma hint handling, multi-selection gestures, Focus controls, Layout controls, preset management, import, export, and safety diagnostics.
- [x] 8.3 Add or extend browser smoke tests for Graph Controls, multi-selection, N-hop focus, layout preview, browser-local preset restoration, responsive drawer behavior, and idea detail opening.
- [x] 8.4 Add hundreds-node and high-degree fixtures, profile layout and React Flow interaction performance, and select documented transfer, projection, and layout safety defaults from measured results.
- [x] 8.5 Run `npm test`, `npm run build`, targeted Playwright and performance smoke scripts in `web/ui`, then verify the packaged static assets include the layout worker and updated Idea Graph bundle.
- [x] 8.6 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, and resolve every regression without modifying Sigma.js or Graphology behavior.
