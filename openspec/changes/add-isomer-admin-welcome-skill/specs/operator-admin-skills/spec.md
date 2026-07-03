## ADDED Requirements

### Requirement: Welcome Operator Skill Inventory
The operator/admin skillset SHALL include `isomer-admin-welcome` as the user-facing action menu and path chooser for supported Isomer Labs operator workflows.

#### Scenario: Welcome skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-welcome/` as an active operator skill folder
- **AND** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-admin-welcome`

#### Scenario: Operator docs list welcome entrypoint
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-admin-welcome`
- **AND** it describes the skill as the action-oriented menu and path chooser that tells users what Isomer Labs can do and which owner skill to invoke directly

#### Scenario: Manifest includes welcome and excludes retired compatibility entries
- **WHEN** `skillset/manifest.toml` is inspected
- **THEN** it includes `operator/isomer-admin-welcome`
- **AND** it does not include `operator/isomer-admin-topic-prepare`
- **AND** it does not include `operator/isomer-admin-manual-research-session`

#### Scenario: Operator validation covers welcome
- **WHEN** operator skill validation runs
- **THEN** it validates the welcome skill with frontmatter, UI metadata, local-reference, workflow, subcommand, output-contract, read-only posture, active-owner routing, and retired-skill exclusion checks
