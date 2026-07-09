## ADDED Requirements

### Requirement: Structured Payload Display Validation
The artifact-format validation engine SHALL validate `title` and `summary` as required display fields for supported `structured-record.v2` DeepSci structured research payloads.

#### Scenario: DeepSci v2 payload validates display fields
- **WHEN** a caller validates a DeepSci `structured-record.v2` payload through a resolved format profile or direct schema ref
- **THEN** validation requires non-empty top-level `title` and `summary` strings
- **AND** the validation result identifies the schema ref, payload digest, and display-field validation status

#### Scenario: DeepSci v1 payload is unsupported for normal writes
- **WHEN** a normal write path resolves a DeepSci `structured-record.v1` schema ref or v1-backed profile
- **THEN** artifact-format processing reports that the schema version is unsupported for accepted new records
- **AND** validation, repair, or migration code may still inspect v1 payloads as legacy input

#### Scenario: Missing display field reports schema diagnostic
- **WHEN** a payload omits `title`, omits `summary`, or supplies either field as an empty string
- **THEN** validation fails with a deterministic diagnostic that includes the JSON path and failing keyword when available
- **AND** the diagnostic uses `summary` as the canonical brief display field name

#### Scenario: Render templates use summary
- **WHEN** a Jinja2 template renders a supported structured research payload for display
- **THEN** the template uses `summary` for the brief display description
- **AND** shipped DeepSci templates do not require `one_liner` for accepted structured record rendering

### Requirement: Structured Payload Idea Display Validation
DeepSci schemas that contain idea-bearing sections SHALL validate the display fields for accepted idea entries.

#### Scenario: Idea-bearing entry validates display fields
- **WHEN** a structured payload profile declares a section that can create, select, reject, defer, merge, subsume, or follow up Research Ideas
- **THEN** each accepted idea entry in that section has non-empty `title` and `summary` strings
- **AND** validation reports a structured diagnostic for any entry that lacks either field

#### Scenario: Context notes are not idea display fields
- **WHEN** a payload contains filter notes, route context, report summaries, or provenance sections near idea-bearing entries
- **THEN** validation does not treat those context fields as replacements for the idea entry's own `title` and `summary`
