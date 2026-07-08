## ADDED Requirements

### Requirement: Placeholder Bindings Name Artifact Lineage
Production DeepSci placeholder binding pages SHALL describe expected canonical lineage metadata for structured records that derive from, revise, select, merge, or follow up prior records.

#### Scenario: Binding row expects parents
- **WHEN** a placeholder binding describes a record that is normally produced from prior artifacts, evidence, decisions, runs, or route state
- **THEN** the binding guidance names the expected parent record refs, parent roles, lineage kind, and whether a generation group is expected

#### Scenario: Binding row expects revision behavior
- **WHEN** a placeholder binding describes a current-state snapshot, selected hypothesis, draft, route decision, or paper-facing artifact that may be revised
- **THEN** the binding guidance states whether agents should use record revision, create a follow-up child, or update only metadata/status

#### Scenario: Binding row separates lineage from relationship hints
- **WHEN** a structured record also needs evidence refs, file refs, claim refs, citations, or GUI facets
- **THEN** the binding guidance distinguishes canonical lineage inputs from optional `--relationships-json`, `--files-json`, and `--index-hints-json`

### Requirement: Idea-stage Bindings Preserve Generation Groups
Idea-stage placeholder bindings SHALL preserve enough lineage information to reconstruct candidate siblings and selected paths.

#### Scenario: Candidate frontier is recorded
- **WHEN** an agent records a candidate idea frontier
- **THEN** the binding guidance requires parent refs to the raw slate or source evidence and a generation group for serious candidates when separate candidate records are created

#### Scenario: Selected hypothesis is recorded
- **WHEN** an agent records a selected hypothesis
- **THEN** the binding guidance requires lineage parents for the selected candidate or pre-idea draft and the decision record that selected it

#### Scenario: Rejected and deferred ideas are recorded
- **WHEN** an agent records rejected or deferred ideas
- **THEN** the binding guidance preserves their shared parent set or generation group so future agents can see they were siblings of the selected route
