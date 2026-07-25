## MODIFIED Requirements

### Requirement: Trial Execution Requires an Approved Plan
The system SHALL create `kaoju:method-trial-plan` and SHALL obtain human approval by default or explicit prompt-delegated agent approval before implementing or executing the claim-bearing trial.

#### Scenario: Plan is presented for human review by default
- **WHEN** trial prerequisites and the actor's selected data basis are known and the prompt has not delegated trial-plan review
- **THEN** the plan records source commit, environment ref, data path or generated-data contract, task, entry point, wrapper, metrics, expected outputs, resource boundary, adaptations, risks, and interpretation limit
- **AND** execution waits for the human Gate decision

#### Scenario: Prompt delegates bounded trial-plan review
- **WHEN** the current prompt explicitly delegates trial-plan review and execution for a named target with pinned inputs, resource and attempt bounds, and interpretation limits
- **THEN** the trial skill may review, revise, and approve the plan and execute it without another user turn
- **AND** it records the agent-review posture, prompt basis, approved plan ref, rationale, exact command request, resources, and Run provenance

#### Scenario: Reviewing actor requests plan changes
- **WHEN** the human actor or delegated agent review rejects or revises the plan
- **THEN** the system preserves the decision and plan revision history
- **AND** it does not execute until the current plan is approved

#### Scenario: Revised plan remains inside delegated scope
- **WHEN** a failed attempt requires a plan revision that remains within the prompt-delegated inputs, resource boundary, attempt bound, fidelity, and research meaning
- **THEN** delegated agent review may evaluate and approve that revision without a new user turn
- **AND** the repaired attempt remains a distinct Run with the prior failure preserved

#### Scenario: Revised plan crosses a protected boundary
- **WHEN** a proposed plan or repair needs credentials, restricted data, a material license decision, a source or meaning change outside the delegated target, unexpected resources, destructive action, or another protected authorization
- **THEN** the system pauses for the applicable owner-specific decision
- **AND** prompt-delegated trial review does not satisfy that protected boundary
