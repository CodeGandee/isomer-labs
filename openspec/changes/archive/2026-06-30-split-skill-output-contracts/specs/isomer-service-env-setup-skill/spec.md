## ADDED Requirements

### Requirement: Topic Env Setup Uses Essential and Complete Output
The topic environment setup service skill SHALL split its output contract into Essential Output and Complete Output.

#### Scenario: Essential topic env output reports user-facing readiness
- **WHEN** `isomer-srv-topic-env-setup` reports a result without a complete-output request
- **THEN** it reports the selected topic, Topic Workspace, Pixi binding summary, readiness status, Topic Main Development Repository status, external repo projection summary, critical gate checklist result, important changed files, blockers, and next action
- **AND** it reports `per_agent_readiness_status: not checked` when Agent Workspace cwd readiness is relevant to the caller

#### Scenario: Complete topic env output preserves handoff detail
- **WHEN** complete output is requested from `isomer-srv-topic-env-setup`
- **THEN** it reports semantic paths, source and target spec labels and paths, path diagnostics, repo source details, dependency plan, enclosure records, operation classification evidence, resource probes, commands run, changed files, warnings, blockers, and next action

#### Scenario: Reference pages use parent output mode
- **WHEN** a topic env setup reference page reports through the parent output contract
- **THEN** it follows the parent skill's Essential Output by default and Complete Output on request
