## Context

The topic `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` is the main realistic sample for the planned topic idea iteration map. It currently has dense runtime data: roughly 174 indexed records, 188 canonical lineage edges, 45 route rows, 43 claim rows, and 150 metric rows. It also has two gaps that make it a weak fixture for the new GUI: the normalized idea table contains only a thin and duplicated view of raw ideas, and canonical generation groups are absent even though the topic contains obvious sibling alternatives.

The topic has already been partially repaired with best-guessed canonical lineage. That gives a usable record DAG, but it still does not look like a topic produced from the latest skill guidance because serious candidates, sibling alternatives, selected hypothesis revisions, and follow-up experiment ideas are not all represented through explicit structured records and generation groups. Query export also reports a missing index row for `experiment-result-summary-bottleneck-saturation-20260706`.

## Goals / Non-Goals

**Goals:**

- Make the Flash Attention topic self-describing enough for the idea iteration map to render idea nodes, alternatives, selected paths, follow-up hypotheses, evidence outcomes, and route decisions without reading generated Markdown.
- Make the topic pass current runtime, query-index, lineage, and representative GUI-read validation checks with no integrity diagnostics.
- Add canonical generation groups for sibling candidate sets and follow-up idea alternatives where the topic already implies siblings.
- Prefer current `isomer-cli` create/revise/lineage/index commands over direct SQLite edits.
- Preserve historical records rather than rewriting the research history into a tidier but false timeline.

**Non-Goals:**

- Do not implement the GUI idea iteration map in this change.
- Do not add new generic CLI commands, schemas, or DeepSci skill behavior unless implementation discovers that a data-only repair cannot pass validation.
- Do not make every raw idea inside the initial raw slate a durable record unless needed to support serious candidate lineage.
- Do not infer new scientific conclusions; only encode relationships already supported by payloads, record titles/summaries, route decisions, and the prior operator-audited lineage pass.

## Decisions

### Decision: Treat this as a fixture-quality data migration, not a product feature

The implementation should repair one Topic Workspace and validate it against existing APIs. The topic data is ignored by Git, but the OpenSpec change should still make the work reproducible: commands, invariants, and validation outputs belong in implementation notes or the final report.

Alternative considered: build the idea-map backend first and special-case this topic at render time. Rejected because the user wants the topic data itself to be sound for future agents.

### Decision: Add durable serious-candidate records for the candidate frontier

The existing `artifact-CANDIDATE_IDEA_FRONTIER-ece06ce63e08` payload has three serious candidates: C1 selected, C2 precision-only, and C3 occupancy-only. C1 already has a pre-idea draft and selected hypothesis. C2 and C3 should get durable candidate/pre-idea records so the GUI can show them as sibling alternatives rather than hidden payload items.

Those new records should carry concise idea text, status, family, source candidate id, source raw idea ids when known, why-now/risk/minimal-validation fields, and expected next action. They should be connected to the candidate frontier with `selected_from` or `derived_from` lineage and placed in one generation group that represents the serious-candidate exploration pass.

Alternative considered: leave C2/C3 only inside the candidate frontier payload and teach the GUI to parse them. Rejected because the feature needs stable source records, statuses, and lineage for selectable idea nodes.

### Decision: Use generation groups for sibling semantics

The repaired topic should add generation groups for at least:

- serious candidates C1, C2, C3 generated from the candidate frontier;
- follow-up hypotheses generated from real-hardware transfer-gap analysis, when represented as multiple durable alternatives;
- later bottleneck-saturation or overlap-revision exploration only when there are actual sibling alternatives, not merely a linear follow-up.

Each generation group should have a stable id, purpose, parent-set digest, producer skill when known, optional decision record, and metadata explaining that it was repaired from historical records.

Alternative considered: encode siblings through pairwise `alternative_to` edges. Rejected because the accepted lineage design uses generation groups for siblings and avoids pairwise edge explosion.

### Decision: Preserve canonical lineage but improve metadata quality

Existing canonical lineage should remain unless validation or clearer structured evidence shows a wrong direction. Repair should add missing parent roles, generation ids, decision record ids, and rationale where useful. Migration metadata should identify that the relationship was repaired from historical data, but the lineage itself should use the same canonical kinds that latest skills would have emitted: `derived_from`, `selected_from`, `revision_of`, `merged_from`, and `follow_up_to`.

Alternative considered: delete and recreate all existing lineage edges. Rejected because the current graph validates and already captures useful historical work.

### Decision: Make query-index diagnostics part of acceptance

After data repair, read-only export for `--view ideas` should have no integrity diagnostics. The missing index row for `experiment-result-summary-bottleneck-saturation-20260706` must be fixed by explicit rebuild, canonical record archival repair, or a minimal indexed row consistent with runtime records. The chosen fix must survive `isomer-cli ext research records index validate`.

Alternative considered: ignore archived or test-like record diagnostics. Rejected because a new agent should not need to decide which warnings are harmless.

### Decision: Keep raw idea item duplication from blocking the fixture only if it is non-diagnostic

The current idea extractor emits duplicate rows for array-valued `raw_ideas` because it sees both the array and each item. If that behavior is still present in latest `isomer-cli`, the implementation can leave duplicate raw idea rows as a known extractor limitation only when the GUI read model can dedupe by `(record_id, idea_id, one_liner)` and validation reports no integrity issue. Serious candidate and selected-hypothesis records must still be non-duplicated and stable.

Alternative considered: hand-delete duplicate idea rows after rebuild. Rejected as the primary strategy because an explicit rebuild could reintroduce them; manual cleanup is only acceptable if implementation also documents the rebuild caveat.

## Risks / Trade-offs

- [Risk] Direct SQLite edits may create data that the current CLI would not produce. → Prefer CLI writes, and if direct SQL is needed for generation-group repair, constrain it to canonical tables and immediately run lineage/query-index/runtime validation.
- [Risk] New durable candidate records may overstate historical certainty. → Mark repair provenance in metadata and use only candidate text already present in structured payloads.
- [Risk] Rebuilding the query index may regenerate duplicate raw idea rows. → Validate that duplicates are presentation noise, not integrity diagnostics, and make serious candidate records the primary GUI nodes.
- [Risk] `isomer-content/` is ignored by Git, so repair state is local. → Final implementation report must name the mutated DB/files and the validation commands so the local fixture can be recreated if needed.
- [Risk] Existing tests or archived smoke-test records may pollute the fixture. → Archive, index, or mark test records explicitly so export diagnostics are clean and the idea map can filter them.

## Migration Plan

1. Snapshot the topic runtime DB and list baseline diagnostics for runtime validation, lineage validation, query-index validation, and `query export --view ideas`.
2. Create or revise structured candidate records for C2 and C3, and add missing metadata to the C1 path if needed.
3. Add generation groups and attach candidate/hypothesis lineage edges with parent roles and rationales.
4. Add explicit relationship metadata for selected, rejected, deferred, superseded, and follow-up states that the idea iteration map needs.
5. Repair query-index rows through explicit rebuild/cleanup; if current extractor limitations remain, document the accepted duplicate shape and ensure validation has no warnings.
6. Run representative read checks: topic export, facets for raw slate/candidate frontier/selected hypotheses, lineage for selected and follow-up hypotheses, siblings for generation-group members, files for candidate records, and record detail with payload.
7. Keep rollback simple: restore the DB snapshot and remove any newly created topic-owned payload folders/files from the Topic Workspace.

## Open Questions

- Should the final repaired fixture include C2/C3 as `PRE_IDEA_DRAFT` records, or introduce a more explicit candidate profile if one already exists in the local format registry?
- Should historical smoke-test records remain indexed as archived records, or be archived and hidden from the fixture-oriented idea export?
- If generation groups cannot be created correctly through the current CLI for existing records, should implementation use direct runtime-store calls or direct SQL with validation?
