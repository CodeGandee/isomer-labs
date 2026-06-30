# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <ANALYSIS_CONTEXT_BRIEF> | parent result, selected idea, paper gap, reviewer item, route decision, or failure mode | The current parent object and analysis question. | isomer-rsch-analysis-v2 | analysis slices and route decision | evidence |
| <PARENT_RESULT_EVIDENCE> | recent run artifacts, analysis reports, baseline state, paper rows, reviewer items | Evidence that defines what the campaign may update. | experiment, write, review, decision, or user context | isomer-rsch-analysis-v2 | evidence |
| <ANALYSIS_SLICE_PLAN> | campaign-plan-template and campaign-design source pages | The bounded list of follow-up slices and stop conditions. | isomer-rsch-analysis-v2 | slice execution | handoff |
| <ANALYSIS_SLICE_RECORD> | slice evidence path, metric, comparability, claim update | One recorded analysis slice. | isomer-rsch-analysis-v2 | campaign summary and downstream decision | evidence |
| <ANALYSIS_CAMPAIGN_SUMMARY> | campaign checklist and interpretation boundary | Aggregate interpretation of recorded slices. | isomer-rsch-analysis-v2 | decision, finalize, write, experiment, idea | report |
| <ANALYSIS_ROUTE_DECISION> | next route after analysis campaign | The evidence-backed next route. | isomer-rsch-analysis-v2 | any v2 research skill | decision |
| <ANALYSIS_BLOCKER_RECORD> | blocked analysis state | Missing data, resources, comparability, or parent clarity that blocks analysis. | isomer-rsch-analysis-v2 | user, decision, or continued analysis | decision |
| <ANALYSIS_CONTINUITY_UPDATE> | memory, status, report, or route update | Continuity note preserving reusable analysis conclusions. | isomer-rsch-analysis-v2 | future research work | runtime state |
