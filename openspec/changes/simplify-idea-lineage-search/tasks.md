## 1. Dependency and Search Model

- [x] 1.1 Add `fuse.js` to `web/ui` dependencies and update `package-lock.json`.
- [x] 1.2 Define the idea lineage Fuse.js search document fields and weighting in or near `IdeaLineagePanel`.
- [x] 1.3 Add a helper that filters graph nodes with Fuse.js and prunes edges whose endpoints are not both visible.

## 2. Idea Lineage UI

- [x] 2.1 Replace `GraphFiltersBar` in `IdeaLineagePanel` with a single search input labeled for idea search.
- [x] 2.2 Keep the idea lineage backend query overview-only with `includeSecondary: false` and no status, relation, producer, or time-range filters.
- [x] 2.3 Apply client-side fuzzy filtering before `layoutFlowGraph()` and before converting data to ReactFlow nodes and edges.
- [x] 2.4 Ensure clearing the search restores the unfiltered idea lineage overview.
- [x] 2.5 Keep `GraphFiltersBar` available for dense non-idea graph panels.

## 3. Tests and Validation

- [x] 3.1 Update graph filter tests so dense graph controls remain covered without expecting them in idea lineage.
- [x] 3.2 Add idea lineage tests for the single search input and absence of status, relation, and supporting-record controls.
- [x] 3.3 Add tests for fuzzy matching over node fields and pruning edges attached to hidden nodes.
- [x] 3.4 Run frontend tests covering idea lineage and graph filters.
- [x] 3.5 Run TypeScript checks for `web/ui`.
- [x] 3.6 Rebuild packaged frontend static assets.
- [x] 3.7 Run `openspec validate simplify-idea-lineage-search`.
