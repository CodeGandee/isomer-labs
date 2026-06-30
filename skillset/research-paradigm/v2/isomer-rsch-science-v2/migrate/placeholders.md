# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <SCIENCE_TASK_BRIEF> | science-task-brief-template output | Scientific task, domain, package needs, resources, risks, and downstream consumer. | isomer-rsch-science-v2 or caller | science execution and validation | handoff |
| <SCIENCE_PACKAGE_CHECK> | package-check-playbook and package cards | Availability, version, executable, import, module, container, and smoke-test evidence. | isomer-rsch-science-v2 | science run decision | evidence |
| <SCIENCE_RUN_RECORD> | computational run, dataset analysis, simulation, sweep, or solver execution | Scientific execution evidence and outputs. | isomer-rsch-science-v2 | validation and claims | run record |
| <SCIENCE_VALIDATION_RESULT> | convergence, units, schema, controls, invariants, correctness checks | Validity check over scientific outputs. | isomer-rsch-science-v2 | claim record and downstream analysis | evidence |
| <SCIENCE_CLAIM_RECORD> | science.claim node | Calibrated scientific claim linked to supporting evidence. | isomer-rsch-science-v2 | experiment, analysis, decision, finalize | evidence |
| <SCIENCE_EVIDENCE_GRAPH_UPDATE> | artifact.science(...) Science Evidence Graph update | Compatibility record for science evidence graph mutation. | isomer-rsch-science-v2 | downstream research skills | runtime state |
| <SCIENCE_BLOCKER_RECORD> | blocked science task | Missing package, data, resources, validation, or scientific assumptions. | isomer-rsch-science-v2 | caller or user | decision |
| <SCIENCE_ROUTE_DECISION> | next route after science support | Return route to caller, experiment, analysis, decision, or blocker. | isomer-rsch-science-v2 | any v2 research skill | decision |
