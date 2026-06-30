## ADDED Requirements

### Requirement: Topic Workspace Manager Uses Essential and Complete Output
The Topic Workspace Manager operator skill SHALL split its output contract into Essential Output and Complete Output.

#### Scenario: Essential topic workspace output reports topology status
- **WHEN** `isomer-admin-topic-workspace-mgr` reports a result without a complete-output request
- **THEN** it reports the selected Research Topic, Topic Workspace, topic-main status, Agent Workspace path summary, local tmp posture summary, blockers, and next action
- **AND** it highlights unsafe topology problems that need operator attention

#### Scenario: Complete topic workspace output preserves semantic path detail
- **WHEN** complete output is requested from `isomer-admin-topic-workspace-mgr`
- **THEN** it reports semantic paths, path sources, readiness diagnostics, topic-main path evidence, `isomer-managed/` status, tmp posture, Agent Workspace paths, branch plan, boundary material paths, generated links, validation status, blockers, and next action
