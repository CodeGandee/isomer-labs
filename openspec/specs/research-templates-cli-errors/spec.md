# research-templates-cli-errors Specification

## Purpose
TBD - created by archiving change fix-research-templates-cli-ux-and-performance. Update Purpose after archive.

## Requirements

### Requirement: Unknown commands under research extension groups show context-sensitive examples
The CLI SHALL provide usage examples that match the active research extension group when a user invokes an unknown subcommand or passes invalid options under `isomer-cli ext research templates`, `isomer-cli ext research records`, or `isomer-cli ext research ideas`.

#### Scenario: Unknown command under templates
- **WHEN** the user runs `isomer-cli ext research templates <unknown>`
- **THEN** the error diagnostic includes examples such as `isomer-cli --print-json ext research templates create --name main` and `isomer-cli --print-json ext research templates list`

#### Scenario: Unknown command under records
- **WHEN** the user runs `isomer-cli ext research records <unknown>`
- **THEN** the error diagnostic includes examples such as `isomer-cli --print-json ext research records list --topic my-topic` and `isomer-cli --print-json ext research records show <record-id> --topic my-topic`

#### Scenario: Unknown command under ideas
- **WHEN** the user runs `isomer-cli ext research ideas <unknown>`
- **THEN** the error diagnostic includes examples such as `isomer-cli --print-json ext research ideas list --topic my-topic` and `isomer-cli --print-json ext research ideas graph --topic my-topic`
