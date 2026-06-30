# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <BASELINE_CONTEXT_BRIEF> | baseline state, requested baseline ref, confirmed baseline ref, metric contract, blockers | Current comparator trust situation. | isomer-rsch-baseline-v2 | route selection | evidence |
| <COMPARATOR_ROUTE_RECORD> | baseline route decision | Selected attach, import, verify-local-existing, reproduce, repair, publish, waive, or block route. | isomer-rsch-baseline-v2 | verification | decision |
| <COMPARABILITY_CONTRACT> | <baseline_root>/json/metric_contract.json and metric contract fields | Semantic comparison contract pending storage binding. | isomer-rsch-baseline-v2 | idea, experiment, analysis, decision | handoff |
| <BASELINE_VERIFICATION_EVIDENCE> | real outputs, logs, service responses, source artifacts, or registry records | Evidence proving comparator trust or failure. | isomer-rsch-baseline-v2 | accepted baseline or blocker | evidence |
| <ACCEPTED_BASELINE_RECORD> | artifact.confirm_baseline(...) or overwrite_baseline | Accepted comparator record. | isomer-rsch-baseline-v2 | idea, experiment, analysis, decision | handoff |
| <BASELINE_WAIVER_RECORD> | artifact.waive_baseline(...) | Explicit waiver and reason. | isomer-rsch-baseline-v2 or decision | idea, experiment, decision | decision |
| <BASELINE_BLOCKER_RECORD> | blocked baseline state | Why the comparator gate cannot close and what is needed. | isomer-rsch-baseline-v2 | user or decision | decision |
| <BASELINE_ROUTE_DECISION> | next route after baseline | Next route after confirmation, waiver, or blocker. | isomer-rsch-baseline-v2 | any v2 research skill | decision |
