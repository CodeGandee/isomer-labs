# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:EXPERIMENT-CONTEXT-BRIEF | selected idea, accepted baseline, metric contract, current workspace | Current run-ready context. | idea, optimize, baseline, decision, or user context | isomer-rsch-experiment | evidence |
| DEEPSCI:EXPERIMENT-CONTRACT | main-experiment-plan-template and run contract fields | The fixed measured-run contract. | isomer-rsch-experiment | execution and validation | handoff |
| DEEPSCI:EXPERIMENT-PLAN | `PLAN.md` and `references/main-experiment-plan-template.md` | Native plan for non-trivial, expensive, branch-sensitive, or long-running experiment work. | isomer-rsch-experiment | execution and validation | runtime state |
| DEEPSCI:EXPERIMENT-CHECKLIST | `CHECKLIST.md` and `references/main-experiment-checklist-template.md` | Live control checklist for planning, implementation, smoke, main run, validation, and closeout. | isomer-rsch-experiment | execution and validation | runtime state |
| DEEPSCI:IMPLEMENTATION-CHANGE-MAP | minimal code-change map | The smallest hypothesis-bound implementation plan. | isomer-rsch-experiment | execution | code |
| DEEPSCI:SMOKE-CHECK-RECORD | smoke or pilot checks | Bounded command-path, schema, or evaluator-wiring check. | isomer-rsch-experiment | real run decision | run record |
| DEEPSCI:MAIN-RUN-RECORD | main experiment record and run manifest | Commands, configs, logs, outputs, metrics, and environment facts for the real run. | isomer-rsch-experiment | analysis, decision, optimize, finalize | run record |
| DEEPSCI:EXPERIMENT-ARTIFACT-MANIFEST | artifact manifest, run manifest, metrics, summary, logs, environment snapshot | Durable evidence inventory for the experiment run. | isomer-rsch-experiment | analysis, decision, optimize, finalize | evidence |
| DEEPSCI:CLAIM-VALIDATION-RECORD | claim validation table and claim-to-metric traceability | Claim, metric key, expected direction, observed result, verdict, and caveat mapping. | isomer-rsch-experiment | analysis, write, decision, finalize | evidence |
| DEEPSCI:EXPERIMENT-RESULT-SUMMARY | evaluation summary, claim update, baseline relation, failure mode, next action | Stable interpretation of the measured result. | isomer-rsch-experiment | analysis, decision, optimize, finalize | evidence |
| DEEPSCI:EXPERIMENT-ROUTE-DECISION | next route after experiment | Evidence-backed route after the run. | isomer-rsch-experiment | analysis, optimize, decision, finalize, idea | decision |
| DEEPSCI:EXPERIMENT-BLOCKER-RECORD | blocked experiment state | Why execution or validation cannot complete responsibly. | isomer-rsch-experiment | user or decision | decision |
