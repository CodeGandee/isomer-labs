## Why

Research artifacts currently carry lineage only through optional payload fields, revision hints, or query-index relationship metadata. This is too soft for GUI views and operator recovery because agents can describe parent-child relationships in prose without creating durable edges, so proposed ideas, route decisions, experiments, results, and revisions cannot reliably form an inspectable DAG.

## What Changes

- Add canonical artifact lineage DAG storage to Workspace Runtime, separate from derived query-index edge tables.
- Add lineage-aware research record create, update, revise, validate, and query CLI behavior.
- Treat revisions as new descendant records in a linear revision chain rather than in-place mutation of generated Markdown or old payloads.
- Derive query-index graph and lineage views from canonical lineage edges, authored relationship hints, and payload refs.
- Teach production DeepSci skills to identify parent records, generation groups, sibling sets, selected children, merged children, follow-ups, and revision parents when writing durable records.
- Preserve support for non-lineage relationship metadata, file hints, and GUI facets without making those optional hints the canonical artifact DAG.

## Capabilities

### New Capabilities

- `research-artifact-lineage-dag`: Canonical parent-child lineage DAG for durable research records, including multi-parent children, generation groups for siblings, revision chains, and validation rules.

### Modified Capabilities

- `workspace-runtime-persistence`: Workspace Runtime must persist canonical lineage edges and generation groups, validate acyclicity, and expose current/latest views from lineage and revision records.
- `research-recording-contracts`: Research record create, update, revise, and delete/archive operations must accept and preserve canonical lineage inputs separately from optional query-index relationship hints.
- `research-record-query-index`: Query-index graph and lineage exports must derive from canonical lineage edges and distinguish canonical lineage from non-canonical relationship refs.
- `research-placeholder-bindings`: Placeholder binding guidance must name expected lineage parents, generation groups, sibling behavior, and revision behavior for structured research records.
- `research-paradigm-skills`: Production DeepSci skills must include lineage-recording steps in the workflows that create or revise durable artifacts.

## Impact

- Affects Workspace Runtime SQLite schema, runtime records, validation, migrations, and reset/bootstrap behavior.
- Affects `isomer-cli ext research records ...` create/update/revise/query/index command shapes and JSON outputs.
- Affects query-index rebuild, validation, export, lineage, facets, and GUI read models.
- Affects production DeepSci skill instructions, placeholder binding pages, and packaged system skill copies.
- Requires tests for DAG acyclicity, multi-parent lineage, generation-group siblings, revision chains, query export, and skill instruction coverage.
