## 1. Backend Read Models

- [x] 1.1 Add query-index freshness metadata, including `index_revision` or an equivalent deterministic change token, to topic export/read-model responses without mutating Workspace Runtime.
- [x] 1.2 Implement backend graph projection helpers that build renderer-neutral nodes, edges, groups, facets, paging, diagnostics, and renderer hints from query-index export, canonical lineage, siblings, files, facets, and runtime diagnostics.
- [x] 1.3 Add `GET /api/topics/{topic_id}/graphs/{graph_scope}` with supported scopes `idea-lineage`, `artifact-overview`, `experiment-records`, and `paper-revisions`.
- [x] 1.4 Add validation and error handling for unknown topics, unsupported graph scopes, stale or unavailable query-index state, unsuitable renderer requests, missing records, and missing files.
- [x] 1.5 Add `GET /api/topics/{topic_id}/viewer/records/{record_id}` for lightweight viewer descriptors that avoid full payloads and heavy content.
- [x] 1.6 Add `GET /api/events?topic_id={topic_id}` as a topic-scoped SSE invalidation stream with bounded polling-compatible semantics and no raw payload, file, terminal, or credential content.

## 2. Frontend Workbench Foundation

- [x] 2.1 Add a Vite React TypeScript frontend source tree and build path that emits static assets served by the existing FastAPI app.
- [x] 2.2 Add frontend dependencies for TanStack Router, TanStack Query, TanStack Table, Dockview, RxJS, React Flow, ELK, Sigma.js, Graphology, Plotly.js, Markdown rendering, Mermaid, KaTeX, Zod, and test tooling.
- [x] 2.3 Implement typed API clients and Zod validation for topics, graph views, viewer descriptors, record detail, render, lineage, siblings, files, facets, runtime, and diagnostics.
- [x] 2.4 Implement a workbench shell with topic selection, URL-backed topic/view state, Dockview tabs, responsive layout, and local persistence for non-sensitive layout state.
- [x] 2.5 Preserve no-cache behavior for GUI shell, static assets, and API responses so local browser testing loads the latest build.

## 3. Idea Iteration Viewer

- [x] 3.1 Implement the idea-lineage graph tab using React Flow and ELK layout for bounded sparse graphs.
- [x] 3.2 Implement dense graph overview tabs using Sigma.js and Graphology for artifact overview, experiment records, and paper revisions.
- [x] 3.3 Implement idea and artifact list/table views with filtering by status, relation kind, producer or skill, time range, and search text.
- [x] 3.4 Show idea nodes and rows with stable id, concise title or one-liner, summary, status, source record id, producer or skill, timestamps, selection state, and diagnostics.
- [x] 3.5 Show predecessor, successor, sibling, selected, rejected, superseded, revised, follow-up, route, evidence, and decision context when source data provides it.
- [x] 3.6 Show unconnected or partial-data groups with diagnostics when relationship metadata is missing, stale, unsupported, or ambiguous.

## 4. Detail Viewers and Resource Policy

- [x] 4.1 Implement record detail tabs that open from graph or table selections and use existing detail, render, lineage, siblings, files, and facets APIs.
- [x] 4.2 Implement Markdown rendering with GFM, Mermaid, math, and KaTeX for rendered record content.
- [x] 4.3 Implement lightweight PDF/image/table/JSON fallback viewers using viewer descriptors and browser-native PDF support where possible.
- [x] 4.4 Gate file actions on backend openability metadata and avoid offering actions for missing, external, unresolved, or outside-project files.
- [x] 4.5 Ensure closed tabs stop polling, SSE-triggered refetch, graph layout, graph rendering, Markdown rendering, PDF rendering, and future session attachment work.
- [x] 4.6 Ensure topic refresh preserves selected topic, filters, layout mode, and selected detail when the selected record still exists.

## 5. Live Updates and Diagnostics

- [x] 5.1 Use RxJS to fan in SSE events, fallback polling ticks, user refresh actions, and cross-tab invalidation commands.
- [x] 5.2 Use TanStack Query keys scoped by topic id, graph scope, renderer, filters, record id, and detail kind so only relevant mounted views refetch.
- [x] 5.3 Add visible diagnostics and maintenance hints for stale index rows, missing index rows, broken edges, missing files, unsupported relation kinds, extractor failures, and partial lineage.
- [x] 5.4 Keep all browsing paths read-only and route rebuild, cleanup, and repair to explicit existing maintenance actions only.

## 6. Verification

- [x] 6.1 Add Python unit tests for query-index freshness metadata, graph projection, graph route errors, viewer descriptors, and read-only mutation flags.
- [x] 6.2 Add frontend tests for API validation, renderer selection, tab resource cleanup, graph/list filtering, and detail viewer selection.
- [x] 6.3 Add Playwright coverage for selecting a topic, opening idea lineage, selecting an idea, opening detail, resizing the browser, and observing refresh behavior without stale static assets.
- [x] 6.4 Validate against a fixture topic with idea lineage, sibling alternatives, revisions, partial metadata, missing files, Markdown with Mermaid and KaTeX, and PDF-like file refs.
- [x] 6.5 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, frontend tests, and the relevant Playwright checks.
