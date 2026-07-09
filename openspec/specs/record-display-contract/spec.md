# record-display-contract Specification

## Purpose
TBD - created by archiving change standardize-record-summary-contract. Update Purpose after archive.
## Requirements
### Requirement: Canonical Display Fields
The system SHALL use non-empty `title` and `summary` strings as the canonical display contract for accepted `structured-record.v2` Research Record payloads and idea-bearing payload objects.

#### Scenario: Structured record payload is accepted
- **WHEN** a create, update, import, repair-apply, or validation-acceptance path accepts a supported `structured-record.v2` Research Record payload
- **THEN** the payload root contains non-empty `title` and `summary` strings
- **AND** `summary` is interpreted as the brief display description for the record

#### Scenario: v1 payload usage is unsupported for new writes
- **WHEN** a normal create or update path receives a `structured-record.v1` payload or v1-backed profile
- **THEN** the system rejects the write with a deterministic unsupported-schema diagnostic
- **AND** v1 data may only be read by validation, repair, or migration code

#### Scenario: Idea-bearing payload object is accepted
- **WHEN** an idea-bearing payload object is used to create, update, import, realize, or preview a canonical Research Idea
- **THEN** the object contains non-empty `title` and `summary` strings
- **AND** those fields are the source display fields for the canonical idea unless an explicit repair plan changes them

#### Scenario: Legacy one-liner is not a normal write contract
- **WHEN** a normal write path receives an idea payload object with `one_liner` and without `summary`
- **THEN** the system rejects the object or marks it invalid with a deterministic diagnostic
- **AND** it does not silently treat `one_liner` as the accepted display contract outside migration or repair code

### Requirement: Display Contract Diagnostics
The system SHALL report display-field integrity problems without crashing CLI, API, or GUI read paths.

#### Scenario: Existing data is missing display fields
- **WHEN** validation, query export, graph read, timeline read, or idea detail read encounters existing data without a required `title` or `summary`
- **THEN** the response includes a deterministic diagnostic that names the missing field and affected record or idea
- **AND** the read path returns all safely interpretable data instead of crashing

#### Scenario: Display fields duplicate each other
- **WHEN** validation detects an accepted record or idea whose `title` and `summary` are identical after trimming whitespace
- **THEN** the system reports a warning diagnostic so the data can be repaired
- **AND** it does not invent a replacement summary during ordinary reads

#### Scenario: Recent display errors are queryable
- **WHEN** a Project Web or CLI read path records display-contract warnings or errors
- **THEN** the recent-error query capability exposes those warnings or errors with severity, code, message, and affected object refs

