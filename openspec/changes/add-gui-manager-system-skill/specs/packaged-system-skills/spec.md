## ADDED Requirements

### Requirement: Core Packaged Skills Include GUI Manager
The packaged core system-skill group SHALL include `operator/isomer-op-gui-mgr` and materialize it with the rest of the core operator skills.

#### Scenario: Core manifest includes GUI manager
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `operator/isomer-op-gui-mgr`
- **AND** the listed path resolves below the packaged system-skill root
- **AND** the listed directory contains `SKILL.md`

#### Scenario: Core materialization copies GUI manager
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `operator/isomer-op-gui-mgr/SKILL.md`
- **AND** it receives the GUI manager skill's directly linked reference pages

#### Scenario: Packaged skill discovery returns GUI manager
- **WHEN** code asks for manifest-relative skill paths for the `core` group
- **THEN** the result includes `operator/isomer-op-gui-mgr`
- **AND** it keeps the path manifest-relative rather than deriving a repository checkout path
