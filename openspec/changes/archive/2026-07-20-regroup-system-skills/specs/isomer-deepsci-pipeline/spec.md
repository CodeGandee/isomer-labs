## MODIFIED Requirements

### Requirement: Pipeline skill exists
The project SHALL provide the production DeepSci pipeline as public pack `isomer-ext-deepsci-entrypoint` under `research-paradigm/deepsci/isomer-ext-deepsci-entrypoint/`.

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
The public DeepSci entrypoint SHALL define each accepted pass as a dedicated command page and SHALL route recipe stages through declared protected member designators.

#### Scenario: Pass page is inspected
- **WHEN** a page under `isomer-ext-deepsci-entrypoint/commands/` is read
- **THEN** it contains the existing recipe fields for stage order, consumed artifacts, produced artifacts, continue condition, pause condition, and expensive posture
- **AND** each stage maps a protected logical id to an invocation designator such as `isomer-ext-deepsci-entrypoint->experiment`

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

### Requirement: Initial pipeline catalog
The public DeepSci entrypoint SHALL retain the accepted single-pass catalog for empirical research, paper work, review, rebuttal, and publication packaging.

#### Scenario: Catalog is inspected
- **WHEN** `isomer-ext-deepsci-entrypoint/commands/` is listed
- **THEN** it contains `empirical-pass.md`, `hypothesis-pass.md`, `paper-pass.md`, `revision-pass.md`, `rebuttal-pass.md`, `polish-pass.md`, `submission-pass.md`, and `list-passes.md`

#### Scenario: Empty invocation uses help
- **WHEN** the public entrypoint is invoked without a task or command
- **THEN** it runs `help` and lists the accepted public pass commands

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
