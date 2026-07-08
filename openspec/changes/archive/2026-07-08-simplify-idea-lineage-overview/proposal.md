## Why

The current Idea Lineage view shows user-facing ideas mixed with route decisions, claims, and evidence details, so the graph reads like an internal process trace instead of an idea map. The backend can already distinguish real idea nodes from secondary detail nodes, so the next step is to make the default view match the user's mental model and move details behind drill-down.

## What Changes

- Make the top-level Idea Lineage graph show only user-facing idea nodes by default.
- Treat route decisions, claims, evidence, files, and supporting records as detail material for a selected idea rather than first-level graph nodes.
- Add a backend-supported collapsed idea overview contract so the idea graph can stay connected without rendering secondary nodes directly.
- Use the selected idea's record-detail tab as the first drill-down surface, with lineage, siblings, files, facets, diagnostics, and supporting records lazy-loaded only after selection.
- Keep secondary material available through an explicit **Supporting Records** control and detail tabs for advanced inspection.
- Preserve read-only browsing behavior and avoid topic-specific assumptions.

## Capabilities

### New Capabilities
- `topic-idea-lineage-overview`: Defines the cleaned user-facing idea lineage overview, collapsed idea-to-idea projection, and selected-idea drill-down behavior for the Project Web GUI and Topic Graph API.

### Modified Capabilities
- None.

## Impact

- Affects `src/isomer_labs/web/graph.py`, Project Web graph API responses, frontend graph defaults in `web/ui/src/App.tsx`, graph API client filters, graph tests, and Playwright smoke coverage.
- Does not require new third-party dependencies.
- Does not mutate topic data, Workspace Runtime records, or query-index rows during browsing.
