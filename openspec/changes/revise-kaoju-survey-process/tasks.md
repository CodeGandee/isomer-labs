## 1. Resolve Supersession and Implementation Inputs

- [ ] 1.1 Add an implementation-facing supersession map that identifies the LaTeX-first requirements and incomplete tests from `add-kaoju-paper-writing` replaced by ADR-0006, while retaining compatible audit, citation, validation, build-provenance, and publication-quality behavior.
- [ ] 1.2 Record the final fourteen-skill inventory, ten survey-intent procedure ids, compatibility procedure ids, and grouped manager actions in one checked package contract used by manifests and validators.
- [ ] 1.3 Select a Python 3.11-compatible MyST parser and validation dependency, add it through Pixi project configuration, and record the locked dependency decision.
- [ ] 1.4 Complete license and provenance review for candidate LLM Wiki viewer code; record whether the implementation can bundle it or must use an independently implemented compatible viewer.
- [ ] 1.5 Capture baseline focused test results for Kaoju skill assets, artifact bindings, research records, template CLI, execution adapters, repository handling, and Workspace Runtime before changing behavior.

## 2. Build the Kaoju Binding Registry

- [ ] 2.1 Define the versioned machine-readable Kaoju binding registry schema with record kind, profile ref, semantic label, content mode, producer, consumers, relationships, revision mode, scope-key policy, latest-selection policy, and validation and acceptance fields.
- [ ] 2.2 Implement package-resource loading and deterministic diagnostics for the binding registry without embedding executable validators, providers, credentials, or command bodies.
- [ ] 2.3 Populate the registry for all existing active Kaoju semantic ids and mark legacy writing ids with explicit compatibility and migration dispositions.
- [ ] 2.4 Add bindings for every semantic id named by UC-01 through UC-10, including direction, reading, source, paper, wiki, environment, smoke, and trial artifacts.
- [ ] 2.5 Add or revise family-neutral Artifact Format Profiles, schemas, renderers, and validation hints for all new structured Kaoju artifacts.
- [ ] 2.6 Add content-mode validation for structured files, ordinary files, directory manifests, external paths, and canonical repository references.
- [ ] 2.7 Replace independent per-skill physical binding authorities with generated summaries or concise registry references while preserving storage-neutral semantics in `isomer-kaoju-shared`.
- [ ] 2.8 Update binding validation to compare semantics, registry entries, profiles, schemas, renderers, skill references, producers, consumers, content modes, and scope policies bidirectionally.
- [ ] 2.9 Replace exact legacy inventory assertions in `tests/unit/test_kaoju_artifact_bindings.py` with registry-derived coverage, compatibility, and invalid-fixture tests.

## 3. Extend Artifact Persistence and Scoped Queries

- [ ] 3.1 Add optional binding-defined `scope_key` metadata and indexes to Workspace Runtime research-record queries without changing the minimal Artifact Core Record contract.
- [ ] 3.2 Implement scoped current-candidate resolution for direction, source, paper line, and export target scopes with deterministic ambiguity reporting.
- [ ] 3.3 Add backward-compatible query behavior for unscoped legacy records and a migration helper that backfills scope only when it can be established unambiguously.
- [ ] 3.4 Implement ordinary-file Artifact registration with media type, checksum, size, locator posture, lineage, validation, and provenance links.
- [ ] 3.5 Implement versioned checksummed directory-manifest registration and validation for TeX trees, wiki exports, viewer deployments, generated-data directories, and other multi-file artifacts.
- [ ] 3.6 Implement authorized external-path and canonical-repository Artifact registration without copying, rewriting, or deleting externally owned content.
- [ ] 3.7 Add staged managed writes, atomic rename where supported, DB commit ordering, idempotency keys, and recovery diagnostics for failed file-and-record creation.
- [ ] 3.8 Add stale and corrupt locator detection that reports missing or checksum-mismatched content without directory-scan fallback.
- [ ] 3.9 Add integration tests for current-state revision, append-only events, immutable Runs, scoped conflicts, legacy ambiguity, recovery, and file-backed content authority.

## 4. Add Canonical Project Artifact and Run CLI Services

- [ ] 4.1 Implement a typed artifact service over the existing record store that resolves semantic bindings and exposes describe, put, revise, latest, list, show, and archive operations.
- [ ] 4.2 Register `isomer-cli project artifacts` and implement stable human output, JSON output, error codes, mutation status, affected refs, and recovery actions.
- [ ] 4.3 Make artifact put and revise infer record kind, profile, semantic label, content mode, scope policy, and revision behavior while validating producer authorization and relationship refs.
- [ ] 4.4 Implement `isomer-cli project runs begin`, `checkpoint`, `status`, and `complete` using Research Task and Run records stored through Workspace Runtime.
- [ ] 4.5 Record procedure id, control mode, inputs, expected outputs, stage id, completed refs, pending Gate, blocker and Service Request refs, terminal status, and resume hint in Run transitions.
- [ ] 4.6 Make supported `ext research records` operations delegate to the same underlying record and artifact services without changing existing compatible behavior.
- [ ] 4.7 Add unit and integration tests for artifact command inference, producer rejection, content modes, scoped queries, Run checkpoints, expected errors, and JSON contracts.

## 5. Add Repository Acquisition and Service Request CLI Services

- [ ] 5.1 Extend the canonical external repository service with verified remote acquisition, semantic-label target resolution, depth-one cloning, immutable commit capture, and post-clone validation.
- [ ] 5.2 Register `isomer-cli project repos acquire` with ambiguity, existing-target, authentication, clone-failure, recovery, optional history-deepening, and JSON result handling.
- [ ] 5.3 Ensure repository registration becomes visible only after successful acquisition and validation, with no half-created canonical registration after failure.
- [ ] 5.4 Define the generic Service Request record and links for supported scope, task, expected outputs, authorization, dispatch form, completion observations, Research Task, Run, command requests, actors, and provenance.
- [ ] 5.5 Implement `isomer-cli project service-requests create`, synchronous-only `dispatch`, and recovery `status` with deterministic lifecycle and support-artifact output; make dispatch wait for terminal completion or return a stable request ref plus timeout or interruption posture, and reject first-release no-wait operation explicitly.
- [ ] 5.6 Adapt the existing topic environment service skill to consume recorded Service Requests and return environment, gate, smoke script, smoke result, blocker, and provenance refs.
- [ ] 5.7 Route repository cloning, Pixi mutation, smoke runs, trials, document builds, and viewer launch through applicable Research Operation Extension Points and Execution Adapter Command Requests.
- [ ] 5.8 Add tests proving Service Requests remain distinct from Research Tasks and Workflow Stages and do not expose provider-specific or Houmao payloads in canonical records.

## 6. Refactor the Kaoju Skill Foundation

- [ ] 6.1 Scaffold `isomer-kaoju-trial` and `isomer-kaoju-export` with canonical identity, near-top workflows, agent metadata, direct resources, shared-contract references, and terminal behavior.
- [ ] 6.2 Refactor `isomer-kaoju-pipeline` into a thin router and add command pages for all ten survey-process intents with owners, inputs, stages, Gates, outputs, blockers, and resume points.
- [ ] 6.3 Preserve landscape, curated intake, direction expansion, theory comparison, method trial, comparative, audit survey, paper, template, survey manager, and dataset manager compatibility routes with explicit mapping to current owners.
- [ ] 6.4 Refactor `isomer-kaoju-shared` to teach binding-registry resolution, DB-only discovery, scope keys, file authority, directory manifests, audits, Gates, Service Requests, execution requests, and Run checkpoints.
- [ ] 6.5 Refactor `isomer-kaoju-workspace-mgr` to validate registry, profile, semantic label, scoped-query, content-mode, Run checkpoint, worker-output, and reset readiness.
- [ ] 6.6 Refactor every producer skill to call typed artifact operations rather than repeating complete record kind, label, profile, path, producer, and consumer command shapes.
- [ ] 6.7 Narrow `isomer-kaoju-reproduce` to genuine reproduction and make `method-trial-pass` route bounded trials and generated-data capability probes to `isomer-kaoju-trial`.
- [ ] 6.8 Update research-paradigm validation for the fourteen-skill inventory, approved commands, registry use, DB-only discovery, MyST-first writing, Service Request routing, adapter execution, and forbidden external wiki routing.
- [ ] 6.9 Regenerate or synchronize agent metadata and direct resources, then update exact valid and invalid Kaoju skill fixtures.

## 7. Implement Direction, Reading-List, and Deep-Ingestion Intents

- [ ] 7.1 Implement `choose-directions` in frame guidance with three proposals by default, stable direction fields, multi-selection, custom directions, rejection, revision, explicit human confirmation, and empirical-feasibility annotations that never filter solely by current host capability.
- [ ] 7.2 Add structured schema, profile, renderer, scoped revision, and tests for `kaoju:direction-set` while keeping it distinct from `kaoju:survey-contract`.
- [ ] 7.3 Implement `build-reading-list` with one scope per direction, three priority plus three secondary reachable targets, five source classes, papers and reports as primary works, version families, query provenance, blocker preservation, bounded backfill, and non-blocking shortage warnings.
- [ ] 7.4 Add structured schema, profile, renderer, scoped revision, inspection, refinement, approval, and tests for `kaoju:reading-list`.
- [ ] 7.5 Refactor discover guidance to record query text or seed, provider or access method, route, searched-through date, identity resolution, version family, disposition, and coverage limits in the discovery ledger.
- [ ] 7.6 Implement `ingest-reading-item` orchestration across acquire and examine, including artifact-library-first lookup, source-type acquisition, authorized online fallback, and explicit blockers.
- [ ] 7.7 Add `kaoju:artifact-library` and `kaoju:associated-source-code` schemas, profiles, relationships, current-state behavior, and integration with canonical repository refs.
- [ ] 7.8 Refactor source-digest and claim-evidence guidance for paper locators, claim-driven figure and table extraction, provisional visual evidence verification, immutable repository commit plus file and line locators, source statement versus interpretation, approval, and refinement.
- [ ] 7.9 Add UC-01, UC-02, and UC-03 integration fixtures covering custom and multiple directions, independent reading lists, short-list approval, version deduplication, local and online ingestion, associated code, blockers, audit prerequisites, and resume.

## 8. Implement Source-Code Ingestion, Environment Preparation, and Trials

- [ ] 8.1 Implement `ingest-source-code` resolution for URLs, names, paper refs, and reading-item refs with automatic bounded associated-paper metadata discovery, normal selection and approval before deep paper ingestion, relationship verification, ambiguity handling, and source-access blockers.
- [ ] 8.2 Route source acquisition through `project repos acquire` and record repository identity, immutable commit, depth posture, associated paper refs, artifact-library state, and provenance.
- [ ] 8.3 Refactor examine guidance so every code-level finding cites commit, repository ref, file, and line range and remains distinct from paper claims and executed behavior.
- [ ] 8.4 Implement `prepare-code-run` planning and the `kaoju:env-prep-plan` schema, profile, renderer, scope, dependencies, task-critical path, candidate environments, risks, authorization, and expected smoke outputs.
- [ ] 8.5 Implement Service Request dispatch for UC-09 and the Pixi preference order: reuse satisfying environment, add flexible compatible constraints to an existing environment while preferring `default`, or create a dedicated environment.
- [ ] 8.6 Record exact resolved package versions and lock identity in `kaoju:pixi-env-ref` while preserving flexible intent constraints and before-and-after gate state in `kaoju:env-gate-revision`.
- [ ] 8.7 Create durable file-backed `kaoju:smoke-run-script` and `kaoju:smoke-run-result` artifacts under resolved owner-preserved record surfaces, permit Run-tied staged execution copies, prevent source-tree or Local Tmp Surface copies from becoming canonical, and require a successful task-critical smoke observation before environment readiness.
- [ ] 8.8 Implement `run-code-trial` prerequisite resolution, `kaoju:method-trial-plan`, human Gate checkpoint, durable minimal wrapper, recorded use of a compatible upstream command or smallest necessary adaptation, and no-ambient-environment enforcement.
- [ ] 8.9 Execute approved trials through the adapter and record immutable `kaoju:method-trial-run` and `kaoju:method-trial-result` artifacts with source, environment, data, logs, outputs, timing, resources, adaptations, checks, verdict, depth, and limitations.
- [ ] 8.10 Implement the retry classifier and recorded attempt bound: permit identical transient retries automatically, require a revised plan and human Gate for material dependency, source, data, wrapper, evaluator, metric, resource, or interpretation changes, preserve every attempt as a separate Run, and prevent later results from overwriting earlier fidelity or verdict.
- [ ] 8.11 Reuse `kaoju:generated-dataset` for random-data trials and enforce `capability-probe` purpose and no stronger than executed verification depth.
- [ ] 8.12 Add UC-08, UC-09, and UC-10 integration fixtures covering ambiguous repos, inaccessible repos, shallow acquisition, environment reuse and creation, unsatisfiable dependencies, smoke failure and repair, Gate rejection, path data, random data, Run failure, and resume.

## 9. Replace the Paper Path with MyST-First Production

- [ ] 9.1 Add profiles, schemas, renderers, bindings, content modes, scopes, and lineage for all MyST, Markdown, template exchange, citation, revision, TeX, compile-log, and PDF semantic ids.
- [ ] 9.2 Refactor `isomer-kaoju-write` to require accepted audit and synthesis inputs, select and explain an adaptive typed structure profile from the accepted direction, create `kaoju:paper-structure-myst`, `kaoju:paper-draft-myst`, `kaoju:citation-map`, and `kaoju:paper-revision-log` as canonical paper state, and reference figures and tables as separate file-backed Artifacts through typed placeholders.
- [ ] 9.3 Implement MyST syntax, required-section, placeholder, citation-role, display, source-ref, and evidence-boundary validation with structured file-location diagnostics.
- [ ] 9.4 Register `isomer-cli ext kaoju paper export-template` with actor-selected or semantic-label-resolved targets, automatic export revisions, versioned managed directories, explicit update or overwrite policy for actor targets, base digest, source revision, paper line, tied draft, source refs, and export Artifact registration.
- [ ] 9.5 Register `apply-template` with manifest validation, optimistic concurrency, required-section and placeholder checks, orphaned grounded-content reporting and confirmation, canonical template revision, draft regeneration handoff, and no-mutation failure behavior.
- [ ] 9.6 Implement deterministic `derive-markdown` from MyST with source revision, checksum, unsupported-construct diagnostics, lineage, and non-canonical status.
- [ ] 9.7 Implement `init-tex` using the selected MyST parser to create TeX template and draft manifests, compatibility fingerprints over venue or document class, toolchain policy, and required constructs, stable template reuse, incompatible template revision, conversion diagnostics, citation inputs, included files, and lineage without claiming build readiness.
- [ ] 9.8 Add write-skill guidance and state for direct agent inspection and repair of TeX directives, tables, citations, floats, raw blocks, and venue structure.
- [ ] 9.9 Implement `build-pdf` through `document_build`, capture toolchain and fallback rationale, permit bounded automatic presentation-only and TeX-syntax repair after build authorization, require a revised plan and Gate for material repairs, create distinct build Runs and compile logs, inspect PDF output, and apply publication Gate policy.
- [ ] 9.10 Keep legacy writing and manuscript records readable, prevent automatic TeX-to-MyST promotion, and support actor-authorized registration of legacy TeX only as derived TeX artifacts with provenance.
- [ ] 9.11 Deprecate new canonical creation through `ext research templates`, preserve supported historical inspection and repair, and return migration guidance to `ext kaoju paper`.
- [ ] 9.12 Update `paper-pass` as a compatibility composition of draft and optional PDF stages and update `create-paper-template` to produce canonical MyST templates.
- [ ] 9.13 Add UC-04, UC-05, and UC-06 integration fixtures for missing audits, supported and contradicted claims, derived Markdown, external template editing, stale-base conflicts, invalid placeholders, TeX repair diagnostics, build fallback, PDF validation, Gate rejection, lineage, and resume.

## 10. Implement Self-Contained LLM Wiki Export and Viewer

- [ ] 10.1 Define and validate versioned wiki export and viewer manifest schemas with topic, artifact, revision, checksum, page, relationship, provenance, target, version, and launch metadata.
- [ ] 10.2 Implement accepted-artifact selection through state-DB queries with explicit subset, direction, and paper scopes and deterministic ambiguity and stale-content handling.
- [ ] 10.3 Implement an idempotent Markdown page and canonical JSON mapping exporter with a Topic Workspace default and actor-path override, staged in-place updates of recognized managed files, unrecognized-file preservation, and a created, changed, unchanged, stale, and removed path changelog.
- [ ] 10.4 Register wiki output directories through checksummed manifests as `kaoju:llm-wiki-export` and `kaoju:llm-wiki-metadata`.
- [ ] 10.5 Package the licensed or independently implemented compatible viewer and validate it from installed package resources without an external skill checkout.
- [ ] 10.6 Implement viewer deployment to a resolved Topic Workspace default or actor-selected directory with recognized-target in-place refresh, unrecognized-target clarification, checksums, wiki target validation, JSON manifest output, and `kaoju:llm-wiki-viewer` and `kaoju:llm-wiki-viewer-manifest` registration.
- [ ] 10.7 Implement viewer start through command execution with loopback default, port conflict handling, optional network-exposure Gate, Run and log recording, and local URL output.
- [ ] 10.8 Refactor `isomer-kaoju-export` to select accepted records, invoke only `isomer-cli ext kaoju wiki`, report created and stale pages, and never invoke the external `imsight-llm-wiki` skill.
- [ ] 10.9 Add UC-07 integration fixtures for subset and default-path export, path overrides, canonical JSON metadata, provenance mapping, idempotent in-place update, changelog output, protected human files, installed-package operation, viewer deployment and refresh, stale wiki targets, port conflict, local launch, and forbidden external skill routing.

## 11. Update Packaging, Documentation, and Compatibility

- [ ] 11.1 Update the packaged Kaoju manifest to the fourteen-skill inventory, keep `isomer-kaoju-pipeline` as entry skill, and declare all ten survey intents plus retained compatibility commands in deterministic order.
- [ ] 11.2 Update callback insertion points, extension discovery metadata, materialization tests, installer selectors, and generated asset inventories for the new trial and export skills.
- [ ] 11.3 Update Kaoju and system-skill documentation with the user-intent surface, capability ownership, MyST graph, state-DB discovery rule, Service Request boundary, CLI groups, and migration notices.
- [ ] 11.4 Update CLI help and public documentation for project artifacts, Runs, repository acquisition, Service Requests, Kaoju paper, Kaoju wiki, and legacy command deprecations.
- [ ] 11.5 Document that Houmao remains an adapter and Service Dispatch Form implementation detail and verify no new Kaoju schema, CLI label, or skill instruction promotes Houmao terminology.
- [ ] 11.6 Document reset-checkpoint treatment for selected directions, reading lists, source digests, paper state, wiki manifests, environment refs, and trial results.

## 12. Verify the Complete Survey Process

- [ ] 12.1 Add a contract test that extracts every durable semantic id from the ten use cases and proves that it resolves to one valid binding, profile or explicit non-structured disposition, producer, consumer set, and content mode.
- [ ] 12.2 Add cross-cutting tests proving every accepted durable output has a state-DB entry and valid content link and that skills never use directory scanning as a fallback.
- [ ] 12.3 Add cross-cutting tests for clarification-first behavior, custom and multiple selections, human Gates, Service Requests, Run checkpoints, paused and blocked terminal reports, and resumption from the first incomplete stage.
- [ ] 12.4 Add cross-cutting tests for source identity and version families, exact claim locators, audit-before-synthesis, contradictions, failed Runs, repairs, limitations, and calibrated coverage language.
- [ ] 12.5 Add compatibility tests for existing pipeline procedures, legacy writing records, `ext research records`, `ext research templates`, existing DeepSci behavior, and installation without a repository checkout.
- [ ] 12.6 Run focused Kaoju, record, query-index, path-resolution, repository, service, execution-adapter, paper, wiki, packaging, installer, and CLI unit and integration tests and resolve all introduced failures.
- [ ] 12.7 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`; record unrelated pre-existing failures separately.
- [ ] 12.8 Run `openspec validate revise-kaoju-survey-process --strict` and verify every requirement scenario maps to implementation or test evidence before requesting archive.
