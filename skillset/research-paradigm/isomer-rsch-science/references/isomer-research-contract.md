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

Use Isomer Labs terms: Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Research Topic Config, Effective Topic Context, Topic Workspace, Workspace Runtime, Agent Workspace, Agent Runtime, Workspace Boundary, Artifact, Artifact Core Record, Artifact Format Profile, Artifact Extension, Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Agent Team Instance lifecycle state, Coordination Policy, Capability Binding, Execution Adapter, Workflow Stage, Workflow Stage Cursor, and Completion Watcher Contract.


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

This skill describes scientific research judgment. It does not define Isomer runtime APIs, schedulers, ordinary path layouts covered by Workspace Path Resolution, credentials, SSH profiles, queue profiles, package managers, solver installation, or concrete agent launch behavior.

## TBD Surface Registry

Use registered TBD-surface placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design. Ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are settled by Workspace Path Resolution. `isomer-cli` topic selection and topic-specific CLI context are settled as Effective Topic Context by CLI Topic Context Resolution, and Artifact Core Records, Artifact Format Profiles, and Artifact Extensions are settled as generic recording metadata by Research Recording Contracts. Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are settled by Research Recording Contracts. Research Topics, Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, Workflow Stage Cursors, and Agent Team Instance lifecycle state are settled by Research Lifecycle State. Skills should name semantic workspace scopes, Artifact kinds, durable record types, accepted recording APIs, accepted lifecycle objects, or Effective Topic Context instead of emitting TBD placeholders for resolved surfaces.

Effective Topic Context and artifact format customization do not settle execution commands, scheduler policy, Skill Binding projection, credential binding, literature providers, baseline-waiver policy, cost/privacy Gate thresholds, or validation/render/export command behavior. Use the open placeholders below for those concrete surfaces until an accepted design resolves them.

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
