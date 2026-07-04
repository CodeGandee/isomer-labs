## ADDED Requirements

### Requirement: Switch Identity Operator Skill Inventory
The operator skillset SHALL include `isomer-op-switch-identity` as the active operator skill for switching a Project Operator's working identity posture to a Topic Actor or Agent.

#### Scenario: Switch identity skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-op-switch-identity/` as an active operator skill folder
- **AND** the packaged system-skill assets contain `operator/isomer-op-switch-identity/`

#### Scenario: Manifest lists switch identity skill
- **WHEN** `skillset/manifest.toml` or the packaged system-skill manifest is inspected
- **THEN** it lists `operator/isomer-op-switch-identity` in the core skill group

#### Scenario: Operator docs list switch identity skill
- **WHEN** a developer reads operator skillset documentation or welcome skill-map guidance
- **THEN** it lists `isomer-op-switch-identity`
- **AND** it describes the skill as the operator surface for switching to a selected Topic Actor or Agent workspace cwd

#### Scenario: Operator validation covers switch identity
- **WHEN** operator skill validation runs
- **THEN** it validates `isomer-op-switch-identity` frontmatter, UI metadata, command links, numbered workflow, freeform fallback, persistence-mode guidance, target workspace resolution guidance, cwd discipline, and provenance guardrails
- **AND** it fails if active switch-identity guidance claims OS-level impersonation, Agent Instance execution, Houmao launch, or directory-scanning target resolution
