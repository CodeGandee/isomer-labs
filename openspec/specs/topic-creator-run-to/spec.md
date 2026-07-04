# topic-creator-run-to Specification

## Purpose
TBD - created by archiving change add-topic-creator-finalize-summary. Update Purpose after archive.
## Requirements
### Requirement: Topic Creator Targeted Run-to Subcommand
The Topic Creator skill SHALL expose `run-to` as a targeted fast-forward mode that runs the main workflow until the predecessor of a user-specified procedural subcommand by default, and includes the target only on explicit inclusive request.

#### Scenario: Help lists run-to as targeted fast-forward
- **WHEN** `isomer-op-topic-creator help` runs or the skill is invoked without a prompt
- **THEN** the command list includes `run-to`
- **AND** the help text describes `run-to <procedural-subcommand>` as targeted fast-forward execution
- **AND** it explains that the target step is excluded by default unless the user explicitly asks for inclusive execution

#### Scenario: Run-to requires procedural target
- **WHEN** the user invokes `run-to` without a target procedural subcommand
- **THEN** Topic Creator reports that a procedural target is required
- **AND** it lists valid procedural targets from the main workflow
- **AND** it does not execute workflow steps

#### Scenario: Helper or misc target is rejected
- **WHEN** the user invokes `run-to` with a helper command, misc command, unknown command, or command outside the main workflow ladder
- **THEN** Topic Creator reports that `run-to` only accepts procedural main workflow targets
- **AND** it lists valid procedural targets
- **AND** it does not execute workflow steps

#### Scenario: Run-to excludes target by default
- **WHEN** the user invokes `run-to <procedural-subcommand>` without inclusive wording
- **THEN** Topic Creator runs the readiness ladder through the latest predecessor step that is in scope
- **AND** it does not execute the target step
- **AND** it reports that the target was excluded by default

#### Scenario: Run-to includes target when explicitly inclusive
- **WHEN** the user invokes `run-to` with wording such as `through <procedural-subcommand>`, `include <procedural-subcommand>`, or `<procedural-subcommand> inclusive`
- **THEN** Topic Creator follows the same readiness ladder and reuse rules as `fast-forward` through the named target step
- **AND** it executes the target step when its prerequisites and required inputs are available
- **AND** it stops after the target step completes, blocks, or reports skipped-by-scope status

#### Scenario: Run-to stops at predecessor missing input blocker
- **WHEN** a predecessor step required to reach the default stop boundary lacks required user input, source material, selected context, or semantic path resolution needed to run safely
- **THEN** Topic Creator stops at the blocked step
- **AND** it reports the missing input or unresolved dependency
- **AND** it does not skip the blocked step to reach a later target

#### Scenario: Inclusive run-to stops at target missing input blocker
- **WHEN** the user explicitly requests inclusive execution and the target step lacks required user input, source material, selected context, or semantic path resolution needed to run safely
- **THEN** Topic Creator stops at the target step
- **AND** it reports the missing input or unresolved dependency
- **AND** it does not treat the target as completed

#### Scenario: Run-to reuses ready predecessors
- **WHEN** earlier workflow steps already have valid readiness evidence
- **THEN** `run-to` validates and reuses those stages using the same rules as `fast-forward`
- **AND** it only creates, delegates, repairs, or executes missing stages needed to reach the target

#### Scenario: Inclusive run-to final target produces summary
- **WHEN** the user invokes `run-to finalize` with explicit inclusive wording and all predecessor stages are ready, skipped by explicit scope, or completed
- **THEN** Topic Creator runs `finalize` as the included target
- **AND** it writes `topic.workspace.summary`
- **AND** it stops after printing the final ready, verified, and blocked report without next-step routing

#### Scenario: Default run-to final target stops before summary
- **WHEN** the user invokes `run-to finalize` without inclusive wording
- **THEN** Topic Creator runs the readiness ladder through the latest in-scope predecessor before `finalize`
- **AND** it does not run `finalize`
- **AND** it does not write or refresh `topic.workspace.summary`

