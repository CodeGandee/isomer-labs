## ADDED Requirements

### Requirement: Core Packaged Skills Include Toolbox Manager
The packaged core system-skill group SHALL include `operator/isomer-op-toolbox-mgr` and materialize it with the rest of the core operator skills.

#### Scenario: Core manifest includes toolbox creator
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `operator/isomer-op-toolbox-mgr`
- **AND** the listed path resolves below the packaged system-skill root
- **AND** the listed directory contains `SKILL.md`

#### Scenario: Core materialization copies toolbox creator
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `operator/isomer-op-toolbox-mgr/SKILL.md`
- **AND** it receives the skill's directly linked reference pages

#### Scenario: Packaged skill discovery returns toolbox creator
- **WHEN** code asks for manifest-relative skill paths for the `core` group
- **THEN** the result includes `operator/isomer-op-toolbox-mgr`
- **AND** it keeps the path manifest-relative rather than deriving a repository checkout path
