## ADDED Requirements

### Requirement: Kaoju Exposes Its Own Topic-Creation Workflow
The public Kaoju entrypoint SHALL expose `create-topic` as an extension-specific topic-preparation command owned by `isomer-ext-kaoju-entrypoint->topic-creator`.

#### Scenario: User creates a Kaoju topic
- **WHEN** the user invokes `$isomer-ext-kaoju-entrypoint use create-topic to <task>` with concrete topic substance
- **THEN** the entrypoint routes generic Project and topic creation stages to `isomer-op-entrypoint->topic-create`, then routes derived mindset generation to `isomer-ext-kaoju-entrypoint->topic-creator`
- **AND** the terminal result distinguishes generic topic readiness from created, preserved, invalid, missing, or drifted Mindset Source files

#### Scenario: Existing topic needs Kaoju repair
- **WHEN** the selected Research Topic and `topic.intent.overview` already exist but one or more required Mindset Sources are missing
- **THEN** `create-topic` reuses the generic topic state and invokes create-missing derivation for the selected topic
- **AND** it does not rerun or claim ownership of ready generic lifecycle stages

#### Scenario: Create-topic appears in public help
- **WHEN** Kaoju welcome, command-map, entrypoint help, and checked command metadata are inspected
- **THEN** `create-topic` appears as a topic-preparation command distinct from the ten survey intents, retained compatibility procedures, exploration, and grouped managers
- **AND** it explains that direct generic Topic Creator use does not generate Kaoju derived intent

### Requirement: Kaoju Process Contract Declares Mindset Routes
The checked Kaoju survey-process contract SHALL expose deterministic mindset route metadata for applicable actions without embedding topic Source bodies or treating packaged defaults as runtime fallback.

#### Scenario: Entrypoint loads the checked contract
- **WHEN** `isomer-ext-kaoju-entrypoint` runs `isomer-cli --print-json ext kaoju process show`
- **THEN** the response includes mindset schema version, required action routes, applicability selectors, selected keys, Source semantic label `topic.intent.kaoju_mindsets`, Record semantic id `KAOJU:MINDSET-RECORD`, and the `topic-creator` repair designator
- **AND** it does not embed topic-owned questions, answers, a `KAOJU:MINDSET-SOURCE` id, or a package-default runtime fallback

#### Scenario: Process and seed inventories diverge
- **WHEN** package validation compares process routes, packaged seed keys, protected resource metadata, and Source validators
- **THEN** missing, extra, duplicated, unresolved, or inapplicable required seed keys fail validation
- **AND** the diagnostic names the route and affected key

### Requirement: Applicable Kaoju Workflows Enforce Mindset Injection
The public Kaoju entrypoint and every first-version consuming system-skill workflow SHALL ensure missing topic Mindset Sources before Run creation and SHALL treat the resulting Mindset Record ref as a mandatory Run input and closeout dependency rather than relying on the executing agent to discover or re-read a mutable Source independently.

#### Scenario: Concrete Kaoju action enters extension preflight
- **WHEN** one reconciled topic receives a concrete mutation-bearing Kaoju command whose checked route may require a mindset
- **THEN** the entrypoint runs `isomer-kaoju-topic-creator` create-missing preflight before beginning the research Run
- **AND** it preserves valid existing Sources, creates missing default-key Sources, and starts the Run only after the required topic Source validates

#### Scenario: Installed pack sees existing topics
- **WHEN** Kaoju installation or materialization completes while Research Topics already exist
- **THEN** no topic is scanned or mutated as part of installation
- **AND** the first concrete mutation-bearing Kaoju action initializes only its explicitly reconciled topic through the extension entrypoint

#### Scenario: Read-only public route enters preflight
- **WHEN** welcome, help, `explore`, or a status-only management route observes missing mindset state
- **THEN** it reports the state and the explicit or lazy preparation route without invoking create-missing
- **AND** the read-only route begins no research Run and writes no Source or Record

#### Scenario: Entrypoint begins an applicable procedure Run
- **WHEN** create-missing preflight has completed and the checked route requires a mindset
- **THEN** the entrypoint begins the selected Run, re-resolves and validates the exact topic Source, pins active survey context, snapshots the Source into a Mindset Record, and includes the Record ref in Run inputs and downstream handoffs before focused-owner dispatch
- **AND** it pauses without dispatch when final Source or survey-context state cannot be resolved

#### Scenario: Reading-item workflow selects an inspection depth
- **WHEN** `commands/ingest-reading-item.md` resolves a paper to skim or triage depth or to deep or full-text depth
- **THEN** it requires a Mindset Record materialized from `paper.skimming` or `paper.deep-dive` respectively and passes the Record ref to `isomer-kaoju-examine`
- **AND** absent or ambiguous depth pauses instead of selecting a key by guesswork

#### Scenario: Source-code workflow reaches examination
- **WHEN** `commands/ingest-source-code.md` is ready to dispatch repository or source-tree examination
- **THEN** it requires a Mindset Record materialized from `source-code.ingest` and passes that ref to `isomer-kaoju-examine`
- **AND** acquisition or registration evidence does not substitute for the Record

#### Scenario: Examine consumes a required mindset
- **WHEN** `isomer-kaoju-examine/SKILL-MAIN.md` receives an applicable paper, repository, or source-tree task
- **THEN** it requires and loads the handed-off Mindset Record snapshot, answers and checkpoints materialized Source questions during existing inspection stages, and captures supplemental questions only when the user explicitly targets the Record
- **AND** it pauses on a missing or mismatched Record instead of re-reading a changed Source file or proceeding from route metadata or conversation memory

#### Scenario: Ordinary follow-up question is asked
- **WHEN** the user asks a paper or source-code question without explicitly targeting a Mindset Source or Mindset Record
- **THEN** the applicable workflow saves the answer or unresolved posture in its existing reading Artifacts
- **AND** it does not infer Record association from timing, topic relevance, or the fact that a mindset is active

#### Scenario: Applicable Run reaches closeout
- **WHEN** the entrypoint attempts to mark an applicable examination Run complete or present its claim-bearing output for acceptance
- **THEN** it requires a terminal Mindset Record revision whose materialized Source and explicitly assigned supplemental rows have terminal answer states, whose collector is checked, and whose ref appears in the terminal report and applicable output lineage
- **AND** a paused or blocked Run preserves incomplete or unresolved Record rows while a missing or nonterminal Record prevents `complete`

### Requirement: Kaoju Workflow Authority Remains Separate from Mindsets
Kaoju procedures SHALL treat Mindset Source content and its materialized Record snapshot as reflective input while preserving existing Workflow Stage, evidence, Gate, execution, ownership, and terminal contracts.

#### Scenario: Mindset Record contains questions
- **WHEN** a protected member consumes a Mindset Record during a procedure
- **THEN** it answers materialized Source and explicitly assigned supplemental questions while performing the procedure's already authorized actions
- **AND** the questions do not add, remove, reorder, or authorize those actions

#### Scenario: Mindset content conflicts with procedure authority
- **WHEN** a snapshotted prompt or `additional_notes` requests behavior that conflicts with instructions, a procedure boundary, a Gate, or an authorization limit
- **THEN** the higher-authority contract prevails and the Mindset Record records the question as unresolved or inapplicable with rationale
- **AND** the agent does not execute the conflicting request

## MODIFIED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju pack with independent public welcome and execution entrypoint bundles plus the protected `isomer-kaoju-<purpose>` capabilities required by its checked command and process contracts.

#### Scenario: Kaoju public pair exists
- **WHEN** packaged Kaoju assets are inspected
- **THEN** sibling bundles `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint` contain valid public skill metadata
- **AND** the fifteen current Kaoju capabilities remain protected below the entrypoint

#### Scenario: Exact production inventory exists
- **WHEN** the packaged Kaoju root is inspected
- **THEN** it contains public directory `isomer-ext-kaoju-entrypoint`
- **AND** that pack contains protected bundles for `isomer-kaoju-shared`, `isomer-kaoju-workspace-mgr`, `isomer-kaoju-topic-creator`, `isomer-kaoju-frame`, `isomer-kaoju-discover`, `isomer-kaoju-acquire`, `isomer-kaoju-examine`, `isomer-kaoju-reproduce`, `isomer-kaoju-trial`, `isomer-kaoju-compare`, `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, `isomer-kaoju-write`, `isomer-kaoju-export`, and `isomer-kaoju-explore`
- **AND** no `isomer-kaoju-mindsets` manager, `isomer-kaoju-pipeline` folder, or duplicate public facade is active

#### Scenario: Topic creator is privately projected
- **WHEN** `isomer-kaoju-topic-creator` is selected for bounded private projection
- **THEN** its local generation guidance and default mindset JSON resources remain available inside the projected bundle
- **AND** it can delegate generic creation through the public operator entrypoint without copying the generic Topic Creator into its bundle

#### Scenario: Artifact identity is consistent
- **WHEN** a protected Kaoju member names durable mindset output
- **THEN** it uses exact registered id `KAOJU:MINDSET-RECORD`
- **AND** it does not assign an Artifact id to a Mindset Source file

#### Scenario: Kaoju welcome is self-contained
- **WHEN** `isomer-ext-kaoju-welcome` is copied or linked as part of the pack
- **THEN** it resolves its active typical-use-case and command-map resources without loading private files from the entrypoint or protected subskills
- **AND** it may reference public entrypoint invocation names without becoming an execution owner

#### Scenario: Shared machine contracts remain package-owned
- **WHEN** welcome or entrypoint needs current Kaoju command or process metadata
- **THEN** checked machine contracts remain owned by the installed Kaoju Python package and manifest
- **AND** welcome does not introduce a second survey-process registry

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

### Requirement: Kaoju Pipeline Command Surface
`isomer-ext-kaoju-entrypoint` SHALL remain the single Kaoju execution entrypoint and SHALL expose checked survey, topic-preparation, exploration, compatibility, and grouped-management commands without promoting protected members as public skills.

#### Scenario: Kaoju topic preparation is requested
- **WHEN** a user asks to create or prepare a topic specifically for Kaoju
- **THEN** the entrypoint selects public command `create-topic` and routes its stages to the generic Topic Creator and protected Kaoju topic-creation owner
- **AND** it does not reinterpret `create-topic` as a survey intent or generic manager action

#### Scenario: Survey-process commands match ten use cases
- **WHEN** the checked public command inventory is inspected
- **THEN** the ten existing survey-process commands remain unchanged and `create-topic` is classified separately as topic preparation
- **AND** no specialized mindset-management command group is added

#### Scenario: Concrete Kaoju task uses entrypoint
- **WHEN** a user requests reading-list work, source ingestion, direction selection, comparison, code preparation, trial execution, paper production, wiki export, or task planning
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

#### Scenario: Exploration procedure is public
- **WHEN** public help or the command map is inspected
- **THEN** it exposes `explore` as an exploration procedure
- **AND** `explore` routes to the protected `isomer-kaoju-explore` member
- **AND** the `explore` command page delegates interactive planning to that member and routes to the selected command after consent

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
- **THEN** it executes help and reports the public command groups including survey intents, compatibility procedures, exploration procedures, and grouped managers

### Requirement: Kaoju Entrypoint Explains Every Protected Route
The `isomer-ext-kaoju-entrypoint` skill SHALL provide one context-aware `When to Route Here` sentence for every protected Kaoju subskill in its protected-subskill table.

#### Scenario: Kaoju protected inventory is inspected
- **WHEN** `isomer-ext-kaoju-entrypoint/SKILL.md` is inspected
- **THEN** all 15 protected-member rows contain one routing sentence
- **AND** `topic-creator` uses logical id `isomer-kaoju-topic-creator` and designator `isomer-ext-kaoju-entrypoint->topic-creator`, while existing member names and designators remain unchanged

#### Scenario: Topic creation and framing overlap
- **WHEN** a task has a Research Topic but lacks derived Kaoju Mindset Sources, Direction Set, or Survey Contract
- **THEN** `topic-creator` owns missing derived intent while `frame` owns survey directions, boundary, evidence depth, and Survey Contract after topic preparation
- **AND** neither owner writes the other's state

#### Scenario: Explore and topic creation overlap
- **WHEN** a user needs read-only planning for an unprepared Kaoju topic
- **THEN** `explore` may diagnose and recommend `create-topic`, while `topic-creator` owns authorized generic delegation and Mindset Source writes
- **AND** `explore` does not mutate the derived-intent root

#### Scenario: Shared support is selected
- **WHEN** a Kaoju task needs cross-stage evidence, Gate, Artifact, lineage, or terminal-state rules rather than topic creation or a standalone survey stage
- **THEN** the `shared` sentence identifies it as internal cross-stage support and does not present it as an independent public workflow

#### Scenario: Source-evidence routes overlap
- **WHEN** a task may require source discovery, acquisition, examination, comparison, or audit
- **THEN** the applicable routing sentences distinguish `discover`, `acquire`, `examine`, `compare`, and `audit` by evidence state and intended output

#### Scenario: Execution routes overlap
- **WHEN** a source-code task may be a bounded environment or method trial or a genuine reproduction claim
- **THEN** the routing sentences distinguish `trial` from `reproduce` by the requested fidelity and claim contract

#### Scenario: Closeout routes overlap
- **WHEN** accepted evidence may need synthesis, authored survey output, or export
- **THEN** the applicable routing sentences distinguish `synthesize`, `write`, and `export` by whether the task creates conclusions, prose, or a target projection

### Requirement: Kaoju Welcome Maps the Complete Public Command Inventory
The Kaoju welcome skill SHALL teach every checked public Kaoju command and SHALL keep protected implementation members out of the public command map.

#### Scenario: Command map is validated
- **WHEN** welcome resources are compared with checked public command metadata
- **THEN** `create-topic` appears once with a Kaoju topic-preparation description and exact public invocation shape
- **AND** neither `topic-creator` nor a mindset manager appears as an independently invocable public skill

#### Scenario: Typical use cases are curated
- **WHEN** default Kaoju welcome output is inspected
- **THEN** it prioritizes landscape discovery, reading-list work, evidence intake, comparison, trials, paper production, and wiki export
- **AND** it does not dump the complete command inventory before offering those representative patterns
