# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <DECISION_CONTEXT_BRIEF> | current board packet, latest result, stale-route state, quest documents | Decision-ready summary of current state. | isomer-rsch-decision-v2 | route judgment | evidence |
| <ROUTE_QUESTION> | real decision question | The explicit route choice being judged. | isomer-rsch-decision-v2 | decision evidence packet | decision |
| <DECISION_EVIDENCE_PACKET> | support, contradiction, risk, cost, new evidence | Evidence used to select the route. | isomer-rsch-decision-v2 | route decision record | evidence |
| <ROUTE_DECISION_RECORD> | strategic-decision-template output | Durable verdict, action, reason, evidence, rejected alternatives, and next route. | isomer-rsch-decision-v2 | any v2 research skill | decision |
| <DECISION_CHECKPOINT_MEMORY> | checkpoint-memory-template output | Resume memory for route-changing decisions. | isomer-rsch-decision-v2 | future work | runtime state |
| <USER_DECISION_REQUEST> | request_user_decision canonical action | User-facing choice request when local evidence cannot resolve preference, scope, or cost. | isomer-rsch-decision-v2 | user | decision |
| <DECISION_BLOCKER_RECORD> | blocked route judgment | Why the route cannot be decided responsibly. | isomer-rsch-decision-v2 | user or continued decision work | decision |
