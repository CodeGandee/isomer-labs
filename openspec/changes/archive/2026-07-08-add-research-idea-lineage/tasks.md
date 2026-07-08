## 1. Domain and Schema

- [x] 1.1 Update `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` with Research Idea, Primary Idea, Idea Realization, and Idea Lineage Edge definitions.
- [x] 1.2 Add runtime dataclasses/constants for Research Idea, Idea Realization, Idea Lineage Edge, and Idea Generation Group.
- [x] 1.3 Add SQLite schema and migrations for `research_ideas`, `research_idea_realizations`, `research_idea_lineage_edges`, and `research_idea_generation_groups`.
- [x] 1.4 Add runtime store upsert/list/get helpers for the new idea tables.
- [x] 1.5 Add runtime validation for missing refs, cross-topic refs, duplicate semantic idea ids, invalid status/visibility/kind values, cycles, rejected idea-level `revision_of` edges, and generation-group consistency.

## 2. Recording APIs and CLI

- [x] 2.1 Add `isomer-cli ext research ideas upsert` with deterministic JSON output and validation diagnostics.
- [x] 2.2 Add `isomer-cli ext research ideas realize` for linking ideas to durable records and source JSON paths.
- [x] 2.3 Add `isomer-cli ext research ideas lineage add` and `generation upsert` for idea DAG and sibling candidate maintenance.
- [x] 2.4 Add `isomer-cli ext research ideas query`, `graph`, `validate`, `import-from-record`, and `repair`.
- [x] 2.5 Extend structured record create/update requests with accepted idea realization and idea parent metadata fields that route through the canonical idea store.
- [x] 2.6 Add unit tests for CLI success, validation failure, preview/apply repair behavior, and read-only query behavior.

## 3. Query Index and Graph API

- [x] 3.1 Extend query-index schema/export payloads with canonical ideas, idea realizations, idea lineage edges, and idea generation groups.
- [x] 3.2 Keep extracted `research_record_ideas` facets queryable while marking them as legacy/fallback when canonical idea rows exist.
- [x] 3.3 Update index rebuild/validation so canonical idea export rows are derived from Workspace Runtime idea tables and not Markdown prose.
- [x] 3.4 Update backend `idea-lineage` graph projection to prefer canonical primary ideas and canonical idea edges.
- [x] 3.5 Add backend diagnostics for heuristic fallback, duplicate extracted facets, missing canonical idea data, stale suggested idea status, and ambiguous legacy projection.
- [x] 3.6 Add query-index and graph API tests for canonical primary graph, expanded supporting material, and legacy fallback.

## 4. Project Web GUI

- [x] 4.1 Update TypeScript graph types to accept canonical idea nodes, idea realization refs, idea lineage edges, and idea generation groups.
- [x] 4.2 Update the default idea-lineage graph to render canonical primary ideas and links when available.
- [x] 4.3 Add idea detail tab behavior that opens latest realization, realization history, linked records, incoming/outgoing idea edges, and sibling group metadata.
- [x] 4.4 Preserve secondary material expansion without showing route decisions, claims, and raw details as default primary ideas.
- [x] 4.5 Add frontend tests or Playwright checks for linked primary ideas, detail tab opening, fallback diagnostics, and browser-size behavior.

## 5. DeepSci Skill Guidance

- [x] 5.1 Add shared Research Idea Recording guidance beside Artifact Lineage Recording.
- [x] 5.2 Update `isomer-deepsci-idea` workflow and references to record raw ideas, candidate frontiers, pre-idea drafts, selected hypotheses, selected idea drafts, rejected/deferred ideas, and route decisions with canonical idea identity and lineage.
- [x] 5.3 Update `isomer-deepsci-experiment` guidance so result evidence may suggest stale idea status, but only an explicit accepted idea write updates idea status or creates follow-up ideas.
- [x] 5.4 Update `isomer-deepsci-analysis` guidance to update existing Research Ideas in place for record revisions, and to record follow-ups, splits, merges, and returns to ideation as explicit idea relationships when they introduce a new research direction.
- [x] 5.5 Update `isomer-deepsci-decision` and related placeholder bindings so idea selection, rejection, deferral, sibling generation groups, and collapse rationale are durable.
- [x] 5.6 Update DeepSci idea guidance so candidate collapse records explicit `subsumes` idea lineage edges when one candidate covers another as an ablation, mechanism subset, or test role.
- [x] 5.7 Extend skill validation so active DeepSci guidance cannot rely on Markdown prose or record-lineage projection as authoritative idea lineage.

## 6. Existing Topic Repair

- [x] 6.1 Inspect `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` records and produce a repair plan for raw time-parent ideas, candidate branch ideas, later primary ideas, supporting details, realizations, edges, generation groups, and inferred confidence metadata.
- [x] 6.2 Apply canonical idea rows for primary raw time-parent ideas R1-R8 and primary branch/follow-up ideas C1, C2, C3, real-hardware validation, launch-overhead/NCU calibration, bottleneck-threshold calibration, and bottleneck saturation predictability.
- [x] 6.3 Use semantic topic-scoped canonical `idea_id` values in the repaired topic and preserve `R1` through `R8` and `C1` through `C3` as source aliases.
- [x] 6.4 Link each idea to the best available realization records and source JSON paths, including legacy Markdown-only selected hypothesis material.
- [x] 6.5 Add best-guessed idea lineage edges and generation-group metadata with repair rationale.
- [x] 6.6 Run idea validation and query-index rebuild/validation for the repaired topic.

## 7. Documentation and Validation

- [x] 7.1 Update relevant docs or context notes describing the distinction between record lineage and idea lineage.
- [x] 7.2 Add or update tests for runtime schema reopening, store APIs, CLI output shape, query-index export, graph projection, and repaired fixture data.
- [x] 7.3 Run `pixi run lint`.
- [x] 7.4 Run `pixi run typecheck`.
- [x] 7.5 Run `pixi run test`.
- [x] 7.6 Run a targeted project web GUI smoke check for the flash-attention idea-lineage view.
