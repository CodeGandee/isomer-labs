## MODIFIED Requirements

### Requirement: Research Paradigm Skillset Layout
The project SHALL provide generationed reusable research-paradigm skillsets under `skillset/research-paradigm/`, with preserved v1 skills under `v1/` and active core-methodology v2 skills under `v2/`.

#### Scenario: Generation directories exist
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains `skillset/research-paradigm/v1/` and `skillset/research-paradigm/v2/`

#### Scenario: Root contains no active flat research skill folders
- **WHEN** direct children of `skillset/research-paradigm/` are inspected
- **THEN** no active skill folder named `isomer-rsch-*` exists directly under the root generation directory

#### Scenario: V1 skill folders preserve existing skills
- **WHEN** the v1 generation is inspected
- **THEN** every research-paradigm skill that existed before this change is present under `skillset/research-paradigm/v1/` with a folder name of the form `isomer-rsch-<purpose>-v1`

#### Scenario: V2 core skill folders exist
- **WHEN** the v2 generation is inspected
- **THEN** it contains `isomer-rsch-shared-v2`, `isomer-rsch-scout-v2`, `isomer-rsch-baseline-v2`, `isomer-rsch-idea-v2`, `isomer-rsch-optimize-v2`, `isomer-rsch-experiment-v2`, `isomer-rsch-analysis-v2`, `isomer-rsch-decision-v2`, `isomer-rsch-finalize-v2`, and `isomer-rsch-science-v2`

#### Scenario: V2 excludes paper-production skills in first pass
- **WHEN** the v2 generation is inspected after this change
- **THEN** it does not contain v2 folders for write, review, rebuttal, paper-outline, paper-plot, or figure-polish
- **AND** those preserved skills remain available under v1

#### Scenario: Skill frontmatter is generation-suffixed
- **WHEN** any v1 or v2 research skill `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields
- **AND** the `name` field exactly matches the generation-suffixed folder name

#### Scenario: Skill manifest matches generation-suffixed name
- **WHEN** any v1 or v2 research skill includes an `agents/openai.yaml` manifest
- **THEN** its UI-facing display name and default prompt use the same generation-suffixed skill name as the folder and `SKILL.md` frontmatter

#### Scenario: Operator admin skills remain excluded
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
The skillset SHALL keep v2 skill entrypoints concise and use references only for shared semantic contracts or genuinely necessary method detail.

#### Scenario: V2 entrypoint has concise method sections
- **WHEN** a v2 `SKILL.md` is inspected
- **THEN** it contains compact sections for purpose, when to use, workflow, semantic inputs, semantic outputs, guardrails, and source lineage when needed

#### Scenario: V2 references are bounded
- **WHEN** a v2 skill links local references
- **THEN** those references are one level below the skill folder and support placeholder semantics, route guardrails, or source lineage rather than storage implementation detail

#### Scenario: V2 active skill bundle is self-contained
- **WHEN** a v2 `SKILL.md` and directly linked references are inspected
- **THEN** they do not actively require files outside the v2 skill directory except for intentional references to `isomer-rsch-shared-v2` within the same generation

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
The implementation SHALL include or update repository-runnable validation that checks generationed skill structure, naming consistency, v2 placeholder registration, v2 storage-binding deferral, local reference integrity, manifest consistency, and provenance boundaries.

#### Scenario: Generationed structural validation runs
- **WHEN** the validation harness inspects `skillset/research-paradigm`
- **THEN** it confirms v1 and v2 generation directories exist, no active flat root `isomer-rsch-*` folders remain, and expected v1 and v2 skill folders are present

#### Scenario: Generationed naming validation runs
- **WHEN** the validation harness inspects v1 and v2 skills
- **THEN** it confirms every skill folder, `SKILL.md` frontmatter `name:`, manifest display name, and manifest default prompt uses the matching `-v1` or `-v2` generation suffix

#### Scenario: V2 placeholder registry validation runs
- **WHEN** the validation harness finds `[[rsch-object:<id>]]` in a v2 skill
- **THEN** it confirms the placeholder id is listed in the v2 semantic-placeholder registry

#### Scenario: V2 unregistered placeholder is reported
- **WHEN** a v2 skill emits a `[[rsch-object:<id>]]` placeholder whose id is absent from the v2 registry
- **THEN** validation reports the unregistered id and identifies the file and line that emitted it

#### Scenario: V2 storage binding is reported
- **WHEN** active v2 skill guidance requires Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, concrete path, storage label, runtime row, scheduler field, or execution adapter behavior
- **THEN** validation reports the storage binding unless the occurrence is inside an allowed provenance, migration, or rejected-storage-binding zone

#### Scenario: V1 storage vocabulary is allowed as preserved material
- **WHEN** validation scans v1 preserved skills
- **THEN** it allows existing storage, runtime, lifecycle, and DeepScientist translation vocabulary that remains bounded by v1 provenance and migration context

#### Scenario: V2 workflow formatting is validated
- **WHEN** validation inspects a v2 `SKILL.md`
- **THEN** it confirms the file has a near-top `## Workflow`, numbered workflow steps, concise reference routing when references exist, and a fallback for tasks that do not map cleanly to the default steps

#### Scenario: Local reference validation runs
- **WHEN** validation inspects v1 or v2 skill entrypoints and linked references
- **THEN** it reports broken local references and active dependencies on `context/explore`, `extern/orphan`, archived OpenSpec paths, local absolute paths, or other paths outside the intended generation boundary

#### Scenario: Repository command runs validation
- **WHEN** a developer or agent runs the repository skillset validation command
- **THEN** the command validates `skillset/research-paradigm`, prints deterministic diagnostics as `path:line: code message`, and exits nonzero when validation errors exist

## ADDED Requirements

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

## REMOVED Requirements

### Requirement: Unsettled Concrete Surfaces Are Explicit
**Reason**: The v2 rewrite intentionally defers concrete surfaces and storage binding. Requiring v2 skills to classify unresolved APIs, providers, policies, schemas, and storage roots would reintroduce the bookkeeping layer this change removes from active methodology skills.

**Migration**: Preserve the old treatment in v1. Future storage-binding work can introduce a new v2 binding contract after the semantic placeholders are stable.

#### Scenario: V2 does not classify platform TBDs
- **WHEN** a v2 skill needs to name a research object
- **THEN** it uses a semantic placeholder rather than a platform TBD-surface placeholder

### Requirement: Parallelized Skill Enrichment
**Reason**: The first v2 pass is a concise semantic rewrite, not a large enrichment pass that must preserve every source detail through parallel workers.

**Migration**: Preserve enriched v1 content as the historical generation. Use ordinary implementation planning for the smaller v2 core rewrite.

#### Scenario: V2 implementation is not required to use subagents
- **WHEN** the v2 core skills are implemented
- **THEN** the implementation is valid if it satisfies the generation, placeholder, provenance, and validation requirements without using subagents

### Requirement: Workspace Path Resolution Consumption
**Reason**: V2 skill instructions must not bind semantic research objects to workspace paths yet.

**Migration**: Keep path-resolution behavior in the platform contracts and v1 migration history. Bind v2 placeholders to paths only in a later storage-design change.

#### Scenario: V2 does not request semantic paths
- **WHEN** a v2 skill describes a research object
- **THEN** it uses a registered `[[rsch-object:<id>]]` placeholder instead of requesting a Workspace Path Resolution label

### Requirement: Research Recording Contract Consumption
**Reason**: V2 skill instructions must not bind semantic research objects to recording contract types yet.

**Migration**: Keep the research recording contracts available for the later storage-binding phase. For this change, v2 skills define semantics only.

#### Scenario: V2 does not require record APIs
- **WHEN** a v2 skill describes a research object
- **THEN** it uses a registered `[[rsch-object:<id>]]` placeholder instead of requiring an Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, or Provenance Record

### Requirement: Research Lifecycle State Consumption
**Reason**: V2 skill instructions should describe research process flow without forcing lifecycle-state objects into every stage.

**Migration**: Preserve lifecycle-state consumption in platform specs and v1 content. Later binding work may map placeholders and stage transitions to lifecycle state.

#### Scenario: V2 does not require lifecycle objects
- **WHEN** a v2 skill routes from one research action to another
- **THEN** it names the next research action or semantic output rather than requiring a Workflow Stage Cursor, Research Inquiry Relationship, Research Task, or Agent Team Instance state update

### Requirement: Research Execution Extension Contract Consumption
**Reason**: V2 skill instructions should state what research execution must answer, not which extension point, adapter, provider, scheduler, or policy records implement it.

**Migration**: Preserve execution-extension contracts in platform specs and v1 content. Later binding work may map v2 experiment and science placeholders to execution-extension mechanisms.

#### Scenario: V2 does not require execution extension refs
- **WHEN** a v2 skill needs computation, literature lookup, package checking, experiment execution, rendering, or analysis
- **THEN** it states the research action and semantic output rather than requiring an Execution Adapter Command Request, provider binding, scheduler policy, Skill Binding projection, baseline-waiver policy, or Gate policy ref
