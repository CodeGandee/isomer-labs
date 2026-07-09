## ADDED Requirements

### Requirement: Core Packaged Skills Include Toolbox Manager
The packaged core system-skill group SHALL include `operator/isomer-op-toolbox-mgr` and materialize it with the rest of the core operator skills.

#### Scenario: Core manifest includes toolbox manager
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `operator/isomer-op-toolbox-mgr`
- **AND** `groups.core.skills` does not include `operator/isomer-op-toolbox-creator`
- **AND** the listed manager path resolves below the packaged system-skill root
- **AND** the listed manager directory contains `SKILL.md`

#### Scenario: Core materialization copies toolbox manager
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `operator/isomer-op-toolbox-mgr/SKILL.md`
- **AND** it receives the manager skill's directly linked command pages
- **AND** it does not receive `operator/isomer-op-toolbox-creator/`

#### Scenario: Packaged skill discovery returns toolbox manager
- **WHEN** code asks for manifest-relative skill paths for the `core` group
- **THEN** the result includes `operator/isomer-op-toolbox-mgr`
- **AND** the result does not include `operator/isomer-op-toolbox-creator`
- **AND** it keeps the manager path manifest-relative rather than deriving a repository checkout path
