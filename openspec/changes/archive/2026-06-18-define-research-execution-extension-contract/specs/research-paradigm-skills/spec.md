## MODIFIED Requirements

### Requirement: Generic Research Vocabulary
The extracted skills SHALL describe portable research behavior using established Isomer Labs concepts and without requiring DeepScientist workspace APIs or DeepScientist-specific runtime surfaces.

#### Scenario: DeepScientist API terms are mapped to Isomer concepts
- **WHEN** an extracted skill describes artifacts, memory, terminal execution, paper search, execution isolation, workflow progress, lifecycle state, route branching, scheduler behavior, Skill Binding, baseline waiver, or cost/privacy policy
- **THEN** it uses Isomer concepts such as Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Topic Workspace, Workspace Runtime, Agent Workspace, Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Workflow Stage Cursor, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Agent Team Instance lifecycle state, Capability Binding, Skill Binding projection, Research Operation Extension Point, Execution Adapter, Execution Adapter Command Request, Coordination Policy, Gate policy, scheduler policy, literature provider binding, and baseline-waiver policy

#### Scenario: Source-specific terms are bounded
- **WHEN** an extracted skill mentions a source-specific or stale term such as DeepScientist, `artifact.*`, `memory.*`, `bash_exec(...)`, DeepXiv, quest, Research Goal, Research Thread, Research Branch, Isomer Workspace, branch, worktree, `workspace_mode`, `continuation_policy`, `auto_continue`, or `wait_for_user_or_resume`
- **THEN** the mention is limited to provenance, adaptation notes, source-term mapping, or migration notes and is not a required runtime operation or active Isomer domain term

#### Scenario: Continuation policy is not ported
- **WHEN** an extracted skill preserves DeepScientist behavior about continuing, pausing, resuming, or monitoring long-running work
- **THEN** it describes the behavior through Agent Team Instance lifecycle state under Coordination Policy, paused waiting for Operator Agent instruction, Workflow Stage Cursor recommendations, Gates, Decision Records, Completion Watcher Contracts, Signal Observations, or accepted scheduler policy refs, and does not require an Isomer `continuation_policy` field

### Requirement: Unsettled Concrete Surfaces Are Explicit
The extracted skills SHALL mark concrete commands, runtime APIs, providers, schemas, policies, storage roots, and generated layouts as `yet-to-be-determined` only when they are not settled by accepted Isomer designs such as Workspace Path Resolution, Research Recording Contracts, Research Lifecycle State, CLI Topic Context Resolution, or Research Execution and Extension Contract.

#### Scenario: Path surface is covered by workspace path resolution
- **WHEN** a skill needs an ordinary Topic Workspace, Workspace Runtime, Agent Workspace, Run log, experiment output, analysis output, paper output, figure output, or Artifact class location covered by the Workspace Path Resolution contract
- **THEN** the skill names the semantic workspace scope or Artifact kind and relies on the resolver instead of emitting a path TBD placeholder

#### Scenario: Recording surface is covered by research recording contracts
- **WHEN** a skill needs to record or query Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, or Gates covered by the Research Recording Contracts
- **THEN** the skill names the accepted record type or recording API instead of emitting `api-artifact-record`, `api-finding-query`, `api-gate`, `schema-decision-record`, `schema-evidence-item`, `schema-research-claim`, or `schema-gate` TBD placeholders

#### Scenario: Lifecycle surface is covered by research lifecycle state
- **WHEN** a skill needs Workflow Stage Cursor fields, Agent Team Instance lifecycle state, or Research Inquiry Relationship branching behavior covered by Research Lifecycle State
- **THEN** the skill names the accepted lifecycle object, state, relationship, or policy instead of emitting `schema-stage-cursor`, `schema-agent-team-state`, or `policy-branching` TBD placeholders

#### Scenario: Execution and extension surfaces are covered by research execution extension contract
- **WHEN** a skill needs command execution, repository inspection, package management, notebook execution, HPC jobs, document builds, figure rendering, scheduler behavior, Skill Binding projection, literature search, baseline-waiver policy, cost/privacy Gate policy, credential use, data export, service requests, or agent launch behavior covered by Research Execution and Extension Contract
- **THEN** the skill names the accepted Research Operation Extension Point, Capability Binding, Skill Binding projection, Execution Adapter Command Request, provider binding, scheduler policy, baseline-waiver policy, or Gate policy ref instead of emitting `api-execution-command`, `provider-literature-search`, `schema-skill-binding`, `policy-scheduler`, `policy-baseline-waiver`, or `policy-cost-privacy-gate` TBD placeholders

#### Scenario: Path surface remains unsettled outside the resolver
- **WHEN** a source skill uses a concrete path or filename that is not covered by the Workspace Path Resolution contract and no Isomer equivalent is settled by existing domain concepts or ADRs
- **THEN** the extracted skill marks that path or filename as `yet-to-be-determined` and states the missing design decision

#### Scenario: Provider-specific implementation remains external
- **WHEN** a skill depends on a provider-specific command body, scheduler queue, package manager invocation, credential backend, literature API, baseline registry, renderer, exporter, service backend, or agent launch mechanism that is not part of accepted Isomer contracts
- **THEN** the skill names the accepted extension point and leaves the provider-specific implementation to user-filled topic config, Capability Binding refs, provider binding refs, Gate policy refs, opaque adapter payload refs, or Execution Adapter implementation

## ADDED Requirements

### Requirement: Research Execution Extension Contract Consumption
The research-paradigm skillset SHALL consume the Research Execution and Extension Contract for executable operations, provider-backed operations, scheduler boundaries, policy preflight, and user-fillable topic-specific details.

#### Scenario: Skills declare required extension points
- **WHEN** a research-paradigm skill requires executable or provider-backed behavior
- **THEN** it declares the required Research Operation Extension Points, expected inputs, expected outputs, expected Artifact kinds, policy refs, and recording obligations instead of relying on implicit host behavior

#### Scenario: Skills do not embed topic-specific implementations
- **WHEN** a skill mentions research-specific details such as datasets, metrics, package managers, CUDA tools, venue templates, literature providers, queue names, credentialed services, repository commands, notebook runners, or render/export tools
- **THEN** it treats those details as topic-specific extension refs or user-provided inputs rather than mandatory generic skill behavior

#### Scenario: Command-heavy skills use execution command requests
- **WHEN** intake, baseline, optimize, experiment, analysis, science, paper-plot, figure-polish, write, review, rebuttal, or finalize needs command, repository, package, notebook, HPC, build, render, export, or service execution
- **THEN** it routes the work through an Execution Adapter Command Request with accepted extension refs, expected Artifacts, Run linkage, policy preflight, and Provenance obligations

#### Scenario: Literature-facing skills use provider extension refs
- **WHEN** scout, idea, write, review, rebuttal, paper-outline, baseline, or decision needs external literature, paper metadata, citation metadata, benchmark lookup, repository lookup, or adjacent-work scouting
- **THEN** it names the literature provider extension point and records results as Artifacts, Findings, or Evidence Items according to evidence-use intent

#### Scenario: Baseline-facing skills use waiver policy refs
- **WHEN** baseline, decision, optimize, experiment, analysis, review, rebuttal, or write would proceed without an accepted active baseline
- **THEN** it requires a baseline-waiver policy ref or an explicit Gate/Decision Record before treating the route as valid

#### Scenario: Shared registry removes resolved extension placeholders
- **WHEN** the shared TBD registry is inspected after this change
- **THEN** `api-execution-command`, `provider-literature-search`, `schema-skill-binding`, `policy-scheduler`, `policy-baseline-waiver`, and `policy-cost-privacy-gate` are mapped to accepted Research Execution and Extension Contract terms or removed as open placeholders

#### Scenario: Local contract copies stay consistent
- **WHEN** a local `isomer-research-contract.md` copy is inspected in an `isomer-rsch-*` skill directory
- **THEN** its execution, provider, scheduler, Skill Binding, baseline-waiver, and cost/privacy guidance matches the shared Research Execution and Extension Contract and does not reintroduce resolved placeholders as active open TBDs

#### Scenario: Validation checks extension contract consumption
- **WHEN** implementation validation runs
- **THEN** it confirms active research-paradigm skill text uses accepted extension-point terms for the six formerly open surfaces, leaves provider-specific implementation bodies outside generic skills, and keeps only genuinely unsettled surfaces registered in the TBD registry
