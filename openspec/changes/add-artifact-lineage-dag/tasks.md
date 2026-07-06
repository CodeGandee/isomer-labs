## 1. Runtime Data Model

- [ ] 1.1 Add canonical lineage edge and generation group dataclasses to the runtime records model.
- [ ] 1.2 Add SQLite schema creation and migration support for `research_record_lineage_edges` and `research_record_generation_groups`.
- [ ] 1.3 Add topic-scoped indexes for parent, child, lineage kind, generation group, and parent-set digest lookups.
- [ ] 1.4 Add store methods to create, list, validate, and delete or archive canonical lineage edges and generation groups.
- [ ] 1.5 Implement cycle detection for canonical lineage insertions within one Topic Workspace.
- [ ] 1.6 Enforce revision-chain constraints so `revision_of` has exactly one immediate parent per child record.

## 2. Recording API And CLI

- [ ] 2.1 Extend research record create/update request parsing with canonical lineage inputs separate from `--relationships-json`.
- [ ] 2.2 Add `--parents-json`, `--lineage-kind`, `--generation-id`, `--generation-purpose`, and `--decision-record-id` options to create where appropriate.
- [ ] 2.3 Add `ext research records revise <record-id>` to create a descendant record with a `revision_of` lineage edge and preserved semantic identity.
- [ ] 2.4 Add lineage maintenance commands for explicit edge add, DAG validation, ancestor/descendant query, and sibling query.
- [ ] 2.5 Ensure create/revise operations store lifecycle record and payload first, then validated lineage rows in the same Topic Workspace.
- [ ] 2.6 Return lineage diagnostics in JSON output without mixing them with query-index relationship hint diagnostics.

## 3. Query Index And GUI Read Model

- [ ] 3.1 Project canonical lineage edges into query-index rebuild and export outputs with a distinct source classification.
- [ ] 3.2 Update lineage query behavior to prefer canonical lineage traversal for ancestors and descendants.
- [ ] 3.3 Add sibling query/read-model behavior based on generation groups and parent-set identity.
- [ ] 3.4 Extend relation or lineage vocabulary handling for `revision_of`, `selected_from`, `merged_from`, and `follow_up_to`.
- [ ] 3.5 Update Project Web GUI backend read models to expose canonical lineage, generation groups, siblings, and diagnostics.
- [ ] 3.6 Keep read-only query/export operations from repairing, backfilling, or mutating lineage rows.

## 4. DeepSci Skill Contracts

- [ ] 4.1 Add a shared DeepSci reference that defines artifact lineage recording, lineage kinds, generation groups, sibling semantics, and revision behavior.
- [ ] 4.2 Update all DeepSci `placeholder-bindings.md` files to distinguish canonical lineage inputs from relationship, file, and facet hints.
- [ ] 4.3 Update `isomer-deepsci-idea` workflow and references to record lineage from objective/board/survey through raw slate, candidate frontier, pre-idea drafts, route decision, and selected hypothesis.
- [ ] 4.4 Update `isomer-deepsci-optimize` workflow and references to persist candidate board parent and generation information as canonical lineage.
- [ ] 4.5 Update `isomer-deepsci-experiment` and `isomer-deepsci-analysis` workflows to continue lineage from selected hypothesis to experiment contract, run, result, analysis finding, and route decision.
- [ ] 4.6 Update `isomer-deepsci-decision`, writing, review, and finalize workflows to use revision or follow-up lineage when they change route, content, or publication-facing state.
- [ ] 4.7 Synchronize packaged system skill copies under `src/isomer_labs/assets/system_skills`.

## 5. Migration And Diagnostics

- [ ] 5.1 Add an explicit backfill command or migration helper that converts unambiguous existing `revision_of_record_id`, `supersedes_record_id`, `parent_record_id`, `source_refs`, and authored relationships into canonical lineage rows.
- [ ] 5.2 Report missing lineage for profiles that normally require parents without inferring parentage from generated Markdown.
- [ ] 5.3 Add validation diagnostics for missing records, cross-topic refs, cycles, unsupported lineage kinds, invalid revision chains, and missing generation groups.
- [ ] 5.4 Ensure reset/bootstrap paths initialize lineage schema and leave existing topics without lineage rows valid but diagnostically incomplete.

## 6. Tests And Validation

- [ ] 6.1 Add unit tests for lineage table creation, store round-trips, cycle rejection, cross-topic rejection, multi-parent edges, and revision-chain validation.
- [ ] 6.2 Add CLI tests for create with parents, revise, lineage add, lineage validate, ancestor/descendant query, and sibling query.
- [ ] 6.3 Add query-index tests proving canonical lineage projects to graph/export output and read-only query operations do not mutate runtime state.
- [ ] 6.4 Add skill-content tests or snapshot checks that key DeepSci skills mention lineage recording at durable write steps.
- [ ] 6.5 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
