# Topic Graph Contract

The topic graph contract feeds the Idea Graph relationship panel. It is renderer-neutral: React Flow and future graph viewers consume the same graph read model.

## Required Fields

- `ok`: whether the graph request succeeded.
- `mutated`: always `false` for read-only graph views.
- `topic_id`: Research Topic id.
- `topic_workspace_id`: Topic Workspace id.
- `graph_scope`: requested graph scope. The supported Project Web graph API scope is `idea-lineage`.
- `renderer_hint`: recommended renderer, such as `react-flow-detail` or `sigma-overview`.
- `generated_at`: generation timestamp.
- `nodes`: graph nodes.
- `edges`: graph edges.
- `groups`: generation groups or graph clusters.
- `facets`: summary data used by filters and side panels.
- `topology_complete`: whether the response contains every eligible source node and every eligible edge between those nodes. Clients must treat an omitted value from an older server as incomplete.
- `total_node_count` and `total_edge_count`: counts for the eligible source topology before paging or neighborhood projection.
- `projection`: neighborhood projection identity and counts, or `null` for an ordinary source-topology response.
- `diagnostics`: list of diagnostic objects.

## Complete and Bounded Topology

The ordinary Idea Graph request asks for React Flow as a client capability, but `renderer` does not change the renderer-neutral graph payload. Project Web currently uses a complete-transfer default of 1,000 nodes. A response that fits the bound has `topology_complete: true`; its `edges` contain every eligible Idea Lineage Edge whose source and target occur in the returned nodes. A response limited by `limit`, `cursor`, or the complete-transfer policy has `topology_complete: false`, preserves source totals, and reports paging diagnostics. The browser must not merge pages and infer that cross-page topology is complete.

The Idea Graph always renders usable `idea-lineage` responses with React Flow. A legacy `renderer_hint: sigma-overview` does not select Sigma.js for this panel.

## N-hop Projection Request

A bounded read-only neighborhood request uses repeated `seed_node_id` query parameters plus `hop_radius`, `direction`, optional `relation_kind`, and `edge_mode`:

```text
GET /api/topics/alpha/graphs/idea-lineage?renderer=react-flow&seed_node_id=idea:a&seed_node_id=idea:b&hop_radius=2&direction=both&relation_kind=derived_from&edge_mode=induced
```

`hop_radius` is between 0 and 8, `direction` is `incoming`, `outgoing`, or `both`, and `edge_mode` is `induced` or `traversal`. The server accepts at most 64 unique seeds. It applies relation-kind filtering before deterministic multi-source breadth-first traversal. The default `induced` mode returns every eligible edge between visible nodes; `traversal` returns only discovery edges. Current projection safety bounds are 2,000 visible nodes and 10,000 visible edges.

Unknown seeds do not fail the request. The response lists them in `unresolved_seed_node_ids` and emits `graph_projection_seed_not_found`. A projection above a configured safety bound fails with `graph_projection_too_large` and no partial topology.

## Projection Response

`projection` records `seed_node_ids`, resolved and unresolved seeds, `hop_radius`, `direction`, sorted `relation_kinds`, `edge_mode`, source and visible node and edge counts, `source_index_revision`, and projected-scope `topology_complete`. The projection is the union of each selected seed's reachable N-hop neighborhood. A zero-hop projection contains resolved seeds and no edges.

Complete source topology is projected in the browser. If `topology_complete` is false, the browser sends the same focus configuration to this read-only endpoint instead. Both paths use the same reachability and induced-edge semantics.

## Read-only and Layout Persistence

Ordinary graph reads and neighborhood projection always return `mutated: false`. They do not write Workspace Runtime, query-index state, graph coordinates, focus state, or Graph Layout Presets. Layout recipes are validated and stored only in the browser under `isomer-web-idea-graph-layout-presets-v1`; users can export and import those JSON files. The backend does not persist browser layout recipes or calculated React Flow positions.

## Initial Safety Defaults and Smoke Baseline

The initial renderer-independent policies are a 1,000-node complete transfer, at most 64 projection seeds, at most 8 hops, and a projected result of at most 2,000 nodes or 10,000 edges. Browser preset imports are limited to 1 MiB and 500 presets. These constants leave room above the normal hundreds-node Idea Graph while bounding transfer, traversal, and local file work.

The deterministic performance fixture contains 400 nodes and 579 edges, including a 180-neighbor hub. On the repository test host on 2026-07-13, its client projection took 7.1 ms, React Flow conversion took 1.6 ms, selection highlighting took 2.7 ms, and deterministic grid layout took 2.9 ms. The smoke budget remains 2,000 ms to avoid making CI depend on workstation-class timing. Run `npm run test:idea-graph-performance` from `web/ui` to repeat this check.

## Node Fields

Each node must include `id`, `record_id`, `material_kind`, `density_class`, and `title`. A canonical Research Idea node also includes `idea_id`, `exploration_state`, `decision_state`, `evidence_state`, `archive_state`, `visibility`, `needs_classification`, `backend_selected`, `decision_summary`, `transition_refs`, and lazy `detail_refs`. Useful optional fields include `summary`, deprecated compatibility `status`, `producer`, `skill`, `created_at`, `updated_at`, `display_key`, `source`, and `renderer_hints`. Canonical Research Idea nodes use `display_key` as their short GUI label in the `I-<index>` format when the Workspace Runtime has been repaired to the current display-key shape.

Portfolio behavior uses the canonical facets, never compatibility `status`. See [Research Idea Portfolio](idea-portfolio.md) for fixed presets, explicit filter composition, facet counts, canonical-versus-browser selection, and legacy fallback rules.

Project Web no longer serves `artifact-overview`, `experiment-records`, or `paper-revisions` graph scopes. Requests for those scopes return `unsupported_graph_scope`.

## Edge Fields

Each edge must include `id`, `source`, `target`, `relation_kind`, and `canonical`. Useful optional fields include `lineage_kind`, `generation_id`, `status`, `rationale`, `confidence`, `source_classification`, `source_record_refs`, and `metadata`.

## Extra Fields

Extra fields are allowed on the response, nodes, edges, groups, and facets. The GUI should ignore fields it does not understand unless a specific viewer opts into them.

## Example

```json
{
  "ok": true,
  "mutated": false,
  "topic_id": "alpha",
  "topic_workspace_id": "alpha",
  "graph_scope": "idea-lineage",
  "renderer_hint": "react-flow-detail",
  "generated_at": "2026-07-08T00:00:00Z",
  "topology_complete": true,
  "total_node_count": 1,
  "total_edge_count": 0,
  "projection": null,
  "nodes": [
    {
      "id": "idea:idea-a",
      "record_id": "record-a",
      "material_kind": "idea",
      "density_class": "sparse",
      "title": "Launch-overhead correction",
      "summary": "Separate host launch time from kernel runtime.",
      "idea_id": "idea-a",
      "display_key": "I-1"
    }
  ],
  "edges": [],
  "groups": [],
  "facets": {
    "counts": {
      "ideas": 1
    }
  },
  "diagnostics": []
}
```
