## ADDED Requirements

### Requirement: Core Packaged Skills Include Entrypoint
The packaged core system-skill group SHALL include `operator/isomer-op-entrypoint` and materialize it with the rest of the core operator, service, and misc skills.

#### Scenario: Core manifest includes entrypoint
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** `groups.core.skills` includes `operator/isomer-op-entrypoint`
- **AND** the listed path resolves below the packaged system-skill root
- **AND** the listed directory contains `SKILL.md`

#### Scenario: Core materialization copies entrypoint
- **WHEN** a caller materializes the `core` group to an empty target directory
- **THEN** the target receives `operator/isomer-op-entrypoint/SKILL.md`
- **AND** it receives the entrypoint's `agents/openai.yaml` and directly linked references

#### Scenario: Packaged skill discovery returns entrypoint
- **WHEN** code asks for manifest-relative skill paths for the `core` group
- **THEN** the result includes `operator/isomer-op-entrypoint`
- **AND** it keeps the path manifest-relative rather than deriving a repository checkout path
