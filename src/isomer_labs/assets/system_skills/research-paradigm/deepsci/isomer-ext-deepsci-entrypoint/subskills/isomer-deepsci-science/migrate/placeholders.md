# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:SCIENCE-TASK-BRIEF | science-task-brief-template output | Scientific task, domain, package needs, resources, risks, and downstream consumer. | isomer-rsch-science or caller | science execution and validation | handoff |
| DEEPSCI:SCIENCE-PACKAGE-CHECK | package-check-playbook and package cards | Availability, version, executable, import, module, container, and smoke-test evidence. | isomer-rsch-science | science run decision | evidence |
| DEEPSCI:SCIENCE-RUN-RECORD | computational run, dataset analysis, simulation, sweep, or solver execution | Scientific execution evidence and outputs. | isomer-rsch-science | validation and claims | run record |
| DEEPSCI:SCIENCE-VALIDATION-RESULT | convergence, units, schema, controls, invariants, correctness checks | Validity check over scientific outputs. | isomer-rsch-science | claim record and downstream analysis | evidence |
| DEEPSCI:SCIENCE-CLAIM-RECORD | science.claim node | Calibrated scientific claim linked to supporting evidence. | isomer-rsch-science | experiment, analysis, decision, finalize | evidence |
| DEEPSCI:SCIENCE-EVIDENCE-GRAPH-UPDATE | Science Evidence Graph update | Compatibility record for science evidence graph mutation. | isomer-rsch-science | downstream research skills | runtime state |
| DEEPSCI:SCIENCE-BLOCKER-RECORD | blocked science task | Missing package, data, resources, validation, or scientific assumptions. | isomer-rsch-science | caller or user | decision |
| DEEPSCI:SCIENCE-ROUTE-DECISION | next route after science support | Return route to caller, experiment, analysis, decision, or blocker. | isomer-rsch-science | any production DeepSci research skill | decision |
