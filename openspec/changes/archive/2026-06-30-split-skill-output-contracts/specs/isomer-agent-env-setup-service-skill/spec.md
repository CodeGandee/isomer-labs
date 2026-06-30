## ADDED Requirements

### Requirement: Agent Env Setup Uses Essential and Complete Output
The Agent Workspace environment setup service skill SHALL split its output contract into Essential Output and Complete Output.

#### Scenario: Essential agent env output reports user-facing readiness
- **WHEN** `isomer-srv-agent-env-setup` reports a result without a complete-output request
- **THEN** it reports the selected topic, Topic Workspace predecessor status, Topic Main Development Repository predecessor status, Agent Workspace readiness summary, readiness by agent or selected-agent partial status, critical verification result, blockers, and next action
- **AND** it makes selected-agent partial evidence visibly partial when overall readiness is not proven

#### Scenario: Complete agent env output preserves handoff detail
- **WHEN** complete output is requested from `isomer-srv-agent-env-setup`
- **THEN** it reports requester and confirmation source, semantic paths, source and target spec labels and paths, topic env predecessor refs, projection predecessor evidence, full Agent Workspace path and branch plan, full readiness matrix, operation classification evidence, resource probes, commands run, changed files, blockers, and next action

#### Scenario: Complete output includes matrix scope
- **WHEN** complete output includes per-agent verification evidence
- **THEN** it names the affected Agent Name or matrix scope for each readiness, blocker, operation classification, and resource check entry
