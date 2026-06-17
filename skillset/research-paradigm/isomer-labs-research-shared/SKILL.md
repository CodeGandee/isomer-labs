---
name: isomer-labs-research-shared
description: Shared research contract for Isomer Labs research-stage skills, including evidence, handoff, terminology, provenance, and unsettled-surface rules.
---

Use this shared skill whenever an Isomer Labs research-stage skill needs common
rules for evidence, Artifacts, handoffs, decisions, provenance, or unsettled
platform surfaces.

Read these references when relevant:

- `references/source-term-mapping.md` for source-term mappings and rejected
  runtime concepts.
- `references/tbd-surface-registry.md` for registered placeholders for
  unsettled concrete paths, APIs, schemas, providers, commands, and policies.

## Truth-Source Order

Prefer durable records over recollection:

1. User instruction and explicit Gate decisions through the Operator Agent.
2. Decision Records, Artifacts, Evidence Items, Findings, Research Claims, and
   Provenance Records.
3. Workspace Runtime state, Run records, handoffs, Signal Observations, and
   validated View Manifests.
4. Agent Artifacts and Agent Runtime notes that have clear provenance.
5. Conversation context, only when durable state is absent or being interpreted.

## Durable Vocabulary

Use Isomer Labs terms: Research Thread, Research Goal, Research Task, Research
Branch, Run, Isomer Workspace, Workspace Runtime, Agent Workspace, Artifact,
Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate,
Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent
Instance, Agent Team Instance, Coordination Policy, Capability Binding,
Execution Adapter, Workflow Stage, and Completion Watcher Contract.

Do not invent concrete paths, filenames, storage roots, command surfaces,
provider names, schemas, or generated layouts. Use
`[[tbd-surface:<id>]]` from `references/tbd-surface-registry.md` when a skill
outcome must mention an unsettled concrete surface.

## Handoff Contract

Every stage or companion handoff should state:

- Current Research Task or Research Branch scope.
- Inputs and durable sources inspected.
- Outputs produced or updated.
- Evidence Items and Research Claims affected.
- Decision Records or Gates opened or resolved.
- Next recommended Workflow Stage, pause, or blocker.
- Known caveats, missing evidence, and unsettled surfaces.

## Evidence Boundaries

Claims must be tied to Evidence Items. Negative, partial, null, failed, or
contradictory results are evidence and should stay visible. Do not turn a
plausible route into a supported Research Claim without a durable Artifact,
measurement, source document, or validation result.

## Runtime Boundary

Research-paradigm skills describe research judgment. They do not define Isomer
runtime APIs, schedulers, storage layouts, credentials, mailbox routes, gateway
routes, or concrete agent launch behavior.

When a source behavior implies execution, literature lookup, storage, or
state mutation, describe the intended Isomer record or capability and mark the
concrete surface as unsettled.

