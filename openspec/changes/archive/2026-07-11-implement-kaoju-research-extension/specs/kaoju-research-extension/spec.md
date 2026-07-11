## ADDED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju research-paradigm skill family under `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/` using the `isomer-kaoju-<purpose>` namespace.

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains `isomer-kaoju-pipeline`, `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, and `isomer-kaoju-synthesize`
- **AND** no retired, version-suffixed, or generic `isomer-ext-*` Kaoju skill is active

#### Scenario: Skill identity is consistent
- **WHEN** a production Kaoju skill is inspected
- **THEN** its folder name, `SKILL.md` frontmatter name, `agents/openai.yaml` display name, and default-prompt invocation use the same `isomer-kaoju-*` name
- **AND** its active instructions and directly linked resources are self-contained within the skill directory

### Requirement: Kaoju Pipeline Command Surface
`isomer-kaoju-pipeline` SHALL use the complex-procedure shape with separate helper, procedural, and miscellaneous command groups.

#### Scenario: Procedural commands match survey use cases
- **WHEN** the pipeline command inventory is inspected
- **THEN** it exposes `landscape-pass`, `curated-intake-pass`, `direction-expansion-pass`, `theory-comparison-pass`, `method-trial-pass`, `comparative-pass`, and `audit-survey-pass`
- **AND** each procedure links to one local command page containing its bounded stage recipe and terminal outputs

#### Scenario: CRUD actions are grouped by object
- **WHEN** helper commands are inspected
- **THEN** `manage-survey` groups `list`, `show`, `status`, and `export`
- **AND** `manage-dataset` groups `register`, `list`, `show`, `refresh`, and `remove`
- **AND** the pipeline does not expose one public subcommand for each CRUD verb

#### Scenario: Interaction and resume stay out of the procedure list
- **WHEN** a user requests clarification before work or resumes accepted prior state
- **THEN** clarification-first is represented as an interaction mode shared by procedures
- **AND** resume is represented by accepted input refs and a starting stage rather than a separate procedure

#### Scenario: Generic maintenance procedures are absent
- **WHEN** the pipeline public procedure list is inspected
- **THEN** it does not include standalone source-audit, reproduction, repository-refresh, environment-repair, full-Kaoju, or list-passes procedures

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
The `method-trial-pass` procedure SHALL support both an intended-data reproduction route and an explicitly generated-data capability-probe route for one paper method.

#### Scenario: Intended-data route preserves faithful and repaired evidence
- **WHEN** a user asks to obtain and run a paper method on its intended data
- **THEN** Kaoju pins the paper, code, data, model, evaluator, environment, and execution contract before the claim-bearing Run
- **AND** an authorized repaired Run and patch remain separate from the upstream-faithful attempt and verdict

#### Scenario: Generated-data route is a capability probe
- **WHEN** the user requests generated data because the intended dataset is too large, restricted, costly, or unnecessary for initial understanding
- **THEN** Kaoju records a Generated Dataset Artifact with generator, schema, size, seeds, assumptions, checks, and limitations
- **AND** resulting numbers are labeled `capability-probe` at no stronger than `executed` depth
- **AND** they are not presented as paper reproduction or benchmark evidence

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
Kaoju skills SHALL use existing Isomer owner skills and extension points for topology, environment, provider, execution, Gate, and recording behavior.

#### Scenario: Governed mutation routes to owner
- **WHEN** a Kaoju procedure needs repository registration, Topic Workspace mutation, environment preparation, managed dataset links, credentials, private data, large downloads, builds, or accelerator execution
- **THEN** it routes the operation to the applicable operator, service, provider-binding, execution-adapter, or Gate owner
- **AND** it records and consumes returned durable refs rather than bypassing the owner

#### Scenario: Generic maintenance is not promoted to survey procedure
- **WHEN** repository refresh, environment repair, claim tracing, or resume is needed only as an implementation step
- **THEN** Kaoju performs or routes that step inside the active survey procedure
- **AND** it does not create a new top-level survey procedure for the generic task
