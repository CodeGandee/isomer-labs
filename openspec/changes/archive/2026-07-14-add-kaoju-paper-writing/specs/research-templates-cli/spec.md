## ADDED Requirements

### Requirement: Research Templates CLI Namespace
The system SHALL expose `isomer-cli ext research templates` as a bounded CLI surface for discovering, generating, inspecting, refreshing, and removing derived paper-writing templates under `intent/derived/writing-template/`.

#### Scenario: Templates namespace is discoverable
- **WHEN** a user runs `isomer-cli ext research --help`
- **THEN** the help lists `templates` alongside `records` and `ideas`
- **AND** running `isomer-cli ext research templates --help` lists `create`, `list`, `show`, `refresh`, `compile`, and `remove`

#### Scenario: Template commands require topic context
- **WHEN** a user runs any `isomer-cli ext research templates` command
- **THEN** the command resolves a Project and Topic Workspace through the same options used by `isomer-cli ext research records`
- **AND** it returns a deterministic error when no Topic Workspace can be resolved

### Requirement: Create Generates or Revises a Template
The `create` command SHALL generate a LaTeX template tree, compile a proof-of-compilation PDF preview, and record template metadata as a durable research record.

#### Scenario: Create default template
- **WHEN** a user runs `isomer-cli ext research templates create` without `--name`
- **THEN** the command generates or revises the `main` template under `intent/derived/writing-template/main/`
- **AND** it writes `.tex` entry point, bibliography stub, style and included files, and `README.md`
- **AND** it compiles a preview PDF using the Tectonic-first LaTeX workflow
- **AND** it creates or updates a research record of kind `artifact` with semantic-id `kaoju:writing-template` and profile `kaoju:writing-template`
- **AND** the record payload stores `template_name` (`main`), `venue`, `paper_type`, `tex_entry`, `preview_pdf_ref`, `source` (`generated`), `engine_posture`, and `status`
- **AND** it returns the template name, record id, file refs, and preview build status

#### Scenario: Create named template
- **WHEN** a user runs `isomer-cli ext research templates create --name <name>`
- **THEN** the command generates or revises the named template under `intent/derived/writing-template/<name>/`
- **AND** it records the template separately from `main`
- **AND** it returns the named template ref

#### Scenario: Create from an existing template record
- **WHEN** a user runs `isomer-cli ext research templates create --from-record <record-id>`
- **THEN** the command copies the source files and posture from the referenced template record
- **AND** it creates a new template revision with those files as parents
- **AND** it does not silently overwrite an unrelated template

#### Scenario: Create fails when preview cannot compile
- **WHEN** the generated LaTeX source cannot compile to a preview PDF
- **THEN** the command returns a non-zero exit code with compile log, diagnostic, and repair hint
- **AND** it records the failed preview build but does not mark the template record as `ready`

### Requirement: List Templates
The `list` command SHALL return the templates available in the selected Topic Workspace, distinguishing the default `main` template from named templates.

#### Scenario: List shows default and named templates
- **WHEN** a user runs `isomer-cli ext research templates list`
- **THEN** the command queries research records by semantic-id `kaoju:writing-template`
- **AND** it returns each template's name, record id, status, venue, paper type, preview build status, and last updated timestamp
- **AND** it marks the template named `main` as the default

#### Scenario: List filters by venue or paper type
- **WHEN** a user runs `isomer-cli ext research templates list --venue <venue>` or `--paper-type <type>`
- **THEN** the command returns only matching templates
- **AND** it still marks `main` as the default when it matches the filter

### Requirement: Show One Template
The `show` command SHALL return metadata and a file tree for one template.

#### Scenario: Show default template
- **WHEN** a user runs `isomer-cli ext research templates show` without `--name`
- **THEN** the command resolves the `main` template
- **AND** it returns the record metadata, file tree, preview PDF ref, and README content

#### Scenario: Show named template
- **WHEN** a user runs `isomer-cli ext research templates show --name <name>`
- **THEN** the command resolves the named template
- **AND** it returns the same details as for `main`

### Requirement: Refresh Revises a Generated Template
The `refresh` command SHALL regenerate a template's files from current inputs while preserving the user's intent and creating a new record revision.

#### Scenario: Refresh default template
- **WHEN** a user runs `isomer-cli ext research templates refresh`
- **THEN** the command regenerates the `main` template files under `intent/derived/writing-template/main/`
- **AND** it compiles a new preview PDF
- **AND** it creates a descendant research record with lineage to the prior template record
- **AND** it returns the new record id

#### Scenario: Refresh preserves user edits optionally
- **WHEN** a user runs `isomer-cli ext research templates refresh --preserve-edits`
- **THEN** the command regenerates only files that the user has not modified since the last generation
- **AND** it records which files were preserved and which were refreshed

### Requirement: Compile Re-runs the Preview Build
The `compile` command SHALL re-run the proof-of-compilation PDF preview without regenerating LaTeX source.

#### Scenario: Compile default template preview
- **WHEN** a user runs `isomer-cli ext research templates compile`
- **THEN** the command compiles the current `main` template files
- **AND** it updates the preview PDF ref and build status on the template record
- **AND** it does not create a new template record revision unless the build status changes

### Requirement: Remove Archives a Template
The `remove` command SHALL archive the template record and optionally remove derived files.

#### Scenario: Remove archives but preserves files by default
- **WHEN** a user runs `isomer-cli ext research templates remove --name <name>`
- **THEN** the command archives the template record
- **AND** it leaves files under `intent/derived/writing-template/<name>/` in place
- **AND** it updates `paper-pass` resolution so the removed template is no longer the latest accepted ref

#### Scenario: Remove with file deletion
- **WHEN** a user runs `isomer-cli ext research templates remove --name <name> --delete-files`
- **THEN** the command archives the template record and removes the template directory
- **AND** it records the removal in provenance

### Requirement: Template Records Are Research Records
Template metadata SHALL be stored through the same transitional research record surface as other research records so that lineage, query, and provenance remain uniform.

#### Scenario: Template record is queryable
- **WHEN** a user runs `isomer-cli ext research records list --semantic-id kaoju:writing-template`
- **THEN** the command returns the same template records as `isomer-cli ext research templates list`

#### Scenario: Template record carries provenance
- **WHEN** a template is created, refreshed, or removed
- **THEN** the system records a Provenance Record linking actor, command, inputs, outputs, and the template record id
