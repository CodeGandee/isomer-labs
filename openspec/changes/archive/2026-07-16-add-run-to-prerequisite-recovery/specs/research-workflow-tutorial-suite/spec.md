## ADDED Requirements

### Requirement: Tutorials Teach Prerequisite Recovery and Run-To
The research-workflow tutorial suite SHALL teach the conservative missing-prerequisite interaction and the explicit run-to option alongside the existing human-steered workflow.

#### Scenario: Tutorial target lacks prerequisites
- **WHEN** a tutorial example asks an agent to perform a target whose accepted inputs are missing
- **THEN** the example AI response pauses before prerequisite mutation
- **AND** it names the missing inputs, recommended producer sequence, run-to choice, next-prerequisite-only choice, alternative-route choice, and stop choice

#### Scenario: User chooses run-to
- **WHEN** a tutorial user responds with `run to <task>`, “automate everything,” “yes to all,” or equivalent target-scoped authorization
- **THEN** the example shows the agent planning and executing transitive prerequisites through their owner skills before resuming the target
- **AND** it explains that routine prerequisite prompts are suppressed only inside that target closure

#### Scenario: Run-to reaches a Gate
- **WHEN** the tutorial traversal reaches a human Gate, material research choice, destructive action, unexpected resource request, or external publication boundary
- **THEN** the example shows the agent pausing with completed refs and the exact required decision
- **AND** it explains that run-to does not bypass nondelegable boundaries

#### Scenario: Tutorial distinguishes run-to from Control Mode
- **WHEN** a tutorial explains run-to semantics
- **THEN** it describes run-to as prompt-scoped prerequisite recovery for one target
- **AND** it does not present run-to as a new Run-level Control Mode, global yes-to-all setting, or CLI command
