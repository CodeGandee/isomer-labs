## ADDED Requirements

### Requirement: Operation Set Acceptance Resolves Worker Context
The system SHALL resolve an operation set through Effective Topic Context and exactly one Topic Actor or Agent worker output policy before it inspects or accepts files.

#### Scenario: Topic Actor operation set is resolved
- **WHEN** a caller selects a Topic Actor and an operation-set path below that actor's resolved worker output root
- **THEN** the system returns the canonical operation-set root, worker identity, Topic Workspace identity, and stable operation-set identity

#### Scenario: Agent operation set is resolved
- **WHEN** a caller selects an Agent and an operation-set path below that agent's resolved worker output root
- **THEN** the system applies the same acceptance contract with the Agent identity recorded in the plan and receipt

#### Scenario: Ambiguous worker context is rejected
- **WHEN** a caller selects both an Agent and a Topic Actor or selects neither when cwd cannot resolve exactly one worker
- **THEN** the system rejects the request without inspecting or mutating research records

### Requirement: Operation Set Paths Stay Inside the Resolved Output Root
The system SHALL reject operation-set manifests and entries that escape the resolved worker output root or selected operation-set root.

#### Scenario: Parent traversal is rejected
- **WHEN** a manifest path is absolute, contains parent traversal, or normalizes outside the operation-set root
- **THEN** validation returns a path-containment error and performs no mutation

#### Scenario: Escaping symlink is rejected
- **WHEN** a file or directory symlink resolves outside the selected operation-set root
- **THEN** inspection reports the escaping entry and does not follow or accept it

#### Scenario: Special file is rejected
- **WHEN** inspection encounters a device, socket, named pipe, or another non-regular material entry
- **THEN** it reports an unsupported-entry diagnostic instead of reading or executing the entry

### Requirement: Acceptance Manifests Exhaustively Classify Material Files
The system SHALL use a versioned Operation Set Acceptance Manifest whose inventory accounts for every regular file outside the reserved coordinator control directory.

#### Scenario: Inspection produces deterministic inventory
- **WHEN** `ext research operation-sets inspect` scans a valid operation set
- **THEN** it returns stable normalized relative paths, streaming content digests, byte sizes, media types when known, and manifest reconciliation status in deterministic order

#### Scenario: Git ignore state does not hide material files
- **WHEN** a regular operation-set file is ignored or untracked by Git
- **THEN** the file still appears in the acceptance inventory because Git tracking does not establish research durability

#### Scenario: Every output has one disposition
- **WHEN** a manifest is validated
- **THEN** each inventoried file has exactly one disposition of `record_payload`, `record_attachment`, or `disposable`
- **AND** no manifest disposition refers to a missing or duplicate normalized path

#### Scenario: Disposable output requires a reason
- **WHEN** an output is classified as `disposable`
- **THEN** the manifest includes a non-empty reason and the acceptance receipt preserves that reason

#### Scenario: Manifest scaffold is explicit
- **WHEN** a caller requests scaffold output from inspection
- **THEN** the system writes only coordinator control material and leaves unresolved dispositions and record bindings visibly incomplete

### Requirement: Record Intents Use Existing Recording Contracts
An Operation Set Acceptance Manifest SHALL map durable output dispositions to named record intents that use existing research-record bindings and mutation semantics.

#### Scenario: Create intent declares a binding
- **WHEN** a record intent creates a durable record
- **THEN** it declares the record kind, semantic id when extension-owned, scope key when required, format profile or supported body form, producer skill, lifecycle refs, and source output keys required by the existing recording contract

#### Scenario: Revise intent preserves history
- **WHEN** a record intent changes accepted content for an existing record
- **THEN** it uses the existing revise path and records the prior record as the unique immediate `revision_of` parent

#### Scenario: Reference intent verifies existing acceptance
- **WHEN** a legacy or repeated operation maps an output to an existing durable record
- **THEN** a `reference` intent verifies the record, managed content digest or attachment relationship, scope, and expected lineage without creating a duplicate record

#### Scenario: Managed attachment is snapshotted
- **WHEN** an output has disposition `record_attachment`
- **THEN** the system copies it into owner-preserved storage under the target record, records its digest and operation-set identity, and indexes the managed copy rather than relying on the worker staging path

### Requirement: Existing Canonical Record and Idea Contracts Remain Authoritative
The operation-set coordinator SHALL delegate durable record, record-lineage, Research Idea, decision, generation, and Idea Lineage mutations to the existing canonical recording contracts and SHALL NOT define a replacement idea model or GUI projection.

#### Scenario: Idea-bearing acceptance uses the current atomic transaction
- **WHEN** a record intent declares authored `research_idea_effects`
- **THEN** the coordinator passes those effects through the existing record mutation transaction and records the canonical returned refs in the acceptance item

#### Scenario: Acceptance receipt does not duplicate idea state
- **WHEN** an accepted record creates or changes a Research Idea, realization, lifecycle state, decision option, generation membership, or Idea Lineage Edge
- **THEN** the canonical research stores remain the source of truth and the acceptance receipt stores only reconciliation status and refs

#### Scenario: Coordinator introduces no implicit idea semantics
- **WHEN** a manifest omits an authored Research Idea effect or conceptual lineage relation
- **THEN** the coordinator neither fabricates that effect nor substitutes a new facet, lifecycle, decision, or lineage vocabulary

#### Scenario: Existing topic data is unchanged by adoption
- **WHEN** Isomer installs, validates, or enables operation-set acceptance
- **THEN** existing records, Research Ideas, realizations, lifecycle state, decisions, lineage, and GUI query results remain unchanged until a caller explicitly applies a manifest that targets supported mutations

### Requirement: Acceptance Planning Is Non-Mutating by Default
The `ext research operation-sets accept` command SHALL preview a complete acceptance plan unless the caller explicitly supplies `--apply`.

#### Scenario: Valid plan is previewed
- **WHEN** a caller runs accept without `--apply` on a valid manifest
- **THEN** the command returns ordered record actions, file snapshots, lineage effects, Research Idea effects, expected receipt identity, and diagnostics without changing Workspace Runtime or managed record files

#### Scenario: Whole-plan preflight fails safely
- **WHEN** any payload, binding, path, parent, idea ref, dependency order, digest, or destination check fails
- **THEN** the command reports every deterministic preflight error it can discover and creates no record, attachment, idea effect, or acceptance receipt

#### Scenario: Local record dependencies are ordered
- **WHEN** a child intent names another intent in the same manifest as an immediate parent
- **THEN** planning topologically orders those intents and rejects a local dependency cycle

### Requirement: Applied Acceptance Is Deterministic and Resumable
The system SHALL persist receipt-backed item progress while applying a valid operation-set plan through existing record and Research Idea mutation services.

#### Scenario: Apply creates receipt and item progress
- **WHEN** a caller applies a valid manifest
- **THEN** Workspace Runtime records an acceptance receipt with scope, worker, root, manifest digest, output dispositions, provenance refs, and one item state per record intent

#### Scenario: Successful apply completes receipt
- **WHEN** every intent commits and verifies successfully
- **THEN** the receipt status becomes `complete` and contains resulting record ids, managed file refs, lineage refs, and Research Idea effect refs

#### Scenario: Mid-apply failure preserves durable progress
- **WHEN** a later intent fails after an earlier intent committed
- **THEN** the earlier durable record remains intact, the failed receipt becomes `partial`, and item diagnostics identify the safe resume point

#### Scenario: Identical retry resumes without duplication
- **WHEN** a caller reapplies the same operation-set revision and manifest digest
- **THEN** the coordinator verifies successful items, resumes incomplete items, and does not create duplicate records, attachments, lineage edges, or Research Idea effects

#### Scenario: Changed manifest requires a new revision
- **WHEN** an operation set already has a receipt and a caller supplies a different manifest digest without an explicit new revision and superseded receipt ref
- **THEN** the system reports an acceptance-revision conflict and performs no mutation

### Requirement: Acceptance Receipts Are Workflow Provenance
Workspace Runtime SHALL store acceptance receipts separately from durable research content while preserving correlation in both directions.

#### Scenario: Receipt is not research evidence
- **WHEN** an acceptance receipt is queried
- **THEN** it identifies reconciliation status and resulting refs but is not treated as an Artifact, Evidence Item, Finding, Research Claim, or Decision Record

#### Scenario: Accepted records identify their operation set
- **WHEN** a record is created or revised through operation-set acceptance
- **THEN** its metadata and managed file rows include the operation-set id and acceptance receipt id

#### Scenario: Receipt history is preserved
- **WHEN** a new acceptance revision supersedes a prior receipt
- **THEN** the prior receipt remains queryable and the supersession relationship is explicit

### Requirement: Verification Gates Operation-Set Completion
The system SHALL mark an acceptance receipt complete only when file reconciliation and all promised canonical effects are queryable and valid.

#### Scenario: Complete receipt verifies
- **WHEN** `ext research operation-sets verify` checks a complete receipt
- **THEN** every material output has its recorded disposition, every managed digest matches, every record exists, canonical lineage validates, promised Research Idea effects exist, and record queries return the accepted refs

#### Scenario: Unclassified file prevents completion
- **WHEN** an operation set contains a material file absent from the manifest or lacking a valid disposition
- **THEN** acceptance cannot become complete and verification reports the exact relative path

#### Scenario: File drift is reported
- **WHEN** a staged or managed file no longer matches the digest recorded by the receipt
- **THEN** verification reports drift without silently changing the receipt or durable record

#### Scenario: Missing canonical effect is reported
- **WHEN** a receipt promises a parent edge, realization, transition, decision option, generation membership, or Idea Lineage Edge that is not queryable
- **THEN** verification reports the missing effect and does not treat prose or query-index extraction as a substitute

### Requirement: Acceptance Preserves Record and Idea Lineage Boundaries
The coordinator SHALL require authored canonical lineage and SHALL keep record lineage separate from Research Idea lineage.

#### Scenario: Immediate record parents are explicit
- **WHEN** a record intent derives from prior durable records
- **THEN** the manifest declares each immediate parent, lineage kind, and parent role when applicable before apply

#### Scenario: Unknown parent is not invented
- **WHEN** the producer cannot responsibly identify a parent
- **THEN** the manifest records an explicit root or missing-parent reason or remains incomplete instead of inferring lineage from filenames, timestamps, or prose

#### Scenario: Idea-bearing output requires idea effects
- **WHEN** a supported profile or manifest marks an accepted record as idea-bearing
- **THEN** the intent requires explicit Research Idea effects with stable idea ids and exact object-valued realization paths before completion

#### Scenario: Record lineage does not imply idea lineage
- **WHEN** accepted records have canonical parent edges but no authored Idea Lineage Edge
- **THEN** the coordinator records only record lineage and does not synthesize an Idea Lineage Edge

### Requirement: Legacy Operation Sets Can Be Repaired Explicitly
The system SHALL support inspection and receipt-backed acceptance of existing operation sets without scanning or mutating them automatically during upgrade.

#### Scenario: Legacy set is inspected
- **WHEN** a user selects an existing operation set created before this capability
- **THEN** inspection inventories its current files and reports missing dispositions, binding fields, parents, and idea effects needed for acceptance

#### Scenario: Manually recovered record is referenced
- **WHEN** a legacy output already has a manually created durable record
- **THEN** the repair manifest can reference and verify that record and record-lineage state instead of creating another copy

#### Scenario: Upgrade leaves legacy sets unchanged
- **WHEN** Isomer installs or upgrades this capability
- **THEN** it creates no acceptance receipt and mutates no legacy operation-set file until a caller explicitly inspects or applies that set
