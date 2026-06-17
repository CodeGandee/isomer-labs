# Isomer Research Contract

Use this local reference for terminology, evidence boundaries, runtime boundaries, and TBD placeholders. This skill must be self-contained, so do not load source-tree files or source-analysis notes to execute it.

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
| plotting workspace | figure-generation Artifact under `[[tbd-surface:path-figure-output]]` |
| paper figure source data | Source data Artifact or linked Evidence Item |
| bundled style script | local style reference plus task-local figure-generation Artifact |
| rendered output | Figure Artifact and Evidence Item |
| template copy | Artifact derivation recorded with a Provenance Record |
| script execution | Capability Binding through an Execution Adapter |
| final export schema | existing Artifact, Evidence Item, Provenance Record, and figure-output surfaces until a dedicated schema is accepted |

## Evidence Boundaries

Figure claims must be tied to Evidence Items. A plot can make a comparison easier to see, but it does not create evidence by itself. Keep null, negative, partial, failed, blocked, infeasible, and contradictory data visible when those records affect the figure.

## Runtime Boundary

This skill describes figure-generation judgment. It does not define Isomer storage layouts, command APIs, notebook runtimes, asset registries, or chart export schemas. When concrete output paths or execution commands are needed, use the placeholders below.

## TBD Surface Registry

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| path-figure-output | path | `[[tbd-surface:path-figure-output]]` | Figure source and export layout. |
| api-artifact-record | api | `[[tbd-surface:api-artifact-record]]` | API for recording Artifacts and Provenance Records. |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| schema-evidence-item | schema | `[[tbd-surface:schema-evidence-item]]` | Evidence Item fields and validation. |
