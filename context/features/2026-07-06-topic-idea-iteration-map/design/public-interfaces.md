# Public Interfaces

## Scope

This design covers the topic-scoped read APIs, frontend view contracts, live-update events, renderer selection rules, and future terminal or AG-UI integration points for the Research Topic idea iteration and artifact relationship viewer. The first implementation remains read-only for research browsing: terminal-side workflows and Isomer CLI write paths mutate Workspace Runtime; the Project Web GUI reads prepared topic view models and opens details.

## Covered Use Cases

- `UC-01`: Inspect Live Idea Lineage While Continuing Topic Work

## Architecture

The backend remains the Project Web GUI FastAPI service created for one Project root. It resolves Project, Research Topic, Effective Topic Context, Topic Workspace, Workspace Runtime, and query-index rows, then returns renderer-neutral view models to the TypeScript frontend.

The frontend is a routable React workbench. Dockview owns open tabs and pane layout, TanStack Router owns durable URL navigation, TanStack Query owns server-state fetching, and RxJS owns long-lived interaction streams such as live update fan-in, future terminal control, and cross-tab command routing.

Graph rendering is split by artifact density. Sparse, high-touch materials such as ideas, hypotheses, Decision Records, and selected reasoning paths use React Flow because users need readable cards, comments, editing affordances later, and deep inspection. Dense materials such as experiment records, run outputs, paper revisions, generated figures, result summaries, and repeated logs use Sigma.js with Graphology for WebGL overview and drill into detail tabs.

## Backend Interfaces

### Existing Topic and Record APIs

The current web API remains supported and should be reused by detail panels whenever possible.

| Route | Purpose | Notes |
| --- | --- | --- |
| `GET /api/topics` | List Research Topics discovered from the Project Manifest. | Used by topic picker. |
| `GET /api/topics/{topic_id}` | Return topic context, Topic Actor bindings, and Topic Workspace Manifest summary. | Used by topic header and diagnostics. |
| `GET /api/topics/{topic_id}/runtime` | Return Workspace Runtime inspection. | Read-only runtime status. |
| `GET /api/topics/{topic_id}/records/export?view=ideas` | Return query-index nodes, edges, files, ideas, routes, metrics, claims, facts, and diagnostics. | First implementation can compose graph read models from this response. |
| `GET /api/topics/{topic_id}/records/{record_id}` | Return canonical record detail. | Use `include_payload=true` only for explicit detail inspection. |
| `GET /api/topics/{topic_id}/records/{record_id}/render?format=markdown` | Return rendered Markdown for one record. | Used by Markdown viewer. |
| `GET /api/topics/{topic_id}/records/{record_id}/lineage?direction=both` | Return canonical lineage when present, otherwise query-index lineage. | Used by selected-node detail. |
| `GET /api/topics/{topic_id}/records/{record_id}/siblings` | Return generation group siblings for one record. | Used for candidate passes and alternatives. |
| `GET /api/topics/{topic_id}/records/{record_id}/files` | Return openability-aware file rows. | File actions must depend on `exists_flag` and media type. |
| `GET /api/topics/{topic_id}/records/{record_id}/facets` | Return idea, route, metric, claim, and fact rows for one record. | Used by detail panels. |

### Topic Graph View API

Add a renderer-neutral graph endpoint that prepares graph view models on the backend instead of asking the frontend to reconstruct lineage, generation groups, route status, evidence summaries, and diagnostics from raw export rows.

```http
GET /api/topics/{topic_id}/graphs/{graph_scope}
```

Query parameters:

| Parameter | Required | Meaning |
| --- | --- | --- |
| `renderer` | Optional | `auto`, `react-flow`, or `sigma`; default `auto`. |
| `status` | Optional | Comma-separated normalized statuses. |
| `relation_kind` | Optional | Comma-separated relation kinds. |
| `producer` | Optional | Producer or skill filter. |
| `time_range` | Optional | `all`, `7d`, `30d`, `90d`, or an ISO interval. |
| `search` | Optional | Case-insensitive label, summary, idea id, or record id search. |
| `limit` | Optional | Maximum nodes returned, default chosen by graph scope. |
| `cursor` | Optional | Opaque page cursor for dense graphs. |
| `include_secondary` | Optional | Include evidence, claims, decisions, runs, or files as secondary nodes. |

Supported `graph_scope` values:

| Scope | Default Renderer | Purpose |
| --- | --- | --- |
| `idea-lineage` | `react-flow` | Sparse idea, hypothesis, route decision, and selected reasoning path graph. |
| `artifact-overview` | `sigma` | Dense overview across topic records and relationship clusters. |
| `experiment-records` | `sigma` | Dense experiment, run, metric, claim, and result summary map. |
| `paper-revisions` | `sigma` | Dense manuscript, draft, figure, PDF, and revision relationship map. |

Response model:

```ts
type TopicGraphView = {
  ok: boolean
  mutated: false
  topic_id: string
  topic_workspace_id: string
  graph_scope: "idea-lineage" | "artifact-overview" | "experiment-records" | "paper-revisions"
  renderer_hint: "react-flow-detail" | "sigma-overview"
  index_revision: string | null
  generated_at: string
  nodes: TopicGraphNode[]
  edges: TopicGraphEdge[]
  groups: TopicGraphGroup[]
  facets: TopicGraphFacets
  paging?: { cursor?: string | null; next_cursor?: string | null; truncated: boolean }
  diagnostics: Diagnostic[]
}
```

Node model:

```ts
type TopicGraphNode = {
  id: string
  record_id: string
  material_kind: "idea" | "decision" | "evidence" | "claim" | "metric" | "experiment" | "paper_revision" | "file" | "record"
  density_class: "sparse" | "dense"
  title: string
  one_liner?: string | null
  summary?: string | null
  status?: string | null
  selected?: boolean
  producer?: string | null
  skill?: string | null
  created_at?: string | null
  updated_at?: string | null
  source: {
    record_id: string
    idea_id?: string | null
    source_json_path?: string | null
    source_classification?: string | null
  }
  detail_refs: {
    record_detail: string
    rendered_markdown?: string | null
    files?: string | null
    facets?: string | null
    lineage?: string | null
    siblings?: string | null
  }
  renderer_hints: {
    color?: string | null
    size?: number | null
    cluster?: string | null
    card_variant?: "idea" | "decision" | "evidence" | "record" | null
  }
}
```

Edge model:

```ts
type TopicGraphEdge = {
  id: string
  source: string
  target: string
  relation_kind: "follows_from" | "alternative_to" | "supersedes" | "supports" | "contradicts" | "blocks" | "derived_from" | "revision_of" | "selected_from" | "follow_up_to" | "evidence_basis" | "routes_to" | "produces" | "materializes_file" | "cites" | "summarizes"
  canonical: boolean
  lineage_kind?: string | null
  generation_id?: string | null
  status?: string | null
  rationale?: string | null
  confidence?: number | null
  source_classification?: "canonical-lineage" | "authored" | "payload-derived" | "file-derived" | "body-inferred" | null
}
```

Group model:

```ts
type TopicGraphGroup = {
  id: string
  group_kind: "generation_group" | "unconnected" | "status_bucket" | "artifact_cluster"
  title: string
  purpose?: string | null
  parent_set_digest?: string | null
  node_ids: string[]
  diagnostics: Diagnostic[]
}
```

Validation rules:

- `topic_id` must resolve through the Project Manifest and Effective Topic Context.
- `graph_scope` must be one of the supported values.
- `renderer=react-flow` must return a bounded sparse graph or an error with a Sigma.js fallback hint when the graph is too large.
- Relationship labels must map to stable query-index relation kinds, canonical lineage kinds, or Research Inquiry Relationship vocabulary.
- The backend must not infer authoritative lineage from generated Markdown prose.
- File-opening metadata must only expose actions for existing files under accepted Project or Topic Workspace surfaces.

Errors:

| Code | Meaning |
| --- | --- |
| `topic_not_found` | The selected Research Topic is not declared in the Project Manifest. |
| `unsupported_graph_scope` | The requested graph scope is unknown. |
| `query_index_unavailable` | Workspace Runtime or query-index tables cannot be read. |
| `query_index_stale` | The graph was built from stale or incomplete index rows. |
| `graph_too_large_for_renderer` | The requested renderer is unsuitable for the returned graph size. |
| `record_not_found` | A selected record no longer exists in the read model. |
| `file_missing` | A file facet points to a missing or unavailable path. |

### Viewer Descriptor API

Add a lightweight descriptor endpoint so dockable tabs can decide which viewer to open before loading heavy content.

```http
GET /api/topics/{topic_id}/viewer/records/{record_id}
```

Response model:

```ts
type RecordViewerDescriptor = {
  ok: boolean
  mutated: false
  topic_id: string
  record_id: string
  title: string
  viewer_kind: "markdown" | "pdf" | "image" | "table" | "json" | "unknown"
  primary_content_url?: string | null
  detail_url: string
  render_url?: string | null
  files_url?: string | null
  facets_url?: string | null
  media_type?: string | null
  exists: boolean
  diagnostics: Diagnostic[]
}
```

The first version may derive this descriptor inside the frontend by combining existing `record_detail`, `record_render`, and `record_files` endpoints. A backend endpoint becomes useful once multiple viewer types and dense graph drill-downs share the same open logic.

### Live Topic Event Stream

Add a server-sent event stream for topic read-model invalidation. Events are hints for active tabs, not complete payload replacements.

```http
GET /api/events?topic_id={topic_id}
```

Event model:

```ts
type TopicChangeEvent = {
  event_id: string
  event_type: "topic.index.changed" | "topic.records.changed" | "topic.diagnostics.changed" | "topic.runtime.changed"
  topic_id: string
  topic_workspace_id?: string | null
  index_revision?: string | null
  changed_record_ids?: string[]
  changed_material_kinds?: string[]
  graph_scopes?: string[]
  diagnostics_count?: number
  occurred_at: string
}
```

Validation and behavior:

- Events must be topic-scoped.
- Events must not include raw payload bodies, terminal output, credentials, or file contents.
- The frontend must filter events by open Dockview tabs before invalidating TanStack Query keys.
- Polling remains the fallback when SSE is unavailable.

## Frontend Interfaces

### Workbench Tab Contract

Every expensive viewer must be owned by an open Dockview panel. Closed panels stop polling, SSE-triggered refetch, graph layout, Sigma rendering, React Flow rendering, Mermaid rendering, PDF rendering, and AG-UI or tmux attachment.

```ts
type WorkbenchTab = {
  id: string
  kind: "idea-graph" | "artifact-graph" | "record-detail" | "markdown" | "pdf" | "table" | "diagnostics" | "tmux" | "ag-ui"
  topic_id?: string
  record_id?: string
  graph_scope?: TopicGraphView["graph_scope"]
  query_keys: readonly unknown[][]
  keep_background_watch?: boolean
}
```

### Renderer Selection

The frontend should choose the renderer from the backend `renderer_hint`, graph scope, and node count.

| Condition | Renderer |
| --- | --- |
| `graph_scope=idea-lineage` and sparse graph | React Flow |
| User opens selected idea path detail | React Flow |
| Dense experiment, paper, result, or revision graph | Sigma.js |
| User selects one dense node | Detail tab using existing record APIs |
| User opens generated analytical chart | Plotly.js |

### Query Key Policy

TanStack Query keys should include topic id, graph scope, renderer, filter state, and selected record when applicable.

```ts
["topic", topicId, "graph", graphScope, renderer, filters]
["topic", topicId, "record", recordId, "detail", includePayload]
["topic", topicId, "record", recordId, "render", "markdown"]
["topic", topicId, "record", recordId, "files"]
["topic", topicId, "record", recordId, "facets", facet ?? "all"]
```

Unmounted tabs should disable their queries. Hidden but mounted tabs may keep cheap cached state, but they should not run expensive renderers or frequent refresh loops.

## Future Session and Generative UI Interfaces

### Tmux Session Control

Terminal tabs should follow Houmao's tmux bridge pattern but through the Isomer Project Web GUI backend. The backend owns session discovery and PTY attachment; the browser owns presentation only.

| Interface | Purpose |
| --- | --- |
| `GET /api/sessions/tmux/status` | Report whether `tmux` and the backend PTY bridge are available. |
| `GET /api/sessions/tmux` | List sessions with session name, attached state, window count, created time, and matched Topic Actor or Agent Workspace when known. |
| `WS /api/sessions/tmux/attach` | Attach to one session and exchange structured attach, input, resize, scroll, interrupt, close, and output messages. |

Closing a tmux tab closes only the browser attachment and the backend attach process. It must not kill the tmux session, mutate Workspace Runtime, detach unrelated clients, or stop an Agent Instance.

### AG-UI and Generated Components

AG-UI support should remain separate from tmux. AG-UI streams carry agent-authored UI events and typed components; tmux WebSockets carry terminal bytes and terminal controls.

The first generated component set should support Plotly-backed `plotly2d` charts, tables, metric grids, and dashboards. Unknown or invalid typed components should render explicit fallbacks with diagnostics rather than raw HTML, raw SVG, or JavaScript injection.

## Lifecycle and Persistence

Backend read endpoints must return `mutated: false` and must not rebuild, repair, cleanup, migrate, or write query-index rows during browsing. Existing maintenance endpoints remain explicit user actions.

The browser may persist Dockview layout, selected topic, selected graph scope, filters, and non-sensitive tab descriptors in local storage. It must not persist raw terminal output, terminal input, WebSocket payloads, AG-UI request bodies, credentials, authorization headers, raw record payloads, or local file contents.

The backend should derive expensive graph read models from Workspace Runtime and query-index rows, then expose `index_revision` or another change token so the frontend can refresh only when relevant data changes.

## Compatibility Notes

The first implementation can use `GET /api/topics/{topic_id}/records/export?view=ideas` plus existing record detail endpoints before introducing `/graphs/{graph_scope}`. The dedicated graph endpoint should be introduced when frontend derivation becomes duplicated, slow, or renderer-specific.

React Flow and Sigma.js must consume the same renderer-neutral graph model. Do not store React Flow positions or Sigma.js camera state as canonical research data.

UI labels may say "branch" only for visual branching when unavoidable, but schema and API fields should use Research Inquiry, relationship, lineage, generation group, alternative, predecessor, and successor language.

## Open Questions

- Should `idea-lineage` include Decision Records and evidence as secondary nodes by default, or only in selected-node detail?
- What exact `index_revision` token should the backend expose: SQLite WAL revision, query-index max `indexed_at`, or a Workspace Runtime sequence?
- Should Sigma.js dense graph clustering be computed on the backend, in a Web Worker, or inside the renderer adapter?
- Which tmux control actions should be available in the first session-control slice: attach only, interrupt, stop, resume, or prompt injection?

