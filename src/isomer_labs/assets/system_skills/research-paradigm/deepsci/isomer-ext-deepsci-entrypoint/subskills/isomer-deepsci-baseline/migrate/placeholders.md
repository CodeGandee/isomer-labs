# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:BASELINE-CONTEXT-BRIEF | baseline state, requested baseline ref, confirmed baseline ref, metric contract, blockers | Current comparator trust situation. | isomer-rsch-baseline | route selection | evidence |
| DEEPSCI:COMPARATOR-ROUTE-RECORD | baseline route decision | Selected attach, import, verify-local-existing, reproduce, repair, publish, waive, or block route. | isomer-rsch-baseline | verification | decision |
| DEEPSCI:BASELINE-ROUTE-PLAN | `references/baseline-plan-template.md`, route record, or plan-like compatibility surface | Durable route record for ambiguous, code-touching, expensive, broken, long-running, or reuse-facing baseline work. | isomer-rsch-baseline | verification and closeout | runtime state |
| DEEPSCI:BASELINE-GATE-CHECKLIST | `references/baseline-checklist-template.md` | Optional acceptance-boundary checklist for baseline route validation. | isomer-rsch-baseline | verification and closeout | runtime state |
| DEEPSCI:COMPARABILITY-CONTRACT | `<baseline_root>/json/metric_contract.json` and metric contract fields | Semantic comparison contract pending storage binding. | isomer-rsch-baseline | idea, experiment, analysis, decision | handoff |
| DEEPSCI:CODEBASE-AUDIT-RECORD | source audit notes, implementation map, evaluation path, practical constraints | Focused source audit used only when reproduce or repair requires source understanding. | isomer-rsch-baseline | reproduce, repair, verification | evidence |
| DEEPSCI:BASELINE-PROVENANCE-RECORD | `attachment.yaml` or equivalent provenance for attached or imported baseline material | Durable source, package, registry, service, or local bundle identity and caveats. | isomer-rsch-baseline | verification and acceptance | evidence |
| DEEPSCI:BASELINE-VERIFICATION-EVIDENCE | real outputs, logs, service responses, source artifacts, registry records, or package records | Evidence proving comparator trust or failure. | isomer-rsch-baseline | accepted baseline or blocker | evidence |
| DEEPSCI:BASELINE-PAYLOAD-RECORD | accepted, waived, blocked, or route-decision payload fields | Compact structured payload carrying baseline id, metrics, provenance, caveats, route, and next direction. | isomer-rsch-baseline | downstream production DeepSci research skills | handoff |
| DEEPSCI:ACCEPTED-BASELINE-RECORD | confirmed or overwritten accepted baseline record | Accepted comparator record. | isomer-rsch-baseline | idea, experiment, analysis, decision | handoff |
| DEEPSCI:BASELINE-WAIVER-RECORD | waived baseline gate record | Explicit waiver and reason. | isomer-rsch-baseline or decision | idea, experiment, decision | decision |
| DEEPSCI:BASELINE-BLOCKER-RECORD | blocked baseline state | Why the comparator gate cannot close and what is needed. | isomer-rsch-baseline | user or decision | decision |
| DEEPSCI:BASELINE-ROUTE-DECISION | next route after baseline | Next route after confirmation, waiver, blocker, or route change. | isomer-rsch-baseline | any production DeepSci research skill | decision |
