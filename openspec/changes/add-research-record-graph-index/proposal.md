## Why

DeepSci topics already produce structured research records in Workspace Runtime: lifecycle rows, JSON payloads, rendered Markdown, operation-set files, decisions, ideas, metrics, evidence, and run outputs. Future GUI and operator views need to query those records without opening every Markdown body or guessing structure from prose.

The current change was too graph-first. Lineage matters, but the GUI needs a broader SQL-backed query index: record summaries, profile metadata, typed edges, file attachments, and normalized facets such as ideas, routes, metrics, and claims.

## What Changes

- Add a SQL-backed research record query index in Workspace Runtime, with `lifecycle_records` and `structured_research_payloads` remaining the source of truth.
- Make Workspace Runtime responsible for writing and rebuilding query-index rows; agents, skills, and GUI clients provide canonical payloads and optional hints through the record API instead of writing SQL tables directly.
- Refresh the query index by default during explicit mutating record operations such as create, update, and archive; keep list, show, validate, render, and export operations read-only with respect to the DB.
- Add a `research_record_index` table that denormalizes topic-scoped record metadata for fast list, filter, timeline, and detail-entry queries.
- Add typed edge and file index tables for lineage, decision paths, operation-set files, generated outputs, and record attachments.
- Add normalized facet tables for GUI-ready ideas, routes, metrics, claims, and future scalar JSON facts extracted from structured payloads.
- Add deterministic index maintenance commands for rebuild, validation, and cleanup so existing topic workspaces can be indexed from stored payloads and operation-set files.
- Add deterministic query commands for indexed lists, graph/dashboard/timeline exports, lineage, files, and facets.
- Extend record create/update contracts with optional relationship, file, and index-hint metadata while keeping payload-first structured records as the normal write path.
- Update DeepSci placeholder binding guidance so skills describe expected relationship, file, and facet metadata without forcing agents to hand-author every derived index row.

## Capabilities

### New Capabilities

- `research-record-query-index`: Provide a topic-scoped SQL query index for research records, facets, files, and graph export.

### Modified Capabilities

- `research-recording-contracts`: Extend record CRUD and validation contracts with optional relationship, file, and index-hint metadata while preserving payload-first records.
- `workspace-runtime-persistence`: Persist additive query-index tables in Workspace Runtime and make rebuild/validation idempotent.
- `research-placeholder-bindings`: Require DeepSci placeholder binding guidance to describe expected relationship, file, and GUI facet metadata for structured records.

## Impact

- Affects Workspace Runtime schema preparation, record store APIs, index rebuild, index cleanup, validation, and inspection/export behavior.
- Affects `isomer-cli ext research records` create/update/list/show and adds `records index` and `records query` command groups for GUI and operator consumers.
- Affects DeepSci `placeholder-bindings.md` guidance and profile-driven extraction metadata.
- Existing record bodies, lifecycle rows, and structured payload rows remain valid; older topic workspaces can be indexed by deterministic rebuild with derived rows marked by source.
