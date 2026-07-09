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
- `diagnostics`: list of diagnostic objects.

## Node Fields

Each node must include `id`, `record_id`, `material_kind`, `density_class`, and `title`. Useful optional fields include `summary`, `status`, `producer`, `skill`, `created_at`, `updated_at`, `idea_id`, `display_key`, `visibility`, `source`, `detail_refs`, and `renderer_hints`. Canonical Research Idea nodes use `display_key` as their short GUI label in the `I-<index>` format when the Workspace Runtime has been repaired to the current display-key shape.

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
