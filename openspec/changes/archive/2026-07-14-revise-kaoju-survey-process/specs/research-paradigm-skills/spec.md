## MODIFIED Requirements

### Requirement: Research-Paradigm Validation Supports Kaoju
The research-paradigm validation harness SHALL validate the fourteen-skill Kaoju survey-process family through family-specific rules while preserving all existing DeepSci checks.

#### Scenario: Valid Kaoju family passes validation
- **WHEN** the validator inspects the complete production Kaoju family
- **THEN** it accepts the exact fourteen-skill inventory, valid frontmatter and manifests, near-top workflows, approved survey-intent and compatibility command inventory, self-contained direct references, canonical namespace, and binding-registry use

#### Scenario: Invalid Kaoju family reports deterministic diagnostics
- **WHEN** a Kaoju skill is missing, uses the wrong namespace, has manifest identity drift, references a missing local file, hardcodes a local or provider-specific runtime path, scans for durable records, repeats a physical binding as independent authority, invokes an unregistered executable path, treats Markdown or TeX as canonical paper content, invokes the external wiki skill, mutates Pixi state directly, or exposes an unapproved procedure
- **THEN** validation fails with a deterministic diagnostic that names the file, line when available, skill, semantic id when applicable, and violated Kaoju rule

#### Scenario: Shared checks do not erase family-specific checks
- **WHEN** common frontmatter, manifest, reference, CLI-spelling, terminology, or binding checks are refactored for multiple families
- **THEN** DeepSci retains its inventory, placeholder, source-lineage, structured-output, and other existing family-specific validation
- **AND** the existing DeepSci validation tests continue to pass unchanged in meaning

#### Scenario: Validator tests cover Kaoju active and invalid zones
- **WHEN** unit tests exercise family-aware research-paradigm validation
- **THEN** they include valid Kaoju fixtures and failures for missing inventory, wrong namespace, manifest mismatch, broken direct references, stale domain terms, hard-coded provider or local paths, procedural-command drift, binding drift, directory scanning, canonical-format violations, external wiki routing, and direct environment mutation
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

## ADDED Requirements

### Requirement: Kaoju Skills Separate Research Judgment from Deterministic Operations
Production Kaoju skills SHALL make research and human-interaction decisions while delegating deterministic state and executable operations to typed Isomer CLI and owner services.

#### Scenario: Skill performs research judgment
- **WHEN** a procedure selects a direction, appraises a source, forms or qualifies a claim, audits evidence, writes paper prose, interprets code, repairs TeX semantics, or recommends a trial design
- **THEN** the responsible Kaoju capability skill performs and records that judgment with evidence and actor provenance

#### Scenario: Skill needs deterministic mutation
- **WHEN** the procedure persists an artifact, resolves a managed path, acquires a repository, exports or applies a template, initializes a conversion, dispatches environment support, executes a trial, builds a PDF, exports a wiki, deploys a viewer, or launches a process
- **THEN** it invokes the applicable typed CLI or owner service and consumes returned durable refs
- **AND** it does not substitute prose instructions for a missing deterministic contract

### Requirement: Kaoju Write Guidance Is MyST-First
`isomer-kaoju-write` SHALL treat MyST structure, template, and draft artifacts as canonical and SHALL treat Markdown, TeX, and PDF as derived views or publication artifacts.

#### Scenario: Write skill starts a paper
- **WHEN** accepted audit and synthesis inputs are available
- **THEN** the skill creates and fills MyST artifacts, citation mapping, and revision provenance before requesting derived publication artifacts
- **AND** it does not create `kaoju:survey-manuscript` or `kaoju:writing-template` as new canonical state

#### Scenario: TeX requires semantic repair
- **WHEN** the paper service initializes TeX from MyST
- **THEN** the write skill inspects and directly repairs directives, tables, citations, floats, raw blocks, and venue structure before build readiness
- **AND** a script or successful compiler exit does not replace this inspection obligation

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
