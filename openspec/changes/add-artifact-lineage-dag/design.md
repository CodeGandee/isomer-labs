## Context

Isomer already stores durable research records in Workspace Runtime and derives a query index for GUI and operator inspection. The current lineage mechanisms are optional and split across payload fields, `revision_of_record_id`, `supersedes_record_id`, `--relationships-json`, and derived `research_record_edges`, so agents can create readable artifacts without creating a durable parent-child graph.

The new requirement is stricter: durable research artifacts should form a topic-scoped DAG. A child can have many parents, siblings are children produced from the same parent set, and back-and-forth revisions become a linear descendant history instead of overwriting prior records.

## Goals / Non-Goals

**Goals:**

- Add canonical lineage storage for parent-child relationships between durable research records.
- Preserve many-to-one and many-to-many derivation patterns without forcing a tree.
- Represent sibling exploration paths through generation groups rather than pairwise sibling edges.
- Treat revisions as new descendant records and keep old records visible.
- Make `isomer-cli` the write path that validates DAG rules.
- Derive query-index graph exports and GUI views from canonical lineage plus existing relationship/facet metadata.
- Teach DeepSci skills to emit lineage parents, generation groups, selected children, merged children, follow-ups, and revision parents when writing records.

**Non-Goals:**

- Do not make all record references part of the DAG. Evidence links, citations, file materialization, summaries, and support/contradiction refs can remain non-canonical query relationships.
- Do not infer authoritative lineage from generated Markdown or unstructured prose.
- Do not force Research Inquiries into a tree or replace Research Inquiry Relationships.
- Do not require every raw idea inside a slate to become a separate record. The DAG becomes precise when serious candidates, selected hypotheses, decisions, experiments, and results are durable records.
- Do not delete or rewrite historical records during revision.

## Decisions

### Decision: Add canonical lineage tables, not just more query-index edges

Workspace Runtime should add `research_record_lineage_edges` and `research_record_generation_groups`. `research_record_edges` remains a rebuildable read model.

`research_record_lineage_edges` stores `parent_record_id`, `child_record_id`, `lineage_kind`, optional `parent_role`, optional `generation_id`, optional `decision_record_id`, `rationale`, `status`, timestamps, and metadata. `research_record_generation_groups` stores `purpose`, `parent_set_digest`, producer skill, optional decision record, timestamps, and metadata.

Alternative considered: treat `research_record_edges` as authoritative. Rejected because the existing table mixes authored hints, payload-derived refs, body inference, and file relations; it is intentionally rebuildable and should not own canonical state.

### Decision: Direction is parent-to-child in canonical storage

Canonical lineage edges use `parent_record_id -> child_record_id`. Query-index projection can preserve current edge semantics by exposing lineage as child-to-parent references where useful, with canonical edge ids in metadata.

Alternative considered: keep query-index direction everywhere. Rejected because parent-to-child is easier for acyclicity validation, descendant traversal, and GUI DAG layout.

### Decision: Small canonical lineage vocabulary

The first canonical lineage kinds should be `derived_from`, `revision_of`, `selected_from`, `merged_from`, and `follow_up_to`.

- `derived_from`: child was produced from parent content.
- `revision_of`: child is the next version of the same semantic artifact.
- `selected_from`: child was selected from one or more candidate parents.
- `merged_from`: child combines multiple parents.
- `follow_up_to`: child continues a prior result, decision, or question.

Alternative considered: add domain-specific kinds such as `idea_to_experiment`, `analysis_to_decision`, or `sibling_of`. Rejected because those are roles or generation-group facts, not core parent-child lineage kinds.

### Decision: Siblings are generation-group membership

Siblings are records created in the same generation group from the same parent set. The system should not create pairwise `sibling_of` edges for every candidate pair.

This keeps a frontier with 8 candidates from creating 28 sibling edges and preserves the real meaning: the candidates represent alternative children of the same parents under one exploration pass.

### Decision: Revisions create new descendant records

A content-changing revision creates a new record with `revision_of` pointing to the immediate prior revision. The older record remains visible and may be marked non-latest or superseded. `latest_for_semantic_id` remains a latest-view helper, not the lineage source of truth.

Alternative considered: update the existing structured payload row in place. Rejected because GUI history, auditability, and paper/research traceability require previous payloads to remain inspectable.

### Decision: CLI validates lineage at write time

`isomer-cli ext research records create` should accept lineage parents and generation-group metadata. A new `revise` command should create a descendant record from an existing record. Lineage mutation commands should exist for repair or migration, but normal agents should use create/revise.

Proposed command shapes:

```bash
isomer-cli ext research records create --topic <topic> --record-kind artifact --payload-file <payload.json> --parents-json '[{"record_id":"artifact-A","role":"candidate_frontier"}]' --lineage-kind selected_from --generation-id idea-pass-20260706-01
```

```bash
isomer-cli ext research records revise <record-id> --topic <topic> --payload-file <payload.json> --rationale "Tightened hypothesis after analysis result"
```

### Decision: Query index projects canonical lineage

Query-index rebuild should read canonical lineage tables, payload refs, relationship hints, and file attachments. Exported graph views should mark each edge's `source_classification`, with canonical lineage clearly distinguished from authored relationship hints and payload-derived refs.

### Decision: Skills must record lineage in workflow steps

The production DeepSci skill contract should add a shared `artifact-lineage-recording` reference and include explicit lineage steps in idea, optimize, experiment, analysis, decision, write, review, and finalize flows when they create durable records.

For idea flow, the expected chain is objective/board/survey to raw slate, raw slate to candidate frontier, candidate frontier to serious pre-idea drafts, serious drafts and evidence to route decision, selected draft and route decision to selected hypothesis, selected hypothesis to experiment contract.

## Risks / Trade-offs

- [Risk] Existing topics have sparse or prose-only lineage. → Treat migration as best-effort backfill from explicit refs only, report gaps as diagnostics, and do not infer authoritative parentage from Markdown.
- [Risk] Agents may keep using `--relationships-json` instead of canonical lineage inputs. → Update DeepSci placeholder bindings and skill workflows, and add validation warnings when idea/experiment/analysis profiles omit expected lineage.
- [Risk] DAG validation can be slow on large topics. → Scope checks to one Topic Workspace, index parent/child columns, and use recursive SQL only on candidate insert paths.
- [Risk] Many raw ideas inside one artifact cannot be exact DAG nodes. → Require serious candidates and selected hypotheses to become separate durable records when precise lineage is needed.
- [Risk] Revision command may overlap with update command. → Keep update for metadata/status and repair; use revise for content-changing accepted records.

## Migration Plan

1. Add Workspace Runtime tables and schema migration helpers for lineage edges and generation groups.
2. Add runtime dataclasses, store methods, and validation diagnostics for canonical lineage.
3. Add CLI create/revise/lineage/query command options and JSON parsing.
4. Project canonical lineage into query-index rebuild/export/lineage APIs.
5. Update GUI/backend read models to prefer canonical lineage when available.
6. Update DeepSci shared guidance, placeholder bindings, and key workflow references.
7. Backfill only explicit existing refs such as `revision_of_record_id`, `supersedes_record_id`, `parent_record_id`, `source_refs`, and authored relationship metadata when the source is unambiguous.
8. Leave historical topics with missing lineage diagnostics rather than fabricating edges.

Rollback is straightforward before data migration because new tables are additive. After migration, rollback should leave canonical lineage tables in place as ignored extra state rather than deleting audit history.

## Open Questions

- Should `supersedes` remain a non-lineage relationship, or should it be modeled as a status/result of `revision_of` and route decisions?
- Should query-index relation vocabulary add canonical `revision_of`, `selected_from`, `merged_from`, and `follow_up_to`, or should it expose them through metadata while keeping existing relation kinds?
- Should create reject expected-lineage omissions for known profiles, or warn first and tighten later after skill updates land?
