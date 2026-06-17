# Isomer Research Contract

Use this local reference for terminology, evidence boundaries, runtime boundaries, and TBD placeholders. This skill must be self-contained, so do not load source-tree files, source-analysis notes, or external package-card directories to execute it.

## Truth-Source Order

Prefer durable records over recollection:

1. User instruction and explicit Gate decisions through the Operator Agent.
2. Decision Records, Artifacts, Evidence Items, Findings, Research Claims, and Provenance Records.
3. Workspace Runtime state, Run records, handoffs, Signal Observations, and validated View Manifests.
4. Agent Artifacts and Agent Runtime notes that have clear provenance.
5. Conversation context, only when durable state is absent or being interpreted.

## Durable Vocabulary

Use Isomer Labs terms: Research Thread, Research Task, Research Branch, Run, Isomer Workspace, Workspace Runtime, Agent Workspace, Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Capability Binding, Execution Adapter, Workflow Stage, and Completion Watcher Contract.

## Source-Term Mappings

| Source term or operation | Isomer Labs framing |
| --- | --- |
| Science Evidence Graph | linked Evidence Items, Artifacts, Research Claims, Validation Evidence Items, and Provenance Records |
| science node | durable Evidence Item, Run record, Research Claim, Decision Record, or Provenance Record |
| package card | routing reference that does not prove local availability |
| command wrapper | Capability Binding through an Execution Adapter |
| HPC through shell | SSH, scheduler, queue, and log work through an Execution Adapter |
| package catalog | optional local reference asset or deferred Capability Binding, not a runtime dependency |
| startup brief | science-task brief Artifact or handoff note |

## Evidence Boundaries

Claims must be tied to Evidence Items. Negative, partial, null, failed, blocked, infeasible, and contradictory scientific results are evidence and should stay visible. Do not turn a plausible route into a supported Research Claim without durable input, execution, output, validation, source document, or diagnostic evidence.

## Runtime Boundary

This skill describes scientific research judgment. It does not define Isomer runtime APIs, schedulers, storage layouts, credentials, SSH profiles, queue profiles, package managers, solver installation, or concrete agent launch behavior.

## TBD Surface Registry

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| path-isomer-workspace | path | `[[tbd-surface:path-isomer-workspace]]` | Concrete Isomer Workspace path convention. |
| path-run-logs | path | `[[tbd-surface:path-run-logs]]` | Run log and result file layout. |
| path-experiment-output | path | `[[tbd-surface:path-experiment-output]]` | Experiment output layout. |
| api-artifact-record | api | `[[tbd-surface:api-artifact-record]]` | API for recording Artifacts and Provenance Records. |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| api-gate | api | `[[tbd-surface:api-gate]]` | API for opening, resolving, and recording Gates. |
| schema-evidence-item | schema | `[[tbd-surface:schema-evidence-item]]` | Evidence Item fields and validation. |
| schema-research-claim | schema | `[[tbd-surface:schema-research-claim]]` | Research Claim state and fields. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |
