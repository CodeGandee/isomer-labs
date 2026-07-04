# topic-creator-step-by-step Specification

## Purpose
TBD - created by archiving change add-topic-creator-finalize-summary. Update Purpose after archive.
## Requirements
### Requirement: Topic Creator Guided Step-by-Step Subcommand
The Topic Creator skill SHALL expose `step-by-step` as a guided execution mode that runs the same main workflow as `fast-forward` while pausing for user understanding, option resolution, and acknowledgement before each step.

#### Scenario: Help lists step-by-step as guided counterpart
- **WHEN** `isomer-op-topic-creator help` runs or the skill is invoked without a prompt
- **THEN** the command list includes `step-by-step`
- **AND** the help text describes `step-by-step` as the guided counterpart to `fast-forward`
- **AND** it explains that `step-by-step` proceeds through the main workflow one acknowledged step at a time

#### Scenario: Step-by-step uses main workflow order
- **WHEN** `step-by-step` starts for a new or partial topic
- **THEN** it follows the same main workflow order as `fast-forward`: topic input resolution, Project and Topic Workspace readiness, `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, `bootstrap-research`, and `finalize`
- **AND** it reuses ready stages and stops at blockers using the same readiness rules as `fast-forward`

#### Scenario: Each step begins with a preview
- **WHEN** `step-by-step` is about to run a workflow step
- **THEN** it first tells the user the step name, what the step is going to do, what inputs it will read, what artifacts or semantic labels it may write or update, whether it may mutate state, and what blockers can stop it
- **AND** it does not run the step until the user acknowledges the preview or selects an option that authorizes proceeding

#### Scenario: Multiple choices are shown as option table
- **WHEN** a step has multiple valid choices, unresolved decisions, or open questions that affect execution
- **THEN** `step-by-step` shows a Markdown table with option IDs such as `A`, `B`, and `C`
- **AND** each row explains what the option is, its pros, its cons, any related open questions, and whether it is the recommended choice
- **AND** the user can answer with the option ID or equivalent explicit instruction

#### Scenario: Recommended choice is explicit but not automatic
- **WHEN** `step-by-step` presents multiple options
- **THEN** it marks one option as recommended when enough context exists
- **AND** it explains why that choice is recommended
- **AND** it does not treat the recommendation as accepted until the user acknowledges or selects it

#### Scenario: No-choice step still requires acknowledgement
- **WHEN** a workflow step has no meaningful options
- **THEN** `step-by-step` presents the step preview and asks for acknowledgement to proceed
- **AND** it does not invent artificial choices solely to fill an option table

#### Scenario: User can pause or change direction
- **WHEN** the user declines acknowledgement, asks to pause, or chooses an option that changes the planned path
- **THEN** `step-by-step` stops or updates the planned stage according to the user's instruction
- **AND** it does not continue mutating later stages under the old plan

#### Scenario: Step-by-step ends with finalize
- **WHEN** every predecessor stage is ready, skipped by explicit scope, or completed under `step-by-step`
- **THEN** `step-by-step` runs `finalize` as the terminal step after user acknowledgement
- **AND** it prints the final ready, verified, and blocked report from `finalize`
- **AND** it does not route to `start-manual-research` or recommend a next research command

