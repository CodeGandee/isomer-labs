# Provenance

This skill adapts the DeepScientist `baseline` research method and reference material into a self-contained Isomer Labs skill.

The adaptation preserves reusable methodology: route selection, comparator-first acceptance, metric-contract fields, verification gates, evidence-flow examples, route records, gate checklists, payload shapes, boundary cases, codebase audit checks, operational guidance, blocked classes, and stopping rules.

Source-runtime concepts were intentionally translated:

- quest lifecycle language became Research Thread, Research Task, Research Branch, Run, and Workflow Stage language.
- artifact operations such as `artifact.confirm_baseline(...)`, `artifact.waive_baseline(...)`, package attachment, package import, and package publication became Artifacts, Evidence Items, Decision Records, Gates, Provenance Records, host Artifact APIs, or reusable Artifact packages.
- memory operations became Findings, Evidence Items, Artifacts, or durable context queries.
- command execution and source tool wrappers became Capability Binding through an Execution Adapter.
- source worktree and workspace assumptions became Isomer Workspace, Workspace Runtime, Agent Workspace, or TBD placeholders.
- concrete metric-contract paths became metric-contract Artifacts plus `[[tbd-surface:path-artifact-layout]]` or `[[tbd-surface:schema-evidence-item]]` when a concrete surface must be named.
- source package-manager, container, and service-endpoint tactics became Execution Adapter choices or Capability Bindings, not required Isomer skill behavior.
- source scheduler and continuation terms became Workflow Stage recommendations, Gates, Decision Records, observations, or pauses for Operator Agent instruction.

License context: the source project is licensed under Apache 2.0. Preserve this notice near this self-contained adaptation when copying, distributing, or materially revising the skill.
