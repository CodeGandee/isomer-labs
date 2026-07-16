# research-paradigm-skills Specification

## Purpose
Define the reusable Isomer Labs research-paradigm skillset, including portable research-stage skills, shared evidence vocabulary, generic agent mappings, provenance handling, Imsight skill-entrypoint structure, and validation rules that prevent DeepScientist runtime coupling from becoming an Isomer requirement.
## Requirements

### Requirement: Research Paradigm Skillset Layout
The project SHALL provide a reusable production DeepSci research-paradigm skillset under `skillset/research-paradigm/deepsci/` using Codex skill folder layout and the `isomer-deepsci-<purpose>` naming convention for research-stage method skills only.

#### Scenario: Production DeepSci root exists
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains production skill folders under `skillset/research-paradigm/deepsci/`
- **AND** it does not contain active retired-generation or temporary-generation skill roots

#### Scenario: Retired v1 skill folders are absent
- **WHEN** the active research-paradigm skillset is inspected
- **THEN** retired first-generation research skill folders are absent
- **AND** active docs do not route users to `isomer-deepsci-*-v1` skills

#### Scenario: Production DeepSci skill folders exist
- **WHEN** the production DeepSci research-paradigm skillset is inspected
- **THEN** it contains `isomer-deepsci-shared` and folders for scout, baseline, idea, optimize, experiment, analysis, decision, finalize, science, write, review, rebuttal, paper-outline, paper-plot, figure-polish, nature-data, nature-figure, nature-paper2ppt, nature-polishing, workspace-mgr, and pipeline

#### Scenario: Migrated production DeepSci companion skills keep bounded traceability material
- **WHEN** a refactor-migrated production DeepSci companion skill is inspected
- **THEN** it MAY contain `migrate/`, `org/analysis/`, `org/src/`, and passive `templates/` material for migration review and provenance
- **AND** active execution guidance remains in `SKILL.md`, `agents/openai.yaml`, directly linked `references/`, active `assets/`, and active `scripts/`

#### Scenario: Skill frontmatter is valid
- **WHEN** each production DeepSci research-stage skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields
- **AND** the `name` field matches the suffixless `isomer-deepsci-<purpose>` folder name

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Standalone skill bundle is self-contained
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** its active `SKILL.md` and directly linked active resources do not require files outside that skill's directory

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*` as active skill folder names, frontmatter names, manifests, or role mappings

#### Scenario: Operator skills are excluded
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** Project Operator Session and Operator Agent orchestration skills are not stored or named as `isomer-deepsci-*` skills and instead use the operator skillset

### Requirement: Generic Research Vocabulary
The generationed skillset SHALL distinguish research-method semantics from Isomer platform implementation terms.

#### Scenario: Production DeepSci uses research-process terms
- **WHEN** a production DeepSci core skill describes the method it performs
- **THEN** it uses research-process terms such as frame, comparator, metric, hypothesis, route, experiment, result, analysis, claim, decision, blocker, limitation, and final summary

#### Scenario: Production DeepSci uses semantic placeholders for research objects
- **WHEN** a production DeepSci core skill needs to name a durable or reusable research object
- **THEN** it uses a registered semantic placeholder of the form `[[rsch-object:<id>]]`
- **AND** it does not require that placeholder to be stored as an Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, database row, workspace path, or storage label

#### Scenario: Production DeepSci storage-facing terms are bounded
- **WHEN** a production DeepSci skill mentions storage-facing terms such as Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, Workspace Path Resolution, Topic Workspace records, lifecycle rows, execution adapters, or database state
- **THEN** the mention is confined to provenance, migration notes, rejected-storage-binding notes, or explicit statements that storage binding is deferred

#### Scenario: V1 may retain translated implementation vocabulary
- **WHEN** a v1 preserved skill is inspected
- **THEN** it may retain the existing Isomer translation of DeepScientist storage, runtime, lifecycle, and recording terms
- **AND** v1 documentation identifies the content as preserved historical generation material rather than the concise production DeepSci methodology contract

#### Scenario: Source-specific terms remain bounded
- **WHEN** any generation mentions a source-specific or stale term such as DeepScientist, quest, artifact operation, memory operation, command wrapper, source provider name, continuation scheduling, or source-local path
- **THEN** the mention is limited to provenance, adaptation notes, source-term mapping, rejected-runtime notes, or migration notes and is not a required active production DeepSci operation

### Requirement: Shared Research Contract
The skillset SHALL include generation-specific shared research contracts, with v1 preserving the current contract and production DeepSci defining the concise methodology and semantic-placeholder contract.

#### Scenario: V1 shared contract is preserved
- **WHEN** the v1 generation is inspected
- **THEN** it contains `isomer-deepsci-shared/SKILL.md` migrated from the previous `isomer-deepsci-shared` skill with generation-suffixed names

#### Scenario: Production DeepSci shared contract defines semantic placeholders
- **WHEN** `skillset/research-paradigm/deepsci/isomer-deepsci-shared/SKILL.md` and its directly linked references are inspected
- **THEN** they define the production DeepSci research loop, placeholder syntax, placeholder registry location, and rule that placeholders are not storage bindings

#### Scenario: Production DeepSci stage skills reference production DeepSci shared rules
- **WHEN** a production DeepSci core skill needs common placeholder, handoff, evidence, or process discipline
- **THEN** it references `isomer-deepsci-shared` instead of duplicating long shared rules or referencing v1 shared rules

#### Scenario: Production DeepSci shared registry defines placeholder semantics
- **WHEN** the production DeepSci semantic-placeholder registry is inspected
- **THEN** each placeholder entry defines id, meaning, minimum content, producer skills, consumer skills, and storage-binding status

### Requirement: DeepScientist Methodology Preservation
The skillset SHALL preserve DeepScientist-derived material in v1 while distilling production DeepSci to the core research process described by the local DeepScientist skill analysis.

#### Scenario: V1 preserves existing source-derived material
- **WHEN** v1 skill folders are inspected
- **THEN** they retain the existing DeepScientist-derived method, references, provenance, and license context except for generation-suffix renames required by this change

#### Scenario: Production DeepSci preserves core process rather than bookkeeping
- **WHEN** a production DeepSci core skill is inspected
- **THEN** it preserves the corresponding stage purpose, entry signals, central research actions, exit criteria, and route guardrails from the core process analysis
- **AND** it omits nonessential storage, runtime, provider, scheduler, lifecycle, and path bookkeeping from active instructions

#### Scenario: Production DeepSci does not require source analysis at runtime
- **WHEN** a production DeepSci skill is executed by an agent
- **THEN** the skill contains enough local methodology guidance to run without reading `context/explore/...`, `extern/orphan/...`, archived OpenSpec files, or local absolute paths

#### Scenario: Source lineage remains traceable
- **WHEN** a reader wants to understand why a production DeepSci skill has its process shape
- **THEN** the research-paradigm README or nearby provenance material points to the local DeepScientist skill analysis and source lineage without making those paths active runtime dependencies

### Requirement: Progressive Disclosure
The skillset SHALL keep active skill entrypoints concise, move long reusable method detail into one-level local active resources, and keep migration or source-copy material bounded from active execution guidance.

#### Scenario: Long methodology detail is moved to active resources
- **WHEN** a skill needs templates, checklists, long playbooks, route examples, operational notes, or boundary cases for active use
- **THEN** the skill stores them under that skill's active `references/`, `assets/`, or `scripts/` directory and links them directly from `SKILL.md`

#### Scenario: Active skill bundle is self-contained
- **WHEN** an enriched skill's active `SKILL.md` and directly linked active references are inspected
- **THEN** they do not require `context/explore/...`, `extern/orphan/...`, archived OpenSpec files, local absolute paths, or other files outside that skill's directory to execute the skill

#### Scenario: Source provenance remains traceable
- **WHEN** source text, templates, scripts, assets, or reference files are copied or materially adapted
- **THEN** the target skill includes nearby provenance that identifies the DeepScientist source skill and applicable license context without making the source tree a runtime dependency

#### Scenario: Migration notes and source copies are non-active traceability material
- **WHEN** a refactor-migrated skill contains `migrate/`, `org/analysis/`, `org/src/`, passive `templates/`, license notices, or deferred-resource notes
- **THEN** those files are classified as migration, provenance, passive template, or source-copy material and are not required runtime inputs for invoking the skill

#### Scenario: Scripts and assets are sanitized before active import
- **WHEN** source scripts or assets are imported into an active `scripts/` or `assets/` directory
- **THEN** they are directly useful for the skill and do not contain source-local user paths, demo-output defaults, private paths, unsatisfied hard dependencies, or DeepScientist runtime assumptions as active behavior

#### Scenario: No extraneous active documentation is added
- **WHEN** a skill folder's active runtime surface is inspected
- **THEN** it contains only files that directly support skill use, such as `SKILL.md`, `agents/openai.yaml`, `references/`, `assets/`, `scripts/`, and explicitly bounded non-active traceability directories

### Requirement: Imsight Workflow Entrypoints
Each production DeepSci `isomer-deepsci-*-production DeepSci` skill SHALL use a concise Imsight-compatible skill entrypoint structure while preserving trigger behavior and research guardrails.

#### Scenario: Workflow section is near the top
- **WHEN** a production DeepSci `SKILL.md` is inspected
- **THEN** it has a near-top `## Workflow` section before detailed guardrail, placeholder, or provenance sections

#### Scenario: Workflow steps are methodology actions
- **WHEN** a production DeepSci `## Workflow` section is inspected
- **THEN** it uses numbered steps that name research-method actions rather than storage, path, adapter, scheduler, or database actions

#### Scenario: Workflow includes freeform fallback
- **WHEN** a production DeepSci `## Workflow` section is inspected
- **THEN** it tells the agent to use its native planning tool to build and execute a step-by-step plan from the skill's constraints and user request when the task does not map cleanly to the default steps

#### Scenario: Reference routing is explicit
- **WHEN** a production DeepSci skill has local references
- **THEN** its entrypoint states which references to read first and which references to read for route-specific, placeholder-specific, validation, or provenance needs

### Requirement: Generic Agent Mapping
The team documentation SHALL map generic research agents to the extracted `isomer-deepsci-*` skills without making the skills depend on one team topology.

#### Scenario: Generic role map exists
- **WHEN** the updated team documentation is inspected
- **THEN** it defines generic research roles and lists the `isomer-deepsci-*` research-paradigm skills installed for each role

#### Scenario: Skill bundles are topology-neutral
- **WHEN** an extracted skill is inspected
- **THEN** it does not require a specific Houmao specialist name, mailbox route, gateway, credential, or agent topology to perform its research operation

### Requirement: Provenance and Licensing
The implementation SHALL preserve source provenance and license notices for copied, moved, or adapted DeepScientist-derived material across both generations.

#### Scenario: V1 moved materials keep license notices
- **WHEN** existing research-paradigm skills are moved into v1
- **THEN** the v1 generation retains nearby Apache 2.0 or upstream license notices and provenance files that applied before the move

#### Scenario: Production DeepSci adapted materials identify source lineage
- **WHEN** a production DeepSci skill materially adapts DeepScientist-derived process content
- **THEN** the production DeepSci skill, production DeepSci shared reference, or research-paradigm provenance file identifies the corresponding source-analysis file or DeepScientist source skill used during distillation

#### Scenario: Source checkout is not a runtime dependency
- **WHEN** production DeepSci skill instructions are executed
- **THEN** they do not require the local `extern/orphan` source checkout to be present, except as optional provenance context for maintainers

### Requirement: Validation
The implementation SHALL include a repository-runnable validation harness that checks skill structure, naming consistency, Imsight entrypoint formatting, self-containment, placeholder registration, stale terminology, resolved TBD placeholders, local reference integrity, manifest consistency, and removal of runtime-specific coupling with file-role-aware rules.

#### Scenario: Structural validation runs
- **WHEN** the validation harness inspects the research-paradigm skillset
- **THEN** validation confirms each expected `isomer-deepsci-*` skill folder has a valid `SKILL.md`, valid frontmatter, expected supporting resources, and directly linked one-level active references

#### Scenario: Expected production inventory is validated
- **WHEN** the validation harness inspects `skillset/research-paradigm/deepsci`
- **THEN** validation confirms the production DeepSci inventory contains the current core, companion, Nature-facing, shared, and workspace-manager skills listed in the skillset layout requirement
- **AND** validation does not require retired-generation skill roots

#### Scenario: Naming validation runs
- **WHEN** the validation harness inspects the research-paradigm skillset
- **THEN** validation confirms every active skill folder, `SKILL.md` frontmatter `name:`, manifest `interface.display_name`, manifest `default_prompt`, and active role mapping uses `isomer-deepsci-*` versioned names consistently

#### Scenario: Imsight workflow formatting is validated
- **WHEN** the validation harness inspects an enriched active `SKILL.md`
- **THEN** validation confirms it has a near-top `## Workflow`, numbered workflow steps, concise reference routing, and a fallback for tasks that do not map cleanly to the default steps

#### Scenario: File roles are classified before strict checks
- **WHEN** the validation harness runs against `skillset/research-paradigm`
- **THEN** validation classifies Markdown, YAML, scripts, assets, templates, migration notes, provenance notes, source-analysis files, and source-copy files by role before applying active-guidance checks or rule-specific allow zones

#### Scenario: Coupling validation runs
- **WHEN** the validation harness inspects active research-paradigm skill text
- **THEN** validation searches for DeepScientist-specific runtime terms, including artifact APIs, memory APIs, command wrappers, provider names, workspace terms, continuation scheduling terms, and concrete source paths, and confirms any remaining matches are provenance, adaptation notes, explicit mappings, deferred-resource notes, explicit rejection notes, or clearly optional compatibility bridges through accepted Isomer extension points

#### Scenario: Placeholder registry validation runs
- **WHEN** the validation harness finds a `[[tbd-surface:<id>]]`, `[[rsch-object:<id>]]`, or angle-bracket migration placeholder in active research-paradigm skill text
- **THEN** validation confirms the placeholder id is listed in the directly linked shared registry or skill-local migration placeholder registry, and confirms unresolved storage binding is not treated as a concrete runtime API

#### Scenario: Production DeepSci storage binding remains deferred
- **WHEN** the validation harness inspects active production DeepSci skill text
- **THEN** validation reports active requirements to create concrete Artifact storage, concrete host API records, or source-runtime storage paths unless they are explicitly framed as unsettled, optional source-compatible bridges, provenance, or migration notes

#### Scenario: Self-containment validation runs
- **WHEN** the validation harness inspects enriched skill entrypoints and linked active references
- **THEN** validation confirms they do not actively depend on files outside their own skill directory, except for intentional shared-skill references when the bundle is installed as part of the research-paradigm subtree

#### Scenario: Guessed concrete surfaces are checked
- **WHEN** the validation harness inspects active research-paradigm skill text
- **THEN** validation searches for concrete DeepScientist-style paths, command wrappers, runner homes, and API calls, and confirms unsettled equivalents are marked `yet-to-be-determined`, represented by registered unresolved TBD-surface placeholders, or confined to non-active traceability material

#### Scenario: Repository command runs the harness
- **WHEN** a developer or agent runs the repository skillset validation command
- **THEN** the command validates `skillset/research-paradigm`, prints deterministic diagnostics as `path:line: code message`, and exits nonzero when validation errors exist

#### Scenario: Whole bundle validation surface is scanned
- **WHEN** the validation harness runs against `skillset/research-paradigm`
- **THEN** validation inspects Markdown, YAML, active scripts, active assets, passive templates, migration notes, provenance notes, source-analysis files, and source-copy files in the subtree with role-aware rule application

#### Scenario: Allow zones preserve explanatory mapping text
- **WHEN** stale source terms, former TBD ids, source-runtime names, or source-local paths appear inside configured provenance files, license notices, deferred-resource notes, source-term mapping sections, rejected-runtime sections, resolved-surface mapping tables, migration notes, source-analysis files, source-copy files, or passive templates
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
- **WHEN** the validation harness validates `[[tbd-surface:<id>]]` placeholders or resolved former IDs anywhere in active research-paradigm guidance
- **THEN** validation treats `isomer-deepsci-shared/references/tbd-surface-registry.md` as the canonical registry for the subtree

#### Scenario: Local TBD registry mirror drift is reported
- **WHEN** a directly loaded local contract file contains a `## TBD Surface Registry` mirror section
- **THEN** validation confirms the local mirror has exact resolved-ID coverage and normalized resolution text matching the shared registry, and reports missing IDs, extra IDs, or changed resolution meaning

#### Scenario: Hard-coded local and source-analysis paths are reported
- **WHEN** active research-paradigm skill text depends on local absolute paths, source-analysis paths, archived OpenSpec change paths, `extern/orphan` paths, DeepScientist runtime paths, or concrete runner homes outside an allowed provenance, migration, source-copy, passive-template, or deferred-resource zone
- **THEN** validation reports the hard-coded path and directs the skill text to use self-contained references, accepted Isomer contracts, or registered unresolved TBD-surface placeholders

#### Scenario: Concrete broken local reference is reported
- **WHEN** a `SKILL.md` references a concrete local `references/`, `assets/`, or `scripts/` path that does not exist inside the same skill directory
- **THEN** validation reports the broken reference with the referring `SKILL.md` file and line

#### Scenario: Pattern reference is not treated as a concrete broken path
- **WHEN** a `SKILL.md` describes a placeholder path pattern such as `references/packages/<package_id>.md` or `scripts/<script>.py`
- **THEN** validation treats the pattern as documentation of a route-specific resource shape rather than a literal required local file

#### Scenario: Manifest mismatch is reported
- **WHEN** a skill's `agents/openai.yaml` `interface.display_name` does not equal the skill folder and `SKILL.md` frontmatter name, or `interface.default_prompt` does not invoke the same `$isomer-deepsci-*` skill
- **THEN** validation reports the manifest mismatch and identifies the affected manifest field

#### Scenario: Validator tests cover active and non-active zones
- **WHEN** unit tests exercise the research-paradigm validation harness
- **THEN** they include fixtures for expanded production DeepSci inventory, migrated companion-skill traceability directories, passive templates, active stale-term failures, allow-zone acceptance, concrete broken references, pattern references, placeholder registration, storage-binding deferral, and deterministic CLI output

### Requirement: Isomer Project Operator and Topic Service Skills
The repository SHALL include provider-neutral skill instructions for Project Operator Sessions, Operator Agents, and Topic Service Agents to perform Topic Team Specialization and instantiate topic teams from Domain Agent Team Templates.

#### Scenario: Project awareness skill exists
- **WHEN** an agent is pointed at an Isomer Project root with a topic prompt, topic file, or existing Research Topic ref
- **THEN** a skill instructs it to resolve the project root, inspect Project Manifest, read supplied topic material, list Research Topics, locate or create the selected Topic Workspace, discover Domain Agent Team Templates, and discover Topic Service Agents

#### Scenario: Service request routing skill exists
- **WHEN** a Project Operator Session or Operator Agent needs topic-scoped service help
- **THEN** a skill instructs it to open a bounded Service Request to a Topic Service Agent with scope, expected output, authorization, dispatch form, and provenance obligations

#### Scenario: Template inspection skill exists
- **WHEN** the project operator or Topic Service Agent needs to perform Topic Team Specialization
- **THEN** a skill instructs it to inspect template manifest, placeholder catalog, role bindings, workflow stages, workspace contract, instantiation schema, and validation diagnostics

#### Scenario: Topic context resolution skill exists
- **WHEN** the project operator or Topic Service Agent needs topic-specific values
- **THEN** a skill instructs it to resolve Project Manifest, Research Topic Config, Effective Topic Context, Topic Workspace, Workspace Runtime readiness, policy refs, Capability Binding refs, Skill Binding Projection refs, provider refs, and Gate policy refs

#### Scenario: Placeholder reconciliation skill exists
- **WHEN** the project operator or Topic Service Agent maps template placeholders to topic-specific values
- **THEN** a skill instructs it to record resolved substitutions, copied material plans, proposed topic edits, explicit deferrals, unresolved blockers, Service Request outputs, user review outcomes, and packet-shaped approval provenance in an instantiation packet

#### Scenario: Profile drafting and review skills exist
- **WHEN** a Project Operator Session or Operator Agent reviews a Topic Agent Team Profile Bundle draft
- **THEN** skills instruct it to produce reviewable profile bundle material, summarize the copied material plan, summarize proposed topic edits and rewritten template content, summarize role and policy choices, identify launch blockers, include Topic Service Agent support outputs when relevant, and request bundle-local approval provenance before materialization

#### Scenario: Materialization and launch orchestration skills exist
- **WHEN** the project operator has approval to proceed
- **THEN** skills instruct it to call generic Isomer validators/materializers, record provenance, and route launch requests through the Houmao adapter without hand-editing runtime state

#### Scenario: Topic Service Agent support skills exist
- **WHEN** a Topic Service Agent receives a Service Request
- **THEN** skills instruct it to perform only bounded Service Team work such as environment readiness, work-agent setup, Topic Team Specialization support, copied material planning, topic edit drafting, monitoring, diagnostics, and support Artifact writing

### Requirement: Project Operator and Topic Service Skills Stay Bounded
Project operator and Topic Service Agent skills SHALL describe orchestration and support decisions without granting authority to bypass Isomer validation, Gates, or runtime recording.

#### Scenario: Skills require validation
- **WHEN** a skill produces a packet, profile, runtime request, handoff, Service Request, support Artifact, or launch request
- **THEN** the skill requires validation through generic Isomer APIs or CLI before treating the artifact as authoritative, including validation for copied material plans and proposed topic edits when present

#### Scenario: Skills preserve domain boundaries
- **WHEN** a skill handles Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Service Requests, Topic Service Agents, or adapter material
- **THEN** it uses the canonical Isomer domain terms and does not collapse template, profile, runtime team, service team, and Houmao managed-agent concepts

### Requirement: Research Paradigm Skillset References Operator Skills by Boundary
Research-paradigm documentation SHALL distinguish research-stage skills from operator skills instead of presenting Project Operator Session orchestration as research method.

#### Scenario: Research docs point to operator skillset
- **WHEN** research-paradigm README or role mapping documentation mentions project operation, Topic Team Specialization orchestration, Service Request routing, profile materialization, approval, or team launch
- **THEN** it points to the `isomer-op-*` operator skillset rather than listing those capabilities as `isomer-deepsci-*` research-stage skills

#### Scenario: Research role mappings avoid operator skills
- **WHEN** generic research agent role mappings are inspected
- **THEN** ordinary research roles such as scout, baseline, experiment, analysis, writer, reviewer, or synthesis reviewer do not install `isomer-op-*` skills unless the role is explicitly an Operator Agent role

### Requirement: Production DeepSci Core Research Process
The production DeepSci core skillset SHALL organize research conduction around the core process rather than around implementation bookkeeping.

#### Scenario: Core loop is documented
- **WHEN** `isomer-deepsci-shared` is inspected
- **THEN** it documents the loop `Frame -> Comparator -> Hypothesis -> Experiment -> Analysis -> Decision -> Finalize`

#### Scenario: Optimize is an overlay
- **WHEN** `isomer-deepsci-optimize` is inspected
- **THEN** it describes optimization as an overlay on hypothesis, experiment, and analysis work rather than as a separate storage model

#### Scenario: Science is a computation-validity companion
- **WHEN** `isomer-deepsci-science` is inspected
- **THEN** it describes scientific computation, package checks, simulations, dataset analysis, and validation as support for the core research loop rather than as a separate storage model

#### Scenario: Each production DeepSci stage declares semantic handoff
- **WHEN** any production DeepSci core skill is inspected
- **THEN** it declares the semantic inputs it expects and the semantic outputs it produces using registered placeholders

#### Scenario: Production DeepSci guardrails preserve research judgment
- **WHEN** a production DeepSci core skill is inspected
- **THEN** it includes guardrails for false progress, missing comparator or metric, unsupported claims, non-comparable experiments, failed or null results, and premature finalization where relevant to that stage

### Requirement: Production DeepSci Research Workspace Manager Skill
The research-paradigm skillset SHALL include an `isomer-deepsci-workspace-mgr` skill that performs research-specific Topic Workspace bootstrap after Topic Team Specialization and full Topic Workspace initialization.

#### Scenario: Workspace manager skill exists
- **WHEN** the production DeepSci research-paradigm skillset is inspected
- **THEN** it contains `skillset/research-paradigm/deepsci/isomer-deepsci-workspace-mgr/SKILL.md` with valid frontmatter, workflow, reference routing, fallback guidance, and an `agents/openai.yaml` manifest that invokes `$isomer-deepsci-workspace-mgr`

#### Scenario: Workspace manager runs after specialization
- **WHEN** the skill explains its entry conditions
- **THEN** it requires a selected Research Topic, a fully initialized Topic Workspace, completed Topic Team Specialization material, Workspace Runtime readiness, and Agent Workspace context before ordinary production DeepSci research skills rely on its bootstrap outputs

#### Scenario: Workspace manager is distinct from operator topic management
- **WHEN** the skill describes its boundary
- **THEN** it states that `isomer-op-topic-mgr` remains the operator initialized-topic manager while `isomer-deepsci-workspace-mgr` owns research placeholder binding and production DeepSci storage bootstrap guidance

#### Scenario: Topic Service Master is optional
- **WHEN** the skill describes the actor that performs bootstrap
- **THEN** it names the Topic Service Master as the preferred topic-workspace manager when started and states that the Project Operator Session or Operator Agent performs the same bounded work when no Topic Service Master is running

### Requirement: Production DeepSci Research Storage Bootstrap Contract
The `isomer-deepsci-workspace-mgr` skill SHALL define consistent placeholders and outputs for research storage bootstrap, using the same placeholder registry style as the other production DeepSci research skills.

#### Scenario: Manager placeholder registry exists
- **WHEN** `isomer-deepsci-workspace-mgr/migrate/placeholders.md` is inspected
- **THEN** it defines placeholders for workspace context, storage label planning, placeholder binding registry, storage bootstrap record, agent access plan, bootstrap validation report, and workspace blocker record

#### Scenario: Placeholder kinds use existing production DeepSci storage mapping
- **WHEN** the manager placeholder registry is inspected
- **THEN** every placeholder has a `Kind` value from the existing production DeepSci placeholder kind set and maps to the storage item mapping for evidence, report, handoff, decision, runtime state, or related accepted kinds

#### Scenario: Storage bootstrap names semantic labels
- **WHEN** the manager describes storage preparation
- **THEN** it names existing labels such as `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, and `topic.records.logs`, planned labels such as `topic.records.evidence`, `topic.records.provenance`, and `topic.records.packages`, and custom labels such as `custom.datasets.*` only when a placeholder needs distinct storage behavior

#### Scenario: Missing storage support becomes a blocker
- **WHEN** a required semantic label, directory, runtime record, or command surface is unavailable
- **THEN** the manager records a blocker placeholder instead of inventing a hard-coded path or claiming a missing storage surface exists

#### Scenario: Agent access plan preserves storage authority
- **WHEN** the manager prepares guidance for working agents
- **THEN** it uses `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links` as pre-promotion or convenience surfaces while preserving semantic labels and typed refs as the durable storage authority

### Requirement: Research Workspace Manager Validation
The research-paradigm validation harness SHALL recognize `isomer-deepsci-workspace-mgr` as an expected production DeepSci skill and apply the normal production DeepSci structure and placeholder checks to it.

#### Scenario: Validator expects workspace manager
- **WHEN** the research-paradigm validation harness runs against the repository skillset
- **THEN** it treats `isomer-deepsci-workspace-mgr` as part of the expected production DeepSci skill set

#### Scenario: Validator checks manager placeholders
- **WHEN** active manager skill text uses migration placeholders
- **THEN** validation confirms those placeholders are registered in `isomer-deepsci-workspace-mgr/migrate/placeholders.md`

### Requirement: Production DeepSci Skills Read Placeholder Bindings
Active production DeepSci research skills SHALL read local placeholder binding pages before writing durable placeholder outputs.

#### Scenario: Skill entrypoint names binding page
- **WHEN** an active production DeepSci research skill has placeholder definitions
- **THEN** its `SKILL.md` tells the agent that placeholder definitions live in `migrate/placeholders.md` and storage bindings live in `placeholder-bindings.md`

#### Scenario: Durable output uses binding page
- **WHEN** a production DeepSci skill step produces a durable placeholder output
- **THEN** the skill instructs the agent to use the corresponding `placeholder-bindings.md` row rather than inventing a path or directly editing Workspace Runtime

#### Scenario: Compatibility fallback remains bounded
- **WHEN** a production DeepSci skill still needs a source-shaped DeepScientist compatibility call
- **THEN** the skill allows `isomer-cli ext deepsci call ...` only as a compatibility fallback and still summarizes durable meaning through the placeholder binding

### Requirement: Writing Artifacts Use Paper-Line Placeholder Bindings
The research-paradigm production DeepSci skillset SHALL map writing-related uppercase artifact identifiers to paper-line storage profiles through local `placeholder-bindings.md` pages while preserving the same identifiers in workflow prose.

#### Scenario: Paper contract binding uses a paper contract view
- **WHEN** a production DeepSci skill binds an uppercase artifact identifier that represents the active paper contract, selected outline, evidence view, paper view, section writing plan, or claim-evidence boundary
- **THEN** the binding maps it to an Isomer record kind and profile that preserves its paper-line role, such as `view_manifest` with `paper.contract.selected-outline`, `artifact` with `paper.outline.*`, or `view_manifest` with `paper.claim-evidence-map`

#### Scenario: Paper control surfaces use view records
- **WHEN** a production DeepSci skill binds an uppercase artifact identifier that represents the paper evidence ledger, experiment matrix, manuscript validation, outline validation, paper-line state, or another paper control surface
- **THEN** the binding uses `topic.records.views` with a paper-specific profile such as `paper.evidence-ledger`, `paper.experiment-matrix`, `paper.validation.*`, or `paper.line-state`

#### Scenario: Paper bodies use artifact records
- **WHEN** a production DeepSci skill binds an uppercase artifact identifier that represents manuscript drafts, LaTeX material, bibliography files, compile reports, PDFs, review reports, rebuttal packets, response letters, final summaries, or paper bundle manifests
- **THEN** the binding uses `topic.records.artifacts` with a paper, review, rebuttal, figure, release, or package profile rather than a generic report or handoff profile when a more precise profile exists

#### Scenario: Paper work queues use task records when resumable
- **WHEN** a production DeepSci skill binds an uppercase artifact identifier that represents a resumable writing plan, reviewer-linked evidence TODO, or paper-facing work queue
- **THEN** the binding uses `research_task` under `topic.records.tasks` when the item must be resumed, assigned, or queried as work, and may use `view_manifest` only when the item is a read-only board

#### Scenario: Binding commands include queryable paper metadata
- **WHEN** a production DeepSci skill binding provides an `isomer-cli ext research records` create or update command for a writing-related artifact
- **THEN** the command includes the exact uppercase `--semantic-id`, `--semantic-label`, `--profile`, `--skill`, producer, consumer, and natural query metadata such as `selected_outline_ref`, `paper_surface`, `package_type`, `section_id`, `claim_id`, or `reviewer_item_id`

#### Scenario: Binding convention avoids paper-specific semantic labels
- **WHEN** writing-related production DeepSci binding pages are updated
- **THEN** they use existing semantic labels such as `topic.records.views`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, and `topic.records.logs`
- **AND** they do not introduce paper-specific top-level semantic labels as required storage surfaces

#### Scenario: Workflow placeholders remain stable
- **WHEN** writing-related binding rows are updated
- **THEN** `SKILL.md` workflow prose keeps the existing placeholder tokens and relies on `placeholder-bindings.md` for storage mapping

#### Scenario: Placeholder registries change only for real drift
- **WHEN** implementation inspects `migrate/placeholders.md` for writing-related skills
- **THEN** it changes placeholder definitions only when a placeholder is missing or its kind conflicts with the durable storage role that the binding page must express

#### Scenario: Workflow identifiers remain stable
- **WHEN** writing-related binding rows are updated
- **THEN** `SKILL.md` workflow prose keeps the exact registered uppercase identifiers and relies on `placeholder-bindings.md` for storage mapping

#### Scenario: Registry definitions change only for real drift
- **WHEN** implementation inspects writing-related migration registries
- **THEN** it changes semantic definitions only when an artifact is missing or its kind conflicts with the durable storage role that the binding page must express

### Requirement: Research Workspace Bootstrap Supports Actor Topology
The production DeepSci research workspace bootstrap SHALL support base topic readiness, Topic Actor readiness, and optional formal team readiness as composable topology layers.

#### Scenario: Bootstrap accepts Topic Actor readiness
- **WHEN** `isomer-deepsci-workspace-mgr` or its successor runs for human-orchestrated research
- **THEN** it validates the selected Topic Workspace, Workspace Runtime, Research Topic overview, topic environment readiness, ready `topic.repos.main`, available research record labels, skill-local placeholder binding files, the topic-level placeholder binding index or readiness report, selected Topic Actor bindings, and selected Topic Actor Workspaces
- **AND** it does not require Topic Agent Team Profile material, formal Agent Workspace access plans, per-Agent Instance cwd proof, Agent Instance records, or Agent Team Instance records unless the selected topology includes a formal team layer

#### Scenario: Placeholder binding index points to skill-local authority
- **WHEN** research workspace bootstrap creates or validates a topic-level placeholder binding index
- **THEN** the index references relevant skill-local `placeholder-bindings.md` files and their selected placeholder groups
- **AND** the bootstrap treats skill-local files as authoritative when the index and skill-local binding content disagree

#### Scenario: Bootstrap keeps formal team checks when present
- **WHEN** the research workspace bootstrap runs in a Topic Workspace with formal team material selected for use
- **THEN** it keeps the existing post-specialization checks for topic team summary, profile material, formal Agent Workspace access, and worker-visible storage boundaries

### Requirement: Production DeepSci Skills Read Placeholder Bindings from Actor Workspaces
The production DeepSci research skills SHALL use skill-local placeholder binding guidance to map workflow placeholders to Topic Workspace records from Topic Actor Workspaces, topic-main, or formal Agent Workspaces.

#### Scenario: Actor skill run resolves placeholders through bindings
- **WHEN** a Topic Actor runs a production DeepSci research skill from its Topic Actor Workspace
- **THEN** the skill reads its `placeholder-bindings.md` and uses the listed record kind, semantic label, profile, topic actor metadata, and `isomer-cli ext research records` command shape for accepted research artifacts
- **AND** it does not replace workflow placeholders with hard-coded Topic Actor Workspace paths in `SKILL.md`

#### Scenario: Missing binding blocks accepted record write
- **WHEN** a production DeepSci skill needs to write an accepted artifact but no binding exists for the placeholder
- **THEN** the skill reports the missing binding as a blocker instead of writing the artifact only to local scratch, a Topic Actor Workspace, a formal Agent Workspace, or an untracked repo path

### Requirement: Research Skills Use Global Isomer CLI
Non-dev research paradigm skills SHALL call Isomer CLI surfaces through direct `isomer-cli` commands.

#### Scenario: Research skill CLI examples omit pixi prefix
- **WHEN** validation scans `skillset/research-paradigm/**`
- **THEN** it reports `pixi run isomer-cli` as invalid command guidance
- **AND** accepted Isomer extension calls use direct shapes such as `isomer-cli ext deepsci call ...` and `isomer-cli ext research records ...`

#### Scenario: Research environment commands remain separate
- **WHEN** a research skill describes commands to run inside a user Topic Workspace environment
- **THEN** it may describe that environment's own package or task runner when relevant
- **AND** it still must not use that runner to invoke Isomer's global CLI

### Requirement: Production DeepSci Research Workspace Manager Owns Production DeepSci Bootstrap
The production DeepSci research-paradigm skillset SHALL make `isomer-deepsci-workspace-mgr` the owner of production DeepSci-specific research workspace bootstrap.

#### Scenario: Production DeepSci bootstrap consumes operator readiness
- **WHEN** `isomer-deepsci-workspace-mgr` prepares production DeepSci research workspace readiness for a Topic Workspace
- **THEN** it consumes Topic Workspace and Topic Actor readiness evidence produced by operator skills as input
- **AND** it does not require operator skills to validate selected production DeepSci skills, production DeepSci placeholder binding files, production DeepSci placeholder binding registries, or accepted research artifact command shapes

#### Scenario: Production DeepSci bootstrap reports research recording guidance
- **WHEN** `isomer-deepsci-workspace-mgr` completes production DeepSci bootstrap
- **THEN** it reports selected production DeepSci skill readiness, placeholder binding entrypoints, research storage or record guidance, actor access plans, and accepted research artifact recording instructions when those are in scope
- **AND** it treats those outputs as research-paradigm material rather than operator Topic Actor topology material

#### Scenario: Production DeepSci actor access plan preserves actor metadata
- **WHEN** production DeepSci bootstrap includes human-orchestrated Topic Actors
- **THEN** it preserves Topic Actor names, actor kind, runtime kind, role kind, controller kind, and cwd labels from operator readiness evidence
- **AND** it adds production DeepSci-specific recording metadata only inside production DeepSci research workspace outputs

### Requirement: Production DeepSci Package Setup Routes to Topic Manager
Active research-paradigm production DeepSci skills SHALL route package installation, package update, package removal, and package verification needs to `isomer-op-topic-mgr` environment commands instead of installing packages directly.

#### Scenario: Missing Python package routes to topic manager
- **WHEN** a production DeepSci research skill detects that a required Python package is missing from the selected Topic Workspace environment
- **THEN** it stops before the dependent research action and routes a natural-language package request to `$isomer-op-topic-mgr env-install-packages`
- **AND** it does not create a local virtual environment, run ambient `pip`, or mutate machine-global Python state

#### Scenario: Missing R package routes to topic manager
- **WHEN** a production DeepSci research skill detects that a required R package is missing from the selected Topic Workspace environment
- **THEN** it stops before the dependent render, analysis, or verification action and routes a natural-language package request to `$isomer-op-topic-mgr env-install-packages`

#### Scenario: Package update or removal request routes to topic manager
- **WHEN** a production DeepSci research skill needs a package update, package downgrade, or package removal to proceed safely
- **THEN** it routes the request to `$isomer-op-topic-mgr env-update-packages` or `$isomer-op-topic-mgr env-remove-packages`
- **AND** it includes the research purpose and desired verification evidence in the request

#### Scenario: Package readiness evidence is consumed after verification
- **WHEN** `isomer-op-topic-mgr` reports package mutation or verification evidence with passing checks
- **THEN** the production DeepSci research skill may continue the blocked workflow from the same selected Topic Workspace context
- **AND** it treats failed or skipped verification as a blocker rather than silently switching environments

### Requirement: Production DeepSci Skills Author Structured Accepted Outputs
Active production DeepSci research-paradigm skills SHALL treat accepted durable research outputs as structured payloads when their placeholder binding names a structured Artifact Format Profile or schema/template inputs.

#### Scenario: Skill routes accepted output through binding
- **WHEN** a production DeepSci skill produces an accepted durable output for a registered placeholder with a structured binding
- **THEN** the skill directs the agent to follow the skill-local `placeholder-bindings.md` payload-first record guidance rather than authoring a Markdown body directly as the durable source of truth

#### Scenario: Skill authors payload before generated Markdown
- **WHEN** a production DeepSci skill needs to create a structured accepted artifact
- **THEN** the expected agent workflow is to draft the JSON payload, validate it with `isomer-cli ext research records validate`, record it with `isomer-cli ext research records create` or `update`, and request Markdown materialization with explicit `--render markdown` when a generated Markdown view is needed

#### Scenario: Methodology prose remains storage-light
- **WHEN** active production DeepSci `SKILL.md` prose describes the research method
- **THEN** it may reference structured record production through local placeholder bindings
- **AND** it does not embed profile-specific JSON schemas, Jinja2 templates, database schema details, or Workspace Runtime table details in the methodology workflow

### Requirement: Production DeepSci Structured Payload Guidance Is Self-contained
Active production DeepSci research-paradigm skill bundles SHALL provide enough local guidance for an agent to produce structured payloads for their accepted outputs without reading discarded topic artifacts or external migration notes.

#### Scenario: Binding page names payload expectations
- **WHEN** a production DeepSci skill owns placeholders that produce structured records
- **THEN** its active binding or directly linked active reference names the expected format profile or schema/template inputs and the minimal payload authoring surface for each structured output

#### Scenario: Active accepted-output set is covered
- **WHEN** active production DeepSci placeholder bindings are updated for structured records
- **THEN** every active production DeepSci accepted-output placeholder family that remains in scope has an explicit `isomer:deepsci/record-format/*` profile or an intentional non-structured exclusion recorded in the binding guidance

#### Scenario: Agent can repair validation errors
- **WHEN** `isomer-cli ext research records validate` returns schema diagnostics for a production DeepSci skill payload
- **THEN** the skill's active guidance allows the agent to revise the JSON payload and rerun validation before recording the artifact

#### Scenario: Generated Markdown is not edited as source
- **WHEN** a production DeepSci skill creates Markdown through the structured record pipeline
- **THEN** active guidance treats the Markdown as generated review material
- **AND** corrections to accepted structured content are made by updating the JSON payload and re-rendering through the CLI

### Requirement: Research Skill Validation Allows Accepted Structured Bindings
The research-paradigm validation harness SHALL allow accepted payload-first storage guidance in active production DeepSci placeholder binding material while continuing to reject unbounded runtime coupling in methodology prose.

#### Scenario: Payload-first binding is allowed
- **WHEN** validation scans active production DeepSci placeholder binding pages
- **THEN** it allows direct `isomer-cli ext research records validate`, `create`, `update`, `show`, `list`, and `render` command shapes for structured payload records using `--format-profile` or explicit schema/template inputs

#### Scenario: Database details remain disallowed in skill prose
- **WHEN** validation scans active production DeepSci `SKILL.md` methodology prose and active references
- **THEN** it reports direct Workspace Runtime table names, raw SQL, or implementation-only state fields unless they are confined to accepted binding pages, provenance notes, or explicit implementation references

#### Scenario: Direct Markdown source guidance is reported
- **WHEN** validation scans active production DeepSci structured-output guidance and finds direct Markdown body authoring presented as the normal accepted-artifact source of truth
- **THEN** it reports the guidance

### Requirement: Research Skills Resolve Worker Output Policy
Active production DeepSci research-paradigm skills that write plain files SHALL resolve the current worker output policy through `isomer-cli` before choosing output paths.

#### Scenario: Plain file writing requires output policy
- **WHEN** a production DeepSci research skill will write plain generated outputs such as JSON payload staging files, Markdown drafts, CSVs, figures, paper previews, paper builds, or local reports
- **THEN** the skill guidance tells the agent to resolve the worker output root and `commit_after_operation` preference through `isomer-cli`
- **AND** the skill does not direct the agent to write new generated files directly into the actor or agent workspace root

#### Scenario: Durable records still use record bindings
- **WHEN** a production DeepSci research skill creates an accepted Artifact, Evidence Item, Run record, Decision Record, View Manifest, or other durable research record
- **THEN** the skill continues to use the applicable record binding or `topic.records.*` surface
- **AND** worker output roots are treated as plain output staging or worker-local material unless a promotion or record creation step accepts the material

#### Scenario: Operation outputs use operation sets
- **WHEN** a production DeepSci research skill writes multiple plain outputs for one research operation
- **THEN** the skill guidance tells the agent to place them under one operation-specific child of the resolved worker output root
- **AND** the operation set name includes a discriminator that prevents repeated operations from overwriting each other

### Requirement: Research Skills Apply Post-Operation Commit Preference
Active production DeepSci research-paradigm skills SHALL check the effective `commit_after_operation` preference after research operations that write files and apply it as a post-action step.

#### Scenario: Commit preference true triggers Git status and commit
- **WHEN** a research operation writes files and the resolved worker output policy reports `commit_after_operation=true`
- **THEN** the skill guidance tells the agent to inspect Git status after writing
- **AND** it tells the agent to commit committable changes according to normal Git behavior and the configured worker preference

#### Scenario: Commit preference false leaves workspace uncommitted
- **WHEN** a research operation writes files and the resolved worker output policy reports `commit_after_operation=false`
- **THEN** the skill guidance tells the agent not to commit merely because files were written
- **AND** it tells the agent to report the output location and any dirty workspace status relevant to the user

#### Scenario: Git ignore controls what can be committed
- **WHEN** a skill applies post-operation commit behavior
- **THEN** the skill guidance treats `.gitignore` and Git status as the authority for which output files are tracked, untracked, ignored, or committable
- **AND** it does not ask the agent to override ignore rules unless the user explicitly requests that change

### Requirement: Research Skill Validation Covers Output Policy Guidance
The research-paradigm validation harness SHALL report active production DeepSci research skill entrypoints or references that write plain files without referencing worker output policy resolution.

#### Scenario: Missing output policy guidance is reported
- **WHEN** validation inspects an active production DeepSci research skill that mentions plain file outputs but lacks output-policy resolution guidance
- **THEN** validation reports the skill and explains that generated plain outputs must use the worker output root resolved through `isomer-cli`

#### Scenario: Commit preference guidance is required
- **WHEN** validation inspects an active production DeepSci research skill that performs research operations with file writes
- **THEN** validation confirms the skill includes post-operation guidance to check `commit_after_operation`

#### Scenario: Non-active material is exempt
- **WHEN** validation inspects migration notes, source-copy material under `org/`, passive templates, license files, or provenance material
- **THEN** validation does not require those files to include worker output policy guidance

### Requirement: V2 Skills Apply Latest Context Preflight
Active non-shared v2 research-paradigm skills with durable record bindings SHALL apply the shared latest-context preflight before accepted durable record writes, record refreshes, or durable stage decisions.

#### Scenario: Durable-record-writing skill entrypoints reference preflight
- **WHEN** an active non-shared v2 research skill `SKILL.md` with durable record bindings is inspected
- **THEN** its workflow or entry guidance references the shared latest-context preflight from `isomer-deepsci-shared`
- **AND** it places the preflight before accepted record writes, record refreshes, or durable stage decisions that select routes, accept comparator state, generate ideas, run experiments, analyze evidence, write claims, review manuscripts, create figures, polish prose, prepare data availability, rebut reviewers, or finalize a topic
- **AND** standalone source-only reading may skip the preflight until the skill writes or refreshes accepted Isomer records

#### Scenario: Shared skill owns the reference
- **WHEN** `isomer-deepsci-shared` is inspected
- **THEN** it contains the latest-context preflight reference and semantic registry entry
- **AND** other v2 skills reference that shared material instead of duplicating the full command ladder

#### Scenario: Stage context objects carry freshness verdicts
- **WHEN** a v2 skill creates or refreshes its first durable context object for a pass
- **THEN** the object includes a freshness verdict or an explicit pointer to the latest-context-snapshot content
- **AND** downstream stage work does not proceed when that verdict reports a blocking conflict, missing topic context, invalid runtime, or unresolved active-record ambiguity

### Requirement: V2 Skills Do Not Trust Remembered Research Context
Active non-shared v2 research-paradigm skills with durable record bindings SHALL prefer current Isomer context and durable records over prompt memory, chat memory, or older rendered prose when accepting durable record work.

#### Scenario: Prompt context is treated as input, not authority
- **WHEN** a user prompt includes a Research Topic, route, metric, paper state, or current result that will shape accepted durable record work
- **THEN** the invoked v2 skill treats that prompt as candidate context
- **AND** it checks the current Effective Topic Context and relevant durable records before treating the prompt as the active research context

#### Scenario: Older rendered records are not silently reused
- **WHEN** a v2 skill finds older rendered Markdown for a context object, contract, route, result, finding, paper state, or blocker
- **THEN** it checks record metadata, structured payload status, record status, updated timestamp, and active or supersession signals before using that record as current
- **AND** it routes to decision or blocker handling when the active version cannot be identified

#### Scenario: Scope changes are recorded or routed
- **WHEN** the preflight determines that the user changed the Research Topic scope, accepted dataset, comparator basis, metric contract, evaluation contract, paper target, or claim boundary
- **THEN** the invoked v2 skill records the scope-change implication in its context object or route decision
- **AND** it routes to scout, baseline, decision, paper-outline, workspace bootstrap, or blocker handling when the current stage is no longer ready

### Requirement: Research Skill Validation Covers Context Preflight
The research-paradigm validation harness SHALL check that active non-shared v2 skill entrypoints with durable record bindings include the shared latest-context preflight contract.

#### Scenario: Missing preflight is reported
- **WHEN** validation inspects an active non-shared v2 `SKILL.md` with durable record bindings that lacks a reference to the shared latest-context preflight
- **THEN** validation reports the skill and explains that v2 durable-record-writing entrypoints must resolve current topic context before accepted record work

#### Scenario: Shared and non-active material are not false positives
- **WHEN** validation inspects `isomer-deepsci-shared`, migration notes, source-copy material under `org/`, passive templates, or non-active provenance material
- **THEN** it does not require those files to consume the latest-context preflight as a stage entrypoint

#### Scenario: Validation accepts concise imports
- **WHEN** a v2 stage skill references the shared preflight and states that it must run before prompt memory or prior prose is trusted
- **THEN** validation accepts the entrypoint without requiring the full command ladder to be duplicated in that skill

#### Scenario: Worker output policy remains distinct
- **WHEN** validation inspects a v2 skill that already references worker output policy for plain generated files
- **THEN** that worker-output guidance does not satisfy the latest-context preflight requirement for accepted durable record work
- **AND** the latest-context preflight rule does not replace the worker-output-root policy, operation output set, or `commit_after_operation` requirements for plain file writes

### Requirement: Production DeepSci User Skill Callback Participation
The production `isomer-deepsci-*` skill family SHALL participate in the User Skill Callback mechanism through explicit numbered workflow steps at the beginning and end of each top-level workflow while preserving DeepSci methodology guardrails.

#### Scenario: Top-level workflow includes callback steps
- **WHEN** a production `isomer-deepsci-*` `SKILL.md` is inspected
- **THEN** its `## Workflow` numbered step list includes explicit `begin` and `end` User Skill Callback resolution steps for that skill name
- **AND** callback participation is not represented only as unnumbered reminder prose outside the step list

#### Scenario: Begin callback runs before primary workflow action
- **WHEN** an agent invokes a production `isomer-deepsci-*` top-level workflow
- **THEN** the skill instructs the agent in a numbered workflow step to resolve `begin` callbacks through `isomer-cli project skill-callbacks resolve --skill <skill-name> --stage begin` after mandatory context checks and before the first workflow-specific research action

#### Scenario: End callback runs before final completion
- **WHEN** an agent reaches the end of a production `isomer-deepsci-*` top-level workflow
- **THEN** the skill instructs the agent in a numbered workflow step to resolve `end` callbacks through `isomer-cli project skill-callbacks resolve --skill <skill-name> --stage end` after tentative outputs exist and before final response, handoff, or treating the workflow as complete

#### Scenario: Empty callback resolution does not block workflow
- **WHEN** `isomer-cli project skill-callbacks resolve` returns no active callbacks for a production DeepSci skill and stage
- **THEN** the skill continues through its normal workflow without treating the missing callback as a blocker

#### Scenario: Callback instructions remain subordinate to DeepSci rules
- **WHEN** resolved callback instructions conflict with `isomer-deepsci-shared`, the skill's own guardrails, required placeholder discipline, evidence discipline, validation gates, or the current user request
- **THEN** the skill preserves the owning DeepSci requirements and reports any callback conflict that affects the workflow

#### Scenario: DeepSci validation checks callback workflow steps
- **WHEN** the repository DeepSci skill validation harness inspects production `isomer-deepsci-*` skills
- **THEN** it confirms each participating skill includes the required User Skill Callback resolution guidance for the `begin` and `end` stages as numbered workflow steps
- **AND** it reports callback guidance that appears only as a free-floating reminder under `## Workflow`

### Requirement: Payload-file Research Record Guidance
Production DeepSci system skills SHALL teach agents to create durable structured records as JSON payload files managed by the research recording CLI.

#### Scenario: Skill workflow creates payload records
- **WHEN** a production DeepSci skill instructs an agent to create an accepted durable structured output
- **THEN** it tells the agent to draft JSON, validate the payload, call the record create or update command, and let Workspace Runtime snapshot the payload file into managed storage

#### Scenario: Skill workflow does not grow generated Markdown
- **WHEN** a production DeepSci skill describes repeated research rounds
- **THEN** it tells the agent to create new payload-backed records, snapshots, or revision links rather than appending to or overwriting generated Markdown files

#### Scenario: Skill workflow renders only for review
- **WHEN** a production DeepSci skill mentions Markdown review
- **THEN** it frames Markdown as on-demand display or explicit export from payload JSON, not as the accepted durable record itself

#### Scenario: Skill validation checks payload-file contract
- **WHEN** the research-paradigm validation harness scans active production DeepSci guidance
- **THEN** it reports instructions that make SQLite payload blobs or generated Markdown files the canonical accepted-output content for structured records

### Requirement: Production DeepSci Artifact Lineage Workflow
Production DeepSci skills SHALL identify canonical artifact lineage before writing or revising durable research records.

#### Scenario: Skill creates a durable record
- **WHEN** a production DeepSci skill creates a durable Artifact, Evidence Item, Decision Record, Run, View Manifest, or related structured research record
- **THEN** the skill workflow tells the agent to identify parent records, lineage kind, parent roles, generation group when relevant, decision record when relevant, and revision parent when relevant before calling the recording CLI

#### Scenario: Skill cannot identify parents
- **WHEN** a production DeepSci skill cannot responsibly identify lineage parents for a durable record
- **THEN** the skill records the omission as a blocker, diagnostic, or explicit no-parent/root-lineage reason rather than inventing parentage

#### Scenario: Skill revises accepted content
- **WHEN** a production DeepSci skill changes accepted record content in a way that should remain historically visible
- **THEN** the skill uses the record revision path and preserves the prior record as the immediate revision parent

### Requirement: DeepSci Idea Flow Records Artifact DAG
The DeepSci idea flow SHALL record parent-child lineage across raw ideas, candidate frontiers, pre-idea drafts, route decisions, and selected hypotheses.

#### Scenario: Raw slate is produced
- **WHEN** `isomer-deepsci-idea` records a raw idea slate
- **THEN** it records lineage parents such as objective contract, current board, literature survey, limitations map, and mechanism framing when those records exist

#### Scenario: Serious candidates are produced
- **WHEN** `isomer-deepsci-idea` promotes serious candidates into candidate frontier or pre-idea draft records
- **THEN** it records those candidates as children of the raw slate or candidate frontier and associates sibling alternatives with a generation group

#### Scenario: Selected hypothesis is produced
- **WHEN** `isomer-deepsci-idea` records a selected hypothesis
- **THEN** it records the selected hypothesis as a child of the selected pre-idea draft or candidate record and the route decision that selected it

### Requirement: DeepSci Downstream Flows Continue Artifact DAG
Downstream DeepSci flows SHALL continue canonical artifact lineage after idea selection.

#### Scenario: Experiment flow creates records
- **WHEN** `isomer-deepsci-experiment` creates an experiment contract, run record, artifact manifest, result summary, or route decision
- **THEN** it records lineage from the selected hypothesis, comparator contract, prior run, and relevant decision records according to the artifact's actual parents

#### Scenario: Analysis flow creates records
- **WHEN** `isomer-deepsci-analysis` creates context briefs, slice records, campaign plans, findings, summaries, or route decisions
- **THEN** it records lineage from parent results, parent claims, runs, evidence, and decisions according to the artifact's actual parents

#### Scenario: Decision flow changes route
- **WHEN** `isomer-deepsci-decision` records a route-changing decision or checkpoint memory
- **THEN** it records lineage from the evidence packet, route question, selected target record, and superseded or rejected route records when those refs are explicit

### Requirement: DeepSci Skills Record Research Idea Identity
Production DeepSci skills SHALL record stable Research Idea identity when producing idea-bearing durable records.

#### Scenario: Idea skill records candidate ideas
- **WHEN** `isomer-deepsci-idea` produces raw idea slates, candidate frontiers, pre-idea drafts, selected hypotheses, selected idea drafts, rejected ideas, or deferred ideas
- **THEN** the skill instructs the agent to record stable semantic topic-scoped Research Idea ids, source-local aliases, visibility, status, realization records, source JSON paths, sibling generation groups, and idea lineage where the relationship is known

#### Scenario: Experiment skill records explicit idea outcome
- **WHEN** `isomer-deepsci-experiment` records an experiment result that supports, refutes, narrows, or motivates a follow-up to a selected idea
- **THEN** the skill instructs the agent to explicitly update the relevant Research Idea status or create a follow-up Research Idea with canonical idea lineage and supporting evidence refs

#### Scenario: Experiment result does not auto-mutate idea
- **WHEN** `isomer-deepsci-experiment` records an experiment result without an explicit accepted idea status update
- **THEN** the skill guidance treats the result as evidence or a stale-status diagnostic and does not claim that the Research Idea status changed automatically

#### Scenario: Analysis skill records conceptual redirection
- **WHEN** `isomer-deepsci-analysis` concludes that the current line should continue, revise, split, merge, or return to ideation
- **THEN** the skill instructs the agent to record the affected Research Idea relationship, realization, status change, or follow-up idea before routing onward

### Requirement: DeepSci Skills Separate Idea Lineage from Record Lineage
Production DeepSci skills SHALL distinguish record lineage from idea lineage in active workflow guidance.

#### Scenario: Durable record has both lineage layers
- **WHEN** a DeepSci skill produces a durable record from prior durable records and the record also expresses an idea relationship
- **THEN** the skill instructs the agent to record record parents through `--parents-json` and idea parents through the Research Idea CLI/API or accepted idea metadata fields

#### Scenario: Siblings use generation group
- **WHEN** a DeepSci idea pass creates alternative serious candidates from the same parent context
- **THEN** the skill instructs the agent to use an idea generation group rather than pairwise sibling edges as the primary sibling representation

#### Scenario: Candidate collapse records subsumption
- **WHEN** a DeepSci idea pass concludes that one serious candidate subsumes another as an ablation, mechanism subset, or test role
- **THEN** the skill instructs the agent to record a canonical `subsumes` idea lineage edge in addition to the shared generation group

#### Scenario: Markdown is not authoritative lineage
- **WHEN** a DeepSci skill renders or writes Markdown for human review
- **THEN** the skill instructs the agent that Markdown prose does not replace canonical Research Idea rows, realizations, lineage edges, or generation groups

### Requirement: Skill Validation Covers Idea Recording Guidance
The research-paradigm skill validation harness SHALL detect missing or contradictory active guidance for Research Idea recording.

#### Scenario: Idea recording guidance is present
- **WHEN** the validation harness inspects active DeepSci idea, experiment, analysis, decision, optimize, and shared skill guidance
- **THEN** it confirms that idea-bearing workflows mention canonical Research Idea identity, realization, and lineage obligations where applicable

#### Scenario: Contradictory guidance is reported
- **WHEN** active skill guidance tells agents to infer authoritative idea lineage only from chat memory, generated Markdown, or record-lineage projection
- **THEN** validation reports the guidance as stale and directs the skill to use canonical Research Idea recording

### Requirement: DeepSci Skills Preserve Exact Idea Content
Production DeepSci skills SHALL teach agents to preserve Primary Idea content separately from slate/report context and to record exact Idea Realization source paths.

#### Scenario: Idea skill records exact source fragments
- **WHEN** `isomer-deepsci-idea` produces raw slates, candidate frontiers, pre-idea drafts, selected hypotheses, selected idea drafts, rejected/deferred ideas, route decisions, or paper-facing idea seeds
- **THEN** its workflow and directly linked research-idea recording guidance tell the agent to write canonical Research Ideas and Idea Realizations with exact object-valued source paths
- **AND** the guidance says that filter notes, summaries, and route context belong to the source record, not the Primary Idea main content

#### Scenario: Downstream skills update existing idea identity
- **WHEN** experiment, analysis, optimize, decision, write, review, rebuttal, or finalize skills support, refute, narrow, supersede, or follow up a Research Idea
- **THEN** their guidance tells the agent to update or realize the existing Research Idea when the concept is unchanged
- **AND** it tells the agent to create a new Research Idea only for a true follow-up or alternative concept with explicit lineage

### Requirement: Packaged DeepSci Skills Carry Source Contract Guidance
Packaged system-skill assets SHALL include the same Primary Idea source contract guidance as the repository skillset.

#### Scenario: Package skill mirrors are updated
- **WHEN** repository skill guidance or placeholder bindings are updated for exact idea source fragments
- **THEN** the corresponding files under `src/isomer_labs/assets/system_skills/research-paradigm/deepsci/` are updated consistently
- **AND** packaged skill validation does not route installed agents to stale broad-path guidance

### Requirement: Production Skills Teach the Display Contract
Production DeepSci system skills SHALL teach agents to create supported v2 structured research records with canonical `title` and `summary` display fields.

#### Scenario: Shared guidance defines display fields
- **WHEN** an agent reads production DeepSci shared guidance or directly linked record-authoring references
- **THEN** the guidance defines `title` as the concise display name and `summary` as the brief display description
- **AND** it tells agents to include both fields in supported v2 accepted structured payloads

#### Scenario: Idea-stage guidance defines idea display fields
- **WHEN** an agent reads production DeepSci idea-stage, decision-stage, writing-stage, or other idea-producing guidance
- **THEN** the guidance instructs the agent to include `title` and `summary` on each idea-bearing payload entry that can become a canonical Research Idea
- **AND** it treats source labels and candidate ids as aliases rather than display-field replacements

#### Scenario: Skills avoid stale one-liner terminology
- **WHEN** active production DeepSci skill text describes accepted structured record or Research Idea display fields
- **THEN** it uses `summary` instead of `one_liner`
- **AND** any retained `one_liner` reference is clearly marked as legacy migration context

#### Scenario: Skills avoid stale v1 authoring guidance
- **WHEN** active production DeepSci skill text describes accepted structured record writes
- **THEN** it uses the supported v2 display contract
- **AND** any retained v1 reference is clearly marked as legacy validation, repair, or migration context

### Requirement: Skill Validation Checks Display Contract
The research-paradigm validation harness SHALL check active production DeepSci skills for display-contract compliance.

#### Scenario: Validation detects missing title-summary instruction
- **WHEN** validation inspects active production DeepSci skill text and directly linked active references
- **THEN** it reports missing `title` and `summary` guidance for structured record authoring surfaces that produce accepted payloads

#### Scenario: Validation detects stale one-liner instruction
- **WHEN** validation finds active skill guidance that tells agents to create `one_liner` for accepted records or ideas
- **THEN** validation reports the stale instruction with file path and skill name

#### Scenario: Validation detects stale v1 instruction
- **WHEN** validation finds active skill guidance that tells agents to create `structured-record.v1` payloads for accepted new records
- **THEN** validation reports the stale instruction with file path and skill name

### Requirement: Production Kaoju Research-Paradigm Layout
The research-paradigm asset tree SHALL document and package Kaoju as a production family alongside DeepSci without changing DeepSci's active layout.

#### Scenario: Research-paradigm documentation lists both families
- **WHEN** `src/isomer_labs/assets/system_skills/research-paradigm/README.md` is inspected
- **THEN** it identifies `deepsci/` and `kaoju/` as separate optional domain-extension families
- **AND** it describes Kaoju as evidence-led survey work rather than hypothesis-driven new-method research

#### Scenario: Kaoju active surface is concise and self-contained
- **WHEN** a production Kaoju skill directory is inspected
- **THEN** active execution guidance is limited to `SKILL.md`, `agents/openai.yaml`, and directly useful local `commands/`, `references/`, `assets/`, or `scripts/`
- **AND** it does not require feature-design files, archived OpenSpec changes, external source checkouts, local absolute paths, or provider-specific credentials at runtime

#### Scenario: Kaoju skills use canonical Isomer language
- **WHEN** active Kaoju guidance names platform concepts
- **THEN** it uses Research Topic, Research Inquiry, Topic Workspace, Artifact, Evidence Item, Run, Finding, Decision Record, Gate, Provenance Record, and Workspace Path Resolution consistently
- **AND** it does not introduce a Kaoju-specific runtime database or lifecycle vocabulary

### Requirement: Research-Paradigm Validation Supports Kaoju
The research-paradigm validation harness SHALL validate the fourteen-skill Kaoju survey-process family through family-specific rules while preserving all existing DeepSci checks.

#### Scenario: Valid Kaoju family passes validation
- **WHEN** the validator inspects the complete production Kaoju family
- **THEN** it accepts the exact fourteen-skill inventory, valid frontmatter and manifests, near-top workflows, approved survey-intent and compatibility command inventory, self-contained direct references, canonical namespace, binding-registry use, and external-acquisition followed by semantic-registration guidance

#### Scenario: Invalid Kaoju family reports deterministic diagnostics
- **WHEN** a Kaoju skill is missing, uses the wrong namespace, has manifest identity drift, references a missing local file, hardcodes a local or provider-specific runtime path, scans for durable records, repeats a physical binding as independent authority, invokes an unregistered executable path other than an authorized external repository command, routes repository acquisition through `isomer-cli` or an Isomer execution request, registers before verification, treats Markdown or TeX as canonical paper content, invokes the external wiki skill, mutates Pixi state directly, or exposes an unapproved procedure
- **THEN** validation fails with a deterministic diagnostic that names the file, line when available, skill, semantic id when applicable, and violated Kaoju rule

#### Scenario: Shared checks do not erase family-specific checks
- **WHEN** common frontmatter, manifest, reference, CLI-spelling, terminology, repository-boundary, or binding checks are refactored for multiple families
- **THEN** DeepSci retains its inventory, artifact-identity, source-lineage, structured-output, and other existing family-specific validation
- **AND** the existing DeepSci validation tests continue to pass unchanged in meaning

#### Scenario: Validator tests cover Kaoju active and invalid zones
- **WHEN** unit tests exercise family-aware research-paradigm validation
- **THEN** they include valid Kaoju fixtures and failures for missing inventory, wrong namespace, manifest mismatch, broken direct references, stale domain terms, hard-coded provider or local paths, procedural-command drift, binding drift, directory scanning, canonical-format violations, external wiki routing, direct environment mutation, Isomer-owned repository acquisition, and pre-verification registration
- **AND** they retain regression fixtures for valid and invalid DeepSci material

### Requirement: Production Kaoju Skills Use Artifact Binding Authority
Production Kaoju skills SHALL route accepted durable outputs through registered semantic ids and the versioned machine-readable Kaoju binding registry.

#### Scenario: Stage writes a bound artifact
- **WHEN** a Kaoju stage accepts a durable output
- **THEN** it reads the storage-neutral semantic definition from `isomer-kaoju-shared`, resolves the physical contract through `isomer-cli project artifacts describe` or its package service, and invokes the typed put or revise operation
- **AND** the service validates the exact semantic id, record kind, label, profile, content mode, producer, consumers, scope, lineage, actor, and provenance required by the binding

#### Scenario: Binding is unavailable
- **WHEN** the stage's semantic id, profile, semantic label, content mode, scope policy, producer authorization, or recording command cannot be resolved
- **THEN** the stage returns an explicit storage blocker
- **AND** it does not fall back to an invented path, direct Markdown state, a DeepSci profile, an untracked JSON file, or a hand-authored physical binding

#### Scenario: Per-skill binding guidance is inspected
- **WHEN** a skill contains `artifact-bindings.md` or equivalent local guidance
- **THEN** that guidance is generated from or points to the versioned registry and may explain semantic usage
- **AND** it does not become an independent physical binding authority or repeat full executable command shapes

### Requirement: Kaoju Shared Defines Durable Record Discipline
`isomer-kaoju-shared` SHALL teach the common latest-context, scoped-query, worker-output, file-authority, lineage, revision, view, material-boundary, audit, Gate, and resumption rules used by every bound stage.

#### Scenario: Durable work starts from current context
- **WHEN** a Kaoju skill will write, refresh, revise, audit, compare, synthesize, manage, export, build, prepare, or execute accepted durable work
- **THEN** it resolves current Effective Topic Context, fresh Workspace Runtime state, applicable semantic ids and scopes, latest candidate records, duplicates, conflicts, and supersession posture before trusting prompt memory or prior prose

#### Scenario: Worker file and durable artifact remain distinct
- **WHEN** a Kaoju skill produces operation-local notes, payload staging, tables, logs, exports, conversion output, or trial output
- **THEN** it applies the worker output policy and treats those files as pre-promotion until the applicable artifact operation succeeds
- **AND** accepted content remains the registered structured file, ordinary file, directory manifest, external locator, or canonical repository reference named by the binding

#### Scenario: Claim-bearing input requires audit
- **WHEN** a downstream stage selects claim-bearing source, comparison, Run, or synthesis input
- **THEN** shared guidance requires the applicable accepted audit disposition and exact input revision
- **AND** missing audit state pauses the downstream stage rather than being inferred from prose

#### Scenario: Paused work is resumable
- **WHEN** a stage pauses for a Gate, clarification, blocker, Service Request, or actor action
- **THEN** shared guidance requires a Run checkpoint with completed output refs, pending refs, and resume hint
- **AND** resume uses Workspace Runtime and state-DB queries rather than directory scanning or conversation memory

### Requirement: Kaoju Workspace Manager Owns Binding Bootstrap
`isomer-kaoju-workspace-mgr` SHALL prepare and validate the Kaoju semantic-to-binding, scoped-query, and path contract before ordinary production survey work.

#### Scenario: Selected skills become ready
- **WHEN** a Research Topic and selected Kaoju skill set have base Topic Workspace readiness
- **THEN** the workspace manager validates record labels, provider profiles, semantic registry, versioned binding registry, binding index, scope-key query support, dataset-manifest state, actor posture, worker output policy, Run checkpoint support, and reset treatment
- **AND** it records readiness through bound Kaoju records before handing control to the selected stage

#### Scenario: Bootstrap preserves selected setup state
- **WHEN** the binding index, readiness record, registered custom support, or user-selected survey state should survive reset
- **THEN** the workspace manager updates the selected Topic Workspace reset checkpoint with exact durable refs and content locators
- **AND** it reports unpreserved state as subject to the accepted reset plan

#### Scenario: Bootstrap detects legacy ambiguity
- **WHEN** legacy unscoped Kaoju records or LaTeX-first writing records compete with the new scoped or MyST-first state
- **THEN** the workspace manager reports their compatibility and migration posture
- **AND** it does not silently select or promote a legacy record

### Requirement: Kaoju Managers Use Exact Bound Operations
The Kaoju pipeline's grouped management helpers SHALL use exact binding and query operations rather than unspecified recording interfaces.

#### Scenario: Manage survey dispatches bound reads
- **WHEN** a user selects `manage-survey list`, `show`, `status`, or `export`
- **THEN** the helper follows its documented family, semantic-id, record-id, latest, lineage, render, and export operations
- **AND** it does not mutate canonical content during read or export actions

#### Scenario: Manage dataset revises manifest through owner route
- **WHEN** a user selects dataset `register`, `refresh`, or `remove`
- **THEN** the Topic Workspace owner performs material or link mutation and the Kaoju helper revises the bound Topic Dataset Manifest with returned refs and provenance
- **AND** read-only `list` and `show` actions query the canonical manifest record

### Requirement: Formal Team Recovery Is Conditional on Selected Team Topology
Research-paradigm workspace and readiness skills SHALL route missing formal-team material to Topic Team Specialization only when the selected research topology includes a formal Agent Team layer.

#### Scenario: Selected formal team lacks its summary
- **WHEN** authoritative context selects formal team material and its required `isomer-topic-summary.md` is missing, blocked, stale, or not checked
- **THEN** the research workspace manager routes recovery to `isomer-op-topic-team-specialize` or the applicable formal-team setup service
- **AND** it names the selected template, profile, packet, Agent Team Instance, or other formal-team evidence

#### Scenario: Human-orchestrated topology lacks a team summary
- **WHEN** the selected topology uses Topic Actors or other non-team preparation and does not select a formal Agent Team layer
- **THEN** absence of `isomer-topic-summary.md` is not a Topic Team Specialization blocker
- **AND** the workspace manager evaluates Topic Creator, Topic Manager, runtime, actor, environment, and research-bootstrap evidence without requiring formal team material

#### Scenario: Missing Agent Workspace does not create team intent
- **WHEN** Agent Workspace or worker-access evidence is missing but no formal Agent Team target is established
- **THEN** the research workspace manager routes to the owner of the selected actor or workspace topology or reports the missing selection
- **AND** it does not infer Topic Team Specialization from the missing workspace evidence alone

### Requirement: Kaoju Skills Separate Research Judgment from Deterministic Operations
Production Kaoju skills SHALL own arbitrary template construction, interpretation, and reconciliation while delegating named-template CRUD, export inspection, state-token checks, integrity validation, and atomic mutation to typed Isomer CLI and owner services.

#### Scenario: Skill performs research judgment
- **WHEN** a procedure selects a direction, appraises a source, forms a claim, writes prose, interprets a template tree, reconciles template changes, identifies entrypoints, repairs TeX semantics, or recommends a trial design
- **THEN** the responsible Kaoju skill performs and records that judgment with evidence and actor provenance

#### Scenario: Skill needs deterministic mutation
- **WHEN** the procedure persists an artifact, resolves a managed path, acquires a repository, exports or applies a template, initializes a conversion, dispatches environment support, executes a trial, builds a PDF, exports a wiki, deploys a viewer, or launches a process
- **THEN** it invokes the applicable typed CLI or owner service and consumes returned durable refs
- **AND** it does not substitute prose instructions for a missing deterministic contract

#### Scenario: Skill needs deterministic Isomer mutation
- **WHEN** the procedure persists an artifact, resolves or registers a managed path, exports or applies a template, initializes a conversion, dispatches environment support, executes a trial, builds a PDF, exports a wiki, deploys a viewer, or launches a managed process
- **THEN** it invokes the applicable typed CLI or owner service and consumes returned durable refs
- **AND** it does not substitute prose instructions for a missing deterministic Isomer contract

#### Scenario: Skill needs repository acquisition
- **WHEN** the procedure needs to clone, fetch, copy, check out, deepen, repair, or inspect source-control state to obtain a repository
- **THEN** the acting agent runs user-supplied or task-appropriate commands outside Isomer APIs under the applicable authorization
- **AND** it uses typed Isomer operations only to plan a semantic target, register the verified existing path, and record Artifacts, provenance, checkpoints, or blockers

#### Scenario: Skill needs deterministic support
- **WHEN** the procedure lists, reads, creates, updates, copies, replaces, archives, or exports a named template; calculates digests; resolves a managed path; edits allowed metadata; initializes a conversion; executes a trial; or builds a PDF
- **THEN** it invokes the applicable typed CLI or owner service and consumes returned state tokens, paths, digests, diagnostics, and refs
- **AND** it does not directly update SQL or managed Artifact files

#### Scenario: Arbitrary directory drives an update
- **WHEN** a user asks to update a database template from an arbitrary directory
- **THEN** the Kaoju skill inspects the source and current target, prepares the intended candidate, records its assessment, and invokes low-level template update with the expected target state token
- **AND** it does not delegate high-level conversion or merge decisions to isomer-cli

#### Scenario: Known named source replaces target
- **WHEN** the user explicitly asks to replace one named template with another known named template
- **THEN** the skill invokes exact named-template replacement after reporting source and target
- **AND** it does not construct a merge unless the user requested one

### Requirement: Kaoju Write Guidance Is MyST-First
`isomer-kaoju-write` SHALL treat mutable named MyST-oriented template records and MyST draft Artifacts as canonical and SHALL treat exported template directories, Markdown, TeX, and PDF as non-canonical exchange, review, or publication material.

#### Scenario: Write skill starts a paper
- **WHEN** accepted audit and synthesis inputs are available
- **THEN** the skill resolves the explicitly named template or canonical `main`, interprets its current tree and entrypoint metadata, and creates paper state with the selected stable ref and observed digest
- **AND** it does not create legacy `kaoju:writing-template` state

#### Scenario: TeX requires semantic repair
- **WHEN** the paper service initializes TeX from current MyST template state
- **THEN** the write skill inspects and repairs directives, tables, citations, floats, raw blocks, and venue structure before build readiness
- **AND** a compiler exit does not replace inspection

#### Scenario: User requests export without a name
- **WHEN** the user asks to get, edit, or export the paper template without naming one
- **THEN** the skill selects canonical `main` and exports to resolved `intent/derived/writing-template/main/`
- **AND** it reports that the directory is non-canonical

#### Scenario: Unnamed database update finds an edited export
- **WHEN** the user asks to update the current database template without any locator and exactly one registered export is edited
- **THEN** the skill selects that export and its recorded target name before constructing the update candidate
- **AND** it does not prefer topic `main/` merely because it exists

#### Scenario: Unnamed database update falls back to topic main
- **WHEN** no eligible edited export exists and the current Topic Workspace contains `intent/derived/writing-template/main/`
- **THEN** the skill uses that directory as source and target name `main`, subject to consistent export metadata
- **AND** it does not require database `main` to exist before selecting the source

#### Scenario: Unnamed database update remains ambiguous
- **WHEN** several edited exports qualify, an edited export has inconsistent identity, or neither an edited export nor topic `main/` exists
- **THEN** the skill asks the user to select a concrete template or path and presents discovered candidates
- **AND** it does not choose by timestamp or unrelated database record order

#### Scenario: Explicit source bypasses discovery
- **WHEN** the database-update request names a template, canonical ref, template path, or export path
- **THEN** the skill validates and uses the explicit source and performs agentic construction as needed
- **AND** it does not run implicit source discovery

#### Scenario: User requests an explicit saved copy
- **WHEN** the user asks to preserve the current template before an edit
- **THEN** the skill chooses or confirms a new ordinary template name and invokes create-from-template
- **AND** it does not attach snapshot type or lifecycle metadata

#### Scenario: Agent chooses to preserve a state
- **WHEN** the agent determines that an explicit saved copy is useful and the request authorizes that additional named template
- **THEN** it reports the chosen name and creates the copy before mutation
- **AND** ordinary updates do not create copies silently

#### Scenario: User restores from a named copy
- **WHEN** the user asks to restore or replace target `main` from another name
- **THEN** the skill invokes exact update-from-template with current target state token
- **AND** the source named template remains unchanged

#### Scenario: User requests a merge
- **WHEN** the user asks to merge current target state with another named template or editable directory
- **THEN** the skill interprets both inputs, asks about material ambiguity, constructs a new candidate, and invokes low-level update
- **AND** it does not invoke generic CLI merge or treat the source name as a special snapshot

### Requirement: Kaoju Environment Guidance Uses Service Requests
Kaoju skills SHALL represent UC-09 as a research intent whose environment mutation is owned by the Service Team through a Service Request.

#### Scenario: Code-run preparation needs Pixi changes
- **WHEN** the environment plan requires package or environment mutation
- **THEN** the pipeline or operator creates a Service Request and the service owner performs the mutation through registered execution
- **AND** Kaoju records the plan and returned environment, gate, smoke script, and result refs without presenting itself as environment owner

### Requirement: Kaoju Export Guidance Does Not Invoke External Wiki Skills
`isomer-kaoju-export` SHALL use only package-owned Isomer CLI and assets for LLM Wiki export, viewer deployment, and viewer launch.

#### Scenario: Wiki export intent executes
- **WHEN** the actor selects `export-survey-wiki`
- **THEN** the skill selects accepted artifacts through state-DB queries and invokes `isomer-cli ext kaoju wiki`
- **AND** it does not route to, mention as a required runtime dependency, or invoke the external `imsight-llm-wiki` skill

### Requirement: Research Skill Validation Enforces Shared Resource Ownership
The research-paradigm validation harness SHALL enforce the skill/shared-resource contract and canonical uppercase artifact identity contract for production research skill families without relying on repository symlink layout.

#### Scenario: Active extension artifact identity is validated
- **WHEN** the validator inspects an active DeepSci or Kaoju skill, registry, binding projection, generated summary, source declaration, or command example
- **THEN** it requires an exact registered `DEEPSCI:WHAT` or `KAOJU:WHAT` identifier owned by the skill's manifest extension
- **AND** it rejects angle-wrapped, double-bracket, bare, lowercase, mixed-case, wrong-family, unknown, duplicate, aliased, or lossy artifact identities without an old-form exemption

#### Scenario: Kaoju active reference leaves its bundle
- **WHEN** the validator finds parent traversal, a sibling-skill link, a family-root contract path, or an absolute source path in active Kaoju filesystem guidance
- **THEN** it fails with the skill, file, line when available, and offending reference
- **AND** it directs a private resource into the owning skill or a shared machine resource behind `isomer-cli ext kaoju`

#### Scenario: Kaoju guidance names a shared contract file
- **WHEN** active Kaoju guidance names `survey-process.v2.json`, `bindings.v2.json`, `bindings.v2.schema.json`, or their package locations as an agent-readable authority
- **THEN** validation fails and names the required `ext kaoju process` or `ext kaoju bindings` query
- **AND** internal package loader code and passive source-provenance material remain outside this active-guidance rule

#### Scenario: Local binding projection is valid
- **WHEN** a Kaoju skill bundles an `artifact-bindings.md` projection for its own semantic ids
- **THEN** validation accepts the page only when it contains no parent-relative registry dependency, does not repeat the full physical registry, uses exact uppercase identifiers, and routes current resolution through `ext kaoju bindings describe`

#### Scenario: Cross-skill process uses Kaoju shared
- **WHEN** a Kaoju stage needs the family-wide evidence, source identity, lineage, Gate, owner-routing, recording, or terminal process
- **THEN** validation requires routing to `isomer-kaoju-shared`
- **AND** it rejects active sibling-file traversal or a known duplicated full process that bypasses the shared skill

#### Scenario: Flat projection fixtures exercise the boundary
- **WHEN** unit tests validate the production Kaoju family or an invalid Kaoju fixture
- **THEN** they copy each skill to an ordinary non-symlink projection with no family-root contracts and test extension queries separately from skill-local links
- **AND** fixtures cover parent traversal, missing local resources, direct registry paths, missing extension-query routing, shared-procedure bypass, and every noncanonical artifact identity class

### Requirement: Production DeepSci Skills Use Canonical Artifact Identifiers
Active production DeepSci skills SHALL use exact uppercase `DEEPSCI:WHAT` artifact identifiers throughout their workflow, registry, binding, source, and record-operation guidance.

#### Scenario: Existing DeepSci registry is replaced
- **WHEN** a DeepSci migration registry or binding page is inspected
- **THEN** every registered artifact uses the deterministic canonical form obtained by removing the old wrapper, converting underscores to hyphens, retaining uppercase letters, and prefixing `DEEPSCI:`
- **AND** the replacement inventory is implementation-only, registry-to-binding coverage remains one-to-one, and no runtime conversion table remains

#### Scenario: Active DeepSci prose names an artifact
- **WHEN** a DeepSci workflow step names an expected input, output, control object, route decision, report, or handoff
- **THEN** it uses the exact registered `DEEPSCI:WHAT` identifier
- **AND** it does not use an angle-wrapped token, double-bracket form, bare object name, lowercase value, or mixed-case value

#### Scenario: DeepSci binding performs a record operation
- **WHEN** an active DeepSci binding page shows how to create, update, revise, list, show, or query a durable artifact
- **THEN** the command passes or filters by the canonical identifier through `--semantic-id`
- **AND** it does not use `--placeholder` or ask the agent or source code to translate between representations

#### Scenario: DeepSci pipeline control artifacts are qualified
- **WHEN** `isomer-deepsci-pipeline` produces or consumes recipe context, terminal report, run record, or resume packet state
- **THEN** it uses `DEEPSCI:PIPELINE-RECIPE-CONTEXT`, `DEEPSCI:PIPELINE-TERMINAL-REPORT`, `DEEPSCI:PIPELINE-RUN-RECORD`, or `DEEPSCI:PIPELINE-RESUME-PACKET` respectively
- **AND** the same identifiers appear in pipeline guidance, bindings, profiles when declared, source constants, record metadata, and tests

#### Scenario: DeepSci source and package mirrors agree
- **WHEN** validation compares the source DeepSci skill tree with packaged system-skill assets
- **THEN** every active artifact identifier and binding reference agrees exactly
- **AND** no source or packaged skill copy retains a superseded artifact identity

### Requirement: Research Skill Validation Preserves Unrelated Family Rules
Adding shared-resource and artifact-identity checks SHALL preserve existing DeepSci and Kaoju content, inventory, binding, evidence, and command-surface validation except where the uppercase clean break explicitly replaces artifact identity behavior.

#### Scenario: Shared boundary validation is introduced
- **WHEN** the research-paradigm validation suite runs after the resource and identifier refactor
- **THEN** existing valid DeepSci and Kaoju behavior continues to pass except for guidance or fixtures that use a removed artifact identity or violate the new ownership boundary
- **AND** family-specific diagnostics unrelated to artifact identity retain their existing meaning and deterministic identifiers where defined

### Requirement: Participating Research Skills Consume Compact Callback Resolution
DeepSci and Kaoju system skills that declare User Skill Callback insertion points SHALL consume the compact execution projection during ordinary workflow execution.

#### Scenario: Skill applies compact callbacks in returned order
- **WHEN** a participating research skill resolves `begin` or `end` callbacks
- **THEN** its workflow guidance tells the agent to process callback entries in their returned order
- **AND** the agent reads each reported `instruction_path` as supplemental instruction material according to its `source_type`

#### Scenario: Skill-directory callback remains supplemental
- **WHEN** a compact callback entry has source type `skill_dir`
- **THEN** the agent reads the reported `SKILL.md` entrypoint and any directly required relative resources as supplemental callback material
- **AND** it does not treat the callback directory as an installed system skill or execute its scripts solely because resolution returned it

#### Scenario: Ordinary workflow avoids explanation metadata
- **WHEN** callback resolution succeeds during a normal participating skill workflow
- **THEN** the skill does not request `--explain` or parse registry, priority, scope, status, Toolbox registration, or gating metadata
- **AND** it uses `--explain`, `list`, `show`, or `validate` only when diagnosis or management is required

#### Scenario: Empty compact resolution continues normally
- **WHEN** ordinary callback resolution returns an empty callback list
- **THEN** the participating skill continues without treating the missing callback as a blocker

#### Scenario: Callback authority remains subordinate
- **WHEN** compact callback instruction material conflicts with higher-priority instructions, the current user request, the owning skill, shared research rules, evidence discipline, required Gates, validation, or recording obligations
- **THEN** the participating skill preserves the higher-priority constraint and reports a material callback conflict

#### Scenario: Skill validation enforces compact consumption
- **WHEN** the research-paradigm skill validation harness inspects callback-participating DeepSci and Kaoju skills
- **THEN** it requires guidance for ordered compact callback consumption and instruction-entrypoint reading
- **AND** it reports ordinary workflow guidance that requests detailed explanation or depends on management-only callback fields
