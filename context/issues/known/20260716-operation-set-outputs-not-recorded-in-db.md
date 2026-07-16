# Operation-Set Outputs Are Not Automatically Recorded in the Research Database

**Discovered**: 2026-07-16
**Last confirmed**: 2026-07-17
**Topic**: flash-attention-4-whitebox-runtime-model
**Severity**: process/intent
**Status**: open

## What happened

During active research on the Flash Attention 4 white-box runtime model, several important operation-set outputs were produced under `actors/operator/isomer-managed/worker-output/topic-actors/operator/sets/`:

- `20260716-190425-idea-exploration-0d3cfc2d/idea_exploration_report.json`
- `20260716-191336-gpu-microbenchmarks-fc087965/gpu_microbenchmark_report.json`
- `20260716-192358-optimized-gpu-microbenchmarks-e2995ac6/optimized_microbenchmark_report.json`
- `20260716-192756-predictor-validation-94a9fbf5/predictor_validation_report.json`
- `20260716-195800-dataflow-predictor/dataflow_predictor.py`
- `20260716-sass-grounded-research/sass_grounded_references.md`

These artifacts were left as plain files in the Topic Actor output tree. They were **not** created as durable `ext research records` with canonical lineage at the time they were produced. A separate manual pass was required to import them into the research database and wire lineage edges after the fact.

## What this is

This is a workflow-contract and skill-intent failure at the operation-set persistence boundary. The operation completed when its files and terminal summary existed, even though no terminal gate required the agent to create durable records, attach immediate parents, link applicable Research Ideas, and verify the stored result. The database and CLI already support those actions, so this is not primarily a database-write or GUI-rendering defect.

The failure has two distinct layers:

1. Research-relevant operation-set files were not persisted as durable research records when produced.
2. Creating records and record-to-record lineage does not automatically create canonical Research Ideas or idea-to-idea lineage. The Idea Graph reads canonical `research_ideas` and `research_idea_lineage_edges` once any canonical idea exists; it does not mix in extracted legacy idea facets.

The second layer explains why importing the missing outputs can repair the Records and record-lineage views while the Idea Graph still shows only one node. At confirmation time, this topic contained one canonical Research Idea, one realization, no canonical idea-lineage edges, and ten extracted legacy idea facets from earlier idea-slate records.

## Why this is a problem

- **Lineage is reconstructed, not captured**. The relationship between the selected hypothesis, the idea exploration sweep, the microbenchmarks, the predictor validation, and the SASS-grounded follow-up was only established by a later manual step. If that step had been skipped, the provenance chain would have been broken.
- **Records are not queryable during research**. While the files exist in the actor workspace, they do not appear in `ext research records list`, `ext research ideas query`, or lineage queries until someone manually imports them. This defeats the purpose of a canonical research database.
- **Risk of loss or duplication**. Plain generated files are not tracked by the research record index. They can be overwritten, moved, or duplicated without the system noticing.
- **Skill intent is unclear**. The production DeepSci skills (`isomer-deepsci-pipeline`, `isomer-deepsci-idea`, `isomer-deepsci-experiment`, `isomer-deepsci-analysis`) emphasize durable records and lineage in their documentation, but the actual operation-set outputs from helper passes were not persisted as records. This suggests the skills either do not instruct agents to record plain operation-set outputs, or the instruction is not strong enough to be followed.

## Correct intent

Any operation set that produces a research-relevant artifact should, by default, create a corresponding durable research record at the end of the operation:

1. JSON experiment reports → `evidence_item` / `DEEPSCI:EXPERIMENT-RESULT` (or appropriate experiment semantic id).
2. Analysis reports and exploration summaries → `artifact` / `DEEPSCI:ANALYSIS-CAMPAIGN-SUMMARY` (or appropriate analysis semantic id).
3. Code deliverables → `artifact` / `DEEPSCI:IMPLEMENTATION-CHANGE-MAP` with a JSON wrapper that references the source file.
4. Reference notes and literature summaries → `artifact` / `DEEPSCI:RESEARCH-NOTE` (or body record) and linked to the relevant Research Idea via `ext research ideas realize`.
5. Each record must carry `--parents-json` lineage to its immediate durable predecessors.

The default should be opt-out, not opt-in. If an operation set genuinely produces only disposable scratch output, the agent should explicitly record that decision.

## Recovery performed

The manual recovery created or confirmed these durable records:

| Operation set | Record kind | Semantic id | Record id |
| --- | --- | --- | --- |
| Idea exploration report | `artifact` | `DEEPSCI:ANALYSIS-CAMPAIGN-SUMMARY` | `artifact-DEEPSCI-ANALYSIS-CAMPAIGN-SUMMARY-7ab990596bcc` |
| GPU microbenchmarks, first pass | `evidence_item` | `DEEPSCI:EXPERIMENT-RESULT` | `evidence_item-DEEPSCI-EXPERIMENT-RESULT-3349842e3d1a` |
| Optimized GPU microbenchmarks | `evidence_item` | `DEEPSCI:EXPERIMENT-RESULT` | `evidence_item-DEEPSCI-EXPERIMENT-RESULT-1efa1724538c` |
| Predictor validation, 12.774x result | `evidence_item` | `DEEPSCI:EXPERIMENT-RESULT` | `evidence_item-DEEPSCI-EXPERIMENT-RESULT-6fe490f02531` |
| Dataflow predictor code | `artifact` | `DEEPSCI:IMPLEMENTATION-CHANGE-MAP` | `artifact-DEEPSCI-IMPLEMENTATION-CHANGE-MAP-c4af0935da74` |
| SASS reference note | `artifact` | `DEEPSCI:RESEARCH-NOTE` | `artifact-DEEPSCI-RESEARCH-NOTE-36be5f056187` |

The selected hypothesis `artifact-DEEPSCI-SELECTED-HYPOTHESIS-6ff8d6824fa3` is the common ancestor. The recovered record chain connects idea exploration to the first microbenchmarks with `follow_up_to`, the first microbenchmarks to the optimized pass with `revision_of`, the optimized pass and idea exploration to predictor validation with `derived_from`, predictor validation to the dataflow predictor with `derived_from`, and the dataflow predictor to the SASS note with `derived_from`. The SASS note is also a realization of Research Idea `I-1` / `sass-grounded-interpretable-model` at the `exploration` stage.

This recovery repairs durable record storage and record lineage. It does not by itself promote the candidate ideas embedded in earlier raw-idea-slate and candidate-frontier payloads into canonical Research Ideas or construct their idea lineage.

## Recommended fixes

1. Update `isomer-deepsci-pipeline` and the focused production DeepSci skills to include an explicit final step: "persist operation-set deliverables as durable research records with lineage" before returning the terminal report.
2. Provide a helper command or skill (e.g., `isomer-op-project-mgr record-operation-set`) that wraps the common case of importing an operation-set output directory into the research database.
3. Add a quality gate to pipeline terminal reports: verify that all non-temporary operation-set outputs are queryable as records.
4. Document the expectation in `AGENTS.md` and the operator skill instructions so that every agent understands that plain files in `worker-output/sets/` are not the final durable artifact unless explicitly marked disposable.
5. Consider introducing a dedicated relationship-building skill (e.g., `isomer-deepsci-lineage` or `isomer-op-record-lineage`) because agent behavior around durable-record creation is uncertain. A focused skill can:
   - Inspect an operation-set output directory.
   - Decide the correct `record_kind`, `semantic_id`, and schema/profile for each file.
   - Infer or accept explicit parent record ids.
   - Call `ext research records create` with `--parents-json` and the correct lineage kind.
   - Link records to Research Ideas via `ext research ideas realize` when applicable.
   - Validate the resulting graph and report missing parents or orphan files.
   This keeps lineage construction as a first-class, testable capability rather than relying on every agent to remember the right CLI incantations.

6. Integrate the scan-and-build-lineage skill into the standard workflow of skills that generate ideas (for example, `isomer-deepsci-idea`, `isomer-deepsci-pipeline` idea stages, and any helper operation set that produces candidate routes). After an idea-generation stage finishes, the skill should scan the operation-set output directory, create or update Research Ideas for each candidate, and wire `derived_from`, `selected_from`, `follow_up_to`, and `subsumes` edges automatically. This makes lineage a built-in step rather than a separate manual cleanup pass.

## Related records

- `artifact-DEEPSCI-SELECTED-HYPOTHESIS-6ff8d6824fa3` — stage-pipeline predictor hypothesis.
- `artifact-DEEPSCI-ANALYSIS-CAMPAIGN-SUMMARY-7ab990596bcc` — manually imported idea exploration report.
- `evidence_item-DEEPSCI-EXPERIMENT-RESULT-3349842e3d1a` — manually imported first GPU microbenchmark report.
- `evidence_item-DEEPSCI-EXPERIMENT-RESULT-1efa1724538c` — manually imported optimized microbenchmark report.
- `evidence_item-DEEPSCI-EXPERIMENT-RESULT-6fe490f02531` — manually imported predictor validation report (12.774× result).
- `artifact-DEEPSCI-IMPLEMENTATION-CHANGE-MAP-c4af0935da74` — manually imported dataflow predictor.
- `artifact-DEEPSCI-RESEARCH-NOTE-36be5f056187` — manually imported SASS reference note.
- Research Idea `I-1` / `sass-grounded-interpretable-model` — linked to the SASS reference note via `ext research ideas realize`.
