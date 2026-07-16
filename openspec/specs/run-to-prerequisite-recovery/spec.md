# run-to-prerequisite-recovery Specification

## Purpose
TBD - created by syncing completed OpenSpec changes.

## Requirements

### Requirement: Controlling Workflows Expose Prerequisite Recovery
The system SHALL place expected prerequisite preflight and recovery-choice handling in the numbered workflow of each controlling skill and SHALL keep detailed run-to semantics in directly linked active references when they do not fit concisely in the workflow.

#### Scenario: Controlling skill is inspected
- **WHEN** `isomer-op-entrypoint`, `isomer-kaoju-pipeline`, or `isomer-deepsci-pipeline` is inspected
- **THEN** its numbered `## Workflow` includes required-input preflight, ordinary pause and recovery-choice presentation, and the explicit transition into authorized run-to execution
- **AND** the workflow points to the active reference that defines target closure, status classification, and nondelegable boundaries

#### Scenario: Procedure page declares predecessor artifacts
- **WHEN** an active command or procedure page can encounter missing predecessor artifacts
- **THEN** its numbered workflow checks those artifacts before target execution
- **AND** it returns a producible gap to the controlling recovery contract with producer and resume information

#### Scenario: Troubleshooting guidance is inspected
- **WHEN** an editor considers where to place the expected missing-prerequisite branch
- **THEN** the branch remains in workflow and linked recovery guidance rather than relying on a generic `## Troubleshooting Guide` entry
- **AND** troubleshooting remains reserved for concrete execution failures with corrective actions under the existing troubleshooting format

### Requirement: Missing Prerequisites Pause Before Recovery Mutation
The system SHALL preflight the requested target's required artifacts and inputs before target execution and SHALL pause before mutating prerequisite state when an ordinary task request lacks a required input.

#### Scenario: Ordinary target request has a producible prerequisite gap
- **WHEN** the user requests `do <task>` without run-to authorization
- **AND** preflight finds a missing or stale prerequisite with a known in-scope producer
- **THEN** the system does not execute prerequisite mutation or begin the target operation
- **AND** it reports the target as paused with the missing input, producer route, and resume point

#### Scenario: Requested target is already ready
- **WHEN** preflight finds that the target's required inputs are current and accepted
- **THEN** the system executes the target through its owning skill or CLI surface without presenting prerequisite recovery choices

### Requirement: Recovery Prompt Presents Recommended Choices
The system SHALL explain the recoverable dependency closure and present a user choice before satisfying prerequisites for an ordinary task request.

#### Scenario: Recovery choices are presented
- **WHEN** a requested target pauses for one or more producible prerequisites
- **THEN** the response identifies the missing inputs and an ordered recommended recovery route
- **AND** it offers to run through all recommended prerequisites and execute the target, execute only the recommended next prerequisite, inspect or choose another recovery route, or stop
- **AND** it marks the safest complete recovery choice as recommended when the closure is sufficiently clear

#### Scenario: Multiple material recovery paths exist
- **WHEN** two or more prerequisite routes would materially change the target's research meaning, resource posture, or resulting scope
- **THEN** the system explains the material alternatives instead of selecting one under ordinary target authorization
- **AND** it asks the user to choose or refine the recovery route

### Requirement: Run-To Authorization Is Inclusive and Target Scoped
The system SHALL interpret an explicit run-to selection as authorization to execute the selected target's in-scope transitive prerequisite closure and then execute the original target.

#### Scenario: User selects run-to from the recovery prompt
- **WHEN** the user chooses “run through all prerequisites and execute the target,” `run to <task>`, “automate everything,” “yes to all,” or a semantically equivalent offered choice
- **THEN** the agent creates and maintains an internal plan ending at the named target
- **AND** it invokes prerequisite owners in dependency order and resumes the original target when its required inputs become ready

#### Scenario: User supplies run-to authorization with the original request
- **WHEN** the user explicitly requests both automatic prerequisite satisfaction and execution of a named target
- **THEN** the system may begin the target-scoped prerequisite plan without first repeating the recovery choice prompt
- **AND** it still performs prerequisite discovery and reports any nondelegable boundary before crossing it

#### Scenario: Traversal discovers another routine prerequisite
- **WHEN** an authorized prerequisite owner discovers another routine, reversible, in-scope prerequisite needed for the same target closure
- **THEN** the agent adds that prerequisite to the current plan without requesting another routine confirmation
- **AND** it preserves the newly selected owner's own preflight, evidence, and validation requirements

#### Scenario: Target completes
- **WHEN** the original target meets its acceptance and validation conditions
- **THEN** run-to authorization ends
- **AND** the system does not execute unrelated work or stages after the target solely because they are recommended next actions

### Requirement: Run-To Preserves Owner and Run Boundaries
The system SHALL coordinate run-to recovery through existing owner skills and SHALL preserve separate durable execution and provenance boundaries for each prerequisite and target operation.

#### Scenario: Recovery crosses owner workflows
- **WHEN** satisfying the target requires multiple operator or extension owner skills
- **THEN** the agent invokes each owner under that owner's existing contract
- **AND** it preserves each required Research Task, Run, terminal report, Artifact, checkpoint, Gate, and provenance record rather than merging the traversal into one opaque Run

#### Scenario: Bounded procedure returns a recoverable terminal report
- **WHEN** a prerequisite procedure completes or pauses with a producer or repair route inside the authorized target closure
- **THEN** the run-to controller consumes its accepted refs and resume information
- **AND** it advances the plan or resumes the target without treating the bounded procedure's terminal report as a mandatory user-turn boundary

### Requirement: Run-To Stops at Nondelegable Boundaries
The system SHALL stop an authorized run-to traversal when continuation requires authority or information outside the target-scoped grant.

#### Scenario: Nondelegable Gate is reached
- **WHEN** continuation requires a human Gate, material goal change, destructive or irreversible action, credentials or restricted data, material license decision, unexpected resource authorization, public exposure, publication, submission, or a materially ambiguous choice
- **THEN** the system checkpoints completed work and pauses at that boundary
- **AND** it presents the exact decision or authorization required to resume the same target

#### Scenario: User interrupts traversal
- **WHEN** the user asks the agent to stop, changes the target, or revokes run-to authorization
- **THEN** the system stops starting new prerequisite work
- **AND** it reports completed refs and the current resume point without applying the former authorization to the new target

### Requirement: Recoverable Dependencies Are Not True Blockers
The system SHALL distinguish a prerequisite gap with an available in-scope producer from a blocker that requires an unavailable external state change.

#### Scenario: Known producer can satisfy the gap
- **WHEN** a required input is missing or stale and an available owner can produce or repair it within the current Project and policy boundaries
- **THEN** the target reports `paused` with recovery choices
- **AND** it does not present the condition as a terminal `blocked` outcome

#### Scenario: No in-scope recovery can change the state
- **WHEN** the target cannot progress without an external state change that no available authorized owner can perform
- **THEN** the system reports `blocked` with the external condition, affected target, and resume condition
