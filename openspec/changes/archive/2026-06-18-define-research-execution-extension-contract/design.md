## Context

Workspace Path Resolution, Research Recording Contracts, Research Lifecycle State, and CLI Topic Context Resolution now settle the basic platform language for research-paradigm skills. The remaining gap is the boundary between generic research method and concrete execution: skills still use TBD placeholders for command execution, scheduler policy, cost/privacy Gate policy, Skill Binding projection, baseline-waiver policy, and literature providers.

The user goal is not to bake CUDA, paper-writing, literature search, package management, or venue-specific behavior into generic skills. The goal is to make every generic skill contract specified, while exposing explicit extension points that a Research Topic Config, Topic Agent Team Profile, Capability Binding, Execution Adapter, provider binding, or Gate policy can fill for a specific research topic.

The current skill text already points in this direction. Command-heavy skills say to execute through Capability Bindings and Execution Adapters. Literature-facing skills use literature capability language. Baseline skills distinguish comparator acceptance from waiver choices. CLI Topic Context already carries Execution Adapter refs, Capability Binding refs, Gate policy refs, Artifact Format Profile refs, and Artifact Extension refs, but it intentionally does not define their runtime contract.

## Goals / Non-Goals

**Goals:**

- Replace the six remaining research-paradigm TBD placeholders with accepted contract-level extension points: execution command, scheduler/continuation policy, cost/privacy Gate policy, Skill Binding, baseline-waiver policy, and literature provider.
- Define a Research Operation Extension Point model that skills can declare and topic-specific config can satisfy through refs.
- Define a provider-neutral Execution Adapter Command Request shape for shell commands, package-manager commands, repository inspection, notebook actions, HPC jobs, document builds, figure renders, service requests, and agent-launch actions.
- Define validation rules that block governed execution when required extension refs or Gate policies are missing, without blocking unrelated inspection or safe planning work.
- Define how extension choices and command outcomes are recorded through existing Run, Artifact, Evidence Item, Finding, Decision Record, Gate, and Provenance Record surfaces.
- Update research-paradigm skills so they name required extension points and expected Artifacts instead of inventing concrete providers, schemas, command runners, or host APIs.

**Non-Goals:**

- Do not implement command runners, shells, schedulers, queues, notebooks, package managers, credential backends, literature providers, baseline systems, service adapters, or provider-specific APIs.
- Do not store credentials, tokens, API keys, passwords, command outputs, process ids, provider payloads, or live runtime state in Research Topic Config or Effective Topic Context.
- Do not make a research-domain-specific artifact schema mandatory for generic Artifact Core Records.
- Do not replace Workspace Path Resolution, Research Recording Contracts, Research Lifecycle State, or CLI Topic Context Resolution.
- Do not decide which specific literature provider, HPC scheduler, package manager, model provider, GUI renderer, or baseline registry a user must use.

## Decisions

### Decision 1: Define contract-level extension points before provider-specific implementations

Research-paradigm skills should declare the kind of operation they need, not the provider that satisfies it. The accepted extension-point catalog should include at least `command_execution`, `repository_inspection`, `package_management`, `notebook_execution`, `hpc_job`, `document_build`, `figure_render`, `literature_search`, `baseline_acceptance`, `baseline_waiver`, `cost_privacy_gate`, `credential_use`, `data_export`, `skill_binding`, `service_request`, and `agent_launch`.

The concrete implementation belongs in refs selected by Project Manifest, Research Topic Config, Topic Agent Team Profile, Capability Binding, Gate policy, or Execution Adapter material. A CUDA topic can bind `hpc_job` to a SLURM adapter, while a paper-only topic can leave that extension point absent and still use `literature_search` or `document_build`.

Alternative considered: write per-skill provider defaults. Rejected because that would make the generic skillset accidentally opinionated about CUDA, Python, LaTeX, literature search providers, or backend agent systems.

### Decision 2: Use one provider-neutral Execution Adapter Command Request shape

Execution Adapter Command Request should be the neutral envelope for executable work. It should contain identity refs, operation kind, selected extension point refs, selected Capability Binding refs, permission profile refs, working-directory semantic target, environment input policy, input refs, expected output specs, expected Artifact kinds, log Artifact refs or specs, timeout or long-running hints, monitor policy refs, Gate policy refs, and source metadata from Effective Topic Context.

The envelope can carry opaque adapter-specific payload refs, but it must not embed provider-specific command implementation bodies as generic Isomer schema. Concrete adapters can translate the envelope into shell commands, notebook runs, HPC jobs, document builds, GUI render requests, service requests, or agent launches.

Alternative considered: define separate command schemas for shell, notebook, HPC, document build, and agent launch. Rejected for the first contract because all of them need the same audit, permission, input/output, Gate, Run, and Provenance behavior.

### Decision 3: Separate scheduler policy from Workflow Stage Cursor

Workflow Stage Cursor remains durable routing state. Scheduler and continuation policy should become an extension point that can authorize automatic dispatch, retry, monitoring cadence, manual checkpoint behavior, and stop conditions for a Run or Agent Team Instance. The scheduler policy may be selected through Topic Agent Team Profile, Coordination Policy, Run plan, or explicit command context, but it does not own research lifecycle statuses.

This keeps research route state stable even when the runtime scheduler is provider-specific or absent.

Alternative considered: fold scheduler behavior into Agent Team Instance lifecycle state. Rejected because lifecycle state tells what happened; scheduler policy says what may be dispatched next.

### Decision 4: Model cost, credential, privacy, and data-export as Gate policy preflight

Command requests and provider operations should run a preflight against selected Gate policy refs before governed actions. The preflight should classify whether an operation touches cost, credentials, private data, external upload, long-running compute, destructive file changes, publication-facing output, or user-controlled resources.

If a required Gate policy is missing or unresolved, the system should block only the governed action and report which extension point or policy ref is missing. The Operator Agent can open a Gate with concrete options when human approval is needed.

Alternative considered: embed cost/privacy booleans in every command request. Rejected because different topics need different thresholds, and policy decisions must remain reviewable and reusable.

### Decision 5: Treat literature providers and baseline waiver as typed extension points, not open provider names

`literature_search` should be a provider extension point with expected source metadata, citation metadata, paper Artifact refs, confidence labels, and Evidence Item or Finding conversion rules. `baseline_waiver` should be a policy extension point that distinguishes relevant comparator attachment, active baseline acceptance, and explicit waiver decisions.

The first version should specify what the skills need and how results are recorded. It should not pick a provider or baseline registry.

Alternative considered: leave literature provider and baseline waiver for later changes. Rejected for this change because the user wants the research-paradigm skills to stop carrying open placeholders; typed extension points can settle the generic contract without picking an implementation.

### Decision 6: Record extension choices through existing durable records

The extension contract should not create a new parallel recording database. Run records should carry selected command request refs, extension point refs, Capability Binding refs, policy refs, source metadata, and outcome summary refs. Artifacts store produced outputs. Evidence Items link measurements, literature observations, or baseline verdicts to claims. Decision Records capture meaningful choices. Gates capture human-return approvals. Provenance Records explain actions, inputs, outputs, actors, and provider refs.

Alternative considered: add a dedicated extension-execution record family. Rejected because it would duplicate Run, Artifact, and Provenance responsibilities before the implementation proves a separate record type is needed.

### Decision 7: Skill Binding becomes a projection contract inside Capability Binding

The open `schema-skill-binding` placeholder should resolve to a Skill Binding projection that says which skills, references, assets, scripts, prompts, model posture, and allowed operation extension points are available to an Agent Role or Agent Profile. The projection belongs under Capability Binding or Agent Profile material; it should not become a provider-specific package installer schema.

Alternative considered: define a standalone skill registry now. Rejected because the current need is to let research skills declare and validate skill availability. Install and packaging mechanics can remain provider-specific or later platform work.

## Risks / Trade-offs

- [Risk] One contract may become too broad. Mitigation: keep the spec focused on neutral extension-point refs, request envelopes, validation, and recording; leave provider implementation bodies out of scope.
- [Risk] Extension points could become vague labels. Mitigation: require each extension point to declare operation kind, required inputs, expected outputs, permission class, recording obligations, and missing-ref behavior.
- [Risk] Gate policy preflight could block too much work. Mitigation: require validation to block only the governed action and allow unrelated inspection, planning, or safe Artifact review.
- [Risk] Scheduler policy may be confused with lifecycle state. Mitigation: repeat that Workflow Stage Cursor and Agent Team Instance lifecycle state remain lifecycle facts; scheduler policy only authorizes dispatch and monitoring behavior.
- [Risk] Literature and baseline provider details may still vary widely. Mitigation: specify result metadata and recording requirements, not provider APIs.
- [Risk] Skill updates may remove placeholders before specs are strong enough. Mitigation: update shared contracts first, then local copies, then stage-specific references, and validate every removed TBD against an accepted extension-point requirement.

## Migration Plan

1. Add the new `research-execution-extension-contract` main spec from the delta spec.
2. Update `cli-topic-context-resolution` so Effective Topic Context carries typed extension refs and validates missing extension refs without storing implementation bodies or runtime truth.
3. Update `research-recording-contracts` so execution, literature, baseline, scheduler, Skill Binding, and Gate policy extension choices record through existing durable records.
4. Update `research-paradigm-skills` so the six remaining TBD placeholders are mapped to accepted extension points.
5. Update `.imsight-arts/project-explore` and context docs with the new extension-point terms.
6. Update `isomer-rsch-shared`, the TBD registry, local research contract copies, and stage-specific references.
7. Search `skillset/research-paradigm` for all six placeholders and confirm each is removed or moved to archival/provenance text only.
8. Run OpenSpec validation for the new and modified specs, then run repository whitespace checks.

Rollback is documentation-only: restore the prior OpenSpec specs and skill references if the accepted extension-point vocabulary proves too broad before implementation.

## Resolved Follow-up Decisions

### Decision 8: Show extension refs in both topic config and team profile examples

The first implementation should include example TOML fragments for both Research Topic Config and Topic Agent Team Profile. Research Topic Config examples should show topic-level defaults and selected extension refs. Topic Agent Team Profile examples should show role, Workflow Stage, Capability Binding, and Skill Binding projection availability for the topic-specialized team.

Neither example location should embed provider-specific command bodies, credentials, scheduler internals, command outputs, or provider payloads. The examples are explanatory fixtures for the contract, not a provider implementation.

Alternative considered: only show Research Topic Config examples. Rejected because role-scoped and stage-scoped capability availability belongs to Topic Agent Team Profile, Capability Binding, and Skill Binding projection material rather than the topic-level config alone.

### Decision 9: Baseline waiver is a separate policy ref that may open a Gate

`baseline_waiver` should remain a distinct policy extension point. The policy answers whether a route may proceed without an accepted active baseline, what rationale must be recorded, and what later promotions are blocked or allowed. When the policy requires human judgment, it may open or reference a Gate, and the Gate resolution records the specific human-return decision.

This keeps reusable baseline rules separate from the pending-decision object. A Gate is the workflow control point; baseline-waiver policy is the reusable rule set that decides when such a control point is needed.

Alternative considered: model baseline waiver as a Gate policy subtype only. Rejected because waiver rules also need non-interactive validation, comparator context preservation, and later promotion checks even when no human-return Gate is open.

### Decision 10: Context-only literature starts as provider-output Artifact

When literature provider output is collected only for orientation, source review, adjacent-work scouting, or future comparison, record it first as a provider-output Artifact with source metadata and Provenance. It can later be distilled into a Finding when it becomes reusable research context, or linked as an Evidence Item when it supports, contradicts, contextualizes, refutes, or motivates withdrawal of a Research Claim.

This preserves the Research Recording Contracts distinction: provider output is not claim support by itself. Evidence status begins only when a relation intent to a claim or decision is recorded.

Alternative considered: record literature output directly as Findings. Rejected because raw provider output and researcher-distilled insight have different authorship, quality, and reuse semantics.

### Decision 11: Service requests and agent launches share the command request envelope

Service requests and agent-launch operations should use the same Execution Adapter Command Request envelope, with operation kinds such as `service_request` and `agent_launch`. The envelope supplies the shared audit surface: identity refs, Effective Topic Context source metadata, extension refs, permission and Gate policy refs, expected outputs, Run linkage, and Provenance obligations.

The domain objects remain distinct. A Service Request still records operational support intent, a Service Agent Instance remains outside Agent Team Instance membership, and an Agent Team Instance still comes from a Topic Agent Team Profile. The shared envelope only normalizes dispatch, preflight, monitoring, and recording behavior.

Alternative considered: create a narrower dispatch envelope for service requests and agent launches. Rejected for the first contract because service dispatch and launch dispatch need the same permission, Gate, Run, Artifact, and Provenance behavior as other executable operations.
