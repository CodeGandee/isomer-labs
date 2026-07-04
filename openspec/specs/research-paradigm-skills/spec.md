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

### Requirement: Production DeepSci Semantic Placeholder Contract
The production DeepSci research-paradigm skillset SHALL define semantic placeholders before binding research objects to Isomer storage.

#### Scenario: Placeholder syntax is stable
- **WHEN** a production DeepSci skill names a research object whose storage binding is deferred
- **THEN** it uses the syntax `[[rsch-object:<id>]]`

#### Scenario: Placeholder ids are semantic
- **WHEN** a placeholder id is defined
- **THEN** the id names research meaning rather than storage mechanism, for example `research-frame`, `comparator-contract`, `selected-hypothesis`, `experiment-result`, `analysis-finding`, `route-decision`, or `final-summary`

#### Scenario: Placeholder registry is authoritative for production DeepSci
- **WHEN** production DeepSci placeholder meaning is inspected
- **THEN** the authoritative definitions live in `skillset/research-paradigm/deepsci/isomer-deepsci-shared/references/semantic-placeholders.md`

#### Scenario: Placeholder entry has minimum semantic fields
- **WHEN** a placeholder entry is inspected
- **THEN** it defines id, plain-language meaning, required semantic content, typical producer skills, typical consumer skills, and storage-binding status

#### Scenario: Placeholder entry rejects premature storage binding
- **WHEN** a placeholder entry is inspected
- **THEN** it states that the placeholder is not yet bound to Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, path, storage label, or database schema

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

### Requirement: Binding Pages Preserve Workflow Flexibility
The production DeepSci research skills SHALL keep placeholders in workflow prose and bind them through local binding pages.

#### Scenario: Workflow placeholders are not replaced
- **WHEN** placeholder binding pages are added to production DeepSci skills
- **THEN** the existing workflow steps keep semantic placeholders such as `<MAIN_RUN_RECORD>` and `<NEXT_ROUTE_DECISION>` instead of replacing them with concrete paths or record ids

#### Scenario: Binding updates do not rewrite method prose
- **WHEN** a storage target changes from extension-backed CRUD to a future native command
- **THEN** the binding page can change without requiring workflow prose to rename the placeholder

### Requirement: Writing Artifacts Use Paper-Line Placeholder Bindings
The research-paradigm production DeepSci skillset SHALL map writing-related placeholders to paper-line storage profiles through local `placeholder-bindings.md` pages while preserving placeholders in workflow prose.

#### Scenario: Paper contract binding uses a paper contract view
- **WHEN** a production DeepSci skill binds a placeholder that represents the active paper contract, selected outline, evidence view, paper view, section writing plan, or claim-evidence boundary
- **THEN** the binding maps it to an Isomer record kind and profile that preserves its paper-line role, such as `view_manifest` with `paper.contract.selected-outline`, `artifact` with `paper.outline.*`, or `view_manifest` with `paper.claim-evidence-map`

#### Scenario: Paper control surfaces use view records
- **WHEN** a production DeepSci skill binds a placeholder that represents the paper evidence ledger, experiment matrix, manuscript validation, outline validation, paper-line state, or other paper control surface
- **THEN** the binding uses `topic.records.views` with a paper-specific profile such as `paper.evidence-ledger`, `paper.experiment-matrix`, `paper.validation.*`, or `paper.line-state`

#### Scenario: Paper bodies use artifact records
- **WHEN** a production DeepSci skill binds a placeholder that represents manuscript drafts, LaTeX material, bibliography files, compile reports, PDFs, review reports, rebuttal packets, response letters, final summaries, or paper bundle manifests
- **THEN** the binding uses `topic.records.artifacts` with a paper, review, rebuttal, figure, release, or package profile rather than a generic report or handoff profile when a more precise profile exists

#### Scenario: Paper work queues use task records when resumable
- **WHEN** a production DeepSci skill binds a placeholder that represents a resumable writing plan, reviewer-linked evidence TODO, or paper-facing work queue
- **THEN** the binding uses `research_task` under `topic.records.tasks` when the item must be resumed, assigned, or queried as work, and may use `view_manifest` only when the item is a read-only board

#### Scenario: Binding commands include queryable paper metadata
- **WHEN** a production DeepSci skill binding provides an `isomer-cli ext research records` create or update command for a writing-related placeholder
- **THEN** the command includes explicit `--semantic-label`, `--profile`, `--placeholder`, `--skill`, producer, consumer, and any natural query metadata such as `selected_outline_ref`, `paper_surface`, `package_type`, `section_id`, `claim_id`, or `reviewer_item_id`

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
- **THEN** its workflow or entry guidance references the shared latest-context preflight from `isomer-rsch-shared-v2`
- **AND** it places the preflight before accepted record writes, record refreshes, or durable stage decisions that select routes, accept comparator state, generate ideas, run experiments, analyze evidence, write claims, review manuscripts, create figures, polish prose, prepare data availability, rebut reviewers, or finalize a topic
- **AND** standalone source-only reading may skip the preflight until the skill writes or refreshes accepted Isomer records

#### Scenario: Shared skill owns the reference
- **WHEN** `isomer-rsch-shared-v2` is inspected
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
- **WHEN** validation inspects `isomer-rsch-shared-v2`, migration notes, source-copy material under `org/`, passive templates, or non-active provenance material
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
