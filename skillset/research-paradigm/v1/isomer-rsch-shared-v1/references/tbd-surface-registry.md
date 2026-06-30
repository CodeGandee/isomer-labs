# TBD Surface Registry

Use registered TBD-surface placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design. Ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are settled by Workspace Path Resolution. `isomer-cli` topic selection and topic-specific CLI context are settled as Effective Topic Context by CLI Topic Context Resolution, and Artifact Core Records, Artifact Format Profiles, and Artifact Extensions are settled as generic recording metadata by Research Recording Contracts. Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are settled by Research Recording Contracts. Research Topics, Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, Workflow Stage Cursors, and Agent Team Instance lifecycle state are settled by Research Lifecycle State. Research Operation Extension Points, Execution Adapter Command Requests, Skill Binding projections, Scheduler Policy refs, Gate Policy refs, Literature Provider Bindings, and Baseline-Waiver Policy refs are settled by the Research Execution and Extension Contract. Skills should name semantic workspace scopes, Artifact kinds, durable record types, accepted recording APIs, accepted lifecycle objects, Effective Topic Context, or accepted extension-contract terms instead of emitting TBD placeholders for resolved surfaces.

The Research Execution and Extension Contract settles the generic command, provider, scheduler, Skill Binding, baseline-waiver, and Gate-policy surfaces formerly tracked as open TBDs. Provider-specific command bodies, scheduler queues, provider payload schemas, credential backend details, concrete literature providers, baseline registries, renderer implementations, exporter implementations, service backends, and agent launch mechanisms remain implementation details behind provider bindings, opaque adapter payload refs, credential backends, or Execution Adapter implementations.

## Resolved Workspace Path Surfaces

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

## Resolved Research Recording Surfaces

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

## Resolved Research Lifecycle Surfaces

These former lifecycle TBDs are mapped to Research Lifecycle State and must not be emitted as open TBD placeholders in research-stage skill text.

| Former ID | Resolution |
| --- | --- |
| schema-stage-cursor | Use Workflow Stage Cursor as durable routing state through Research Lifecycle State. |
| schema-agent-team-state | Use Agent Team Instance lifecycle state through Research Lifecycle State. |
| policy-branching | Use Research Inquiry Relationship policy through Research Lifecycle State; create Decision Records only for meaningful route choices. |

## Resolved Research Execution Extension Surfaces

These former execution and extension TBDs are mapped to the Research Execution and Extension Contract and must not be emitted as open TBD placeholders in research-stage skill text.

| Former ID | Resolution |
| --- | --- |
| api-execution-command | Use Execution Adapter Command Requests with Research Operation Extension Point refs, Capability Binding refs, Skill Binding projection refs, Gate Policy refs, Scheduler Policy refs, workspace refs, and recording refs. |
| provider-literature-search | Use Literature Provider Bindings and record context-only provider results as provider-output Artifacts before deriving Findings, Evidence Items, or Research Claims. |
| schema-skill-binding | Use Skill Binding projections from Research Topic Config and Topic Agent Team Profile refs; do not define provider install schemas in generic skill text. |
| policy-scheduler | Use Scheduler Policy refs for dispatch, retry, monitoring, checkpoint, resume, and stop behavior; keep durable routing state in Workflow Stage Cursor and lifecycle state in Agent Team Instance lifecycle state. |
| policy-baseline-waiver | Use Baseline-Waiver Policy refs for routes that proceed without an accepted active baseline; waiver policy may open or reference Gates and must preserve comparator context. |
| policy-cost-privacy-gate | Use Gate Policy refs for cost, credential, privacy, data-export, long-compute, destructive-change, publication-facing, and other governed-action preflight. |
