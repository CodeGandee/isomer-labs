## 1. Family-Neutral Artifact Format Provider

- [x] 1.1 Add the `isomer.research.record-formats` provider module, family-neutral ref parser, provider registration helper, and packaged asset layout without changing the DeepSci provider API.
- [x] 1.2 Add the `research-structured-record.v1` JSON Schema and Markdown template with required display, family, semantic-id, artifact-type, and sections fields.
- [x] 1.3 Implement declarative built-in family catalog loading with family, semantic id, class, compatible record kinds, required paths, relationship paths, file paths, facet paths, renderer, version, and status validation.
- [x] 1.4 Implement deterministic duplicate-ref, family-mismatch, semantic-id-mismatch, missing-asset, and unsupported-version diagnostics for neutral provider registration and resolution.
- [x] 1.5 Register the neutral provider everywhere built-in Artifact Format providers are resolved for validation, rendering, research-record writes, runtime validation, reset inspection, and CLI commands.
- [x] 1.6 Add provider unit tests for ref parsing, catalog resolution, common and required-path validation, Markdown rendering, collision diagnostics, missing profiles, and packaged asset discovery.
- [x] 1.7 Add compatibility tests proving every current DeepSci catalog profile, schema, template, validation result, and public ref still resolves through the existing provider without aliasing.

## 2. Family-Neutral Semantic Record Identity

- [x] 2.1 Add optional `semantic_id` to research record request, stored metadata, structured payload metadata, response models, and revision inheritance while preserving the original placeholder field.
- [x] 2.2 Add `--semantic-id` to create, update, revise, list, and applicable query CLI paths with exact `<family>:<semantic-id>` validation and payload/profile consistency checks.
- [x] 2.3 Preserve existing `--placeholder` command behavior, responses, stored metadata, and filters, and mark any compatibility-derived generalized identity as derived rather than authored.
- [x] 2.4 Extend the query-index schema and rebuild path with artifact family, authored or derived semantic id, semantic-id source, artifact type, procedure, and terminal-status fields.
- [x] 2.5 Add composable `--artifact-family`, exact `--semantic-id`, procedure, and `--latest-only` query filters with explicit revision and supersession precedence plus ambiguity diagnostics.
- [x] 2.6 Extend profile-driven index extraction to consume declarative relationship, file, claim, metric, catalog, source, evidence, procedure, and terminal-status paths without Kaoju-specific Python branches.
- [x] 2.7 Add record-store and CLI tests for semantic-id create, show, list, update, revise, archive, payload mismatch, profile mismatch, topic scoping, placeholder compatibility, and deterministic JSON output.
- [x] 2.8 Add query-index migration, rebuild, filter, latest-state, ambiguity, unknown-profile, facet-provenance, file, lineage, and export tests for both Kaoju-style and existing DeepSci records.

## 3. Kaoju Artifact Semantics and Profiles

- [x] 3.1 Add the storage-neutral Kaoju artifact semantic registry with exact `kaoju:<semantic-id>` entries, meanings, required semantic content, producers, consumers, update intent, and the complete core durable object inventory.
- [x] 3.2 Add the declarative Kaoju neutral-profile catalog with one exact `isomer:research/record-format/profile/kaoju/<class>/<semantic-id>/v1` entry per structured binding.
- [x] 3.3 Define and fixture each Kaoju profile's compatible record kind, required payload paths, relationship paths, file paths, query facets, and renderer behavior.
- [x] 3.4 Define shared Kaoju payload authoring guidance for canonical managed JSON, required top-level fields, validation, actor metadata, lineage, revisions, on-demand rendering, explicit exports, and structured diagnostics.
- [x] 3.5 Define the large-material boundary for papers, repositories, datasets, models, checkpoints, generated data, raw outputs, and logs, including immutable locator, revision or digest, access, license, staleness, managed-link, file, and provenance refs.

## 4. Kaoju Per-Skill Artifact Bindings

- [x] 4.1 Add `artifact-bindings.md` to each Kaoju producer skill and map exact semantic ids to storage item, record kind, existing semantic label, neutral profile, producer, consumer, payload role, lineage, revision, query metadata, and normal create command.
- [x] 4.2 Add binding-page lifecycle patterns for validate, create, exact list, show with payload, metadata-only update, content revision, follow-up child creation, on-demand render, explicit export, and archive.
- [x] 4.3 Bind workspace readiness, binding index, Survey Contract, Comparison Intent Document, Proceed Decision, terminal reports, and other control or contract records.
- [x] 4.4 Bind discovery, catalogs and deltas, curated intake, Source Digests and blockers, Claim-Evidence Ledger, comparisons, audits, claim status, summaries, and the Kaoju Dossier.
- [x] 4.5 Bind material acquisition, Topic Dataset Manifest, Generated Dataset, Method Trial, method-trial Runs, comparison Runs, raw-output file refs, and repaired or adapted Run lineage without embedding material bytes.
- [x] 4.6 Update active Kaoju stage and pipeline guidance to cite registered semantic ids, read local binding authority before accepted writes, and return a storage blocker rather than inventing paths, profiles, direct Markdown state, or untracked JSON.
- [x] 4.7 Update `isomer-kaoju-shared` with latest-context preflight, worker output policy, canonical payload and derived-view rules, lineage and revision discipline, material boundaries, and binding reference routing.

## 5. Kaoju Workspace and Manager Behavior

- [x] 5.1 Extend `isomer-kaoju-workspace-mgr` to validate Effective Topic Context, fresh Workspace Runtime state, record labels, neutral provider profiles, semantic registry, selected binding pages, query filters, actor posture, worker output policy, and dataset-manifest posture.
- [x] 5.2 Add a topic-level Kaoju binding index and bound Workspace Readiness or blocker records, with selected-skill coverage, binding status, exact profile refs, labels, and next allowed stage.
- [x] 5.3 Add reset-checkpoint handling for Kaoju bootstrap records and explicitly user-selected survey state while reporting ordinary unpreserved records as subject to the accepted reset plan.
- [x] 5.4 Update `manage-survey list`, `show`, `status`, and `export` to use exact family, semantic-id, record-id, latest, payload, lineage, render, and export queries without mutating canonical state.
- [x] 5.5 Update `manage-dataset register`, `list`, `show`, `refresh`, and `remove` to query or revise `kaoju:topic-dataset-manifest`, consume Topic Workspace owner results, preserve prior revisions, and never mutate the external target.
- [x] 5.6 Add skill-contract tests for bootstrap blockers, bound-write routing, current versus historical survey state, ambiguous latest records, derived export behavior, dataset-manifest reuse, and owner-routed mutations.

## 6. Family-Aware Binding Validation

- [x] 6.1 Extend research-paradigm family configuration with semantic registry path, semantic-id pattern, binding filename, neutral profile namespace, binding owners, and required binding fields while leaving DeepSci configuration intact.
- [x] 6.2 Implement bidirectional semantic-registry, active-skill, binding-row, and profile-catalog coverage checks with deterministic file and line diagnostics.
- [x] 6.3 Reject physical binding fields in the storage-neutral semantic registry and conflicting record kinds, labels, profiles, or normal command shapes in active stage prose.
- [x] 6.4 Validate Kaoju payload-first commands, `--semantic-id`, global CLI spelling, actor metadata hooks, display fields, lineage and revision guidance, query metadata, lifecycle operations, and absence of canonical Markdown authoring.
- [x] 6.5 Add invalid fixtures for missing, extra, duplicate, cross-family, unresolved, mismatched, direct-body, stale-profile, missing-lifecycle, missing-lineage, missing-facet, and premature-physical-binding cases.
- [x] 6.6 Run the complete existing DeepSci validator suite and preserve all current inventory, placeholder, payload, display, latest-context, lineage, query-metadata, and profile diagnostics unchanged in meaning.

## 7. Documentation and Integration Tests

- [x] 7.1 Update Artifact Format, research-record, query-index, reset, packaged-skill, research-paradigm, and CLI documentation for neutral refs, semantic ids, canonical payloads, derived views, Kaoju bindings, material manifests, and DeepSci compatibility.
- [x] 7.2 Add package-asset and installer tests proving the Kaoju semantic registry and binding pages materialize with the extension and neutral provider assets ship in the Python package.
- [x] 7.3 Add integration tests that create, revise, query, status, render, export, index, rebuild, and reset bound Kaoju records in a temporary Topic Workspace.
- [x] 7.4 Add Project Web and read-API regression tests showing neutral Kaoju records expose generic title, summary, payload, lineage, file, facet, and validation metadata without a Kaoju-specific GUI backend.

## 8. Verification and Handoff

- [x] 8.1 Run strict OpenSpec validation and the research-paradigm validator against the packaged DeepSci and Kaoju roots.
- [x] 8.2 Run targeted Artifact Format provider, research-record CLI, query-index, lineage, reset, Kaoju binding, system-skill asset, installer, and Project Web unit and integration tests.
- [x] 8.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` from the repository root.
- [x] 8.4 Perform a temporary-Topic smoke test that bootstraps Kaoju bindings, creates and revises a Survey Contract and Related-Work Catalog, lists latest survey state, renders an explicit view, and verifies historical lineage.
- [x] 8.5 Verify all existing DeepSci profile refs and placeholder-backed workflows remain unchanged, then record final provider, binding, query, reset, package, and compatibility evidence in the change handoff.
