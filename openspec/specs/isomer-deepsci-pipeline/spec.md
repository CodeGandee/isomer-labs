# isomer-deepsci-pipeline Specification

## Purpose

Define the `isomer-deepsci-pipeline` production DeepSci skill, which executes named single-pass recipes that chain other production DeepSci skills with automatic artifact handoffs while preserving each wrapped skill's gate discipline.

## Requirements

### Requirement: Pipeline skill exists

The project SHALL provide a production DeepSci skill named `isomer-deepsci-pipeline` under `skillset/research-paradigm/deepsci/isomer-deepsci-pipeline/`.

#### Scenario: Skill folder is present

- **WHEN** the production DeepSci research-paradigm skillset is inspected
- **THEN** it contains a folder named `isomer-deepsci-pipeline`
- **AND** the folder contains `SKILL.md` with valid YAML frontmatter including `name: isomer-deepsci-pipeline`
- **AND** the folder contains `agents/openai.yaml` with skill metadata

### Requirement: Pipeline passes are self-contained subcommand pages

The skill SHALL define each pass as a dedicated subcommand page under its `commands/` directory. Each page embeds the pass recipe as a readable table and describes any pass-specific behavior, entry context, and notes.

#### Scenario: Pass page is inspected

- **WHEN** a page under `isomer-deepsci-pipeline/commands/` is read
- **THEN** it contains a recipe table with stage order, skill, consumed artifacts, produced artifacts, continue condition, pause condition, and expensive flag
- **AND** each stage's skill value is an existing production DeepSci skill name

#### Scenario: Pass recipe is valid

- **WHEN** the skill validates a recipe before execution
- **THEN** every artifact id in the recipe appears either in the production DeepSci semantic-placeholder registry or in the producing or consuming skill's placeholder registry
- **AND** the first stage's consumed artifacts are empty or satisfied by the caller-provided context

### Requirement: Skill executes stages in order

When invoked with a pipeline name, the skill SHALL run the pass's stages sequentially from first to last.

#### Scenario: Normal execution

- **WHEN** the skill is invoked with `pipeline: empirical-pass` and valid initial context
- **THEN** it runs the first stage
- **AND** after each stage completes, it runs the next stage until the terminal stage finishes or a pause condition is met

#### Scenario: Stage failure blocks progression

- **WHEN** a stage emits a blocker record
- **THEN** the skill does not start the next stage
- **AND** it produces a terminal report with `status: blocked`

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

The skill SHALL ship with a catalog of common single-pass recipes covering empirical research, paper writing, review, rebuttal, and publication packaging.

#### Scenario: Catalog is inspected

- **WHEN** `isomer-deepsci-pipeline/commands/` is listed
- **THEN** it contains at minimum `empirical-pass.md`, `hypothesis-pass.md`, `paper-pass.md`, `revision-pass.md`, `rebuttal-pass.md`, `polish-pass.md`, `submission-pass.md`, and `list-passes.md`

#### Scenario: Recipe stages are bounded

- **WHEN** any shipped recipe is inspected
- **THEN** it contains no backward edges, loop constructs, or references to looping
- **AND** it names only production DeepSci skills as stages

### Requirement: DeepSci Pipeline Supports Authorized Run-To Control
The DeepSci pipeline SHALL preserve linear single-pass recipes while allowing the current agent to act as their external controller after explicit run-to authorization for a named target.

#### Scenario: DeepSci target lacks a producible input
- **WHEN** the selected pass or target lacks an input that an available DeepSci or platform owner can produce
- **THEN** the DeepSci pipeline's numbered workflow makes the bounded operation record `paused`, the missing placeholder or accepted ref, its producer route, and a resume point
- **AND** it offers run-to recovery rather than classifying the producible gap as a terminal blocker

#### Scenario: Run-to controller consumes a DeepSci terminal report
- **WHEN** an authorized pass completes or pauses with a recommended producer, repair, revision, or resume route inside the target closure
- **THEN** the current agent may invoke the recommended bounded skill or pass as the external controller
- **AND** it refreshes latest context and accepted records before advancing the internal plan
- **AND** the individual pass recipe remains linear and contains no backward edge or internal macro loop

#### Scenario: DeepSci target becomes ready
- **WHEN** the run-to controller produces every accepted input required by the original DeepSci target
- **THEN** it resumes and executes that target
- **AND** it stops after the target's acceptance and validation conditions are met

#### Scenario: DeepSci has no run-to authorization
- **WHEN** a DeepSci pipeline terminal report recommends a different macro action without an active target-scoped run-to grant
- **THEN** the pipeline surfaces the recommendation to the user or external controller
- **AND** it does not select the next macro action itself

### Requirement: DeepSci Run-To Preserves Wrapped Skill Boundaries
The DeepSci run-to controller SHALL preserve callbacks, latest-context preflight, worker-output policy, placeholder bindings, quality gates, resource checks, and blocker semantics for every wrapped skill.

#### Scenario: Controller advances to another pass
- **WHEN** run-to requires another DeepSci pass or focused production skill
- **THEN** that invocation receives the accepted outputs of completed prerequisites
- **AND** it applies its own begin and end callbacks, current-context checks, durable recording, and terminal reporting

#### Scenario: Controller reaches a protected or repeating route
- **WHEN** continuation requires a nondelegable Gate, a material research choice, an unauthorized resource change, or repeats a recovery route without producing new accepted state
- **THEN** the controller pauses with completed artifacts and a precise resume point
- **AND** it does not continue under the prior run-to grant until the boundary is resolved
