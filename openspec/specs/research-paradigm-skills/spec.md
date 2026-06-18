# research-paradigm-skills Specification

## Purpose
Define the reusable Isomer Labs research-paradigm skillset, including portable research-stage skills, shared evidence vocabulary, generic agent mappings, provenance handling, Imsight skill-entrypoint structure, and validation rules that prevent DeepScientist runtime coupling from becoming an Isomer requirement.
## Requirements
### Requirement: Research Paradigm Skillset Layout
The project SHALL provide a reusable research-paradigm skillset under `skillset/research-paradigm/` using Codex skill folder layout and the `isomer-rsch-<purpose>` naming convention.

#### Scenario: Core skill folders exist
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains `isomer-rsch-shared` and core research skill folders for intake, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, write, review, rebuttal, paper-outline, paper-plot, figure-polish, and science

#### Scenario: Skill frontmatter is valid
- **WHEN** each extracted skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields, and the `name` field matches the `isomer-rsch-<purpose>` folder name

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Standalone skill bundle is self-contained
- **WHEN** an extracted skill is packaged as a standalone skill bundle
- **THEN** its `SKILL.md` and directly linked references do not require files outside that skill's directory

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*` as active skill folder names, frontmatter names, manifests, or role mappings

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

### Requirement: Shared Research Contract
The skillset SHALL include a shared research contract skill that defines common evidence, artifact, handoff, and validation rules for all research-stage skills.

#### Scenario: Shared contract covers common surfaces
- **WHEN** `isomer-rsch-shared/SKILL.md` is inspected
- **THEN** it defines truth-source order, Isomer concept mapping, durable Artifact vocabulary, handoff expectations, claim and evidence boundaries, source provenance, `yet-to-be-determined` handling, and validation discipline

#### Scenario: Stage skills reference shared rules
- **WHEN** a stage or companion skill needs common research discipline
- **THEN** it references the shared research contract instead of duplicating long common instructions

### Requirement: DeepScientist Methodology Preservation
The extracted skills SHALL preserve reusable research-stage logic from the corresponding DeepScientist source skill directories, including source `SKILL.md` content and directly supporting source references, templates, scripts, or assets when those materials contain portable research method.

#### Scenario: Stage gate behavior is preserved
- **WHEN** a stage skill is inspected
- **THEN** it includes the corresponding stage purpose, entry signals, exit criteria, route taxonomy, durable outputs, key pitfalls, and source-derived gates needed to perform the stage without reading DeepScientist source files

#### Scenario: Companion behavior is preserved
- **WHEN** a companion skill such as review, rebuttal, paper-outline, paper-plot, figure-polish, or science is inspected
- **THEN** it includes the companion's bounded purpose, expected inputs, durable outputs, validation rules, source-derived templates or examples, and handoff behavior needed to perform the companion task without reading DeepScientist source files

#### Scenario: Rich source details are preserved locally
- **WHEN** a source skill contains reusable route taxonomies, playbooks, templates, checklists, examples, boundary cases, failure handling, or operational guidance
- **THEN** the extracted skill preserves that detail in its `SKILL.md`, local `references/`, local `assets/`, or local `scripts/`, or records an explicit implementation rationale for deferring the detail

#### Scenario: Source concepts are translated correctly
- **WHEN** preserved source material mentions DeepScientist-specific concepts such as quest, artifact operations, memory operations, command wrappers, literature providers, workspace paths, branch/worktree assumptions, continuation scheduling, or generated artifact layouts
- **THEN** the extracted skill maps the concept to accepted Isomer terms, marks unsettled concrete surfaces with `[[tbd-surface:<id>]]`, or confines the source term to provenance or explicit mapping text

### Requirement: Progressive Disclosure
The skillset SHALL keep skill entrypoints concise, move long reusable detail into one-level local resources, and avoid active dependencies on files outside the skill bundle.

#### Scenario: Long methodology detail is moved to references
- **WHEN** a skill needs templates, checklists, long playbooks, route examples, operational notes, or boundary cases
- **THEN** the skill stores them under that skill's `references/`, `assets/`, or `scripts/` directory and links them directly from `SKILL.md`

#### Scenario: Active skill bundle is self-contained
- **WHEN** an enriched skill's active `SKILL.md` and directly linked references are inspected
- **THEN** they do not require `context/explore/...`, `extern/orphan/...`, archived OpenSpec files, local absolute paths, or other files outside that skill's directory to execute the skill

#### Scenario: Source provenance remains traceable
- **WHEN** source text, templates, scripts, assets, or reference files are copied or materially adapted
- **THEN** the target skill includes nearby provenance that identifies the DeepScientist source skill and applicable license context without making the source tree a runtime dependency

#### Scenario: Scripts and assets are sanitized before import
- **WHEN** source scripts or assets are imported into an enriched skill
- **THEN** they are directly useful for the skill and do not contain source-local user paths, demo-output defaults, private paths, unsatisfied hard dependencies, or DeepScientist runtime assumptions as active behavior

#### Scenario: No extraneous documentation is added
- **WHEN** a skill folder is inspected
- **THEN** it contains only files that directly support skill use, such as `SKILL.md`, `agents/openai.yaml`, `references/`, `assets/`, or `scripts/`

### Requirement: Imsight Workflow Entrypoints
Each enriched `isomer-rsch-*` skill SHALL use the Imsight skill-entrypoint structure for its `SKILL.md` while preserving the skill's trigger behavior and research guardrails.

#### Scenario: Workflow section is near the top
- **WHEN** an enriched `SKILL.md` is inspected
- **THEN** it has a near-top `## Workflow` section before detailed procedure, contract, guardrail, or reference sections

#### Scenario: Workflow steps are actionable and concise
- **WHEN** an enriched `## Workflow` section is inspected
- **THEN** it uses numbered steps that name the action to take and point to detailed sections or local references rather than embedding long procedures inline

#### Scenario: Workflow includes freeform fallback
- **WHEN** an enriched `## Workflow` section is inspected
- **THEN** it tells the agent to use its native planning tool to build and execute a step-by-step plan from the skill's constraints, references, and user request when the task does not map cleanly to the default steps

#### Scenario: Reference routing is explicit
- **WHEN** an enriched skill has local references
- **THEN** its entrypoint states which references to read first and which references to read for route-specific, template-specific, operational, validation, or writing-facing needs

### Requirement: Parallelized Skill Enrichment
The implementation SHALL use subagents to parallelize enrichment work across disjoint skill folders and centralize integration and validation in the main agent.

#### Scenario: Worker scopes are disjoint
- **WHEN** subagents are launched for implementation
- **THEN** each subagent receives an explicit non-overlapping write scope and instructions not to revert or overwrite unrelated edits from other workers

#### Scenario: Source and target context is provided
- **WHEN** a subagent enriches a skill folder
- **THEN** it is directed to inspect the target skill, `isomer-rsch-analysis`, the corresponding DeepScientist source skill directory, the migration contract, the shared TBD registry, and the Imsight formatting guidance before editing

#### Scenario: Main agent integrates shared files
- **WHEN** subagents complete their assigned work
- **THEN** the main agent reviews and integrates their changes, owns shared files such as the TBD registry and suite README, resolves conflicts, and runs final validation

#### Scenario: Large resources are bounded
- **WHEN** a source skill contains large generated catalogs, plotting scripts, style assets, or venue templates
- **THEN** the implementation either imports sanitized directly useful resources in the assigned skill folder or records a deferred task for a follow-up resource-focused change

### Requirement: Generic Agent Mapping
The team documentation SHALL map generic research agents to the extracted `isomer-rsch-*` skills without making the skills depend on one team topology.

#### Scenario: Generic role map exists
- **WHEN** the updated team documentation is inspected
- **THEN** it defines generic research roles and lists the `isomer-rsch-*` research-paradigm skills installed for each role

#### Scenario: Skill bundles are topology-neutral
- **WHEN** an extracted skill is inspected
- **THEN** it does not require a specific Houmao specialist name, mailbox route, gateway, credential, or agent topology to perform its research operation

### Requirement: Provenance and Licensing
The implementation SHALL preserve source provenance and license notices for copied or adapted DeepScientist-derived material.

#### Scenario: Copied materials include license notices
- **WHEN** source text, templates, scripts, assets, or reference files are copied or materially adapted from DeepScientist or upstream helper skills
- **THEN** the new skillset includes the applicable Apache 2.0 or upstream MIT notice in a nearby license or provenance file

#### Scenario: Source analysis remains traceable
- **WHEN** a reviewer wants to trace an extracted skill back to its source behavior
- **THEN** the skill or its references identify the source analysis file or DeepScientist source skill used during extraction

### Requirement: Validation
The implementation SHALL include a repository-runnable validation harness that checks skill structure, naming consistency, Imsight entrypoint formatting, self-containment, placeholder registration, stale terminology, resolved TBD placeholders, local reference integrity, manifest consistency, and removal of runtime-specific coupling.

#### Scenario: Structural validation runs
- **WHEN** the validation harness inspects the research-paradigm skillset
- **THEN** validation confirms each `isomer-rsch-*` skill folder has a valid `SKILL.md`, valid frontmatter, expected supporting resources, and directly linked one-level references

#### Scenario: Naming validation runs
- **WHEN** the validation harness inspects the research-paradigm skillset
- **THEN** validation confirms every skill folder, `SKILL.md` frontmatter `name:`, manifest `interface.display_name`, manifest `default_prompt`, and active role mapping uses `isomer-rsch-*` names consistently

#### Scenario: Imsight workflow formatting is validated
- **WHEN** the validation harness inspects an enriched `SKILL.md`
- **THEN** validation confirms it has a near-top `## Workflow`, numbered workflow steps, concise reference routing, and a fallback for tasks that do not map cleanly to the default steps

#### Scenario: Coupling validation runs
- **WHEN** the validation harness inspects active research-paradigm skill text
- **THEN** validation searches the research-paradigm skillset for DeepScientist-specific runtime terms, including artifact APIs, memory APIs, command wrappers, provider names, workspace terms, continuation scheduling terms, and concrete source paths, and confirms any remaining matches are provenance, adaptation notes, explicit mappings, deferred-resource notes, or explicit rejection notes

#### Scenario: Placeholder registry validation runs
- **WHEN** the validation harness finds a `[[tbd-surface:<id>]]` placeholder in active research-paradigm skill text
- **THEN** validation confirms the placeholder id is listed in a directly linked TBD registry and is not one of the resolved workspace, recording, lifecycle, CLI topic-context, or execution-extension placeholder ids

#### Scenario: Self-containment validation runs
- **WHEN** the validation harness inspects enriched skill entrypoints and linked references
- **THEN** validation confirms they do not actively depend on files outside their own skill directory, except for intentional shared-skill references when the bundle is installed as part of the research-paradigm subtree

#### Scenario: Guessed concrete surfaces are checked
- **WHEN** the validation harness inspects active research-paradigm skill text
- **THEN** validation searches for concrete DeepScientist-style paths, command wrappers, runner homes, and API calls, and confirms unsettled equivalents are marked `yet-to-be-determined` or represented by registered unresolved TBD-surface placeholders

#### Scenario: Repository command runs the harness
- **WHEN** a developer or agent runs the repository skillset validation command
- **THEN** the command validates `skillset/research-paradigm`, prints deterministic diagnostics as `path:line: code message`, and exits nonzero when validation errors exist

#### Scenario: Whole bundle validation surface is scanned
- **WHEN** the validation harness runs against `skillset/research-paradigm`
- **THEN** validation inspects every Markdown and YAML file in the subtree and classifies files or sections by role before applying strict checks or rule-specific allow zones

#### Scenario: Allow zones preserve explanatory mapping text
- **WHEN** stale source terms, former TBD ids, or source-runtime names appear inside configured provenance files, license notices, deferred-resource notes, source-term mapping sections, rejected-runtime sections, or resolved-surface mapping tables
- **THEN** validation allows those occurrences only for the matching rule and continues to reject the same terms when they appear as active skill guidance

#### Scenario: Stale lifecycle and workspace terms are reported
- **WHEN** active research-paradigm skill text uses Research Goal, Research Thread, Research Branch, or Isomer Workspace as current Isomer domain terms
- **THEN** validation reports the stale term and directs the skill text to use Research Topic, Research Inquiry, Research Inquiry Relationship, or Topic Workspace

#### Scenario: Resolved workspace path TBDs are reported
- **WHEN** active research-paradigm skill text emits an ordinary workspace path TBD placeholder such as `[[tbd-surface:path-topic-workspace]]`, `[[tbd-surface:path-agent-workspace]]`, `[[tbd-surface:path-run-logs]]`, `[[tbd-surface:path-experiment-output]]`, `[[tbd-surface:path-analysis-output]]`, `[[tbd-surface:path-paper-layout]]`, or `[[tbd-surface:path-figure-output]]`
- **THEN** validation reports the placeholder as resolved and directs the skill text to use Workspace Path Resolution, semantic workspace scopes, or semantic Artifact kinds

#### Scenario: Unregistered TBD surface is reported
- **WHEN** active research-paradigm skill text emits a `[[tbd-surface:<id>]]` placeholder whose id is absent from the directly linked TBD registry
- **THEN** validation reports the unregistered id and identifies the file and line that emitted it

#### Scenario: Shared TBD registry is canonical
- **WHEN** the validation harness validates `[[tbd-surface:<id>]]` placeholders or resolved former IDs anywhere in the research-paradigm subtree
- **THEN** validation treats `isomer-rsch-shared/references/tbd-surface-registry.md` as the canonical registry for the subtree

#### Scenario: Local TBD registry mirror drift is reported
- **WHEN** a directly loaded local contract file contains a `## TBD Surface Registry` mirror section
- **THEN** validation confirms the local mirror has exact resolved-ID coverage and normalized resolution text matching the shared registry, and reports missing IDs, extra IDs, or changed resolution meaning

#### Scenario: Hard-coded local and source-analysis paths are reported
- **WHEN** active research-paradigm skill text depends on local absolute paths, source-analysis paths, archived OpenSpec change paths, `extern/orphan` paths, DeepScientist runtime paths, or concrete runner homes outside an allowed provenance or deferred-resource zone
- **THEN** validation reports the hard-coded path and directs the skill text to use self-contained references, accepted Isomer contracts, or registered unresolved TBD-surface placeholders

#### Scenario: Broken local reference is reported
- **WHEN** a `SKILL.md` references a local `references/`, `assets/`, or `scripts/` path that does not exist inside the same skill directory
- **THEN** validation reports the broken reference with the referring `SKILL.md` file and line

#### Scenario: Manifest mismatch is reported
- **WHEN** a skill's `agents/openai.yaml` `interface.display_name` does not equal the skill folder and `SKILL.md` frontmatter name, or `interface.default_prompt` does not invoke the same `$isomer-rsch-*` skill
- **THEN** validation reports the manifest mismatch and identifies the affected manifest field

### Requirement: Workspace Path Resolution Consumption
The research-paradigm skillset SHALL consume the Workspace Path Resolution contract for ordinary files, workspaces, logs, and Artifact class locations.

#### Scenario: Shared registry reflects resolved path surfaces
- **WHEN** `isomer-rsch-shared/references/tbd-surface-registry.md` is inspected after this change
- **THEN** ordinary path surfaces for Topic Workspace, Workspace Runtime, Agent Workspace, Artifact layout, Run logs, experiment output, analysis output, paper layout, and figure output are removed as open TBDs or explicitly mapped to the Workspace Path Resolution contract

#### Scenario: Skill references request semantic outputs
- **WHEN** a research-stage skill needs to create intake notes, baseline records, experiment outputs, analysis results, figures, paper drafts, decisions, evidence, findings, handoffs, logs, or agent scratch files
- **THEN** the skill names the semantic Artifact kind or workspace scope rather than prescribing a concrete path

#### Scenario: Local contract copies stay consistent
- **WHEN** a local `isomer-research-contract.md` copy is inspected in an `isomer-rsch-*` skill directory
- **THEN** its path guidance matches the shared workspace path resolution contract and does not reintroduce ordinary path TBD placeholders

#### Scenario: Non-path TBD surfaces remain explicit
- **WHEN** a research-stage skill needs an unsettled runtime API, command surface, provider, schema, or policy
- **THEN** the skill continues to use the appropriate non-path TBD placeholder until that surface has its own accepted Isomer contract

#### Scenario: Validation checks resolved and unresolved surfaces
- **WHEN** implementation validation runs
- **THEN** it confirms ordinary workspace path TBDs were removed or mapped to the path resolver, non-path TBDs remain registered, and no skill reference depends on hard-coded DeepScientist paths or local absolute paths

### Requirement: Research Recording Contract Consumption
The research-paradigm skillset SHALL consume the Research Recording Contracts for durable record and validation surfaces.

#### Scenario: Shared registry reflects resolved recording surfaces
- **WHEN** `isomer-rsch-shared/references/tbd-surface-registry.md` is inspected after this change
- **THEN** `api-artifact-record`, `api-finding-query`, `api-gate`, `schema-decision-record`, `schema-evidence-item`, `schema-research-claim`, and `schema-gate` are removed as open TBDs or explicitly mapped to Research Recording Contracts

#### Scenario: Skill references use accepted record names
- **WHEN** a research-stage skill needs durable Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, or Gates
- **THEN** the skill names those accepted record types and the accepted recording APIs instead of a TBD placeholder

#### Scenario: Local contract copies stay consistent
- **WHEN** a local `isomer-research-contract.md` copy is inspected in an `isomer-rsch-*` skill directory
- **THEN** its recording guidance matches the shared Research Recording Contracts and does not reintroduce resolved recording TBD placeholders

#### Scenario: Non-recording TBD surfaces remain explicit
- **WHEN** a research-stage skill needs unsettled command execution, literature provider, scheduler policy, Skill Binding, Agent Team State, Stage Cursor, branching policy, baseline-waiver policy, or cost/privacy Gate policy
- **THEN** the skill continues to use the appropriate TBD placeholder until that surface has its own accepted Isomer contract

#### Scenario: Validation checks resolved and unresolved recording surfaces
- **WHEN** implementation validation runs
- **THEN** it confirms resolved recording TBDs were removed or mapped to the Research Recording Contracts, remaining TBDs are registered, and skill references do not invent concrete host APIs outside accepted contracts

### Requirement: Research Lifecycle State Consumption
The research-paradigm skillset SHALL consume Research Lifecycle State for execution levels, route relationships, Workflow Stage Cursor, Agent Team Instance lifecycle state, and branching policy.

#### Scenario: Shared registry reflects resolved lifecycle surfaces
- **WHEN** `isomer-rsch-shared/references/tbd-surface-registry.md` is inspected after this change
- **THEN** `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching` are removed as open TBDs or explicitly mapped to Research Lifecycle State

#### Scenario: Skill references use accepted lifecycle terms
- **WHEN** a research-stage skill needs Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Workflow Stage Cursor, or Agent Team Instance lifecycle state
- **THEN** the skill names those accepted lifecycle terms instead of stale terms or lifecycle TBD placeholders

#### Scenario: Research Inquiry is not parallel execution scope
- **WHEN** a research-stage skill describes parallel execution
- **THEN** it describes Topic-level parallelism across Agent Team Instances or Task-level parallelism across Agent Instances and does not assign parallel execution scope to Research Inquiry

#### Scenario: Local contract copies stay consistent
- **WHEN** a local `isomer-research-contract.md` copy is inspected in an `isomer-rsch-*` skill directory
- **THEN** its lifecycle guidance matches Research Lifecycle State and does not reintroduce Research Goal, Research Thread, Research Branch, Isomer Workspace, or resolved lifecycle TBD placeholders as active terms

#### Scenario: Non-lifecycle TBD surfaces remain explicit
- **WHEN** a research-stage skill needs unsettled command execution, scheduler behavior, literature provider, Skill Binding, baseline-waiver policy, cost/privacy Gate policy, or concrete Capability Binding behavior
- **THEN** the skill continues to use the appropriate TBD placeholder until that surface has its own accepted Isomer contract

#### Scenario: Validation checks stale and resolved lifecycle surfaces
- **WHEN** implementation validation runs
- **THEN** it confirms stale lifecycle terms are removed or confined to provenance and mapping notes, resolved lifecycle TBDs are removed or mapped to Research Lifecycle State, and remaining TBD placeholders are still registered

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
