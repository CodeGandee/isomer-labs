## 1. Source Fragment Resolver

- [x] 1.1 Move the current web-only JSON path extraction helper into shared research record or idea code with unit coverage for the supported subset `$`, `$.field`, nested dot paths, numeric list indexes such as `$.sections.raw_ideas[0]`, missing keys, root paths, and non-object results.
- [x] 1.2 Add shared diagnostics for missing structured payload, unreadable payload file, digest mismatch, unresolved source path, broad source path, and non-object source fragment.
- [x] 1.3 Add one shared Python source-fragment registry, for example `src/isomer_labs/records/idea_sources.py`, with profile-aware idea-bearing section mappings for DeepSci raw idea slate, candidate idea frontier, rejected/deferred ideas, pre-idea draft, selected hypothesis, selected idea draft, route decision, and paper-facing idea seed profiles.

## 2. CLI and Runtime Idea Contract

- [x] 2.1 Tighten `ResearchIdeaRealization` validation so latest Primary Idea realizations with structured source records require exact object-valued source paths, with errors for latest Primary Idea violations and warnings for historical or supporting realization source issues.
- [x] 2.2 Update `isomer-cli ext research ideas realize` and record-create idea convenience metadata to reject payload roots, collection paths, generated Markdown paths, and context-only note paths for Primary Idea preview sources.
- [x] 2.3 Update `isomer-cli ext research ideas validate` to report missing source records, missing payloads, unresolved paths, broad paths, non-object fragments, alias/id mismatches, stale latest flags, and duplicate latest realizations.
- [x] 2.4 Update `isomer-cli ext research ideas import-from-record` to use profile-aware mappings and emit exact item paths such as `$.sections.raw_ideas[0]`.
- [x] 2.5 Update `isomer-cli ext research ideas repair` to return a deterministic preview plan and an apply mode for source path, alias, latest-flag, realization, lineage, and generation repairs, with managed payload-file edits behind an explicit option such as `--update-payloads`.
- [x] 2.6 Add unit tests for realize, validate, import, and repair paths using raw idea slate and candidate frontier payload fixtures.

## 3. Query Index and API Read Models

- [x] 3.1 Update query-index rebuild/export to include idea source fragment status, source classification, source record id, source JSON path, payload digest, and source diagnostics for canonical ideas and realizations, using `exact`, `missing_payload`, `missing_path`, `unresolved_path`, `broad_path`, `non_object`, and `legacy_fallback` status values.
- [x] 3.2 Update facet extraction so declared idea-bearing sections create idea facets while context sections such as filter notes and route notes do not become Primary Idea nodes.
- [x] 3.3 Update the idea-lineage graph backend so Primary Idea nodes open idea detail refs by default and keep source record refs as provenance refs.
- [x] 3.4 Update the FastAPI idea detail payload so `idea_content` is exact idea content or canonical idea metadata with diagnostics, `source_provenance` carries source-record refs and payload metadata, and the legacy `source` object remains compatibility metadata for one release.
- [x] 3.5 Add backend tests for source-fragment success, unresolved-path metadata fallback, full-payload fallback rejection, and source-record provenance refs.

## 4. GUI Idea Detail

- [x] 4.1 Update frontend types and API handling for the new idea content/source provenance fields.
- [x] 4.2 Update `IdeaDetailPanel` so the main Markdown preview renders the true idea content and shows source kind, source path, diagnostics, and source-record provenance separately.
- [x] 4.3 Rename or present the source artifact action as `Open Source Record`, keep it wired to the source artifact record, and place it in a provenance/context area rather than beside idea copy actions.
- [x] 4.4 Update copy Markdown, copy JSON, JSON modal, refresh, and source-truncation behavior to operate on the focused idea content object.
- [x] 4.5 Add frontend unit tests and a Playwright smoke test proving filter notes do not appear in the main preview for a Primary Idea whose source record is a raw idea slate.

## 5. DeepSci Skills and Binding Guidance

- [x] 5.1 Update `isomer-deepsci-shared/references/research-idea-recording.md` to define exact object-valued source paths, idea content versus source-record context, and invalid broad paths.
- [x] 5.2 Update `isomer-deepsci-idea` workflow and reference routing so raw slates, frontiers, drafts, selections, decisions, and paper seeds record exact Idea Realization paths.
- [x] 5.3 Update relevant downstream DeepSci skills so experiment, analysis, optimize, decision, write, review, rebuttal, and finalize flows update existing ideas or create true follow-up ideas with explicit lineage.
- [x] 5.4 Update DeepSci `placeholder-bindings.md` pages for idea-producing placeholders to name idea-bearing sections, context sections, and exact source path patterns.
- [x] 5.5 Update packaged system-skill mirrors under `src/isomer_labs/assets/system_skills/` to match repository skill guidance.
- [x] 5.6 Extend skill and placeholder-binding validation tests to catch missing idea source guidance and broad-path guidance.

## 6. Flash-attention Topic Migration

- [x] 6.1 Inspect all canonical Research Ideas, Idea Realizations, idea lineage edges, generation groups, and managed payloads in `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model`.
- [x] 6.2 Use the explicit payload-update repair path or fixture migration path to enrich idea-bearing payload entries with canonical `idea_id`, source label, title or one-liner, status, visibility, family, concise rationale where available, and repair metadata.
- [x] 6.3 Update runtime Research Idea rows and Idea Realizations so every Primary Idea source path resolves to an exact payload object and each visible idea has coherent latest realization flags.
- [x] 6.4 Preserve raw slate, candidate frontier, rejected/deferred, route-decision, experiment, analysis, and paper records as source artifacts and provenance rather than deleting or flattening them, and leave uncertain historical/supporting rows visible with diagnostics rather than invented content.
- [x] 6.5 Rebuild and validate the topic query index after the migration.

## 7. Verification

- [x] 7.1 Run `openspec validate fix-primary-idea-source-contract --strict`.
- [x] 7.2 Run `pixi run lint`.
- [x] 7.3 Run `pixi run typecheck`.
- [x] 7.4 Run `pixi run test`.
- [x] 7.5 Run frontend tests and build under `web/ui`.
- [x] 7.6 Run targeted CLI validation for the flash-attention topic with `ext research ideas validate` and query-index validate/export checks.
- [x] 7.7 Restart the GUI service and manually or Playwright-check an idea detail URL to confirm the main panel shows only the true idea content while `Open Source Record` shows source artifact context.
