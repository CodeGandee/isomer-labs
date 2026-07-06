## Context

The current Project Web GUI is a FastAPI service with static assets under `src/isomer_labs/web/`. It already exposes topic discovery, runtime inspection, record listing, record export, record detail, rendered Markdown, lineage, siblings, files, facets, and explicit index maintenance endpoints. The current frontend is a small static JavaScript app that can inspect exports and records but does not provide a research workbench, typed graph model, dockable viewers, or live topic refresh.

The query index already stores topic-scoped record summaries, edges, files, ideas, route decisions, metrics, claims, facts, canonical lineage fallback, file openability, and diagnostics. This change should turn those derived rows into a GUI-ready read model while preserving the existing ownership rule: Workspace Runtime and the recording API write canonical data and index rows; GUI browsing is read-only.

## Goals / Non-Goals

**Goals:**

- Add a backend topic graph read model for idea-lineage and dense artifact graph scopes.
- Add a TypeScript research workbench that can select a Research Topic, inspect idea lineage, open record details, and refresh as topic artifacts change.
- Keep expensive fetching, graph layout, graph rendering, Markdown rendering, PDF loading, SSE subscriptions, and future tmux attachments scoped to open relevant tabs.
- Provide diagnostics for missing, stale, partial, or unsupported relationship data instead of inventing authoritative lineage.
- Preserve the existing explicit maintenance boundary for rebuild, cleanup, and validation.

**Non-Goals:**

- Do not create or edit ideas from the first GUI slice.
- Do not model idea evolution as Git branches, worktrees, or a strict tree.
- Do not infer authoritative relationships from generated Markdown prose.
- Do not require topic-specific filenames or fixed artifact counts from `isomer-content/`.
- Do not implement tmux control, AG-UI execution, generated UI editing, or full PDF.js behavior in this change.

## Decisions

### Backend graph read model first

Add `GET /api/topics/{topic_id}/graphs/{graph_scope}` and build it inside `ProjectWebReadModel` from the existing query-index export, lineage, siblings, files, facets, and runtime diagnostics. This keeps graph projection close to the schema, avoids duplicated frontend lineage reconstruction, and gives both React Flow and Sigma.js one renderer-neutral model.

Alternative considered: let the frontend assemble graphs from `/records/export?view=ideas`. That is acceptable for a tiny prototype, but it pushes canonical relation mapping, generation-group grouping, diagnostics, and large-graph limits into browser code.

### Renderer-neutral API with two rendering classes

Return `TopicGraphView` with `nodes`, `edges`, `groups`, `facets`, `renderer_hint`, `index_revision`, `paging`, and diagnostics. Use `idea-lineage` with `react-flow-detail` for sparse, high-touch idea inspection, and use `artifact-overview`, `experiment-records`, and `paper-revisions` with `sigma-overview` for dense maps.

Alternative considered: use React Flow for every graph. DeepScientist showed that rich DOM graph nodes, layout work, polling, and always-mounted overlays are expensive at scale, so dense artifact maps need a WebGL overview path.

### TypeScript workbench over static JavaScript

Introduce a Vite React TypeScript frontend with TanStack Router, TanStack Query, TanStack Table, Dockview, RxJS, React Flow, ELK, Sigma.js, Graphology, Plotly.js, Markdown rendering, Mermaid, KaTeX, Zod, and future-ready terminal dependencies. The initial implementation can keep static FastAPI serving, but the frontend source should build into the existing static asset directory.

Alternative considered: extend the current hand-written static JavaScript. That is lower setup cost, but it does not fit dockable tabs, typed API validation, graph libraries, resource cleanup, or future tmux and AG-UI interaction streams.

### Live updates as invalidation hints

Add an SSE event stream at `GET /api/events?topic_id={topic_id}` for topic-scoped read-model invalidation, with polling as fallback. Events carry topic id, event type, optional `index_revision`, changed record ids, material kinds, graph scopes, diagnostic count, and timestamp; they do not carry raw payloads, file contents, terminal output, or credentials.

Alternative considered: have the frontend poll every open endpoint on a fixed interval. Polling remains a fallback, but open-tab-scoped invalidation lowers load for large topics and keeps the design ready for terminal-driven work.

### Viewer descriptors before heavy content

Add `GET /api/topics/{topic_id}/viewer/records/{record_id}` as a lightweight decision point for Markdown, PDF, image, table, JSON, or unknown viewers. The descriptor should include content/detail URLs, media type, existence/openability, and diagnostics without including full payload JSON or rendered content.

Alternative considered: always call record detail with `include_payload=true`. That is simple but wasteful for graph click-through, dense maps, and dockable tabs where many details may be previewed.

### Read-only browsing boundary

All browsing endpoints must return `mutated: false` and must open runtime/index state read-only. Rebuild, cleanup, and repair remain explicit maintenance actions on existing endpoints.

Alternative considered: auto-rebuild missing query-index rows when a GUI route detects gaps. That hides data-integrity problems and violates the current Workspace Runtime write ownership contract.

## Risks / Trade-offs

- Graph projection may duplicate query-index assumptions. Mitigation: keep projection in backend helpers with tests against query-index fixture rows and use one renderer-neutral response model.
- React Flow may still be slow for unexpectedly large idea graphs. Mitigation: bound `react-flow` responses, return `graph_too_large_for_renderer`, and offer a Sigma.js fallback hint.
- SSE file watching can become noisy. Mitigation: emit coarse topic-scoped invalidation hints and let TanStack Query refetch only mounted query keys that intersect the event.
- Frontend dependency count grows quickly. Mitigation: introduce dependencies around stable workbench boundaries and keep optional future features behind dormant adapters.
- Historical topics may have partial lineage. Mitigation: show unconnected groups and diagnostics; do not infer authoritative links from Markdown bodies.

## Migration Plan

1. Add backend graph/viewer/SSE read-model helpers and routes without removing existing record export/detail routes.
2. Add or update query-index export freshness metadata used as `index_revision`.
3. Add the Vite React TypeScript workbench source and build integration while preserving FastAPI static serving and no-cache headers.
4. Implement the idea-lineage view, list/table fallback, detail drill-down, diagnostics panel, and open-tab resource policy.
5. Add focused backend unit tests, frontend component tests where practical, and Playwright checks against a fixture topic with idea lineage, partial metadata, missing files, Markdown, and PDF-like file refs.
6. Roll back by serving the prior static assets and keeping the backend graph routes unused; no canonical Workspace Runtime migration is required.

## Open Questions

- Should `idea-lineage` include decisions and evidence as secondary nodes by default, or only after selecting an idea?
- Should `index_revision` be computed from query-index max `indexed_at`, a stable row-count/hash summary, a Workspace Runtime sequence, or a combination?
- Should dense graph clustering run in the backend, in a Web Worker, or inside the Sigma.js adapter?
- Which future tmux controls should enter first after this read-only GUI slice: attach only, interrupt, stop/resume, or prompt injection?
