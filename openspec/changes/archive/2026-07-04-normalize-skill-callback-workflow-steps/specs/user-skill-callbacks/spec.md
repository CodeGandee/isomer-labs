## MODIFIED Requirements

### Requirement: Callback Resolution and Merge Order
The system SHALL resolve User Skill Callbacks deterministically from the active Project and topic context before a participating skill applies them through explicit owning-skill workflow steps.

#### Scenario: Exact skill and stage match
- **WHEN** callbacks are resolved for a participating system skill
- **THEN** resolution includes only active callback records whose target system skill name and callback stage match the requested skill and stage

#### Scenario: Scope precedence is deterministic
- **WHEN** both project-scoped and topic-scoped callbacks match the requested skill and stage
- **THEN** resolution orders the more specific topic-scoped callbacks ahead of project-scoped callbacks unless an accepted registry priority rule orders callbacks within the same scope

#### Scenario: Priority order is deterministic
- **WHEN** multiple active callbacks match within the same scope
- **THEN** resolution sorts them by configured priority and then by stable callback id as the tie breaker

#### Scenario: Resolve output includes diagnostics
- **WHEN** callback resolution skips an inactive callback, rejects a malformed callback, or observes a missing optional registry
- **THEN** the result includes deterministic diagnostics without treating unrelated invalid callback records as successful instruction material

#### Scenario: Begin stage applies before workflow work
- **WHEN** a participating skill resolves `begin` callbacks
- **THEN** the skill applies the resolved instructions from an explicit numbered workflow step after mandatory skill identity and context checks and before the first skill-specific workflow action

#### Scenario: End stage applies before completion
- **WHEN** a participating skill resolves `end` callbacks
- **THEN** the skill applies the resolved instructions from an explicit numbered workflow step after producing tentative workflow outputs and before final response, handoff, or marking the top-level workflow complete

#### Scenario: Callback resolution is not implicit hook injection
- **WHEN** a participating skill documents callback participation
- **THEN** callback resolution is described as explicit workflow work owned by that skill
- **AND** the system does not rely on ambient reminder prose or implicit hook injection to make agents run callbacks
