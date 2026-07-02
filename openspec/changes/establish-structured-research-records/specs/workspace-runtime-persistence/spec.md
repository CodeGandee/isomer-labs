## ADDED Requirements

### Requirement: Structured Research Payload Persistence
Workspace Runtime SHALL persist structured research record payload state separately from generic lifecycle record identity while keeping both records topic scoped.

#### Scenario: Payload row links to lifecycle record
- **WHEN** a structured research record is stored
- **THEN** Workspace Runtime persists structured payload state linked to the lifecycle record id, Research Topic id, and Topic Workspace id
- **AND** the lifecycle record remains the durable identity for record kind, status, lifecycle refs, content path, and provenance refs

#### Scenario: Payload state stores validation and render refs
- **WHEN** Workspace Runtime stores structured payload state
- **THEN** it stores format profile ref when used, schema ref, schema version when known, schema source kind, template ref when known, template source kind, payload JSON, payload digest, validation status, validation diagnostics, render status, render diagnostics, rendered Markdown locator when known, rendered Markdown digest when known, timestamps, and provenance refs
- **AND** stored format refs follow the pattern `{isomer,custom}:<topic-or-extension-slug>/<primary-group>/<subgroup>/.../<template-name>`
- **AND** DeepScientist extension-owned formats use refs under `isomer:deepsci/record-format/*`

#### Scenario: Payload persistence is topic scoped
- **WHEN** a structured payload is written or read
- **THEN** Workspace Runtime validates that the payload, linked lifecycle record, Research Topic id, and Topic Workspace id all match the selected Effective Topic Context

#### Scenario: Reopen preserves structured payloads
- **WHEN** the process exits and the Workspace Runtime is reopened
- **THEN** previously stored structured payload state is recoverable with the same linked record id, format profile ref, schema ref, template ref, source kinds, payload digest, validation outcome, render outcome, rendered Markdown locator, and provenance refs

### Requirement: Topic Artifact Format Registration Persistence
Workspace Runtime SHALL persist custom Topic Workspace artifact-format registrations and file snapshots used by durable structured records.

#### Scenario: Custom format registration is stored
- **WHEN** a caller registers a custom Artifact Format Profile, JSON Schema, and Jinja2 template for a selected Topic Workspace
- **THEN** Workspace Runtime records the custom refs, managed snapshot paths, original source paths when known, digests, actor refs when known, timestamps, diagnostics, and provenance refs

#### Scenario: Plain path snapshot is stored
- **WHEN** a durable structured record uses plain schema or template files
- **THEN** Workspace Runtime records managed snapshots, generated `custom:` refs, source kind `file_snapshot`, original source paths when known, digests, actor refs when known, timestamps, and provenance refs

#### Scenario: Custom registration is topic scoped
- **WHEN** a custom artifact format registration is read or written
- **THEN** Workspace Runtime validates that the registration belongs to the selected Research Topic and Topic Workspace

#### Scenario: Project-level custom registry is deferred
- **WHEN** a caller attempts to resolve a `custom:` ref that is not registered in the selected Topic Workspace
- **THEN** Workspace Runtime reports a deterministic missing-ref diagnostic
- **AND** it does not fall back to a Project-level shared custom format registry in this release

#### Scenario: Reopen preserves custom format registrations
- **WHEN** the process exits and Workspace Runtime is reopened
- **THEN** registered custom format refs and file snapshot refs remain resolvable with the same digests and managed paths

### Requirement: Structured Payload Schema Preparation
Workspace Runtime SHALL prepare the storage needed for structured research payloads through idempotent schema setup.

#### Scenario: Runtime init prepares payload storage
- **WHEN** Workspace Runtime is initialized or reopened for a supported schema that includes structured research payloads
- **THEN** the runtime prepares the structured payload storage

#### Scenario: Unsupported schema blocks mutation
- **WHEN** a caller attempts to create or update a structured payload in a Workspace Runtime with an unsupported schema version
- **THEN** the command fails with a schema-version diagnostic
- **AND** it does not alter lifecycle records, structured payload state, or generated Markdown files

#### Scenario: Current content backfill is not required
- **WHEN** structured payload storage is prepared
- **THEN** Workspace Runtime does not require migration, import, backfill, or repair of current generated `isomer-content/` artifacts before accepting new structured records

### Requirement: Structured Payload Validation Diagnostics
Workspace Runtime validation SHALL report structured payload, schema, and generated view issues without deleting records or generated artifacts.

#### Scenario: Invalid stored payload is reported
- **WHEN** validation inspects a structured payload that no longer conforms to its recorded schema ref or schema version
- **THEN** validation reports the record id, format profile ref when known, schema ref, and validation diagnostics
- **AND** it keeps the lifecycle record and structured payload visible for repair or supersession

#### Scenario: Missing custom format snapshot is reported
- **WHEN** validation inspects a custom format registration or file snapshot whose managed schema or template file is missing
- **THEN** validation reports the missing snapshot and identifies the affected custom ref or structured payload record

#### Scenario: Missing rendered Markdown is reported
- **WHEN** a structured payload records a generated Markdown locator and the file is missing
- **THEN** validation reports the missing generated view and identifies the linked lifecycle record
- **AND** it does not delete the structured payload or lifecycle record

#### Scenario: Stale render digest is reported
- **WHEN** a generated Markdown file exists but its digest or render metadata no longer matches the stored structured payload state
- **THEN** validation reports the generated view as stale and leaves remediation to an explicit update or render operation

#### Scenario: Broken payload link is reported
- **WHEN** structured payload state points to a missing lifecycle record or to a lifecycle record outside the selected Topic Workspace
- **THEN** runtime validation reports the broken or cross-topic link and identifies the payload row

### Requirement: Structured Record Inspection
Workspace Runtime inspection APIs SHALL expose structured payload summaries for CLI and future GUI consumers without requiring Markdown parsing.

#### Scenario: List includes structured summary
- **WHEN** a caller lists or inspects research records through a structured-capable API
- **THEN** the response can include format profile ref, schema ref, template ref, source kind, validation status, payload digest, rendered Markdown locator, and render status for each returned structured record

#### Scenario: List defaults are bounded and compact
- **WHEN** Workspace Runtime serves a structured record list without an explicit limit or detail expansion
- **THEN** it returns at most the most recent matching records according to the effective list limit resolved from `defaults.ext.research.records_list_limit` in the Project Manifest TOML
- **AND** it uses 20 as the built-in fallback when the Project Manifest omits that setting
- **AND** it includes compact structured metadata rather than full payload JSON, validation diagnostics, render diagnostics, or rendered Markdown content

#### Scenario: Project default list limit is validated
- **WHEN** the Project Manifest contains `defaults.ext.research.records_list_limit`
- **THEN** Project validation accepts a positive integer value
- **AND** reports a deterministic diagnostic for missing, non-integer, zero, or negative values before using the setting

#### Scenario: Complex analysis can use runtime database directly
- **WHEN** a user needs complex ad hoc queries beyond the CLI filters and bounded list behavior
- **THEN** the Workspace Runtime database exposes the lifecycle and structured payload tables with stable indexed columns for direct read-only SQL inspection

#### Scenario: Show includes payload details
- **WHEN** a caller shows one structured research record with payload details requested
- **THEN** Workspace Runtime returns the linked lifecycle record, structured payload JSON, format refs, source kinds, validation diagnostics, render metadata, generated Markdown locator, and provenance refs in deterministic JSON fields

#### Scenario: Structured filters use runtime state
- **WHEN** a caller filters records by format profile ref, schema ref, template ref, source kind, validation status, rendered state, placeholder, or lifecycle refs
- **THEN** Workspace Runtime evaluates the filter from lifecycle and structured payload state rather than reading Markdown body contents
