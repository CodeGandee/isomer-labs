# Isomer Research Contract

Use this local reference for terminology, evidence boundaries, runtime boundaries, and TBD placeholders. This skill must be self-contained, so do not load shared files from outside this skill directory.

## Truth-Source Order

Prefer durable records over recollection:

1. User instruction and explicit Gate decisions through the Operator Agent.
2. Decision Records, Artifacts, Evidence Items, Findings, Research Claims, and Provenance Records.
3. Workspace Runtime state, Run records, handoffs, Signal Observations, and validated View Manifests.
4. Agent Artifacts and Agent Runtime notes that have clear provenance.
5. Conversation context, only when durable state is absent or being interpreted.

## Durable Vocabulary

Use Isomer Labs terms: Research Thread, Research Goal, Research Task, Research Branch, Run, Isomer Workspace, Workspace Runtime, Agent Workspace, Artifact, Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Coordination Policy, Capability Binding, Execution Adapter, Workflow Stage, and Completion Watcher Contract.

Do not invent concrete paths, filenames, storage roots, command surfaces, provider names, schemas, or generated layouts. Use `tbd-surface:<id>` when a skill outcome must mention an unsettled concrete surface.

## Source-Term Mappings

| Source term or operation | Isomer Labs framing |
| --- | --- |
| candidate idea | method brief Artifact or candidate route Artifact |
| durable line | promoted Research Branch |
| implementation attempt | bounded Run, Evidence Item, or implementation-attempt Artifact inside one Research Branch |
| frontier record | View Manifest or frontier Artifact |
| branch promotion | Research Branch decision and Decision Record |
| artifact operation | Artifact, Evidence Item, Decision Record, Gate, Provenance Record, or host API |
| memory operation | Finding, Evidence Item, Artifact, or durable context query |
| command execution | Capability Binding through an Execution Adapter |
| route decision | Decision Record, possibly resolving a Gate |

## Runtime Boundary

This skill describes research judgment. It does not define Isomer runtime APIs, schedulers, storage layouts, credentials, mailbox routes, gateway routes, provider names, or concrete agent launch behavior.

When a source behavior implies execution, storage, state mutation, monitoring, or chart generation, describe the intended Isomer record or capability and mark the concrete surface as unsettled.

## TBD Surface Registry

Use placeholders as `tbd-surface:<id>` in skill outcomes when a concrete surface is not settled by an accepted Isomer design.

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| path-artifact-layout | path | `[[tbd-surface:path-artifact-layout]]` | Artifact directory and naming layout. |
| path-run-logs | path | `[[tbd-surface:path-run-logs]]` | Run log and result file layout. |
| path-experiment-output | path | `[[tbd-surface:path-experiment-output]]` | Experiment output layout. |
| api-artifact-record | api | `[[tbd-surface:api-artifact-record]]` | API for recording Artifacts and Provenance Records. |
| api-finding-query | api | `[[tbd-surface:api-finding-query]]` | API for querying and writing Findings or durable context. |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| schema-decision-record | schema | `[[tbd-surface:schema-decision-record]]` | Decision Record fields and validation. |
| schema-evidence-item | schema | `[[tbd-surface:schema-evidence-item]]` | Evidence Item fields and validation. |
| schema-stage-cursor | schema | `[[tbd-surface:schema-stage-cursor]]` | Workflow Stage cursor and next-stage representation. |
| policy-branching | policy | `[[tbd-surface:policy-branching]]` | When a candidate route becomes a Research Branch. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |
