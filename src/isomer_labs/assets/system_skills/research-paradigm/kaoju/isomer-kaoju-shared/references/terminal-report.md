# Terminal Report

## Durable Artifact Schema

This table defines the exact stored terminal-report artifact, not the chat response format. Preserve these fields in the durable report, then summarize the outcome, accepted outputs, blockers, and resume point in natural-language Markdown for chat.

Every bounded procedure or stage records:

| Field | Requirement |
| --- | --- |
| `status` | Exactly `complete`, `paused`, or `blocked`. |
| `procedure` | Active procedure and stage range completed. |
| `accepted_inputs` | Durable refs and identity checks. |
| `accepted_outputs` | Artifact, Evidence Item, Run, Finding, Decision Record, and Provenance Record refs. |
| `stage_outcomes` | Completed, skipped with reason, failed, or blocked for each planned stage. |
| `evidence_summary` | Achieved depth, verdicts, fidelity, input basis, contradictions, and limitations. |
| `resources_and_gates` | Material resource use and Gate decisions. |
| `blockers` | Unresolved conditions and affected outputs. |
| `resume_point` | Accepted refs, starting stage, required decision or state change; omit only for complete work with no continuation. |

`paused` means continuation is possible after a user decision, Gate, chosen boundary, or known in-scope producer route. `blocked` means the requested bounded result cannot proceed without an unavailable external state change. `complete` means the selected procedure met its accepted stop conditions, not that the whole field is exhausted.

Do not select or start another macro procedure in the terminal report. The report may name a producer or repair route and the original target resume point. After the report is recorded, an explicitly authorized prompt-level run-to controller may validate its refs, refresh durable state, and consume that route as a separate procedure Run inside the target closure.
