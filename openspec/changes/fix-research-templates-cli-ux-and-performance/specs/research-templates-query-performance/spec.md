## ADDED Requirements

### Requirement: Template record lookup uses the query index
The CLI SHALL locate a writing-template record by semantic id and template name using the indexed query store instead of loading all lifecycle records.

#### Scenario: Show a named template
- **WHEN** the user runs `isomer-cli ext research templates show --name <name>`
- **THEN** the command resolves the record by querying the index for `semantic_id="kaoju:writing-template"` and matching `template_name` in record metadata

#### Scenario: Refresh a named template
- **WHEN** the user runs `isomer-cli ext research templates refresh --name <name>`
- **THEN** the command resolves the parent record via the indexed query path

#### Scenario: Compile a named template
- **WHEN** the user runs `isomer-cli ext research templates compile --name <name>`
- **THEN** the command resolves the record via the indexed query path

#### Scenario: Remove a named template
- **WHEN** the user runs `isomer-cli ext research templates remove --name <name>`
- **THEN** the command resolves the record via the indexed query path and excludes archived or blocked records
