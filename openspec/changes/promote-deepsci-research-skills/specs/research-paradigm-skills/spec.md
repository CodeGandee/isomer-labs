## MODIFIED Requirements

### Requirement: Research Paradigm Skillset Layout
The project SHALL provide a reusable production DeepSci research-paradigm skillset under `skillset/research-paradigm/deepsci/` using Codex skill folder layout and the `isomer-rsch-<purpose>` naming convention for research-stage method skills only.

#### Scenario: Production DeepSci root exists
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains production skill folders under `skillset/research-paradigm/deepsci/`
- **AND** it does not contain active `skillset/research-paradigm/v1/` or `skillset/research-paradigm/v2/` skill roots

#### Scenario: Retired v1 skill folders are absent
- **WHEN** the active research-paradigm skillset is inspected
- **THEN** `skillset/research-paradigm/v1/` is absent
- **AND** active docs do not route users to `isomer-rsch-*-v1` skills

#### Scenario: Production DeepSci skill folders exist
- **WHEN** the production DeepSci research-paradigm skillset is inspected
- **THEN** it contains `isomer-rsch-shared` and folders for scout, baseline, idea, optimize, experiment, analysis, decision, finalize, science, write, review, rebuttal, paper-outline, paper-plot, figure-polish, nature-data, nature-figure, nature-paper2ppt, nature-polishing, and workspace-mgr

#### Scenario: Migrated companion skills keep bounded traceability material
- **WHEN** a refactor-migrated production DeepSci companion skill is inspected
- **THEN** it MAY contain `migrate/`, `org/analysis/`, `org/src/`, and passive `templates/` material for migration review and provenance
- **AND** active execution guidance remains in `SKILL.md`, `agents/openai.yaml`, directly linked `references/`, active `assets/`, and active `scripts/`

#### Scenario: Skill frontmatter is valid
- **WHEN** each production DeepSci research-stage skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields
- **AND** the `name` field matches the suffixless `isomer-rsch-<purpose>` folder name

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Standalone skill bundle is self-contained
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** its active `SKILL.md` and directly linked active resources do not require files outside that skill's directory

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*`, `isomer-rsch-*-v1`, or `isomer-rsch-*-v2` as active skill folder names, frontmatter names, manifests, command examples, or role mappings

#### Scenario: Operator admin skills are excluded
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** Project Operator Session and Operator Agent orchestration skills are not stored or named as `isomer-rsch-*` skills and instead use the operator admin skillset

### Requirement: Generic Research Vocabulary
The production DeepSci skillset SHALL distinguish research-method semantics from Isomer platform implementation terms.

#### Scenario: Production skills use research-process terms
- **WHEN** a production DeepSci core skill describes the method it performs
- **THEN** it uses research-process terms such as frame, comparator, metric, hypothesis, route, experiment, result, analysis, claim, decision, blocker, limitation, and final summary

#### Scenario: Production skills use semantic placeholders for research objects
- **WHEN** a production DeepSci core skill needs to name a durable or reusable research object
- **THEN** it uses a registered semantic placeholder of the form `[[rsch-object:<id>]]`
- **AND** it does not require that placeholder to be stored as an Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, database row, workspace path, or storage label

#### Scenario: Storage-facing terms are bounded
- **WHEN** a production DeepSci skill mentions storage-facing terms such as Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, Workspace Path Resolution, Topic Workspace records, lifecycle rows, execution adapters, or database state
- **THEN** the mention is confined to provenance, migration notes, rejected-storage-binding notes, explicit statements that storage binding is deferred, placeholder binding pages, or workspace bootstrap guidance

#### Scenario: Source-specific terms remain bounded
- **WHEN** active production DeepSci guidance mentions a source-specific or stale term such as DeepScientist, quest, artifact operation, memory operation, command wrapper, source provider name, continuation scheduling, or source-local path
- **THEN** the mention is limited to provenance, adaptation notes, source-term mapping, rejected-runtime notes, or migration notes and is not a required active production operation

### Requirement: Shared Research Contract
The skillset SHALL include one production shared research contract that defines the concise methodology and semantic-placeholder contract for DeepSci skills.

#### Scenario: Production shared contract defines semantic placeholders
- **WHEN** `skillset/research-paradigm/deepsci/isomer-rsch-shared/SKILL.md` and its directly linked references are inspected
- **THEN** they define the production research loop, placeholder syntax, placeholder registry location, and rule that placeholders are not storage bindings

#### Scenario: Production stage skills reference shared rules
- **WHEN** a production DeepSci core skill needs common placeholder, handoff, evidence, or process discipline
- **THEN** it references `isomer-rsch-shared` instead of duplicating long shared rules or referencing retired generationed shared rules

#### Scenario: Production shared registry defines placeholder semantics
- **WHEN** the production semantic-placeholder registry is inspected
- **THEN** each placeholder entry defines id, meaning, minimum content, producer skills, consumer skills, and storage-binding status

### Requirement: DeepScientist Methodology Preservation
The skillset SHALL preserve the distilled DeepScientist-derived research process in production DeepSci skills while removing retired v1 compatibility material from the active tree.

#### Scenario: Production skills preserve core process rather than bookkeeping
- **WHEN** a production DeepSci core skill is inspected
- **THEN** it preserves the corresponding stage purpose, entry signals, central research actions, exit criteria, and route guardrails from the core process analysis
- **AND** it omits nonessential storage, runtime, provider, scheduler, lifecycle, and path bookkeeping from active instructions

#### Scenario: Production skills do not require source analysis at runtime
- **WHEN** a production DeepSci skill is executed by an agent
- **THEN** the skill contains enough local methodology guidance to run without reading `context/explore/...`, `extern/orphan/...`, archived OpenSpec files, or local absolute paths

#### Scenario: Source lineage remains traceable
- **WHEN** a reader wants to understand why a production DeepSci skill has its process shape
- **THEN** the research-paradigm README or nearby provenance material points to the local DeepScientist skill analysis and source lineage without making those paths active runtime dependencies

### Requirement: Imsight Workflow Entrypoints
Each production DeepSci `isomer-rsch-*` skill SHALL use a concise Imsight-compatible skill entrypoint structure while preserving trigger behavior and research guardrails.

#### Scenario: Workflow section is near the top
- **WHEN** a production DeepSci `SKILL.md` is inspected
- **THEN** it contains a near-top `## Workflow` section before long reference routing or detailed notes

#### Scenario: Workflow steps are methodology actions
- **WHEN** a production DeepSci `## Workflow` section is inspected
- **THEN** its numbered steps describe research actions, evidence checks, route choices, and outputs rather than source-runtime bookkeeping

#### Scenario: Workflow includes freeform fallback
- **WHEN** a production DeepSci `## Workflow` section is inspected
- **THEN** it allows the agent to handle user-specific research context without requiring a rigid schema beyond the skill's stated output contract

#### Scenario: Reference routing is explicit
- **WHEN** a production DeepSci skill has local references
- **THEN** its `SKILL.md` names which reference files to read for the relevant branch of work

### Requirement: Provenance and Licensing
The research-paradigm skillset SHALL preserve source lineage and license notices for production DeepSci material without keeping retired generation folders active.

#### Scenario: Production adapted materials identify source lineage
- **WHEN** a production DeepSci skill materially adapts DeepScientist-derived process content
- **THEN** the skill, shared reference, or research-paradigm provenance file identifies the corresponding source-analysis file or DeepScientist source skill used during distillation

#### Scenario: Source checkout is not a runtime dependency
- **WHEN** production DeepSci skill instructions are executed
- **THEN** they do not require the source checkout, archived v1 folders, or `skillset/research-paradigm/v2/` paths to exist

### Requirement: Validation
The repository SHALL provide deterministic validation for the production DeepSci research-paradigm skillset, including layout, naming, workflow, placeholder, binding, output-policy, and coupling checks.

#### Scenario: Structural validation runs
- **WHEN** the validation harness inspects `skillset/research-paradigm`
- **THEN** it validates the expected production DeepSci skill directory structure, required files, and active resource roles

#### Scenario: Expected production inventory is validated
- **WHEN** the validation harness inspects `skillset/research-paradigm/deepsci`
- **THEN** validation confirms the inventory contains the production core, companion, Nature-facing, shared, and workspace-manager skills listed in the skillset layout requirement
- **AND** validation does not require `v1` or `v2` skill roots

#### Scenario: Naming validation runs
- **WHEN** production DeepSci skill folders, frontmatter, manifests, and active references are inspected
- **THEN** validation reports active `isomer-rsch-*-v1`, `isomer-rsch-*-v2`, `research-paradigm/v1`, `research-paradigm/v2`, and `deepsci-v2` references unless they are explicitly classified as non-active provenance

#### Scenario: Imsight workflow formatting is validated
- **WHEN** production DeepSci `SKILL.md` files are inspected
- **THEN** validation confirms workflow sections, numbered workflow steps, active reference routing, and concise section introductions

#### Scenario: File roles are classified before strict checks
- **WHEN** validation scans a production DeepSci skill folder
- **THEN** it distinguishes active runtime files from migration, provenance, passive template, and source-copy material before enforcing active-guidance checks

#### Scenario: Coupling validation runs
- **WHEN** validation scans active production DeepSci guidance
- **THEN** it reports source runtime coupling, local absolute paths, source-analysis paths, archived OpenSpec paths, and unbounded DeepScientist runtime assumptions

#### Scenario: Placeholder registry validation runs
- **WHEN** validation inspects production semantic placeholders
- **THEN** it confirms placeholder syntax, registration, semantic fields, producer and consumer names, and storage-binding status

#### Scenario: Storage binding remains bounded
- **WHEN** the validation harness inspects active production DeepSci skill text
- **THEN** it permits storage guidance in binding and bootstrap material while rejecting unbounded concrete storage requirements in methodology prose

#### Scenario: Self-containment validation runs
- **WHEN** active production DeepSci `SKILL.md` files and directly linked active references are inspected
- **THEN** validation reports concrete broken local links and files outside the skill bundle that are required for runtime execution

#### Scenario: Repository command runs the harness
- **WHEN** the repository validation command for research-paradigm skills is run
- **THEN** it invokes the production DeepSci validation harness and reports deterministic diagnostics suitable for tests

#### Scenario: Validator tests cover active and non-active zones
- **WHEN** validator tests are inspected
- **THEN** they include fixtures for production DeepSci inventory, migrated companion-skill traceability directories, passive templates, active stale-term failures, allow-zone acceptance, concrete broken references, pattern references, placeholder registration, storage-binding deferral, structured binding guidance, output-policy guidance, commit-preference guidance, and deterministic CLI output

### Requirement: V2 Semantic Placeholder Contract
The production DeepSci research-paradigm skillset SHALL define semantic placeholders before binding research objects to Isomer storage.

#### Scenario: Placeholder syntax is stable
- **WHEN** a production DeepSci skill names a research object whose storage binding is deferred
- **THEN** it uses `[[rsch-object:<id>]]` syntax

#### Scenario: Placeholder ids are semantic
- **WHEN** a placeholder id is registered
- **THEN** the id names the research object meaning rather than a concrete path, database table, provider API, or lifecycle implementation

#### Scenario: Placeholder registry is authoritative for production
- **WHEN** production placeholder meaning is inspected
- **THEN** the authoritative definitions live in `skillset/research-paradigm/deepsci/isomer-rsch-shared/references/semantic-placeholders.md`

#### Scenario: Placeholder entry has minimum semantic fields
- **WHEN** a placeholder entry is inspected
- **THEN** it defines id, meaning, minimum content, producer skills, consumer skills, and storage-binding status

#### Scenario: Placeholder entry rejects premature storage binding
- **WHEN** a placeholder has no accepted storage binding yet
- **THEN** its registry entry records the binding as deferred rather than inventing a path or schema

### Requirement: V2 Core Research Process
The production DeepSci core skillset SHALL organize research conduction around the core process rather than around implementation bookkeeping.

#### Scenario: Core loop is documented
- **WHEN** `isomer-rsch-shared` is inspected
- **THEN** it documents the production loop as frame, comparator, hypothesis, experiment, analysis, decision, and finalize

#### Scenario: Optimize is an overlay
- **WHEN** `isomer-rsch-optimize` is inspected
- **THEN** it presents optimization as an overlay for candidate frontier search rather than as a separate storage lifecycle

#### Scenario: Science is a computation-validity companion
- **WHEN** `isomer-rsch-science` is inspected
- **THEN** it presents scientific computation, data, package, simulation, and model checks as companion validation work for any stage

#### Scenario: Each production stage declares semantic handoff
- **WHEN** any production DeepSci core skill is inspected
- **THEN** it declares semantic inputs, semantic outputs, evidence expectations, and next-route guidance

#### Scenario: Production guardrails preserve research judgment
- **WHEN** a production DeepSci core skill is inspected
- **THEN** it retains guardrails for evidence gaps, comparator uncertainty, failed experiments, claim limits, blocker escalation, and non-trivial route choices

### Requirement: V2 Research Workspace Manager Skill
The research-paradigm skillset SHALL include an `isomer-rsch-workspace-mgr` skill that performs research-specific Topic Workspace bootstrap after Topic Team Specialization and full Topic Workspace initialization.

#### Scenario: Workspace manager skill exists
- **WHEN** the production DeepSci research-paradigm skillset is inspected
- **THEN** it contains `skillset/research-paradigm/deepsci/isomer-rsch-workspace-mgr/SKILL.md` with valid frontmatter, workflow, reference routing, fallback guidance, and an `agents/openai.yaml` manifest that invokes `$isomer-rsch-workspace-mgr`

#### Scenario: Workspace manager runs after specialization
- **WHEN** the workspace manager starts
- **THEN** it requires a selected Research Topic, a fully initialized Topic Workspace, completed Topic Team Specialization material, Workspace Runtime readiness, and Agent Workspace context before ordinary production research skills rely on its bootstrap outputs

#### Scenario: Workspace manager is distinct from operator topic management
- **WHEN** workspace manager guidance is inspected
- **THEN** it states that `isomer-admin-topic-mgr` remains the operator initialized-topic manager while `isomer-rsch-workspace-mgr` owns research placeholder binding and production DeepSci storage bootstrap guidance

#### Scenario: Topic Service Master is optional
- **WHEN** no Topic Service Master is running
- **THEN** the Project Operator Session or Operator Agent may perform the same bounded workspace-manager pass from the Topic Workspace context

### Requirement: V2 Research Storage Bootstrap Contract
The `isomer-rsch-workspace-mgr` skill SHALL define consistent placeholders and outputs for research storage bootstrap, using the same placeholder registry style as the other production DeepSci research skills.

#### Scenario: Manager placeholder registry exists
- **WHEN** `isomer-rsch-workspace-mgr/migrate/placeholders.md` is inspected
- **THEN** it defines the manager-owned bootstrap placeholders

#### Scenario: Placeholder kinds use existing production storage mapping
- **WHEN** manager placeholders are inspected
- **THEN** every placeholder has a `Kind` value from the existing production placeholder kind set and maps to the storage item mapping for evidence, report, handoff, decision, runtime state, or related accepted kinds

#### Scenario: Storage bootstrap names semantic labels
- **WHEN** the workspace manager creates or updates a binding registry
- **THEN** it records semantic labels and binding status instead of writing anonymous paths

#### Scenario: Missing storage support becomes a blocker
- **WHEN** required storage or record support is unavailable
- **THEN** the workspace manager records the binding as planned, custom-needed, blocked, or deferred rather than inventing an untracked storage location

#### Scenario: Agent access plan preserves storage authority
- **WHEN** workspace manager guidance maps bindings for Agent Workspaces or Topic Actor Workspaces
- **THEN** it records the authoritative storage surface and access posture instead of copying ownership to the local actor workspace

### Requirement: Research Workspace Manager Validation
The research-paradigm validation harness SHALL recognize `isomer-rsch-workspace-mgr` as an expected production DeepSci skill and apply the normal production structure and placeholder checks to it.

#### Scenario: Validator expects workspace manager
- **WHEN** validation inspects production DeepSci skill inventory
- **THEN** it treats `isomer-rsch-workspace-mgr` as part of the expected skill set

#### Scenario: Validator checks manager placeholders
- **WHEN** validation inspects workspace-manager placeholder references
- **THEN** validation confirms those placeholders are registered in `isomer-rsch-workspace-mgr/migrate/placeholders.md`

### Requirement: V2 Skills Read Placeholder Bindings
Active production DeepSci research skills SHALL read local placeholder binding pages before writing durable placeholder outputs.

#### Scenario: Skill entrypoint names binding page
- **WHEN** an active production DeepSci research skill has placeholder definitions
- **THEN** its entrypoint or directly linked active reference names the local `placeholder-bindings.md` page as the binding authority

#### Scenario: Durable output uses binding page
- **WHEN** a production DeepSci skill step produces a durable placeholder output
- **THEN** the skill uses the binding page to choose the record kind, semantic label, format profile, command shape, and validation step

#### Scenario: Compatibility fallback remains bounded
- **WHEN** a production DeepSci skill still needs a source-shaped DeepScientist compatibility call
- **THEN** it marks the call as compatibility or provenance material rather than active required operation guidance

### Requirement: Binding Pages Preserve Workflow Flexibility
The production DeepSci research skills SHALL keep placeholders in workflow prose and bind them through local binding pages.

#### Scenario: Workflow placeholders are not replaced
- **WHEN** placeholder binding pages are added to production DeepSci skills
- **THEN** workflow prose keeps the semantic placeholder token rather than replacing it with a concrete path, table, or storage item name

#### Scenario: Binding updates do not rewrite method prose
- **WHEN** storage bindings change
- **THEN** implementation updates binding pages and validation expectations without rewriting unrelated methodology steps

### Requirement: Writing Artifacts Use Paper-Line Placeholder Bindings
The production DeepSci skillset SHALL map writing-related placeholders to paper-line storage profiles through local `placeholder-bindings.md` pages while preserving placeholders in workflow prose.

#### Scenario: Paper contract binding uses a paper contract view
- **WHEN** a production DeepSci skill binds a placeholder that represents the active paper contract, selected outline, evidence view, paper view, section writing plan, or claim-evidence boundary
- **THEN** the binding uses an appropriate paper-line view or structured record profile

#### Scenario: Paper control surfaces use view records
- **WHEN** a production DeepSci skill binds a placeholder that represents the paper evidence ledger, experiment matrix, manuscript validation, outline validation, paper-line state, or other paper control surface
- **THEN** the binding uses a queryable view record or structured profile that preserves control metadata

#### Scenario: Paper bodies use artifact records
- **WHEN** a production DeepSci skill binds a placeholder that represents manuscript drafts, LaTeX material, bibliography files, compile reports, PDFs, review reports, rebuttal packets, response letters, final summaries, or paper bundle manifests
- **THEN** the binding uses an accepted artifact or structured output profile appropriate to the body

#### Scenario: Paper work queues use task records when resumable
- **WHEN** a production DeepSci skill binds a placeholder that represents a resumable writing plan, reviewer-linked evidence TODO, or paper-facing work queue
- **THEN** the binding uses a task-oriented record or structured profile that can be resumed

#### Scenario: Binding commands include queryable paper metadata
- **WHEN** a production DeepSci skill binding provides an `isomer-cli ext research records` create or update command for a writing-related placeholder
- **THEN** it includes stable metadata needed to query paper state, producer skill, consumer skill, topic actor context, and lifecycle context when applicable

#### Scenario: Binding convention avoids paper-specific semantic labels
- **WHEN** writing-related production DeepSci binding pages are updated
- **THEN** they preserve general placeholder semantics and use paper-specific detail in binding metadata rather than renaming placeholder ids unnecessarily

#### Scenario: Workflow placeholders remain stable
- **WHEN** paper-line bindings change
- **THEN** workflow prose still uses the existing placeholder token unless the placeholder meaning itself changes

#### Scenario: Placeholder registries change only for real drift
- **WHEN** implementation updates paper-line binding rows
- **THEN** it updates the semantic placeholder registry only when the placeholder's meaning, minimum content, producer, consumer, or storage-binding status changes

### Requirement: Research Workspace Bootstrap Supports Actor Topology
The production DeepSci research workspace bootstrap SHALL support base topic readiness, Topic Actor readiness, and optional formal team readiness as composable topology layers.

#### Scenario: Bootstrap accepts Topic Actor readiness
- **WHEN** `isomer-rsch-workspace-mgr` or its successor runs for human-orchestrated research
- **THEN** it can bootstrap a Topic Actor's research recording and placeholder-binding posture without requiring a formal Agent Team

#### Scenario: Placeholder binding index points to skill-local authority
- **WHEN** the bootstrap creates a placeholder binding index
- **THEN** each entry points back to the owning production DeepSci skill's `placeholder-bindings.md` authority

#### Scenario: Bootstrap keeps formal team checks when present
- **WHEN** formal Agent Team specialization material is present
- **THEN** the bootstrap records that readiness layer without requiring it for plain Topic Actor work

### Requirement: V2 Skills Read Placeholder Bindings from Actor Workspaces
The production DeepSci research skills SHALL use skill-local placeholder binding guidance to map workflow placeholders to Topic Workspace records from Topic Actor Workspaces, topic-main, or formal Agent Workspaces.

#### Scenario: Actor skill run resolves placeholders through bindings
- **WHEN** a Topic Actor runs a production DeepSci research skill from its Topic Actor Workspace
- **THEN** the skill resolves accepted artifact writes through the active binding page and workspace-manager bootstrap output before writing durable records

#### Scenario: Missing binding blocks accepted record write
- **WHEN** a production DeepSci skill needs to write an accepted artifact but no binding exists for the placeholder
- **THEN** the skill records a blocker or routes to workspace bootstrap instead of inventing an unregistered local path

### Requirement: V2 Research Workspace Manager Owns V2 Bootstrap
The production DeepSci research-paradigm skillset SHALL make `isomer-rsch-workspace-mgr` the owner of production research workspace bootstrap.

#### Scenario: Production bootstrap consumes operator readiness
- **WHEN** `isomer-rsch-workspace-mgr` prepares production research workspace readiness for a Topic Workspace
- **THEN** it consumes operator-produced Topic Workspace, Topic Actor, and environment readiness evidence
- **AND** it does not require operator skills to validate selected production DeepSci skills, placeholder binding files, placeholder binding registries, or accepted research artifact command shapes

#### Scenario: Production bootstrap reports research recording guidance
- **WHEN** `isomer-rsch-workspace-mgr` completes production bootstrap
- **THEN** it reports selected production skill readiness, placeholder binding entrypoints, research storage or record guidance, actor access plans, and accepted research artifact recording instructions when those are in scope

#### Scenario: Actor access plan preserves actor metadata
- **WHEN** production bootstrap includes human-orchestrated Topic Actors
- **THEN** it preserves actor identity and workspace metadata in research recording guidance
- **AND** it adds production-specific recording metadata only inside research workspace outputs

### Requirement: V2 Package Setup Routes to Topic Manager
Active production DeepSci skills SHALL route package installation, package update, package removal, and package verification needs to `isomer-admin-topic-mgr` environment commands instead of installing packages directly.

#### Scenario: Missing Python package routes to topic manager
- **WHEN** a production DeepSci research skill detects that a required Python package is missing from the selected Topic Workspace environment
- **THEN** it routes package installation to `isomer-admin-topic-mgr` environment commands

#### Scenario: Missing R package routes to topic manager
- **WHEN** a production DeepSci research skill detects that a required R package is missing from the selected Topic Workspace environment
- **THEN** it routes package installation to `isomer-admin-topic-mgr` environment commands

#### Scenario: Package update or removal request routes to topic manager
- **WHEN** a production DeepSci research skill needs a package update, package downgrade, or package removal to proceed safely
- **THEN** it routes the mutation to `isomer-admin-topic-mgr` environment commands

#### Scenario: Package readiness evidence is consumed after verification
- **WHEN** `isomer-admin-topic-mgr` reports package readiness evidence for the selected Topic Workspace
- **THEN** the production DeepSci research skill may continue the blocked workflow from the same selected Topic Workspace context

### Requirement: V2 Skills Author Structured Accepted Outputs
Active production DeepSci skills SHALL treat accepted durable research outputs as structured payloads when their placeholder binding names a structured Artifact Format Profile or schema/template inputs.

#### Scenario: Skill routes accepted output through binding
- **WHEN** a production DeepSci skill produces an accepted durable output for a registered placeholder with a structured binding
- **THEN** it follows the binding's format profile, schema or template refs, validation command, render mode, and naming guidance

#### Scenario: Skill authors payload before generated Markdown
- **WHEN** a production DeepSci skill needs to create a structured accepted artifact
- **THEN** it authors the structured payload source and lets the record pipeline render Markdown when Markdown materialization is requested

#### Scenario: Methodology prose remains storage-light
- **WHEN** active production DeepSci `SKILL.md` prose describes the research method
- **THEN** it keeps storage details in binding or bootstrap guidance rather than turning the methodology into record API instructions

### Requirement: V2 Structured Payload Guidance Is Self-contained
Active production DeepSci skill bundles SHALL provide enough local guidance for an agent to produce structured payloads for their accepted outputs without reading discarded topic artifacts or external migration notes.

#### Scenario: Binding page names payload expectations
- **WHEN** a production DeepSci skill owns placeholders that produce structured records
- **THEN** its binding page names payload file role, required format profile, schema or schema-bearing format profile, template ref when applicable, generated content name when durable Markdown is expected, and validation command shape

#### Scenario: Active accepted-output set is covered
- **WHEN** active production DeepSci placeholder bindings are updated for structured records
- **THEN** every active production accepted-output placeholder family that remains in scope has an explicit `isomer:deepsci/record-format/*` profile or an intentional non-structured exclusion recorded in the binding guidance

#### Scenario: Agent can repair validation errors
- **WHEN** `isomer-cli ext research records validate` returns schema diagnostics for a production DeepSci skill payload
- **THEN** local binding or reference guidance gives the agent enough context to repair the payload source

#### Scenario: Generated Markdown is not edited as source
- **WHEN** a production DeepSci skill creates Markdown through the structured record pipeline
- **THEN** it treats generated Markdown as an output view rather than the authoritative structured source

### Requirement: Research Skill Validation Allows Accepted Structured Bindings
The research-paradigm validation harness SHALL allow accepted payload-first storage guidance in active production DeepSci placeholder binding material while continuing to reject unbounded runtime coupling in methodology prose.

#### Scenario: Payload-first binding is allowed
- **WHEN** validation scans active production DeepSci placeholder binding pages
- **THEN** it permits `isomer-cli ext research records` commands, format profile refs, schema refs, template refs, payload file roles, validation commands, and generated content names

#### Scenario: Database details remain disallowed in skill prose
- **WHEN** validation scans active production DeepSci `SKILL.md` methodology prose and active references
- **THEN** it reports database or implementation details that are not confined to binding, bootstrap, validation, or provenance material

#### Scenario: Direct Markdown source guidance is reported
- **WHEN** validation scans active production structured-output guidance and finds direct Markdown body authoring presented as the normal accepted-artifact source of truth
- **THEN** it reports the binding row or guidance block

### Requirement: Research Skills Resolve Worker Output Policy
Active production DeepSci skills that write plain files SHALL resolve the current worker output policy through `isomer-cli` before choosing output paths.

#### Scenario: Plain file writing requires output policy
- **WHEN** a production DeepSci research skill will write plain generated outputs such as JSON payload staging files, Markdown drafts, CSVs, figures, paper previews, paper builds, or local reports
- **THEN** it instructs the agent to resolve the current worker output policy with `isomer-cli` before choosing paths

#### Scenario: Durable records still use record bindings
- **WHEN** a production DeepSci research skill creates an accepted Artifact, Evidence Item, Run record, Decision Record, View Manifest, or other durable research record
- **THEN** it uses placeholder binding and record guidance rather than the plain-file output policy as the authority

#### Scenario: Operation outputs use operation sets
- **WHEN** a production DeepSci research skill writes multiple plain outputs for one research operation
- **THEN** it keeps those files under the configured operation output root or the default managed operation output root

### Requirement: Research Skills Apply Post-Operation Commit Preference
Active production DeepSci skills SHALL check the effective `commit_after_operation` preference after research operations that write files and apply it as a post-action step.

#### Scenario: Commit preference true triggers Git status and commit
- **WHEN** a production DeepSci research operation writes files and `isomer-cli` reports that `commit_after_operation` is true
- **THEN** the skill instructs the agent to inspect Git status and commit the relevant operation changes after the operation completes

#### Scenario: Commit preference false leaves workspace uncommitted
- **WHEN** a production DeepSci research operation writes files and `isomer-cli` reports that `commit_after_operation` is false
- **THEN** the skill instructs the agent to leave the workspace uncommitted and report the changed paths

#### Scenario: Git ignore controls what can be committed
- **WHEN** post-operation commit guidance runs
- **THEN** it relies on the workspace's generated `.gitignore` and Git status to determine tracked and untracked files instead of duplicating track or untrack policy in the skill

### Requirement: Research Skill Validation Covers Output Policy Guidance
The research-paradigm validation harness SHALL report active production DeepSci research skill entrypoints or references that write plain files without referencing worker output policy resolution.

#### Scenario: Missing output policy guidance is reported
- **WHEN** validation inspects an active production DeepSci research skill that mentions plain file outputs but lacks output-policy resolution guidance
- **THEN** validation reports the skill

#### Scenario: Commit preference guidance is required
- **WHEN** validation inspects an active production DeepSci research skill that performs research operations with file writes
- **THEN** validation reports the skill if it does not require checking the effective `commit_after_operation` preference as a post-action step

#### Scenario: Non-active material is exempt
- **WHEN** validation inspects migration, provenance, passive template, or source-copy material
- **THEN** output-policy and commit-preference checks do not apply unless that material is linked as active runtime guidance
