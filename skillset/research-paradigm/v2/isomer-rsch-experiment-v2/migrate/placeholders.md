# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <EXPERIMENT_CONTEXT_BRIEF> | selected idea, accepted baseline, metric contract, current workspace | Current run-ready context. | idea, optimize, baseline, decision, or user context | isomer-rsch-experiment-v2 | evidence |
| <EXPERIMENT_CONTRACT> | main-experiment-plan-template and run contract fields | The fixed measured-run contract. | isomer-rsch-experiment-v2 | execution and validation | handoff |
| <EXPERIMENT_PLAN> | `PLAN.md` and `references/main-experiment-plan-template.md` | Native plan for non-trivial, expensive, branch-sensitive, or long-running experiment work. | isomer-rsch-experiment-v2 | execution and validation | runtime state |
| <EXPERIMENT_CHECKLIST> | `CHECKLIST.md` and `references/main-experiment-checklist-template.md` | Live control checklist for planning, implementation, smoke, main run, validation, and closeout. | isomer-rsch-experiment-v2 | execution and validation | runtime state |
| <IMPLEMENTATION_CHANGE_MAP> | minimal code-change map | The smallest hypothesis-bound implementation plan. | isomer-rsch-experiment-v2 | execution | code |
| <SMOKE_CHECK_RECORD> | smoke or pilot checks | Bounded command-path, schema, or evaluator-wiring check. | isomer-rsch-experiment-v2 | real run decision | run record |
| <MAIN_RUN_RECORD> | main experiment record and run manifest | Commands, configs, logs, outputs, metrics, and environment facts for the real run. | isomer-rsch-experiment-v2 | analysis, decision, optimize, finalize | run record |
| <EXPERIMENT_ARTIFACT_MANIFEST> | artifact manifest, run manifest, metrics, summary, logs, environment snapshot | Durable evidence inventory for the experiment run. | isomer-rsch-experiment-v2 | analysis, decision, optimize, finalize | evidence |
| <CLAIM_VALIDATION_RECORD> | claim validation table and claim-to-metric traceability | Claim, metric key, expected direction, observed result, verdict, and caveat mapping. | isomer-rsch-experiment-v2 | analysis, write, decision, finalize | evidence |
| <EXPERIMENT_RESULT_SUMMARY> | evaluation summary, claim update, baseline relation, failure mode, next action | Stable interpretation of the measured result. | isomer-rsch-experiment-v2 | analysis, decision, optimize, finalize | evidence |
| <EXPERIMENT_ROUTE_DECISION> | next route after experiment | Evidence-backed route after the run. | isomer-rsch-experiment-v2 | analysis, optimize, decision, finalize, idea | decision |
| <EXPERIMENT_BLOCKER_RECORD> | blocked experiment state | Why execution or validation cannot complete responsibly. | isomer-rsch-experiment-v2 | user or decision | decision |
