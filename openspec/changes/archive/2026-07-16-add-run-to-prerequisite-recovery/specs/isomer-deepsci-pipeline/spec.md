## ADDED Requirements

### Requirement: DeepSci Pipeline Supports Authorized Run-To Control
The DeepSci pipeline SHALL preserve linear single-pass recipes while allowing the current agent to act as their external controller after explicit run-to authorization for a named target.

#### Scenario: DeepSci target lacks a producible input
- **WHEN** the selected pass or target lacks an input that an available DeepSci or platform owner can produce
- **THEN** the DeepSci pipeline's numbered workflow makes the bounded operation record `paused`, the missing placeholder or accepted ref, its producer route, and a resume point
- **AND** it offers run-to recovery rather than classifying the producible gap as a terminal blocker

#### Scenario: Run-to controller consumes a DeepSci terminal report
- **WHEN** an authorized pass completes or pauses with a recommended producer, repair, revision, or resume route inside the target closure
- **THEN** the current agent may invoke the recommended bounded skill or pass as the external controller
- **AND** it refreshes latest context and accepted records before advancing the internal plan
- **AND** the individual pass recipe remains linear and contains no backward edge or internal macro loop

#### Scenario: DeepSci target becomes ready
- **WHEN** the run-to controller produces every accepted input required by the original DeepSci target
- **THEN** it resumes and executes that target
- **AND** it stops after the target's acceptance and validation conditions are met

#### Scenario: DeepSci has no run-to authorization
- **WHEN** a DeepSci pipeline terminal report recommends a different macro action without an active target-scoped run-to grant
- **THEN** the pipeline surfaces the recommendation to the user or external controller
- **AND** it does not select the next macro action itself

### Requirement: DeepSci Run-To Preserves Wrapped Skill Boundaries
The DeepSci run-to controller SHALL preserve callbacks, latest-context preflight, worker-output policy, placeholder bindings, quality gates, resource checks, and blocker semantics for every wrapped skill.

#### Scenario: Controller advances to another pass
- **WHEN** run-to requires another DeepSci pass or focused production skill
- **THEN** that invocation receives the accepted outputs of completed prerequisites
- **AND** it applies its own begin and end callbacks, current-context checks, durable recording, and terminal reporting

#### Scenario: Controller reaches a protected or repeating route
- **WHEN** continuation requires a nondelegable Gate, a material research choice, an unauthorized resource change, or repeats a recovery route without producing new accepted state
- **THEN** the controller pauses with completed artifacts and a precise resume point
- **AND** it does not continue under the prior run-to grant until the boundary is resolved
