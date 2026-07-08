## Why

The idea lineage graph currently shows three text inputs and a supporting-record checkbox, which makes a user-facing idea map feel like a low-level graph query tool. Users should get one simple search box that finds idea nodes by their visible and identifying information, then open a node when they need supporting details.

## What Changes

- Replace the idea lineage graph's shared graph filter bar with a dedicated single search box.
- Use Fuse.js for client-side fuzzy matching over relevant idea node fields.
- Filter only nodes; edges should remain only when both endpoints are visible after node filtering.
- Remove status, relation, producer, time-range, and supporting-record controls from the idea lineage graph view.
- Always request the idea lineage overview without supporting records; supporting records remain available through node detail views.
- Keep the generic graph filter bar available for dense non-idea graph views.

## Capabilities

### New Capabilities
- `idea-lineage-fuzzy-search`: Covers the simplified idea lineage graph search UX, Fuse.js node matching, and removal of supporting-record controls from the idea lineage view.

### Modified Capabilities

## Impact

- Frontend dependency: add `fuse.js` to `web/ui`.
- Frontend graph UI: `IdeaLineagePanel` gets a dedicated search bar and client-side node/edge filtering.
- Frontend shared graph controls: `GraphFiltersBar` stays available for dense graph panels.
- Backend graph API: idea lineage requests should always use `include_secondary=false` from the simplified UI; no new backend endpoint is required.
- Tests: update graph filter tests and add idea lineage fuzzy-search coverage.
