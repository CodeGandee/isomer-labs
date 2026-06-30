# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <ANALYSIS_CONTEXT_BRIEF> | parent result, selected idea, paper gap, reviewer item, route decision, or failure mode | The current parent object and analysis question. | isomer-rsch-analysis-v2 | analysis slices and route decision | evidence |
| <PARENT_RESULT_EVIDENCE> | recent run artifacts, analysis reports, baseline state, paper rows, reviewer items | Evidence that defines what the campaign may update. | experiment, write, review, decision, or user context | isomer-rsch-analysis-v2 | evidence |
| <ANALYSIS_RESOURCE_ENVELOPE> | current device and runtime limits, available assets, dependencies, services, credentials, storage, wall-clock budget, and blocked slices | Practical execution boundary that conditions slice design and ordering. | isomer-rsch-analysis-v2 | campaign design and execution | runtime state |
| <ANALYSIS_CAMPAIGN_PLAN> | `references/campaign-plan-template.md`, campaign route record, or campaign object | Durable route record for multi-slice, writing-facing, route-changing, expensive, unstable, or long-running analysis. | isomer-rsch-analysis-v2 | slice execution and downstream decision | handoff |
| <ANALYSIS_CAMPAIGN_CHECKLIST> | `references/campaign-checklist-template.md` | Optional acceptance-boundary checklist for frontier, resource, evidence, comparability, paper or review, blocker, and closeout gates. | isomer-rsch-analysis-v2 | campaign validation | runtime state |
| <ANALYSIS_SLICE_PLAN> | campaign-plan-template and campaign-design source pages | The bounded list of follow-up slices and stop conditions. | isomer-rsch-analysis-v2 | slice execution | handoff |
| <ANALYSIS_SLICE_RECORD> | slice evidence path, metric, comparability, claim update | One recorded analysis slice. | isomer-rsch-analysis-v2 | campaign summary and downstream decision | evidence |
| <ANALYSIS_WRITEBACK_MAP> | selected outline, paper matrix, evidence ledger, section, claim, table, reviewer item, rebuttal item, and paper-facing metadata | Map from writing-facing or review-facing slice evidence back to the paper, review, or rebuttal contract. | isomer-rsch-analysis-v2 | write, review, rebuttal, decision, finalize | handoff |
| <ANALYSIS_CAMPAIGN_SUMMARY> | campaign checklist and interpretation boundary | Aggregate interpretation of recorded slices. | isomer-rsch-analysis-v2 | decision, finalize, write, experiment, idea | report |
| <ANALYSIS_ROUTE_DECISION> | next route after analysis campaign | The evidence-backed next route. | isomer-rsch-analysis-v2 | any v2 research skill | decision |
| <ANALYSIS_BLOCKER_RECORD> | blocked analysis state | Missing data, resources, comparability, parent clarity, write-back target, or execution feasibility that blocks analysis. | isomer-rsch-analysis-v2 | user, decision, or continued analysis | decision |
| <ANALYSIS_CONTINUITY_UPDATE> | memory, status, report, or route update | Continuity note preserving reusable analysis conclusions. | isomer-rsch-analysis-v2 | future research work | runtime state |
