# Design Rationale: Accept Operation-Set Research Outputs

## Intended Reader

This rationale is for Isomer maintainers and research-workflow authors who need to understand why operation-set persistence requires a new completion contract, even though research-record creation already exists.

## Executive Summary

The known issue describes a historical gap between producing research files and accepting research results. DeepSci operations wrote valuable reports, evidence, code, and notes into worker operation sets, then returned successful terminal summaries. Nothing required the agent or pipeline to prove that those files had become durable research records with canonical lineage and any required Research Idea effects.

Since that incident, v0.4.0 added the current Research Idea portfolio contract, including atomic `research_idea_effects`, canonical lifecycle and decision data, lineage, and GUI-facing queries. The Flash Attention 4 records and ideas were also repaired. This proposal does not redesign that model or repair that data again. It addresses the remaining recurrence risk: a future file-producing operation can still finish without invoking the existing durable-record transaction for every material output.

The proposal introduces an explicit Operation Set Acceptance boundary. Every material file must be mapped to a durable record payload, copied as a managed record attachment, or marked disposable with a reason. A preview-first command validates the full plan, an apply step records resumable progress, and a verify step produces a machine-checkable completion receipt. DeepSci skills and pipelines cannot report success until that receipt is complete.

This addresses the remaining issue because it changes operation-set closeout from advisory guidance into a terminal invariant that the system can inspect, enforce, retry, and test.

## What Is Actually Being Changed

This proposal changes both `isomer-cli` and the skills, but the core capability belongs to `isomer-cli`. It is not only a revision of skill wording.

| Layer | Proposed change |
| --- | --- |
| `isomer-cli` | Add `ext research operation-sets inspect`, `accept`, and `verify`; add manifest validation, managed attachment copying, resumable acceptance, and Workspace Runtime receipts while reusing current record and idea mutations. |
| Core recording skill | Add `isomer-research-operation-set-recording` to guide agents through the CLI workflow without duplicating command details in every research skill. |
| DeepSci skills | Revise file-producing workflows to invoke operation-set acceptance after end callbacks and before reporting success. |
| DeepSci pipeline | Refuse to advance when a stage provides only worker file paths; require verified durable record refs and a complete receipt. |

The runtime flow is:

```text
DeepSci produces files
  -> a skill invokes operation-set acceptance
  -> isomer-cli validates and records the outputs
  -> isomer-cli returns a verified receipt
  -> the skill or pipeline may report completion
```

The CLI is the enforcement mechanism. It inventories files, validates record intent, applies durable mutations, records progress, and verifies the result. Skills do not implement another persistence layer; they call the CLI and treat its receipt as their completion gate.

Both parts are required. Skill changes alone remain instructions that an agent may overlook. CLI changes alone provide a mechanism that research workflows are not required to call. Combining them makes the behavior available, mandatory, and machine-verifiable.

The proposal is therefore best described as a new CLI-backed Operation Set Acceptance capability that is integrated by revising the core recording guidance, production DeepSci skills, and DeepSci pipeline. It is not a new Research Idea model, a GUI redesign, or a migration of the repaired Flash Attention 4 topic.

## Historical Incident and Current Baseline

The issue was written before two later changes: the v0.4.0 Research Idea portfolio implementation and the manual correction of the affected Topic Workspace. The design must separate what remains open from what is already fixed.

| Concern exposed by the issue | Current status | Scope of this proposal |
| --- | --- | --- |
| Six valuable operation-set outputs had no durable record. | The six outputs were imported and their record lineage was reconstructed. | Do not import them again. Prevent future operations from reaching success with unreconciled files. |
| Record import alone did not populate the Idea Graph. | The current record request supports atomic authored `research_idea_effects`, and the topic now uses canonical Research Ideas, realizations, lineage, portfolio facets, and decision context. | Delegate to and verify this current contract. Do not add another idea schema or GUI projection. |
| Skills described persistence but did not prove closeout. | File-producing DeepSci workflows can still omit the recording step because no exhaustive receipt gates completion. | Add manifest, receipt, verification, skill closeout, and pipeline gates. |
| Accepted supporting files could still depend on worker paths. | Payload and body snapshots are managed, but arbitrary operation-set attachments have no general owner-preserved acceptance path. | Add managed attachment snapshotting as part of acceptance. |

The current durable-record path is authoritative:

```text
record create or revise
  -> current payload and lineage validation
  -> durable record plus authored research_idea_effects in one transaction
  -> current query index and GUI-facing APIs
```

The proposal adds a coordinator before and around that path:

```text
operation-set files
  -> exhaustive manifest and preflight
  -> current record create or revise path
  -> additive receipt proving every file disposition and promised effect
```

The receipt answers whether one staging set was reconciled. The research database remains the authority for records, Research Ideas, lifecycle state, decisions, and lineage.

## The Problem

### Operation Sets Are Staging Areas, Not the Research Database

`project outputs policy` gives a Topic Actor or Agent a safe worker-local directory and an operation-set naming pattern. Files placed there are plain generated outputs. They are useful during execution, but they do not become Artifacts, Evidence Items, Decision Records, Provenance Records, or Research Ideas merely because they exist.

The Flash Attention 4 work exposed this boundary before the current data repair. The research process produced an idea exploration report, two microbenchmark reports, a predictor validation report, predictor code, and a SASS reference note. These files remained under the operator's worker output root. They were absent from research-record queries until a separate manual recovery imported them. They are present now; this history serves as the motivating example rather than as migration input.

### The Workflow Had a False Completion Signal

The operation treated two weak signals as completion evidence:

- The expected files existed in an operation-set directory.
- The agent returned a terminal summary describing the work.

Neither signal proves that the Topic Workspace owns a durable record, that the payload passed its format contract, or that immediate parents were recorded. They also do not prove that downstream queries and the GUI can find the result.

Existing DeepSci instructions mention durable records and lineage, but those instructions are distributed across skills and references. An agent can produce plausible output while omitting the final recording commands. A later agent cannot distinguish a genuinely disposable file from an important result that was forgotten.

### The Historical Failure Had Two Independent Lineage Layers

Research record lineage and Research Idea lineage answer different questions:

- Record lineage explains how durable Artifacts and Evidence Items were produced from earlier durable records.
- Idea lineage explains how concepts were derived, selected, merged, deferred, closed, or followed up.

Manual record import initially repaired the Records view and record-lineage graph but did not automatically promote embedded candidate ideas into canonical Research Ideas or create Idea Lineage Edges. That historical mismatch motivated the later v0.4.0 portfolio contract and topic-data correction. The current GUI can consume canonical idea data; this proposal does not alter those GUI semantics.

Operation-set acceptance must preserve this separation by passing explicitly authored idea effects through the current transaction and verifying them. Automatically projecting record parents into idea parents would create unsupported conceptual claims.

### Plain Worker Files Remain Fragile

A record that only points back to a worker output path is not fully durable. Worker output sets can be cleaned, moved, overwritten, or duplicated. Code, figures, CSV files, and reference notes must be copied into owner-preserved record storage when they are accepted as attachments.

### Manual Recovery Does Not Scale

The Flash Attention 4 recovery required a human or capable agent to inspect six operation sets, choose record kinds and semantic ids, create records, reconstruct immediate parent edges, link a note to a Research Idea, and validate the result. This was possible because the research history was still fresh. The same reconstruction becomes unreliable after more stages, workers, or revisions.

The system needs to capture acceptance intent at operation closeout, when the producer still knows what each file means and which records are its immediate parents.

## Root Cause

The remaining root cause is not the absence of record-writing or idea-writing primitives. `ResearchRecordRequest` already supports managed payload snapshots, record lineage, and explicit Research Idea effects. Record creation also updates the query index.

The missing capability is coordination and enforcement across a whole operation set:

1. No exhaustive inventory identifies every material file that needs a disposition.
2. No single plan connects files to record bindings, immediate parents, and Research Idea effects.
3. No receipt proves that the complete plan committed and remains queryable.
4. No terminal gate prevents skills or pipelines from reporting success when acceptance is incomplete.
5. No idempotent recovery model handles a multi-record closeout that stops partway.

## Proposed Design

### 1. Add an Explicit Acceptance Manifest

Each operation set receives a versioned manifest under a reserved `.isomer-operation-set/` control directory. The manifest inventories every other regular file, regardless of Git tracking state.

Each file has exactly one disposition:

| Disposition | Meaning |
| --- | --- |
| `record_payload` | The file is the structured payload or body of a durable record and will be snapshotted into managed record storage. |
| `record_attachment` | The file supports a durable record and will be copied into owner-preserved attachment storage. |
| `disposable` | The file is scratch output that does not belong in the research database; the manifest records a concrete reason. |

The default is opt-out. A material file without a disposition blocks completion. This makes forgotten results visible without forcing disposable debug output into the database.

The manifest also contains named record intents. A record intent declares whether it will create, revise, or reference a record. It includes the existing record binding fields, its source files, immediate parents, and explicit Research Idea effects when applicable.

### 2. Add Inspect, Accept, and Verify Commands

The provider-neutral CLI family is:

```text
worker operation set
        |
        v
inspect -> complete manifest -> accept preview -> accept --apply -> verify
                                                           |
                                                           v
                                                complete receipt
```

`inspect` resolves the selected worker output policy, checks path containment, inventories files, computes digests, and reports missing dispositions or bindings. It can create a scaffold when explicitly requested, but it does not guess semantics.

`accept` is non-mutating by default. It resolves record bindings, validates payloads, expands local record dependencies, checks parents and Research Idea refs, topologically orders record actions, and reports the expected effects. `--apply` is required for mutation.

`verify` checks the receipt, file digests, records, managed attachments, canonical record lineage, explicit Research Idea effects, and queryability. A terminal workflow uses this result as completion evidence.

### 3. Reuse Existing Record and Idea Mutations

The coordinator does not create a parallel storage model. Each record intent is converted into the current create, revise, or reference behavior. Record-level transactions keep the existing format validation, lineage validation, idea-effect validation, provenance, and query-index refresh behavior.

This choice reduces semantic drift. A record created through operation-set acceptance behaves like the same record created directly through `ext research records`.

The coordinator does not define idea facets, lifecycle transitions, decision semantics, generation groups, or Idea Lineage Edge meaning. It carries authored `research_idea_effects` into the current transaction and records the returned refs in the acceptance receipt. Existing records and ideas remain untouched unless an explicit operation-set manifest targets them through a supported create, revise, or reference action.

### 4. Snapshot Accepted Attachments

Payload and body files already have managed copy paths. The proposal extends managed storage to operation-set attachments. Accepted code, figures, tables, CSV files, and notes are copied under the owning record and indexed from the managed path.

The receipt preserves the original operation-set path and digest for audit, but durable queries do not depend on the worker staging file remaining present.

### 5. Use a Resumable Receipt Instead of False Atomicity

One operation set can create several records and copy several files. These actions span SQLite and the filesystem. A global transaction cannot honestly roll back every side effect, and deleting a successfully committed record would erase durable provenance.

The design performs full preflight before mutation, then applies the plan as a resumable saga. Workspace Runtime stores an acceptance receipt and one item state per record intent.

- If every item succeeds and verifies, the receipt becomes `complete`.
- If a later item fails, earlier records remain durable and the receipt becomes `partial`.
- Reapplying the same manifest digest verifies completed items and resumes the remainder without duplicates.
- A changed manifest requires an explicit new acceptance revision that identifies the superseded receipt.

This model matches the actual consistency boundary and gives operators a precise recovery point.

### 6. Preserve Explicit Lineage

The manifest must name immediate durable record parents using accepted lineage kinds. It can refer to earlier record intents in the same manifest. The planner orders those dependencies and rejects cycles.

If the producer cannot identify a parent, it must record an explicit root reason, report a missing-parent diagnostic, or leave the plan incomplete. The coordinator does not infer authoritative parents from filenames, timestamps, directory order, or prose.

Idea-bearing outputs require explicit Research Idea effects with stable idea ids and exact object-valued realization paths. Record lineage never implies Idea Lineage Edges.

### 7. Make Acceptance the Final DeepSci Gate

Every active DeepSci workflow that writes an operation set gains a numbered closeout step after end callbacks and before the final response or handoff. Running after end callbacks ensures callback-generated files are also reconciled.

The skill may report success only when it has one of these outcomes:

- A complete acceptance receipt and the accepted durable record refs.
- `closeout: not_applicable` because the skill opened no operation set and worked only with durable records.

Missing dispositions, invalid payloads, unknown parents, partial receipts, or missing Research Idea effects produce a paused result with diagnostics and a resume command.

`isomer-deepsci-pipeline` applies the same rule at stage boundaries. It passes durable record refs to the next stage. A worker path or terminal summary alone is not a produced artifact.

### 8. Add a Focused Core Recording Skill

The core `isomer-research-operation-set-recording` skill owns the guided workflow for inspection, binding lookup, manifest completion, preview, apply, verification, partial recovery, and legacy repair.

This skill is provider-neutral because operation-set durability belongs to Isomer's research-record boundary, not to DeepSci or Project lifecycle management. DeepSci calls the focused skill instead of duplicating a long command recipe in every stage skill.

## Why This Addresses the Issue

| Observed failure | Design response | Resulting guarantee |
| --- | --- | --- |
| Important files remained only in worker output sets. | Exhaustive manifest plus mandatory disposition. | A material file cannot be silently omitted from a complete closeout. |
| Agents returned success without creating records. | DeepSci and pipeline terminal gates require a verified receipt. | File existence and chat summaries no longer count as completion evidence. |
| Record kinds and profiles were chosen during manual recovery. | Record intents resolve existing placeholder bindings and format profiles during preflight. | Accepted outputs follow the same contracts as direct record creation. |
| Parent edges were reconstructed later. | Each intent declares immediate parents before apply. | Provenance is captured while the producer still has current context. |
| Historical record import did not populate the Idea Graph. | Idea-bearing intents delegate explicit effects and exact realization paths to the current v0.4.0 record transaction, then verify its canonical results. | Future closeout uses the current model consistently without introducing a second idea store or changing GUI semantics. |
| Code and notes depended on worker paths. | Managed attachment snapshots copy accepted files into topic-owned storage. | Durable records remain usable after worker cleanup. |
| Re-running recovery could duplicate records. | Manifest digests, receipt items, and idempotent resume identify completed effects. | An identical retry verifies or resumes instead of duplicating. |
| A failure during a multi-record import had no clear recovery point. | Partial receipts preserve item-level progress and diagnostics. | Operators can resume from the failed item without deleting committed history. |
| Legacy operation sets still exist. | Explicit inspect and reference intents support repair. | Existing records can be verified and linked without automatic duplication. |

The central guarantee is:

> A research operation that wrote material files cannot report successful completion until every file has an explicit disposition and every promised durable effect is queryable and verified.

That guarantee closes the still-open workflow boundary that caused the historical Flash Attention 4 omission. The separate data-model and topic-data corrections remain intact and outside this change.

## Why Simpler Alternatives Are Insufficient

### Strengthen Skill Wording Only

Stronger prose still relies on agent compliance. It cannot inventory forgotten files, prove a record exists, detect a missing parent edge, or stop a pipeline from advancing. The proposal retains clear instructions but backs them with a receipt and validator-enforced terminal gate.

### Automatically Infer Records and Lineage

Filename and extension heuristics cannot determine whether a JSON file is experiment evidence, an analysis summary, a cache, or a disposable diagnostic. They also cannot establish immediate parents or conceptual idea relationships. Automatic inference would replace missing provenance with fabricated provenance.

The system may generate a manifest scaffold and surface known bindings, but unresolved semantics remain explicit decisions.

### Watch Worker Directories and Import Everything

A watcher would race with files that are still being written and would persist temporary logs, failed drafts, secrets, or incomplete payloads. It would also lack the producer's route and parent context. Explicit closeout runs after the operation reaches a stable boundary.

### Treat Git Commit as Acceptance

Git answers whether a file is version-controlled. It does not provide research record identity, semantic profile validation, canonical lineage, evidence meaning, or Research Idea state. A file can be safely committed and still remain invisible to research queries and the GUI.

### Create One Record for the Entire Directory

One directory record would hide the different meanings and parent chains of experiment evidence, code, reports, and notes. It would also prevent precise query, revision, and Research Idea realization behavior. The manifest allows several files to support one record and several records to belong to one operation set.

### Require One Global Transaction

The workflow copies files and creates several provenance-bearing records. Deleting earlier records when a later copy fails would damage history. Preflight plus resumable item receipts gives stronger and more honest recovery semantics.

## Example: How the Historical Flash Attention 4 Closeout Would Differ

If the proposed closeout contract had existed during the original workflow, it would have created manifests as the research progressed:

1. The idea exploration report becomes an analysis campaign summary with the selected hypothesis as an immediate parent.
2. The first microbenchmark report becomes experiment evidence with the exploration report as a `follow_up_to` parent.
3. The optimized report revises the first benchmark result through `revision_of`.
4. Predictor validation derives from the optimized benchmark and the exploration report.
5. Predictor code becomes an implementation change-map record with the validation result as its parent and the code copied as a managed attachment.
6. The SASS note becomes a research-note record with the implementation record as its parent and an explicit realization of the SASS-grounded Research Idea.

Each operation could verify its own receipt immediately. The next stage would receive record ids instead of paths, so the lineage chain would already exist when the research moved forward.

This is a counterfactual validation scenario. Implementation tests should reproduce the shape of the chain in a fresh temporary Topic Workspace; they must not re-import or mutate the current Flash Attention 4 records and ideas.

## Scope and Limits

The first mandatory integration targets production DeepSci workflows because that is where the failure occurred. The CLI and core skill remain provider-neutral so Kaoju or future research paradigms can adopt the same boundary later.

The change does not automatically migrate existing operation sets. Automatic migration would lack trustworthy semantic and parent context. Maintainers can repair legacy sets explicitly with inspection, reference intents, and verification.

The change also does not infer Research Idea lineage from record lineage. It makes missing idea effects visible and blocks a promised effect from being reported as complete, but the producer must author the conceptual relationship.

The change does not revise canonical Research Idea facets, lifecycle states, decision options, generation groups, lineage semantics, CLI contracts, or GUI projections introduced by v0.4.0. It also does not treat the current Flash Attention 4 data as needing repair. Those contracts are dependencies and regression-test targets.

## Success Criteria

The implementation closes the known issue's remaining systemic prevention gap when all of these statements hold:

- A DeepSci skill cannot finish successfully while its operation set contains an unclassified material file.
- A complete receipt proves that every accepted record, managed file, record-lineage edge, and promised Research Idea effect is queryable.
- Accepted attachments remain available if the worker operation set is removed.
- Reapplying an unchanged manifest creates no duplicate durable effects.
- A partial application reports an exact safe resume point.
- The pipeline never treats a worker path or terminal summary as a durable artifact handoff.
- Legacy operation sets can be repaired without automatic mutation or invented lineage.
- Direct record creation, atomic Research Idea effects, canonical idea queries, and GUI-facing idea contracts retain their v0.4.0 behavior.
- Installation and validation do not mutate the already repaired Flash Attention 4 topic.

Together, these criteria replace the original best-effort closeout convention with a durable, observable, and testable research completion contract while preserving the current data model.
