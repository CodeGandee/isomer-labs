# Pipeline Terminal Report Template

Use this template for the durable `DEEPSCI:PIPELINE-TERMINAL-REPORT` artifact produced at the end of every pipeline run. The field tables and YAML example define the stored artifact, not the chat response. A successful report proves stage and pipeline Operation Set Closeout; plain paths and terminal prose do not count as available artifacts. After recording the artifact, summarize the pipeline outcome, accepted outputs, acceptance receipts or explicit `not_applicable` closeouts, blocker or resume point, and recommended next action in natural-language Markdown.

## Required fields

| Field | Type | Description |
| --- | --- | --- |
| `pipeline_id` | string | The recipe name that was executed. |
| `status` | string | One of `complete`, `paused`, `blocked`. |
| `stages_run` | list | One entry per stage that executed, in order. |
| `accepted_record_refs` | list | Deduplicated durable record refs accepted across completed stages. |
| `pipeline_closeout` | object | Pipeline-level closeout status, receipt id when applicable, durable refs, diagnostics, and resume command. |
| `final_artifact` | string or null | The durable record ref of the last produced artifact, when status is `complete`. |
| `recommended_next` | string or null | The next macro action recommended by the last stage, when status is `complete`. |
| `blocker` | object or null | The blocker record, when status is `blocked`. |
| `resume_point` | string or null | Stage id where execution should resume, when status is `paused` or `blocked`. |

For `paused` prerequisite recovery, record the missing input and known producer in the relevant stage entry, and set `resume_point` to the original target stage. For closeout failure, preserve completed stage refs, the partial receipt when present, deterministic diagnostics, and the exact acceptance resume command. For `blocked`, name the unavailable external state change. The report ends the bounded pass and never invokes its recommendation.

`pipeline_closeout.status` is `complete` when pipeline-level material files have a verified complete receipt, `not_applicable` when the pipeline opened no operation set and created its report directly as a durable record, or `paused` when reconciliation failed. If the terminal report itself is staged as a plain file, its verified receipt belongs to the returned terminal envelope after acceptance; the pipeline cannot report `status: complete` until that evidence exists.

After the report is stored, an explicitly authorized target-scoped run-to controller may validate its refs, invoke the recommended producer as a separate focused-skill or pass Run, refresh latest context, and resume the original target. The controller preserves callbacks, Worker Output Policy, placeholder bindings, quality Gates, and separate terminal reports, and it stops after the target or at a nondelegable boundary.

## Stage entry fields

Each item in `stages_run` must contain:

| Field | Type | Description |
| --- | --- | --- |
| `stage_id` | string | Stage id from the recipe. |
| `skill` | string | Skill that was invoked. |
| `status` | string | One of `complete`, `paused`, `blocked`, `skipped`. |
| `artifacts_in` | list | Artifact ids consumed by the stage. |
| `artifacts_out` | list | Artifact ids produced by the stage. |
| `durable_refs` | list | Queryable durable record refs produced or used by the stage and available for handoff. |
| `closeout` | string | One of `complete`, `not_applicable`, `paused`. |
| `acceptance_receipt_id` | string or null | Verified complete or partial receipt id; null only for `not_applicable`. |
| `closeout_diagnostics` | list | Empty after successful closeout; deterministic diagnostics when paused. |
| `closeout_resume_command` | string or null | Exact acceptance or verification command needed to resume a paused closeout. |
| `route_decision` | string or null | The stage's route decision, if any. |
| `notes` | string or null | Brief note, e.g., pause reason or blocker summary. |

## Example

```yaml
pipeline_id: empirical-pass
status: complete
stages_run:
  - stage_id: frame
    skill: isomer-deepsci-scout
    status: complete
    artifacts_in: []
    artifacts_out: [research-frame]
    durable_refs: [artifact-DEEPSCI-RESEARCH-FRAME-a1b2c3d4e5f6]
    closeout: complete
    acceptance_receipt_id: operation-set-acceptance-frame-r1-111111111111
    closeout_diagnostics: []
    closeout_resume_command: null
    route_decision: baseline
    notes: null
  - stage_id: comparator
    skill: isomer-deepsci-baseline
    status: complete
    artifacts_in: [research-frame]
    artifacts_out: [comparator-contract]
    durable_refs: [artifact-DEEPSCI-COMPARATOR-CONTRACT-b1c2d3e4f5a6]
    closeout: complete
    acceptance_receipt_id: operation-set-acceptance-comparator-r1-222222222222
    closeout_diagnostics: []
    closeout_resume_command: null
    route_decision: idea
    notes: null
  - stage_id: ideate
    skill: isomer-deepsci-idea
    status: complete
    artifacts_in: [research-frame, comparator-contract]
    artifacts_out: [selected-hypothesis]
    durable_refs: [artifact-DEEPSCI-SELECTED-HYPOTHESIS-c1d2e3f4a5b6]
    closeout: complete
    acceptance_receipt_id: operation-set-acceptance-ideate-r1-333333333333
    closeout_diagnostics: []
    closeout_resume_command: null
    route_decision: experiment
    notes: null
  - stage_id: run
    skill: isomer-deepsci-experiment
    status: complete
    artifacts_in: [selected-hypothesis, comparator-contract]
    artifacts_out: [experiment-result]
    durable_refs: [evidence_item-DEEPSCI-EXPERIMENT-RESULT-d1e2f3a4b5c6]
    closeout: complete
    acceptance_receipt_id: operation-set-acceptance-run-r1-444444444444
    closeout_diagnostics: []
    closeout_resume_command: null
    route_decision: analysis
    notes: null
  - stage_id: interpret
    skill: isomer-deepsci-analysis
    status: complete
    artifacts_in: [experiment-result, comparator-contract]
    artifacts_out: [analysis-finding]
    durable_refs: [artifact-DEEPSCI-ANALYSIS-FINDING-e1f2a3b4c5d6]
    closeout: complete
    acceptance_receipt_id: operation-set-acceptance-interpret-r1-555555555555
    closeout_diagnostics: []
    closeout_resume_command: null
    route_decision: decision
    notes: null
accepted_record_refs:
  - artifact-DEEPSCI-RESEARCH-FRAME-a1b2c3d4e5f6
  - artifact-DEEPSCI-COMPARATOR-CONTRACT-b1c2d3e4f5a6
  - artifact-DEEPSCI-SELECTED-HYPOTHESIS-c1d2e3f4a5b6
  - evidence_item-DEEPSCI-EXPERIMENT-RESULT-d1e2f3a4b5c6
  - artifact-DEEPSCI-ANALYSIS-FINDING-e1f2a3b4c5d6
pipeline_closeout:
  status: not_applicable
  receipt_id: null
  durable_refs: [artifact-DEEPSCI-PIPELINE-TERMINAL-REPORT-f1a2b3c4d5e6]
  diagnostics: []
  resume_command: null
final_artifact: artifact-DEEPSCI-ANALYSIS-FINDING-e1f2a3b4c5d6
recommended_next: decision
blocker: null
resume_point: null
```
