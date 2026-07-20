# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:OPTIMIZATION-CONTEXT-BRIEF | current algorithm-first state and latest measured result | Context for frontier review. | optimize, experiment, decision, or user context | isomer-rsch-optimize | evidence |
| DEEPSCI:OPTIMIZATION-FRONTIER | optimization frontier state | Candidate set, active lines, results, failures, blockers, and recommended route. | isomer-rsch-optimize | ranking, experiment, decision | runtime state |
| DEEPSCI:OPTIMIZE-CHECKLIST | `OPTIMIZE_CHECKLIST.md` and optimize checklist template | Pass-level frontier and execution checklist. | isomer-rsch-optimize | optimize closeout and resume | runtime state |
| DEEPSCI:CANDIDATE-BOARD | `CANDIDATE_BOARD.md` | Compact ledger for candidate briefs and implementation attempts. | isomer-rsch-optimize | frontier review and ranking | runtime state |
| DEEPSCI:CANDIDATE-BRIEF | method-brief-template output or candidate submission | One branchless method proposal. | isomer-rsch-optimize | ranking or promotion | draft |
| DEEPSCI:METHOD-BRIEF | `references/method-brief-template.md` | Structured method brief fields for bottleneck, mechanism, family, change layer, risk, and next target. | isomer-rsch-optimize | ranking or promotion | draft |
| DEEPSCI:CANDIDATE-RANKING | candidate-ranking-template output | Scored candidate set, winner, non-winner notes, and promotion cap. | isomer-rsch-optimize | promotion or decision | report |
| DEEPSCI:CODEGEN-ROUTE-PLAN | codegen route playbook response | Chosen code-generation route, bounded implementation surface, keep-unchanged contract, and validation step. | isomer-rsch-optimize | implementation attempt | code |
| DEEPSCI:PROMOTED-OPTIMIZATION-LINE | promoted durable optimization line | Durable line worth experiment or implementation work. | isomer-rsch-optimize | experiment | handoff |
| DEEPSCI:OPTIMIZATION-ATTEMPT-RECORD | optimization candidate report, smoke result, patch attempt, debug result, or fusion candidate | Within-line implementation, debug, smoke, or fusion attempt. | isomer-rsch-optimize or experiment | frontier review | run record |
| DEEPSCI:DEBUG-RESPONSE | `references/debug-response-template.md` | Concrete failure, prior lesson, root cause, minimal fix, next check, and archive threshold. | isomer-rsch-optimize | implementation or frontier review | report |
| DEEPSCI:FUSION-PLAN | `references/fusion-playbook.md` | Source line strengths, weakness, fusion claim, keep-unchanged contract, and bounded validation plan. | isomer-rsch-optimize | implementation or experiment | handoff |
| DEEPSCI:PLATEAU-RESPONSE | `references/plateau-response-playbook.md` | Plateau diagnosis, route change, and non-repeat rule. | isomer-rsch-optimize | frontier review and future optimize pass | decision |
| DEEPSCI:PROMPT-CONTRACT | `references/prompt-patterns.md` | Stable prompt and reasoning contract for an optimize subroutine. | isomer-rsch-optimize | candidate shaping, debug, fusion, or codegen | runtime state |
| DEEPSCI:OPTIMIZATION-MEMORY-CARD | optimization-memory-template output | Reusable success pattern, failure pattern, fusion lesson, or non-retry rule. | isomer-rsch-optimize | future optimize work | runtime state |
| DEEPSCI:FRONTIER-REVIEW | frontier-review-template output | Interpretation of latest result, plateau, fusion, debug, or route state. | isomer-rsch-optimize | route decision | report |
| DEEPSCI:OPTIMIZE-ROUTE-DECISION | explore, exploit, fusion, debug, experiment, decision, stop | One next route or stop condition. | isomer-rsch-optimize | any production DeepSci research skill | decision |
| DEEPSCI:OPTIMIZE-BLOCKER-RECORD | blocked optimization state | Why frontier work cannot proceed responsibly. | isomer-rsch-optimize | user or decision | decision |
