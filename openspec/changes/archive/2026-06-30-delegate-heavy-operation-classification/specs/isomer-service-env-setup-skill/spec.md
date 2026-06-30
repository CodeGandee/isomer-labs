## ADDED Requirements

### Requirement: Topic Env Gate Delegates Operation Classification
The service environment setup skill SHALL delegate setup and verification operation classification to `isomer-misc-bounded-run-tips` before deciding whether a topic env gate item needs a resource check plan.

#### Scenario: Derivation records classification evidence
- **WHEN** `derive-env-gate` converts source intent or an explicit target spec into `topic.env.topic_setup_target_spec`
- **THEN** it asks `isomer-misc-bounded-run-tips` to classify each setup or verification operation whose resource cost affects readiness planning
- **AND** the generated gate records classification source, classification result, reason, resource dimensions, and whether bounded guidance is required

#### Scenario: Heavy and unknown-risk classifications require bounded plan
- **WHEN** bounded-run tips classifies a topic env operation as `heavy` or `unknown-risk`
- **THEN** `derive-env-gate` includes a `Resource Check Plan` entry with bounded-run guidance, a bounded real-path command, expected result, and blocker condition
- **AND** the gate does not replace the source-intent operation with an unrelated smoke test

#### Scenario: Light classification can skip resource plan
- **WHEN** bounded-run tips classifies a topic env operation as `light`
- **THEN** `derive-env-gate` may record that no resource check plan is required for that operation
- **AND** the gate preserves the classification evidence and reason

#### Scenario: Topic env setup does not own heavy-operation list
- **WHEN** topic env setup documentation mentions examples of operations that may be resource-heavy
- **THEN** the documentation states that bounded-run tips owns the classification decision
- **AND** it does not make the example list the normative definition of heavy operation
