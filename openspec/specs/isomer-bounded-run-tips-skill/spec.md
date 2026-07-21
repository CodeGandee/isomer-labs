# isomer-bounded-run-tips-skill Specification

## Purpose
Defines the bounded-run tips misc skill contract for classifying resource risk and producing bounded execution guidance.
## Requirements
### Requirement: Bounded Run Tips Classifies Operation Resource Risk
The bounded-run tips misc skill SHALL own user-tunable classification of whether a requested operation needs bounded resource handling.

#### Scenario: Operation classification returns an auditable result
- **WHEN** an agent asks `isomer-misc-bounded-run-tips` to classify a setup, verification, benchmark, compile, inference, dataset, test, download, archive, or other operation
- **THEN** the skill returns a classification result of `light`, `heavy`, `unknown-risk`, or `not-applicable`
- **AND** the result includes the command or task, cwd when known, expected result, reason, relevant resource dimensions, and whether bounded execution guidance is required

#### Scenario: Classification is user-tunable
- **WHEN** a user edits `isomer-misc-bounded-run-tips` to change which operations count as heavy for their project or host
- **THEN** topic env setup, agent env setup, and topic team specialization consume the updated classification guidance through the misc skill
- **AND** core service skills do not override that decision with their own fixed heavy-operation category list

#### Scenario: Unknown-risk requires bounded handling or blocker
- **WHEN** bounded-run tips cannot confidently classify an operation as light or not-applicable
- **THEN** it may classify the operation as `unknown-risk`
- **AND** callers treat `unknown-risk` like heavy for resource-check and bounded-plan purposes until better evidence is available

#### Scenario: Classification examples are non-normative
- **WHEN** bounded-run tips lists examples such as CUDA compilation, model inference, broad tests, downloads, or benchmark scripts
- **THEN** the examples guide agents without limiting the user's ability to classify other operations as heavy or light

### Requirement: Bounded Run Tips Produces Bounded Execution Guidance After Classification
The bounded-run tips misc skill SHALL provide bounded real-path execution guidance for operations classified as `heavy` or `unknown-risk`.

#### Scenario: Heavy classification routes to matching recipe
- **WHEN** an operation classified as `heavy` or `unknown-risk` matches a bounded-run tips subcommand such as `cuda-compile`
- **THEN** the skill applies the matching recipe
- **AND** it reports the recipe name, probes, limits, bounded command, expected result, and blocker condition

#### Scenario: Heavy classification without recipe uses generic bounded judgment
- **WHEN** no bounded-run tips subcommand matches an operation classified as `heavy` or `unknown-risk`
- **THEN** the skill reports generic best-effort bounded guidance
- **AND** the guidance includes probes, limits, bounded command, expected result, blocker condition, and the limitation that no specific recipe matched

#### Scenario: Light classification does not need resource plan
- **WHEN** an operation is classified as `light`
- **THEN** the skill reports that a resource check plan is not required
- **AND** it still states the reason so callers can record why no bounded execution plan was generated

### Requirement: Bounded Guidance Preserves Pixi Wrapper Tool Shape
The bounded-run tips misc skill SHALL preserve Pixi-first command ordering when producing bounded commands for wrapper tools that execute target commands as subprocesses.

#### Scenario: Bounded profiler command keeps wrapper inside Pixi
- **WHEN** bounded-run tips produces a bounded command for a profiler, tracer, debugger, memory checker, or similar wrapper tool
- **THEN** the bounded command uses `pixi run <wrapper-tool> ... <target-command>` or the explicit manifest equivalent
- **AND** it does not use `<wrapper-tool> pixi run ...` unless local evidence proves that Pixi itself is the intended target process

#### Scenario: Bounded guidance lists representative wrapper tools
- **WHEN** bounded-run tips documents common mistakes or generic bounded guidance
- **THEN** it names representative wrapper tools such as `ncu`, `nsys`, `valgrind`, `gdb`, and `cuda-gdb`

### Requirement: Bounded Run Tips Is Protected Shared Support
The core public pack SHALL preserve logical capability `isomer-misc-bounded-run-tips` as protected shared member `bounded-run`.

#### Scenario: Protected bundle exists
- **WHEN** core pack assets are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-misc-bounded-run-tips/SKILL.md` exists
- **AND** its logical identity and release version remain valid

#### Scenario: Owning workflow requests bounded guidance
- **WHEN** a protected operator, service, or extension capability classifies a resource-heavy operation
- **THEN** it invokes `isomer-op-entrypoint->bounded-run` or includes the logical id through declared dependency closure
- **AND** the bounded-run capability preserves its existing risk classification and execution guidance

#### Scenario: Helper is not top-level
- **WHEN** ordinary host discovery runs
- **THEN** it does not list `isomer-misc-bounded-run-tips` as an independent user skill

