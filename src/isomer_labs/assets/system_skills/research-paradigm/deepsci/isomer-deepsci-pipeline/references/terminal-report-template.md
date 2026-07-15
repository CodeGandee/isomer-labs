# Pipeline Terminal Report Template

Use this template for the durable `DEEPSCI:PIPELINE-TERMINAL-REPORT` artifact produced at the end of every pipeline run. The field tables and YAML example define the stored artifact, not the chat response. After recording the artifact, summarize the pipeline outcome, accepted outputs, blocker or resume point, and recommended next action in natural-language Markdown.

## Required fields

| Field | Type | Description |
| --- | --- | --- |
| `pipeline_id` | string | The recipe name that was executed. |
| `status` | string | One of `complete`, `paused`, `blocked`. |
| `stages_run` | list | One entry per stage that executed, in order. |
| `final_artifact` | string or null | The id of the last produced artifact, when status is `complete`. |
| `recommended_next` | string or null | The next macro action recommended by the last stage, when status is `complete`. |
| `blocker` | object or null | The blocker record, when status is `blocked`. |
| `resume_point` | string or null | Stage id where execution should resume, when status is `paused` or `blocked`. |

## Stage entry fields

Each item in `stages_run` must contain:

| Field | Type | Description |
| --- | --- | --- |
| `stage_id` | string | Stage id from the recipe. |
| `skill` | string | Skill that was invoked. |
| `status` | string | One of `complete`, `paused`, `blocked`, `skipped`. |
| `artifacts_in` | list | Artifact ids consumed by the stage. |
| `artifacts_out` | list | Artifact ids produced by the stage. |
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
    route_decision: baseline
    notes: null
  - stage_id: comparator
    skill: isomer-deepsci-baseline
    status: complete
    artifacts_in: [research-frame]
    artifacts_out: [comparator-contract]
    route_decision: idea
    notes: null
  - stage_id: ideate
    skill: isomer-deepsci-idea
    status: complete
    artifacts_in: [research-frame, comparator-contract]
    artifacts_out: [selected-hypothesis]
    route_decision: experiment
    notes: null
  - stage_id: run
    skill: isomer-deepsci-experiment
    status: complete
    artifacts_in: [selected-hypothesis, comparator-contract]
    artifacts_out: [experiment-result]
    route_decision: analysis
    notes: null
  - stage_id: interpret
    skill: isomer-deepsci-analysis
    status: complete
    artifacts_in: [experiment-result, comparator-contract]
    artifacts_out: [analysis-finding]
    route_decision: decision
    notes: null
final_artifact: analysis-finding
recommended_next: decision
blocker: null
resume_point: null
```
