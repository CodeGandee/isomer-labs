## ADDED Requirements

### Requirement: Placeholder Bindings Declare Display Fields
Active production DeepSci placeholder binding pages SHALL instruct agents to author supported v2 structured payloads with canonical `title` and `summary` fields for payload roots and idea-bearing entries.

#### Scenario: Binding names payload display fields
- **WHEN** `placeholder-bindings.md` describes a structured payload-backed accepted artifact
- **THEN** the binding guidance names the supported v2 profile or schema and required top-level `title` and `summary` fields
- **AND** it describes `summary` as the brief display description consumed by records, query index, and GUI views

#### Scenario: Binding names idea entry display fields
- **WHEN** a binding describes an idea-producing structured profile
- **THEN** the binding guidance states that each idea-bearing entry must include non-empty `title` and `summary`
- **AND** it distinguishes those fields from aliases, source-local labels, route notes, filter notes, and provenance fields

#### Scenario: Binding avoids one-liner guidance
- **WHEN** a production DeepSci placeholder binding gives active create, update, import, or realization guidance
- **THEN** it does not instruct agents to author `one_liner` as an accepted display field
- **AND** any historical mention of `one_liner` is marked as legacy migration context

#### Scenario: Binding avoids v1 guidance for new writes
- **WHEN** a production DeepSci placeholder binding gives active create or update guidance for structured records
- **THEN** it does not instruct agents to use `structured-record.v1` or a v1-backed profile for new accepted records
- **AND** any v1 mention is marked as legacy validation, repair, or migration context

### Requirement: Placeholder Binding Validation Checks Display Guidance
The placeholder binding validation harness SHALL detect missing or stale display-contract guidance in active production DeepSci binding pages.

#### Scenario: Missing payload display guidance is reported
- **WHEN** validation inspects a structured payload binding without required top-level `title` and `summary` guidance
- **THEN** validation reports the skill, placeholder, and missing display-field guidance

#### Scenario: Missing idea display guidance is reported
- **WHEN** validation inspects an idea-producing binding without per-entry `title` and `summary` guidance
- **THEN** validation reports the skill, placeholder, profile, and missing idea display-field guidance

#### Scenario: Stale one-liner guidance is reported
- **WHEN** validation finds active production binding guidance that treats `one_liner` as the accepted display field
- **THEN** validation reports the stale guidance and directs the binding to use `summary`

#### Scenario: Stale v1 guidance is reported
- **WHEN** validation finds active production binding guidance that uses `structured-record.v1` for new accepted structured records
- **THEN** validation reports the stale guidance and directs the binding to use the supported v2 contract
