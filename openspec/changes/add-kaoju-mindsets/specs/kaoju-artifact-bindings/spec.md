## ADDED Requirements

### Requirement: Kaoju Mindset Records Preserve Run-Scoped Source Snapshots
The Kaoju semantic and binding registries SHALL define `KAOJU:MINDSET-RECORD` as a validated structured-file current-state Artifact whose required Run scope preserves one action's exact mutable Mindset Source snapshot and evolving reflective answers.

#### Scenario: Mindset Record binding is described
- **WHEN** a caller describes `KAOJU:MINDSET-RECORD`
- **THEN** the binding reports producer `isomer-ext-kaoju-entrypoint`, applicable Kaoju consumers, `current_state`, required Run scope, scoped-current selection, the Mindset Record format profile, and relationships to the Run, active survey context, and cited evidence
- **AND** it does not register the Mindset Source file as an Artifact or claim that the derived-intent root is a records directory

#### Scenario: Mindset Record snapshots a Source
- **WHEN** the entrypoint creates a Mindset Record from a validated topic Mindset Source
- **THEN** the body records `mindset_key`, source semantic label `topic.intent.kaoju_mindsets`, safe relative Source path, Source content digest, and optional Source derivation metadata
- **AND** every materialized answer row snapshots the exact question id, prompt, `additional_notes`, answer expectation, required posture, and evidence expectation before recording answer state, answer or rationale, and evidence refs

#### Scenario: Mindset Record pins active survey context
- **WHEN** a Mindset Record is accepted
- **THEN** it contains the canonical Research Topic ref and exact current `KAOJU:SURVEY-CONTRACT` revision ref
- **AND** it contains the selected `KAOJU:DIRECTION-SET` or direction-scoped `KAOJU:READING-LIST` ref and current `KAOJU:RELATED-WORK-CATALOG` and `KAOJU:CLAIM-EVIDENCE-LEDGER` refs when those Artifacts are present

#### Scenario: Mindset Record is revised during a Run
- **WHEN** an authorized producer checkpoints changed answers, rationale, collector posture, supplemental rows, or evidence with the expected current revision
- **THEN** the service creates a new Mindset Record revision in the same Run scope and preserves earlier answer state
- **AND** it rejects any request that changes the Source digest, materialized Source-question snapshot, or pinned survey context within that Run

#### Scenario: Mutable Source changes after snapshot
- **WHEN** the Mindset Source file changes after its Record has started
- **THEN** the existing Record remains independently readable from its exact snapshot and retains the original Source digest and path
- **AND** no Artifact relationship validator requires the current mutable Source file to retain the old content

### Requirement: Mindset Record Payload Validation Is Closed and Bounded
The Kaoju Mindset Record profile and semantic validator SHALL accept only declared fields and SHALL enforce bounded source locators, question snapshots, prompts, `additional_notes`, answers, supplemental questions, evidence refs, and total serialized content.

#### Scenario: Valid Mindset Record is checked
- **WHEN** a Mindset Record satisfies the common structured envelope and Mindset Record profile
- **THEN** validation returns its normalized Run identity, mindset key, Source digest, snapshot inventory, collector posture, supplemental inventory, and acceptance posture
- **AND** the exact snapshotted prompt and note content remains canonical Record data rather than a projection from the mutable Source file

#### Scenario: Source locator is invalid
- **WHEN** a Record has a malformed semantic label, unsafe or absolute Source path, key and filename mismatch, malformed digest, or Source path outside the resolved mindset root
- **THEN** validation rejects the revision with the affected field
- **AND** the prior Run-scoped Mindset Record remains current

#### Scenario: Snapshot inventory is invalid
- **WHEN** snapshot rows have duplicate ids, omit required Source fields, include undeclared authority-bearing fields, exceed a bound, or differ across revisions in the same Run
- **THEN** validation rejects the revision with the affected row and field
- **AND** the prior Run-scoped Mindset Record remains current

#### Scenario: Supplemental question is invalid
- **WHEN** a supplemental row has a duplicate or malformed Record-local id, unsupported origin, association basis, or disposition, missing introduction stage, collides with a snapshotted Source question, claims `source_updated` without a valid new Source path and digest, lacks explicit Record targeting, or exceeds a declared bound
- **THEN** validation rejects the revision with the affected supplemental id and field
- **AND** the prior Run-scoped Mindset Record remains current

#### Scenario: Evidence or context relationship is invalid
- **WHEN** a Mindset Record contains a malformed, cross-topic, stale, ambiguous, or disallowed required context or evidence ref
- **THEN** relationship validation rejects the revision
- **AND** the prior Run-scoped Mindset Record remains current

## MODIFIED Requirements

### Requirement: Kaoju Binding Inventory Covers Core Survey Objects
The production Kaoju binding inventory SHALL cover every durable object required by the legacy procedures, the ten survey-process use cases, and checked mindset routes while leaving derived-intent Mindset Sources outside the Artifact registry.

#### Scenario: Core semantic inventory is present
- **WHEN** the shared registry and binding registry are inspected
- **THEN** they cover workspace readiness, binding index, `KAOJU:SURVEY-CONTRACT`, Comparison Intent Document, `KAOJU:PROCEED-DECISION`, `KAOJU:DISCOVERY-LEDGER`, `KAOJU:RELATED-WORK-CATALOG` and its deltas, `KAOJU:CURATED-INTAKE-DELTA`, Source Digest, Source Access Blocker, `KAOJU:CLAIM-EVIDENCE-LEDGER`, material acquisition, Topic Dataset Manifest, Generated Dataset, Method Trial, theory comparison, Comparison Matrix, Audit Report, `KAOJU:CLAIM-STATUS-TABLE`, `KAOJU:FIELD-SUMMARY`, Kaoju Dossier, terminal report, method-trial Runs, comparison Runs, and `KAOJU:MINDSET-RECORD`
- **AND** neither `KAOJU:MINDSET-SOURCE` nor another semantic id is registered for a topic Mindset Source file

#### Scenario: New durable output needs a disposition
- **WHEN** a later Kaoju skill adds an accepted durable output
- **THEN** it adds a semantic registry entry, binding entry, and family-neutral profile or records an explicit non-structured binding disposition
- **AND** derived-intent input files remain outside this rule unless they become accepted durable research output
