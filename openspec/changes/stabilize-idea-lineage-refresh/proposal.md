## Why

The idea lineage graph refetches and relayouts while the user is idle, which makes nodes briefly disappear and can erase selected-node highlights. This is visible now because the graph view has richer hover, selection, and lineage highlighting state that users expect to remain stable during inspection.

## What Changes

- Stop unconditional background graph invalidation when no topic index revision has changed.
- Keep graph layout and base React Flow data stable when a refetch returns the same graph content with a new response timestamp.
- Preserve selected-node lineage highlights across harmless refresh, loading, and transient graph responses.
- Separate backend idea status/selection styling from UI interaction selection styling.
- Add regression coverage for idle refresh behavior and selection persistence.

## Capabilities

### New Capabilities
- `project-web-idea-graph-refresh`: Covers refresh, invalidation, layout, and selection-stability requirements for the Project Web idea lineage graph.

### Modified Capabilities

## Impact

- Frontend event invalidation flow in `web/ui/src/events.ts` and `web/ui/src/App.tsx`.
- Idea lineage React Flow data derivation in `web/ui/src/features/idea-lineage/` and `web/ui/src/graph-utils.ts`.
- Unit or integration tests around graph invalidation and idle graph stability.
- No backend API or storage schema change is expected.
