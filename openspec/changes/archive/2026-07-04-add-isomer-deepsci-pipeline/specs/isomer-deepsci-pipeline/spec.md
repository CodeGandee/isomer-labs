# isomer-deepsci-pipeline Specification

## Purpose

Define the `isomer-deepsci-pipeline` production DeepSci skill, which executes named single-pass recipes that chain other production DeepSci skills with automatic artifact handoffs while preserving each wrapped skill's gate discipline.

## ADDED Requirements

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
