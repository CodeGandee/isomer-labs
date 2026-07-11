# artifact-format-processing Specification

## Purpose
TBD - created by archiving change establish-structured-research-records. Update Purpose after archive.
## Requirements
### Requirement: Artifact Format Ref Naming
The system SHALL use origin-prefixed hierarchical refs for Artifact Format Profiles, JSON Schemas, and Jinja2 templates that distinguish Isomer-owned formats from user-registered formats.

#### Scenario: Ref follows canonical pattern
- **WHEN** a format profile, schema, or template ref is recorded or resolved
- **THEN** the ref follows the pattern `{isomer,custom}:<topic-or-extension-slug>/<primary-group>/<subgroup>/.../<template-name>`

#### Scenario: Isomer-owned ref is explicit
- **WHEN** a format is shipped or registered by Isomer package code or an Isomer extension
- **THEN** its ref begins with `isomer:` and uses the extension or package slug as the first path segment

#### Scenario: Custom ref is explicit
- **WHEN** a format is registered by a user into a selected Topic Workspace
- **THEN** its ref begins with `custom:` and uses the topic slug or an explicitly selected topic-local slug as the first path segment

#### Scenario: DeepScientist format uses Isomer origin
- **WHEN** the DeepScientist extension provides a record format
- **THEN** the profile, schema, and template refs are under `isomer:deepsci/record-format/*`

#### Scenario: DeepScientist initial bundle covers active v2 outputs
- **WHEN** the first DeepScientist record-format provider bundle is implemented
- **THEN** active v2 accepted-output placeholder families for run, evidence, decision, handoff/control, figure, report, paper, Nature-specific, presentation, and finalization records resolve to explicit `isomer:deepsci/record-format/*` profiles
- **AND** reusable family schemas or templates may be shared only when each placeholder still resolves to an explicit profile with deterministic schema and template refs

### Requirement: Artifact Format Resolution
The system SHALL resolve Artifact Format Profiles, schema refs, and template refs through a provider registry that is independent of any one research extension.

#### Scenario: Registered provider resolves ref
- **WHEN** a caller requests a profile, schema, or template ref with an origin and path supported by a registered provider
- **THEN** the artifact-format engine resolves the ref to content, digest metadata when available, source kind, and diagnostics

#### Scenario: Missing ref reports diagnostic
- **WHEN** no registered provider can resolve a requested profile, schema, or template ref
- **THEN** the engine returns a deterministic missing-ref diagnostic and does not guess from filenames or Markdown bodies

#### Scenario: Profile points to schema and template refs
- **WHEN** an Artifact Format Profile is resolved
- **THEN** the engine can read its declarative schema ref, template refs by output format, media type expectations, validation hints, renderer hints, compatibility version, and status

#### Scenario: Profile remains declarative
- **WHEN** a profile is resolved
- **THEN** the profile does not execute Python validators, renderers, exporters, command requests, provider calls, or adapter-specific runtime behavior

### Requirement: JSON Schema Payload Validation
The system SHALL validate JSON payloads against resolved JSON Schemas through a generic artifact-format validation engine.

#### Scenario: Payload validates against profile schema
- **WHEN** a caller validates a payload with a resolved format profile that names a schema ref
- **THEN** the engine validates the payload with `jsonschema` and returns validation status, diagnostics, schema ref, schema digest when available, and payload digest

#### Scenario: Payload validates against direct schema ref
- **WHEN** a caller validates a payload with a direct schema ref and no format profile
- **THEN** the engine validates the payload with the resolved schema and returns deterministic validation output

#### Scenario: Invalid payload reports schema diagnostics
- **WHEN** the payload does not satisfy the selected schema
- **THEN** the engine returns deterministic diagnostics that identify the schema ref or schema file, JSON path when available, failing keyword when available, and human-readable message

#### Scenario: Validation does not mutate runtime by default
- **WHEN** a caller runs an artifact-format validation command
- **THEN** validation does not mutate Workspace Runtime unless the caller explicitly performs a registration, snapshot, or durable record operation

### Requirement: Jinja2 Artifact Rendering
The system SHALL render artifacts from JSON payloads through resolved Jinja2 templates.

#### Scenario: Payload renders with profile template
- **WHEN** a caller renders a payload with a resolved format profile and output format such as `markdown`
- **THEN** the engine resolves the profile-selected Jinja2 template, renders it with the payload, and returns rendered content, template ref, template digest when available, payload digest, and render diagnostics

#### Scenario: Payload renders with direct template ref
- **WHEN** a caller renders a payload with a direct template ref and no format profile
- **THEN** the engine resolves the template ref and renders it with the payload

#### Scenario: Render failure reports diagnostic
- **WHEN** the selected template cannot be loaded or rendering fails
- **THEN** the engine returns deterministic diagnostics and does not return the rendered artifact as successful

#### Scenario: Jinja2 template extension is conventional
- **WHEN** Isomer-owned or custom Markdown render templates are stored as files
- **THEN** Markdown Jinja2 templates use the `.md.j2` extension

### Requirement: Topic-registered Artifact Formats
The system SHALL allow users to register custom Artifact Format Profiles, JSON Schemas, and Jinja2 templates for a Topic Workspace.

#### Scenario: User registers custom format
- **WHEN** a caller registers a custom format with a `custom:` format profile ref, schema file, template file, and output format
- **THEN** the system copies or snapshots the assets into managed Topic Workspace runtime storage
- **AND** it records refs, original source paths when known, digests, timestamps, actor refs when known, validation diagnostics, and provenance refs

#### Scenario: Custom ref resolves from runtime storage
- **WHEN** a caller resolves a `custom:` profile, schema, or template ref for a selected Topic Workspace
- **THEN** the engine resolves the ref from Workspace Runtime registration state and managed snapshots rather than arbitrary mutable source paths

#### Scenario: Custom registration is topic scoped
- **WHEN** a caller resolves a `custom:` ref in the first release
- **THEN** resolution is limited to the selected Effective Topic Context and selected Topic Workspace
- **AND** the engine does not search a Project-level shared custom registry

#### Scenario: Duplicate custom ref is rejected without update flag
- **WHEN** a caller registers a custom format ref that already exists in the selected Topic Workspace without an explicit update or replace request
- **THEN** the system rejects the registration and preserves the existing registration

#### Scenario: Invalid custom registration is rejected
- **WHEN** the schema file, template file, profile metadata, or ref shape is invalid during registration
- **THEN** the system reports deterministic diagnostics and does not create an accepted custom format registration

### Requirement: Plain Path Artifact Format Inputs
The system SHALL support plain schema and template path inputs for ad hoc validation and rendering while snapshotting those inputs before durable record creation depends on them.

#### Scenario: Plain path validation is ad hoc
- **WHEN** a caller validates a payload with `--schema-file`
- **THEN** the engine reads the schema file for that command, validates the payload, returns diagnostics and digests, and does not require prior registration

#### Scenario: Plain path rendering is ad hoc
- **WHEN** a caller renders with `--schema-file`, `--template-file`, and `--payload-file`
- **THEN** the engine reads those files for that command, validates and renders when validation succeeds, and does not require prior registration

#### Scenario: Durable record snapshots plain paths
- **WHEN** a caller creates or updates a durable structured record using plain schema or template files
- **THEN** the system snapshots the schema and template into managed Workspace Runtime storage
- **AND** it records generated `custom:` refs, source kind `file_snapshot`, original source paths when known, digests, and provenance refs

#### Scenario: Durable record does not depend on mutable plain path
- **WHEN** a durable structured record was created from plain schema or template paths
- **THEN** later validation and rendering use the recorded snapshot refs and digests rather than rereading the original plain paths

### Requirement: Artifact Format CLI and API
The system SHALL expose generic CLI and Python API surfaces for artifact-format validation, rendering, and custom registration.

#### Scenario: Generic validate command exists
- **WHEN** a caller runs `isomer-cli project artifact-formats validate`
- **THEN** the command accepts `--format-profile`, `--schema-ref`, or `--schema-file` with `--payload-file` and returns deterministic validation JSON when requested

#### Scenario: Generic render command exists
- **WHEN** a caller runs `isomer-cli project artifact-formats render`
- **THEN** the command accepts `--format-profile`, direct schema/template refs, or schema/template files with `--payload-file` and returns or writes rendered content with deterministic diagnostics

#### Scenario: Generic render prints when no output file is provided
- **WHEN** a caller runs `isomer-cli project artifact-formats render` without an output file path
- **THEN** the command prints the rendered content to the console when rendering succeeds
- **AND** when `--print-json` is used, the deterministic JSON response carries the rendered content and render diagnostics

#### Scenario: Generic render writes explicit output file
- **WHEN** a caller runs `isomer-cli project artifact-formats render` with an output file path
- **THEN** the command writes the rendered content to that path when rendering succeeds
- **AND** it reports the output path and render diagnostics deterministically

#### Scenario: Generic register command exists
- **WHEN** a caller runs `isomer-cli project artifact-formats register`
- **THEN** the command registers a custom format for the selected Topic Workspace from profile metadata, schema file, template file, and output format

#### Scenario: Format profile flag is explicit
- **WHEN** new artifact-format commands or structured research-record commands accept an Artifact Format Profile ref
- **THEN** the documented flag is `--format-profile` rather than a bare `--profile`

### Requirement: On-demand Jinja2 Record Rendering
The artifact-format processing system SHALL render Markdown from structured payload files on demand through resolved Jinja2 templates.

#### Scenario: Record render reads payload file
- **WHEN** a caller requests Markdown for a structured research record
- **THEN** the renderer reads the managed JSON payload file, validates or checks its recorded digest, resolves the selected template, and returns rendered Markdown content

#### Scenario: Render does not create durable file by default
- **WHEN** a caller renders a structured research record as Markdown for display
- **THEN** the renderer returns content to the CLI, API, or GUI without writing a generated Markdown file unless the caller explicitly requests export

#### Scenario: Explicit export writes generated artifact
- **WHEN** a caller explicitly exports rendered Markdown to a file
- **THEN** the system records the export as a generated artifact with source record id, payload digest, template ref, template digest when known, output locator, output digest, and provenance refs

#### Scenario: Template remains a view transform
- **WHEN** a Jinja2 template renders structured research payload JSON
- **THEN** the template produces display content and does not define lifecycle identity, revision policy, query-index ownership, or durable payload storage

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

### Requirement: Family-Neutral Research Record Format Namespace
The Artifact Format system SHALL expose built-in family-neutral structured research format refs under `isomer:research/record-format/*`.

#### Scenario: Research profile ref identifies family and semantic id
- **WHEN** a built-in extension profile is recorded or resolved
- **THEN** its ref has the form `isomer:research/record-format/profile/<family>/<class>/<semantic-id>/v1`
- **AND** the resolved profile metadata identifies the same family, class, semantic id, compatibility version, and active status

#### Scenario: Shared schema and renderer have neutral refs
- **WHEN** the provider resolves its reusable JSON Schema or Markdown renderer
- **THEN** their refs use `isomer:research/record-format/schema/research-structured-record/v1` and `isomer:research/record-format/template/markdown/research-structured-record/v1`
- **AND** they do not use a DeepSci or Kaoju provider namespace

### Requirement: Family-Neutral Provider Uses Declarative Catalogs
The system SHALL register a built-in provider `isomer.research.record-formats` that loads explicitly packaged family profile catalogs.

#### Scenario: Kaoju catalog resolves through neutral provider
- **WHEN** the Kaoju built-in catalog declares an active semantic profile
- **THEN** the provider resolves that profile, its schema, and its Markdown template without registering a Kaoju-specific Python provider
- **AND** the resolution provenance identifies the neutral provider and Kaoju catalog entry

#### Scenario: Catalog entry declares profile behavior
- **WHEN** a family profile catalog entry is inspected
- **THEN** it declares family, semantic id, artifact class, compatible record kinds, required payload paths, relationship paths, file paths, facet paths, renderer, version, and status as data
- **AND** profile-specific validation or extraction does not require a hard-coded Python branch

#### Scenario: Catalog collisions fail deterministically
- **WHEN** two built-in catalogs declare the same canonical profile ref or one catalog mismatches its family or semantic id
- **THEN** provider registration fails with deterministic diagnostics naming both sources and the violated catalog rule

### Requirement: Neutral Structured Payload Validation and Rendering
The family-neutral provider SHALL validate and render canonical structured research payloads independently of the owning research family.

#### Scenario: Common fields validate
- **WHEN** a payload is validated against a neutral research profile
- **THEN** validation requires non-empty `title`, `summary`, `artifact_family`, `semantic_id`, `artifact_type`, and an object-valued `sections`
- **AND** family and semantic id must match the selected profile

#### Scenario: Declarative required paths validate
- **WHEN** the selected profile declares required payload paths
- **THEN** validation reports each missing or invalid path with the profile ref and JSON path
- **AND** the provider does not silently accept a payload solely because its common fields are valid

#### Scenario: Markdown is rendered on demand
- **WHEN** a caller renders a valid neutral structured payload as Markdown
- **THEN** the shared renderer uses canonical display and section fields and reports the profile, schema, template, and payload digest
- **AND** rendering does not modify the payload or durable record

### Requirement: DeepSci Artifact Format Compatibility Is Preserved
The family-neutral provider SHALL coexist with the current DeepSci Artifact Format provider without changing DeepSci public refs or resolution behavior.

#### Scenario: Existing DeepSci profile still resolves
- **WHEN** any existing `isomer:deepsci/record-format/*` profile, schema, or template ref is resolved after the neutral provider is registered
- **THEN** it resolves through the DeepSci provider with the same compatibility, validation, and rendering behavior as before this change

#### Scenario: No automatic profile alias is introduced
- **WHEN** a caller supplies a DeepSci ref
- **THEN** the system does not rewrite it to `isomer:research/*`
- **AND** existing records retain their recorded DeepSci format refs

