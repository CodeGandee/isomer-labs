# Version the Literature Query Projection Separately

Literature paper and citation indexes are rebuildable views derived from canonical provider-output Artifacts. Isomer will store those tables inside the selected Topic Workspace's Workspace Runtime database but version them as `isomer-literature-query-index.v1` instead of changing the canonical `isomer-workspace-runtime.v1` contract.

## Status

Accepted.

## Considered Options

- Add literature index tables under Workspace Runtime v1 without a separate version.
- Revise all Workspace Runtime databases to v2.
- Give the literature query projection its own schema version inside the existing database.
- Store the literature query projection in a separate SQLite sidecar.

## Consequences

- `literature_observation_index`, `literature_paper_index`, `literature_citation_edge_index`, and literature-index metadata are derived projection tables rather than canonical lifecycle tables.
- The projection metadata records `isomer-literature-query-index.v1` and enough rebuild state to diagnose missing, stale, or incompatible rows.
- Read-only literature commands do not create, migrate, repair, or rebuild projection tables.
- Recording a valid canonical observation succeeds even when the compatible projection is absent; the result reports that an explicit rebuild is required.
- `ext research literature index rebuild` creates or replaces projection rows from canonical normalized observations without rewriting those observations.
- `ext research literature index validate` reports schema, source-record, digest, completeness, and stale-row diagnostics without mutation.
- Workspace Runtime remains `isomer-workspace-runtime.v1` because the accepted change adds only a separately versioned, disposable query projection.
