## 1. Baseline, Acceptance Data Model, and Safe Inventory

- [x] 1.1 Add regression tests that freeze the current direct record create and revise behavior, atomic authored `research_idea_effects`, canonical idea and lineage queries, and GUI-facing idea data contracts before adding the coordinator.
- [x] 1.2 Add versioned Operation Set Acceptance Manifest models, strict JSON parsing, canonical serialization, manifest and intent digests, output dispositions, record actions, local record refs, and deterministic diagnostics.
- [x] 1.3 Add additive Workspace Runtime schema and store models for acceptance receipt headers and per-intent item progress, including scope, worker identity, revisions, supersession, statuses, resulting refs, diagnostics, timestamps, and provenance refs; do not change canonical Research Idea schemas.
- [x] 1.4 Implement Topic Actor and Agent operation-set resolution through Effective Topic Context and worker output policy, including real-path containment, reserved control-directory handling, symlink escape checks, special-file rejection, and normalized relative paths.
- [x] 1.5 Implement deterministic streaming inventory and manifest reconciliation that includes Git-ignored files, detects drift and duplicate paths, and writes a scaffold only on explicit request.
- [x] 1.6 Add unit tests for manifest validation, stable digests, exhaustive dispositions, disposable reasons, worker ambiguity, traversal, symlinks, special files, control files, and Git-independent inventory.

## 2. Acceptance Planning and Managed Content

- [x] 2.1 Implement whole-plan preflight that resolves current record bindings, validates payloads and body sources, checks existing record and Research Idea refs, verifies file digests, and returns all deterministic diagnostics without mutation.
- [x] 2.2 Implement local record-key dependency resolution, topological ordering, cycle diagnostics, immediate-parent expansion, revision constraints, generation context, decision context, and explicit root or missing-parent handling.
- [x] 2.3 Extend managed record storage to snapshot operation-set attachments under owner-preserved record directories with collision-safe names, digests, media types, original relative paths, operation-set ids, receipt ids, and query-index file rows.
- [x] 2.4 Build create, revise, and reference execution requests on the existing research-record service so payload snapshots, canonical record lineage, and authored Research Idea effects retain current validation and transaction behavior; do not duplicate idea facets, lifecycle state, decisions, generation state, lineage, or GUI projection in the acceptance store.
- [x] 2.5 Add unit tests for valid plans, preview immutability, binding failures, payload errors, dependency ordering, cycles, revision parents, managed attachment copies, reference verification, and rejection of worker-path-only attachments.

## 3. Resumable Apply and Verification

- [x] 3.1 Implement preview-first acceptance output with ordered actions, managed-copy plans, record lineage, Research Idea effects, expected receipt identity, and stable diagnostic codes.
- [x] 3.2 Implement `--apply` as a receipt-backed saga that records item progress, correlates accepted records and managed files, preserves committed items on later failure, and marks receipts `applying`, `partial`, or `complete` accurately.
- [x] 3.3 Implement deterministic replay and resume for an identical operation-set revision and manifest digest without duplicate records, attachments, lineage edges, realizations, transitions, decision options, or generation memberships.
- [x] 3.4 Implement explicit acceptance revisions and receipt supersession, rejecting changed manifests that omit the required revision and superseded receipt refs.
- [x] 3.5 Implement receipt verification for exhaustive dispositions, staged and managed digests, record queryability, canonical record lineage, promised Research Idea effects, and stale or missing refs without silent repair.
- [x] 3.6 Add optional explicit legacy-repair support for existing operation sets and already recovered records, with no automatic workspace scan, data migration, or upgrade-time mutation.
- [x] 3.7 Add failure-injection and integration tests for preflight no-op, partial apply, safe resume, identical replay, changed-manifest conflict, supersession history, file drift, missing canonical effects, and legacy references.

## 4. Research CLI Surface

- [x] 4.1 Register `isomer-cli ext research operation-sets inspect` with topic and worker selectors, deterministic JSON output, optional manifest comparison, and explicit scaffold writing.
- [x] 4.2 Register preview-first `isomer-cli ext research operation-sets accept` with `--apply`, clear mutation posture, receipt output, and partial-recovery diagnostics.
- [x] 4.3 Register `isomer-cli ext research operation-sets verify` for receipt or operation-set lookup and non-mutating verification.
- [x] 4.4 Add CLI unit and integration tests for help, selector errors, JSON contracts, exit codes, preview versus apply, replay, verify, and human-readable recovery guidance.

## 5. Focused Core Skill and Operator Routing

- [x] 5.1 Create packaged `research/isomer-research-operation-set-recording` assets with a bounded workflow, manifest reference, command reference, recovery guidance, legacy repair guidance, and explicit prohibitions on inferred record or Research Idea lineage.
- [x] 5.2 Add the recording skill to the core system-skill manifest and catalog, set its `agents/openai.yaml` metadata version to `project.version`, and cover package discovery and materialization.
- [x] 5.3 Update `isomer-op-entrypoint` research and CLI indexes to route operation-set persistence, verification, and repair to the focused skill or explicit CLI family instead of generic Project lifecycle management.
- [x] 5.4 Extend packaged-skill and operator validators and tests for the new core inventory, required resources, workflow markers, version contract, routing coverage, and stale file-only acceptance guidance.

## 6. DeepSci Closeout Enforcement

- [x] 6.1 Add shared DeepSci Operation Set Closeout guidance that runs after end callbacks, distinguishes complete receipts from `not_applicable`, returns durable refs, preserves both lineage layers, and pauses with resumable diagnostics.
- [x] 6.2 Update every active non-shared production DeepSci workflow that can write material files with a numbered closeout step after end callbacks and before final response or handoff.
- [x] 6.3 Update `isomer-deepsci-pipeline` stage handoffs so plain paths are unavailable artifacts, complete receipts or explicit `not_applicable` closeouts are required, and durable record refs flow to the next stage.
- [x] 6.4 Update DeepSci pipeline terminal reports to list stage receipts and accepted refs, reconcile pipeline-level files, and pause rather than report `complete` when closeout fails.
- [x] 6.5 Extend the research-paradigm validation harness and fixtures to detect missing or misordered closeout steps, file-only terminal claims, absent receipt evidence, and pipeline progression from partial acceptance.

## 7. Documentation, Migration, and End-to-End Validation

- [x] 7.1 Document the manifest schema, inspect-preview-apply-verify workflow, managed attachment behavior, receipt statuses, recovery model, `not_applicable` rule, and the distinction between Git tracking, record lineage, and Research Idea lineage.
- [x] 7.2 Add a read-only legacy audit and optional repair walkthrough based on the shape of the Flash Attention 4 recovery chain, and update the known issue to distinguish the repaired historical data from the resolved systemic closeout gap when implementation is complete.
- [x] 7.3 Run focused unit and integration suites for Workspace Runtime, research records, Research Ideas, CLI, packaged skills, operator routing, and DeepSci validation.
- [x] 7.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, then fix all regressions caused by this change.
- [x] 7.5 Validate the OpenSpec change and perform an end-to-end exercise in a fresh temporary Topic Workspace proving that unclassified files block completion, accepted files appear in record and lineage queries, idea-bearing effects appear through the existing Idea Graph contract, and identical replay is non-duplicating; do not mutate the current Flash Attention 4 topic.
- [x] 7.6 Verify that the change introduces no canonical Research Idea schema, lifecycle, decision, lineage, CLI, or GUI-contract migration and that the baseline regression suite from task 1.1 remains green.
