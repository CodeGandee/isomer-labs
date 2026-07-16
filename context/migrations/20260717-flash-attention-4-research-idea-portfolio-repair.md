# Flash Attention 4 Research Idea Portfolio Repair

Date: 2026-07-17

Topic Workspace: `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model`

## Problem

The Workspace Runtime contains one canonical Research Idea, `sass-grounded-interpretable-model`, although the accepted DeepSci operation set proposed four raw ideas, retained one serious candidate, selected one hypothesis, recorded two explicit rejections, and later developed a SASS-grounded follow-up. The missing concepts make Idea Graph and Idea Timeline answer portfolio questions incorrectly.

## Preview Evidence

`ideas import-from-record` was run without `--apply` against `artifact-DEEPSCI-RAW-IDEA-SLATE-2aea71980e49` and returned four exact proposal objects at `$.sections.raw_ideas[0..3]` with `mutated: false`. The same preview against `artifact-DEEPSCI-CANDIDATE-IDEA-FRONTIER-be48d49e27b6` returned the serious stage-pipeline candidate at `$.sections.serious_candidates[0]` with `mutated: false`.

`ideas migrate-status` was run without `--apply` and returned one proposed migration for `sass-grounded-interpretable-model`: preserve selected decision meaning while leaving exploration and evidence unknown. `ideas validate` reported that same missing classification plus the known missing structured payload for its manually imported Research Note realization.

The generic import preview was not applied because its legacy title-based IDs preserve case and would split the raw `Stage-pipeline predictor` from the lower-case candidate ID. This plan assigns stable concept IDs explicitly and keeps multiple expressions as Idea Realizations of the same concept.

## Reviewed Canonical Plan

| Idea ID | Source meaning | Exploration | Decision | Evidence | Decision reason |
| --- | --- | --- | --- | --- | --- |
| `pure-roofline-predictor` | Raw proposal, later rejected because it cannot identify SFU and synchronization bottlenecks | `unexplored` | `closed` | `unknown` | Rejection recorded at `$.sections.rejected[1]`; closure reason `rejection` |
| `stage-pipeline-predictor` | Raw proposal, serious candidate, and selected hypothesis | `explored` | `selected` | `supported` | Selected hypothesis and subsequent experiment, validation, and analysis records |
| `probabilistic-occupancy-predictor` | Raw proposal with no later recorded disposition | `unexplored` | `unknown` | `unknown` | No disposition or rationale will be invented |
| `sass-critical-path-predictor` | Raw proposal, later set aside because it was too heavy for that pass | `unexplored` | `deferred` | `unknown` | Deferral recorded at `$.sections.rejected[0]`; the wording supports later reconsideration rather than permanent closure |
| `sass-grounded-interpretable-model` | Later SASS-grounded model with microbenchmark and predictor-validation records | `explored` | `selected` | `supported` | Existing selected concept, supported by the 12.774× predictor-validation result and implementation artifacts |

The raw slate becomes generation `flash-attention-4-raw-idea-slate`. The existing `decision_record-DEEPSCI-IDEA-ROUTE-DECISION-1a182e0154c5` receives explicit option membership for the four ideas that the operation set considered: selected stage pipeline, closed pure roofline, deferred SASS critical path, and considered probabilistic occupancy. Missing rationale for the probabilistic option remains explicit.

The stage-pipeline concept receives realizations from the raw slate, candidate frontier, and selected-hypothesis object. Rejection objects become non-latest disposition realizations for the affected concepts. The existing SASS-grounded concept keeps its Research Note as the latest realization and receives the raw SASS proposal as an earlier realization.

Two idea-level edges are justified by durable record lineage and the imported operation-set lineage: stage pipeline `derived_from` to SASS-grounded, and SASS critical path `follow_up_to` SASS-grounded. No edge is created among the other raw alternatives.

## Apply and Verification Policy

Create a backup of `state.sqlite`, apply the existing status migration, write the reviewed ideas and exact realizations, record the generation, Decision Record options, transitions, and two justified lineage edges, then run `ideas validate`, all fixed Project Web presets, decision context, bounded ancestry and descendant traversal, and graph/timeline read-model checks. Stop if any preview, expected-state transition, exact-path validation, or topic-boundary check fails.

The topic database is generated local content and remains ignored by Git. This repair note is the durable review artifact for the applied local migration.

## Applied Result

The reviewed plan was applied after backing up `state.sqlite` as `state.sqlite.bak.20260717-idea-portfolio`. The runtime now contains five canonical Research Ideas. Stage pipeline and SASS-grounded are `explored`, `selected`, and `supported`; pure roofline is `unexplored` and `closed` with reason `rejection`; probabilistic occupancy is `unexplored` with unknown decision and evidence; SASS critical path is `unexplored` and `deferred` with unknown evidence.

The raw slate generation contains its four exact proposal concepts. The route Decision Record contains four explicit options and reports `option_set_complete: true`. The probabilistic option has no invented rationale. The stage-pipeline concept has proposal, candidate, and selected-hypothesis realizations at `$.sections.raw_ideas[1]`, `$.sections.serious_candidates[0]`, and the selected-hypothesis object `$.sections`. The two reviewed Idea Lineage Edges are present, and descendant traversal from stage pipeline returns stage pipeline plus SASS-grounded with `topology_complete: true`.

`ideas validate` returned no errors. It returned four expected warnings: the pre-existing SASS Research Note has no managed structured payload, and pure roofline, probabilistic occupancy, and SASS critical path retain one or more unknown facets. The query-index rebuild completed with 85 records, 1,416 facts, 87 files, 10 extracted idea facets, 37 metrics, and 27 routes. The rebuild exposed a same-database SQLite lock in canonical lineage refresh; the implementation now preloads canonical record-lineage rows before the query-index write transaction, and a regression test covers rebuild with canonical lineage.

## Project Web Verification

The latest source-checkout GUI was built and served at `http://127.0.0.1:8766` in debug cache mode. All fixed presets returned complete, non-mutating topology over the five-idea source scope: `current` 3, `all-proposed` 5, `open-for-exploration` 2, `unexplored` 3, `exploring` 0, `explored` 2, `selected` 2, `deferred` 1, `closed` 1, and `needs-classification` 3. Filtered edges remained coherent.

Playwright verified initial current-portfolio loading, all five ideas in graph and timeline, graph controls collapsed by default, independent graph and timeline filter state, all four route options with rationale and closure diagnostics, stage-pipeline descendant traversal, exact realization paths, and the unsubmitted `Explore instead` confirmation with exact target and replacement transitions. The same browser test rendered shared Kaoju-only and mixed-paradigm fixtures through the generic graph and timeline components without Kaoju-specific payload parsing.
