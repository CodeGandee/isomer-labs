# Research Idea Traversal Contract

`GET /api/topics/{topic_id}/ideas/traverse` performs bounded read-only traversal over canonical Idea Lineage Edges. Repeat `root_idea_id` for multiple roots. `direction` is `ancestors` or `descendants`; repeat `relation_kind` to restrict eligible canonical edge kinds. `max_depth`, `max_nodes`, and `max_edges` bound the result.

The response includes `mutated: false`, `roots`, `resolved_roots`, `unresolved_roots`, `direction`, sorted `relation_kinds`, canonical `nodes` and induced `edges`, `maximum_observed_depth`, returned and source `counts` when known, requested `bounds`, `topology_complete`, `limiting_bounds`, `continuation`, `index_revision`, and diagnostics.

`topology_complete: false` means a depth, node, edge, or response bound omitted reachable material. `limiting_bounds` names the cause, and `continuation` describes a safe refinement such as increasing a bound or narrowing relation kinds. Unknown roots remain in `unresolved_roots` with diagnostics while valid roots still traverse. The route never infers Idea Lineage Edges from record lineage or prose.
