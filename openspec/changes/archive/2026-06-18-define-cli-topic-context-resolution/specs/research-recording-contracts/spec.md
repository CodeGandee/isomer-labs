## ADDED Requirements

### Requirement: Minimal Artifact Core Record
The system SHALL keep the core Artifact record generic and minimal so topic-specific formats cannot fragment durable Artifact identity, lookup, or validation.

#### Scenario: Core artifact fields are minimal
- **WHEN** the system records the core fields for an Artifact
- **THEN** the core record contains only stable Artifact id, Topic Workspace id, Artifact kind, status, locator kind, locator, created timestamp, updated timestamp, and media type when known

#### Scenario: Core artifact locates content
- **WHEN** an Artifact points to project-local content or external content
- **THEN** the core record uses a locator kind and locator value to identify the file-backed or external content without embedding the rich content inline

#### Scenario: Core artifact does not require topic-specific format fields
- **WHEN** an Artifact is created without a matching Artifact Format Profile or Artifact Extension
- **THEN** the system can still list, locate, validate existence, display generically, and reference the Artifact through durable records

#### Scenario: Optional refs are attached outside core
- **WHEN** an Artifact needs lifecycle refs, producer refs, Run refs, Provenance Record refs, Evidence Item refs, supersession refs, format profile refs, extension refs, validation outcomes, or renderer hints
- **THEN** the system records those values through Artifact Link Records, metadata records, Provenance Records, or other accepted recording APIs rather than requiring them as core Artifact fields

### Requirement: Artifact Format Profiles
The system SHALL support optional Artifact Format Profiles for content-level expectations while preserving the generic Artifact Core Record.

#### Scenario: Format profile is optional
- **WHEN** a Research Topic, Research Task, Run, or command context selects an Artifact Format Profile for an expected output
- **THEN** the system records the selected profile as an optional format attachment or metadata ref for the Artifact and does not make the profile a mandatory core Artifact field

#### Scenario: Format profile describes content expectations
- **WHEN** an Artifact Format Profile is inspected
- **THEN** it may describe artifact kind applicability, media type expectations, schema refs, template refs, validation hints, renderer hints, export hints, opaque future capability refs, compatibility version, and status

#### Scenario: Format profile is declarative-only
- **WHEN** an Artifact Format Profile describes validation, rendering, export, or capability behavior
- **THEN** it does so with declarative metadata and opaque future capability refs, and does not define executable validators, renderers, exporters, command requests, provider contracts, or adapter-specific runtime behavior

#### Scenario: Format profile does not redefine core identity
- **WHEN** an Artifact Format Profile defines schema or template fields
- **THEN** validation rejects any profile field that shadows or redefines the Artifact id, Topic Workspace id, Artifact kind, status, locator kind, locator, or timestamps from the Artifact Core Record

#### Scenario: Unknown format profile is non-fatal
- **WHEN** a recorded Artifact references an Artifact Format Profile that is missing, unsupported, disabled, or unknown
- **THEN** validation reports the format issue while preserving generic Artifact lookup, path validation, provenance linking, and display behavior

### Requirement: Artifact Extensions
The system SHALL support optional Artifact Extensions for topic-specific metadata without changing the core Artifact record.

#### Scenario: Extension adds topic metadata
- **WHEN** a Research Topic enables an Artifact Extension
- **THEN** the extension may add topic-specific metadata fields, validation hints, or renderer hints for matching Artifacts

#### Scenario: Extension is additive only
- **WHEN** an Artifact Extension is validated
- **THEN** validation rejects extension fields that shadow, rename, or redefine core Artifact fields or accepted durable record refs

#### Scenario: Extension data is separable
- **WHEN** an Artifact has topic-specific extension data
- **THEN** the system records that data as an extension record, metadata record, sidecar Artifact, or other explicit attachment linked to the Artifact Core Record

#### Scenario: Missing extension is non-fatal
- **WHEN** an Artifact references an Artifact Extension that is missing, unsupported, disabled, or unknown
- **THEN** validation reports the extension issue while preserving generic Artifact lookup, path validation, provenance linking, and display behavior

### Requirement: Artifact Format Resolution
The system SHALL resolve Artifact Format Profiles and Artifact Extensions from the most specific expected-output context before falling back to topic or built-in defaults.

#### Scenario: Format resolution uses specificity order
- **WHEN** the system determines an Artifact Format Profile for an expected Artifact output
- **THEN** it checks explicit Run or command expected output, Research Task expected output, Research Topic Config defaults, Topic Agent Team Profile or Domain Agent Team Template defaults, and built-in Artifact kind defaults in that order

#### Scenario: Resolved format source is recorded
- **WHEN** an Artifact Format Profile or Artifact Extension is applied to an Artifact
- **THEN** the system records the selected ref and resolution source in an attachment, metadata record, or Provenance Record

#### Scenario: Format resolution does not execute commands
- **WHEN** a resolved Artifact Format Profile references validation, rendering, or export behavior that needs command execution
- **THEN** the system treats those references as opaque future capability refs and does not execute them through Research Recording Contracts
