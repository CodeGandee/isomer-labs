## ADDED Requirements

### Requirement: Agent Env Gate Heavy Operations Use Bounded Run Tips First
The Agent Workspace environment setup service SHALL require agent env gate derivation to consult `isomer-misc-bounded-run-tips` before inventing resource plans for heavy per-agent cwd verification work.

#### Scenario: Derivation routes heavy per-agent commands to bounded run tips first
- **WHEN** `derive-agent-env-gate` converts source agent intent or an explicit target spec into `topic.env.agent_setup_target_spec`
- **AND** a per-agent cwd verification item involves compilation, deep model inference, full dataset download, large archive extraction, broad test suites, multi-process training, large GPU jobs, benchmark execution, or another resource-heavy operation
- **THEN** the generated `Resource Check Plan` identifies the operation as heavy
- **AND** the derivation first checks `isomer-misc-bounded-run-tips` for an applicable subcommand or recipe
- **AND** the generated gate records the selected bounded-run guidance source, probes, capacity signals, bounded command, affected Agent Name scope, expected result, and blocker condition

#### Scenario: Selected-agent partial checks keep their scope
- **WHEN** a heavy per-agent command would multiply across all authoritative Agent Workspaces
- **THEN** `derive-agent-env-gate` may use selected-agent partial coverage or another bounded real-path tactic only when it still exercises the required cwd command path
- **AND** the gate records the partial scope and the bounded-run guidance source
- **AND** selected-agent partial evidence is not enough for `overall_readiness_status: ready` unless every required authoritative Agent Name has equivalent passing evidence

#### Scenario: Generic best-effort plan is explicit when no recipe exists
- **WHEN** a heavy per-agent cwd operation has no matching `isomer-misc-bounded-run-tips` subcommand
- **THEN** `derive-agent-env-gate` creates a generic bounded real-path plan that balances useful verification against host crash prevention
- **AND** the gate records that the source is generic best-effort judgment
- **AND** the plan still exercises the source-agent required cwd command path rather than replacing it with an unrelated smoke test

#### Scenario: Agent verification enforces the derived bounded plan
- **WHEN** `verify-agent-env-gate` encounters a required heavy matrix command from `topic.env.agent_setup_target_spec`
- **THEN** it uses the generated `Resource Check Plan` and matching checklist item as the execution contract
- **AND** it reports a blocker when the bounded-run plan is missing, ambiguous, unsafe, or cannot exercise the required cwd path
- **AND** it does not mark an agent ready from an unrelated smoke test or mark all agents ready from selected-agent partial evidence
