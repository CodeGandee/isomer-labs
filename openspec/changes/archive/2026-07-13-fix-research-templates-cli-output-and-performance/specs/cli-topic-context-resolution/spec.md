## ADDED Requirements

### Requirement: Research Template Commands Use Task-Scoped Context Validation
The system SHALL resolve a valid Effective Topic Context for `isomer-cli ext research templates` using the Project and topic information required to select and operate on the target Topic Workspace, without validating unrelated Project capabilities that the selected template command does not consume.

#### Scenario: Template command validates required topic inputs
- **WHEN** any research-template subcommand resolves context
- **THEN** it validates Project discovery, Project Manifest topic registration, topic-selection precedence, the selected Research Topic Config identity, Topic Workspace mapping and path bounds, and the inputs required to open the selected Workspace Runtime

#### Scenario: Unrelated callback registries do not block template listing
- **WHEN** the Project or another Research Topic registers User Skill Callback material that the template command does not consume
- **THEN** `ext research templates list` does not load or validate that callback material while resolving its selected Topic Workspace
- **AND** callback count does not change the template command's context-validation work

#### Scenario: Unrelated capability validation remains available
- **WHEN** a caller runs Project validation, callback inspection, Toolbox inspection, Domain Agent Team Template inspection, or another command that consumes the skipped configuration
- **THEN** that command continues to use the full validation required by its own contract

#### Scenario: Consumed inputs are validated at use
- **WHEN** a template command creates, revises, compiles, or archives a template record
- **THEN** the record, file, Workspace Runtime, and artifact-format inputs consumed by that operation remain validated before mutation
- **AND** focused context resolution does not authorize a mutation after a required input fails validation
