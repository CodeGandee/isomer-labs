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

Use Isomer Labs terms: Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Topic Workspace, Workspace Runtime, Agent Workspace, Agent Runtime, Workspace Boundary, Artifact, Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Agent Team Instance lifecycle state, Coordination Policy, Capability Binding, Execution Adapter, Workflow Stage, Workflow Stage Cursor, and Completion Watcher Contract.


## Workspace Path Resolution

Ordinary Project, Topic Workspace, Workspace Runtime, task support, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are resolved surfaces. Ask for semantic targets such as Topic Workspace, Workspace Runtime, task support directory, run log Artifact, experiment output Artifact, analysis output Artifact, figure output Artifact, paper Artifact, decision Artifact, evidence Artifact, finding Artifact, handoff Artifact, Agent Workspace scratch, Agent Runtime state, or Agent Artifact.

Do not emit ordinary path TBD placeholders for these surfaces. Workspace plans have precedence, then supported Execution Adapter `ISOMER_*` environment variables, then Project Manifest defaults, then built-in defaults. Environment variables are launch-time adapter inputs, not durable truth; resolved effective paths and their source belong in Workspace Runtime or Provenance Records.

## Research Recording Contracts

Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are resolved durable record surfaces. Use accepted recording APIs for Artifact and Provenance recording, Finding query/write, and Gate open/resolve/record behavior.

Do not emit recording TBD placeholders for these surfaces. Evidence Items are the support, contradiction, or context boundary for Research Claims. Research Claim status is `open`, `supported`, `refuted`, or `withdrawn` unless a later accepted contract extends it; contradiction and context belong on Evidence Items or claim-evidence links. Findings are primarily scoped to Research Inquiries when an applicable inquiry exists. A Gate may resolve through a Decision Record, but cancelled or superseded Gates can close with a Provenance Record when no meaningful choice was made.

## Research Lifecycle State

Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Workflow Stage Cursor, and Agent Team Instance lifecycle state are resolved lifecycle surfaces. Use Workflow Stage Cursor for durable routing state, not scheduling. Use Agent Team Instance lifecycle state for planned, active, paused, blocked, completed, stopped, or archived team execution state; optional active or relevant Research Inquiry refs are context and routing anchors, not execution scope. Use Research Inquiry Relationships for inquiry graph links and require Decision Records only when a meaningful route choice was made.

Do not emit lifecycle TBD placeholders for `schema-stage-cursor`, `schema-agent-team-state`, or `policy-branching`. Research Inquiry is a question object and not a parallel execution scope. Express parallel work only as Topic-level parallelism across Agent Team Instances or Task-level parallelism across Agent Instances inside one Agent Team Instance.

## Source-Term Mappings

| Source term or operation | Isomer Labs framing |
| --- | --- |
| lifecycle-level research work | Research Topic, Research Inquiry, or Research Task depending on scope |
| Research Goal | Research Topic; put metrics or targets in optional Measurable Objectives |
| Research Thread | Research Inquiry |
| Research Branch | Research Inquiry Relationship; do not imply a tree or branch collection |
| Isomer Workspace | Topic Workspace through Workspace Path Resolution |
| bounded unit of research work | Research Task |
| one execution attempt | Run |
| forked research route | Research Inquiry Relationship plus Decision Record when a choice is made |
| artifact operation | Artifact, Evidence Item, Decision Record, Gate, Provenance Record, or host API |
| memory operation | Finding, Evidence Item, Artifact, or durable context query |
| command execution | Capability Binding through an Execution Adapter |
| paper lookup | literature search capability; provider is unsettled |
| route decision | Decision Record, possibly resolving a Gate |
| user choice on scope, cost, privacy, safety, or finality | Gate through the Operator Agent |

## Rejected Runtime Concepts

Do not port source runtime scheduling terms as Isomer concepts. The Operator Agent is always the human-facing control boundary. Use Workflow Stage Cursor recommendations, Gates, Decision Records, observations, or pauses for Operator Agent instruction instead of scheduler fields.

## Evidence Boundaries

Claims must be tied to Evidence Items. Negative, partial, null, failed, blocked, infeasible, or contradictory results are evidence and should stay visible. Finalization is invalid if it hides failed lines, drops caveats, or turns missing evidence into completion language.

## Runtime Boundary

This skill describes research judgment. It does not define Isomer runtime APIs, schedulers, ordinary path layouts covered by Workspace Path Resolution, credentials, mailbox routes, gateway routes, graph exporters, or concrete agent launch behavior.

## TBD Surface Registry

Use registered TBD-surface placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design. Ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are settled by Workspace Path Resolution. Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are settled by Research Recording Contracts. Research Topics, Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, Workflow Stage Cursors, and Agent Team Instance lifecycle state are settled by Research Lifecycle State. Skills should name semantic workspace scopes, Artifact kinds, durable record types, accepted recording APIs, or accepted lifecycle objects instead of emitting TBD placeholders for resolved surfaces.

### Resolved Workspace Path Surfaces

These former path TBDs are mapped to Workspace Path Resolution and must not be emitted as path-prefixed TBD placeholders in research-stage skill text.

| Former ID | Resolution |
| --- | --- |
| path-isomer-workspace | Legacy name for Topic Workspace; use Topic Workspace through Workspace Path Resolution. |
| path-topic-workspace | Use Topic Workspace through Workspace Path Resolution. |
| path-workspace-runtime | Use Workspace Runtime through Workspace Path Resolution. |
| path-agent-workspace | Use Agent Workspace or Agent Runtime through Workspace Path Resolution. |
| path-artifact-layout | Use semantic Artifact kinds through Workspace Path Resolution. |
| path-run-logs | Use Run log Artifact or Run log scope through Workspace Path Resolution. |
| path-experiment-output | Use experiment output Artifact through Workspace Path Resolution. |
| path-analysis-output | Use analysis output Artifact through Workspace Path Resolution. |
| path-paper-layout | Use paper Artifact through Workspace Path Resolution. |
| path-figure-output | Use figure output Artifact through Workspace Path Resolution. |

### Resolved Research Recording Surfaces

These former recording TBDs are mapped to Research Recording Contracts and must not be emitted as open TBD placeholders in research-stage skill text.

| Former ID | Resolution |
| --- | --- |
| api-artifact-record | Use the accepted Artifact and Provenance recording API through Research Recording Contracts. |
| api-finding-query | Use the accepted Finding query/write API through Research Recording Contracts. |
| api-gate | Use the accepted Gate open, resolve, and record API through Research Recording Contracts. |
| schema-decision-record | Use the accepted Decision Record fields and validation from Research Recording Contracts. |
| schema-evidence-item | Use the accepted Evidence Item fields and validation from Research Recording Contracts. |
| schema-research-claim | Use the accepted Research Claim status, evidence-link, and validation rules from Research Recording Contracts. |
| schema-gate | Use the accepted Gate status and validation rules from Research Recording Contracts. |

### Resolved Research Lifecycle Surfaces

These former lifecycle TBDs are mapped to Research Lifecycle State and must not be emitted as open TBD placeholders in research-stage skill text.

| Former ID | Resolution |
| --- | --- |
| schema-stage-cursor | Use Workflow Stage Cursor as durable routing state through Research Lifecycle State. |
| schema-agent-team-state | Use Agent Team Instance lifecycle state through Research Lifecycle State. |
| policy-branching | Use Research Inquiry Relationship policy through Research Lifecycle State; create Decision Records only for meaningful route choices. |

### Open TBD Surfaces

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| provider-literature-search | provider | `[[tbd-surface:provider-literature-search]]` | Literature search and paper-reading provider. |
| schema-skill-binding | schema | `[[tbd-surface:schema-skill-binding]]` | Capability Binding projection and skill install schema. |
| policy-scheduler | policy | `[[tbd-surface:policy-scheduler]]` | Runtime scheduling and continuation policy. |
| policy-baseline-waiver | policy | `[[tbd-surface:policy-baseline-waiver]]` | Baseline acceptance and waiver rules. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |
