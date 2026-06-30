# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <OPTIMIZATION_CONTEXT_BRIEF> | current algorithm-first state and latest measured result | Context for frontier review. | optimize, experiment, decision, or user context | isomer-rsch-optimize-v2 | evidence |
| <OPTIMIZATION_FRONTIER> | artifact.get_optimization_frontier(...) and frontier state | Candidate set, active lines, results, failures, and recommended route. | isomer-rsch-optimize-v2 | ranking, experiment, decision | runtime state |
| <CANDIDATE_BRIEF> | method-brief-template output | One branchless method proposal. | isomer-rsch-optimize-v2 | ranking or promotion | draft |
| <CANDIDATE_RANKING> | candidate-ranking-template output | Scored candidate set and winner. | isomer-rsch-optimize-v2 | promotion or decision | report |
| <PROMOTED_OPTIMIZATION_LINE> | artifact.submit_idea submission_mode=line | Durable line worth experiment or implementation work. | isomer-rsch-optimize-v2 | experiment | handoff |
| <OPTIMIZATION_ATTEMPT_RECORD> | optimization candidate report or debug response | Within-line implementation, debug, smoke, or fusion attempt. | isomer-rsch-optimize-v2 or experiment | frontier review | run record |
| <FRONTIER_REVIEW> | frontier-review-template output | Interpretation of latest result, plateau, fusion, debug, or route state. | isomer-rsch-optimize-v2 | route decision | report |
| <OPTIMIZE_ROUTE_DECISION> | explore, exploit, fusion, debug, experiment, decision, stop | One next route or stop condition. | isomer-rsch-optimize-v2 | any v2 research skill | decision |
| <OPTIMIZE_BLOCKER_RECORD> | blocked optimization state | Why frontier work cannot proceed responsibly. | isomer-rsch-optimize-v2 | user or decision | decision |
