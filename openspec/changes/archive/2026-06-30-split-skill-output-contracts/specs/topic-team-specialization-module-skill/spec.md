## ADDED Requirements

### Requirement: Topic Team Specialization Uses Essential and Complete Output
The Topic Team Specialization operator skill SHALL split its output contract into Essential Output and Complete Output.

#### Scenario: Essential specialization output reports user-facing progress
- **WHEN** `isomer-admin-topic-team-specialize` reports a result without a complete-output request
- **THEN** it reports the selected Research Topic and Topic Workspace, registration status, selected Domain Agent Team Template, topic-team material status, topic environment status, agent environment status when checked, validation status, blockers, and next action
- **AND** it names important created or changed paths such as topic overview, copied team material, environment gates, and final summary when those paths exist

#### Scenario: Complete specialization output preserves handoff detail
- **WHEN** complete output is requested from `isomer-admin-topic-team-specialize`
- **THEN** it reports registration evidence, environment binding evidence, copied material paths, placeholder resolutions, source and target intent paths, delegated service outputs, semantic path evidence, Agent Workspace paths, tmp posture, validation details, deferrals, packet/profile inputs, blockers, and next action

#### Scenario: Delegated service output remains summarized by default
- **WHEN** topic or agent environment services return large output payloads during specialization
- **THEN** Essential Output summarizes their readiness, blockers, important paths, and next action
- **AND** Complete Output may include the full delegated service output or the complete field groups needed for handoff
