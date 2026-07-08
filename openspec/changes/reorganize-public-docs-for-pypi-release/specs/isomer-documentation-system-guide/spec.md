## MODIFIED Requirements

### Requirement: Documentation Information Architecture
The system SHALL provide a coherent `docs/` documentation set with stable tutorial, manual, developer, and UI contract entry points for published users, operators, and contributors.

#### Scenario: Required docs pages exist
- **WHEN** repository documentation is validated
- **THEN** the docs tree includes entry pages for index, tutorial quickstart, installation, first Project, first Research Topic, Project Web GUI, system-skill installation, manual CLI reference, Project lifecycle, Research Topics, Topic Workspace definition, Workspace Runtime, research records, Project Web, Houmao adapter, troubleshooting, developer architecture, storage, packaged system skills, UI contracts, release process, testing, and contributing to docs

#### Scenario: Pages use section-appropriate tone
- **WHEN** a current docs page is moved into the new layout
- **THEN** it is rewritten for tutorial, manual, developer, or UI contract use rather than copied unchanged

#### Scenario: README points to detailed docs
- **WHEN** a reader opens `README.md`
- **THEN** it gives a concise published-tool orientation and links to tutorial, manual, and developer docs rather than duplicating the full system guide

#### Scenario: Public install path is distinct from developer setup
- **WHEN** docs show how to install Isomer Labs for ordinary use
- **THEN** they recommend installing the published CLI with `uv tool install isomer-labs`
- **AND** they keep Pixi checkout setup in developer docs

#### Scenario: System skill install path is documented
- **WHEN** docs show how to install Isomer system skills for an agent
- **THEN** they recommend `npx skills add` examples and distinguish core skills from DeepSci extension skills
