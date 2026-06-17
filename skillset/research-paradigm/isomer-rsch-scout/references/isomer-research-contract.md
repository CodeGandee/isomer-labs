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
| artifact operation | Artifact, Evidence Item, Decision Record, Gate, Provenance Record, or host API |
| memory operation | Finding, Evidence Item, Artifact, or durable context query |
| command execution | Capability Binding through an Execution Adapter |
| paper lookup | literature search capability; provider is unsettled |
| route decision | Decision Record, possibly resolving a Gate |
| user choice on scope, cost, privacy, safety, or finality | Gate through the Operator Agent |

## Rejected Runtime Concepts

Do not port source runtime scheduling terms as Isomer concepts. The Operator Agent is always the human-facing control boundary. Use Workflow Stage recommendations, Gates, Decision Records, observations, or pauses for Operator Agent instruction instead of scheduler fields.

## Evidence Boundaries

Claims must be tied to Evidence Items. Negative, partial, null, failed, blocked, infeasible, or contradictory results are evidence and should stay visible. Scout may justify a route, but it must not convert a plausible paper neighborhood into a supported Research Claim without durable evidence.

## Runtime Boundary

This skill describes research judgment. It does not define Isomer runtime APIs, schedulers, storage layouts, credentials, mailbox routes, gateway routes, paper-search providers, or concrete agent launch behavior.

## TBD Surface Registry

Use registered TBD placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design.

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| api-finding-query | api | `[[tbd-surface:api-finding-query]]` | API for querying and writing Findings or durable context. |
| provider-literature-search | provider | `[[tbd-surface:provider-literature-search]]` | Literature search and paper-reading provider. |
| schema-decision-record | schema | `[[tbd-surface:schema-decision-record]]` | Decision Record fields and validation. |
| schema-evidence-item | schema | `[[tbd-surface:schema-evidence-item]]` | Evidence Item fields and validation. |
| schema-stage-cursor | schema | `[[tbd-surface:schema-stage-cursor]]` | Workflow Stage cursor and next-stage representation. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |
