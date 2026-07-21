## Context

`project outputs policy` currently resolves a worker-local output root, an operation-set naming pattern, and the `commit_after_operation` preference. It deliberately leaves files under that root as staging material until a separate research-record action accepts them. Production DeepSci guidance already says durable outputs belong in research records and already teaches `--parents-json`, Research Idea recording, and payload validation, but completion is not conditioned on proving that every material file in an operation set crossed that boundary.

The existing record store is the correct mutation authority. A `ResearchRecordRequest` can snapshot payload or body content, create canonical record-lineage edges, and apply explicit Research Idea effects in the same record-level transaction. Record creation also refreshes the query index. The new layer must coordinate these existing operations, not introduce a second record model or infer semantics from filenames.

An operation set can contain several records, supporting files, staging payloads, and disposable diagnostics. Accepting the set therefore spans filesystem copies and multiple record-level transactions. A single rollback transaction would either be false or would require deleting already durable provenance. The coordinator needs preflight validation plus resumable, receipt-backed application instead.

## Current v0.4.0 Baseline

The known issue records a historical incident, not the current state of the Flash Attention 4 Topic Workspace. Two distinct gaps appeared during that incident:

| Historical gap | Current state | Response in this change |
| --- | --- | --- |
| Important operation-set files were not promoted to durable records before the workflow reported completion. | The affected files were manually imported, but future file-producing operations can still omit this step. | Add an exhaustive, receipt-backed closeout coordinator and make DeepSci completion depend on it. |
| Importing records alone did not create canonical Research Ideas or Idea Lineage visible to the GUI. | v0.4.0 supplies atomic `research_idea_effects`, portfolio facets, decision context, canonical lineage, and GUI-facing queries; the affected topic data was updated to that contract. | Reuse and verify the existing contract. Do not add another idea model or migrate the repaired data. |

The current direct path remains authoritative:

```text
existing record create/revise request
  -> payload and lineage validation
  -> durable record plus authored research_idea_effects in one record transaction
  -> query-index refresh
  -> current Records and Idea Graph APIs
```

The proposed coordinator inserts a closeout boundary before that path. It does not change what a Research Idea means or how the GUI classifies one:

```text
worker operation set
  -> exhaustive manifest and preflight
  -> existing record create/revise transaction
  -> additive acceptance receipt and verification
```

## Goals / Non-Goals

**Goals:**

- Make every material operation-set file accountable before a research workflow reports success.
- Prevent recurrence of the historical omission while preserving the current v0.4.0 record, Research Idea, lineage, decision, and GUI contracts.
- Provide one explicit manifest that maps staged files to durable record actions, managed attachments, canonical record parents, and any authored Research Idea effects.
- Reuse current format-profile resolution, payload validation, record creation or revision, lineage validation, idea mutation, and query-index refresh behavior.
- Preserve durable progress when a multi-record acceptance fails partway and make an identical retry idempotent.
- Give production DeepSci skills and pipelines a small, testable terminal gate rather than relying on prose reminders.
- Support explicit repair of legacy operation sets without sweeping or mutating them automatically.

**Non-Goals:**

- Watch worker directories or automatically import files in the background.
- Guess record kinds, semantic ids, parents, evidence meaning, Research Ideas, or idea lineage from filenames, extensions, Markdown, or model interpretation.
- Replace `ext research records`, `ext research ideas`, Artifact Format Profiles, placeholder bindings, or canonical lineage stores.
- Define new Research Idea facets, lifecycle states, selection semantics, decision vocabulary, lineage semantics, or GUI projections.
- Rewrite, backfill, or migrate the already repaired Flash Attention 4 records and Research Ideas as part of installation or implementation validation.
- Make Git tracking or `.gitignore` state determine whether research content is durable.
- Roll back or delete a record that committed successfully because a later item in the same operation set failed.
- Require a durable record for files explicitly classified as disposable scratch material with a concrete reason.

## Decisions

### 1. Use an Explicit Operation Set Acceptance Manifest

Each operation set has a reserved `.isomer-operation-set/` control directory containing a versioned manifest and optional generated plan views. Files inside that control directory are coordinator state; every other regular file under the operation-set root enters the inventory regardless of Git tracking state.

The manifest contains topic and worker identity, a stable `operation_set_id`, producer skill and lifecycle refs, an `outputs` inventory, and named `record_intents`. Each output carries a normalized relative path, digest, size, and one disposition:

- `record_payload`: the file is the body or structured payload of a named record intent and will be snapshotted into owner-preserved record storage.
- `record_attachment`: the file is a managed attachment of a named record intent and will be copied into owner-preserved record storage with its digest and operation-set identity.
- `disposable`: the file is intentionally excluded from durable research state and includes a non-empty reason.

Record intents use stable local keys and declare `create`, `revise`, or `reference` actions. They carry the existing record binding fields, source output keys, immediate parent specs, generation and decision context when applicable, and existing `research_idea_effects` data. `reference` supports legacy repair or a file already accepted through another operation without duplicating the record.

This split lets one record consume several files and prevents the manifest from repeating record metadata on every output row. It also makes completeness mechanical: the inventory and output dispositions must match exactly.

Alternative considered: infer one record per file from the extension and filename. Rejected because a Python file may be an implementation artifact, an attachment to a structured change map, or disposable scratch code, and no filename can establish canonical parents or idea effects.

### 2. Resolve and Secure the Operation-Set Boundary Through Worker Output Policy

`inspect` resolves Effective Topic Context plus exactly one Topic Actor or Agent output policy. The selected operation-set root must be a direct or nested operation-specific child of that resolved worker output root. Paths are normalized and checked by real path; absolute manifest paths, parent traversal, duplicate normalized paths, special device files, and symlinks that escape the operation set are rejected. Inspection does not follow directory symlinks or execute content.

The coordinator hashes files by streaming reads. Apply rechecks every size and digest immediately before mutation, and verify rechecks them against the accepted receipt. A changed file blocks the affected acceptance rather than silently updating the plan.

Alternative considered: accept any user-provided directory. Rejected because it would bypass Topic Workspace and worker ownership boundaries and could import unrelated or secret files.

### 3. Add a Provider-Neutral CLI and Service Layer

The public family is:

- `isomer-cli ext research operation-sets inspect <operation-set-path>` inventories the set, compares an optional manifest, reports missing dispositions and binding gaps, and can write a manifest scaffold only when explicitly requested.
- `isomer-cli ext research operation-sets accept <manifest-path>` performs a non-mutating plan by default; `--apply` executes the validated plan.
- `isomer-cli ext research operation-sets verify <receipt-or-operation-set-id>` checks the receipt, managed content, durable records, canonical lineage, Research Idea effects, and queryability.

The service belongs under the research extension because it orchestrates research records and ideas. `project outputs policy` remains the path-policy authority, while operator routing points users and agents to the focused recording skill or this CLI family.

The service is deliberately additive. It translates each manifest intent into the current record service request and delegates authored idea effects to the current atomic mutation path. Acceptance receipts track operation-set reconciliation only; they do not become a second source of truth for idea state, selection, decisions, or lineage. Existing records and ideas are unaffected until an explicit acceptance request targets a selected operation set.

Alternative considered: add `record-operation-set` to `isomer-op-project-mgr`. Rejected because Project lifecycle management does not own research-record semantics and non-operator Agents also need this capability.

### 4. Preflight the Whole Plan, Then Apply It as a Resumable Saga

Acceptance first resolves every binding, loads and validates every payload, validates every referenced record and Research Idea, detects record dependency cycles, topologically orders local record keys, reserves deterministic result ids where possible, checks destination collisions, and verifies the exhaustive file inventory. Any preflight error produces a plan with diagnostics and performs no mutation.

With `--apply`, Workspace Runtime creates an acceptance receipt header and one item row per record intent. Each item has an input digest and state. The coordinator then calls existing record create or revise behavior, including record-level lineage and idea effects, and snapshots managed attachments. A successful item stores its durable record id and effect refs before the next item starts.

Receipt states are `applying`, `partial`, `complete`, and `superseded`. If an item fails, already committed records remain durable and the receipt becomes `partial`. Reapplying the same manifest digest verifies completed items and resumes pending or failed items without creating duplicates. A changed manifest conflicts with the existing operation-set revision unless it declares a new revision and the receipt it supersedes.

Alternative considered: wrap all files and records in one global transaction. Rejected because filesystem snapshots and record-level provenance cannot be rolled back reliably, and deleting committed research history would violate the existing corrective-provenance model.

### 5. Store Durable Receipts Separately from Research Content

Workspace Runtime adds `operation_set_acceptances` and `operation_set_acceptance_items`. The header stores scope, worker identity, canonical root, manifest digest, status, supersession, timestamps, diagnostics, output disposition summary, and provenance refs. Item rows store record key, intent digest, action, state, resulting record id, idea-effect refs, and failure diagnostics.

The receipt proves that staging was reconciled; it is not itself an Artifact, Evidence Item, or claim. Research content stays in existing lifecycle records. Accepted record metadata and managed file rows carry `operation_set_id` and the receipt id so records and receipts can be correlated in either direction.

### 6. Snapshot Durable Attachments into Owner-Preserved Storage

Payload and body inputs continue to use the existing managed copy paths. Operation-set acceptance extends record storage with managed file attachments copied under the owning record directory using collision-safe names and recorded digests. Query-index file rows point to the managed copies, not the worker staging paths. The receipt retains the original relative path for audit.

This prevents a record from appearing durable while its code, CSV, figure, or reference note exists only in a disposable worker tree. Explicit external or repository content may use `reference` only when the manifest names an already durable locator and verification can prove the relationship.

Alternative considered: keep attachments in place and index their worker paths. Rejected because worker output roots can be cleaned, moved, or overwritten independently of topic-owned records.

### 7. Keep Record Lineage and Research Idea Effects Explicit and Separate

Each record intent declares immediate durable parents using the existing lineage kinds and may refer to earlier local record keys in the same plan. Missing parent knowledge is a blocking diagnostic or an explicit root reason; the coordinator does not derive a parent from file timestamps or prose.

Idea-bearing payload profiles require `idea_effects_required=true` and exact object-valued realization paths. The coordinator passes those authored effects to the existing record transaction and verifies the resulting Research Ideas, realizations, transitions, decision options, generation groups, and lineage refs. Record lineage never becomes idea lineage automatically.

### 8. Make Operation-Set Acceptance the Final DeepSci Gate

The shared DeepSci guidance gains an Operation Set Closeout reference. Any focused production skill that opens or writes an operation set adds a numbered closeout step after end callbacks and before its final response. The step invokes the focused core recording skill or CLI, then reports accepted record refs and a complete receipt. If no operation set was opened, the terminal result records `closeout: not_applicable`; merely losing track of a path does not qualify.

An incomplete inventory, failed record, unverifiable lineage, or missing idea effect yields a recoverable paused result with the manifest path, receipt when present, diagnostics, and resume command. It does not become a successful chat summary.

The pipeline accepts stage outputs only as durable refs plus a complete receipt or an explicit `not_applicable` closeout. Pipeline-level files are reconciled in the same way before the pipeline terminal report can say `complete`.

### 9. Package a Focused Core Recording Skill

`research/isomer-research-operation-set-recording` becomes a core packaged skill beside `isomer-research-idea-recording`. Its workflow covers context and worker selection, inspection, binding lookup, manifest completion, preview, apply, verify, partial recovery, and legacy repair. It explicitly refuses to invent semantic ids or lineage and routes idea-bearing entries through the established idea-recording contract.

The operator entrypoint indexes the skill and `ext research operation-sets` commands. DeepSci references the core skill rather than duplicating command recipes across every focused skill. Repository validators check the packaged manifest, skill resources, workflow markers, DeepSci closeout steps, and pipeline terminal-gate language.

## Risks / Trade-offs

- [Manifest authoring adds friction] → `inspect` emits a deterministic scaffold and the focused skill resolves known placeholder bindings, while unresolved semantics remain visible instead of guessed.
- [A strict inventory can include low-value logs] → Explicit `disposable` dispositions are cheap but require a reason, and the reserved control directory avoids self-referential manifests and receipts.
- [Multi-record application can stop midway] → Preflight catches deterministic failures first, item receipts preserve committed work, and identical retries resume safely.
- [Files may change between execution and acceptance] → Digests are checked at inspect, apply, and verify; drift requires a new manifest revision.
- [Managed attachment copies consume storage] → Durability takes precedence for accepted output; later content-addressed deduplication can optimize storage without weakening the contract.
- [Skill-only enforcement can still be ignored] → CLI receipts and validator-enforced terminal fields make completion machine-checkable by pipelines and acceptance tests.
- [Legacy operation sets lack complete semantic context] → Repair remains explicit, supports existing-record references, and reports unknown parents or ideas rather than fabricating them.

## Migration Plan

1. Freeze the current v0.4.0 baseline with regression tests for direct record create and revise behavior, atomic `research_idea_effects`, canonical queries, and GUI-facing idea data contracts.
2. Add the additive Workspace Runtime tables, store models, manifest parser, path checks, and read-only inspection and planning APIs without changing current record or Research Idea schemas.
3. Add managed attachment snapshotting, resumable apply, receipt queries, and verification by delegating durable mutations to the existing record and Research Idea transaction.
4. Register the CLI family and add unit and integration tests using a fresh temporary Topic Workspace fixture that models the historical Flash Attention 4 chain without mutating the current topic.
5. Package and validate `isomer-research-operation-set-recording`, then expose it through operator entrypoint routing.
6. Update shared and focused DeepSci guidance and validators, followed by the pipeline stage and terminal gates.
7. Document an optional legacy repair procedure. Do not scan or mutate existing Topic Workspaces during installation, upgrade, or routine validation.

Rollback removes the new CLI registration and skill gates while leaving the additive runtime tables and any completed receipts readable. Records created through acceptance remain ordinary durable research records and must not be deleted during rollback.

## Open Questions

None required before implementation. The v0.4.0 record and Research Idea model is a fixed dependency of this change, not an open design area. Attachment deduplication and adoption by research paradigms other than DeepSci can be separate changes after the core acceptance contract proves stable.
