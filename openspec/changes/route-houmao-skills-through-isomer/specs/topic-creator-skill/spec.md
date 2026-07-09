## ADDED Requirements

### Requirement: Topic Creator Handles Houmao Integration Skips
The Topic Creator skill SHALL treat Houmao-backed Topic Service Master preparation as optional Project integration work governed by Project Manifest Houmao integration policy.

#### Scenario: Disabled integration skips service master preparation
- **WHEN** Topic Creator setup reaches a Houmao-backed Topic Service Master or Houmao-backed operator actor step and the Project disables Houmao integration
- **THEN** the skill records that Houmao-backed preparation was skipped
- **AND** it continues any non-Houmao topic readiness work that remains valid

#### Scenario: Skipped Houmao work is visible in final output
- **WHEN** Topic Creator finalization reports Topic Workspace readiness after skipping Houmao integration
- **THEN** Essential Output includes the skipped Houmao-backed preparation state and skip reason
- **AND** Complete Output includes the Project Manifest integration evidence used for the skip

#### Scenario: Enabled integration routes through service support
- **WHEN** Topic Creator setup reaches Houmao-backed Topic Service Master preparation and the Project enables Houmao integration
- **THEN** the skill routes the work through Isomer service support that obtains Houmao skill context from `isomer-cli`
- **AND** it does not directly require the user to install or invoke Houmao-owned system skills
