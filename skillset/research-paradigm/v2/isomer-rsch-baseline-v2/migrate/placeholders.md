# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <BASELINE_CONTEXT_BRIEF> | baseline state, requested baseline ref, confirmed baseline ref, metric contract, blockers | Current comparator trust situation. | isomer-rsch-baseline-v2 | route selection | evidence |
| <COMPARATOR_ROUTE_RECORD> | baseline route decision | Selected attach, import, verify-local-existing, reproduce, repair, publish, waive, or block route. | isomer-rsch-baseline-v2 | verification | decision |
| <BASELINE_ROUTE_PLAN> | `references/baseline-plan-template.md`, route record, or plan-like compatibility surface | Durable route record for ambiguous, code-touching, expensive, broken, long-running, or reuse-facing baseline work. | isomer-rsch-baseline-v2 | verification and closeout | runtime state |
| <BASELINE_GATE_CHECKLIST> | `references/baseline-checklist-template.md` | Optional acceptance-boundary checklist for baseline route validation. | isomer-rsch-baseline-v2 | verification and closeout | runtime state |
| <COMPARABILITY_CONTRACT> | `<baseline_root>/json/metric_contract.json` and metric contract fields | Semantic comparison contract pending storage binding. | isomer-rsch-baseline-v2 | idea, experiment, analysis, decision | handoff |
| <CODEBASE_AUDIT_RECORD> | source audit notes, implementation map, evaluation path, practical constraints | Focused source audit used only when reproduce or repair requires source understanding. | isomer-rsch-baseline-v2 | reproduce, repair, verification | evidence |
| <BASELINE_PROVENANCE_RECORD> | `attachment.yaml` or equivalent provenance for attached or imported baseline material | Durable source, package, registry, service, or local bundle identity and caveats. | isomer-rsch-baseline-v2 | verification and acceptance | evidence |
| <BASELINE_VERIFICATION_EVIDENCE> | real outputs, logs, service responses, source artifacts, registry records, or package records | Evidence proving comparator trust or failure. | isomer-rsch-baseline-v2 | accepted baseline or blocker | evidence |
| <BASELINE_PAYLOAD_RECORD> | accepted, waived, blocked, or route-decision payload fields | Compact structured payload carrying baseline id, metrics, provenance, caveats, route, and next direction. | isomer-rsch-baseline-v2 | downstream v2 research skills | handoff |
| <ACCEPTED_BASELINE_RECORD> | confirmed or overwritten accepted baseline record | Accepted comparator record. | isomer-rsch-baseline-v2 | idea, experiment, analysis, decision | handoff |
| <BASELINE_WAIVER_RECORD> | waived baseline gate record | Explicit waiver and reason. | isomer-rsch-baseline-v2 or decision | idea, experiment, decision | decision |
| <BASELINE_BLOCKER_RECORD> | blocked baseline state | Why the comparator gate cannot close and what is needed. | isomer-rsch-baseline-v2 | user or decision | decision |
| <BASELINE_ROUTE_DECISION> | next route after baseline | Next route after confirmation, waiver, blocker, or route change. | isomer-rsch-baseline-v2 | any v2 research skill | decision |
