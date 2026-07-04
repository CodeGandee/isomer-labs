# Pipeline Placeholders

This page defines the control-surface objects that `isomer-deepsci-pipeline` produces or consumes. The pipeline skill does not introduce new research objects; it orchestrates the existing objects defined in `isomer-deepsci-shared/references/semantic-placeholders.md`.

| Semantic id | Meaning | Required semantic content | Typical producers | Typical consumers |
| --- | --- | --- | --- | --- |
| `pipeline-recipe-context` | Initial context provided by the caller | Pipeline name, optional starting stage, input artifacts, parameters, budget or checkpoint preferences | External controller | `isomer-deepsci-pipeline` |
| `pipeline-terminal-report` | End-of-run summary for external controllers | Pipeline id, status, completed stages, produced artifacts, final artifact, recommended next action, blocker or pause reason, resume point | `isomer-deepsci-pipeline` | External controller, `isomer-deepsci-decision`, user |
| `pipeline-run-record` | Audit log of one pipeline invocation | Recipe id, stage sequence, stage results, artifact handoffs, transition decisions, pause/block events | `isomer-deepsci-pipeline` | External controller, future resume logic |
| `pipeline-resume-packet` | Resume context for a paused pipeline | Pipeline id, last completed stage, current stage, pending stages, available artifacts, blocker or pause reason | `isomer-deepsci-pipeline` | External controller, future `isomer-deepsci-pipeline` resume |
