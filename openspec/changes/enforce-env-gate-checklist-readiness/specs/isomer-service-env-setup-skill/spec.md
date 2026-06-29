## MODIFIED Requirements

### Requirement: Environment Gate Verification
The service environment setup skill SHALL use a derived topic env target spec as the operational verification gate for Topic Workspace environment readiness. The target spec can come from `topic.env.topic_setup_target_spec`, derivation from `topic.intent.topic_env_requirements`, or explicit manual input.

#### Scenario: Source gate can derive target spec
- **WHEN** an agent uses `isomer-srv-topic-env-setup` for a Topic Workspace environment
- **THEN** the skill instructs the agent to resolve `topic.intent.topic_env_requirements`
- **AND** the skill treats the resolved file as the source of user intent for deriving `topic.env.topic_setup_target_spec` when no explicit target spec is supplied

#### Scenario: Missing gate file blocks readiness only when no target spec is supplied
- **WHEN** `topic.intent.topic_env_requirements` is missing or unreadable
- **AND** no explicit derived topic env target spec is supplied
- **THEN** the skill reports a blocker instead of claiming the Topic Workspace environment is ready
- **AND** it asks for `resolve-topic-env-gate` to create or repair the source gate, or for the caller to provide an explicit target spec, before final readiness verification

#### Scenario: Legacy source gate path is not canonical
- **WHEN** `<topic-workspace-dir>/user-intent/src/env-gate.md` exists but `<topic-workspace-dir>/intent/src/topic-env-gate.md` is missing
- **THEN** the skill reports a legacy-path blocker naming `topic.intent.topic_env_requirements` and its default-layout path
- **AND** it does not silently treat the legacy file as the canonical source gate

#### Scenario: Derived gate is generated from source intent
- **WHEN** `topic.intent.topic_env_requirements` is present and readable
- **AND** no explicit derived topic env target spec is supplied
- **THEN** the skill instructs the agent to generate `topic.env.topic_setup_target_spec`
- **AND** the generated gate preserves the source gate's user intent while converting it into operational environment-readiness checks based on the user requirement and any required repo contents

#### Scenario: Target spec uses fixed Markdown sections
- **WHEN** the skill generates or accepts a derived topic env target spec
- **THEN** the target spec includes top-level sections named `Source Intent`, `Gate Checklist`, `Runnable Target`, `Repo Requirements`, `Inferred Source Warnings`, `Dependency Plan`, `Resource Check Plan`, `Pixi Install Commands`, `Verification Commands`, `Expected Results`, `Blockers`, and `Execution Log`
- **AND** every section is present even when the section content is `None.` or a short reason that it does not apply

#### Scenario: Gate checklist records required readiness work
- **WHEN** the skill generates `topic.env.topic_setup_target_spec`
- **THEN** every required setup, repo, projection, dependency, resource, verification, expected-result, and blocker-resolution item needed for readiness is represented as a Markdown checkbox under `Gate Checklist`
- **AND** optional diagnostics or supporting smoke checks that are not required for readiness are recorded outside `Gate Checklist`

#### Scenario: Vague source gate is made operational
- **WHEN** the source gate is vague but understandable about what must be available or runnable after environment setup
- **THEN** the generated `isomer-env-gate.md` includes concrete required-to-succeed dependencies, Pixi install commands, Pixi run commands, scripts, imports, tools, expected outputs, checklist items, or equivalent pass/fail checks
- **AND** it establishes success criteria that another agent can execute or inspect without reinterpreting the vague source wording

#### Scenario: Target spec contents drive post-setup checks
- **WHEN** the target spec describes tools, libraries, repos, datasets, commands, scripts, imports, or other runnable checks expected after setup
- **THEN** the skill uses the derived `isomer-env-gate.md` expectations and `Gate Checklist` to select or report dependency installation commands and verification commands after Pixi setup
- **AND** readiness is reported only when every required checklist item is checked and backed by evidence that satisfies the expected result for that item

#### Scenario: Unchecked checklist item blocks readiness
- **WHEN** any required item under `Gate Checklist` remains unchecked after setup or verification
- **THEN** the skill does not report the Topic Workspace environment as ready
- **AND** it reports `blocked` when the item could not be run, `failed` when it ran and missed its expected result, or `not checked` only when verification was explicitly not requested
- **AND** it names the exact checklist item, reason, and next safe action in `Blockers`, `Execution Log`, or the final output

#### Scenario: Bounded real-path evidence can complete heavy checklist item
- **WHEN** a required checklist item names heavy work such as compilation, model inference, dataset processing, benchmark execution, large archive extraction, or a broad test suite
- **THEN** the skill may check the item only after a bounded real-path command exercises the same critical path named by the item and passes its expected result
- **AND** bounded real-path evidence may use reduced parallelism, selected build targets, tiny model or tensor shapes, sample data, reduced iterations, reduced batch size, selected tests, or short benchmark cases

#### Scenario: Unrelated smoke test cannot complete critical checklist item
- **WHEN** a required checklist item names a critical build, inference, dataset, benchmark, or repo-specific runtime path
- **THEN** the skill does not mark that item checked merely because a weaker smoke test passed
- **AND** generic import success, device visibility, Pixi install success, repository inspection, or path existence counts only for a checklist item that specifically asks for that smoke evidence

#### Scenario: User downgrade is explicit evidence
- **WHEN** the user explicitly instructs the agent to accept a weaker check instead of the original critical-path checklist item
- **THEN** the skill records the user instruction, original checklist item, weaker evidence, and resulting limitation in the execution log or blocker record
- **AND** it does not silently present the weaker check as proof that the original critical path passed

#### Scenario: Gate verification remains service-safe
- **WHEN** either gate file names checks that imply live agent launch, Agent Instance creation, unrelated runtime mutation, GUI operation, research decision authority, or Topic Agent Team Profile materialization
- **THEN** the skill reports those parts as out-of-scope blockers or non-readiness notes
- **AND** it verifies only the service-safe Topic Workspace environment setup portion
