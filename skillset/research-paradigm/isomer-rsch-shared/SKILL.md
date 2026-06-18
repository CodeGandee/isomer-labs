---
name: isomer-rsch-shared
description: Shared research contract for Isomer Labs research-stage skills, including evidence, handoff, terminology, provenance, and unsettled-surface rules.
---

# Isomer Research Shared

## Overview

Use this shared skill whenever an Isomer Labs research-stage skill needs common rules for evidence, Artifacts, handoffs, decisions, provenance, recording, or unsettled platform surfaces.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load shared references** from **Reference Routing** when source-term mapping, rejected runtime concepts, or TBD-surface registration matters.
2. **Apply truth-source order** before making, routing, or revising claims.
3. **Use durable vocabulary** for Research Topics, Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, Research Topic Configs, Effective Topic Context, Workflow Stage Cursors, Agent Team Instance lifecycle state, Artifacts, Artifact Core Records, Artifact Format Profiles, Artifact Extensions, Evidence Items, Findings, Research Claims, Decision Records, Gates, Provenance Records, Capability Bindings, Execution Adapters, and Workflow Stages.
4. **Map source-runtime concepts** through `references/source-term-mapping.md` instead of importing source APIs, schedulers, command wrappers, provider names, or concrete paths covered by Workspace Path Resolution.
5. **Use accepted recording contracts** for Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates.
6. **Mark unsettled concrete surfaces** with ids from `references/tbd-surface-registry.md` only when the surface is not settled by an accepted Isomer contract.
7. **Write handoffs with durable evidence boundaries**, including affected Evidence Items, Research Claims, Decision Records, Gates, next Workflow Stage Cursor, blocker, caveats, and unsettled surfaces.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read references as needed:

- `references/source-term-mapping.md` for source-term mappings and rejected runtime concepts.
- `references/tbd-surface-registry.md` for registered placeholders for unsettled APIs, schemas, providers, commands, policies, and any concrete path surface outside Workspace Path Resolution.

## Truth-Source Order

Prefer durable records over recollection:

1. User instruction and explicit Gate decisions through the Operator Agent.
2. Decision Records, Artifacts, Evidence Items, Findings, Research Claims, and Provenance Records.
3. Workspace Runtime state, Run records, handoffs, Signal Observations, and validated View Manifests.
4. Agent Artifacts and Agent Runtime notes that have clear provenance.
5. Conversation context, only when durable state is absent or being interpreted.

## Durable Vocabulary

Use Isomer Labs terms: Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Research Topic Config, Effective Topic Context, Topic Workspace, Workspace Runtime, Agent Workspace, Agent Runtime, Workspace Boundary, Artifact, Artifact Core Record, Artifact Format Profile, Artifact Extension, Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Agent Team Instance lifecycle state, Coordination Policy, Capability Binding, Execution Adapter, Workflow Stage, Workflow Stage Cursor, and Completion Watcher Contract.

Do not invent concrete paths, filenames, storage roots, command surfaces, provider names, schemas, or generated layouts. Use a registered TBD-surface placeholder from `references/tbd-surface-registry.md` when a skill outcome must mention an unsettled concrete surface.

## Workspace Path Resolution

Ordinary Project, Topic Workspace, Workspace Runtime, task support, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are resolved surfaces. Ask for semantic targets such as Topic Workspace, Workspace Runtime, task support directory, run log Artifact, experiment output Artifact, analysis output Artifact, figure output Artifact, paper Artifact, decision Artifact, evidence Artifact, finding Artifact, handoff Artifact, Agent Workspace scratch, Agent Runtime state, or Agent Artifact.

Do not emit ordinary path TBD placeholders for these surfaces. For topic-scoped CLI behavior, `isomer-cli` first resolves Effective Topic Context and then passes the selected Research Topic, Topic Workspace, optional Research Inquiry, Research Task, Run, Agent Team Instance, and Agent Instance refs into Workspace Path Resolution. Workspace plans have precedence, then supported Execution Adapter `ISOMER_*` path environment variables, then Project Manifest defaults, then built-in defaults. Environment variables are launch-time adapter inputs, not durable truth; resolved effective paths and their source belong in Workspace Runtime or Provenance Records.

## CLI Topic Context Resolution

When an `isomer-cli` command needs topic-specific behavior, skills may name Effective Topic Context instead of inventing command-specific lookup rules. Effective Topic Context is the resolved CLI view of the selected Project, Research Topic, Research Topic Config, Topic Workspace, optional lifecycle refs, Topic Agent Team Profile default, Execution Adapter refs, Capability Binding refs, Gate policy refs, Artifact Format Profile refs, Artifact Extension refs, and source metadata.

Use only these topic-context identity environment refs when examples must show launch-time topic selection or disambiguation: `ISOMER_RESEARCH_TOPIC_ID`, `ISOMER_TOPIC_WORKSPACE_ID`, `ISOMER_RESEARCH_INQUIRY_ID`, `ISOMER_RESEARCH_TASK_ID`, `ISOMER_RUN_ID`, `ISOMER_AGENT_TEAM_INSTANCE_ID`, and `ISOMER_AGENT_INSTANCE_ID`. These refs do not define command execution, credentials, scheduling, or durable state; durable refs and source metadata belong in Workspace Runtime, Provenance Records, or the applicable lifecycle and recording records.

## Research Recording Contracts

Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are resolved durable record surfaces. Use accepted recording APIs for Artifact and Provenance recording, Finding query/write, and Gate open/resolve/record behavior.

Do not emit recording TBD placeholders for these surfaces. Artifact Core Records are generic and minimal; topic-specific output expectations attach through optional Artifact Format Profile refs and Artifact Extension refs, not mandatory core fields. Unknown or missing profiles and extensions degrade to generic Artifact handling. Evidence Items are the support, contradiction, or context boundary for Research Claims. Research Claim status is `open`, `supported`, `refuted`, or `withdrawn` unless a later accepted contract extends it; contradiction and context belong on Evidence Items or claim-evidence links. Findings are primarily scoped to Research Inquiries when an applicable inquiry exists. A Gate may resolve through a Decision Record, but cancelled or superseded Gates can close with a Provenance Record when no meaningful choice was made.

## Research Lifecycle State

Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Workflow Stage Cursor, and Agent Team Instance lifecycle state are resolved lifecycle surfaces. Use Workflow Stage Cursor for durable routing state, not scheduling. Use Agent Team Instance lifecycle state for planned, active, paused, blocked, completed, stopped, or archived team execution state; optional active or relevant Research Inquiry refs are context and routing anchors, not execution scope. Use Research Inquiry Relationships for inquiry graph links and require Decision Records only when a meaningful route choice was made.

Do not emit lifecycle TBD placeholders for `schema-stage-cursor`, `schema-agent-team-state`, or `policy-branching`. Research Inquiry is a question object and not a parallel execution scope. Express parallel work only as Topic-level parallelism across Agent Team Instances or Task-level parallelism across Agent Instances inside one Agent Team Instance.

## Handoff Contract

Every stage or companion handoff should state:

- Current Research Topic, Research Inquiry, or Research Task scope.
- Inputs and durable sources inspected.
- Outputs produced or updated.
- Evidence Items and Research Claims affected.
- Decision Records or Gates opened or resolved.
- Next recommended Workflow Stage Cursor, pause, or blocker.
- Known caveats, missing evidence, and unsettled surfaces.

## Evidence Boundaries

Claims must be tied to Evidence Items. Negative, partial, null, failed, or contradictory results are evidence and should stay visible. Do not turn a plausible route into a supported Research Claim without a durable Artifact, measurement, source document, or validation result.

## Runtime Boundary

Research-paradigm skills describe research judgment. They do not define Isomer runtime APIs, schedulers, credentials, mailbox routes, gateway routes, concrete agent launch behavior, validation/render/export commands, or ordinary path layouts covered by Workspace Path Resolution.

When a source behavior implies execution, literature lookup, storage, lifecycle state, route branching, or state mutation, describe the intended Isomer lifecycle object, durable record, semantic Artifact kind, workspace scope, or capability. Mark the concrete surface as unsettled only when it is outside accepted Isomer contracts.
