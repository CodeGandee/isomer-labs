## 1. Add the Kaoju Topic-Creation Skill and Default Seeds

- [x] 1.1 Add protected member `isomer-kaoju-topic-creator` at `isomer-ext-kaoju-entrypoint->topic-creator`, declare its dependency and projection metadata, and add a context-aware protected routing row.
- [x] 1.2 Add public Kaoju command `create-topic`, command page, checked command classification, welcome mapping, and delegation guidance that sends generic Project, Research Topic, Topic Workspace, and `topic.intent.overview` work to `isomer-op-entrypoint->topic-create` before Kaoju derivation.
- [x] 1.3 Add schema-valid default JSON resources under `isomer-kaoju-topic-creator/assets/defaults/mindsets/` for `paper.deep-dive`, `paper.skimming`, and `source-code.ingest` with the approved exact 8/6/8 seed inventories, empty `additional_notes`, and exact `additional-questions` collector.
- [x] 1.4 Update packaged-skill manifest, validation, materialization, extension command metadata, versioned skill metadata, and inventory tests for seventeen Kaoju bundles and fifteen protected members, and verify that no protected mindset manager is exposed.

## 2. Add the Derived-Intent Mindset Source Surface and Schema

- [x] 2.1 Add topic-scoped semantic directory label `topic.intent.kaoju_mindsets`, default path `intent/derived/mindsets`, owner-editable durable-directory metadata, configured and recorded-aware resolution, and label-based materialization.
- [x] 2.2 Add safe deterministic `<mindset_key>.json` child resolution with key grammar, direct-child containment, filename/body equality, and no cwd, sibling-topic, or directory-scan fallback.
- [x] 2.3 Add a closed bounded non-Artifact Mindset Source schema and validator covering schema version, key, purpose, applicability, optional derivation metadata, ordered questions, collector, `additional_notes`, answer and evidence expectations, ids, counts, lengths, total size, and rejection of executable or authority-bearing fields.
- [x] 2.4 Add package validation that loads each topic-creator default through the same Source validator, verifies exact seed ids, prompts, empty notes, collector contract, unique keys, filenames, applicability, and deterministic digests, and compares required keys with process routes.
- [x] 2.5 Add human-readable Source rendering or skill reporting that escapes user content and distinguishes packaged seed, topic-derived Source, optional provenance, current path, digest, fixed questions, notes, and collector without registering an Artifact.

## 3. Derive and Preserve Topic Mindset Sources

- [x] 3.1 Teach `isomer-kaoju-topic-creator` to require one concrete `topic.intent.overview`, resolve `topic.intent.kaoju_mindsets`, read packaged seeds, and generate missing Sources only after generic topic state is ready, whether invoked by explicit `create-topic` or extension-local lazy ensure.
- [x] 3.2 Implement topic-specific generation that preserves each key and collector, may adapt fixed questions and `additional_notes` from stable overview concerns, retains ids for reused concepts, assigns unique ids to new concepts, avoids inventing future survey context, and permits unchanged seed copies when specialization adds no value.
- [x] 3.3 Add create-missing idempotency that preserves every existing valid Source across explicit create-topic, lazy ensure, retry, repair, and package upgrade and reports created, preserved, invalid, missing, and advisory derivation-drift results by key.
- [x] 3.4 Add explicit regeneration, replacement, or reconciliation behavior within the Kaoju topic-creation workflow that re-reads the current file and digest, validates the proposal, checks the observed base before atomic replacement, and reports old and new digests without changing active Run snapshots.
- [x] 3.5 Add direct packaged-default copy support and tests showing that a copied valid JSON file becomes topic-owned Source state without export, import, Artifact mutation, or specialized mindset CLI commands.
- [x] 3.6 Add missing, invalid, conflicting, wrong-topic, unsafe-path, and stale-derivation diagnostics; missing Sources trigger extension-local create-missing before a concrete research Run, while invalid existing Sources block with Kaoju `create-topic` repair and never trigger overwrite or package-default runtime fallback.

## 4. Define Mindset Record Artifact Contracts

- [x] 4.1 Register only `KAOJU:MINDSET-RECORD` in the Kaoju semantic and binding inventories with structured-file content, `topic.records.artifacts`, producer and consumer metadata, `current_state`, required Run scope, scoped-current selection, and Source-snapshot, survey-context, and evidence relationships.
- [x] 4.2 Add a family-neutral Mindset Record Artifact Format Profile and schema containing Source semantic label, safe relative path, key, digest, optional derivation metadata, immutable materialized question snapshots, exact prompts and `additional_notes`, answers, rationale, evidence refs, collector posture, supplemental rows, and terminal unresolved state.
- [x] 4.3 Add Mindset Record semantic and relationship validation for Run and topic scope, current Survey Contract and optional survey-context refs, Source locator syntax, immutable snapshot inventory across revisions, answer states, evidence refs, explicit supplemental association, and `record_only`, `source_update_requested`, and `source_updated` dispositions.
- [x] 4.4 Add Record rendering that remains independently readable after Source edits and clearly distinguishes materialized Source questions, exact snapshotted notes, answers, collector posture, explicitly assigned supplemental questions, Source-update status, evidence, and unresolved items.
- [x] 4.5 Extend generic Artifact service tests for create, scoped-current query, optimistic-concurrency checkpoint, prior revision preservation, malformed locator, changed snapshot rejection, invalid evidence, cross-topic context, and terminal validation.

## 5. Inject Mindset Records into Applicable Workflows

- [x] 5.1 Extend checked Kaoju process metadata with Source schema version, semantic root label, required route keys, applicability selectors, Record semantic id, and topic-creator repair designator without embedding Source bodies or a packaged runtime fallback.
- [x] 5.2 Implement route validation and selection for deep or full-text paper examination, skim or triage paper examination, and repository or source-tree examination; actions without declared mindset requirements continue unchanged.
- [x] 5.3 Update the public Kaoju entrypoint to run `isomer-kaoju-topic-creator` create-missing preflight before a concrete mutation-bearing research Run, then begin the Run, re-resolve and validate the selected Source, pin current survey context, create the exact Mindset Record snapshot before focused-owner dispatch, include its ref in Run inputs and handoffs, and reject applicable `complete` or claim-bearing acceptance without a terminal Record.
- [x] 5.4 Keep installation, welcome, help, `explore`, and status-only management non-mutating; they may report missing mindset intent but must not enumerate topics, invoke lazy ensure, create a Run, or write Source files.
- [x] 5.5 Update `commands/ingest-reading-item.md`, `commands/ingest-source-code.md`, direct examination routing, and `isomer-kaoju-examine/SKILL-MAIN.md` to require the handed-off Record, answer and checkpoint its immutable materialized questions, check the collector, and avoid re-reading a changed Source during the Run.
- [x] 5.6 Route ordinary paper and source-code follow-up questions to Source Digest, Claim-Evidence Ledger, Associated Source Code, or other reading Artifacts; add supplemental Record rows only under explicit Record targeting and clarify ambiguous bare-mindset mutation requests.
- [x] 5.7 Implement explicit Source-only, Record-only, and both targeting: direct validated Source edit with no Record row, `record_only`, and `source_update_requested` to `source_updated` with new path and digest while the active Record keeps its original snapshot.

## 6. Remove Superseded Planned Surfaces

- [x] 6.1 Ensure the implementation adds no `KAOJU:MINDSET-SOURCE`, Source Artifact Format Profile, Source binding, generic post-runtime extension bootstrap, or core Topic Creator mindset behavior.
- [x] 6.2 Ensure public and protected inventories add no `manage-mindset`, `isomer-kaoju-mindsets`, eight-leaf mindset command tree, or `isomer-cli ext kaoju mindsets` list, show, bootstrap, export, import, or reset surface.
- [x] 6.3 Remove or update any provisional tests, docs, fixtures, or process metadata from the superseded Artifact-backed Source design before implementation acceptance.

## 7. Document and Validate the End-to-End Contract

- [x] 7.1 Update the canonical Isomer domain-language document with packaged mindset default, Mindset Source, Mindset Record, derived-intent ownership, direct-edit lifecycle, mutable-Source snapshot semantics, and mindset-versus-Workflow distinction.
- [x] 7.2 Update Kaoju entrypoint, welcome, topic-creation, examination, reading-item, source-code, shared guidance, README, command maps, process-contract documentation, semantic-path documentation, and CLI reference where applicable.
- [x] 7.3 Add integration tests for explicit new-topic generic delegation plus mindset derivation, first concrete Kaoju use after late installation, existing-topic lazy create-missing, no install-time topic scan or write, read-only no-write behavior, no mindset data passed into the core Topic Creator, unchanged-seed fallback, topic-specialized generation, direct edit, copied default, preserve-on-retry and upgrade, explicit replacement, derivation drift, invalid Source blockers, active-Run Source mutation, ordinary-question routing, explicit Source/Record/both targeting, and fail-closed terminal Record validation.
- [x] 7.4 Run package asset validation, focused unit and integration tests, `pixi run lint`, `pixi run typecheck`, `pixi run test`, and strict OpenSpec validation; record any unrelated pre-existing failures separately.
