## Context

Workspace Runtime already stores research lifecycle records in `state.sqlite`, and `isomer-cli ext research records` can create file-backed records for Artifacts, Evidence Items, Decision Records, Runs, Research Tasks, and View Manifests. The current model is intentionally generic: a row has `record_kind`, status, lifecycle refs, transition metadata, optional `content_path`, and provenance refs. That gives durable identity, but it does not make record relationships queryable.

The FlashAttention GB10 topic workspace shows the failure mode clearly. The records form a meaningful research chain from scout to baseline, idea, optimize, experiment, analysis, paper, review, and finalization. The important edges are present in body prose, for example "contract reference", "parent object", "linked records", and "next route". They are not stored as normalized refs. As a result, a Topic Actor, Operator Agent, validator, or GUI cannot reliably answer lineage questions without reading Markdown bodies and guessing.

The design must preserve existing Topic Workspace ownership rules. The graph belongs in Workspace Runtime, rich content remains file-backed under semantic record labels, and v2 research skills should continue to write readable Markdown or JSON bodies. The graph index adds structured relationship metadata beside those bodies.

## Goals / Non-Goals

**Goals:**

- Add a topic-scoped graph index for relationships between existing Workspace Runtime lifecycle records.
- Add a file attachment index for durable files produced or cited by records.
- Keep lifecycle records as the node authority instead of introducing parallel record identity.
- Make graph writes available through the existing research records extension surface.
- Make common inspection questions deterministic: lineage, children, route, attached files, and export.
- Validate graph refs, file refs, cross-topic leakage, and claim/evidence consistency.
- Keep existing body files and current generic record rows valid.

**Non-Goals:**

- Do not replace `lifecycle_records` with one table per record kind in this change.
- Do not infer graph truth by scraping Markdown as an authoritative write path.
- Do not make `producer` and `consumer` strings into graph edges automatically.
- Do not design a scheduler, workflow engine, or task router.
- Do not require every result file, log, PDF, or script to become a top-level lifecycle record.
- Do not define implementation tasks in this change artifact.

## Decisions

### Store Graph Edges in Workspace Runtime

Add a normalized runtime table for record-to-record edges. Each edge links two existing lifecycle record ids inside the selected Topic Workspace and carries a small relation kind, optional role, status, rationale, metadata JSON, timestamps, actor refs, and provenance refs.

Conceptual shape:

```text
research_record_edges
  id
  research_topic_id
  topic_workspace_id
  source_record_id
  target_record_id
  relation_kind
  relation_role
  status
  rationale
  metadata_json
  created_at
  updated_at
  actor_ref
  provenance_refs_json
```

This table should reference `lifecycle_records` by id at the application validation layer. SQLite foreign keys are optional because existing runtime code already performs scoped validation and because archived or corrective records must remain visible for repair.

Alternative considered: store edges only in `lifecycle_refs_json`. That would be simpler to write, but it leaves edge queries as JSON scans and makes validation weak. A normalized edge table is the cleaner index while preserving the generic lifecycle record envelope.

### Use a Small Relation Vocabulary with Custom Escape Hatch

Use a compact vocabulary that matches research recording needs:

```text
uses_input
produces
derived_from
validates
updates_claim
routes_to
supersedes
blocks
cites
summarizes
materializes_file
```

Allow `custom.*` relation kinds only when the user or a later accepted spec needs a domain-specific edge. Validation should accept `custom.*` but report unknown non-custom relation kinds.

Alternative considered: use unrestricted freeform relation strings. That would avoid early vocabulary debate, but it would recreate the current mess at the graph layer.

### Keep Files as Attachments, Not Always Records

Add a file attachment index for files that belong to, support, or are materialized by a lifecycle record. This covers harness scripts, raw JSON, TXT tables, logs, figures, patches, TeX, PDFs, and package manifests without forcing each file to become an Artifact lifecycle record.

Conceptual shape:

```text
research_record_files
  id
  research_topic_id
  topic_workspace_id
  record_id
  semantic_label
  path
  file_role
  media_type
  digest
  size_bytes
  status
  metadata_json
  created_at
  updated_at
  provenance_refs_json
```

`path` should be stored as the resolved project-local path or as a stable workspace-relative locator, with path resolution and validation still governed by Workspace Path Resolution. `file_role` should use practical values such as `body`, `harness`, `raw_results`, `summary`, `log`, `figure`, `patch`, `paper`, `manifest`, and `custom.*`.

Alternative considered: represent every file as an Artifact record and only use record edges. That is too heavy for generated logs and result shards, and it makes ordinary experiment folders noisy.

### Extend Research Record CRUD Instead of Adding a Separate Indexer API First

The primary write path should remain `isomer-cli ext research records create` and `update`. Add structured options or JSON input for:

- relationship edges created with the record
- file attachments created with the record
- lifecycle refs that point to Research Topic, Research Inquiry, Research Task, Run, Agent Team Instance, Agent Instance, Agent Workspace, or Topic Actor context

The command can expose simple repeatable flags for common cases and a JSON option for complex batches. Python APIs should receive typed request objects and write the record, edges, and files in one transaction.

Alternative considered: create a separate `graph add-edge` command as the only write path. Separate edge writes are useful for repair, but relying on them for normal record creation would make agents forget edges. The default record write path should capture relationships at the moment the author knows them.

### Add Graph Query Commands for Human and GUI Inspection

Add deterministic read commands under the research extension surface, such as:

```text
isomer-cli ext research graph lineage <record-id>
isomer-cli ext research graph children <record-id>
isomer-cli ext research graph route <record-id>
isomer-cli ext research graph files <record-id>
isomer-cli ext research graph export --format json
```

The JSON output should include nodes, edges, attached files, diagnostics, and enough record metadata for a GUI or text UI to render the graph without reopening every body file.

Alternative considered: overload `records list` with graph traversal options. That keeps the command count smaller, but graph traversal and record filtering are different mental models. A small `graph` group is clearer.

### Validation Should Report Graph Breakage Without Deleting Records

Runtime validation should check that graph source and target records exist, belong to the same Topic Workspace, and do not point across topics unless a future cross-topic contract permits it. File attachment validation should check that project-local files exist, remain under allowed semantic surfaces, and do not depend on unpromoted Agent Workspace private material as accepted truth.

Validation should also add focused semantic checks:

- supported Research Claims must cite valid Evidence Items through graph edges or accepted metadata
- `supersedes` edges should not leave multiple ready records claiming to be the active version for the same placeholder without an explicit rationale
- `routes_to` edges should point from a Decision Record or route-bearing record to a plausible next record, cursor, task, or planned lifecycle object
- open Gates and blocking edges should remain visible as blockers

Alternative considered: enforce all graph constraints at insert time. Some research work is partial or corrective, so strict insert-time rejection would make repair harder. Write-time checks should prevent obvious errors; validation should carry the fuller audit.

### Migrate by Adding Index Tables, Then Backfill Opportunistically

Existing workspaces should remain readable. Runtime initialization or schema preparation should create the new tables when opening a current supported schema, or use the repository's existing schema-version path if the change requires a version bump.

Existing `lifecycle_records` can be left as-is. A later repair or bootstrap command may do best-effort backfill from known metadata and body patterns, but scraped edges must be marked as inferred and lower confidence. New writes should be authoritative because agents provide structured refs at creation time.

Alternative considered: require a full migration that parses all existing Markdown before validation passes. That would make adoption fragile and would turn prose parsing into a source of truth.

### Update V2 Placeholder Binding Guidance

Each active v2 skill placeholder binding page should describe the relationship and file refs that its records normally provide. For example, an experiment `MAIN_RUN_RECORD` should link to its `EXPERIMENT_CONTRACT`, produce its artifact manifest, result summary, and route decision, and attach raw output files. An analysis slice should derive from a parent result and update a claim or route boundary.

This is guidance for write-time metadata, not a new skill workflow. The skill remains responsible for readable body content; the record API becomes responsible for durable graph structure.

Alternative considered: centralize all relationship rules only in the workspace manager skill. That would keep per-skill pages smaller, but the producer skill knows the real parents and outputs when it writes the record. Central-only guidance would become stale.

## Risks / Trade-offs

- [Risk] Agents may still omit edges when writing records. Mitigation: make common edges part of placeholder binding command examples and add validation warnings for edge-free records whose profile normally requires lineage.
- [Risk] The relation vocabulary may be too small. Mitigation: allow `custom.*` while keeping core queries focused on accepted relations.
- [Risk] Backfilled edges from old Markdown may be wrong. Mitigation: mark inferred edges distinctly and do not treat them as authoritative support for claims without human or agent confirmation.
- [Risk] Graph tables duplicate information that also appears in body files. Mitigation: treat body prose as explanation and graph rows as indexable refs; validation can report disagreement when a structured ref is stale.
- [Risk] The CLI could become awkward if complex edges are passed through many flags. Mitigation: support both simple repeatable flags and JSON batch input.
- [Risk] File attachments can point at transient logs or private Agent Workspace material. Mitigation: validate paths through semantic labels and report unpromoted private material as not accepted research truth.

## Migration Plan

1. Extend Workspace Runtime schema preparation to create graph edge and file attachment tables without altering existing lifecycle records.
2. Add runtime model and store APIs for creating, listing, validating, and deleting or archiving graph edges and file attachments.
3. Extend research record create and update operations so a record, its edges, and its file attachments can be written transactionally.
4. Add read-only graph query commands and include graph diagnostics in runtime validation output.
5. Update v2 placeholder binding pages and workspace manager bootstrap guidance to include structured graph and file-ref metadata for future records.
6. Optionally add a best-effort repair/index command that proposes inferred edges for existing records, clearly marking them as inferred.

Rollback is straightforward for new code paths: keep reading existing `lifecycle_records` and ignore graph tables if absent. If a runtime has graph tables but the feature is disabled, existing record CRUD remains valid because body files and lifecycle records still carry the durable record identity.

## Open Questions

- Should graph tables require a Workspace Runtime schema version bump, or can they be introduced as idempotent additive tables under the current version?
- Should graph query commands live under `ext research graph`, or should they eventually move to a native `project records graph` surface?
- Which placeholder profiles should require at least one structured edge at validation time in the first release?
- Should file digests be mandatory for all attached files, or optional for large logs and generated binaries?
- How much inferred backfill should the first implementation attempt for existing FlashAttention GB10 records?
