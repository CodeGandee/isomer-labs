# Terminal Report

## Required Shape

Every bounded procedure or stage returns:

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

`paused` means continuation is possible after a user decision, Gate, or chosen boundary. `blocked` means the requested bounded result cannot proceed without an external state change. `complete` means the selected procedure met its accepted stop conditions, not that the whole field is exhausted.

Do not select or start another macro procedure in the terminal report.
