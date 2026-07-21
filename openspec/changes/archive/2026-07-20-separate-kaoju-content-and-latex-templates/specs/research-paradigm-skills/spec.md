## ADDED Requirements

### Requirement: Kaoju Skills Use Content-Template and LaTeX-Template Terminology
Active Kaoju guidance SHALL call MyST-oriented template state a content template and LaTeX presentation state a LaTeX template whenever an actor or agent must select, create, update, export, inspect, or report one.

#### Scenario: Paper drafting selects a template
- **WHEN** Kaoju drafts canonical MyST
- **THEN** it resolves an explicit content template or content `main` and records its exact observed identity
- **AND** it does not resolve a LaTeX template during content-structure selection

#### Scenario: PDF construction selects a template
- **WHEN** Kaoju composes or builds TeX
- **THEN** it resolves an explicit LaTeX template or LaTeX `main` independently of the content template
- **AND** it reports both template identities in the terminal result

### Requirement: Kaoju Template Management Routes by Role
The `manage-paper-template` procedure SHALL resolve template role before applying named-template discovery, assessment, concurrency, exchange, and mutation rules.

#### Scenario: Explicit role and source are supplied
- **WHEN** the user supplies a LaTeX or content role plus a directory, record, export, or name
- **THEN** the agent validates and uses that role and locator directly
- **AND** it does not search the other role's exports or records

#### Scenario: Edited export is discovered
- **WHEN** an update omits a source but the selected role has exactly one eligible edited export
- **THEN** the agent selects that working directory and recorded target name
- **AND** same-named exports of the other role remain ineligible

### Requirement: Kaoju Skills Keep Presentation Repair Paper-Local
The write skill SHALL distinguish paper-specific TeX repair from stocked LaTeX-template mutation.

#### Scenario: Build repair succeeds
- **WHEN** a bounded presentation-only repair changes the derived TeX draft
- **THEN** the skill records the repair in TeX and build lineage and retries within authorization
- **AND** it does not update the stocked LaTeX template

#### Scenario: User promotes a repair
- **WHEN** the user explicitly asks to update the stocked LaTeX template from assessed edits
- **THEN** the skill routes through named LaTeX-template export or update with the current state token
- **AND** later paper composition must explicitly consume the new stock state
