## ADDED Requirements

### Requirement: Entrypoint Offers Target-Scoped Run-To Recovery
The operator entrypoint SHALL preserve its single initial route selection for ordinary tasks and SHALL offer target-scoped run-to recovery when the selected owner reports producible missing prerequisites.

#### Scenario: Selected owner reports missing prerequisites
- **WHEN** the entrypoint routes an ordinary concrete task to one owner
- **AND** that owner reports missing or stale inputs with available producer routes
- **THEN** the entrypoint's numbered workflow pauses before invoking those producers
- **AND** it presents the missing inputs, recommended recovery sequence, inclusive run-to option, next-prerequisite-only option, alternative-route option, and stop option

#### Scenario: User authorizes run-to across owners
- **WHEN** the user selects the inclusive run-to option for the original target
- **THEN** the entrypoint uses the agent's native planning tool to coordinate the target's prerequisite closure across the applicable owner skills
- **AND** it resumes and executes the original target after its prerequisites are satisfied
- **AND** it does not claim ownership of lower-level mutation performed by those owner skills

#### Scenario: Entrypoint run-to reaches a nondelegable boundary
- **WHEN** an owner reports a Gate, material ambiguity, or external authorization boundary during run-to traversal
- **THEN** the entrypoint pauses with completed evidence and the exact decision needed
- **AND** it does not reinterpret the original target request as blanket approval

### Requirement: Entrypoint Reports Recovery Posture
The operator entrypoint SHALL make the difference between an ordinary paused request and an authorized run-to traversal visible in its user-facing result.

#### Scenario: Ordinary request pauses
- **WHEN** the target has producible missing prerequisites and run-to is not authorized
- **THEN** Essential Output states that the target was not executed
- **AND** it names the missing inputs, recommended next step, recovery choices, and target resume point

#### Scenario: Run-to traversal finishes
- **WHEN** run-to satisfies the prerequisite closure and completes the original target
- **THEN** Essential Output leads with the target outcome
- **AND** it summarizes prerequisite owner work, important Runs or accepted refs, preserved Gates, and target validation without presenting each intermediate terminal report as a separate user action request
