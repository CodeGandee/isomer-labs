## ADDED Requirements

### Requirement: Kaoju Paper Operations Report Selected Context
Context-sensitive Kaoju named-template and TeX composition or build commands SHALL expose the compact selected Research Topic and Topic Workspace context used for each success or structured failure.

#### Scenario: Template success reports selected context
- **WHEN** a Kaoju template list, show, create, update, file, metadata, archive, delete, export-inspection, export, or validation operation succeeds
- **THEN** its machine-readable result includes selected Research Topic id, Topic Workspace id, Topic Workspace path, and relevant context selection source metadata
- **AND** it does not embed the full Effective Topic Context or unrelated Project configuration

#### Scenario: TeX composition and build report selected context
- **WHEN** `init-tex`, `tex-status`, or `build-pdf` returns a machine-readable success or structured failure
- **THEN** the result includes selected Research Topic id, Topic Workspace id, Topic Workspace path, and relevant context selection source metadata
- **AND** the metadata does not change the agent-fill obligations, paper-local repair boundary, or build Gate outcome

#### Scenario: Template not found names lookup context
- **WHEN** a Kaoju template operation returns `template_not_found` or an equivalent missing-template diagnostic
- **THEN** the structured failure identifies the Research Topic and Topic Workspace searched and their selection sources
- **AND** its corrective guidance names an explicit `--topic` selector when selecting the intended topic could resolve the failure

#### Scenario: Context metadata does not broaden lookup
- **WHEN** a selected Research Topic does not contain the requested template
- **THEN** the command reports failure for that selected context
- **AND** it does not search, read, export, or mutate templates in sibling registered Research Topics

#### Scenario: Default export remains on resolved exchange surface
- **WHEN** `ext kaoju paper template export` succeeds without an explicit `--target`
- **THEN** the result reports the export path resolved from the selected Topic Workspace writing-template exchange surface
- **AND** it does not substitute a Topic Actor Workspace, Agent Workspace, Topic Main repository, or process cwd
