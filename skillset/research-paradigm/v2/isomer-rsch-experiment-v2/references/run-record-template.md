# Run Record Template

Use this reference to record the measured result. This page distills the source entrypoint and execution-playbook recording rules into native Isomer evidence records. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Summarize the run**. Write a concise `1-2` sentence outcome summary that names the research question, intervention, primary metric result, comparator relation, and strongest caveat.
2. **Record the execution payload**. Attach contract, code or config delta, commands, logs, outputs, metric values, seeds, environment facts, changed files, and relevant config paths to <MAIN_RUN_RECORD> and <EXPERIMENT_ARTIFACT_MANIFEST>.
3. **Validate the claim**. Create <CLAIM_VALIDATION_RECORD> that maps claim, metric key, expected direction, observed result, and verdict: `supported`, `refuted`, `inconclusive`, `partial`, or `blocked`.
4. **Write the stable evaluation summary**. Fill `takeaway`, `claim_update`, `baseline_relation`, `comparability`, `failure_mode`, and `next_action` in <EXPERIMENT_RESULT_SUMMARY>.
5. **Record partial or blocked states honestly**. If the run failed before comparable metrics, record what was attempted, where failure occurred, whether it was methodological or infrastructural, and the single best next action.
6. **Route from the record**. Produce <EXPERIMENT_ROUTE_DECISION> only after the result or blocker is recorded.

## Preferences

- Prefer exact evidence pointers over narrative reconstruction (if an output is missing, otherwise record the gap).
- Prefer concise structured fields on top of longer narrative notes (if the result is complex, otherwise include both).
- Prefer preserving failed attempts and anomalies (if they affect interpretation, otherwise keep them as supporting evidence).
- Prefer a milestone-style user update when a meaningful measured result is recorded (if the result is partial or blocked, otherwise name the blocker plainly).

## Constraints

- <MAIN_RUN_RECORD> must not claim completion before durable evidence exists.
- <EXPERIMENT_RESULT_SUMMARY> must not omit comparability, failure mode, or next action.
- <CLAIM_VALIDATION_RECORD> must not map a claim to a missing, non-finite, or non-comparable metric as if it were supported.
- <EXPERIMENT_ROUTE_DECISION> must not be chosen before the result or blocker is recorded.
- A partial or blocked run must be labeled partial or blocked rather than converted into a success story.

## Quality Gates

- Payload completeness: contract, implementation delta, commands, logs, outputs, metrics, seeds, environment facts, changed files, and config paths are present or gaps are recorded.
- Evaluation summary: `takeaway`, `claim_update`, `baseline_relation`, `comparability`, `failure_mode`, and `next_action` are filled.
- Claim traceability: each claim has a metric key, expected direction, observed result, and verdict.
- Comparability: baseline relation is `better`, `worse`, `mixed`, or `not_comparable`, with caveats.
- Failure handling: failed runs identify failure layer, failure type, attempted fix if any, and the next action.
- Handoff quality: later analysis, writing, optimization/frontier review, or decision stages can reconstruct what changed and why.

## Template

Use this structure when a concrete record is needed.

### Outcome Summary

- research question:
- selected hypothesis:
- intervention:
- primary result:
- comparator relation:
- strongest caveat:
- next action:

### Execution Payload

- run id:
- contract reference:
- implementation change map:
- commands:
- logs:
- outputs:
- metrics:
- seeds:
- environment facts:
- changed files:
- config paths:

### Claim Validation

| Claim | Metric Key | Expected Direction | Observed Result | Verdict | Caveat |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

### Evaluation Summary

- takeaway:
- claim_update:
- baseline_relation:
- comparability:
- failure_mode:
- next_action:
