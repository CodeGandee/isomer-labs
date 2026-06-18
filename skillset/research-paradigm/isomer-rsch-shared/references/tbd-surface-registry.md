# TBD Surface Registry

Use registered TBD-surface placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design. Ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are settled by Workspace Path Resolution. Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are settled by Research Recording Contracts. Skills should name semantic workspace scopes, Artifact kinds, durable record types, or accepted recording APIs instead of emitting TBD placeholders for resolved surfaces.

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

## Open TBD Surfaces

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| provider-literature-search | provider | `[[tbd-surface:provider-literature-search]]` | Literature search and paper-reading provider. |
| schema-stage-cursor | schema | `[[tbd-surface:schema-stage-cursor]]` | Workflow Stage cursor and next-stage representation. |
| schema-agent-team-state | schema | `[[tbd-surface:schema-agent-team-state]]` | Agent Team Instance pause and advancement states. |
| schema-skill-binding | schema | `[[tbd-surface:schema-skill-binding]]` | Capability Binding projection and skill install schema. |
| policy-scheduler | policy | `[[tbd-surface:policy-scheduler]]` | Runtime scheduling and continuation policy. |
| policy-branching | policy | `[[tbd-surface:policy-branching]]` | Policy for recording Research Inquiry Relationships and route decisions. |
| policy-baseline-waiver | policy | `[[tbd-surface:policy-baseline-waiver]]` | Baseline acceptance and waiver rules. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |
