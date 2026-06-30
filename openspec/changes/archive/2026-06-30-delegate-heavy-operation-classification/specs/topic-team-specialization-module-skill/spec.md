## ADDED Requirements

### Requirement: Topic Team Specialization Consumes Operation Classification Evidence
The Topic Team Specialization operator skill SHALL rely on delegated service outputs for operation classification and bounded-run evidence instead of defining heavy-operation categories itself.

#### Scenario: Operator requires classification evidence from topic env service
- **WHEN** Topic Team Specialization delegates Topic Workspace environment setup to `isomer-srv-topic-env-setup`
- **THEN** the operator output contract expects classification source, classification result, resource dimensions, bounded guidance when required, and blockers from the delegated service output
- **AND** the operator does not classify operations from a fixed heavy-operation category list before delegation

#### Scenario: Operator requires classification evidence from agent env service
- **WHEN** Topic Team Specialization delegates Agent Workspace environment setup to `isomer-srv-agent-env-setup`
- **THEN** the operator output contract expects per-agent or matrix-scope classification source, classification result, resource dimensions, bounded guidance when required, selected-agent partial scope when used, and blockers from the delegated service output
- **AND** the operator does not classify per-agent operations from a fixed heavy-operation category list before delegation

#### Scenario: Operator examples remain non-normative
- **WHEN** Topic Team Specialization documentation gives examples of operations that often need bounded handling
- **THEN** it states that `isomer-misc-bounded-run-tips` owns the classification decision
- **AND** it treats the examples as reader guidance rather than the definition of heavy operation
