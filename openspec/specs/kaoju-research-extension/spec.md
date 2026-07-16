# kaoju-research-extension Specification

## Purpose
TBD - created by archiving change implement-kaoju-research-extension. Update Purpose after archive.
## Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju research-paradigm skill family under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/` using the `isomer-kaoju-<purpose>` namespace and the skill/shared-resource contract.

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains `isomer-kaoju-pipeline`, `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, and `isomer-kaoju-export`
- **AND** no retired, version-suffixed, generic `isomer-ext-*`, or duplicate survey-facade Kaoju skill is active

#### Scenario: Skill identity is consistent
- **WHEN** a production Kaoju skill is inspected
- **THEN** its folder name, `SKILL.md` frontmatter name, `agents/openai.yaml` display name, and default-prompt invocation use the same `isomer-kaoju-*` name
- **AND** its active instructions and directly linked resources are self-contained within the skill directory

#### Scenario: Trial and reproduction remain distinct
- **WHEN** the production inventory is inspected for executable evidence work
- **THEN** `isomer-kaoju-trial` owns bounded method trials and generated-data capability probes while `isomer-kaoju-reproduce` owns only work that satisfies the stronger reproduction contract
- **AND** neither skill treats a repaired or capability-probe result as faithful paper reproduction

#### Scenario: Skill identity and resource boundary are consistent
- **WHEN** a production Kaoju skill is inspected
- **THEN** its folder name, `SKILL.md` frontmatter name, `agents/openai.yaml` display name, and default-prompt invocation use the same `isomer-kaoju-*` name
- **AND** every active filesystem-linked resource resolves within that skill directory, shared machine data is queried through `isomer-cli ext kaoju`, and shared procedures are routed through `isomer-kaoju-shared`

#### Scenario: Artifact identity is consistent
- **WHEN** a production Kaoju skill names, resolves, produces, consumes, or queries a durable extension artifact
- **THEN** it uses the exact registered `KAOJU:WHAT` identifier in prose, local projections, source declarations, and commands
- **AND** it does not use an angle-wrapped token, a bare object name, lowercase or mixed case, or an artifact alias

### Requirement: Kaoju Pipeline Command Surface
`isomer-kaoju-pipeline` SHALL use the complex-procedure shape as the single extension entry skill, with separate helper, survey-intent, legacy-procedure, and miscellaneous command groups.

#### Scenario: Survey-process commands match the ten use cases
- **WHEN** the pipeline command inventory is inspected
- **THEN** it exposes `choose-directions`, `build-reading-list`, `ingest-reading-item`, `draft-paper`, `manage-paper-template`, `build-paper-pdf`, `export-survey-wiki`, `ingest-source-code`, `prepare-code-run`, and `run-code-trial`
- **AND** each command links to one local command page containing its bounded stage recipe, owners, decisions, durable outputs, terminal states, and resume inputs

#### Scenario: Existing procedures remain callable
- **WHEN** the pipeline compatibility inventory is inspected
- **THEN** it retains `landscape-pass`, `curated-intake-pass`, `direction-expansion-pass`, `theory-comparison-pass`, `method-trial-pass`, `comparative-pass`, `audit-survey-pass`, `paper-pass`, and `create-paper-template`
- **AND** compatibility pages state how each procedure maps to current capability owners and canonical artifacts

#### Scenario: CRUD actions are grouped by object
- **WHEN** helper commands are inspected
- **THEN** `manage-survey` groups `list`, `show`, `status`, and `export`
- **AND** `manage-dataset` groups `register`, `list`, `show`, `refresh`, and `remove`
- **AND** `manage-paper-template` groups template `export`, `apply`, `inspect`, and `status` actions rather than exposing unrelated generic CRUD verbs

#### Scenario: Interaction and resume stay out of the procedure list
- **WHEN** a user requests clarification before work or resumes accepted prior state
- **THEN** clarification-first is represented as an interaction mode shared by procedures
- **AND** resume is represented by a Research Task, Run checkpoint, accepted input refs, and starting stage rather than a separate procedure

#### Scenario: Generic maintenance procedures are absent
- **WHEN** the pipeline public procedure list is inspected
- **THEN** it does not include standalone source-audit, repository-refresh, generic environment-repair, full-Kaoju, resume, or list-passes procedures
- **AND** `prepare-code-run` remains a specific UC-09 survey intent rather than a generic environment administration command

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
Kaoju active guidance SHALL obtain the checked survey-process inventory through the package-owned Kaoju extension query instead of a family-root contract file.

#### Scenario: Pipeline loads its checked contract
- **WHEN** `isomer-kaoju-pipeline` starts a Kaoju routing task
- **THEN** it runs `isomer-cli --print-json ext kaoju process show` and treats the returned version, entry skill, skill inventory, survey intents, compatibility procedures, manager actions, aliases, and policy decisions as the checked machine contract
- **AND** it does not open `../contracts`, an absolute checkout path, or another skill's resources

#### Scenario: Pipeline loads a command process
- **WHEN** the selected survey intent, compatibility procedure, or grouped manager action has a procedure used only by the pipeline
- **THEN** the pipeline loads the corresponding command page from its own `commands/` directory
- **AND** the machine contract identifies the command without becoming a duplicate prose procedure

### Requirement: Kaoju Cross-Skill Procedures Are Shared-Skill Owned
Kaoju guidance used across multiple stages SHALL remain in `isomer-kaoju-shared` and SHALL be consumed through skill routing rather than sibling filesystem references.

#### Scenario: Stage needs common Kaoju discipline
- **WHEN** a stage needs common evidence semantics, source identity, lineage, latest-context, Gate, owner-routing, Artifact recording, or terminal-state procedure
- **THEN** it invokes or follows `isomer-kaoju-shared` and loads only its own bundle-local stage guidance
- **AND** it does not copy the complete shared command process or traverse into the shared skill directory

### Requirement: Kaoju Pipeline Supports Authorized Run-To Recovery
The Kaoju pipeline SHALL keep each survey intent and compatibility procedure bounded while allowing a prompt-level controller to chain their producer and repair routes after explicit run-to authorization for a named target.

#### Scenario: Kaoju target lacks accepted artifacts
- **WHEN** a Kaoju target such as synthesis, drafting, PDF construction, comparison, or export lacks accepted prerequisite artifacts
- **AND** the required artifacts have known Kaoju or platform owner routes
- **THEN** the Kaoju pipeline's numbered workflow makes the bounded target report `paused` with exact missing semantic ids, producer routes, and resume point
- **AND** the user is offered inclusive run-to recovery before those producer routes execute

#### Scenario: Authorized Kaoju run-to chains bounded procedures
- **WHEN** the user authorizes run-to for a Kaoju target
- **THEN** the controller uses separate bounded Kaoju procedures to produce or repair the required inputs in dependency order
- **AND** it consumes each procedure's terminal report and accepted refs before selecting the next planned procedure or resuming the target
- **AND** every procedure retains its own Run, audit boundary, evidence semantics, and terminal report

#### Scenario: Kaoju audit recommends repair
- **WHEN** an audit procedure remains non-repairing and returns defects with bounded producer or repair routes inside an authorized target closure
- **THEN** the controller invokes those repair owners as separate procedures
- **AND** it starts a fresh audit after repair before allowing synthesis or paper writing to consume the repaired evidence

#### Scenario: Kaoju has no run-to authorization
- **WHEN** a bounded Kaoju procedure returns a terminal report without an active target-scoped run-to grant
- **THEN** the pipeline does not select another macro procedure autonomously
- **AND** it returns the recommended next procedure to the user as before

### Requirement: Kaoju Run-To Preserves Interaction and Gate Contracts
Kaoju run-to traversal SHALL automate only routine in-scope prerequisite routing and SHALL preserve every applicable clarification, Proceed Decision, resource, publication, and human Gate contract.

#### Scenario: Routine transitive prerequisite is discovered
- **WHEN** a Kaoju prerequisite procedure discovers another routine in-scope input needed for the same target
- **THEN** the controller adds the known producer route to the active plan without another routine confirmation
- **AND** the producer still resolves durable state through the state DB and writes through its typed Artifact bindings

#### Scenario: Kaoju traversal reaches a protected boundary
- **WHEN** the next stage requires a nondelegable Gate or a material choice that changes survey direction, evidence meaning, resource posture, or publication state
- **THEN** the controller checkpoints the active procedures and pauses
- **AND** it asks only for the decision needed to resume the named target
