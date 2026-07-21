# isomer-deepsci-pipeline Specification

## Purpose

Define the `isomer-deepsci-pipeline` production DeepSci skill, which executes named single-pass recipes that chain other production DeepSci skills with automatic artifact handoffs while preserving each wrapped skill's gate discipline.
## Requirements
### Requirement: Pipeline skill exists
The project SHALL provide `isomer-ext-deepsci-entrypoint` as the DeepSci execution entrypoint and `isomer-ext-deepsci-welcome` as its independent public newcomer skill.

#### Scenario: DeepSci public pair is packaged
- **WHEN** the production DeepSci pack is inspected
- **THEN** it contains sibling public bundles `isomer-ext-deepsci-welcome` and `isomer-ext-deepsci-entrypoint`
- **AND** all existing DeepSci stage capabilities remain protected below the entrypoint

#### Scenario: DeepSci public roles are distinct
- **WHEN** DeepSci metadata is inspected
- **THEN** welcome describes typical production-research patterns and performs no research task mutation
- **AND** entrypoint executes named pass commands or routes concrete tasks through protected DeepSci stages

#### Scenario: Historical pipeline identity is used
- **WHEN** compatibility lookup encounters `isomer-deepsci-pipeline`
- **THEN** it resolves to the execution entrypoint rather than the welcome skill
- **AND** guidance recommends the welcome skill only for onboarding or command-learning intent

#### Scenario: Public entrypoint folder is present
- **WHEN** the production DeepSci package is inspected
- **THEN** it contains `isomer-ext-deepsci-entrypoint/SKILL.md` with matching frontmatter and `agents/openai.yaml`
- **AND** it does not contain a top-level or nested `isomer-deepsci-pipeline` skill folder

#### Scenario: Old pipeline id is resolved
- **WHEN** catalog compatibility lookup receives `isomer-deepsci-pipeline`
- **THEN** it resolves to `isomer-ext-deepsci-entrypoint`
- **AND** it reports the old id as deprecated without a shim directory

#### Scenario: DeepSci protected inventory exists
- **WHEN** the public pack's `subskills/` tree is inspected
- **THEN** it contains protected logical capabilities for analysis, baseline, decision, experiment, figure polish, finalize, idea, Nature data, Nature figure, Nature paper-to-PPT, Nature polishing, optimize, paper outline, paper plot, rebuttal, review, science, scout, shared, workspace management, and write
- **AND** each capability retains its `isomer-deepsci-*` folder and frontmatter identity
### Requirement: Pipeline passes are self-contained subcommand pages
The DeepSci execution entrypoint SHALL retain self-contained pass command pages, while the independent DeepSci welcome skill SHALL own only newcomer use-case and command-learning resources.

#### Scenario: Pass page is inspected
- **WHEN** an active DeepSci pass command is inspected
- **THEN** its execution stages, handoffs, Gates, callbacks, and terminal contract remain owned by `isomer-ext-deepsci-entrypoint`
- **AND** the welcome skill links to the public command without copying the pass procedure

#### Scenario: Welcome example references a pass
- **WHEN** DeepSci welcome teaches a hypothesis, empirical, paper, revision, rebuttal, or polish pattern
- **THEN** it provides an exact `$isomer-ext-deepsci-entrypoint use <pass> to <task>` example
- **AND** it explains prerequisites and mutation posture without executing the pass

#### Scenario: Pass recipe is valid
- **WHEN** the entrypoint validates a recipe
- **THEN** every stage resolves to one manifest-declared protected DeepSci member
- **AND** every artifact id remains valid under the production semantic-placeholder and binding contracts
- **AND** the first stage's consumed artifacts are empty or satisfied by accepted context

#### Scenario: Object notation is declared
- **WHEN** a pass page uses protected invocation designators
- **THEN** its frontmatter declares the standard `skill_invocation_notation` value
### Requirement: Skill executes stages in order
When invoked with a public pass command, `isomer-ext-deepsci-entrypoint` SHALL run the pass's protected stages sequentially.

#### Scenario: Public pass invocation executes
- **WHEN** the user invokes `$isomer-ext-deepsci-entrypoint use empirical-pass to <task>` with valid context
- **THEN** the entrypoint runs the first declared protected stage and advances until completion or a pause condition

#### Scenario: Task-only invocation selects a stage or pass
- **WHEN** a concrete DeepSci task omits a public subcommand
- **THEN** the entrypoint selects the matching pass or protected member and proceeds

#### Scenario: Stage failure blocks progression
- **WHEN** a protected stage emits a blocker record
- **THEN** the entrypoint does not start the next stage
- **AND** it produces a blocked terminal report

### Requirement: Skill passes artifacts between stages automatically

The skill SHALL make each stage's produced artifacts available as input context to the next stage without requiring the user to restate them.

#### Scenario: Artifact handoff

- **WHEN** stage N produces an artifact listed in the next stage's consumed artifacts
- **THEN** stage N+1 receives that artifact as part of its invocation context
- **AND** stage N+1 does not prompt the user to re-supply the artifact

### Requirement: Skill pauses on deviation or blocker

The skill SHALL stop execution and produce a paused terminal report when a stage's output indicates a route the recipe cannot satisfy or when a blocker is recorded.

#### Scenario: Unexpected route decision

- **WHEN** a stage completes with a route decision that does not match the recipe's continue condition
- **THEN** the skill records `status: paused`
- **AND** the terminal report includes the stage id, the unexpected route, and the produced artifacts

#### Scenario: Blocker recorded

- **WHEN** a stage produces a blocker record
- **THEN** the skill records `status: blocked`
- **AND** the terminal report includes the blocker record and a resume point pointing to the failed stage

### Requirement: Skill produces a terminal report

At the end of a pipeline run, the skill SHALL produce a `pipeline-terminal-report` that summarizes status, stages, artifacts, and the last stage's recommended next action.

#### Scenario: Successful completion

- **WHEN** all stages complete without pausing or blocking
- **THEN** the terminal report contains `status: complete`, a list of completed stages, the final artifact, and a `recommended_next` value derived from the last stage's route decision

#### Scenario: Paused or blocked completion

- **WHEN** execution stops early
- **THEN** the terminal report contains `status: paused` or `status: blocked`, the completed stages, the current stage, the reason for stopping, and a `resume_point`

### Requirement: Initial pipeline catalog
The DeepSci pack SHALL preserve its accepted execution-pass catalog and expose complete newcomer mapping for that catalog through the independent welcome skill.

#### Scenario: Execution pass catalog is inspected
- **WHEN** `isomer-ext-deepsci-entrypoint` public commands are read from the manifest
- **THEN** they include the accepted empirical, hypothesis, paper, polish, rebuttal, revision, submission, list, and help commands in deterministic order
- **AND** protected stage ownership remains unchanged

#### Scenario: Welcome command map is inspected
- **WHEN** `isomer-ext-deepsci-welcome` command-map guidance is validated
- **THEN** every manifest-declared DeepSci entrypoint command appears exactly once with a one-sentence use condition and exact invocation
- **AND** no protected DeepSci logical id is advertised as a direct public skill

#### Scenario: Catalog is inspected
- **WHEN** `isomer-ext-deepsci-entrypoint/commands/` is listed
- **THEN** it contains `empirical-pass.md`, `hypothesis-pass.md`, `paper-pass.md`, `revision-pass.md`, `rebuttal-pass.md`, `polish-pass.md`, `submission-pass.md`, and `list-passes.md`

#### Scenario: Recipe stages are bounded
- **WHEN** a shipped recipe is inspected
- **THEN** it contains no backward edges or internal macro loops
- **AND** it names only declared protected DeepSci logical capabilities as stages
### Requirement: DeepSci Pipeline Supports Authorized Run-To Control
The public DeepSci entrypoint SHALL preserve linear pass recipes while allowing target-scoped run-to control across protected members after explicit authorization.

#### Scenario: DeepSci target lacks a producible input
- **WHEN** a selected pass or protected target lacks an input that a known owner can produce
- **THEN** the current operation records paused status, missing accepted ref, producer route, and resume point
- **AND** it offers run-to recovery

#### Scenario: Run-to controller consumes terminal report
- **WHEN** authorized continuation selects another DeepSci member or pass
- **THEN** the parent invokes the catalog-declared protected designator and refreshes current accepted context before advancing
- **AND** the individual pass remains linear

#### Scenario: DeepSci target becomes ready
- **WHEN** every accepted prerequisite exists
- **THEN** the entrypoint resumes and executes the original target
- **AND** it stops after that target's acceptance conditions are met

#### Scenario: No run-to authorization exists
- **WHEN** a terminal report recommends another macro action without active authorization
- **THEN** the entrypoint reports the recommendation to the user
- **AND** it does not select the action autonomously

### Requirement: DeepSci Run-To Preserves Wrapped Skill Boundaries
DeepSci run-to control SHALL preserve each protected member's callbacks, preflight, output policy, bindings, quality gates, resource checks, and blocker semantics.

#### Scenario: Controller invokes another protected member
- **WHEN** run-to requires a focused DeepSci capability
- **THEN** the parent routes through that member's invocation designator and accepted inputs
- **AND** callback resolution uses the member's preserved logical id

#### Scenario: Protected or repeating route is reached
- **WHEN** continuation reaches a nondelegable Gate, material research choice, unauthorized resource change, or no-progress repeat
- **THEN** control pauses with completed artifacts and a precise resume point

### Requirement: DeepSci Pipeline Requires Accepted Stage Outputs
`isomer-deepsci-pipeline` SHALL advance between stages using verified durable record refs and operation-set closeout status rather than plain file paths.

#### Scenario: Stage with files hands off a complete receipt
- **WHEN** a pipeline stage produces material operation-set files and otherwise satisfies its continue condition
- **THEN** the pipeline verifies that stage's complete acceptance receipt and passes the resulting durable record refs to the next stage

#### Scenario: Stage without files declares closeout not applicable
- **WHEN** a stage opens no operation set and produces or consumes only durable records
- **THEN** the stage handoff records `closeout: not_applicable` with those durable refs and may continue

#### Scenario: Partial acceptance stops progression
- **WHEN** a stage has a missing, partial, stale, or unverifiable acceptance receipt
- **THEN** the pipeline does not start the next stage and emits a paused terminal report with the stage id and receipt recovery action

#### Scenario: File path is not an artifact handoff
- **WHEN** a stage reports only a worker output path or terminal prose for a produced artifact
- **THEN** the pipeline treats the artifact as unavailable until a durable record ref is accepted and verified

### Requirement: Pipeline Completion Reports Acceptance Evidence
The DeepSci pipeline SHALL include operation-set closeout evidence in its terminal report and SHALL reconcile any pipeline-level material files before reporting `status: complete`.

#### Scenario: Successful terminal report lists receipts
- **WHEN** every stage and the pipeline itself complete successfully
- **THEN** the terminal report lists each applicable acceptance receipt id, accepted durable record refs, any `not_applicable` closeouts, the final artifact ref, and the recommended next action

#### Scenario: Pipeline-level report file is reconciled
- **WHEN** the controller writes a pipeline-level report or other material file into its own operation set
- **THEN** it accepts and verifies that set before the terminal status becomes `complete`

#### Scenario: Terminal acceptance failure pauses pipeline
- **WHEN** pipeline-level closeout cannot complete after all research stages ran
- **THEN** the terminal report uses `status: paused`, preserves completed stage refs, and provides the acceptance resume point

### Requirement: DeepSci Entrypoint Explains Every Protected Route
The `isomer-ext-deepsci-entrypoint` skill SHALL provide one context-aware `When to Route Here` sentence for every protected DeepSci subskill in its protected-subskill table. Each sentence SHALL assume the DeepSci pack context and identify the research-stage condition or bounded support need that selects the member.

#### Scenario: DeepSci protected inventory is inspected
- **WHEN** `isomer-ext-deepsci-entrypoint/SKILL.md` is inspected
- **THEN** all 21 protected-member rows contain one routing sentence
- **AND** the existing member names, logical ids, and internal designators remain unchanged

#### Scenario: Early research routes overlap
- **WHEN** a task may require framing, comparator establishment, hypothesis development, optimization, or a bounded experiment
- **THEN** the applicable routing sentences distinguish `scout`, `baseline`, `idea`, `optimize`, and `experiment` by readiness and intended output

#### Scenario: Publication routes overlap
- **WHEN** a task may require paper planning, plotting, visual refinement, Nature-specific data or figure work, review, rebuttal, finalization, or prose polishing
- **THEN** the applicable routing sentences distinguish the protected publication members by artifact state and requested transformation

#### Scenario: Shared support is selected
- **WHEN** a DeepSci task needs cross-stage context, output, lineage, evidence, or recording rules rather than a standalone research stage
- **THEN** the `shared` sentence identifies it as internal cross-stage support and does not present it as an independent public workflow

