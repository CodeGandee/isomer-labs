## ADDED Requirements

### Requirement: Structured Research Record Payloads
The system SHALL support validated JSON payloads as the authoritative content source for accepted structured research records created through the research records extension.

#### Scenario: Structured payload is authoritative
- **WHEN** a caller creates or updates a structured research record with a payload file and Artifact Format Profile
- **THEN** the stored record identifies the selected format profile ref when used, schema ref, template ref when used, source ref kinds, schema version when known, validation status, render status, payload digest, and generated Markdown locator when rendering succeeds
- **AND** later structured readers treat the stored payload as the source of truth instead of parsing generated Markdown prose

#### Scenario: Payload validation precedes accepted storage
- **WHEN** a caller submits a payload for an accepted structured research record
- **THEN** the system validates the payload through the generic artifact-format processing engine before storing the payload as accepted structured state

#### Scenario: Invalid payload does not create accepted structured record
- **WHEN** payload validation fails for a create request
- **THEN** the system returns deterministic validation diagnostics
- **AND** it does not create an accepted lifecycle record, accepted structured payload row, or generated Markdown view for that failed request

#### Scenario: Profile remains declarative
- **WHEN** the research record pipeline uses an Artifact Format Profile for validation or rendering
- **THEN** the profile supplies declarative schema refs, template refs, media type expectations, validation hints, and renderer hints
- **AND** the profile does not contain executable validators, renderers, exporters, command requests, provider contracts, or adapter-specific runtime behavior

#### Scenario: Plain path inputs are snapshotted for durable records
- **WHEN** a caller creates or updates an accepted structured research record with plain schema or template files
- **THEN** the system snapshots those files through the artifact-format processing engine before the durable record depends on them
- **AND** the stored structured payload state records generated `custom:` refs, source kind `file_snapshot`, digests, and provenance refs

### Requirement: Payload-first Research Record CRUD
The system SHALL expose payload-first validate, create, update, show, list, and render behavior through the transitional `isomer-cli ext research records` surface.

#### Scenario: Validate checks without mutation
- **WHEN** a caller runs `isomer-cli ext research records validate` with `--format-profile`, direct schema/template refs, or schema/template files and a payload file
- **THEN** the command validates the payload through the artifact-format processing engine and returns deterministic JSON diagnostics
- **AND** it does not mutate Workspace Runtime or write generated Markdown files

#### Scenario: Create records payload and lifecycle identity
- **WHEN** a caller runs `isomer-cli ext research records create` with record kind, format profile or schema/template inputs, payload file, and valid topic context
- **THEN** the command creates the lifecycle record and structured payload state in the selected Workspace Runtime as one accepted research record
- **AND** the command records placeholder, skill, producer, consumer, lifecycle refs, Topic Actor metadata, and provenance refs when provided

#### Scenario: Create does not render implicitly
- **WHEN** a caller creates a valid structured research record without `--render markdown`
- **THEN** the command stores the lifecycle record and structured payload state
- **AND** it does not write a generated Markdown view merely because the selected profile contains a Markdown template

#### Scenario: Update preserves identity
- **WHEN** a caller updates a structured research record with a valid replacement payload
- **THEN** the system preserves the lifecycle record id
- **AND** it stores the new payload digest, validation outcome, updated timestamp, rendered Markdown locator when rendered, and mutation provenance without silently rewriting prior provenance refs

#### Scenario: Show can separate payload and rendered body
- **WHEN** a caller shows a structured research record
- **THEN** the command can return lifecycle metadata, structured payload JSON, validation diagnostics, generated Markdown locator, and rendered body content as distinct fields

#### Scenario: List can filter structured records
- **WHEN** a caller lists research records
- **THEN** the command can filter or summarize records by format profile ref, schema ref, template ref, source kind, validation status, render status, placeholder, skill, record kind, status, producer, consumer, and lifecycle refs without parsing generated Markdown

#### Scenario: List returns bounded compact summaries by default
- **WHEN** a caller lists structured research records without requesting payload details
- **THEN** the command returns at most the most recent matching records according to `defaults.ext.research.records_list_limit` from the Project Manifest TOML
- **AND** when the Project Manifest does not set `defaults.ext.research.records_list_limit`, the built-in fallback limit is 20
- **AND** each row contains lifecycle identity and status fields plus compact structured metadata, including format refs, source kind, validation status, render status, payload digest, generated Markdown locator when known, placeholder, skill, producer, consumer, and core timestamps
- **AND** it omits full payload JSON, validation diagnostics, render diagnostics, and rendered Markdown content unless explicitly requested

#### Scenario: List limit is caller controlled
- **WHEN** a caller lists structured research records with an explicit limit
- **THEN** the command applies the requested limit to the ordered result set before returning records
- **AND** the explicit request overrides the Project Manifest default for that invocation

### Requirement: Generated Markdown Views
The system SHALL render Markdown artifacts from validated structured payloads through the generic artifact-format processing engine when Markdown rendering is explicitly requested.

#### Scenario: Valid payload renders Markdown
- **WHEN** a valid structured payload is created or updated with Markdown rendering requested through `--render markdown`
- **THEN** the system renders Markdown from the payload and resolved Jinja2 template through the artifact-format processing engine
- **AND** it stores the generated Markdown under the resolved durable semantic record surface
- **AND** it records the generated Markdown path, digest when available, template ref, template source kind, and render status with the structured payload state

#### Scenario: Durable render name comes from binding
- **WHEN** a structured research record create or update materializes a generated Markdown view for a placeholder-backed artifact
- **THEN** the default generated content name comes from the active placeholder binding row rather than the Artifact Format Profile
- **AND** an explicit CLI output name or path is accepted only when the binding permits an override
- **AND** the stored structured payload state records the final rendered path and naming source

#### Scenario: Standalone render preview prints when no output file is provided
- **WHEN** a caller runs a standalone research-record render command without an output file path
- **THEN** the command prints the rendered content to the console when rendering succeeds
- **AND** it does not rewrite the stored generated Markdown locator unless the caller explicitly requests durable view materialization

#### Scenario: Generated Markdown remains file-backed
- **WHEN** generated Markdown is produced for a structured research record
- **THEN** the lifecycle record may reference the generated Markdown through its content path for record inspection
- **AND** the structured payload remains the authoritative content source for structured readers

#### Scenario: Render failure is reported
- **WHEN** payload validation succeeds but Markdown rendering fails
- **THEN** the system reports deterministic render diagnostics
- **AND** it does not mark the structured payload as successfully rendered

#### Scenario: Stale generated view is diagnosable
- **WHEN** the generated Markdown no longer matches the stored payload digest, render digest, or render metadata
- **THEN** research record validation reports the generated view as stale without changing the payload or deleting the Markdown file

### Requirement: Direct Body Inputs Are Not Structured Outputs
The system SHALL exclude direct Markdown, inline body, and body-file authoring from the accepted structured research record path.

#### Scenario: Structured create rejects direct body source
- **WHEN** a caller creates an accepted structured research record with structured format inputs and supplies `--body` or `--body-file` instead of a payload file
- **THEN** the command returns a deterministic diagnostic explaining that the structured path requires a JSON payload
- **AND** it does not store an accepted structured payload or generated Markdown view

#### Scenario: Markdown is never parsed as payload
- **WHEN** a Markdown body or generated Markdown view exists for a research record
- **THEN** structured readers do not infer typed payload fields by scraping that Markdown

#### Scenario: Current generated artifacts are not migration inputs
- **WHEN** the structured record feature is implemented
- **THEN** the system does not require migration, import, backfill, or repair of current generated `isomer-content/` artifacts before accepting new structured records
