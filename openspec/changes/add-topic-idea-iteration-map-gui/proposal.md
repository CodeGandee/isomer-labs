## Why

Research topics now produce structured records, lineage edges, generation groups, facets, and file metadata, but users still need to inspect idea evolution by reading raw exports or individual artifacts. A local Project Web GUI idea iteration map gives users a readable way to see how ideas, alternatives, decisions, and evidence evolve while terminal-side research work continues.

## What Changes

- Add a topic-scoped idea iteration view to the Project Web GUI that shows proposed ideas, predecessors, successors, sibling alternatives, selected or rejected status, evidence summaries, and diagnostics.
- Add renderer-neutral topic graph read APIs for sparse idea-lineage views and dense artifact overview views.
- Add frontend workbench behavior for open-tab-scoped fetching, graph/list/detail browsing, record viewer drill-downs, and live refresh hints.
- Add lightweight viewer descriptors so the GUI can open Markdown, PDF, image, table, JSON, or unknown record details without loading heavy payloads up front.
- Keep GUI browsing read-only: it must not rebuild, repair, cleanup, migrate, or write Workspace Runtime state.
- Preserve graceful degradation for partial or stale relationship metadata by showing diagnostics and unconnected groups rather than inventing authoritative lineage.

## Capabilities

### New Capabilities

- `topic-graph-read-api`: Topic-scoped backend APIs that expose renderer-neutral graph view models, viewer descriptors, and live update hints from Workspace Runtime and query-index read models.
- `project-web-research-viewer`: TypeScript Project Web GUI workbench behavior for selecting topics, inspecting idea lineage, opening record details, and refreshing only open relevant views.

### Modified Capabilities

- `research-record-query-index`: Query/export results must expose enough read-only freshness and relationship metadata for graph read models and live GUI invalidation without mutating index rows during browsing.

## Impact

- Affects `src/isomer_labs/web/` FastAPI routes, read-model helpers, static frontend assets, and tests around topic records export/detail APIs.
- Adds or updates TypeScript frontend code, frontend build/test dependencies, and static asset serving for the Project Web GUI workbench.
- Uses existing Workspace Runtime and query-index tables as derived read models; canonical research data remains in runtime lifecycle records and file-backed structured payloads.
- Adds OpenSpec coverage for the topic graph API, GUI viewer behavior, and query-index freshness contract.
