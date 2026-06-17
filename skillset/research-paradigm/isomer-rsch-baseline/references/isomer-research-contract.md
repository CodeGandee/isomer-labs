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

Use Isomer Labs terms: Research Thread, Research Goal, Research Task, Research Branch, Run, Isomer Workspace, Workspace Runtime, Agent Workspace, Artifact, Agent Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Signal Observation, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Coordination Policy, Capability Binding, Execution Adapter, Workflow Stage, and Completion Watcher Contract.

Do not invent concrete paths, filenames, storage roots, command surfaces, provider names, schemas, or generated layouts. Use the registered TBD-surface placeholder form when a skill outcome must mention an unsettled concrete surface.

## Source-Term Mappings

| Source term or operation | Isomer Labs framing |
| --- | --- |
| lifecycle-level research work | Research Thread |
| initial goal or objective text | Research Goal, Measurable Objective, or Exploratory Goal |
| bounded unit of research work | Research Task |
| one execution attempt | Run |
| forked research route | Research Branch |
| filesystem area for one task | Isomer Workspace, if storage scope is known |
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
| canonical metric-contract file path | metric-contract Artifact; concrete storage uses `[[tbd-surface:path-artifact-layout]]` |
| trusted output path | Evidence Item pointer; concrete path uses `[[tbd-surface:path-artifact-layout]]` or `[[tbd-surface:path-run-logs]]` |
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

- Current Research Task or Research Branch scope.
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

This skill describes research judgment. It does not define Isomer runtime APIs, schedulers, storage layouts, credentials, mailbox routes, gateway routes, service endpoints, package managers, container runtimes, or concrete agent launch behavior.

When a source behavior implies execution, literature lookup, storage, state mutation, monitoring, publication, or chart generation, describe the intended Isomer record or capability and mark the concrete surface as unsettled.

## TBD Surface Registry

Use registered TBD-surface placeholders in skill outcomes when a concrete surface is not settled by an accepted Isomer design.

| ID | Kind | Placeholder | Missing decision |
| --- | --- | --- | --- |
| path-isomer-workspace | path | `[[tbd-surface:path-isomer-workspace]]` | Concrete Isomer Workspace path convention. |
| path-workspace-runtime | path | `[[tbd-surface:path-workspace-runtime]]` | Concrete Workspace Runtime storage layout. |
| path-agent-workspace | path | `[[tbd-surface:path-agent-workspace]]` | Concrete Agent Workspace layout. |
| path-artifact-layout | path | `[[tbd-surface:path-artifact-layout]]` | Artifact directory and naming layout. |
| path-run-logs | path | `[[tbd-surface:path-run-logs]]` | Run log and result file layout. |
| path-experiment-output | path | `[[tbd-surface:path-experiment-output]]` | Experiment output layout. |
| path-analysis-output | path | `[[tbd-surface:path-analysis-output]]` | Analysis output layout. |
| path-paper-layout | path | `[[tbd-surface:path-paper-layout]]` | Report or manuscript layout. |
| path-figure-output | path | `[[tbd-surface:path-figure-output]]` | Figure source and export layout. |
| api-artifact-record | api | `[[tbd-surface:api-artifact-record]]` | API for recording Artifacts and Provenance Records. |
| api-finding-query | api | `[[tbd-surface:api-finding-query]]` | API for querying and writing Findings or durable context. |
| api-execution-command | api | `[[tbd-surface:api-execution-command]]` | Execution command surface, permissions, and logging behavior. |
| api-gate | api | `[[tbd-surface:api-gate]]` | API for opening, resolving, and recording Gates. |
| provider-literature-search | provider | `[[tbd-surface:provider-literature-search]]` | Literature search and paper-reading provider. |
| schema-decision-record | schema | `[[tbd-surface:schema-decision-record]]` | Decision Record fields and validation. |
| schema-evidence-item | schema | `[[tbd-surface:schema-evidence-item]]` | Evidence Item fields and validation. |
| schema-research-claim | schema | `[[tbd-surface:schema-research-claim]]` | Research Claim state and fields. |
| schema-gate | schema | `[[tbd-surface:schema-gate]]` | Gate categories, states, and payload fields. |
| schema-stage-cursor | schema | `[[tbd-surface:schema-stage-cursor]]` | Workflow Stage cursor and next-stage representation. |
| schema-agent-team-state | schema | `[[tbd-surface:schema-agent-team-state]]` | Agent Team Instance pause and advancement states. |
| schema-skill-binding | schema | `[[tbd-surface:schema-skill-binding]]` | Capability Binding projection and skill install schema. |
| policy-scheduler | policy | `[[tbd-surface:policy-scheduler]]` | Runtime scheduling and continuation policy. |
| policy-branching | policy | `[[tbd-surface:policy-branching]]` | When a candidate route becomes a Research Branch. |
| policy-baseline-waiver | policy | `[[tbd-surface:policy-baseline-waiver]]` | Baseline acceptance and waiver rules. |
| policy-cost-privacy-gate | policy | `[[tbd-surface:policy-cost-privacy-gate]]` | Cost, credential, privacy, and data-export Gate thresholds. |
