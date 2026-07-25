## MODIFIED Requirements

### Requirement: Explore returns an agreed plan on consent
The explore subskill SHALL summarize the agreed plan and recommended public invocation, then use human confirmation by default or explicit prompt-delegated agent review before durable work begins.

#### Scenario: Plan summary
- **WHEN** no material ambiguity remains or the user signals proceed
- **THEN** the subskill returns a plan containing the selected command, scope, evidence strategy, output form, risks, and exact public invocation

#### Scenario: Human consent is the default
- **WHEN** the explore subskill proposes a plan and the current prompt has not delegated plan review and handoff
- **THEN** it asks the user for explicit confirmation
- **AND** it does not proceed to the selected command without that confirmation

#### Scenario: Prompt delegates plan review and handoff
- **WHEN** the current prompt explicitly asks exploration to review its own plan and proceed automatically to a named target
- **THEN** the subskill may validate and revise the plan and hand it to the selected command without another user turn
- **AND** it reports the agent-review posture, prompt basis, selected invocation, scope, and unresolved limitations

#### Scenario: Exploration finds material ambiguity
- **WHEN** a material goal, scope, evidence, resource, or target choice remains unresolved after the allowed clarification process
- **THEN** the subskill pauses even when plan review was delegated
- **AND** it does not use automated review to invent the missing user intent
