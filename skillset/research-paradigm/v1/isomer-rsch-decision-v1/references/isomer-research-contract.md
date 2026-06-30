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

Use Isomer Labs terms: Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Research Topic Config, Effective Topic Context, Topic Workspace, Workspace Runtime, Agent Workspace, Agent Runtime, Workspace Boundary, Artifact, Artifact Core Record, Artifact Format Profile, Artifact Extension, Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Agent Team Instance lifecycle state, Coordination Policy, Capability Binding, Skill Binding projection, Research Operation Extension Point, Execution Adapter Command Request, Scheduler Policy, Gate Policy, Literature Provider Binding, Baseline-Waiver Policy, Execution Adapter, Workflow Stage, Workflow Stage Cursor, and Completion Watcher Contract.


## Workspace Path Resolution

Ordinary Project, Topic Workspace, Workspace Runtime, task support, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are resolved surfaces. Ask for semantic targets such as Topic Workspace, Workspace Runtime, task support directory, run log Artifact, experiment output Artifact, analysis output Artifact, figure output Artifact, paper Artifact, decision Artifact, evidence Artifact, finding Artifact, handoff Artifact, Agent Workspace scratch, Agent Runtime state, or Agent Artifact.

Do not emit ordinary path TBD placeholders for these surfaces. For topic-scoped CLI behavior, `isomer-cli` first resolves Effective Topic Context and then passes the selected Research Topic, Topic Workspace, optional Research Inquiry, Research Task, Run, Agent Team Instance, and Agent Instance refs into Workspace Path Resolution. Workspace plans have precedence, then supported Execution Adapter `ISOMER_*` path environment variables, then Project Manifest defaults, then built-in defaults. Environment variables are launch-time adapter inputs, not durable truth; resolved effective paths and their source belong in Workspace Runtime or Provenance Records.

## CLI Topic Context Resolution

When an `isomer-cli` command needs topic-specific behavior, skills may name Effective Topic Context instead of inventing command-specific lookup rules. Effective Topic Context is the resolved CLI view of the selected Project, Research Topic, Research Topic Config, Topic Workspace, optional lifecycle refs, Topic Agent Team Profile default, Execution Adapter refs, Capability Binding refs, Skill Binding projection refs, Research Operation Extension Point refs, Scheduler Policy refs, Gate Policy refs, Literature Provider Binding refs, Baseline-Waiver Policy refs, Artifact Format Profile refs, Artifact Extension refs, and source metadata.

Use only these topic-context identity environment refs when examples must show launch-time topic selection or disambiguation: `ISOMER_RESEARCH_TOPIC_ID`, `ISOMER_TOPIC_WORKSPACE_ID`, `ISOMER_RESEARCH_INQUIRY_ID`, `ISOMER_RESEARCH_TASK_ID`, `ISOMER_RUN_ID`, `ISOMER_AGENT_TEAM_INSTANCE_ID`, and `ISOMER_AGENT_INSTANCE_ID`. These refs do not define command execution, credentials, scheduling, provider payloads, command outputs, or durable state; durable refs and source metadata belong in Workspace Runtime, Provenance Records, or the applicable lifecycle and recording records.

## Research Recording Contracts

Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are resolved durable record surfaces. Use accepted recording APIs for Artifact and Provenance recording, Finding query/write, and Gate open/resolve/record behavior.

Do not emit recording TBD placeholders for these surfaces. Artifact Core Records are generic and minimal; topic-specific output expectations attach through optional Artifact Format Profile refs and Artifact Extension refs, not mandatory core fields. Unknown or missing profiles and extensions degrade to generic Artifact handling. Evidence Items are the support, contradiction, or context boundary for Research Claims. Research Claim status is `open`, `supported`, `refuted`, or `withdrawn` unless a later accepted contract extends it; contradiction and context belong on Evidence Items or claim-evidence links. Findings are primarily scoped to Research Inquiries when an applicable inquiry exists. A Gate may resolve through a Decision Record, but cancelled or superseded Gates can close with a Provenance Record when no meaningful choice was made.

## Research Lifecycle State

Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Workflow Stage Cursor, and Agent Team Instance lifecycle state are resolved lifecycle surfaces. Use Workflow Stage Cursor for durable routing state, not scheduling. Use Agent Team Instance lifecycle state for planned, active, paused, blocked, completed, stopped, or archived team execution state; optional active or relevant Research Inquiry refs are context and routing anchors, not execution scope. Use Research Inquiry Relationships for inquiry graph links and require Decision Records only when a meaningful route choice was made.

Do not emit lifecycle TBD placeholders for `schema-stage-cursor`, `schema-agent-team-state`, or `policy-branching`. Research Inquiry is a question object and not a parallel execution scope. Express parallel work only as Topic-level parallelism across Agent Team Instances or Task-level parallelism across Agent Instances inside one Agent Team Instance.

## Research Execution and Extension Contract

Command execution, repository inspection, package management, notebook execution, HPC jobs, document builds, figure rendering, literature search, baseline acceptance, baseline waiver, cost/privacy policy, credential use, data export, Skill Binding, Service Requests, and agent launch behavior are resolved through the Research Execution and Extension Contract.

Use Research Operation Extension Points for the operation slots a skill requires. Use Capability Binding refs and Skill Binding projections for role, profile, skill, data, credential, adapter, and workspace authority. Use Execution Adapter Command Requests for executable or provider-backed dispatch, including Service Request dispatch, Service Agent Instance launch, and Agent Team Instance launch operations; the envelope carries dispatch, preflight, monitoring, and recording refs while Service Request, Service Agent Instance, Agent Team Instance, and Agent Profile records remain distinct domain objects. Use Scheduler Policy refs for dispatch, retry, monitoring, checkpoints, resume behavior, and stop conditions without redefining Workflow Stage Cursor or Agent Team Instance lifecycle state. Use Gate Policy refs for cost, credential, privacy, data-export, long-compute, destructive-change, publication-facing, and other governed-action preflight. Use Literature Provider Bindings for external literature or metadata requests, and record context-only provider output first as provider-output Artifacts before deriving Findings or Evidence Items. Use Baseline-Waiver Policy refs for routes that proceed without an accepted active baseline; those policies may open or reference Gates and must preserve comparator context.

Do not emit TBD placeholders for `api-execution-command`, `provider-literature-search`, `schema-skill-binding`, `policy-scheduler`, `policy-baseline-waiver`, or `policy-cost-privacy-gate`. Provider-specific command bodies, scheduler queues, credential backends, provider payloads, baseline registries, renderers, exporters, service backends, and agent launch mechanisms remain outside generic skill text and belong behind provider bindings, opaque adapter payload refs, credential backends, or Execution Adapter implementations.

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
| command execution | Execution Adapter Command Request with Research Operation Extension Point, Capability Binding, Skill Binding projection, Gate Policy, Scheduler Policy, workspace, and recording refs |
| route decision | Decision Record, possibly resolving a Gate |
| user choice on scope, cost, privacy, safety, publication-facing output, or finality | Gate Policy preflight and Gate through the Operator Agent when human judgment is required |

## Rejected Runtime Concepts

Do not port source runtime scheduling terms as Isomer concepts. The Operator Agent is always the human-facing control boundary. Use Workflow Stage Cursor recommendations, Gates, Decision Records, observations, or pauses for Operator Agent instruction instead of scheduler fields.

## Evidence Boundaries

Claims and route judgments must be tied to Evidence Items, Findings, Artifacts, Decision Records, or explicit Operator Agent Gates. Negative, partial, null, failed, blocked, infeasible, or contradictory results are evidence and should stay visible.

## Runtime Boundary

This skill describes research judgment. It does not define Isomer runtime APIs, schedulers, credentials, mailbox routes, gateway routes, concrete agent launch behavior, or ordinary path layouts covered by Workspace Path Resolution.

## TBD Surface Registry

Use registered TBD-surface placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design. Ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are settled by Workspace Path Resolution. `isomer-cli` topic selection and topic-specific CLI context are settled as Effective Topic Context by CLI Topic Context Resolution, and Artifact Core Records, Artifact Format Profiles, and Artifact Extensions are settled as generic recording metadata by Research Recording Contracts. Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are settled by Research Recording Contracts. Research Topics, Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, Workflow Stage Cursors, and Agent Team Instance lifecycle state are settled by Research Lifecycle State. Research Operation Extension Points, Execution Adapter Command Requests, Skill Binding projections, Scheduler Policy refs, Gate Policy refs, Literature Provider Bindings, and Baseline-Waiver Policy refs are settled by the Research Execution and Extension Contract. Skills should name semantic workspace scopes, Artifact kinds, durable record types, accepted recording APIs, accepted lifecycle objects, Effective Topic Context, or accepted extension-contract terms instead of emitting TBD placeholders for resolved surfaces.

The Research Execution and Extension Contract settles the generic command, provider, scheduler, Skill Binding, baseline-waiver, and Gate-policy surfaces formerly tracked as open TBDs. Provider-specific command bodies, scheduler queues, provider payload schemas, credential backend details, concrete literature providers, baseline registries, renderer implementations, exporter implementations, service backends, and agent launch mechanisms remain implementation details behind provider bindings, opaque adapter payload refs, credential backends, or Execution Adapter implementations.

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

### Resolved Research Execution Extension Surfaces

These former execution and extension TBDs are mapped to the Research Execution and Extension Contract and must not be emitted as open TBD placeholders in research-stage skill text.

| Former ID | Resolution |
| --- | --- |
| api-execution-command | Use Execution Adapter Command Requests with Research Operation Extension Point refs, Capability Binding refs, Skill Binding projection refs, Gate Policy refs, Scheduler Policy refs, workspace refs, and recording refs. |
| provider-literature-search | Use Literature Provider Bindings and record context-only provider results as provider-output Artifacts before deriving Findings, Evidence Items, or Research Claims. |
| schema-skill-binding | Use Skill Binding projections from Research Topic Config and Topic Agent Team Profile refs; do not define provider install schemas in generic skill text. |
| policy-scheduler | Use Scheduler Policy refs for dispatch, retry, monitoring, checkpoint, resume, and stop behavior; keep durable routing state in Workflow Stage Cursor and lifecycle state in Agent Team Instance lifecycle state. |
| policy-baseline-waiver | Use Baseline-Waiver Policy refs for routes that proceed without an accepted active baseline; waiver policy may open or reference Gates and must preserve comparator context. |
| policy-cost-privacy-gate | Use Gate Policy refs for cost, credential, privacy, data-export, long-compute, destructive-change, publication-facing, and other governed-action preflight. |
