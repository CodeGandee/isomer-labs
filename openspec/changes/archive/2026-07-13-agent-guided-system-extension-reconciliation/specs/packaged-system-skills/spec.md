## ADDED Requirements

### Requirement: Core Packaged Skills Include System Skill Manager
The packaged core system-skill group SHALL include `operator/isomer-op-system-skill-mgr` so every complete Isomer operator installation can manage optional extensions.

#### Scenario: Core manifest includes manager
- **WHEN** the packaged system-skill manifest is inspected
- **THEN** the core group lists `operator/isomer-op-system-skill-mgr`
- **AND** the path resolves to a valid packaged skill directory

#### Scenario: Core installation projects manager
- **WHEN** the core group is installed or materialized
- **THEN** it includes the manager's `SKILL.md`, `agents/openai.yaml`, and directly linked references

#### Scenario: Core catalog exposes manager
- **WHEN** system-skill catalog listing runs
- **THEN** it reports `isomer-op-system-skill-mgr` as a core operator skill
- **AND** it does not classify the manager as an optional extension

### Requirement: Extension Catalog Supports Inventory Classification
The packaged system-skill catalog SHALL provide stable extension-family membership for explicit-root and live-inventory classification.

#### Scenario: Catalog maps extension members
- **WHEN** internal inspection classifies receipt records or inventory names
- **THEN** it derives each extension's entry skill and complete member set from package-owned catalog metadata
- **AND** agents do not maintain duplicate hard-coded member lists
