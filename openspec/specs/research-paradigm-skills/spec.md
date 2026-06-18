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
- **WHEN** an extracted skill describes artifacts, memory, terminal execution, paper search, execution isolation, workflow progress, lifecycle state, or route branching
- **THEN** it uses Isomer concepts such as Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Topic Workspace, Workspace Runtime, Agent Workspace, Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Provenance Record, Workflow Stage Cursor, Operator Agent, Agent Role, Agent Instance, Agent Team Instance, Agent Team Instance lifecycle state, Capability Binding, Coordination Policy, and Execution Adapter

#### Scenario: Source-specific terms are bounded
- **WHEN** an extracted skill mentions a source-specific or stale term such as DeepScientist, `artifact.*`, `memory.*`, `bash_exec(...)`, DeepXiv, quest, Research Goal, Research Thread, Research Branch, Isomer Workspace, branch, worktree, `workspace_mode`, `continuation_policy`, `auto_continue`, or `wait_for_user_or_resume`
- **THEN** the mention is limited to provenance, adaptation notes, source-term mapping, or migration notes and is not a required runtime operation or active Isomer domain term

#### Scenario: Continuation policy is not ported
- **WHEN** an extracted skill preserves DeepScientist behavior about continuing, pausing, resuming, or monitoring long-running work
- **THEN** it describes the behavior through Agent Team Instance lifecycle state under Coordination Policy, paused waiting for Operator Agent instruction, Workflow Stage Cursor recommendations, Gates, Decision Records, Completion Watcher Contracts, or Signal Observations, and does not require an Isomer `continuation_policy` field

### Requirement: Unsettled Concrete Surfaces Are Explicit
The extracted skills SHALL mark unsettled commands, runtime APIs, providers, schemas, policies, storage roots, and generated layouts as `yet-to-be-determined` only when they are not settled by accepted Isomer designs such as Workspace Path Resolution, Research Recording Contracts, or Research Lifecycle State.

#### Scenario: Path surface is covered by workspace path resolution
- **WHEN** a skill needs an ordinary Topic Workspace, Workspace Runtime, Agent Workspace, Run log, experiment output, analysis output, paper output, figure output, or Artifact class location covered by the Workspace Path Resolution contract
- **THEN** the skill names the semantic workspace scope or Artifact kind and relies on the resolver instead of emitting a path TBD placeholder

#### Scenario: Recording surface is covered by research recording contracts
- **WHEN** a skill needs to record or query Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, or Gates covered by the Research Recording Contracts
- **THEN** the skill names the accepted record type or recording API instead of emitting `api-artifact-record`, `api-finding-query`, `api-gate`, `schema-decision-record`, `schema-evidence-item`, `schema-research-claim`, or `schema-gate` TBD placeholders

#### Scenario: Lifecycle surface is covered by research lifecycle state
- **WHEN** a skill needs Workflow Stage Cursor fields, Agent Team Instance lifecycle state, or Research Inquiry Relationship branching behavior covered by Research Lifecycle State
- **THEN** the skill names the accepted lifecycle object, state, relationship, or policy instead of emitting `schema-stage-cursor`, `schema-agent-team-state`, or `policy-branching` TBD placeholders

#### Scenario: Path surface remains unsettled outside the resolver
- **WHEN** a source skill uses a concrete path or filename that is not covered by the Workspace Path Resolution contract and no Isomer equivalent is settled by existing domain concepts or ADRs
- **THEN** the extracted skill marks that path or filename as `yet-to-be-determined` and states the missing design decision

#### Scenario: Runtime API is not settled
- **WHEN** a DeepScientist source skill depends on a command, tool wrapper, runner home, prompt injection mechanism, paper-search provider, scheduler behavior, Skill Binding, baseline-waiver policy, or cost/privacy policy with no settled Isomer equivalent
- **THEN** the extracted skill marks that surface as `yet-to-be-determined` and avoids inventing an implementation-specific default

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
The implementation SHALL include validation steps that check skill structure, naming consistency, Imsight entrypoint formatting, self-containment, placeholder registration, and removal of runtime-specific coupling.

#### Scenario: Structural validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms each `isomer-rsch-*` skill folder has a valid `SKILL.md`, valid frontmatter, expected supporting resources, and directly linked one-level references

#### Scenario: Naming validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms every skill folder, `SKILL.md` frontmatter `name:`, manifest `interface.display_name`, manifest `default_prompt`, and active role mapping uses `isomer-rsch-*` names consistently

#### Scenario: Imsight workflow formatting is validated
- **WHEN** the implementation is complete
- **THEN** validation confirms every enriched `SKILL.md` has a near-top `## Workflow`, numbered workflow steps, concise reference routing, and a fallback for tasks that do not map cleanly to the default steps

#### Scenario: Coupling validation runs
- **WHEN** the implementation is complete
- **THEN** validation searches the research-paradigm skillset for DeepScientist-specific runtime terms, including artifact APIs, memory APIs, command wrappers, provider names, workspace terms, continuation scheduling terms, and concrete source paths, and confirms any remaining matches are provenance, adaptation notes, explicit mappings, or explicit rejection notes

#### Scenario: Placeholder registry validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms every `[[tbd-surface:<id>]]` used by the enriched skills is listed in a directly linked TBD registry or is replaced with an existing registered placeholder

#### Scenario: Self-containment validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms enriched skill entrypoints and linked references do not actively depend on files outside their own skill directory, except for intentional shared-skill references when the bundle is installed as part of the research-paradigm subtree

#### Scenario: Guessed concrete surfaces are checked
- **WHEN** the implementation is complete
- **THEN** validation searches for concrete DeepScientist-style paths, command wrappers, runner homes, and API calls, and confirms unsettled equivalents are marked `yet-to-be-determined`

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
