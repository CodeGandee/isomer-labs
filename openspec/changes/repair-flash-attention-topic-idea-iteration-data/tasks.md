## 1. Baseline and Rollback

- [x] 1.1 Snapshot `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model/state.sqlite` to an ignored backup path and record the restore command.
- [x] 1.2 Capture baseline runtime, lineage, query-index, idea export, facets, siblings, and record-detail diagnostics with current `isomer-cli`.
- [x] 1.3 Identify stale or missing query-index rows, missing payload/file locators, test records, archived records, and unsupported relationship diagnostics that must be repaired.
- [x] 1.4 Inspect available record profiles and CLI write paths so new or revised records use the latest local runtime conventions.

## 2. Idea and Candidate Records

- [x] 2.1 Preserve raw idea slate item ids, one-liners, statuses, and source JSON paths in structured data or normalized facets without requiring generated Markdown parsing.
- [x] 2.2 Create durable structured records for serious alternatives C2 and C3 from the historical candidate frontier payload.
- [x] 2.3 Verify the selected C1 path exposes candidate id, family, one-liner, source raw idea ids, status, source record refs, and repair provenance where useful.
- [x] 2.4 Ensure rejected, deferred, selected, active, superseded, and follow-up idea states are discoverable from records, payload metadata, route decisions, or facts.

## 3. Lineage and Generation Groups

- [x] 3.1 Add or update canonical lineage edges so selected, alternative, rejected, deferred, experiment, analysis, route, follow-up, and revision paths form a valid topic-scoped DAG.
- [x] 3.2 Create a generation group for serious candidates C1, C2, and C3 with a stable purpose, shared parent set, parent-set digest, and producer or repair metadata.
- [x] 3.3 Attach generation ids, parent roles, decision refs, and concise rationales to candidate lineage edges where the current runtime model supports them.
- [x] 3.4 Keep linear follow-ups as `follow_up_to` or `revision_of` edges and avoid inventing generation groups when the topic has no real sibling alternatives.
- [x] 3.5 Query siblings for each serious candidate and verify the response contains the expected alternatives with no missing generation-group diagnostics.

## 4. Query Index Repair

- [x] 4.1 Rebuild or refresh affected query-index rows after record and lineage repair.
- [x] 4.2 Repair the `experiment-result-summary-bottleneck-saturation-20260706` missing-record diagnostic through indexing, archival repair, or derived-row cleanup.
- [x] 4.3 Verify `query export --view ideas` returns topic-scoped nodes, edges, facets, routes, claims, metrics, facts, and files with no integrity diagnostics.
- [x] 4.4 Confirm historical raw idea duplicates, if still emitted by the extractor, have stable ids and source paths that allow GUI read-model deduplication.
- [x] 4.5 Ensure test and archived records are consistently indexed or explicitly filterable so they do not pollute fixture diagnostics.

## 5. Acceptance Checks

- [x] 5.1 Run current runtime validation, lineage validation, query-index validation, and idea export checks and confirm they report no integrity errors.
- [x] 5.2 Run representative GUI-read checks for facets, lineage, siblings, files, record detail, rendered record content, and export payload shape.
- [x] 5.3 Confirm the repaired data supports the idea iteration map feature without topic-specific filenames, fixed record counts, Markdown parsing, or read-time repair.
- [x] 5.4 Summarize changed topic DB/files, validation commands, remaining non-blocking limitations, and rollback path.
