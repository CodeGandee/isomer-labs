## 1. Label Search Implementation

- [x] 1.1 Add a visible-label helper for idea lineage nodes that matches the ReactFlow node label fields.
- [x] 1.2 Replace Fuse metadata matching in `IdeaLineagePanel` with normalized visible-label token filtering.
- [x] 1.3 Keep edge pruning and group trimming based on the visible filtered node set.
- [x] 1.4 Remove unused Fuse-specific search document code from the idea lineage panel.

## 2. Tests

- [x] 2.1 Add tests that `ncu` filters the graph to only visible labels containing NCU.
- [x] 2.2 Add tests for multi-term label matching across middle label words and punctuation.
- [x] 2.3 Add tests that hidden metadata, ids, source paths, and realization refs do not keep nodes visible.
- [x] 2.4 Keep clearing-search and edge-pruning coverage.

## 3. Validation

- [x] 3.1 Run focused idea lineage frontend tests.
- [x] 3.2 Run graph filter frontend tests to confirm dense controls are unaffected.
- [x] 3.3 Run TypeScript checks for `web/ui`.
- [x] 3.4 Rebuild packaged frontend static assets.
- [x] 3.5 Run `openspec validate restrict-idea-lineage-search-to-labels`.
