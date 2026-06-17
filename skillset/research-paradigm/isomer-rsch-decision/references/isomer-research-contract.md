# Isomer Research Contract

Use this local reference for terminology, evidence boundaries, runtime boundaries, and TBD placeholders. This skill must be self-contained, so do not load shared files from outside this skill directory while executing it.

## Truth-Source Order

Prefer durable records over recollection:

1. User instruction and explicit Gate decisions through the Operator Agent.
2. Decision Records, Artifacts, Evidence Items, Findings, Research Claims, and Provenance Records.
3. Workspace Runtime state, Run records, handoffs, Signal Observations, and validated View Manifests.
4. Agent Artifacts and Agent Runtime notes that have clear provenance.
5. Conversation context, only when durable state is absent or being interpreted.

## Durable Vocabulary

Use Isomer Labs terms: Research Thread, Research Goal, Research Task, Research Branch, Run, Isomer Workspace, Workspace Runtime, Agent Workspace, Artifact, Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Coordination Policy, Capability Binding, Execution Adapter, Workflow Stage, and Completion Watcher Contract.

## Source-Term Mappings

| Source term or operation | Isomer Labs framing |
| --- | --- |
| lifecycle-level research work | Research Thread |
| bounded unit of research work | Research Task |
| one execution attempt | Run |
| forked research route | Research Branch |
| artifact operation | Artifact, Evidence Item, Decision Record, Gate, Provenance Record, or host API |
| memory operation | Finding, Evidence Item, Artifact, or durable context query |
| command execution | Capability Binding through an Execution Adapter |
| route decision | Decision Record, possibly resolving a Gate |
| user choice on scope, cost, privacy, safety, or finality | Gate through the Operator Agent |

## Rejected Runtime Concepts

Do not port source runtime scheduling terms as Isomer concepts. The Operator Agent is always the human-facing control boundary. Use Workflow Stage recommendations, Gates, Decision Records, observations, or pauses for Operator Agent instruction instead of scheduler fields.

## Evidence Boundaries

Claims and route judgments must be tied to Evidence Items, Findings, Artifacts, Decision Records, or explicit Operator Agent Gates. Negative, partial, null, failed, blocked, infeasible, or contradictory results are evidence and should stay visible.

## Runtime Boundary

This skill describes research judgment. It does not define Isomer runtime APIs, schedulers, storage layouts, credentials, mailbox routes, gateway routes, or concrete agent launch behavior.

## TBD Surface Registry

Use registered TBD placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design.

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| api-gate | api | `[[tbd-surface:api-gate]]` | API for opening, resolving, and recording Gates. |
| schema-decision-record | schema | `[[tbd-surface:schema-decision-record]]` | Decision Record fields and validation. |
| schema-gate | schema | `[[tbd-surface:schema-gate]]` | Gate categories, states, and payload fields. |
| schema-stage-cursor | schema | `[[tbd-surface:schema-stage-cursor]]` | Workflow Stage cursor and next-stage representation. |
| policy-branching | policy | `[[tbd-surface:policy-branching]]` | When a candidate route becomes a Research Branch. |
| policy-baseline-waiver | policy | `[[tbd-surface:policy-baseline-waiver]]` | Baseline acceptance and waiver rules. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |
