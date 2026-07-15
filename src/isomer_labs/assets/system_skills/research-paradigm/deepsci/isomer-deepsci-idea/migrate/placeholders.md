# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:IDEA-CONTEXT-BRIEF | framed problem, baseline state, metric contract, latest result, constraints | Direction-selection context. | scout, baseline, analysis, decision, or user context | isomer-rsch-idea | evidence |
| DEEPSCI:OBJECTIVE-CONTRACT | objective-contract-template output | Real target, proxies, constraints, metric, and contribution frame. | isomer-rsch-idea | candidate generation and selection | handoff |
| DEEPSCI:CURRENT-BOARD-PACKET | current-board-packet-template output | Incumbent, latest result, blocker, stale routes, and current question. | isomer-rsch-idea | candidate generation | evidence |
| DEEPSCI:LITERATURE-SURVEY-REPORT | literature-survey-template output | Closest prior work and novelty or value boundary. | isomer-rsch-idea | candidate selection and writing | report |
| DEEPSCI:RELATED-WORK-MAP | related-work map, closest-prior-work table, research history lineage | Structured prior-work comparison and history-aware novelty context. | isomer-rsch-idea or scout companion route | candidate generation and selection | report |
| DEEPSCI:LIMITATIONS-MAP | limitations analysis and bottleneck map | Decision-relevant failure regions, contradictions, and root-cause hypotheses. | isomer-rsch-idea | candidate generation | report |
| DEEPSCI:MECHANISM-FRAMING | mathematical and mechanism framing | Symptom, mechanism hypothesis, consequence, lever bucket, and code translation. | isomer-rsch-idea | candidate generation and pre-idea draft | evidence |
| DEEPSCI:RAW-IDEA-SLATE | bounded divergent idea slate | Initial differentiated set of raw route candidates before filtering. | isomer-rsch-idea | candidate frontier filtering | report |
| DEEPSCI:CANDIDATE-IDEA-FRONTIER | candidate ideas and direction families | Bounded differentiated candidate set. | isomer-rsch-idea | selection gate or optimize | report |
| DEEPSCI:REJECTED-AND-DEFERRED-IDEAS | rejected and deferred candidate ledger | Non-selected candidates with rejection or deferral reasons. | isomer-rsch-idea | future idea passes and decision records | decision |
| DEEPSCI:PRE-IDEA-DRAFT | pre-idea-draft-template output | Challenge memo for a serious candidate. | isomer-rsch-idea | selection gate | draft |
| DEEPSCI:SELECTED-HYPOTHESIS | selected idea package | One falsifiable route ready for experiment or optimize. | isomer-rsch-idea | experiment, optimize, decision | handoff |
| DEEPSCI:SELECTED-IDEA-DRAFT | final selected idea draft | Citation-bearing Markdown rationale for the selected route before structured handoff. | isomer-rsch-idea | experiment, optimize, writing, review | draft |
| DEEPSCI:IDEA-ROUTE-DECISION | experiment, optimize, scout, baseline, decision, or blocker route | Route after selection. | isomer-rsch-idea | any production DeepSci research skill | decision |
| DEEPSCI:IDEA-BLOCKER-RECORD | no candidate passes or missing evidence | Why direction selection cannot proceed responsibly. | isomer-rsch-idea | user, scout, baseline, decision | decision |
| DEEPSCI:IDEA-MEMORY-RECORD | source memory cards and durable survey or idea notes | Reusable reasoning, survey deltas, novelty caveats, rejected idea lessons, and retrieval hints. | isomer-rsch-idea | future idea, scout, experiment, or write routes | runtime state |
| DEEPSCI:PAPER-OUTLINE-SEED | outline-seeding-example output | Lightweight paper-facing outline seed for a selected route likely to become a paper line. | isomer-rsch-idea | paper outline, experiment, write, analysis planning | draft |
| DEEPSCI:RESEARCH-OUTLINE-NOTE | research-outline-template output | Structured research-plan note with code, dataset, math, baseline, directions, metrics, and constraints. | isomer-rsch-idea | candidate selection, experiment planning, paper outline | report |
