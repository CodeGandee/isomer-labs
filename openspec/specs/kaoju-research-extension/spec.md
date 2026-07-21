# kaoju-research-extension Specification

## Purpose
TBD - created by archiving change implement-kaoju-research-extension. Update Purpose after archive.
## Requirements
### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju pack with independent public welcome and execution entrypoint bundles plus the existing protected `isomer-kaoju-<purpose>` capabilities.

#### Scenario: Kaoju public pair exists
- **WHEN** packaged Kaoju assets are inspected
- **THEN** sibling bundles `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint` contain valid public skill metadata
- **AND** the thirteen current Kaoju capabilities remain protected below the entrypoint

#### Scenario: Kaoju welcome is self-contained
- **WHEN** `isomer-ext-kaoju-welcome` is copied or linked as part of the pack
- **THEN** it resolves its active typical-use-case and command-map resources without loading private files from the entrypoint or protected subskills
- **AND** it may reference public entrypoint invocation names without becoming an execution owner

#### Scenario: Shared machine contracts remain package-owned
- **WHEN** welcome or entrypoint needs current Kaoju command or process metadata
- **THEN** checked machine contracts remain owned by the installed Kaoju Python package and manifest
- **AND** welcome does not introduce a second survey-process registry

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains public directory `isomer-ext-kaoju-entrypoint`
- **AND** that pack contains protected bundles for `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, and `isomer-kaoju-export`
- **AND** no `isomer-kaoju-pipeline` skill folder or duplicate facade is active

#### Scenario: Public identity is consistent
- **WHEN** the Kaoju public pack is inspected
- **THEN** its folder, frontmatter, metadata, and public default prompt use `isomer-ext-kaoju-entrypoint`

#### Scenario: Protected identity is consistent
- **WHEN** a protected Kaoju bundle is inspected
- **THEN** its folder and frontmatter retain its `isomer-kaoju-*` logical id
- **AND** its active resources remain self-contained

#### Scenario: Trial and reproduction remain distinct
- **WHEN** executable evidence members are inspected
- **THEN** `trial` maps to `isomer-kaoju-trial` and `reproduce` maps to `isomer-kaoju-reproduce`
- **AND** neither capability weakens the accepted evidence distinction

#### Scenario: Artifact identity is consistent
- **WHEN** a protected Kaoju member names a durable extension artifact
- **THEN** it continues to use the exact registered `KAOJU:WHAT` identifier

### Requirement: Kaoju Pipeline Command Surface
`isomer-ext-kaoju-entrypoint` SHALL remain the single Kaoju execution entrypoint, and `isomer-ext-kaoju-welcome` SHALL provide a separate read-only teaching surface for its survey intents, compatibility procedures, and grouped managers.

#### Scenario: Concrete Kaoju task uses entrypoint
- **WHEN** a user requests reading-list work, source ingestion, direction selection, comparison, code preparation, trial execution, paper production, or wiki export
- **THEN** `isomer-ext-kaoju-entrypoint` selects and executes the applicable public command or protected capability
- **AND** existing interaction, evidence, Gate, checkpoint, and terminal contracts remain in force

#### Scenario: Newcomer asks how to use Kaoju
- **WHEN** a user asks what Kaoju is designed for, which procedure fits, or how to form a request
- **THEN** `isomer-ext-kaoju-welcome` presents curated typical use cases and exact entrypoint examples
- **AND** it does not run a Kaoju manager or research procedure

#### Scenario: Historical pipeline identity is used
- **WHEN** compatibility lookup encounters `isomer-kaoju-pipeline`
- **THEN** it resolves to `isomer-ext-kaoju-entrypoint`
- **AND** it does not resolve to the welcome skill

#### Scenario: Nested manager form is taught
- **WHEN** welcome explains a grouped manager or nested subcommand such as paper-template management
- **THEN** it shows the accepted public entrypoint command form and representative task
- **AND** it does not expose internal object-generator notation as the ordinary user invocation

#### Scenario: Survey-process commands match ten use cases
- **WHEN** public help is inspected
- **THEN** it exposes `choose-directions`, `build-reading-list`, `ingest-reading-item`, `draft-paper`, `manage-paper-template`, `build-paper-pdf`, `export-survey-wiki`, `ingest-source-code`, `prepare-code-run`, and `run-code-trial`
- **AND** each command page preserves its bounded recipe, owners, decisions, durable outputs, terminal states, and resume inputs

#### Scenario: Existing procedures remain callable
- **WHEN** compatibility procedures are inspected
- **THEN** the accepted landscape, intake, expansion, theory comparison, method trial, comparative, audit, paper, and template procedures remain public commands of the new entrypoint

#### Scenario: CRUD actions remain grouped by object
- **WHEN** manager actions are inspected
- **THEN** survey and dataset actions remain grouped under their accepted public manager commands

#### Scenario: Paper-template actions remain grouped by object
- **WHEN** the role-aware paper-template manager is migrated into the public pack
- **THEN** `manage-paper-template()` remains one parent command with declared children `list()`, `show()`, `create()`, `copy()`, `update()`, `replace()`, `merge()`, `file()`, `metadata()`, `export()`, `observe()`, `archive()`, `delete()`, and `migrate()`
- **AND** `file()` declares `put()` and `remove()` children while `metadata()` declares `patch()`
- **AND** internal routes may use complete chains such as `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->put()`

#### Scenario: Paper-template role remains command context
- **WHEN** a paper-template action selects content authoring or LaTeX presentation state
- **THEN** the manager resolves explicit `--kind content|latex` context before role-local discovery or mutation
- **AND** content and LaTeX do not become skills, subskills, or command-path components

#### Scenario: Compatibility template creation remains content-only
- **WHEN** the retained `create-paper-template` procedure is invoked
- **THEN** it creates or updates a named content template backed by `KAOJU:PAPER-TEMPLATE-MYST`
- **AND** LaTeX stock creation routes through `manage-paper-template()` with `--kind latex`

#### Scenario: Interaction and resume stay out of the procedure list
- **WHEN** a user requests clarification before work or resumes accepted prior state
- **THEN** clarification-first is represented as an interaction mode shared by procedures
- **AND** resume is represented by a Research Task, Run checkpoint, accepted input refs, and starting stage rather than a separate procedure

#### Scenario: Generic maintenance remains absent
- **WHEN** the public command list is inspected
- **THEN** it excludes standalone source-audit, repository-refresh, generic environment-repair, full-Kaoju, resume, and list-passes commands

#### Scenario: Empty invocation uses help
- **WHEN** the public entrypoint is invoked without a task or command
- **THEN** it executes help and reports the public command groups

### Requirement: Literature-First Landscape Survey
The `landscape-pass` procedure SHALL produce a bounded literature-first survey across papers, technical reports, source code repositories, datasets, and models.

#### Scenario: Broad field survey completes from versioned evidence
- **WHEN** a user requests a broad survey of a field, problem, technique, or representative seed
- **THEN** Kaoju records the survey boundary, date and coverage limits, query and inclusion evidence, version families, and material identities
- **AND** it produces a Related-Work Catalog and Field Summary whose statements cite accepted source evidence

#### Scenario: Linked artifacts remain type-aware
- **WHEN** repositories, datasets, models, or benchmarks are found during a landscape survey
- **THEN** papers and technical reports remain the primary related works
- **AND** the other source classes are linked as implementation or evidence artifacts when their relationships are supported

### Requirement: Curated Source Intake
The `curated-intake-pass` procedure SHALL give every user-nominated reference or codebase priority review without granting automatic authority or inclusion.

#### Scenario: Every nominated item is accounted for
- **WHEN** a user supplies a list of important references or codebases for an existing survey
- **THEN** each item receives a stable intake id, resolved or attempted Source Identity, a Source Digest or Source Access Blocker, and one terminal disposition
- **AND** duplicate, excluded, or blocked items retain explicit reasons

#### Scenario: Audited information updates the survey
- **WHEN** curated item evidence passes the intake audit
- **THEN** Kaoju applies a Curated Source Intake Delta to the applicable catalog, summary, ledger, chronology, taxonomy, limitations, artifact links, or reading path
- **AND** curated code is not executed unless a separate execution-oriented procedure is requested

### Requirement: Seed Direction Expansion
The `direction-expansion-pass` procedure SHALL expand a survey direction from named seed works through backward, neighboring, forward, and post-seed discovery routes.

#### Scenario: Expansion records route and time provenance
- **WHEN** a user asks for more work related to selected seed works
- **THEN** each candidate records its parent seed or query, discovery route, relevance rationale, inclusion decision, `latest_after`, and `searched_through`
- **AND** citation count, publication date, or provider rank alone does not determine inclusion

#### Scenario: Expansion produces a bounded delta
- **WHEN** important additions have been selected and audited
- **THEN** Kaoju produces a Related-Work Catalog Delta and updates affected survey views
- **AND** it states the remaining frontier and does not claim exhaustive coverage

### Requirement: Source-Grounded Theory Comparison
The `theory-comparison-pass` procedure SHALL compare named works using dimensions derived from the survey domain, selected works, and bounded reference discovery when needed.

#### Scenario: Theory matrix retains source depth
- **WHEN** Kaoju creates a Theory Comparison Artifact
- **THEN** every dimension has a definition, rationale, applicability rule, and source basis
- **AND** each comparison cell cites exact source evidence or records `not stated`, `not applicable`, `unclear`, or `disputed`
- **AND** source-only cells do not receive empirical `compared` verification depth

### Requirement: Paper Method Trial
The `method-trial-pass` compatibility procedure and `run-code-trial` survey intent SHALL support an intended-data trial route and an explicitly generated-data capability-probe route while keeping environment preparation separate.

#### Scenario: Trial requires prepared source and environment
- **WHEN** a user asks to run one paper method
- **THEN** Kaoju resolves the acquired source commit and accepted UC-09 environment and smoke result before planning execution
- **AND** missing prerequisites route to source acquisition or `prepare-code-run` without executing in an ambient environment

#### Scenario: Intended-data route preserves faithful and repaired evidence
- **WHEN** the user selects intended data and approves the trial plan
- **THEN** Kaoju pins the paper, code, data, model, evaluator, environment, wrapper, and execution contract before the claim-bearing Run
- **AND** an authorized repaired Run and patch remain separate from the upstream-faithful attempt and verdict

#### Scenario: Generated-data route is a capability probe
- **WHEN** the user requests generated data because the intended dataset is too large, restricted, costly, unavailable, or unnecessary for initial understanding
- **THEN** Kaoju records a Generated Dataset Artifact with generator, schema, size, seeds, assumptions, checks, and limitations
- **AND** resulting numbers are labeled `capability-probe` at no stronger than `executed` depth
- **AND** they are not presented as paper reproduction or benchmark evidence

#### Scenario: Trial waits for approval
- **WHEN** `kaoju:method-trial-plan` is ready
- **THEN** execution waits for the applicable human Gate decision
- **AND** plan revisions and rejected decisions remain durable

### Requirement: Empirical Method Comparison
The `comparative-pass` procedure SHALL require a reviewed Comparison Intent Document before preparing or running candidate methods.

#### Scenario: Intent checkpoint blocks expensive work
- **WHEN** a user asks to compare methods through actual Runs
- **THEN** Kaoju presents candidate identities, readiness, prior-evidence reuse, acquisition and environment needs, reproduction or reimplementation routes, metrics, fairness rules, resources, Gates, and unresolved decisions
- **AND** it asks whether the user wants to clarify for more detail or proceed
- **AND** candidate preparation and research Runs wait for a Proceed Decision

#### Scenario: Controlled results preserve comparability limits
- **WHEN** eligible candidates execute under the accepted Comparison Contract
- **THEN** every measurement links to its Run, inputs, environment, metric definition, quality checks, adaptations, and raw-output evidence
- **AND** the Comparison Matrix reports uncertainty or variability and uses `not-comparable` where normalization would change task or quality semantics

### Requirement: Topic Dataset Management
The `manage-dataset` helper SHALL maintain user-approved local dataset registrations through the Topic Dataset Manifest and Topic Workspace owner.

#### Scenario: Register creates manifest-backed managed link
- **WHEN** a user invokes `manage-dataset register` for an authorized external local dataset directory
- **THEN** Kaoju routes mutation to the Topic Workspace owner
- **AND** the result records a stable dataset id, name, description, source locator, managed-link locator, access and license posture, observed metadata, fingerprint or staleness policy, and provenance
- **AND** source data is not copied, moved, rewritten, or deleted

#### Scenario: Dataset actions share one manager
- **WHEN** a user lists, shows, refreshes, or removes a registered dataset
- **THEN** the action is selected through `manage-dataset <action>`
- **AND** removal affects only the managed link and registration state, never the external target

#### Scenario: Empirical procedures query registered data first
- **WHEN** a method trial or empirical comparison needs a dataset
- **THEN** Kaoju queries and validates the Topic Dataset Manifest before asking the user for data or proposing a download
- **AND** reuse depends on availability, fingerprint, access, task, schema, split, evaluator, and license compatibility

### Requirement: Clarification-First Interaction
Every Kaoju survey procedure SHALL honor an explicit clarification-first request before acquisition, mutation, or research Runs.

#### Scenario: Material ambiguity is presented as structured choice
- **WHEN** read-only inspection finds a material ambiguity after the user requested clarification first
- **THEN** Kaoju asks one A/B/C/D question with three concrete options, one free-form option, explanations, pros, cons, and exactly one suggested choice
- **AND** after the answer it asks whether the user wants to clarify more or proceed to execution

#### Scenario: No ambiguity still requires proceed choice
- **WHEN** no material ambiguity remains after read-only inspection
- **THEN** Kaoju reports that the request is ready
- **AND** it still asks whether the user wants to clarify more or proceed before starting the procedure

### Requirement: Survey Audit and Synthesis
The `audit-survey-pass` procedure SHALL audit accepted survey evidence before producing final survey conclusions.

#### Scenario: Audit diagnoses without silently repairing
- **WHEN** survey evidence is submitted for closeout
- **THEN** Kaoju checks coverage, identity, provenance, exact locators, evidence labels, source drift, patches, failed Runs, metric traceability, and comparison fairness
- **AND** it records gaps and bounded repair routes without inventing or rewriting evidence

#### Scenario: Synthesis uses accepted evidence only
- **WHEN** the audit reports readiness
- **THEN** Kaoju produces a Claim Status Table and Kaoju Dossier that preserve contradictions, failures, limitations, unresolved questions, and exact evidence refs
- **AND** synthesis does not create missing source or Run evidence

### Requirement: Kaoju Evidence and Terminal Contract
All Kaoju skills SHALL preserve the shared evidence dimensions and finish bounded work with explicit status and durable refs.

#### Scenario: Evidence dimensions remain separate
- **WHEN** Kaoju records a claim, source observation, Run, or comparison cell
- **THEN** verification depth, evidence verdict, Run purpose, execution fidelity, input basis, and source or Run locator are stored as separate applicable fields
- **AND** a later repaired, adapted, or stronger result does not overwrite earlier evidence meaning

#### Scenario: Provider output is not automatic evidence
- **WHEN** a literature, repository, model, dataset, or execution provider returns a result
- **THEN** Kaoju records the result and provenance according to its evidence-use intent
- **AND** it does not support a Research Claim until deliberately linked through an accepted Evidence Item

#### Scenario: Bounded procedure returns terminal status
- **WHEN** a procedure stops
- **THEN** its terminal report states `complete`, `paused`, or `blocked`
- **AND** it includes accepted output refs, stage outcomes, resource use, Gates, blockers, and a resume point when applicable
- **AND** it does not select another macro procedure autonomously

### Requirement: Kaoju Uses Existing Platform Owners
Kaoju skills SHALL use existing Isomer owner skills, Service Requests, and extension points for topology, environment, provider, execution, Gate, path, and recording behavior while keeping repository command selection and execution with the acting user or agent.

#### Scenario: Governed mutation routes to owner
- **WHEN** a Kaoju procedure needs Topic Workspace registration or projection, environment preparation, managed dataset links, credentials, private data, large downloads other than repository command execution, document builds, viewer launch, or accelerator execution
- **THEN** it routes the operation to the applicable project, workspace, service, provider-binding, execution-adapter, or Gate owner
- **AND** it records and consumes returned durable refs rather than bypassing the owner

#### Scenario: Environment preparation uses a Service Request
- **WHEN** UC-09 needs to inspect or mutate Pixi environment state
- **THEN** the Project Operator Session or Operator Agent opens a Service Request for the Service Team and relates it to the active Research Task and Run
- **AND** the Kaoju skill does not represent itself as the environment owner

#### Scenario: Generic maintenance is not promoted to a survey procedure
- **WHEN** repository refresh, generic environment repair, claim tracing, or resume is needed only as an implementation step
- **THEN** Kaoju performs an authorized repository command directly or routes another owned step inside the active survey procedure
- **AND** it does not create a new top-level survey procedure for the generic task

#### Scenario: Direct user intent remains public
- **WHEN** the actor explicitly requests source-code ingestion, code-run preparation, or a source-code trial as defined by UC-08, UC-09, or UC-10
- **THEN** the pipeline exposes the corresponding bounded intent while keeping repository execution external and routing other owned mutations to platform owners
- **AND** the public intent does not make the capability skill the owner of workspace topology, environment, or trial-execution infrastructure

#### Scenario: Repository acquisition stays outside platform execution owners
- **WHEN** a Kaoju procedure needs to clone, fetch, copy, check out, deepen, repair, or otherwise acquire repository content
- **THEN** the acting user or agent selects and executes the commands outside `isomer-cli`, Isomer services, Service Requests, and Execution Adapter Command Requests under the applicable Gate and authorization
- **AND** the procedure routes only target planning, post-verification semantic registration, Artifact recording, and provenance recording to Isomer owners

### Requirement: Survey-Process Procedures Use Durable Stage Checkpoints
Each new survey-process procedure SHALL create or resume a bounded Run and checkpoint every accepted durable stage.

#### Scenario: Procedure begins
- **WHEN** a new survey-process intent starts
- **THEN** the pipeline records its Research Task and Run refs, procedure id, actor and control mode, normalized inputs, expected output semantics, initial stage, and applicable Gate policies

#### Scenario: Procedure pauses or completes
- **WHEN** a stage reaches a human decision, blocker, Service Request, or terminal result
- **THEN** the pipeline records completed output refs, pending refs, status, and resume hint through Workspace Runtime
- **AND** it reports `complete`, `paused`, or `blocked` without autonomously selecting another macro procedure

### Requirement: Pipeline Skills Query Durable Inputs Through the State DB
All production Kaoju procedures SHALL discover accepted durable inputs through deterministic state-DB queries.

#### Scenario: Procedure resolves prior work
- **WHEN** a stage needs a direction set, reading list, source digest, artifact library, audit, synthesis, paper, wiki, repository, environment, or trial record
- **THEN** it queries by semantic id, scope key, status, stable ref, and lineage as applicable
- **AND** it does not scan the Topic Workspace directory tree or trust conversation memory as canonical state

### Requirement: Kaoju Survey Process Data Is Extension-Queried
Kaoju active guidance SHALL query the checked process contract through the package extension while resolving protected members through catalog metadata.

#### Scenario: Entrypoint loads checked contract
- **WHEN** `isomer-ext-kaoju-entrypoint` starts a routing task
- **THEN** it runs `isomer-cli --print-json ext kaoju process show`
- **AND** the response identifies the new public entry skill, public commands, protected logical ids, binding policy, manager-action hierarchy, independent content and LaTeX template roles, and current paper-template implementation decisions

#### Scenario: Entrypoint loads local command process
- **WHEN** a selected public command has a parent-owned procedure
- **THEN** it loads the corresponding command page from the public pack's `commands/` directory
- **AND** it does not duplicate that procedure in a protected member

### Requirement: Kaoju Cross-Skill Procedures Are Shared-Skill Owned
Kaoju guidance used across multiple protected stages SHALL remain owned by logical capability `isomer-kaoju-shared` and routed through the public parent.

#### Scenario: Stage needs common discipline
- **WHEN** a protected Kaoju member needs common evidence, source identity, lineage, context, Gate, owner-routing, Artifact recording, or terminal rules
- **THEN** it invokes `isomer-ext-kaoju-entrypoint->shared` or a declared shared subcommand
- **AND** it does not traverse into the shared member or duplicate the complete process

#### Scenario: Shared member is privately projected
- **WHEN** a Kaoju member is selected for bounded private projection
- **THEN** manifest dependency closure includes `isomer-kaoju-shared` when required

### Requirement: Kaoju Pipeline Supports Authorized Run-To Recovery
The public Kaoju entrypoint SHALL keep each survey command bounded while allowing authorized target-scoped chaining across protected members and public procedures.

#### Scenario: Target lacks accepted artifacts
- **WHEN** synthesis, drafting, PDF construction, comparison, or export lacks known producible artifacts
- **THEN** the operation reports paused status, exact missing semantic ids, producer routes, and resume point
- **AND** it offers inclusive run-to recovery

#### Scenario: Authorized run-to chains procedures
- **WHEN** the user authorizes a named target
- **THEN** the public entrypoint may call bounded public commands and protected member designators in prerequisite order
- **AND** each invoked capability preserves its own Gates and terminal contract

#### Scenario: Kaoju audit recommends repair
- **WHEN** an audit procedure remains non-repairing and returns defects with bounded producer or repair routes inside an authorized target closure
- **THEN** the controller invokes those repair owners as separate procedures
- **AND** it starts a fresh audit after repair before allowing synthesis or paper writing to consume the repaired evidence

#### Scenario: No run-to authorization exists
- **WHEN** a bounded procedure recommends another macro action without authorization
- **THEN** the public entrypoint reports the recommendation and stops

### Requirement: Kaoju Run-To Preserves Interaction and Gate Contracts
Kaoju run-to SHALL automate only routine in-scope prerequisite routing and preserve clarification, Proceed Decision, resource, publication, and human Gate contracts.

#### Scenario: Routine prerequisite is discovered
- **WHEN** a protected member or public procedure reports a routine producible prerequisite
- **THEN** the entrypoint may invoke its declared owner under active run-to authorization

#### Scenario: Protected boundary is reached
- **WHEN** continuation requires an unresolved choice, Gate, unauthorized resource, or no-progress repeat
- **THEN** the entrypoint pauses with the current durable state and precise resume guidance

### Requirement: Public Template Management Distinguishes Template Roles
The public Kaoju `manage-paper-template` command SHALL retain one grouped action surface while resolving content-template and LaTeX-template roles explicitly.

#### Scenario: Help is requested
- **WHEN** a user inspects `manage-paper-template` help
- **THEN** it explains content templates, LaTeX templates, their independent `main` defaults, and supported management actions
- **AND** it does not describe all paper templates as MyST-oriented trees

#### Scenario: Natural-language task is routed
- **WHEN** task language names MyST structure, content sections, LaTeX, TeX, a document class, a style, or a venue template
- **THEN** the entrypoint routes the task with the corresponding template role
- **AND** existing evidence, Gate, Run, and owner boundaries remain unchanged

### Requirement: Kaoju Entrypoint Explains Every Protected Route
The `isomer-ext-kaoju-entrypoint` skill SHALL provide one context-aware `When to Route Here` sentence for every protected Kaoju subskill in its protected-subskill table. Each sentence SHALL assume the Kaoju survey context and identify the evidence-stage condition, publication output, or bounded support need that selects the member.

#### Scenario: Kaoju protected inventory is inspected
- **WHEN** `isomer-ext-kaoju-entrypoint/SKILL.md` is inspected
- **THEN** all 13 protected-member rows contain one routing sentence
- **AND** the existing member names, logical ids, and internal designators remain unchanged

#### Scenario: Source-evidence routes overlap
- **WHEN** a task may require source discovery, acquisition, examination, comparison, or audit
- **THEN** the applicable routing sentences distinguish `discover`, `acquire`, `examine`, `compare`, and `audit` by evidence state and intended output

#### Scenario: Execution routes overlap
- **WHEN** a source-code task may be a bounded environment or method trial or a genuine reproduction claim
- **THEN** the routing sentences distinguish `trial` from `reproduce` by the requested fidelity and claim contract

#### Scenario: Closeout routes overlap
- **WHEN** accepted evidence may need synthesis, authored survey output, or export
- **THEN** the applicable routing sentences distinguish `synthesize`, `write`, and `export` by whether the task creates conclusions, prose, or a target projection

#### Scenario: Shared support is selected
- **WHEN** a Kaoju task needs cross-stage evidence, Gate, Artifact, lineage, or terminal-state rules rather than a standalone survey stage
- **THEN** the `shared` sentence identifies it as internal cross-stage support and does not present it as an independent public workflow

### Requirement: Kaoju Template Separation Survives Skill Regrouping
The Kaoju public pack and protected `write` member SHALL preserve the implemented separation between canonical content-template state and named LaTeX presentation stock while changing only skill packaging and routing identities.

#### Scenario: Role-aware process contract is rewritten
- **WHEN** regrouping updates the checked Kaoju survey-process resource
- **THEN** its public entry skill becomes `isomer-ext-kaoju-entrypoint` and its focused skills resolve through protected logical ids and parent-owned designators
- **AND** its manager actions, `template_roles`, independent `main` defaults, `KAOJU:PAPER-TEMPLATE-MYST`, `KAOJU:PAPER-TEMPLATE-LATEX`, preamble, marker, and include composition modes, derived snapshot identities, and drift policy remain intact

#### Scenario: Protected write bundle is moved
- **WHEN** `isomer-kaoju-write` becomes protected member `write`
- **THEN** it retains its private artifact-binding guidance and paper-contract, manuscript-structure, LaTeX-build, validation, and survey-quality references
- **AND** its content-template selection, LaTeX stock selection, exact snapshot composition, entrypoint-aware build, paper-local repair, and publication-lineage behavior remain effective

#### Scenario: Package-owned template services remain external to skill bundles
- **WHEN** the Kaoju skill pack is materialized or `write` is privately projected
- **THEN** template state, payload, support, validation, migration, composition, build, binding, semantic, and process services remain package-owned under `isomer_labs.kaoju`
- **AND** active skills query those services through `isomer-cli ext kaoju` without copying or traversing to their source files

#### Scenario: Existing Topic Workspace template state is encountered
- **WHEN** regrouped skills operate on a Topic Workspace already migrated to the content-template and LaTeX-template contract
- **THEN** they preserve its stable refs, state tokens, managed trees, exports, TeX snapshots, drafts, builds, PDFs, and historical source records
- **AND** skill installation, upgrade, or first invocation does not rerun template-contract migration or adopt another LaTeX source implicitly

### Requirement: Direct User Intent Remains Public
Accepted Kaoju survey intents SHALL remain public commands of `isomer-ext-kaoju-entrypoint` even when protected members perform their bounded stages.

#### Scenario: User requests source-code survey work
- **WHEN** the user explicitly requests source ingestion, code-run preparation, or a source-code trial
- **THEN** the public entrypoint exposes the corresponding accepted command
- **AND** it routes protected acquisition, examination, trial, service, or platform owners without changing their authority

#### Scenario: User requests a protected stage by task
- **WHEN** a concrete Kaoju task maps directly to audit, comparison, synthesis, writing, or export but omits a public subcommand
- **THEN** task-only entrypoint routing may select the applicable protected member
- **AND** the member remains absent from top-level host discovery

### Requirement: Kaoju Welcome Maps the Complete Public Command Inventory
The Kaoju welcome skill SHALL maintain a manifest-validated command map and curated use-case guide for the current Kaoju public entrypoint.

#### Scenario: Command map is validated
- **WHEN** Kaoju welcome validation runs
- **THEN** every current public survey-intent, compatibility-procedure, manager, and help command appears exactly once
- **AND** missing, duplicate, extra, or stale command ids fail validation

#### Scenario: Typical use cases are curated
- **WHEN** default Kaoju welcome output is inspected
- **THEN** it prioritizes landscape discovery, reading-list work, evidence intake, comparison, trials, paper production, and wiki export
- **AND** it does not dump the complete command inventory before offering those representative patterns

