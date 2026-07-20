# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:DECISION-CONTEXT-BRIEF | current board packet, latest result, stale-route state, quest documents | Decision-ready summary of current state. | isomer-rsch-decision | route judgment | evidence |
| DEEPSCI:ROUTE-QUESTION | real decision question | The explicit route choice being judged. | isomer-rsch-decision | decision evidence packet | decision |
| DEEPSCI:DECISION-EVIDENCE-PACKET | support, contradiction, risk, cost, new evidence | Evidence used to select the route. | isomer-rsch-decision | route decision record | evidence |
| DEEPSCI:ROUTE-DECISION-RECORD | strategic-decision-template output | Durable verdict, action, reason, evidence, rejected alternatives, and next route. | isomer-rsch-decision | any production DeepSci research skill | decision |
| DEEPSCI:DECISION-CHECKPOINT-MEMORY | checkpoint-memory-template output | Resume memory for route-changing decisions. | isomer-rsch-decision | future work | runtime state |
| DEEPSCI:USER-DECISION-REQUEST | request_user_decision canonical action | User-facing choice request when local evidence cannot resolve preference, scope, or cost. | isomer-rsch-decision | user | decision |
| DEEPSCI:DECISION-BLOCKER-RECORD | blocked route judgment | Why the route cannot be decided responsibly. | isomer-rsch-decision | user or continued decision work | decision |
