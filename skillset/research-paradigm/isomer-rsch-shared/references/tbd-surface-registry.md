# TBD Surface Registry

Use registered TBD-surface placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design. Ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are settled by Workspace Path Resolution. `isomer-cli` topic selection and topic-specific CLI context are settled as Effective Topic Context by CLI Topic Context Resolution, and Artifact Core Records, Artifact Format Profiles, and Artifact Extensions are settled as generic recording metadata by Research Recording Contracts. Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are settled by Research Recording Contracts. Research Topics, Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, Workflow Stage Cursors, and Agent Team Instance lifecycle state are settled by Research Lifecycle State. Skills should name semantic workspace scopes, Artifact kinds, durable record types, accepted recording APIs, accepted lifecycle objects, or Effective Topic Context instead of emitting TBD placeholders for resolved surfaces.

Effective Topic Context and artifact format customization do not settle execution commands, scheduler policy, Skill Binding projection, credential binding, literature providers, baseline-waiver policy, cost/privacy Gate thresholds, or validation/render/export command behavior. Use the open placeholders below for those concrete surfaces until an accepted design resolves them.

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

## Open TBD Surfaces

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| provider-literature-search | provider | `[[tbd-surface:provider-literature-search]]` | Literature search and paper-reading provider. |
| schema-skill-binding | schema | `[[tbd-surface:schema-skill-binding]]` | Capability Binding projection and skill install schema. |
| policy-scheduler | policy | `[[tbd-surface:policy-scheduler]]` | Runtime scheduling and continuation policy. |
| policy-baseline-waiver | policy | `[[tbd-surface:policy-baseline-waiver]]` | Baseline acceptance and waiver rules. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |
