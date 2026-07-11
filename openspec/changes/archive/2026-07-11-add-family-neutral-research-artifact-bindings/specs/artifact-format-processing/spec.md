## ADDED Requirements

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

