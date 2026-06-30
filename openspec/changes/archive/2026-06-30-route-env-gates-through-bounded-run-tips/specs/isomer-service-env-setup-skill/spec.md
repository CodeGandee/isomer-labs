## ADDED Requirements

### Requirement: Topic Env Gate Heavy Operations Use Bounded Run Tips First
The service environment setup skill SHALL require topic env gate derivation to consult `isomer-misc-bounded-run-tips` before inventing resource plans for heavy setup or verification work.

#### Scenario: Derivation routes heavy topic commands to bounded run tips first
- **WHEN** `derive-env-gate` converts source intent or an explicit target spec into `topic.env.topic_setup_target_spec`
- **AND** a setup or verification item involves compilation, deep model inference, full dataset download, large archive extraction, broad test suites, multi-process training, large GPU jobs, benchmark execution, or another resource-heavy operation
- **THEN** the generated `Resource Check Plan` identifies the operation as heavy
- **AND** the derivation first checks `isomer-misc-bounded-run-tips` for an applicable subcommand or recipe
- **AND** the generated gate records the selected bounded-run guidance source, probes, capacity signals, bounded command, expected result, and blocker condition

#### Scenario: Specific bounded run guidance is applied when available
- **WHEN** a heavy topic env operation matches a bounded-run tips subcommand such as `cuda-compile`
- **THEN** `derive-env-gate` applies that subcommand's relevant guidance in the generated `Resource Check Plan`, `Verification Commands`, `Expected Results`, and `Gate Checklist`
- **AND** the gate records the matched skill and subcommand name as evidence for the resource decision
- **AND** the gate does not duplicate the full reference guide when only the selected probes, limits, and command are needed

#### Scenario: Generic best-effort plan is explicit when no recipe exists
- **WHEN** a heavy topic env operation has no matching `isomer-misc-bounded-run-tips` subcommand
- **THEN** `derive-env-gate` creates a generic bounded real-path plan that balances system resource utilization and crash prevention
- **AND** the gate records that the source is generic best-effort judgment
- **AND** the plan still exercises the source-intent build, inference, dataset, benchmark, or test path with bounded scope rather than replacing it with an unrelated smoke test

#### Scenario: Install and verify enforce the derived bounded plan
- **WHEN** `install-topic-deps` or `verify-env-gate` encounters a required heavy command from `topic.env.topic_setup_target_spec`
- **THEN** it uses the generated `Resource Check Plan` and matching checklist item as the execution contract
- **AND** it reports a blocker when the bounded-run plan is missing, ambiguous, unsafe, or cannot exercise the required path
- **AND** it does not mark readiness ready from an unrelated smoke test or an unrecorded full-scale command
