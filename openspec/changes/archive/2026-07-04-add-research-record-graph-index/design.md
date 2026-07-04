## Context

Workspace Runtime already stores DeepSci research records in `state.sqlite` and renders structured payloads to Markdown files under topic record surfaces. A representative FlashAttention topic workspace contains lifecycle records, structured payload rows, rendered bodies, and operation-set outputs for ideas, decisions, runs, metrics, claims, and artifact manifests.

Those artifacts are structured enough to index, but not queryable enough for a GUI. The durable source of truth is already present; the missing layer is a topic-scoped SQL query index that turns payload fields, record metadata, relationships, and files into predictable tables.

## Goals / Non-Goals

**Goals:**

- Keep `lifecycle_records`, `structured_research_payloads`, rendered Markdown, and operation-set files as canonical storage.
- Add a query index for GUI and operator reads: timeline, ideas, decisions, experiments, claims, files, and lineage.
- Support deterministic rebuild from existing structured payloads and known operation-set files.
- Distinguish authored metadata from payload-derived metadata and low-confidence body inference.
- Use Artifact Format Profile refs and DeepSci placeholder bindings to drive facet extraction.
- Keep record create/update payload-first and allow optional relationship, file, and index-hint metadata at write time.

**Non-Goals:**

- Do not replace durable record storage with GUI-specific tables.
- Do not require every file, metric, or JSON scalar to become a lifecycle record.
- Do not treat Markdown scraping as authoritative research truth.
- Do not implement the GUI in this change.
- Do not define a workflow scheduler, task router, or research planner.

## Data Model

```text
lifecycle_records
structured_research_payloads
rendered markdown
operation-set files
        |
        v
research_record_index
research_record_edges
research_record_files
research_record_ideas
research_record_routes
research_record_metrics
research_record_claims
research_record_json_facts
```

`research_record_index` is the read entry point. It stores stable record ids, kind, status, profile refs, title, summary, content paths, rendered paths, producer/consumer hints, timestamps, validation/render status, and topic/workspace ownership.

`research_record_edges` stores typed relationships between records. Each edge carries relation kind, role, source field, source classification (`authored`, `derived_from_payload`, or `inferred_from_body`), confidence, status, rationale, and metadata.

`research_record_files` stores files attached to, produced by, or materialized from records. Paths remain workspace-relative or project-local locators validated through existing path rules; operation-set outputs can be indexed without becoming lifecycle records.

Facet tables store data the GUI naturally needs: ideas, routes, metrics, claims, and generic scalar JSON facts. Each facet row records the source JSON path or source file locator so the UI can trace extracted data back to the payload.

## Write Responsibility

Producer agents, Topic Actors, Project Operators, and GUI clients do not write query-index SQL tables directly. They write canonical research records through the research recording API or CLI, including structured payloads and optional relationship, file, or index hints when they know them.

Workspace Runtime owns the database mutation. The record store writes `lifecycle_records`, `structured_research_payloads`, rendered locators, and authored metadata, then invokes the query-index service to refresh affected index rows in the same transaction when practical.

The query-index service owns derived rows. It runs profile extractors, records file attachments, classifies edge/facet sources, and marks stale rows when a synchronous refresh cannot finish. An explicit rebuild command can regenerate derived rows for a whole Topic Workspace.

The GUI is a reader of the export/query API, not a table writer. If a GUI creates or edits a record, it does so through the same recording API, so validation and indexing stay centralized.

## CLI/API Shape

Index maintenance commands live under the existing research records extension surface. Mutating maintenance is explicit:

```text
isomer-cli ext research records index rebuild [--record-id <record-id>] [--include-operation-set-files] [--dry-run]
isomer-cli ext research records index validate [--record-id <record-id>]
isomer-cli ext research records index cleanup [--stale-derived] [--orphaned] [--missing-files] [--dry-run|--apply]
```

`index rebuild` refreshes derived rows from canonical runtime records, structured payloads, rendered locators, and accepted operation-set files. `index validate` is read-only and reports stale rows, broken refs, missing files, unsupported relation kinds, and extractor failures. `index cleanup` previews by default; it mutates only with `--apply`, removes or marks only query-index rows, and never deletes lifecycle records, structured payloads, rendered Markdown, operation-set files, or accepted artifacts.

Read-only query commands live under a separate `records query` group:

```text
isomer-cli ext research records query list [--record-kind <kind>] [--status <status>] [--profile <profile-ref>] [--facet <facet>] [--limit <n>]
isomer-cli ext research records query export [--view graph|dashboard|timeline|ideas|experiments|claims] [--format json]
isomer-cli ext research records query lineage <record-id> [--direction upstream|downstream|both]
isomer-cli ext research records query files <record-id>
isomer-cli ext research records query facets <record-id> [--facet ideas|routes|metrics|claims|facts]
```

These query commands open the runtime read-only, read only query-index tables and canonical locators, and return deterministic JSON. If the index is missing or stale, they report diagnostics and recommend `index rebuild`; they do not repair or backfill during the query.

## Decisions

### Refresh the Index Only from Explicit Mutations

Query-index refresh is part of explicit mutating operations. `records create`, `records update`, `records delete` or archive, and an explicit index rebuild can write query-index rows. Runtime initialization or schema preparation can create missing query-index tables, but ordinary read operations must not create, refresh, repair, or backfill index data.

Read-only operations include list, show, validate, render, export, and GUI query paths. If they detect stale or missing index rows, they should report diagnostics or ask the caller to run rebuild; they should not silently mutate `state.sqlite`.

Alternative considered: opportunistically refresh stale index rows during read/export. That would make query output feel fresher, but it would blur command semantics and surprise agents by writing topic-owned state during inspection.

### Use a Query Index, Not a New Source of Truth

The index is a denormalized read layer over existing runtime records and structured payloads. Mutating record operations write canonical records first, then refresh affected index rows in the same transaction when practical. Rebuild can recreate derived index rows from canonical storage.

Alternative considered: make the graph tables authoritative. That would hide the existing payload-first contract and make Markdown/payload records second-class, so the design keeps the index disposable and rebuildable.

### Keep Graph Edges as One Layer of the Index

Lineage remains important, but it is one part of the GUI read model. Relation kinds should cover observed research flows: `uses_input`, `evidence_basis`, `routes_to`, `supports_claim`, `derived_from`, `supersedes`, `produces`, `materializes_file`, `blocks`, `cites`, `summarizes`, and `custom.*`.

Edges must distinguish source. Authored edges come from explicit create/update metadata. Payload-derived edges come from structured payload fields such as `evidence_refs`, `artifact_refs`, `selected_hypothesis_id`, or known profile sections. Body-inferred edges are allowed only as low-confidence repair hints.

### Extract GUI Facets from Structured Payloads

Facet extraction should be profile-driven. The existing DeepSci record profiles already shape payloads for ideas, route decisions, run records, result summaries, artifact manifests, and claim validation records. An extractor registry can map profile refs to facet extractors without asking each skill to write every SQL row manually.

Unknown scalar JSON values can be stored in `research_record_json_facts` when they are useful for inspection but do not deserve a dedicated table yet. This keeps the first schema practical while allowing future GUI panels to discover data.

### Index Operation-Set Files as Attachments

Worker output directories contain result JSON, CSV, configs, metrics, and other files that matter to experiments. The file index should record those paths, roles, operation-set ids when known, digests when available, existence status, media type, and semantic labels.

The file table should not force every output file to become an Artifact record. Artifact records remain useful for accepted durable outputs; file rows handle denser experiment folders and UI drill-down.

### Provide Rebuild and Export Commands

The implementation should provide an idempotent rebuild for one Topic Workspace. It reads lifecycle records, structured payloads, rendered Markdown refs, and accepted operation-set files, then recreates derived index rows while preserving authored rows.

The implementation should also provide cleanup for stale derived rows, orphaned index rows, and missing-file attachment rows. Cleanup is an index maintenance operation only; canonical research records and files remain visible for repair, supersession, or withdrawal.

The GUI-facing export should return nodes, edges, files, facets, diagnostics, and detail locators for a selected topic. The export is a query contract, not a web API commitment; CLI JSON and Python APIs can share the same shape.

### Update Skills Through Binding Guidance

DeepSci placeholder bindings should describe expected relationship, file, and facet metadata per placeholder/profile. Skills should still author structured payload JSON and readable generated Markdown; the record system and extractor registry should handle repetitive index rows.

This avoids the anti-pattern of making every skill workflow hand-maintain a graph while still teaching agents what relationships and files are worth preserving at write time.

## Validation

Runtime validation should report missing indexed records, broken edges, cross-topic refs, missing files, stale derived rows, unsupported claim links, and profile extractor failures. It should not delete canonical records or silently rewrite payloads.

Validation diagnostics should name whether an issue comes from authored metadata, derived payload extraction, file scanning, or low-confidence body inference. That distinction lets operators repair the right layer.

## Migration Plan

1. Add additive query-index tables through Workspace Runtime schema preparation.
2. Add store APIs for refreshing one record, rebuilding one topic index, validating the index, cleaning stale derived index rows, listing indexed records, and exporting indexed records with facets.
3. Add profile-driven extractors for the first observed DeepSci payload families: ideas, route decisions, run records, result summaries, artifact manifests, and claim validation.
4. Extend record create/update request objects and CLI JSON input with optional relationship, file, and index-hint metadata.
5. Update DeepSci placeholder binding guidance with expected relationship, file, and facet metadata.
6. Validate against an existing FlashAttention topic workspace by rebuilding the index, validating/cleaning stale derived rows in preview mode, and exporting ideas, decision path, experiment results, files, and claims.

Rollback is straightforward: ignore or drop query-index tables and continue reading canonical lifecycle records, payload rows, and rendered files.

## Open Questions

- Should authored index metadata be stored in separate append-only source tables, or can authored rows live in the same index tables with source classification?
- Which profile families should get dedicated facet tables after the first GUI panels are chosen?
- Should operation-set file scanning include every file under worker output, or only files named by artifact manifests and known result profiles?
- Which query export views should the first GUI consume first: graph, dashboard, timeline, ideas, experiments, or claims?
