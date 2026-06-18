# Isomer Research Contract

Use this local reference for terminology, evidence boundaries, runtime boundaries, and TBD placeholders. This skill must be self-contained, so do not load shared files from outside this skill directory.

## Truth-Source Order

Prefer durable records over recollection:

1. User instruction and explicit Gate decisions through the Operator Agent.
2. Decision Records, Artifacts, Evidence Items, Findings, Research Claims, and Provenance Records.
3. Workspace Runtime state, Run records, handoffs, Signal Observations, and validated View Manifests.
4. Agent Artifacts and Agent Runtime notes that have clear provenance.
5. Conversation context, only when durable state is absent or being interpreted.

## Durable Vocabulary

Use Isomer Labs terms: Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Topic Workspace, Workspace Runtime, Agent Workspace, Agent Runtime, Workspace Boundary, Artifact, Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Coordination Policy, Capability Binding, Execution Adapter, Workflow Stage, and Completion Watcher Contract.

Do not invent concrete paths, filenames, storage roots, command surfaces, provider names, schemas, or generated layouts. Use the registered TBD-surface placeholder form when a skill outcome must mention an unsettled concrete surface.


## Workspace Path Resolution

Ordinary Project, Topic Workspace, Workspace Runtime, task support, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are resolved surfaces. Ask for semantic targets such as Topic Workspace, Workspace Runtime, task support directory, run log Artifact, experiment output Artifact, analysis output Artifact, figure output Artifact, paper Artifact, decision Artifact, evidence Artifact, finding Artifact, handoff Artifact, Agent Workspace scratch, Agent Runtime state, or Agent Artifact.

Do not emit ordinary path TBD placeholders for these surfaces. Workspace plans have precedence, then supported Execution Adapter `ISOMER_*` environment variables, then Project Manifest defaults, then built-in defaults. Environment variables are launch-time adapter inputs, not durable truth; resolved effective paths and their source belong in Workspace Runtime or Provenance Records.

## Research Recording Contracts

Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are resolved durable record surfaces. Use accepted recording APIs for Artifact and Provenance recording, Finding query/write, and Gate open/resolve/record behavior.

Do not emit recording TBD placeholders for these surfaces. Evidence Items are the support, contradiction, or context boundary for Research Claims. Research Claim status is `open`, `supported`, `refuted`, or `withdrawn` unless a later accepted contract extends it; contradiction and context belong on Evidence Items or claim-evidence links. Findings are primarily scoped to Research Inquiries when an applicable inquiry exists. A Gate may resolve through a Decision Record, but cancelled or superseded Gates can close with a Provenance Record when no meaningful choice was made.

## Source-Term Mappings

| Source term or operation | Isomer Labs framing |
| --- | --- |
| lifecycle-level research work | Research Topic, Research Inquiry, or Research Task depending on scope |
| initial goal or objective text | Research Topic with optional Measurable Objective |
| bounded unit of research work | Research Task |
| one execution attempt | Run |
| forked research route | Research Inquiry Relationship plus Decision Record when a choice is made |
| filesystem area for topic, task, run, output, or agent work | Topic Workspace, Workspace Runtime, semantic Artifact kind, or Agent Workspace through Workspace Path Resolution |
| persistent task state | Workspace Runtime |
| per-agent scratch or local trace area | Agent Workspace or Agent Runtime |
| source artifact operation | Artifact, Evidence Item, Decision Record, Gate, Provenance Record, or host Artifact API |
| source memory operation | Finding, Evidence Item, Artifact, or durable context query |
| source command execution | Capability Binding through an Execution Adapter |
| source literature lookup | literature search capability; provider is unsettled |
| route decision | Decision Record, possibly resolving a Gate |
| user choice on scope, cost, privacy, safety, or finality | Gate through the Operator Agent |
| registry publishing | reusable Artifact package after verification, with concrete publication API unsettled |
| package-manager or container tactic | Execution Adapter choice, not a skill requirement |
| service endpoint | evaluation Capability Binding or Execution Adapter surface, not a hard-coded endpoint |

## Baseline-Specific Mappings

| Source concept | Isomer Labs framing |
| --- | --- |
| baseline confirmation call | Decision Record that resolves the baseline Gate as accepted, plus metric-contract Artifact and Evidence Items |
| baseline waiver call | Decision Record that resolves or bypasses the baseline Gate under `[[tbd-surface:policy-baseline-waiver]]` |
| baseline overwrite call | Decision Record that replaces an accepted comparator after a material metric, code, data, or variant change |
| canonical metric-contract file path | metric-contract Artifact through Workspace Path Resolution |
| trusted output path | Evidence Item pointer or run log Artifact through Workspace Path Resolution |
| attached or imported package root | reusable Artifact package with Provenance Record |
| local service comparator | Capability Binding plus Evidence Items from evaluation observations |

## Rejected Runtime Concepts

Do not port source runtime scheduling terms as Isomer concepts. The Operator Agent is always the human-facing control boundary. Delegated Agent Team Instances either advance under approved Coordination Policy or pause for Operator Agent instruction.

| Source behavior | Isomer skill text should say |
| --- | --- |
| `workspace_mode` | source runtime collaboration detail; do not use as an Isomer mode |
| `continuation_policy` | recommend the next Workflow Stage, Gate, Decision Record, observation, or pause |
| `auto_continue` | source scheduler detail; do not schedule turns in skill text |
| `wait_for_user_or_resume` | pause for Operator Agent instruction, or record a Gate or handoff state |
| `continuation_anchor` | next recommended Workflow Stage or Decision Record target |
| `continuation_reason` | pause reason, Gate reason, failure reason, or Decision Record rationale |

## Handoff Contract

Every baseline handoff should state:

- Current Research Topic, Research Inquiry, or Research Task scope.
- Acceptance target and active route.
- Comparator identity, source identity, and baseline id.
- Metric contract fields inspected or still missing.
- Inputs and durable sources inspected.
- Evidence Items, Artifacts, Run records, or source documents used for trust.
- Comparability verdict and caveats.
- Gate status and Decision Records opened or resolved.
- Next recommended Workflow Stage, pause, or blocker.
- Known caveats, missing evidence, and unsettled surfaces.

## Evidence Boundaries

Claims must be tied to Evidence Items. Negative, partial, null, failed, blocked, infeasible, or contradictory results are evidence and should stay visible. Do not turn a plausible comparator into an accepted baseline without durable evidence and a metric contract.

## Runtime Boundary

This skill describes research judgment. It does not define Isomer runtime APIs, schedulers, ordinary path layouts covered by Workspace Path Resolution, credentials, mailbox routes, gateway routes, service endpoints, package managers, container runtimes, or concrete agent launch behavior.

When a source behavior implies execution, literature lookup, storage, state mutation, monitoring, publication, or chart generation, describe the intended Isomer record, semantic Artifact kind, workspace scope, or capability. Mark the concrete surface as unsettled only when it is outside accepted Isomer contracts.

## TBD Surface Registry

Use registered TBD-surface placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design. Ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, Agent Workspace, and Agent Runtime paths are settled by Workspace Path Resolution. Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates are settled by Research Recording Contracts. Skills should name semantic workspace scopes, Artifact kinds, durable record types, or accepted recording APIs instead of emitting TBD placeholders for resolved surfaces.

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

### Open TBD Surfaces

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
