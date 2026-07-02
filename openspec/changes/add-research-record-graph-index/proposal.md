## Why

V2 research skills now produce many durable records and body files, but the relationships between records live mostly in Markdown prose, broad `producer` or `consumer` strings, and weak JSON metadata. Topic owners therefore cannot reliably answer what produced a record, which files belong to a Run, which Decision followed which Evidence Item, or how a paper claim traces back to experiments without manually reading the whole `records/` tree.

## What Changes

- Add a runtime-backed research record graph index that stores typed edges between existing Workspace Runtime lifecycle records.
- Add file attachment indexing for durable files under topic record surfaces, including harnesses, raw results, summaries, logs, figures, patches, papers, and manifests.
- Extend research record CRUD so record creation and update can attach structured relationships and file refs instead of hiding them in prose.
- Add graph query behavior for lineage, children, route, files, and export views so Topic Actors and future GUIs can inspect what leads to what.
- Extend runtime validation to report broken graph edges, missing attached files, cross-topic links, stale supersession edges, and unsupported claim/evidence links.
- Update v2 research placeholder binding guidance so skills preserve structured relationship metadata at write time.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `research-recording-contracts`: Add first-class recording graph behavior for record-to-record relationships, file attachments, graph queries, and validation.
- `workspace-runtime-persistence`: Persist graph edge and file attachment indexes in Workspace Runtime, keep them topic scoped, and include graph diagnostics in runtime validation and inspection.
- `research-placeholder-bindings`: Require v2 placeholder binding guidance to describe structured relationship and file-ref metadata for accepted research records.

## Impact

- Affects Workspace Runtime schema, model/store APIs, migration or idempotent schema preparation, runtime validation, and inspection output.
- Affects `isomer-cli ext research records` create/update/list/show behavior and adds or extends graph query commands.
- Affects v2 research skill `placeholder-bindings.md` guidance and workspace manager bootstrap/index guidance.
- Existing record body files remain valid; the change adds structured links for new writes and can support a later best-effort indexer for existing topic records.
