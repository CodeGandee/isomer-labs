# research-paradigm-skills Specification

## Purpose
Define the reusable Isomer Labs research-paradigm skillset, including portable research-stage skills, shared evidence vocabulary, generic agent mappings, provenance handling, Imsight skill-entrypoint structure, and validation rules that prevent DeepScientist runtime coupling from becoming an Isomer requirement.
## Requirements
### Requirement: Research Paradigm Skillset Layout
The project SHALL provide a reusable research-paradigm skillset under `skillset/research-paradigm/` using Codex skill folder layout and the `isomer-rsch-<purpose>` naming convention for research-stage method skills only.

#### Scenario: Version roots exist
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains versioned skill roots for preserved v1 skills and current v2 skills under `v1/` and `v2/`

#### Scenario: Preserved v1 skill folders exist
- **WHEN** the preserved v1 research-paradigm skillset is inspected
- **THEN** it contains `isomer-rsch-shared-v1` and v1 folders for intake, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, write, review, rebuttal, paper-outline, paper-plot, figure-polish, and science

#### Scenario: Current v2 skill folders exist
- **WHEN** the current v2 research-paradigm skillset is inspected
- **THEN** it contains `isomer-rsch-shared-v2` and v2 folders for scout, baseline, idea, optimize, experiment, analysis, decision, finalize, science, write, review, rebuttal, paper-outline, paper-plot, figure-polish, nature-data, nature-figure, nature-paper2ppt, and nature-polishing

#### Scenario: Migrated v2 companion skills keep bounded traceability material
- **WHEN** a refactor-migrated v2 companion skill is inspected
- **THEN** it MAY contain `migrate/`, `org/analysis/`, `org/src/`, and passive `templates/` material for migration review and provenance
- **AND** active execution guidance remains in `SKILL.md`, `agents/openai.yaml`, directly linked `references/`, active `assets/`, and active `scripts/`

#### Scenario: Skill frontmatter is valid
- **WHEN** each extracted research-stage skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields, and the `name` field matches the `isomer-rsch-<purpose>-vN` folder name for versioned bundles

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Standalone skill bundle is self-contained
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** its active `SKILL.md` and directly linked active resources do not require files outside that skill's directory

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*` as active skill folder names, frontmatter names, manifests, or role mappings

#### Scenario: Operator admin skills are excluded
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** Project Operator Session and Operator Agent orchestration skills are not stored or named as `isomer-rsch-*` skills and instead use the operator admin skillset

### Requirement: Generic Research Vocabulary
The generationed skillset SHALL distinguish research-method semantics from Isomer platform implementation terms.

#### Scenario: V2 uses research-process terms
- **WHEN** a v2 core skill describes the method it performs
- **THEN** it uses research-process terms such as frame, comparator, metric, hypothesis, route, experiment, result, analysis, claim, decision, blocker, limitation, and final summary

#### Scenario: V2 uses semantic placeholders for research objects
- **WHEN** a v2 core skill needs to name a durable or reusable research object
- **THEN** it uses a registered semantic placeholder of the form `[[rsch-object:<id>]]`
- **AND** it does not require that placeholder to be stored as an Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, database row, workspace path, or storage label

#### Scenario: V2 storage-facing terms are bounded
- **WHEN** a v2 skill mentions storage-facing terms such as Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, Workspace Path Resolution, Topic Workspace records, lifecycle rows, execution adapters, or database state
- **THEN** the mention is confined to provenance, migration notes, rejected-storage-binding notes, or explicit statements that storage binding is deferred

#### Scenario: V1 may retain translated implementation vocabulary
- **WHEN** a v1 preserved skill is inspected
- **THEN** it may retain the existing Isomer translation of DeepScientist storage, runtime, lifecycle, and recording terms
- **AND** v1 documentation identifies the content as preserved historical generation material rather than the concise v2 methodology contract

#### Scenario: Source-specific terms remain bounded
- **WHEN** any generation mentions a source-specific or stale term such as DeepScientist, quest, artifact operation, memory operation, command wrapper, source provider name, continuation scheduling, or source-local path
- **THEN** the mention is limited to provenance, adaptation notes, source-term mapping, rejected-runtime notes, or migration notes and is not a required active v2 operation

### Requirement: Shared Research Contract
The skillset SHALL include generation-specific shared research contracts, with v1 preserving the current contract and v2 defining the concise methodology and semantic-placeholder contract.

#### Scenario: V1 shared contract is preserved
- **WHEN** the v1 generation is inspected
- **THEN** it contains `isomer-rsch-shared-v1/SKILL.md` migrated from the previous `isomer-rsch-shared` skill with generation-suffixed names

#### Scenario: V2 shared contract defines semantic placeholders
- **WHEN** `skillset/research-paradigm/v2/isomer-rsch-shared-v2/SKILL.md` and its directly linked references are inspected
- **THEN** they define the v2 research loop, placeholder syntax, placeholder registry location, and rule that placeholders are not storage bindings

#### Scenario: V2 stage skills reference v2 shared rules
- **WHEN** a v2 core skill needs common placeholder, handoff, evidence, or process discipline
- **THEN** it references `isomer-rsch-shared-v2` instead of duplicating long shared rules or referencing v1 shared rules

#### Scenario: V2 shared registry defines placeholder semantics
- **WHEN** the v2 semantic-placeholder registry is inspected
- **THEN** each placeholder entry defines id, meaning, minimum content, producer skills, consumer skills, and storage-binding status

### Requirement: DeepScientist Methodology Preservation
The skillset SHALL preserve DeepScientist-derived material in v1 while distilling v2 to the core research process described by the local DeepScientist skill analysis.

#### Scenario: V1 preserves existing source-derived material
- **WHEN** v1 skill folders are inspected
- **THEN** they retain the existing DeepScientist-derived method, references, provenance, and license context except for generation-suffix renames required by this change

#### Scenario: V2 preserves core process rather than bookkeeping
- **WHEN** a v2 core skill is inspected
- **THEN** it preserves the corresponding stage purpose, entry signals, central research actions, exit criteria, and route guardrails from the core process analysis
- **AND** it omits nonessential storage, runtime, provider, scheduler, lifecycle, and path bookkeeping from active instructions

#### Scenario: V2 does not require source analysis at runtime
- **WHEN** a v2 skill is executed by an agent
- **THEN** the skill contains enough local methodology guidance to run without reading `context/explore/...`, `extern/orphan/...`, archived OpenSpec files, or local absolute paths

#### Scenario: Source lineage remains traceable
- **WHEN** a reader wants to understand why a v2 skill has its process shape
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
Each v2 `isomer-rsch-*-v2` skill SHALL use a concise Imsight-compatible skill entrypoint structure while preserving trigger behavior and research guardrails.

#### Scenario: Workflow section is near the top
- **WHEN** a v2 `SKILL.md` is inspected
- **THEN** it has a near-top `## Workflow` section before detailed guardrail, placeholder, or provenance sections

#### Scenario: Workflow steps are methodology actions
- **WHEN** a v2 `## Workflow` section is inspected
- **THEN** it uses numbered steps that name research-method actions rather than storage, path, adapter, scheduler, or database actions

#### Scenario: Workflow includes freeform fallback
- **WHEN** a v2 `## Workflow` section is inspected
- **THEN** it tells the agent to use its native planning tool to build and execute a step-by-step plan from the skill's constraints and user request when the task does not map cleanly to the default steps

#### Scenario: Reference routing is explicit
- **WHEN** a v2 skill has local references
- **THEN** its entrypoint states which references to read first and which references to read for route-specific, placeholder-specific, validation, or provenance needs

### Requirement: Generic Agent Mapping
The team documentation SHALL map generic research agents to the extracted `isomer-rsch-*` skills without making the skills depend on one team topology.

#### Scenario: Generic role map exists
- **WHEN** the updated team documentation is inspected
- **THEN** it defines generic research roles and lists the `isomer-rsch-*` research-paradigm skills installed for each role

#### Scenario: Skill bundles are topology-neutral
- **WHEN** an extracted skill is inspected
- **THEN** it does not require a specific Houmao specialist name, mailbox route, gateway, credential, or agent topology to perform its research operation

### Requirement: Provenance and Licensing
The implementation SHALL preserve source provenance and license notices for copied, moved, or adapted DeepScientist-derived material across both generations.

#### Scenario: V1 moved materials keep license notices
- **WHEN** existing research-paradigm skills are moved into v1
- **THEN** the v1 generation retains nearby Apache 2.0 or upstream license notices and provenance files that applied before the move

#### Scenario: V2 adapted materials identify source lineage
- **WHEN** a v2 skill materially adapts DeepScientist-derived process content
- **THEN** the v2 skill, v2 shared reference, or research-paradigm provenance file identifies the corresponding source-analysis file or DeepScientist source skill used during distillation

#### Scenario: Source checkout is not a runtime dependency
- **WHEN** v1 or v2 skill instructions are executed
- **THEN** they do not require the local `extern/orphan` source checkout to be present, except as optional provenance context for maintainers

### Requirement: Validation
The implementation SHALL include a repository-runnable validation harness that checks skill structure, naming consistency, Imsight entrypoint formatting, self-containment, placeholder registration, stale terminology, resolved TBD placeholders, local reference integrity, manifest consistency, and removal of runtime-specific coupling with file-role-aware rules.

#### Scenario: Structural validation runs
- **WHEN** the validation harness inspects the research-paradigm skillset
- **THEN** validation confirms each expected `isomer-rsch-*` skill folder has a valid `SKILL.md`, valid frontmatter, expected supporting resources, and directly linked one-level active references

#### Scenario: Expected versioned inventory is validated
- **WHEN** the validation harness inspects `skillset/research-paradigm/v1` and `skillset/research-paradigm/v2`
- **THEN** validation confirms the v1 inventory contains the preserved v1 skills and the v2 inventory contains the current core, companion, and Nature-facing v2 skills listed in the skillset layout requirement

#### Scenario: Naming validation runs
- **WHEN** the validation harness inspects the research-paradigm skillset
- **THEN** validation confirms every active skill folder, `SKILL.md` frontmatter `name:`, manifest `interface.display_name`, manifest `default_prompt`, and active role mapping uses `isomer-rsch-*` versioned names consistently

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

#### Scenario: V2 storage binding remains deferred
- **WHEN** the validation harness inspects active v2 skill text
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
- **THEN** validation treats `isomer-rsch-shared/references/tbd-surface-registry.md` as the canonical registry for the subtree

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
- **WHEN** a skill's `agents/openai.yaml` `interface.display_name` does not equal the skill folder and `SKILL.md` frontmatter name, or `interface.default_prompt` does not invoke the same `$isomer-rsch-*` skill
- **THEN** validation reports the manifest mismatch and identifies the affected manifest field

#### Scenario: Validator tests cover active and non-active zones
- **WHEN** unit tests exercise the research-paradigm validation harness
- **THEN** they include fixtures for expanded v2 inventory, migrated companion-skill traceability directories, passive templates, active stale-term failures, allow-zone acceptance, concrete broken references, pattern references, placeholder registration, storage-binding deferral, and deterministic CLI output

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
Research-paradigm documentation SHALL distinguish research-stage skills from operator/admin skills instead of presenting Project Operator Session orchestration as research method.

#### Scenario: Research docs point to operator skillset
- **WHEN** research-paradigm README or role mapping documentation mentions project operation, Topic Team Specialization orchestration, Service Request routing, profile materialization, approval, or team launch
- **THEN** it points to the `isomer-admin-*` operator skillset rather than listing those capabilities as `isomer-rsch-*` research-stage skills

#### Scenario: Research role mappings avoid admin skills
- **WHEN** generic research agent role mappings are inspected
- **THEN** ordinary research roles such as scout, baseline, experiment, analysis, writer, reviewer, or synthesis reviewer do not install `isomer-admin-*` skills unless the role is explicitly an Operator Agent role

### Requirement: V2 Semantic Placeholder Contract
The v2 research-paradigm skillset SHALL define semantic placeholders before binding research objects to Isomer storage.

#### Scenario: Placeholder syntax is stable
- **WHEN** a v2 skill names a research object whose storage binding is deferred
- **THEN** it uses the syntax `[[rsch-object:<id>]]`

#### Scenario: Placeholder ids are semantic
- **WHEN** a placeholder id is defined
- **THEN** the id names research meaning rather than storage mechanism, for example `research-frame`, `comparator-contract`, `selected-hypothesis`, `experiment-result`, `analysis-finding`, `route-decision`, or `final-summary`

#### Scenario: Placeholder registry is authoritative for v2
- **WHEN** v2 placeholder meaning is inspected
- **THEN** the authoritative definitions live in `skillset/research-paradigm/v2/isomer-rsch-shared-v2/references/semantic-placeholders.md`

#### Scenario: Placeholder entry has minimum semantic fields
- **WHEN** a placeholder entry is inspected
- **THEN** it defines id, plain-language meaning, required semantic content, typical producer skills, typical consumer skills, and storage-binding status

#### Scenario: Placeholder entry rejects premature storage binding
- **WHEN** a placeholder entry is inspected
- **THEN** it states that the placeholder is not yet bound to Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, path, storage label, or database schema

### Requirement: V2 Core Research Process
The v2 core skillset SHALL organize research conduction around the core process rather than around implementation bookkeeping.

#### Scenario: Core loop is documented
- **WHEN** `isomer-rsch-shared-v2` is inspected
- **THEN** it documents the loop `Frame -> Comparator -> Hypothesis -> Experiment -> Analysis -> Decision -> Finalize`

#### Scenario: Optimize is an overlay
- **WHEN** `isomer-rsch-optimize-v2` is inspected
- **THEN** it describes optimization as an overlay on hypothesis, experiment, and analysis work rather than as a separate storage model

#### Scenario: Science is a computation-validity companion
- **WHEN** `isomer-rsch-science-v2` is inspected
- **THEN** it describes scientific computation, package checks, simulations, dataset analysis, and validation as support for the core research loop rather than as a separate storage model

#### Scenario: Each v2 stage declares semantic handoff
- **WHEN** any v2 core skill is inspected
- **THEN** it declares the semantic inputs it expects and the semantic outputs it produces using registered placeholders

#### Scenario: V2 guardrails preserve research judgment
- **WHEN** a v2 core skill is inspected
- **THEN** it includes guardrails for false progress, missing comparator or metric, unsupported claims, non-comparable experiments, failed or null results, and premature finalization where relevant to that stage

### Requirement: V2 Research Workspace Manager Skill
The research-paradigm skillset SHALL include an `isomer-rsch-workspace-mgr-v2` skill that performs research-specific Topic Workspace bootstrap after Topic Team Specialization and full Topic Workspace initialization.

#### Scenario: Workspace manager skill exists
- **WHEN** the v2 research-paradigm skillset is inspected
- **THEN** it contains `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/SKILL.md` with valid frontmatter, workflow, reference routing, fallback guidance, and an `agents/openai.yaml` manifest that invokes `$isomer-rsch-workspace-mgr-v2`

#### Scenario: Workspace manager runs after specialization
- **WHEN** the skill explains its entry conditions
- **THEN** it requires a selected Research Topic, a fully initialized Topic Workspace, completed Topic Team Specialization material, Workspace Runtime readiness, and Agent Workspace context before ordinary v2 research skills rely on its bootstrap outputs

#### Scenario: Workspace manager is distinct from operator topology management
- **WHEN** the skill describes its boundary
- **THEN** it states that `isomer-admin-topic-workspace-mgr` remains the operator topology helper while `isomer-rsch-workspace-mgr-v2` owns research placeholder binding and v2 storage bootstrap guidance

#### Scenario: Topic Service Master is optional
- **WHEN** the skill describes the actor that performs bootstrap
- **THEN** it names the Topic Service Master as the preferred topic-workspace manager when started and states that the Project Operator Session or Operator Agent performs the same bounded work when no Topic Service Master is running

### Requirement: V2 Research Storage Bootstrap Contract
The `isomer-rsch-workspace-mgr-v2` skill SHALL define consistent placeholders and outputs for research storage bootstrap, using the same placeholder registry style as the other v2 research skills.

#### Scenario: Manager placeholder registry exists
- **WHEN** `isomer-rsch-workspace-mgr-v2/migrate/placeholders.md` is inspected
- **THEN** it defines placeholders for workspace context, storage label planning, placeholder binding registry, storage bootstrap record, agent access plan, bootstrap validation report, and workspace blocker record

#### Scenario: Placeholder kinds use existing v2 storage mapping
- **WHEN** the manager placeholder registry is inspected
- **THEN** every placeholder has a `Kind` value from the existing v2 placeholder kind set and maps to the storage item mapping for evidence, report, handoff, decision, runtime state, or related accepted kinds

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
The research-paradigm validation harness SHALL recognize `isomer-rsch-workspace-mgr-v2` as an expected v2 skill and apply the normal v2 structure and placeholder checks to it.

#### Scenario: Validator expects workspace manager
- **WHEN** the research-paradigm validation harness runs against the repository skillset
- **THEN** it treats `isomer-rsch-workspace-mgr-v2` as part of the expected v2 skill set

#### Scenario: Validator checks manager placeholders
- **WHEN** active manager skill text uses migration placeholders
- **THEN** validation confirms those placeholders are registered in `isomer-rsch-workspace-mgr-v2/migrate/placeholders.md`

### Requirement: V2 Skills Read Placeholder Bindings
Active v2 research skills SHALL read local placeholder binding pages before writing durable placeholder outputs.

#### Scenario: Skill entrypoint names binding page
- **WHEN** an active v2 research skill has placeholder definitions
- **THEN** its `SKILL.md` tells the agent that placeholder definitions live in `migrate/placeholders.md` and storage bindings live in `placeholder-bindings.md`

#### Scenario: Durable output uses binding page
- **WHEN** a v2 skill step produces a durable placeholder output
- **THEN** the skill instructs the agent to use the corresponding `placeholder-bindings.md` row rather than inventing a path or directly editing Workspace Runtime

#### Scenario: Compatibility fallback remains bounded
- **WHEN** a v2 skill still needs a source-shaped DeepScientist compatibility call
- **THEN** the skill allows `isomer-cli ext deepsci call ...` only as a compatibility fallback and still summarizes durable meaning through the placeholder binding

### Requirement: Binding Pages Preserve Workflow Flexibility
The v2 research skills SHALL keep placeholders in workflow prose and bind them through local binding pages.

#### Scenario: Workflow placeholders are not replaced
- **WHEN** placeholder binding pages are added to v2 skills
- **THEN** the existing workflow steps keep semantic placeholders such as `<MAIN_RUN_RECORD>` and `<NEXT_ROUTE_DECISION>` instead of replacing them with concrete paths or record ids

#### Scenario: Binding updates do not rewrite method prose
- **WHEN** a storage target changes from extension-backed CRUD to a future native command
- **THEN** the binding page can change without requiring workflow prose to rename the placeholder

### Requirement: Writing Artifacts Use Paper-Line Placeholder Bindings
The research-paradigm v2 skillset SHALL map writing-related placeholders to paper-line storage profiles through local `placeholder-bindings.md` pages while preserving placeholders in workflow prose.

#### Scenario: Paper contract binding uses a paper contract view
- **WHEN** a v2 skill binds a placeholder that represents the active paper contract, selected outline, evidence view, paper view, section writing plan, or claim-evidence boundary
- **THEN** the binding maps it to an Isomer record kind and profile that preserves its paper-line role, such as `view_manifest` with `paper.contract.selected-outline`, `artifact` with `paper.outline.*`, or `view_manifest` with `paper.claim-evidence-map`

#### Scenario: Paper control surfaces use view records
- **WHEN** a v2 skill binds a placeholder that represents the paper evidence ledger, experiment matrix, manuscript validation, outline validation, paper-line state, or other paper control surface
- **THEN** the binding uses `topic.records.views` with a paper-specific profile such as `paper.evidence-ledger`, `paper.experiment-matrix`, `paper.validation.*`, or `paper.line-state`

#### Scenario: Paper bodies use artifact records
- **WHEN** a v2 skill binds a placeholder that represents manuscript drafts, LaTeX material, bibliography files, compile reports, PDFs, review reports, rebuttal packets, response letters, final summaries, or paper bundle manifests
- **THEN** the binding uses `topic.records.artifacts` with a paper, review, rebuttal, figure, release, or package profile rather than a generic report or handoff profile when a more precise profile exists

#### Scenario: Paper work queues use task records when resumable
- **WHEN** a v2 skill binds a placeholder that represents a resumable writing plan, reviewer-linked evidence TODO, or paper-facing work queue
- **THEN** the binding uses `research_task` under `topic.records.tasks` when the item must be resumed, assigned, or queried as work, and may use `view_manifest` only when the item is a read-only board

#### Scenario: Binding commands include queryable paper metadata
- **WHEN** a v2 skill binding provides an `isomer-cli ext research records` create or update command for a writing-related placeholder
- **THEN** the command includes explicit `--semantic-label`, `--profile`, `--placeholder`, `--skill`, producer, consumer, and any natural query metadata such as `selected_outline_ref`, `paper_surface`, `package_type`, `section_id`, `claim_id`, or `reviewer_item_id`

#### Scenario: Binding convention avoids paper-specific semantic labels
- **WHEN** writing-related v2 binding pages are updated
- **THEN** they use existing semantic labels such as `topic.records.views`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, and `topic.records.logs`
- **AND** they do not introduce paper-specific top-level semantic labels as required storage surfaces

#### Scenario: Workflow placeholders remain stable
- **WHEN** writing-related binding rows are updated
- **THEN** `SKILL.md` workflow prose keeps the existing placeholder tokens and relies on `placeholder-bindings.md` for storage mapping

#### Scenario: Placeholder registries change only for real drift
- **WHEN** implementation inspects `migrate/placeholders.md` for writing-related skills
- **THEN** it changes placeholder definitions only when a placeholder is missing or its kind conflicts with the durable storage role that the binding page must express

### Requirement: Research Workspace Bootstrap Supports Actor Topology
The v2 research workspace bootstrap SHALL support base topic readiness, Topic Actor readiness, and optional formal team readiness as composable topology layers.

#### Scenario: Bootstrap accepts Topic Actor readiness
- **WHEN** `isomer-rsch-workspace-mgr-v2` or its successor runs for human-orchestrated research
- **THEN** it validates the selected Topic Workspace, Workspace Runtime, Research Topic overview, topic environment readiness, ready `topic.repos.main`, available research record labels, skill-local placeholder binding files, the topic-level placeholder binding index or readiness report, selected Topic Actor bindings, and selected Topic Actor Workspaces
- **AND** it does not require Topic Agent Team Profile material, formal Agent Workspace access plans, per-Agent Instance cwd proof, Agent Instance records, or Agent Team Instance records unless the selected topology includes a formal team layer

#### Scenario: Placeholder binding index points to skill-local authority
- **WHEN** research workspace bootstrap creates or validates a topic-level placeholder binding index
- **THEN** the index references relevant skill-local `placeholder-bindings.md` files and their selected placeholder groups
- **AND** the bootstrap treats skill-local files as authoritative when the index and skill-local binding content disagree

#### Scenario: Bootstrap keeps formal team checks when present
- **WHEN** the research workspace bootstrap runs in a Topic Workspace with formal team material selected for use
- **THEN** it keeps the existing post-specialization checks for topic team summary, profile material, formal Agent Workspace access, and worker-visible storage boundaries

### Requirement: V2 Skills Read Placeholder Bindings from Actor Workspaces
The v2 research skills SHALL use skill-local placeholder binding guidance to map workflow placeholders to Topic Workspace records from Topic Actor Workspaces, topic-main, or formal Agent Workspaces.

#### Scenario: Actor skill run resolves placeholders through bindings
- **WHEN** a Topic Actor runs a v2 research skill from its Topic Actor Workspace
- **THEN** the skill reads its `placeholder-bindings.md` and uses the listed record kind, semantic label, profile, topic actor metadata, and `isomer-cli ext research records` command shape for accepted research artifacts
- **AND** it does not replace workflow placeholders with hard-coded Topic Actor Workspace paths in `SKILL.md`

#### Scenario: Missing binding blocks accepted record write
- **WHEN** a v2 skill needs to write an accepted artifact but no binding exists for the placeholder
- **THEN** the skill reports the missing binding as a blocker instead of writing the artifact only to local scratch, a Topic Actor Workspace, a formal Agent Workspace, or an untracked repo path

