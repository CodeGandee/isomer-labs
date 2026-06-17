# TBD Surface Registry

Use placeholders as `[[tbd-surface:<id>]]` in skill outcomes when a concrete
surface is not settled by an accepted Isomer design.

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| path-isomer-workspace | path | `[[tbd-surface:path-isomer-workspace]]` | Concrete Isomer Workspace path convention. |
| path-workspace-runtime | path | `[[tbd-surface:path-workspace-runtime]]` | Concrete Workspace Runtime storage layout. |
| path-agent-workspace | path | `[[tbd-surface:path-agent-workspace]]` | Concrete Agent Workspace layout. |
| path-artifact-layout | path | `[[tbd-surface:path-artifact-layout]]` | Artifact directory and naming layout. |
| path-run-logs | path | `[[tbd-surface:path-run-logs]]` | Run log and result file layout. |
| path-experiment-output | path | `[[tbd-surface:path-experiment-output]]` | Experiment output layout. |
| path-analysis-output | path | `[[tbd-surface:path-analysis-output]]` | Analysis output layout. |
| path-paper-layout | path | `[[tbd-surface:path-paper-layout]]` | Report or manuscript layout. |
| path-figure-output | path | `[[tbd-surface:path-figure-output]]` | Figure source and export layout. |
| api-artifact-record | api | `[[tbd-surface:api-artifact-record]]` | API for recording Artifacts and Provenance Records. |
| api-finding-query | api | `[[tbd-surface:api-finding-query]]` | API for querying and writing Findings or durable context. |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| api-gate | api | `[[tbd-surface:api-gate]]` | API for opening, resolving, and recording Gates. |
| provider-literature-search | provider | `[[tbd-surface:provider-literature-search]]` | Literature search and paper-reading provider. |
| schema-decision-record | schema | `[[tbd-surface:schema-decision-record]]` | Decision Record fields and validation. |
| schema-evidence-item | schema | `[[tbd-surface:schema-evidence-item]]` | Evidence Item fields and validation. |
| schema-research-claim | schema | `[[tbd-surface:schema-research-claim]]` | Research Claim state and fields. |
| schema-gate | schema | `[[tbd-surface:schema-gate]]` | Gate categories, states, and payload fields. |
| schema-stage-cursor | schema | `[[tbd-surface:schema-stage-cursor]]` | Workflow Stage cursor and next-stage representation. |
| schema-agent-team-state | schema | `[[tbd-surface:schema-agent-team-state]]` | Agent Team Instance pause and advancement states. |
| schema-skill-binding | schema | `[[tbd-surface:schema-skill-binding]]` | Capability Binding projection and skill install schema. |
| policy-scheduler | policy | `[[tbd-surface:policy-scheduler]]` | Runtime scheduling and continuation policy. |
| policy-branching | policy | `[[tbd-surface:policy-branching]]` | When a candidate route becomes a Research Branch. |
| policy-baseline-waiver | policy | `[[tbd-surface:policy-baseline-waiver]]` | Baseline acceptance and waiver rules. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |

