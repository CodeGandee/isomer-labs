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
| surface class | figure target surface recorded on an Artifact or Provenance Record |
| paper figure catalog | figure-output Artifact index under `[[tbd-surface:path-figure-output]]` |
| style asset | local asset or Capability Binding selected by the host |
| render-inspect-revise pass | Evidence Item plus Provenance Record for the figure Artifact |
| export schema | existing Artifact, Evidence Item, Provenance Record, and figure-output surfaces until a dedicated schema is accepted |
| plotting execution | Capability Binding through an Execution Adapter |

## Evidence Boundaries

A polished figure can support communication, but it does not create the underlying evidence. Link every figure-level claim to source Evidence Items, Research Claims, or Decision Records. Keep visual limitations, partial evidence, failed renders, and contradictory data visible when they affect interpretation.

## Runtime Boundary

This skill describes figure-polishing judgment. It does not define Isomer storage layouts, command APIs, notebook runtimes, asset registries, or export schemas. Use registered TBD placeholders when concrete surfaces are needed.

## TBD Surface Registry

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| path-figure-output | path | `[[tbd-surface:path-figure-output]]` | Figure source and export layout. |
| api-artifact-record | api | `[[tbd-surface:api-artifact-record]]` | API for recording Artifacts and Provenance Records. |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| schema-evidence-item | schema | `[[tbd-surface:schema-evidence-item]]` | Evidence Item fields and validation. |
| schema-research-claim | schema | `[[tbd-surface:schema-research-claim]]` | Research Claim state and fields. |
