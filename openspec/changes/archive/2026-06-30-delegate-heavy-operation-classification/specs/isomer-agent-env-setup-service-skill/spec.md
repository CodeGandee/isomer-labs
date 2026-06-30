## ADDED Requirements

### Requirement: Agent Env Gate Delegates Operation Classification
The Agent Workspace environment setup service SHALL delegate per-agent cwd operation classification to `isomer-misc-bounded-run-tips` before deciding whether an agent env matrix item needs bounded handling.

#### Scenario: Derivation records per-agent classification evidence
- **WHEN** `derive-agent-env-gate` converts source agent intent or an explicit target spec into `topic.env.agent_setup_target_spec`
- **THEN** it asks `isomer-misc-bounded-run-tips` to classify each per-agent cwd verification operation whose resource cost affects readiness planning
- **AND** the generated gate records classification source, classification result, reason, resource dimensions, affected Agent Name or matrix scope, and whether bounded guidance is required

#### Scenario: Heavy and unknown-risk classifications require bounded matrix handling
- **WHEN** bounded-run tips classifies a per-agent cwd operation as `heavy` or `unknown-risk`
- **THEN** `derive-agent-env-gate` includes a `Resource Check Plan` entry with bounded-run guidance, a bounded real-path command, affected Agent Name scope, expected result, and blocker condition
- **AND** selected-agent partial coverage is labeled partial unless every authoritative Agent Name has equivalent passing evidence

#### Scenario: Light classification can skip bounded matrix handling
- **WHEN** bounded-run tips classifies a per-agent cwd operation as `light`
- **THEN** `derive-agent-env-gate` may record that no resource check plan is required for that operation
- **AND** the gate preserves the classification evidence and reason

#### Scenario: Agent env setup does not own heavy-operation list
- **WHEN** agent env setup documentation mentions examples of operations that may be resource-heavy across Agent Workspaces
- **THEN** the documentation states that bounded-run tips owns the classification decision
- **AND** it does not make the example list the normative definition of heavy operation
