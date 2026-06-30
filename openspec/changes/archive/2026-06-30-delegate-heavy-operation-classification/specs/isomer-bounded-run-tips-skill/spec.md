## ADDED Requirements

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
