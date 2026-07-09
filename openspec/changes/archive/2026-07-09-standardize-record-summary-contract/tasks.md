## 1. Schemas and Format Assets

- [x] 1.1 Add `structured-record.v2` JSON schemas so accepted DeepSci payload roots require non-empty `title` and `summary`, and mark v1 usage unsupported for new writes.
- [x] 1.2 Update idea-bearing DeepSci schemas or profile-specific validation so accepted idea entries require non-empty `title` and `summary`.
- [x] 1.3 Update active DeepSci profile refs and shipped Jinja2 templates to use v2 and render `summary` as the brief display description.
- [x] 1.4 Add schema and renderer tests that cover valid v2 `title`/`summary`, missing `summary`, empty `summary`, unsupported v1 writes, and stale `one_liner`-only payloads.

## 2. Runtime Models and Persistence

- [x] 2.1 Replace `ResearchIdea.one_liner` with `ResearchIdea.summary` in runtime dataclasses, Python contract models, serializers, and row mappers.
- [x] 2.2 Add clean Workspace Runtime SQLite migration logic that rewrites affected idea and idea facet tables to canonical `summary` columns while preserving existing `display_key` uniqueness.
- [x] 2.3 Update record store create/update/import/repair paths to require `title` and `summary` for structured payloads and canonical Research Ideas.
- [x] 2.4 Limit legacy `one_liner` reads to migration, validation, or repair code, and remove normal read-time conversion from GUI/API/CLI paths.
- [x] 2.5 Add validation diagnostics and process-local recent-error reporting for missing display fields, duplicate `title`/`summary`, legacy-only display aliases, and non-interpretable idea data.

## 3. CLI and Query Index

- [x] 3.1 Update research record and research idea CLI inputs and JSON outputs to use `summary` instead of `one_liner`.
- [x] 3.2 Update query-index extraction so record rows and idea facets store `summary` from payload roots and idea-bearing entries.
- [x] 3.3 Update query list, export, lineage, facets, graph, and timeline response builders so they expose `summary` and do not expose `one_liner` as a first-class or generic subtitle display field.
- [x] 3.4 Add query-index rebuild and validation tests for missing summaries, stale legacy fields, duplicated display fields, and non-crashing partial exports.

## 4. Project Web GUI Contracts

- [x] 4.1 Update Project Web backend graph, timeline, hover, detail, and record read models to expose `summary` across graph node material kinds and canonical idea `display_key`, parent refs, visibility, and diagnostics.
- [x] 4.2 Update documented UI contracts under `docs/ui/contracts/` and generated or hand-maintained TypeScript types to remove `one_liner` and replace it with `summary`.
- [x] 4.3 Update idea graph and timeline components so display text and fuzzy search use `summary` and all other intended searchable table/node fields.
- [x] 4.4 Add or update GUI contract tests for graph nodes, timeline rows, hover previews, idea details, missing-summary diagnostics, and extra-field tolerance.

## 5. DeepSci Skill Guidance

- [x] 5.1 Update active production DeepSci `placeholder-bindings.md` pages so structured payload guidance uses supported v2 profiles and requires top-level `title` and `summary`.
- [x] 5.2 Update idea-producing placeholder bindings so each idea-bearing entry requires `title` and `summary` and treats labels or candidate ids as aliases.
- [x] 5.3 Update active production DeepSci shared and stage skill guidance to teach supported v2 payloads, `summary`, and remove active `one_liner` authoring instructions.
- [x] 5.4 Extend `scripts/validate_research_paradigm_skillset.py` and related tests to report missing display-field guidance, stale active `one_liner` guidance, and stale v1 new-write guidance.

## 6. Flash-attention Topic Migration

- [x] 6.1 After code-level support lands, create a backup or restorable snapshot of `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model`.
- [x] 6.2 Scan all managed payload JSON files and fix stored payload roots and idea-bearing entries with meaningful authored `summary` values so no GUI/runtime conversion is needed.
- [x] 6.3 Migrate `state.sqlite` canonical idea rows, structured payload cache/index rows, and idea facet rows to clean `summary` columns while preserving existing display keys and lineage refs.
- [x] 6.4 Rebuild the query index for the migrated topic workspace and run idea validation, record validation, source-fragment validation, and recent-error inspection.
- [x] 6.5 Manually smoke-check the migrated GUI graph, timeline, hover, and detail views to confirm display labels and summaries come from stored data.

## 7. Verification

- [x] 7.1 Run targeted unit tests for schemas, record store, SQLite migration, query-index extraction, Project Web contracts, and skill validation.
- [x] 7.2 Run `pixi run lint`.
- [x] 7.3 Run `pixi run typecheck`.
- [x] 7.4 Run `pixi run test`.
- [x] 7.5 Run `openspec validate standardize-record-summary-contract --strict` or the repository-equivalent OpenSpec validation command and confirm the change is apply-ready.
